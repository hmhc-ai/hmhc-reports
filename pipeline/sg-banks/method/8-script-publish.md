# Publish — spec for `publish.py` (release bookkeeping)

> **Artifact:** `pipeline/sg-banks/method/8-script-publish.md` — the specification for `publish.py`; keep the two in sync.
> **Status:** Active. Introduced 2026-07-27 to collapse the release ritual (six hand-edits per version) into one command, after the version-embedded-in-health coupling caused repeated regen churn and one CI failure.

## Contract

| | |
|---|---|
| **Invocation** | `python3 pipeline/sg-banks/method/8-script-publish.py --desc "<one-sentence note>" [--changelog "<rich entry>"] [--dry-run]` — run only when the **published report changed** (pipeline/meta/site-only changes ship without a version). |
| **Writes** | `reports/index.json` (`current_version` — `YYYY.MM.DD`, `-rN` same-day; `last_updated`; `refresh_note` = this release's note + registry pointer) · registry changelog entry (top of `index.md` § Changelog) · `meta/history.csv` append (version, date, thesis score parsed from the report, questions answered, fill/dual-verified/agreement from `meta/health.json`) — the score/quality **time series**. |
| **Gates** | After writing, runs docs lint + every `--check` module (tables, charts, benchmarks, health, gaps, report-tables) and fails loudly on any failure. |
| **Does NOT** | Commit, push, tag, or edit the report/pipeline content. The tag is auto-created on `main` by the tag-version Action. Not date-deterministic, so it has **no `--check` of its own** and never runs in CI. |

## Conventions it encodes

- The **registry changelog is the canonical release history**; `refresh_note` holds only the current release + pointer.
- `meta/history.csv` is **append-only** (one row per published version); never rewritten, never regenerated.
- Health artifacts deliberately do **not** embed the version (removed 2026-07-27), so releases never force a health regen.
