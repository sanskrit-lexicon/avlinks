# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**avlinks** provides web pages displaying individual verses of the Atharva Veda, enabling direct links from CDSL dictionaries to cited Atharva Veda passages. Deployed at `https://sanskrit-lexicon.github.io/avlinks/`.

Each verse page shows the verse in Devanagari (with accents), IAST transliteration, and Russian translation (Elizarenkova).

## Architecture

| File/Directory | Purpose |
|---|---|
| `avhymns/` | Generated HTML files, one per hymn (`av01.001.html` through `av20.NNN.html`) |
| `make_hymns_01.py` | Generates `avhymns/*.html` from the processed AV source |
| `avtest.py` | Processes the raw AV HTML source into pipeline-ready format |
| `AVS2.html` | Primary source: Atharva Veda with Sanskrit, Russian columns |
| `avhymns.css` | Stylesheet for hymn display pages |
| `fonts/` | Sanskrit display fonts (Siddhanta) |
| `make_hymns_log.txt` | Log from the last build run |

### Build pipeline

```bash
python avtest.py <step> <input> <output>    # transform AV source
python make_hymns_01.py <processed_source> avhymns   # generate hymn pages
```

After building, `avhymns/` is pushed and served via GitHub Pages at `https://sanskrit-lexicon.github.io/avlinks/`.

## Dependencies

- **Python 3**
- `AVS2.html` — source Atharva Veda file (in repo)
