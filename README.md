# PulseJournal

AI health diary generator — turns your wearable data into a daily story.

## Usage

```bash
pip install -r requirements.txt

python -m pulsejournal.cli generate --input health_export.zip --tone hero
```

`--input` is the ZIP from Health app → your profile → Export All Health Data.

`--tone` selects the narrative voice:

| Tone | Description |
| --- | --- |
| `reflective` | Calm, observational |
| `motivational` | Upbeat, encouraging |
| `hero` | Epic fantasy chronicle |
| `scifi` | Starship captain's log |
| `poetic` | Free-verse poem |

Requires [Ollama](https://ollama.com) running locally (`ollama serve`) — generation happens entirely on your machine, no data leaves it.

Parsing and generation are scaffolded but not yet implemented; that logic lands in a follow-up step.
