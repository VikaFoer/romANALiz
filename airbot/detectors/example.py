"""Example detector – template for custom detectors."""
from airbot.detectors.base import BaseDetector, DetectorResult
from airbot.detectors.registry import register_detector


@register_detector
class ExampleDetector(BaseDetector):
    """Sample detector that scores input and returns one result."""

    name = "example"

    async def run(self, input_data: dict) -> DetectorResult:
        score = float(input_data.get("value", 0)) / 100.0
        return DetectorResult(
            event_id=input_data.get("id", "unknown"),
            score=min(1.0, max(0.0, score)),
            payload=input_data,
            detector_name=self.name,
        )
