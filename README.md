# AI Model Deployment

FastAPI asosidagi ML model xizmati, Docker bilan konteynerlashtirilgan.

## Arxitektura

Nginx (reverse proxy, rate limiting) → FastAPI (model) → Redis (kesh)

## Xususiyatlar

- Model volume orqali beriladi, image ichida emas
- Liveness va readiness probe'lar ajratilgan
- Non-root foydalanuvchi
- Memory va CPU cheklovlari
- Redis kesh (graceful degradation bilan)
- Canary deployment qo'llab-quvvatlanadi

## Ishga tushirish

```bash
docker compose up -d
curl -X POST http://localhost:8090/predict \
  -H "Content-Type: application/json" \
  -d '{"text":"juda zor mahsulot"}'
```
