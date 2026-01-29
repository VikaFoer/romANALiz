"""Async queue for events – bounded, max size from config."""
import asyncio
from typing import Any
from airbot.config import get_settings


class CollectorQueue:
    """Bounded asyncio queue for incoming events."""

    def __init__(self) -> None:
        max_size = get_settings().queue_max_size
        self._queue: asyncio.Queue[dict[str, Any]] = asyncio.Queue(maxsize=max_size)

    async def put(self, item: dict[str, Any]) -> None:
        await self._queue.put(item)

    def put_nowait(self, item: dict[str, Any]) -> None:
        self._queue.put_nowait(item)

    async def get(self) -> dict[str, Any]:
        return await self._queue.get()

    def get_nowait(self) -> dict[str, Any]:
        return self._queue.get_nowait()

    def qsize(self) -> int:
        return self._queue.qsize()

    def empty(self) -> bool:
        return self._queue.empty()
