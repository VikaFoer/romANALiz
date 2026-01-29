"""Detectors – pluggable event detectors."""
from airbot.detectors.base import BaseDetector, DetectorResult
from airbot.detectors.registry import get_detectors, register_detector

__all__ = ["BaseDetector", "DetectorResult", "get_detectors", "register_detector"]
