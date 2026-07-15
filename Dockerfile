FROM python:3.12-alpine

WORKDIR /app

RUN apk add --no-cache \
    build-base \
    python3-dev

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN opentelemetry-bootstrap -a install && pip check

COPY . .

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost:8000/api/health || exit 1

CMD ["opentelemetry-instrument", "gunicorn", "-w", "3", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8000", "--access-logfile", "-", "--error-logfile", "-"]