"""Unit tests for scoring engine."""
import pytest
from airbot.detectors.base import DetectorResult
from airbot.scoring.engine import ScoringEngine


def test_aggregate_empty():
    engine = ScoringEngine()
    assert engine.aggregate([]) == 0.0


def test_aggregate_single():
    engine = ScoringEngine()
    r = DetectorResult("e1", 0.8, {}, "d1")
    assert engine.aggregate([r]) == 0.8


def test_aggregate_weighted():
    engine = ScoringEngine(weights={"d1": 2.0, "d2": 1.0})
    results = [
        DetectorResult("e1", 0.5, {}, "d1"),
        DetectorResult("e1", 0.5, {}, "d2"),
    ]
    # (0.5*2 + 0.5*1) / 3 = 0.5
    assert engine.aggregate(results) == 0.5
