"""FastAPI app for Railway – HTTP API + worker pool (health, POST /events)."""
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"

from airbot.config import get_settings
from airbot.collector import CollectorQueue, WorkerPool
from airbot.output import OutputRouter

# Ensure detectors are registered
import airbot.detectors.example  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    Path("data").mkdir(exist_ok=True)
    settings = get_settings()
    queue = CollectorQueue()
    output = OutputRouter()
    pool = WorkerPool(queue, output, pool_size=settings.worker_pool_size)
    await pool.start()
    app.state.queue = queue
    app.state.pool = pool
    yield
    await pool.stop()
    app.state.queue = None
    app.state.pool = None


app = FastAPI(title="Air-bot", version="0.1.0", lifespan=lifespan)

if STATIC_DIR.is_dir():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


class EventIn(BaseModel):
    """POST /events body."""

    id: str = "unknown"
    value: float = 0.0
    payload: dict[str, Any] | None = None


@app.get("/")
async def root():
    if STATIC_DIR.is_dir() and (STATIC_DIR / "index.html").exists():
        return FileResponse(STATIC_DIR / "index.html")
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
async def post_events(request: Request, event: EventIn) -> dict[str, Any]:
    queue = getattr(request.app.state, "queue", None)
    if not queue:
        raise HTTPException(503, "Worker pool not ready")
    item = {"id": event.id, "value": event.value, **(event.payload or {})}
    await queue.put(item)
    return {"status": "queued", "id": event.id}
