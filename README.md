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

`--lang` selects the entry's language: `en` (default) or `ja`.

Requires [Ollama](https://ollama.com) running locally (`ollama serve`), with the generation model pulled beforehand:

```bash
ollama pull qwen2.5:7b
```

Generation happens entirely on your machine — no data leaves it.
