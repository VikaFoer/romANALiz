"""Registry of detectors – pluggable, extensible."""
from typing import Type
from airbot.detectors.base import BaseDetector

_registry: list[Type[BaseDetector]] = []


def register_detector(cls: Type[BaseDetector]) -> Type[BaseDetector]:
    """Register a detector class."""
    _registry.append(cls)
    return cls


def get_detectors() -> list[Type[BaseDetector]]:
    """Return list of registered detector classes."""
    return list(_registry)
