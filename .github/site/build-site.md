# Build-Site — spec for `build_site.py` (static site generator)

> **Artifact:** `.github/site/build-site.md` — the specification for `.github/site/build_site.py`; keep the two in sync.
> **Status:** Active — TEST deployment. The site deploys to `https://hmhc-ai.github.io/hmhc-reports/` only; **no custom domain is configured** (the author is comparing against a Replit-hosted alternative before deciding where reports.hmhc.ai points).

## Module contract

| | |
|---|---|
| **Inputs** | `reports.json` (series index) · `reports/<slug>/report.md` + `meta.json` + `assets/` · `pipeline/<slug>/meta/health.json` + `gaps.json` · `pipeline/<slug>/data/*.csv` + `benchmarks.md` · `.github/site/style.css`. |
| **Sole output** | `_site/` — self-contained static HTML (landing page · one report page per series · workflow-dashboard page · data page with sortable CSV tables). Never committed (`.gitignore`); built fresh per deploy. |
| **Executor** | **No model — a deterministic script:** `python3 .github/site/build_site.py` (dep: `pip install markdown`). No timestamps, no network, no CDN dependencies — same inputs in, same site out. |
| **Deploy** | `.github/workflows/pages.yml` — on every push to `main`, build + deploy via the official GitHub Pages actions. Publishing a report version *is* deploying the site. |
| **CI** | docs-lint runs the build on every PR — a site-breaking content change fails the PR. |

## Rules

- **Markdown rendering is owned here** (Python-Markdown, `tables` extension) — the renderer that broke `<sub>` on the old host is irrelevant; published files stay pure markdown per `guides/style.md`.
- Design: hand-written `style.css`, light/dark via `prefers-color-scheme`, no frameworks. The only JavaScript is the ~20-line client-side column sorter for CSV tables.
- Dashboard values come **only** from `meta/health.json` / `meta/gaps.json` (themselves CI-verified pipeline outputs) — the site never computes analytics of its own.
- `ledger.csv` is truncated to the first 100 rows on the data page (full file linked on GitHub); other CSVs render in full.
- The site is a **generated artifact**: never hand-edit `_site/`; change the builder or the content instead.
