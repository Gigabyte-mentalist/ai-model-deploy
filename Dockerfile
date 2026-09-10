FROM python:3.11-slim

# Xavfsizlik: root emas, oddiy foydalanuvchi
RUN useradd -m -u 1000 appuser

WORKDIR /app

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/main.py .

# Model papkasi — volume shu yerga ulanadi
RUN mkdir -p /models && chown appuser:appuser /models

ENV MODEL_PATH=/models/model.joblib
ENV MODEL_VERSION=v2

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
