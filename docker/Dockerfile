# Air-bot – multi-stage Docker build
FROM python:3.12-slim as builder
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
COPY pyproject.toml ./
RUN pip install --no-cache-dir build
COPY airbot ./airbot
COPY config ./config
RUN pip install --no-cache-dir -e . --target /install

FROM python:3.12-slim as runtime
WORKDIR /app
ENV PYTHONUNBUFFERED=1
RUN useradd --create-home appuser
COPY --from=builder /install /usr/local
COPY pyproject.toml ./
COPY airbot ./airbot
COPY config ./config
RUN pip install --no-cache-dir -e . && \
    mkdir -p /app/data /app/logs && chown -R appuser /app
USER appuser
EXPOSE 8000
ENTRYPOINT ["python", "-m", "airbot.main"]
