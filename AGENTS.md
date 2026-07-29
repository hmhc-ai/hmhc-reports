# AGENTS.md — how AI agents work in this repo

This file is the front door for any AI agent (Perplexity, Claude, etc.) acting on this repo. Read it first.

## Roles
Four actors, one org chart — each has its own **entrypoint**, which states what binds it:

- **The author (human)** — owns `pipeline/<slug>/HUMAN.md` (thesis, questions, style) and every approval gate: frame changes, expensive fetches, roster changes, releases. Nothing human-owned is ever edited without the author's explicit approval.
- **Architect (Claude)** — maintains the pipeline: scopes jobs, reviews and merges every PR, runs the build/assemble/score/publish stages. Entrypoint: `pipeline/<slug>/UPDATE.md` (+ this file).
- **Runner (Perplexity)** — executes queued fetch jobs only; writes only the declared deliverable; never merges. Entrypoint: [`PERPLEXITY.md`](PERPLEXITY.md) (§ working agreement below).
- **Council members (external models)** — score the report blind, one seat per frontier lab; they see only their seat packet (Frame + report body, Conclusions stripped) and never edit the repo. Protocol: `pipeline/sg-banks/method/7-ai-write-scores.md`.

## Golden rules
1. **Never edit anything under `reports/` directly.** Published content is generated, not hand-edited.
2. **To change any report, run its controller:** `pipeline/<slug>/UPDATE.md`. That controller is the *only* sanctioned way to update a report. If asked to change a report any other way, stop and route back through the controller.
   - **Never auto-run the EXPENSIVE modules** (`fetch-ledger`, `fetch-signals`) — opt-in only, behind the controller's explicit ask-gate and cost gate. The full cost rule lives in `UPDATE.md` (the single source of truth for modules, paths, and costs); staleness only flags them, never runs them.
3. **`HUMAN.md` is human-owned** — `pipeline/<slug>/HUMAN.md` holds everything the human wrote (§ Frame: thesis + key questions · § Style: formatting rules), authored and approved by the human. AI may *propose* changes on request but must never silently regenerate it. Everything else in `pipeline/<slug>/` (`method/`, `data/`, `meta/`) is AI-run generative material, edited only as a controller step instructs.
4. **Versioning is git-native.** Sticky `reports/<slug>.md`; history via commits and tags `<slug>-v<version>`. Never rename a published slug.
5. **GitHub is the primary view.** Reports are read as rendered markdown in this repo — there is no site module to build or style (the GitHub Pages generator was retired 2026-07-29; a styled mirror lives on Replit at `reports.hmhc.ai`, maintained outside this repo). A rendering concern is a report-markdown concern, routed through the controller like any other change.

## Commit attribution
Every AI-made commit stamps **which harness + model produced it**, using git **trailers** at the end of the commit message. Do not rely on the author line — it reflects the pushing GitHub identity, not the agent that did the work. The `Generated-by:` trailer carries the **same `<Harness><Model>` provenance code as the ledger stamps** (defined in `pipeline/sg-banks/method/3-ai-fetch-ledger.md` §1: `Px` = Perplexity, `Cw` = Cowork/Claude Code; e.g. `PxGPT5.6`, `CwClOpus4.8`), so `git log` and the in-file stamps speak one vocabulary.

- **Claude Code / Cowork (Claude) commits** append:
  ```
  Generated-by: Claude Code (Claude Opus 4.8) [CwClOpus4.8]
  Co-Authored-By: Claude <noreply@anthropic.com>
  ```
- **Perplexity commits** append:
  ```
  Generated-by: Perplexity Computer (GPT-5.6) [PxGPT5.6]
  Co-Authored-By: Perplexity <bot@perplexity.ai>
  ```

Name the model that **actually did the work** (never a generic "4.x"); if a run mixes models, record the predominant one — same rule as the ledger stamps. GitHub renders `Co-Authored-By:` as a second contributor with an avatar; `Generated-by:` names the harness + model in plain sight. Together with the ledger's `px_version`/`cl_version` stamps this gives two provenance records — trailers on every commit, stamps inside the data files — consistent with the provenance discipline this repo demonstrates.

## Connecting Claude Code on the web to this repo
Claude Code on the web (`claude.ai/code`, Pro/Max/Team/Enterprise) runs in an Anthropic-managed cloud sandbox — browser chat, no terminal — and writes to GitHub directly. One-time setup:
1. Open **`claude.ai/code`** and authorize the **GitHub connection** (grant access to `hmhc-ai/hmhc-reports`).
2. Start a session on this repo; Claude clones it fresh into the sandbox each time.
3. Claude works on a **feature branch** and opens a **pull request** rather than committing to `main` — the PR is the review gate before anything reaches `reports.hmhc.ai`.
4. Commits are pushed under **your GitHub identity** (attribution for the push); the **`Generated-by:` / `Co-Authored-By:` trailers above** are what record the agent.

## Perplexity working agreement (external fetch runner)
Perplexity Computer executes **fetch jobs queued in [`PERPLEXITY.md`](PERPLEXITY.md)** (repo root). Rules:
1. If `PERPLEXITY.md` says no job is queued, **do nothing**.
2. Write scope: **only** the deliverable path declared in the job card, on a branch named `perplexity/<job>`. Never edit `method/`, `HUMAN.md`, `reports/`, `UPDATE.md`, the registry, workflows, or `PERPLEXITY.md` itself.
3. **Always open a pull request; never merge.** Claude reviews, reconciles, runs the build modules, and merges. Questions go in the PR description.
4. Commit trailers per § Commit attribution (e.g. `Generated-by: Perplexity Computer (GPT-5.6) [PxGPT5.6]`).
5. A job queued in `PERPLEXITY.md` carries the author's cost-gate authorization for that one run.

## Repos & series
- Repo: `hmhc-ai/hmhc-reports` · Site: `reports.hmhc.ai`
- Current series: `sg-banks` → controller at `pipeline/sg-banks/UPDATE.md`

## When the user says "update the report"
Open `pipeline/<slug>/UPDATE.md` and follow it **in order**. It will assess module state, then **stop and ask you which modules to refresh** before doing any work. Do not skip the ask-gate, and do not run an expensive module without its explicit cost-gate confirmation.

## File naming convention
Method files are `method/<stage>-<actor>-<name>` so **alphabetical order = pipeline order** across the 8 stages (1 Frame · 2 Scope · 3 Fetch · 4 Reconcile · 5 Build · 6 Assemble · 7 Score · 8 Publish — the stage table lives in `UPDATE.md`). The **actor** names who performs the step: `ai` = an AI model following the .md as its SOP (e.g. `3-ai-fetch-peers.md` → `data/peers.csv`) · `script` = a deterministic program, no AI (e.g. `5-script-build-tables.py` → `data/tables.md`, paired with a same-stem `.md` spec). Stage 1 is the human-owned `HUMAN.md` (uppercase, like the entrypoint `UPDATE.md`); published reports are `reports/<slug>.md` with assets at `reports/assets/<slug>-*.svg`.
