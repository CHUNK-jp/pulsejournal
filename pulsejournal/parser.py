"""
Apple Health export parser
============================
Reads the ZIP produced by Health app → profile → Export All Health Data,
and extracts daily metrics (steps, heart rate, sleep, HRV) from the
enclosed export.xml.

Skeleton only — parsing logic lands in a follow-up step.
"""

from dataclasses import dataclass
from datetime import date
from pathlib import Path


@dataclass
class DailyMetrics:
    day: date
    steps: int
    heart_rate_avg_bpm: float
    sleep_hours: float
    hrv_ms: float


def parse_export(zip_path: Path) -> list[DailyMetrics]:
    """Parse an Apple Health export ZIP into a list of DailyMetrics.

    Extracts export.xml from ZIP_PATH and aggregates records per day.
    """
    raise NotImplementedError


def _extract_export_xml(zip_path: Path) -> Path:
    """Unzip ZIP_PATH and return the path to the enclosed export.xml."""
    raise NotImplementedError


def _parse_export_xml(xml_path: Path) -> list[DailyMetrics]:
    """Stream-parse export.xml into per-day aggregated metrics."""
    raise NotImplementedError
