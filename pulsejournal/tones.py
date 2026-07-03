"""
Tone prompt templates
======================
Each tone maps a day's health metrics onto a different narrative voice.
The `{metrics}` placeholder is filled in by ollama_client with a
formatted summary of the day's steps, heart rate, sleep, and HRV.
"""

TONES = {
    "reflective": {
        "label": "Reflective",
        "prompt": (
            "Write a short, calm, first-person diary entry reflecting on today's "
            "health data. Understated and observational — notice patterns without "
            "judging them. Today's data:\n{metrics}"
        ),
    },
    "motivational": {
        "label": "Motivational",
        "prompt": (
            "Write an upbeat, encouraging first-person diary entry celebrating "
            "today's health data. Energetic tone, acknowledge wins, light on "
            "hype. Today's data:\n{metrics}"
        ),
    },
    "hero": {
        "label": "Hero's Journey",
        "prompt": (
            "Write today's health data as a passage from an epic fantasy "
            "chronicle. The body is the hero, the day is a quest. Today's "
            "data:\n{metrics}"
        ),
    },
    "scifi": {
        "label": "Sci-Fi Log",
        "prompt": (
            "Write today's health data as a captain's log entry from a starship "
            "medical bay, in clipped technical sci-fi prose. Today's "
            "data:\n{metrics}"
        ),
    },
    "poetic": {
        "label": "Poetic",
        "prompt": (
            "Write today's health data as a short free-verse poem. Imagery over "
            "explanation, but keep the underlying numbers legible. Today's "
            "data:\n{metrics}"
        ),
    },
}

TONE_CHOICES = list(TONES.keys())


def get_prompt(tone: str) -> str:
    """Return the prompt template for TONE, raising KeyError if unknown."""
    return TONES[tone]["prompt"]
