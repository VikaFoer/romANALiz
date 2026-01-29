"""Base detector interface – extend for custom detectors."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class DetectorResult:
    """Result of a detector run."""
    event_id: str
    score: float
    payload: dict[str, Any]
    detector_name: str


class BaseDetector(ABC):
    """Abstract detector – one file per detector, easy to test."""

    name: str = "base"

    @abstractmethod
    async def run(self, input_data: dict[str, Any]) -> DetectorResult | list[DetectorResult]:
        """Run detection; return one or more results."""
        ...
