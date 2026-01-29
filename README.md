# Air-bot – Maximum-Detail & Maximum-Efficiency Blueprint

Повний проєкт готовий до локального запуску, тестування, CI/CD і продакшн-деплою (Docker/K8s).

## Ключові принципи

- **Безпека** – усі секрети в `.env`, pydantic-валідація, `.gitignore`.
- **Продуктивність** – пул з'єднань (SQLite/PostgreSQL), асинхронна черга + worker-пул, індекси, кешування YAML-конфігів.
- **Модульність** – config, db, detectors, scoring, output, collector – окремий файл, легко тестується.
- **Розширюваність** – інтерфейс Database, Kafka/Webhook, SOC-MINT, NLP-моделі.
- **DevOps** – Docker (multi-stage), GitHub Actions, Kubernetes, systemd.

## Структура

```
airbot/
  config/     # pydantic settings, YAML loader, caching
  db/         # Database interface, SQLite/PostgreSQL pools
  detectors/  # Детектори подій
  scoring/    # Скоринг
  output/     # Kafka, Webhook
  collector/  # Збір та черга
  soc_mint/   # SOC-MINT модуль
main.py       # Entry point
tests/        # Unit-тести
docker/       # Dockerfile
.github/      # CI
k8s/          # Kubernetes
deploy/       # systemd
```

## Швидкий старт

```bash
cp .env.example .env
# Відредагуйте .env

python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -e ".[dev]"
pytest
python -m airbot.main
```

## Docker

```bash
docker build -f docker/Dockerfile -t air-bot .
docker run --env-file .env -p 8000:8000 air-bot
```

## Деплой на Railway

1. Підключіть репо [GitHub → Railway](https://railway.app).
2. Новий проєкт → **Deploy from GitHub** → оберіть `VikaFoer/romANALiz`.
3. У **Variables** додайте змінні з `.env.example` (принаймні `DATABASE_URL`; `PORT` Railway задає сам).
4. Деплой: Railway використовує `Procfile` / `railway.json`, збирає через Nixpacks, запускає `uvicorn airbot.web:app --host 0.0.0.0 --port $PORT`.
5. Після деплою: `https://<your-app>.up.railway.app/health` та `POST /events` для подій.

**Локально (web-режим як на Railway):**

```bash
pip install -e ".[dev]"
uvicorn airbot.web:app --host 0.0.0.0 --port 8000
```

## Ліцензія

MIT
