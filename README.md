# avlinks

_Created: 17-06-2026 · Last updated: 11-07-2026_

A CDSL **linking-tool** repository in the [Sanskrit Lexicon](https://github.com/sanskrit-lexicon) project. It hosts per-hymn web pages that link to the verses of the **Atharva Veda** (Śaunakīya recension, AVS).

## What this repo does

The single source file, [`AVS2.html`](https://github.com/sanskrit-lexicon/avlinks/blob/main/AVS2.html), was provided by Mārcis Gasūns in June 2019 (see [GRA issue #3](https://github.com/sanskrit-lexicon/GRA/issues/3)). A small Python pipeline splits it into one HTML page per hymn, published via GitHub Pages:

- Live site: [sanskrit-lexicon.github.io/avlinks](https://sanskrit-lexicon.github.io/avlinks/)
- Generated pages: [`avhymns/`](https://github.com/sanskrit-lexicon/avlinks/tree/main/avhymns) — one file per hymn, named `av{book}.{hymn}.html` (e.g. `av01.001.html` … `av20.143.html`), plus [`avhymns.css`](https://github.com/sanskrit-lexicon/avlinks/blob/main/avhymns.css) and a [`fonts/`](https://github.com/sanskrit-lexicon/avlinks/tree/main/fonts) directory.

Current coverage: **731 hymns**, **5933 verses** across the 20 books of the Atharva Veda.

## Pipeline

Orientation lives in [`readme.org`](https://github.com/sanskrit-lexicon/avlinks/blob/main/readme.org). The build steps:

1. Normalize line endings: [`unixify.py`](https://github.com/sanskrit-lexicon/avlinks/blob/main/unixify.py) on `AVS2.html`.
2. Check for unknown Unicode characters: [`avtest.py`](https://github.com/sanskrit-lexicon/avlinks/blob/main/avtest.py).
3. Regenerate the `avhymns/` directory: [`redo.sh`](https://github.com/sanskrit-lexicon/avlinks/blob/main/redo.sh), which drives [`make_hymns_01.py`](https://github.com/sanskrit-lexicon/avlinks/blob/main/make_hymns_01.py) (per-hymn log in [`make_hymns_log.txt`](https://github.com/sanskrit-lexicon/avlinks/blob/main/make_hymns_log.txt)).

Repo-specific guidance for agents: [`CLAUDE.md`](https://github.com/sanskrit-lexicon/avlinks/blob/main/CLAUDE.md).

## Issues Overview

Snapshot 11-07-2026: **1** open, **0** closed.

| Milestone | Open | Closed | Total |
|---|---:|---:|---:|
| API Stability | 0 | 0 | 0 |
| User Experience | 0 | 0 | 0 |
| Data Quality | 0 | 0 | 0 |
| Developer Experience | 1 | 0 | 1 |
| Community | 0 | 0 | 0 |

The single open issue is a `documentation` / `trivial` item under Developer Experience.

## GitHub Issue Conventions

Follows the [Cologne tooling-repo taxonomy](https://github.com/sanskrit-lexicon/csl-observatory/blob/main/runbook/cologne-tooling-runbook.md). Every issue carries exactly one **type** label, one **severity** (`trivial`, `minor`, `major`, `critical`), and one **milestone** (API Stability, User Experience, Data Quality, Developer Experience, Community). Cross-tool work is tracked in the org [Tooling Roadmap](https://github.com/orgs/sanskrit-lexicon/projects/9). Full label and milestone definitions are in [`CLAUDE.md`](https://github.com/sanskrit-lexicon/avlinks/blob/main/CLAUDE.md).

---

_Dr. Mārcis Gasūns_
