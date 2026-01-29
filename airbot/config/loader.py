"""YAML config loader with caching for performance."""
from pathlib import Path
from functools import lru_cache
from typing import Any
import yaml


def load_yaml_config(path: str | Path) -> dict[str, Any]:
    """Load YAML file and return dict. No cache – raw loader."""
    p = Path(path)
    if not p.exists():
        return {}
    with open(p, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


@lru_cache(maxsize=8)
def get_cached_config(path: str) -> dict[str, Any]:
    """Load YAML config with cache (path as string for hashability)."""
    return load_yaml_config(path)
