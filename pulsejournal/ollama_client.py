"""
Ollama integration
====================
Sends a day's metrics + tone prompt to a local Ollama model and returns
the generated diary entry text. Local-only — no data leaves the machine.

Skeleton only — generation logic lands in a follow-up step.
"""

import ollama

from pulsejournal.parser import DailyMetrics

GENERATION_MODEL = "llama3.1"


def check_ollama() -> bool:
    """Return True if the Ollama server is reachable."""
    try:
        ollama.list()
        return True
    except Exception:
        return False


def format_metrics(metrics: DailyMetrics) -> str:
    """Render DailyMetrics as a plain-text summary for prompt injection."""
    raise NotImplementedError


def generate_entry(metrics: DailyMetrics, tone: str) -> str:
    """Generate a diary entry for METRICS in the voice of TONE."""
    raise NotImplementedError
