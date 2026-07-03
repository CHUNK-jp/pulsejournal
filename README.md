# PulseJournal

AI health diary generator — turns your wearable data into a daily story.

## Setup

```bash
pip install -r requirements.txt

# One-time: pull the generation model (~4.7 GB)
ollama pull qwen2.5:7b
```

Export your data: Health app → your profile (top right) → Export All Health Data. This produces a ZIP containing `export.xml` — pass that ZIP straight to PulseJournal, no unzipping needed.

## Usage

```bash
python -m pulsejournal.cli generate --input health_export.zip --tone hero --lang ja
```

`--tone` selects the narrative voice:

| Tone | Description |
| --- | --- |
| `reflective` | Calm, observational |
| `motivational` | Upbeat, encouraging |
| `hero` | Epic fantasy chronicle |
| `scifi` | Starship captain's log |
| `poetic` | Free-verse poem |

`--lang` selects the entry's language: `en` (default) or `ja`.

### Examples

```bash
# Hero's Journey, in Japanese
python -m pulsejournal.cli generate --input health_export.zip --tone hero --lang ja

# Reflective, in English
python -m pulsejournal.cli generate --input health_export.zip --tone reflective --lang en

# Sci-Fi captain's log, in English
python -m pulsejournal.cli generate --input health_export.zip --tone scifi --lang en
```

Requires [Ollama](https://ollama.com) running locally (`ollama serve`). Generation happens entirely on your machine — no data leaves it.

### Sample output

`--tone reflective --lang en`, from a day with 800 steps, 72 bpm average heart rate, 8 hours of sleep, and 42 ms HRV:

> Today's numbers are quite standard for me. I walked a bit less than usual, clocking in at 800 steps—nothing too different from the past few days. My heart rate averaged out at 72 bpm, which is right where it should be. It's good to see that steady pace; it feels like my body has found its rhythm.
>
> I slept for eight hours tonight, hitting the mark again. The HRV was a little lower than usual—42 ms—but I'm not overly concerned about it. Sometimes it's higher, sometimes lower. I suppose it just means there are small fluctuations in how my body is resting and recovering from day to day.
>
> Overall, no significant changes today, which can be reassuring. It's comforting to see consistency even when everything seems mundane. Maybe tomorrow will bring something different—or maybe not. Either way, I'm content with where I am right now.

## Troubleshooting

**`✗ Cannot reach Ollama.`**
Ollama isn't running. Start it with `ollama serve`, then re-run the command.

**`✗ Model 'qwen2.5:7b' isn't pulled yet.`**
The generation model hasn't been downloaded on this machine. Run `ollama pull qwen2.5:7b` (one-time, ~4.7 GB) and try again.
