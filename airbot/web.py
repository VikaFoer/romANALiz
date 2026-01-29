"""FastAPI app for Railway – HTTP API + worker pool (health, POST /events)."""
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from airbot.config import get_settings
from airbot.collector import CollectorQueue, WorkerPool
from airbot.output import OutputRouter

# Ensure detectors are registered
import airbot.detectors.example  # noqa: F401

queue: CollectorQueue | None = None
pool: WorkerPool | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    Path("data").mkdir(exist_ok=True)
    global queue, pool
    settings = get_settings()
    queue = CollectorQueue()
    output = OutputRouter()
    pool = WorkerPool(queue, output, pool_size=settings.worker_pool_size)
    await pool.start()
    yield
    if pool:
        await pool.stop()
    queue = None
    pool = None


app = FastAPI(title="Air-bot", version="0.1.0", lifespan=lifespan)


class EventIn(BaseModel):
    """POST /events body."""

    id: str = "unknown"
    value: float = 0.0
    payload: dict[str, Any] | None = None


@app.get("/")
async def root() -> dict[str, Any]:
    return {
        "app": "Air-bot",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/health",
        "events": "POST /events",
    }


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/events")
async def post_events(event: EventIn) -> dict[str, Any]:
    if not queue:
        raise HTTPException(503, "Worker pool not ready")
    item = {"id": event.id, "value": event.value, **(event.payload or {})}
    await queue.put(item)
    return {"status": "queued", "id": event.id}
