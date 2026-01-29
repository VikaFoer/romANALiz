"""SQLite async connection pool."""
from typing import Any
import aiosqlite
from airbot.db.interface import Database


class SQLitePool(Database):
    """SQLite with aiosqlite – one connection, pool-like usage."""

    def __init__(self, url: str) -> None:
        self._url = url.replace("sqlite+aiosqlite:///", "")
        self._conn: aiosqlite.Connection | None = None

    async def connect(self) -> None:
        self._conn = await aiosqlite.connect(self._url)
        self._conn.row_factory = aiosqlite.Row

    async def disconnect(self) -> None:
        if self._conn:
            await self._conn.close()
            self._conn = None

    async def execute(self, query: str, *args: Any, **kwargs: Any) -> Any:
        if not self._conn:
            raise RuntimeError("Database not connected")
        if args and len(args) == 1 and isinstance(args[0], (list, tuple)):
            params = list(args[0])
        else:
            params = list(args) if args else list(kwargs.values())
        await self._conn.execute(query, params)
        await self._conn.commit()

    async def fetch_one(self, query: str, *args: Any, **kwargs: Any) -> dict[str, Any] | None:
        if not self._conn:
            raise RuntimeError("Database not connected")
        if args and len(args) == 1 and isinstance(args[0], (list, tuple)):
            params = list(args[0])
        else:
            params = list(args) if args else list(kwargs.values())
        cursor = await self._conn.execute(query, params)
        row = await cursor.fetchone()
        return dict(row) if row else None

    async def fetch_all(self, query: str, *args: Any, **kwargs: Any) -> list[dict[str, Any]]:
        if not self._conn:
            raise RuntimeError("Database not connected")
        if args and len(args) == 1 and isinstance(args[0], (list, tuple)):
            params = list(args[0])
        else:
            params = list(args) if args else list(kwargs.values())
        cursor = await self._conn.execute(query, params)
        rows = await cursor.fetchall()
        return [dict(r) for r in rows]
