"""Unit tests for config module."""
import pytest
from pathlib import Path

from airbot.config.settings import get_settings, Settings
from airbot.config.loader import load_yaml_config, get_cached_config


def test_get_settings_returns_settings():
    s = get_settings()
    assert isinstance(s, Settings)
    assert s.app_env in ("test", "development")
    assert s.worker_pool_size >= 1


def test_settings_validation():
    s = get_settings()
    assert 1 <= s.worker_pool_size <= 64
    assert s.queue_max_size >= 1


def test_load_yaml_config_missing_file():
    out = load_yaml_config(Path("/nonexistent/file.yaml"))
    assert out == {}


def test_load_yaml_config_real_file():
    path = Path(__file__).parent.parent / "config" / "example.yaml"
    if path.exists():
        out = load_yaml_config(path)
        assert isinstance(out, dict)
        assert "app" in out or out == {}


def test_get_cached_config_same_path():
    path = str(Path(__file__).parent.parent / "config" / "example.yaml")
    if not Path(path).exists():
        pytest.skip("example.yaml not found")
    a = get_cached_config(path)
    b = get_cached_config(path)
    assert a is b  # cached
