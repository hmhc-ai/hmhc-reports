# Build-AI-Notes — spec for `6-script-build-ai-notes.py` (machine-oriented evidence appendix)

> **Artifact:** `pipeline/sg-banks/method/6-script-build-ai-notes.md` — the specification for `method/6-script-build-ai-notes.py`; keep the two in sync.
> **Stage:** 6 (Assemble — a script region-sync, like Build-Report-Tables).
> **Changelog:** 2026-07-29 — first version (author-approved idea: "notes for AI" — since the council context window is ample, hand members the full evidence base, not just the narrated subset).

| | |
|---|---|
| **Inputs** | `data/ledger.csv` · `data/peers.csv` · `data/flows.csv` · `meta/gaps.json` |
| **Output** | The region between `<!-- ai-notes:start -->` / `<!-- ai-notes:end -->` in `reports/sg-banks.md` — **Appendix E — AI reference data**. |
| **Executor** | Deterministic script, no AI, no clocks: same inputs in, same region out. CI runs `--check` on every PR and fails if the region drifts from the data files. |

## Why it exists

The report body is written for humans (~15k tokens); every council member's context window is 200k+. This appendix closes that gap: the **full evidence base in flat, machine-friendly form** rides inside the report, so blind council members (and any other AI reader) score from the data itself — not only the human-narrated subset. It goes to every member identically; the blind protocol is unchanged.

## Content (fixed order)

1. A header note: machine-readers audience, humans can stop here, generated + CI-verified, never hand-edited.
2. **Canonical definitions & principles** — CA, OR, currency principle, HSBC=100 indexing, offshore-wealth definition, cell marking.
3. **E.1** Reconciled ledger *projection* (`data_point_id, period, unit, reconciled_value, reconciliation_status`) in a fenced `csv` block — the full 153KB ledger with per-cell sources stays in `data/ledger.csv` (linked); embedded commas become `;`.
4. **E.2** `data/peers.csv` verbatim (fenced `csv`).
5. **E.3** `data/flows.csv` verbatim (fenced `csv`).
6. **E.4** Open gaps from `meta/gaps.json` — priority, count, note, row ids per gap class.

## Rules

- Flat and unstyled on purpose — fenced code blocks, not markdown tables; this appendix is exempt from the Style guide's table conventions (it is not a human table).
- Nothing in the appendix may be new analysis: it is a projection/copy of existing pipeline files only.
- Always the **last** section of the report, after Appendix D.
- Rerun after any data-file or gaps change; `--check` is a publish gate and a CI gate.
