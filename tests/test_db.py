"""Unit tests for db module."""
import pytest
from airbot.db.interface import Database
from airbot.db.sqlite_pool import SQLitePool
from airbot.db.factory import create_database


@pytest.mark.asyncio
async def test_sqlite_pool_connect_disconnect(tmp_path):
    url = f"sqlite+aiosqlite:///{tmp_path / 't.db'}"
    db: Database = SQLitePool(url)
    await db.connect()
    await db.execute("CREATE TABLE t (id INTEGER PRIMARY KEY, x TEXT)")
    await db.execute("INSERT INTO t (x) VALUES (?)", ("hello",))
    row = await db.fetch_one("SELECT * FROM t WHERE id = 1")
    assert row is not None
    assert row["x"] == "hello"
    await db.disconnect()


@pytest.mark.asyncio
async def test_sqlite_context_manager(tmp_path):
    url = f"sqlite+aiosqlite:///{tmp_path / 'c.db'}"
    async with SQLitePool(url) as db:
        await db.execute("CREATE TABLE t (id INT)")
        rows = await db.fetch_all("SELECT 1 as a")
        assert len(rows) == 1
        assert rows[0]["a"] == 1


def test_factory_returns_sqlite_for_sqlite_url(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite+aiosqlite:///./x.db")
    from airbot.config.settings import get_settings
    get_settings.cache_clear()
    db = create_database()
    assert isinstance(db, SQLitePool)
    get_settings.cache_clear()
