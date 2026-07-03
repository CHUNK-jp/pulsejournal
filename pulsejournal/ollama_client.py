"""
Ollama integration
====================
Sends a day's metrics + tone prompt to a local Ollama model and returns
the generated diary entry text. Local-only — no data leaves the machine.

Requires the generation model to be pulled beforehand:
  ollama pull qwen2.5:7b
"""

import ollama

from pulsejournal.parser import DailyMetrics
from pulsejournal.tones import build_prompt

GENERATION_MODEL = "qwen2.5:7b"


def check_ollama() -> bool:
    """Return True if the Ollama server is reachable."""
    try:
        ollama.list()
        return True
    except Exception:
        return False


def has_generation_model(model: str = GENERATION_MODEL) -> bool:
    """Return True if MODEL is pulled locally."""
    try:
        installed = {m.model for m in ollama.list().models}
    except Exception:
        return False
    return model in installed


def generate_entry(metrics: DailyMetrics, tone: str, lang: str = "en") -> str:
    """Generate a diary entry for METRICS in the voice of TONE, in LANG."""
    prompt = build_prompt(tone, metrics, lang)
    response = ollama.chat(
        model=GENERATION_MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.message.content
