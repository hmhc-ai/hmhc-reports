# CLAUDE.md — the Maintainer's operating manual

Claude is this repo's **Maintainer** (roles: `README.md` § Governance): it maintains the pipeline, reviews and merges every pull request, and runs the build/assemble/score/publish stages. This file is Claude's entrypoint and **the controller for any change to a published report** — what was previously `pipeline/<slug>/UPDATE.md`. Ground rules and commit trailers: `AGENTS.md`.

## ⚠ Cost rule (read first)

Every **`fetch-` module is EXPENSIVE** (live web retrieval, token/time-intensive). They are **opt-in only**:
- **Never run by default** and **never triggered automatically by staleness** — staleness only *flags* them, it never *runs* them.
- They run **only** when BOTH are true: (1) the user **explicitly names** the module, and (2) the user **reconfirms at the cost gate** (Step 2b) in chat.
- No explicit confirmation ⇒ skip that module and continue with the rest.

## HUMAN.md (human-owned) vs modules (agent-run)

Root **`HUMAN.md`** contains everything the human wrote — per report: `<slug> · Frame` (thesis + key factors; the per-factor formats are MUST-includes — Scope may propose *additional* analysis per factor, never replace them; scripts/packets extract the Frame via the `frame:<slug>:start/end` markers) and `<slug> · Style` (formatting & marking rules). The author writes and approves it; Claude may *propose* wording on request but never edits it without explicit author approval. Everything under `pipeline/` and `reports/` is agent-made.

**The 8-stage pipeline.** Every module belongs to exactly one stage; filenames are `<stage>-<actor>-<name>` so **alphabetical order = pipeline order** (`ai` = performed by an AI model · `script` = a deterministic program, same input → same output). Stage 1 is `HUMAN.md` itself; simple updates legitimately skip stages.

| # | Stage | Actor | What it does |
|---|---|---|---|
| 1 | Frame | human (Author) | judgment → `HUMAN.md` (thesis, factors, style) |
| 2 | Scope | script + Maintainer + author gate | what we have / what's missing → the `PERPLEXITY.md` job card (a queued card = the author's cost authorization) |
| 3 | Fetch | AI (EXPENSIVE, opt-in) | live web → `data/` files |
| 4 | Reconcile | AI | raw data → reconciled columns + source grades |
| 5 | Build | script | data → components (tables, charts, benchmarks) |
| 6 | Assemble | AI body + script region-syncs | components → report body |
| 7 | Score | blind council + script aggregation | body (Conclusions stripped) → sheets → Conclusions overlay |
| 8 | Publish | script | version, changelog, history rows, all gates |

The report is **body + generated overlay regions** (Table 6, Conclusions, Appendix E): the body is assembled in stage 6 *before* scoring, the council reads the body only, and scores flow back into the overlay — a DAG, never a cycle.

## Report: sg-banks — module table

| Module | Method file | Output artifact | Cost | Depends on |
|---|---|---|---|---|
| Build-Health | `pipeline/sg-banks/method/2-script-build-health.md` (spec) + `pipeline/sg-banks/method/2-script-build-health.py` | `pipeline/sg-banks/meta/health.md` + `health.json` | cheap | any data change |
| Build-Gaps | `pipeline/sg-banks/method/2-script-build-gaps.md` (spec) + `pipeline/sg-banks/method/2-script-build-gaps.py` | `pipeline/sg-banks/meta/gaps.md` + `gaps.json` | cheap | any data change |
| Fetch-Ledger | `pipeline/sg-banks/method/3-ai-fetch-ledger.md` | `pipeline/sg-banks/data/ledger.csv` (retriever columns) | **EXPENSIVE — opt-in** | Frame |
| Fetch-Signals | `pipeline/sg-banks/method/3-ai-fetch-signals.md` | `pipeline/sg-banks/data/signals.md` | **EXPENSIVE — opt-in** | Frame |
| Fetch-Flows | `pipeline/sg-banks/method/3-ai-fetch-flows.md` | `pipeline/sg-banks/data/flows.csv` | **EXPENSIVE — opt-in** | Frame |
| Fetch-Peers | `pipeline/sg-banks/method/3-ai-fetch-peers.md` | `pipeline/sg-banks/data/peers.csv` | **EXPENSIVE — opt-in** | Frame |
| Reconcile | `pipeline/sg-banks/method/4-ai-reconcile-ledger.md` | `reconciled_*` columns of `pipeline/sg-banks/data/ledger.csv` | cheap | Fetch-Ledger |
| Build-Tables | `pipeline/sg-banks/method/5-script-build-tables.md` (spec) + `pipeline/sg-banks/method/5-script-build-tables.py` | `pipeline/sg-banks/data/tables.md` | cheap | Reconcile |
| Build-Charts | `pipeline/sg-banks/method/5-script-build-charts.md` (spec) + `pipeline/sg-banks/method/5-script-build-charts.py` | `reports/assets/sg-banks-*.svg` | cheap | Reconcile |
| Build-Benchmarks | `pipeline/sg-banks/method/5-script-build-benchmarks.md` (spec) + `pipeline/sg-banks/method/5-script-build-benchmarks.py` | `pipeline/sg-banks/data/benchmarks.md` | cheap | Reconcile (+ Fetch-Peers/Fetch-Flows when run) |
| Build-Report | `pipeline/sg-banks/method/6-ai-build-report.md` | `reports/sg-banks.md` (the body) | cheap | Build-Tables, Frame, Fetch-Signals, Style |
| Build-Report-Tables | `pipeline/sg-banks/method/6-script-build-report-tables.md` (spec) + `pipeline/sg-banks/method/6-script-build-report-tables.py` | benchmarks-marked region of `reports/sg-banks.md` | cheap | Build-Benchmarks |
| Build-AI-Notes | `pipeline/sg-banks/method/6-script-build-ai-notes.md` (spec) + `pipeline/sg-banks/method/6-script-build-ai-notes.py` | ai-notes-marked region of `reports/sg-banks.md` (Appendix E) | cheap | any data change |
| Write-Scores | `pipeline/sg-banks/method/7-ai-write-scores.md` | `pipeline/sg-banks/data/scores/<member>.json` (one per council member, blind) | cheap per member; author authorizes the roster | Build-Report (current body) |
| Build-Conclusions | `pipeline/sg-banks/method/7-script-build-conclusions.md` (spec) + `pipeline/sg-banks/method/7-script-build-conclusions.py` | `pipeline/sg-banks/data/scorecard.md` + the report's Conclusions markers | cheap | Write-Scores |
| Publish | `pipeline/sg-banks/method/8-script-publish.md` (spec) + `pipeline/sg-banks/method/8-script-publish.py` | version/changelog/history bookkeeping in `reports/index.json` + registry + `pipeline/sg-banks/meta/` | cheap | all gates |

Model per module: all Fetch-* → non-Claude search-grounded by design for independence; Reconcile → human + Claude; every `script` module → deterministic program (no model); Build-Report → Claude; Write-Scores → the council roster (latest knowledge-work frontier model per major lab, blind, one seat per lab).

---

## The controller — follow Steps 1–6 in order for any report change

> Do not edit `reports/` directly. Stop at the Step 2 gate to ask the user, and never auto-run an EXPENSIVE module. Never assume which modules to run.

### Step 1 — Assess state (always print; never skip)

For each **module** classify: **MISSING** (method file or output absent) · **STALE** (an upstream output committed more recently than this output — `git log -1 --format=%cI -- <path>`) · **DATA-AGE** (fetch modules only — last retrieval date vs today; new quarter closed ⇒ "possibly outdated") · **OK**.
For **`HUMAN.md`** (Frame + Style): report as *human-owned*; never mark STALE or auto-refresh.

Output a table: `item | type (human/module) | cost | status | reason`. **Flagging an EXPENSIVE module as STALE/DATA-AGE does not authorize running it** — it only informs the user.

### Step 2 — GATE: ask the user (mandatory stop)

Present the table, then ask:
> "Which modules would you like to refresh? Cheap/suggested: [list]. **Expensive (needs explicit confirm): any fetch- module.** Or reply **none** to just refresh the report (lite). Also: revise your **Frame** or **Style** (`HUMAN.md`)? I can propose, you approve."

**Do not proceed until the user answers.**

### Step 2b — COST GATE (only if an EXPENSIVE module was named)

For each expensive module the user selected, ask a **second, explicit confirmation**:
> "Running **<module>** does live web retrieval and is token/time-intensive. Confirm you want to run it now? (yes / no)"

Run it **only** on an explicit "yes". On "no" or anything ambiguous, **skip that module** and continue. Do not batch-assume a single "yes" covers both — confirm each expensive module.

### Step 3 — Run the selected path

- **`HUMAN.md` revised (Frame/Style):** human edit — Claude may propose wording, human approves; then rerun downstream (Frame ⇒ Build-Report ⇒ council rescore; Style ⇒ Build-Report presentation).
- **Modules named (and confirmed where expensive):** run in stage order (Fetch → Reconcile → Build → Assemble → Score), honoring the current `HUMAN.md`. Refreshing any module forces rerun of everything downstream of it.
- **"none":** run the **LITE path** only — rerun the **council** (Write-Scores per `pipeline/sg-banks/method/7-ai-write-scores.md` for the authorized roster, then `pipeline/sg-banks/method/7-script-build-conclusions.py` to reassemble the Conclusions scorecard) and apply **Style**. Writes only `data/scores/` + `data/scorecard.md` + the Conclusions markers. **The lite path is the default and never invokes an expensive module.**

Always finish with **Publish** (Step 5).

### Step 4 — Gates before publishing (all must pass)

- **Build-Report:** arithmetic tie-outs pass; every **Frame** factor is analyzed in the report.
- **Council:** every authorized member's sheet present and valid (Write-Scores self-checks); `7-script-build-conclusions.py --check` green (scorecard + report Conclusions in sync); every Frame factor analyzed in Supporting Data or explicitly marked pending.
- Every refreshed module's output exists and is committed.

### Step 5 — Publish (one command + PR)

- **Run `python3 pipeline/sg-banks/method/8-script-publish.py --desc "<one-sentence release note>" [--changelog "<rich changelog entry>"]`.** It computes the next version (`YYYY.MM.DD`, `-rN` for same-day re-releases), updates this report's entry in `reports/index.json` (`current_version`, `last_updated`, `refresh_note`), inserts the changelog entry at the top of the registry, appends the release row to `pipeline/sg-banks/meta/history.csv` and the full sheets to `history_scores.jsonl`, and runs every CI gate. `--dry-run` previews.
- **Narrative convention:** the registry changelog (`pipeline/sg-banks/index.md`) is the **canonical release history**; `refresh_note` carries only the current release's note plus a pointer; commit messages and PR bodies stay terse and defer to the changelog.
- **Only a change to the published report warrants a version bump** — pipeline/meta-only changes ship without one (and skip publish).
- Commit (trailers per `AGENTS.md`), open the PR, merge on green CI. The tag `sg-banks-v<version>` is **auto-created on `main` by the tag-version GitHub Action** when the registry's version changes — never tag manually.

### Step 6 — Report back

State: the assessment, which of HUMAN.md/modules changed, whether any expensive module was run (and that it was explicitly confirmed), gates passed, new version + tag.

---

## Enforcement note

Convention-enforced: works only if every change starts here (via `AGENTS.md` → this file). It cannot physically stop a rogue edit or an unconfirmed expensive run — for hard enforcement move Steps 1–5 into code (GitHub Actions `workflow_dispatch`), where the cost gate becomes a required input parameter.
