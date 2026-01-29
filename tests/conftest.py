"""Pytest fixtures – env override for tests."""
import pytest


@pytest.fixture(autouse=True)
def env_for_tests(monkeypatch):
    """Use test env so real .env doesn't leak secrets."""
    monkeypatch.setenv("APP_ENV", "test")
    monkeypatch.setenv("DATABASE_URL", "sqlite+aiosqlite:///./data/test.db")
    monkeypatch.setenv("KAFKA_ENABLED", "false")
    monkeypatch.setenv("WEBHOOK_ENABLED", "false")
    monkeypatch.setenv("WORKER_POOL_SIZE", "2")
    monkeypatch.setenv("QUEUE_MAX_SIZE", "100")
    # Invalidate cached settings so tests see new env
    try:
        from airbot.config.settings import get_settings
        get_settings.cache_clear()
    except Exception:
        pass
    yield
    try:
        get_settings.cache_clear()
    except Exception:
        pass
