"""Air-bot main entry – run collector + worker pool."""
import asyncio
import signal
from airbot.config import get_settings
from airbot.collector import CollectorQueue, WorkerPool
from airbot.output import OutputRouter
from airbot.db import create_database

# Ensure detectors are registered
import airbot.detectors.example  # noqa: F401


def main() -> None:
    """Run async app."""
    asyncio.run(_run())


async def _run() -> None:
    settings = get_settings()
    queue = CollectorQueue()
    output = OutputRouter()
    pool = WorkerPool(queue, output, pool_size=settings.worker_pool_size)

    await pool.start()

    # Optional: init DB and create table
    db = create_database()
    try:
        await db.connect()
        # SQLite: create events table with index
        if "sqlite" in settings.database_url:
            await db.execute(
                "CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY, event_id TEXT, score REAL, payload TEXT)"
            )
            await db.execute("CREATE INDEX IF NOT EXISTS idx_events_event_id ON events(event_id)")
    except Exception:
        pass
    finally:
        await db.disconnect()

    stop = asyncio.Event()

    def shutdown() -> None:
        stop.set()

    try:
        loop = asyncio.get_running_loop()
        loop.add_signal_handler(signal.SIGINT, shutdown)
        loop.add_signal_handler(signal.SIGTERM, shutdown)
    except (NotImplementedError, OSError):
        # Windows: no add_signal_handler
        pass

    try:
        await stop.wait()
    finally:
        await pool.stop()
