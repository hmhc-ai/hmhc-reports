# Build-Report-Tables — spec for `build_report_tables.py`

> **Artifact:** `pipeline/sg-banks/method/6-script-build-report-tables.md` — the specification for `build_report_tables.py`; keep the two in sync.
> **Status:** Active. Introduced 2026-07-27 after a hand-transcription error (a swapped CMB column pair, caught in review) showed that manually lifting generated tables into the report is an avoidable risk.

## Module contract

| | |
|---|---|
| **Inputs** | `data/benchmarks.md` (Build-Benchmarks output) · `reports/sg-banks.md` (the marked region). |
| **Sole output** | The region of `reports/sg-banks.md` between `<!-- benchmarks:start -->` and `<!-- benchmarks:end -->` (the Table 6 content), rewritten verbatim from `benchmarks.md`'s three sections with the report's fixed presentation transform: section headings dropped; the flows heading becomes its lead-in sentence. |
| **Executor** | **No model — a deterministic script:** `python3 pipeline/sg-banks/method/6-script-build-report-tables.py`; `--check` verifies the region matches (CI runs it on every PR). |
| **Position** | `Build-Benchmarks → Build-Report-Tables`. Runs whenever Build-Benchmarks output changes; makes the report's lift mechanical instead of manual. |

## Rules

- Everything between the markers is generated — never hand-edit it; change `build_benchmarks.py` (or its inputs) instead, then rerun this module.
- Hand-written content around the markers (the Table 6 heading, the provenance & caveats footnote) is owned by Build-Report/Write-Conclusions and is untouched by this module.
- The Conclusions Q5/Q6/Q2 mini-tables are **not** synced by this module — they are Write-Conclusions outputs with author-approved compressed labels; their numbers must agree with the marked region, which review verifies.
