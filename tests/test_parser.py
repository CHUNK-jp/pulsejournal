"""Tests for pulsejournal.parser using a dummy Apple Health XML snippet
(no real export data required)."""

import unittest
import zipfile
from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory

from pulsejournal.parser import parse_export

# 800 steps, avg HR 72 bpm, 8h sleep (attributed to the wake-up date), 42ms HRV
SAMPLE_EXPORT_XML = """<?xml version="1.0" encoding="UTF-8"?>
<HealthData locale="en_US">
 <ExportDate value="2024-01-16 08:00:00 +0900"/>
 <Record type="HKQuantityTypeIdentifierStepCount" sourceName="iPhone" unit="count"
   startDate="2024-01-15 08:00:00 +0900" endDate="2024-01-15 08:10:00 +0900" value="500"/>
 <Record type="HKQuantityTypeIdentifierStepCount" sourceName="iPhone" unit="count"
   startDate="2024-01-15 12:00:00 +0900" endDate="2024-01-15 12:10:00 +0900" value="300"/>
 <Record type="HKQuantityTypeIdentifierHeartRate" sourceName="Watch" unit="count/min"
   startDate="2024-01-15 09:00:00 +0900" endDate="2024-01-15 09:00:00 +0900" value="70"/>
 <Record type="HKQuantityTypeIdentifierHeartRate" sourceName="Watch" unit="count/min"
   startDate="2024-01-15 15:00:00 +0900" endDate="2024-01-15 15:00:00 +0900" value="74"/>
 <Record type="HKCategoryTypeIdentifierSleepAnalysis" sourceName="Watch"
   startDate="2024-01-14 23:00:00 +0900" endDate="2024-01-15 07:00:00 +0900"
   value="HKCategoryValueSleepAnalysisAsleep"/>
 <Record type="HKQuantityTypeIdentifierHeartRateVariabilitySDNN" sourceName="Watch" unit="ms"
   startDate="2024-01-15 09:00:00 +0900" endDate="2024-01-15 09:00:00 +0900" value="40"/>
 <Record type="HKQuantityTypeIdentifierHeartRateVariabilitySDNN" sourceName="Watch" unit="ms"
   startDate="2024-01-15 15:00:00 +0900" endDate="2024-01-15 15:00:00 +0900" value="44"/>
</HealthData>
"""


class ParseExportTests(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = TemporaryDirectory()
        self.zip_path = Path(self.tmp_dir.name) / "export.zip"
        with zipfile.ZipFile(self.zip_path, "w") as zf:
            zf.writestr("apple_health_export/export.xml", SAMPLE_EXPORT_XML)

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_parses_daily_metrics_from_zip(self):
        results = parse_export(self.zip_path)
        self.assertEqual(len(results), 1)

        day = results[0]
        self.assertEqual(day.day, date(2024, 1, 15))
        self.assertEqual(day.steps, 800)
        self.assertEqual(day.heart_rate_avg_bpm, 72.0)
        self.assertEqual(day.sleep_hours, 8.0)
        self.assertEqual(day.hrv_ms, 42.0)

    def test_missing_export_xml_raises(self):
        empty_zip = Path(self.tmp_dir.name) / "empty.zip"
        with zipfile.ZipFile(empty_zip, "w"):
            pass
        with self.assertRaises(ValueError):
            parse_export(empty_zip)


if __name__ == "__main__":
    unittest.main()
