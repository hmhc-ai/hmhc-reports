# Build-Conclusions — spec for `build_conclusions.py` (council scorecard)

> **Artifact:** `pipeline/sg-banks/method/7-script-build-conclusions.md` — the specification for `build_conclusions.py`; keep the two in sync.
> **Status:** Active — output goes to `data/scorecard.md` AND the report's Conclusions markers (stage 2 live since v2026.07.27-r2; the old write-conclusions module is retired and deleted — see git history).

## Module contract

| | |
|---|---|
| **Inputs** | `data/scores/<member>.json` — one blind answer sheet per council member (Write-Scores outputs; protocol and rubric in `method/7-ai-write-scores.md`) · `meta/health.json` (the frame question list, so ids/topics come from one source). |
| **Sole output** | `data/scorecard.md` — aggregate matrix per question (median performance −5…+5 · range as the disagreement marker · criticality consensus, splits shown) + thesis-overall row + one compact block per member (every score + one-sentence comment). Deterministic: members sorted by filename; no timestamps. Emits a "no council run yet" placeholder when `data/scores/` is empty. |
| **Executor** | **No model — a deterministic script:** `python3 pipeline/sg-banks/method/7-script-build-conclusions.py`; `--check` verifies reproducibility (CI + publish gates). Validates every sheet hard (question coverage/order, integer −5…+5, criticality from the validated list, blind flag, member = filename) and fails loudly on any violation. |
| **Position** | `Write-Scores (× N members, blind) → Build-Conclusions`. Insight lives upstream in the sheets; this step only validates, aggregates, and formats — by design, so the scorecard itself needs no trust in any single model. |

## Rules

- Never edit or normalize a sheet — an invalid sheet is rejected, not repaired (the member reruns).
- Median for performance; criticality consensus = most common (ties broken toward the more critical); ranges and splits are always displayed — disagreement is a signal, not noise.
- `low` criticality consensus on a question is frame feedback (the question may not belong) — surface it, never suppress it.
