"""
Tone prompt templates
======================
Each tone maps a day's health metrics onto a different narrative voice, in
English or Japanese. build_prompt() fills the template with the metrics
returned by parser.parse_export() to produce the final prompt sent to
Ollama.
"""

from pulsejournal.parser import DailyMetrics

TONES = {
    "reflective": {
        "label": "Reflective",
        "prompt": {
            "en": (
                "Write a short, calm, first-person diary entry reflecting on "
                "today's health data. Understated and observational — notice "
                "patterns without judging them.\n\n{metrics}"
            ),
            "ja": (
                "以下の今日の健康データをもとに、落ち着いた一人称の短い日記を"
                "書いてください。淡々とした観察的な文体で、良し悪しの判断はせず"
                "気づいたことを綴ってください。\n\n{metrics}"
            ),
        },
    },
    "motivational": {
        "label": "Motivational",
        "prompt": {
            "en": (
                "Write an upbeat, encouraging first-person diary entry "
                "celebrating today's health data. Energetic tone, acknowledge "
                "wins, light on hype.\n\n{metrics}"
            ),
            "ja": (
                "以下の今日の健康データをもとに、前向きで励ますような一人称の"
                "日記を書いてください。今日の頑張りを称える元気なトーンで、"
                "大げさになりすぎないようにしてください。\n\n{metrics}"
            ),
        },
    },
    "hero": {
        "label": "Hero's Journey",
        "prompt": {
            "en": (
                "Write today's health data as a passage from an epic fantasy "
                "chronicle. The body is the hero, the day is a quest.\n\n{metrics}"
            ),
            "ja": (
                "以下の今日の健康データを、壮大なファンタジー年代記の一節として"
                "書いてください。身体を英雄に、一日を冒険に見立ててください。"
                "\n\n{metrics}"
            ),
        },
    },
    "scifi": {
        "label": "Sci-Fi Log",
        "prompt": {
            "en": (
                "Write today's health data as a captain's log entry from a "
                "starship medical bay, in clipped technical sci-fi prose."
                "\n\n{metrics}"
            ),
            "ja": (
                "以下の今日の健康データを、宇宙船の医療室からの艦長日誌として、"
                "簡潔でテクニカルなSF文体で書いてください。\n\n{metrics}"
            ),
        },
    },
    "poetic": {
        "label": "Poetic",
        "prompt": {
            "en": (
                "Write today's health data as a short free-verse poem. Imagery "
                "over explanation, but keep the underlying numbers legible."
                "\n\n{metrics}"
            ),
            "ja": (
                "以下の今日の健康データを、短い自由詩として書いてください。"
                "説明よりもイメージを大切にしつつ、元の数値が伝わるようにして"
                "ください。\n\n{metrics}"
            ),
        },
    },
}

TONE_CHOICES = list(TONES.keys())
LANG_CHOICES = ("en", "ja")


def format_metrics(metrics: DailyMetrics, lang: str = "en") -> str:
    """Render DailyMetrics as a plain-text block for prompt injection."""
    if lang == "ja":
        return (
            f"日付: {metrics.day.isoformat()}\n"
            f"歩数: {metrics.steps:,} 歩\n"
            f"平均心拍数: {metrics.heart_rate_avg_bpm} bpm\n"
            f"睡眠時間: {metrics.sleep_hours} 時間\n"
            f"HRV: {metrics.hrv_ms} ms"
        )
    return (
        f"Date: {metrics.day.isoformat()}\n"
        f"Steps: {metrics.steps:,}\n"
        f"Average heart rate: {metrics.heart_rate_avg_bpm} bpm\n"
        f"Sleep: {metrics.sleep_hours} hours\n"
        f"HRV: {metrics.hrv_ms} ms"
    )


def build_prompt(tone: str, metrics: DailyMetrics, lang: str = "en") -> str:
    """Assemble the full Ollama prompt for TONE, filling in METRICS, in LANG."""
    if tone not in TONES:
        raise ValueError(f"Unknown tone: {tone!r}. Choose from {TONE_CHOICES}.")
    if lang not in LANG_CHOICES:
        raise ValueError(f"Unknown lang: {lang!r}. Choose from {LANG_CHOICES}.")

    template = TONES[tone]["prompt"][lang]
    return template.format(metrics=format_metrics(metrics, lang))
