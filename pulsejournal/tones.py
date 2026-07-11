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
                "以下の今日の健康データをもとに、一日をひとつの冒険として描いた"
                "短い物語を、必ず日本語だけで書いてください(中国語や英語を"
                "混ぜないこと)。\n"
                "書き方の指針:\n"
                "- 身体の持ち主を旅の主人公に見立て、語り部が物語を語る文体で"
                "書く\n"
                "- 日本語のファンタジー小説のような自然な語り口にする。文体の例"
                "(あくまで雰囲気の参考。この例文の言い回しをそのまま写さず、"
                "自分の言葉で書くこと):\n"
                "  「その朝、旅人は12,000歩の道のりを歩き通した。峠をひとつ"
                "越えた計算になる。」\n"
                "  「胸の奥では、心の臓が変わらぬ調子で鼓動を刻み続けていた。」\n"
                "- 翻訳調の硬い言い回しは避け、数値は物語の流れに自然に"
                "織り込む\n"
                "- 数値は下のデータにある算用数字の表記のまま使う(睡眠時間が"
                "「6.8時間」なら小数のまま「6.8時間」と書く)\n"
                "- 400字程度までにまとめ、物語の本文だけを書く(前置きや解説は"
                "不要)\n"
                "\n{metrics}"
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
                "以下の今日の健康データを、短い自由詩として必ず日本語だけで"
                "書いてください。説明よりもイメージを大切にしつつ、数値は"
                "下のデータにある算用数字の表記のまま、単位(歩・bpm・時間・ms)"
                "もデータのまま行に織り込んでください。"
                "行の例(雰囲気の参考。数値も言い回しもそのまま写さないこと):\n"
                "「12,000歩、まだ名前のない道をたどる」\n"
                "出力は詩の行だけで終えてください。\n\n{metrics}"
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
