# sg-banks — UPDATE (ENTRYPOINT controller)

> **This is the single entrypoint for any change to the sg-banks report.**
> Do not edit `reports/sg-banks/*` directly. Follow Steps 1–6 **in order**, **stop at the Step 2 gate to ask the user**, and **never auto-run an EXPENSIVE module** (see the cost rule below). Never assume which modules to run.

## ⚠ Cost rule (read first)
Every **`fetch-` module is EXPENSIVE** (live web retrieval, token/time-intensive): **`fetch-ledger`**, **`fetch-signals`**, **`fetch-flows`**, **`fetch-peers`**. They are **opt-in only**:
- They are **never run by default** and **never triggered automatically by staleness** — staleness only *flags* them, it never *runs* them.
- They run **only** when BOTH are true: (1) the user **explicitly names** the module, and (2) the user **reconfirms at the cost gate** (Step 2b) in chat.
- No explicit confirmation ⇒ skip that module and continue with the rest.

## Guides (human-owned) vs Modules (AI-run)

**Guides — the human owns these; AI only advises.** Constrain the modules; never auto-generated.

| Guide | File | Purpose |
|---|---|---|
| **Frame** | `guides/frame.md` | Your big questions the report must answer. AI may propose candidates on request; you author/approve. |
| **Style** | `guides/style.md` | Formatting & marking rules. You own them; AI applies them. |

**Modules.** `method/ai/` holds steps performed by AI models; `method/code/` holds steps performed by deterministic programs (no AI — same input, same output). The **verb is the execution category**: `fetch-` = live web (EXPENSIVE, opt-in) · `reconcile-` = human+AI cross-check · `build-` = assembly, low insight · `write-` = insight/synthesis.

| Module | Method file | Output artifact | Cost | Depends on |
|---|---|---|---|---|
| Fetch-Ledger | `method/ai/fetch-ledger.md` | `data/ledger.csv` (retriever columns) | **EXPENSIVE — opt-in** | Frame |
| Fetch-Signals | `method/ai/fetch-signals.md` | `data/signals.md` | **EXPENSIVE — opt-in** | Frame |
| Fetch-Flows | `method/ai/fetch-flows.md` | `data/flows.csv` | **EXPENSIVE — opt-in** | Frame |
| Fetch-Peers | `method/ai/fetch-peers.md` | `data/peers.csv` | **EXPENSIVE — opt-in** | Frame |
| Reconcile | `method/ai/reconcile-ledger.md` | `reconciled_*` columns of `data/ledger.csv` | cheap | Fetch-Ledger |
| Build-Tables | `method/code/build-tables.md` (spec) + `method/code/build_tables.py` (executable) | `data/tables.md` | cheap | Reconcile |
| Build-Charts | `method/code/build-charts.md` (spec) + `method/code/build_charts.py` (executable) | `reports/sg-banks/assets/*.svg` | cheap | Reconcile |
| Build-Benchmarks | `method/code/build-benchmarks.md` (spec) + `method/code/build_benchmarks.py` (executable) | `data/benchmarks.md` | cheap | Reconcile (+ Fetch-Peers/Fetch-Flows when run) |
| Build-Health | `method/code/build-health.md` (spec) + `method/code/build_health.py` (executable) | `meta/health.md` + `meta/health.json` | cheap | any data change |
| Build-Gaps | `method/code/build-gaps.md` (spec) + `method/code/build_gaps.py` (executable) | `meta/gaps.md` + `meta/gaps.json` | cheap | any data change |
| Build-Report | `method/ai/build-report.md` | `reports/sg-banks/report.md` | cheap | Build-Tables, Frame, Fetch-Signals, Style |
| Build-Report-Tables | `method/code/build-report-tables.md` (spec) + `method/code/build_report_tables.py` (executable) | benchmarks-marked region of `reports/sg-banks/report.md` | cheap | Build-Benchmarks |
| Write-Scores | `method/ai/write-scores.md` | `data/scores/<member>.json` (one per council member, blind) | cheap per member; author authorizes the roster | Build-Report (current body) |
| Build-Conclusions | `method/code/build-conclusions.md` (spec) + `method/code/build_conclusions.py` (executable) | `data/scorecard.md` (stage 1; report wiring awaits frame approval) | cheap | Write-Scores |
| Write-Conclusions | RETIRED 2026-07-27 — replaced by Write-Scores + Build-Conclusions (`method/ai/write-conclusions.md` kept for history) |  |  |  |
| Publish | (this controller) | `reports/sg-banks/meta.json` | cheap | Write-Conclusions |

Model per module: all Fetch-* → non-Claude search-grounded (Perplexity Computer / GPT-class, by design for independence); Reconcile → human + Claude; Build-Tables/Build-Charts/Build-Benchmarks/Build-Health/Build-Gaps → deterministic scripts (no model); Build-Report → Claude; Write-Scores → the council roster (latest knowledge-work frontier model per major lab, blind); Build-Conclusions → deterministic script (no model).

---

## Step 1 — Assess state (always print; never skip)

For each **module** classify: **MISSING** (method file or output absent) · **STALE** (an upstream output committed more recently than this output — `git log -1 --format=%cI -- <path>`) · **DATA-AGE** (fetch modules only — last retrieval date vs today; new quarter closed ⇒ "possibly outdated") · **OK**.
For **guides** (Frame, Style): report as *human-owned*; never mark STALE or auto-refresh.

Output a table: `item | type (guide/module) | cost | status | reason`. **Flagging an EXPENSIVE module as STALE/DATA-AGE does not authorize running it** — it only informs the user.

## Step 2 — GATE: ask the user (mandatory stop)

Present the table, then ask:
> "Which modules would you like to refresh? Cheap/suggested: [list]. **Expensive (needs explicit confirm): any fetch- module.** Or reply **none** to just refresh the report (lite). Also: revise your **Frame** or **Style**? I can propose, you approve."

**Do not proceed until the user answers.**

## Step 2b — COST GATE (only if an EXPENSIVE module was named)

For each expensive module the user selected, ask a **second, explicit confirmation**:
> "Running **<module>** does live web retrieval and is token/time-intensive. Confirm you want to run it now? (yes / no)"

Run it **only** on an explicit "yes". On "no" or anything ambiguous, **skip that module** and continue. Do not batch-assume a single "yes" covers both — confirm each expensive module.

## Step 3 — Run the selected path

- **Guide revised (Frame/Style):** human edit — AI may propose wording, human approves; write to `guides/frame.md` / `guides/style.md`; then rerun downstream (Frame ⇒ Build-Report ⇒ Write-Conclusions; Style ⇒ Build-Report/Write-Conclusions presentation).
- **Modules named (and confirmed where expensive):** run in dependency order (Fetch-Ledger ‖ Fetch-Signals → Reconcile → Build-Tables → Build-Report), honoring current Frame & Style. Refreshing any module forces rerun of everything downstream of it.
- **"none":** run the **LITE path** only — rerun the **council** (Write-Scores per `method/ai/write-scores.md` for the authorized roster, then `method/code/build_conclusions.py` to reassemble the Conclusions scorecard) and apply **Style** (`guides/style.md`). Writes only `data/scores/` + `data/scorecard.md` + the Conclusions markers. **The lite path is the default and never invokes an expensive module.**

Always finish with **Publish** (Step 5).

## Step 4 — Gates before publishing (all must pass)
- **Build-Report:** arithmetic tie-outs pass; every **Frame** question is addressed in the report.
- **Council:** every authorized member's sheet present and valid (Write-Scores self-checks); `build_conclusions.py --check` green (scorecard + report Conclusions in sync); every Frame question answered in Supporting Data or explicitly marked pending.
- Every refreshed module's output exists and is committed.

## Step 5 — Publish (one command + PR)
- **Run `python3 method/code/publish.py --desc "<one-sentence release note>" [--changelog "<rich changelog entry>"]`.** It computes the next version (`YYYY.MM.DD`, `-rN` for same-day re-releases), updates `reports/sg-banks/meta.json` (`current_version`, `last_updated`, `refresh_note`), inserts the changelog entry at the top of the registry, appends the release row to `meta/history.csv` (version, date, thesis score, health metrics — the score/quality time series), and runs every CI gate. `--dry-run` previews.
- **Narrative convention:** the registry changelog is the **canonical release history**; `refresh_note` carries only the current release's note plus a pointer; commit messages and PR bodies stay terse and defer to the changelog.
- **Only a change to the published report warrants a version bump** — pipeline/meta/site-only changes ship without one (and skip publish.py).
- Commit (trailers per `AGENTS.md` § Commit attribution), open the PR, merge on green CI. The tag `sg-banks-v<version>` is **auto-created on `main` by the tag-version GitHub Action** when `meta.json`'s version changes — never tag manually.

## Step 6 — Report back
State: the assessment, which guides/modules changed, whether any expensive module was run (and that it was explicitly confirmed), gates passed, new version + tag.

---

## Enforcement note
Convention-enforced: works only if every change starts here (via `AGENTS.md`). It cannot physically stop a rogue edit or an unconfirmed expensive run — for hard enforcement move Steps 1–5 into code (GitHub Actions `workflow_dispatch`), where the cost gate becomes a required input parameter.
