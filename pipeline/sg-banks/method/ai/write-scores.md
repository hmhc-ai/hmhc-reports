# Write-Scores — Module SOP: blind council scoring (SG Banks · Conclusions)

**Module:** Write-Scores · **Inputs:** `guides/frame.md` + the report body **excluding its Conclusions section** · **Output:** one answer sheet `data/scores/<member>.json` per council member · **Depends on:** Build-Report (a current report body)
**Run on:** each council member independently — diverse frontier models across harnesses (e.g. `CwClFable5` via Claude Code, non-Claude members via the Perplexity harness). One sheet per member per report version.
**Changelog:** 2026-07-27 — first version (council architecture stage 1; sheets pilot to `data/scores/`, report wiring follows the author's frame approval).

## Blind protocol (hard rules)

1. A member sees **only**: `guides/frame.md` and `reports/sg-banks/report.md` **with everything between `<!-- conclusions:start -->` and `<!-- conclusions:end -->` removed** (never the prior Conclusions, never another member's sheet, never `meta/history.csv`).
2. **No web search, no outside facts.** Closed-book judgement over the supplied evidence only.
3. Nobody steers the scores: the runner (human or Claude) passes the rubric below verbatim and must not add commentary, hints, examples of "good" scores, or other members' outputs.
4. A member scores every frame question — none skipped, none added.

## Rubric (pass to the member verbatim)

For each key question in `guides/frame.md`, give:

- **`performance`** — integer **−5 … +5**: how strongly the evidence for this question aligns with the thesis. −5 = strongly contradicts · 0 = neutral/mixed/insufficient · +5 = strongly supports.
- **`criticality`** — one of **`critical` · `high` · `medium` · `low`**: how decisive this question is for the thesis, regardless of which way its evidence points. `critical` = if this fails, the thesis fails regardless of the other answers · `high` = materially moves the thesis · `medium` = informative context · `low` = barely bears on the thesis (a `low` consensus signals the question may not belong in the frame).
- **`comment`** — **one sentence**, grounded in the supplied material.

Also give a **`thesis`** line: `performance` −5 … +5 and one sentence on the thesis as a whole, weighing the questions by your own criticality judgements.

## Output — `data/scores/<member>.json`

`<member>` = the harness+model provenance code (ledger convention), e.g. `CwClFable5`, `PxGPT5.6`.

```json
{
  "member": "PxGPT5.6",
  "harness": "Perplexity Computer",
  "model": "GPT-5.6",
  "date": "YYYY-MM-DD",
  "report_version": "<meta.json current_version scored against>",
  "blind": true,
  "answers": [
    {"q": "Q1", "performance": 4, "criticality": "critical", "comment": "…"},
    {"q": "Q2", "performance": 3, "criticality": "high", "comment": "…"}
  ],
  "thesis": {"performance": 2, "comment": "…"}
}
```

## Self-checks (all must pass)

1. Every frame question present exactly once; ids match the frame's numbering (`Q1`…`Q6`).
2. Every `performance` an integer in [−5, +5]; every `criticality` from the validated list; every comment ≤ 1 sentence.
3. `report_version` matches the `meta.json` version of the body scored.
4. The prior Conclusions were **not** in the member's context (`blind: true` asserts this).

## Hand-off

Sheets feed **Build-Conclusions** (`method/code/build_conclusions.py`), which aggregates them deterministically into the scorecard (`data/scorecard.md`; wired into the report's Conclusions after the author approves the frame restructure). Write-Scores never edits the report.
