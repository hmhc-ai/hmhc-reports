# PERPLEXITY.md — the Contributor's job card (currently Perplexity)

> **How to use this file (for the human):** tell the Contributor — *"Read `PERPLEXITY.md` in `hmhc-ai/hmhc-reports` and execute it."* Nothing else needed. The Maintainer (Claude) maintains this file: it queues one job at a time from the gap list (`pipeline/sg-banks/meta/gaps.md`) and rotates it when done.
> **Authorization note:** a job being queued here **is** the author's cost-gate confirmation (`CLAUDE.md` Step 2b) for that one run — the author queues jobs by asking Claude to update this card.
> **Succession note (author, 2026-07-29):** the Contributor seat may move from Perplexity to lab-native harnesses (ChatGPT / Grok / Gemini apps) run directly by the author — the working agreement below binds whoever holds the seat.

## Working agreement (binds the Contributor)

1. If this file says no job is queued, **do nothing**.
2. Write scope: **only** the deliverable path declared in the job card, on a branch named `perplexity/<job>`. Never edit `pipeline/<slug>/method/`, `HUMAN.md`, `reports/`, `CLAUDE.md`, the registry, workflows, or `PERPLEXITY.md` itself.
3. **Always open a pull request; never merge.** The Maintainer reviews, reconciles, runs the build modules, and merges. Questions go in the PR description.
4. Commit trailers per `AGENTS.md` § Commit attribution — name the model that actually ran, printed at run time.
5. A job queued here carries the author's cost-gate authorization for that one run.

## Status: **NO JOB QUEUED** — do not execute anything below the Completed list.

> **Model identity rule (standing, 2026-07-27).** A sheet or dataset is stamped with the model that **actually ran, printed at run time** — never a configured, requested, or menu-label name. Perplexity's **Model Council** (multi-model router: three models + a synthesizer) is **not a valid way to fill non-Claude council seats**: in the 2026-07-27 run every requested seat ("GPT-5.6 Sol", "Gemini 3.1 Pro", "Kimi K3") self-reported **Claude Opus 5** at run time. A job that requires a specific lab's model is only executable when the harness verifiably runs that model; if runtime identity cannot be confirmed, stop and report — exactly as the 2026-07-27 run correctly did.

---

## Completed jobs

- **Job #4 — write-scores (council seats: GPT + Grok)** — **attempted 2026-07-27; closed without merge (PR #45).** Perplexity ran the job via **Model Council**, but every requested seat self-reported **Claude Opus 5** at run time, so no honest GPT or Grok sheet could be produced — the runner correctly refused to commit sheets under false lab identities. The one honest deliverable (`PxClOpus5.json`, blind, thesis +2) was not merged: the roster seats **one member per lab**, and the Claude seat is already held by `CwClFable5`. The three raw Model Council outputs were retained by the author as advisory review context only (all converge on thesis +2). Non-Claude seats will instead be filled by **author-run sessions in each lab's own harness** (ChatGPT / Grok / Gemini apps), with the sheet JSON handed to Claude for validation and commit — no new Perplexity job is planned for scoring.

- **Job #3 — fetch-flows** (wealth-hub capital flows, Frame Q2) — **done 2026-07-25**, delivered in PR #34 (`perplexity/fetch-flows`, 67 rows; BCG booking-centre series as the single share family, regulator series MAS/SFC/SBA as separate never-mixed measures in their own currencies; honest `n/r` on ambiguous UK/UAE early vintages). Reviewed and merged by Claude; Q2 flows table live in `build_benchmarks.py`. Ran on a Claude-family model again (`PxClOpus4.8`) — independence caveat noted in the PR by the runner itself.

- **Job #2 — fetch-peers delta** (NII · NIM · SharePrice · RBC in, CBA out) — **done 2026-07-24**, delivered in PR #30 (`perplexity/fetch-peers-delta`, peers.csv now 100 rows, 10 banks × 10 metrics, stamps `20260724-002 PxClOpus4.8`). Reviewed against independent search anchors (JPM/BofA/UBS/HSBC NII exact) and the ledger's SG rows (NII/NIM exact); merged by Claude; Q5 NII/OR split + Q6 price column live in `build_benchmarks.py`.

- **Job #1 — fetch-peers** (benchmark peer financials, Frame Q5/Q6) — **done 2026-07-24**, delivered in PR #26 (`perplexity/fetch-peers`, 70 rows, 10 banks × 7 metrics, stamp `20260724-001 PxClOpus4.8`). Reviewed, cross-checked against the ledger's SG rows (10/12 exact matches; 2 small deltas flagged), and merged by Claude; `build_benchmarks.py` now computes the full Q5/Q6 indices.

---

## Job queue (next up, not yet authorized — do NOT execute)

- fetch-ledger delta P1 — the 8 never-retrieved `n/r` cells (see `pipeline/sg-banks/meta/gaps.md`).
- fetch-ledger verify P2a — non-Claude verification of the 46-row 1Q2026 block (bundle with the 2Q26 refresh, expected early Aug 2026).
