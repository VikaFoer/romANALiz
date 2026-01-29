"""PostgreSQL async connection pool."""
from typing import Any
import asyncpg
from airbot.db.interface import Database


class PostgresPool(Database):
    """PostgreSQL with asyncpg connection pool."""

    def __init__(self, url: str, min_size: int = 2, max_size: int = 10) -> None:
        self._url = url
        self._min_size = min_size
        self._max_size = max_size
        self._pool: asyncpg.Pool | None = None

    async def connect(self) -> None:
        self._pool = await asyncpg.create_pool(
            self._url,
            min_size=self._min_size,
            max_size=self._max_size,
            command_timeout=60,
        )

    async def disconnect(self) -> None:
        if self._pool:
            await self._pool.close()
            self._pool = None

    async def execute(self, query: str, *args: Any, **kwargs: Any) -> Any:
        if not self._pool:
            raise RuntimeError("Database not connected")
        async with self._pool.acquire() as conn:
            await conn.execute(query, *args)

    async def fetch_one(self, query: str, *args: Any, **kwargs: Any) -> dict[str, Any] | None:
        if not self._pool:
            raise RuntimeError("Database not connected")
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(query, *args)
            return dict(row) if row else None

    async def fetch_all(self, query: str, *args: Any, **kwargs: Any) -> list[dict[str, Any]]:
        if not self._pool:
            raise RuntimeError("Database not connected")
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(query, *args)
            return [dict(r) for r in rows]
