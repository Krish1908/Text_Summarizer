FROM python:3.12-alpine

WORKDIR /app

# Required for some Python packages that compile native extensions
RUN apk add --no-cache \
    build-base \
    python3-dev

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Install OpenTelemetry instrumentation packages
RUN opentelemetry-bootstrap -a install && pip check

COPY . .

CMD [
    "opentelemetry-instrument", "gunicorn", "-w","3", "-k","uvicorn.workers.UvicornWorker", "main:app", "--bind","0.0.0.0:8000", "--access-logfile","-", "--error-logfile","-"]
