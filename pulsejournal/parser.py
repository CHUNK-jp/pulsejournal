"""
Apple Health export parser
============================
Reads the ZIP produced by Health app → profile → Export All Health Data,
and extracts daily metrics (steps, heart rate, sleep, HRV) from the
enclosed export.xml.

Bucketing logic (sum steps per day, average heart rate/HRV per day, sum
sleep duration attributed to the wake-up date) mirrors mirrorhealth's
src/lib/healthParser.ts.
"""

import xml.etree.ElementTree as ET
import zipfile
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import IO, Optional

STEP_TYPE = "HKQuantityTypeIdentifierStepCount"
HEART_RATE_TYPE = "HKQuantityTypeIdentifierHeartRate"
SLEEP_TYPE = "HKCategoryTypeIdentifierSleepAnalysis"
HRV_TYPE = "HKQuantityTypeIdentifierHeartRateVariabilitySDNN"

# Sleep category values that count as "asleep" (excludes in-bed/awake states)
SLEEP_ASLEEP_VALUES = {"HKCategoryValueSleepAnalysisAsleep", "1", "2", "3", "4", "5"}


@dataclass
class DailyMetrics:
    day: date
    steps: int
    heart_rate_avg_bpm: float
    sleep_hours: float
    hrv_ms: float


def parse_export(zip_path: Path) -> list[DailyMetrics]:
    """Parse an Apple Health export ZIP into a list of DailyMetrics, one per day."""
    with zipfile.ZipFile(zip_path) as zf:
        member = _find_export_xml(zf)
        with zf.open(member) as xml_file:
            return _parse_export_xml(xml_file)


def _find_export_xml(zf: zipfile.ZipFile) -> str:
    """Return the archive member name for export.xml inside ZF."""
    candidates = [n for n in zf.namelist() if n.lower().endswith("export.xml")]
    if not candidates:
        raise ValueError("No export.xml found inside the health export ZIP")
    return candidates[0]


def _parse_export_xml(xml_source: IO[bytes]) -> list[DailyMetrics]:
    """Stream-parse export.xml into per-day aggregated metrics."""
    steps_by_day: dict[str, float] = defaultdict(float)
    heart_rate_by_day: dict[str, list] = defaultdict(list)
    sleep_hours_by_day: dict[str, float] = defaultdict(float)
    hrv_by_day: dict[str, list] = defaultdict(list)

    # Track the root element so it can be cleared as we go — export.xml
    # commonly runs to hundreds of MB, so we can't hold the full tree.
    context = iter(ET.iterparse(xml_source, events=("start", "end")))
    _, root = next(context)

    for event, elem in context:
        if event != "end" or elem.tag != "Record":
            continue

        record_type = elem.get("type", "")
        start_raw = elem.get("startDate") or elem.get("creationDate")
        end_raw = elem.get("endDate") or start_raw
        value_raw = elem.get("value", "")

        if start_raw:
            day_key = start_raw[:10]  # "YYYY-MM-DD"

            if record_type == STEP_TYPE:
                steps_by_day[day_key] += _to_float(value_raw)
            elif record_type == HEART_RATE_TYPE:
                heart_rate_by_day[day_key].append(_to_float(value_raw))
            elif record_type == HRV_TYPE:
                hrv_by_day[day_key].append(_to_float(value_raw))
            elif record_type == SLEEP_TYPE and value_raw in SLEEP_ASLEEP_VALUES:
                duration_hours = _sleep_duration_hours(start_raw, end_raw)
                if duration_hours is not None:
                    # Attribute sleep to the wake-up (end) date, not the
                    # date it started.
                    sleep_hours_by_day[end_raw[:10]] += duration_hours

        root.clear()

    all_days = sorted(
        set(steps_by_day) | set(heart_rate_by_day) | set(sleep_hours_by_day) | set(hrv_by_day)
    )

    return [
        DailyMetrics(
            day=date.fromisoformat(day_key),
            steps=round(steps_by_day.get(day_key, 0.0)),
            heart_rate_avg_bpm=_average(heart_rate_by_day.get(day_key, [])),
            sleep_hours=round(sleep_hours_by_day.get(day_key, 0.0), 1),
            hrv_ms=_average(hrv_by_day.get(day_key, [])),
        )
        for day_key in all_days
    ]


def _to_float(value_raw: str) -> float:
    try:
        return float(value_raw)
    except (TypeError, ValueError):
        return 0.0


def _average(values: list) -> float:
    return round(sum(values) / len(values), 1) if values else 0.0


def _sleep_duration_hours(start_raw: str, end_raw: str) -> Optional[float]:
    """Return the duration between two Apple Health timestamps in hours.

    Apple Health timestamps look like "2024-01-15 08:30:00 +0900". Durations
    outside (0, 20) hours are discarded as data glitches, matching the sanity
    check in mirrorhealth's healthParser.ts.
    """
    try:
        start = datetime.strptime(start_raw, "%Y-%m-%d %H:%M:%S %z")
        end = datetime.strptime(end_raw, "%Y-%m-%d %H:%M:%S %z")
    except ValueError:
        return None
    duration = (end - start).total_seconds() / 3600
    return duration if 0 < duration < 20 else None
