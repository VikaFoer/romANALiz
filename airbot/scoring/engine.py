"""Scoring engine – aggregates detector results into final score."""
from airbot.detectors.base import DetectorResult


class ScoringEngine:
    """Combine detector results (e.g. weighted average, max, custom)."""

    def __init__(self, weights: dict[str, float] | None = None) -> None:
        self.weights = weights or {}

    def aggregate(self, results: list[DetectorResult]) -> float:
        """Aggregate scores; default weighted average, fallback simple average."""
        if not results:
            return 0.0
        total = 0.0
        w_sum = 0.0
        for r in results:
            w = self.weights.get(r.detector_name, 1.0)
            total += r.score * w
            w_sum += w
        return total / w_sum if w_sum else 0.0
