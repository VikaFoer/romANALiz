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
airbot/         # Backend (FastAPI, черга, детектори, …)
frontend/       # React (Vite + TS) — збірка в static/
static/         # Зібраний фронтенд (index.html + assets)
config/         # example.yaml
tests/          # Unit-тести
docker/         # Dockerfile (Node + Python, uvicorn)
.github/        # CI
k8s/            # Kubernetes
deploy/         # systemd
```

## Швидкий старт

```bash
cp .env.example .env
# Відредагуйте .env

python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -e ".[dev]"

# Зібрати React-фронтенд (потрібен Node)
cd frontend && npm ci && npm run build && cd ..

pytest
uvicorn airbot.web:app --host 0.0.0.0 --port 8000
```

Відкрийте `http://localhost:8000` — інтерфейс React (форма подій, статус, посилання на API).

## Docker

Dockerfile збирає React-фронтенд і запускає uvicorn:

```bash
docker build -f docker/Dockerfile -t air-bot .
docker run --env-file .env -p 8000:8000 -e PORT=8000 air-bot
```

## Деплой на Railway

1. Підключіть репо [GitHub → Railway](https://railway.app).
2. Новий проєкт → **Deploy from GitHub** → оберіть `VikaFoer/romANALiz`.
3. У **Variables** додайте змінні з `.env.example` (принаймні `DATABASE_URL`; `PORT` Railway задає сам).
4. Деплой: Nixpacks (`nixpacks.toml`) збирає фронтенд (`frontend/` → `static/`) і бекенд, потім `uvicorn airbot.web:app --host 0.0.0.0 --port $PORT`. Альтернатива: **Dockerfile** (Railway → Use Dockerfile).
5. Після деплою: `https://<your-app>.up.railway.app/` — React-інтерфейс, `/health`, `POST /events`.

**Локально (web-режим як на Railway):**

```bash
pip install -e ".[dev]"
uvicorn airbot.web:app --host 0.0.0.0 --port 8000
```

## Ліцензія

MIT
