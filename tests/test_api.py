import os
os.environ["MODEL_PATH"] = "tests/test_model.joblib"

from fastapi.testclient import TestClient
from app.main import app, startup

startup()
client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_ready():
    r = client.get("/ready")
    assert r.status_code == 200


def test_predict_positive():
    r = client.post("/predict", json={"text": "zor sifat tavsiya qilaman"})
    assert r.status_code == 200
    assert r.json()["sentiment"] == "ijobiy"


def test_predict_negative():
    r = client.post("/predict", json={"text": "yomon sifat pul isrof"})
    assert r.status_code == 200
    assert r.json()["sentiment"] == "salbiy"


def test_predict_schema():
    r = client.post("/predict", json={"text": "test"})
    data = r.json()
    for field in ["text", "sentiment", "confidence", "version"]:
        assert field in data


def test_predict_bad_request():
    r = client.post("/predict", json={"wrong_field": "test"})
    assert r.status_code == 422
