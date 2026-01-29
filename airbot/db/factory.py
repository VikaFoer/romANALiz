"""Factory: create Database from DATABASE_URL."""
from airbot.config import get_settings
from airbot.db.interface import Database
from airbot.db.sqlite_pool import SQLitePool
from airbot.db.postgres_pool import PostgresPool


def create_database() -> Database:
    """Create DB implementation from settings (SQLite or PostgreSQL)."""
    url = get_settings().database_url
    if "sqlite" in url:
        return SQLitePool(url)
    if "postgresql" in url:
        # asyncpg expects postgresql:// (no +asyncpg)
        dsn = url.replace("postgresql+asyncpg://", "postgresql://", 1)
        return PostgresPool(dsn)
    raise ValueError(f"Unsupported DATABASE_URL: {url[:50]}...")
