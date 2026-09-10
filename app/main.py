import os, time, json, hashlib, logging
import joblib, redis
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("model-api")

MODEL_PATH = os.getenv("MODEL_PATH", "/models/model.joblib")
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
CACHE_TTL = int(os.getenv("CACHE_TTL", "3600"))
MODEL_VERSION = os.getenv("MODEL_VERSION", "v1")

app = FastAPI()
model = None
model_ready = False
cache = None


class Request(BaseModel):
    text: str


@app.on_event("startup")
def startup():
    global model, model_ready, cache
    model = joblib.load(MODEL_PATH)
    model_ready = True
    try:
        cache = redis.Redis(host=REDIS_HOST, port=6379, socket_timeout=2)
        cache.ping()
        log.info("Redis ulandi")
    except Exception as e:
        log.warning("Redis yoq: %s", e)
        cache = None
    log.info("Model tayyor, versiya: %s", MODEL_VERSION)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/ready")
def ready():
    if not model_ready:
        raise HTTPException(503, "Model yuklanmadi")
    return {"status": "ready", "version": MODEL_VERSION}


@app.post("/predict")
def predict(req: Request):
    if not model_ready:
        raise HTTPException(503, "Model tayyor emas")

    t0 = time.time()
    proba = model.predict_proba([req.text])[0]
    return {
        "text": req.text,
        "sentiment": "positive" if proba[1] > 0.5 else "salbiy",
        "confidence": round(float(max(proba)), 3),
        "latency_ms": round((time.time() - t0) * 1000, 1),
        "version": MODEL_VERSION,
    }
