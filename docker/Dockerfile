# Air-bot – multi-stage: Node (frontend) + Python (backend)
FROM node:22-alpine AS frontend
WORKDIR /app
COPY frontend/package.json frontend/package-lock.json* frontend/
RUN cd frontend && npm ci
COPY frontend frontend/
RUN cd frontend && npm run build

FROM python:3.12-slim AS builder
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
COPY pyproject.toml ./
RUN pip install --no-cache-dir build
COPY airbot ./airbot
COPY config ./config
RUN pip install --no-cache-dir -e . --target /install

FROM python:3.12-slim AS runtime
WORKDIR /app
ENV PYTHONUNBUFFERED=1
RUN useradd --create-home appuser
COPY --from=builder /install /usr/local
COPY pyproject.toml ./
COPY airbot ./airbot
COPY config ./config
COPY --from=frontend /app/static ./static
RUN pip install --no-cache-dir -e . && \
    mkdir -p /app/data /app/logs && chown -R appuser /app
USER appuser
EXPOSE 8000
ENV PORT=8000
ENTRYPOINT ["sh", "-c", "uvicorn airbot.web:app --host 0.0.0.0 --port ${PORT}"]
