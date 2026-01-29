"""Unit tests for detectors."""
import pytest
from airbot.detectors.base import BaseDetector, DetectorResult
from airbot.detectors.registry import get_detectors, register_detector
from airbot.detectors.example import ExampleDetector


@pytest.mark.asyncio
async def test_example_detector_returns_result():
    det = ExampleDetector()
    out = await det.run({"id": "e1", "value": 50})
    assert isinstance(out, DetectorResult)
    assert out.event_id == "e1"
    assert out.score == 0.5
    assert out.detector_name == "example"


@pytest.mark.asyncio
async def test_example_detector_clamps_score():
    det = ExampleDetector()
    out = await det.run({"value": 200})
    assert out.score == 1.0
    out2 = await det.run({"value": -10})
    assert out2.score == 0.0


def test_registry_contains_example():
    detectors = get_detectors()
    assert any(d.name == "example" for d in detectors)
