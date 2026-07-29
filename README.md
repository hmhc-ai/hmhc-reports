# HMHC Reports

The reports are published and read **directly in this repo** — GitHub's native markdown rendering is the primary view (use the outline menu at the top-right of any report for section navigation). A styled mirror lives at **[reports.hmhc.ai](https://reports.hmhc.ai)**.

Each report is a self-contained, source-graded business analysis produced with a disciplined, AI-assisted **modular pipeline**. Reports are **sticky** (a stable URL always shows the latest version) and **versioned** (full history in git commits, tags, and releases).

## Layout

```
reports/      The published reports — what a reader opens.
  <slug>.md         One file per report (e.g. sg-banks.md), always the latest
                    version; generated regions (tables, Conclusions) live
                    between markers inside it.
  index.json        Registry of all reports: title, status, dates, version,
                    current release note.
  assets/           Charts and images (<slug>-*.svg).

pipeline/     How each report is made. Not published.
  <slug>/
    UPDATE.md       Controller — the single entrypoint for any change, and the
                    single source of truth for modules, method files, and costs.
    HUMAN.md        Human-owned — everything the human wrote: § Frame (thesis +
                    key questions) and § Style (formatting & marking rules).
    index.md        Registry of decisions and history: standing decisions,
                    open questions, changelog.
    method/         One file per pipeline step, named <stage>-<actor>-<name> so
                    alphabetical order = pipeline order: 2-script-build-gaps.py,
                    3-ai-fetch-peers.md, … 8-script-publish.py. "ai" steps run
                    on AI models; "script" steps are deterministic programs
                    (each .py pairs with a same-stem .md spec).
    data/           Working data: ledger.csv (reconciliation master), peers.csv,
                    flows.csv, signals.md, generated tables/benchmarks, and
                    scores/ (the blind council answer sheets).
    meta/           Pipeline-about-itself: health.md/json (completeness &
                    confidence), gaps.md/json (worklist), history files.

HOW-ITS-BUILT.md  The outsider's tour: agents, stages, provenance, council.
PERPLEXITY.md     Job card for the external fetch runner (see AGENTS.md).
IDEAS.md          Author ↔ Claude improvement brainstorm — nothing in it is
                  authorized for implementation until explicitly approved.
```

## Pipeline

Eight fixed stages — **1 Frame (human) → 2 Scope → 3 Fetch → 4 Reconcile → 5 Build → 6 Assemble → 7 Score → 8 Publish** — with every module belonging to exactly one stage and the stage number leading its filename. Fetch stages are **expensive** (live web retrieval) and strictly opt-in behind a cost gate; the Score stage is a blind multi-model council. Every module has one SOP in `method/`, explicit inputs, one output, and is **idempotent** (rerunning overwrites its output; git retains history). The full narrative with a process diagram is in [`HOW-ITS-BUILT.md`](HOW-ITS-BUILT.md).

The module table — method files, outputs, costs, dependencies, and the cost gates — lives in **`pipeline/<slug>/UPDATE.md`**, the controller every change must route through. Do not duplicate it here.

## Reports

| Series | Slug | Status |
|---|---|---|
| Analysis of Singapore Banks (DBS · OCBC · UOB) | `sg-banks` | Published |

## Adding a new report

1. Create `reports/<slug>.md` (the report) and put its charts in `reports/assets/` as `<slug>-*.svg`.
2. Create `pipeline/<slug>/` with `UPDATE.md`, `HUMAN.md`, `index.md`, `method/` (the stage-numbered module SOPs), and `data/`.
3. Add the report's entry to `reports/index.json`.
4. Commit and merge; the tag `<slug>-v<version>` is auto-created on `main` by the tag-version workflow.

## Versioning

`report.md` is overwritten in place, so its URL never changes. History lives in git: `git log`, `git blame`, tags, and GitHub Releases for public, dated milestones. Versions are `YYYY.MM.DD` of the publish date; a same-day re-release appends `-r2`, `-r3`, … (e.g. `sg-banks-v2026.07.20-r2`).

## Conventions

Slugs and filenames are lowercase-hyphenated and permanent — never rename a published slug, it breaks links and bookmarks. Files are named for what they contain, not their format. Figures stay in the report's stated currency; sources are Tier-1 filings; no estimates or memory-fills. AI agents start at `AGENTS.md`; every AI commit carries the attribution trailers defined there.
