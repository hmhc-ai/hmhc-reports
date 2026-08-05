# AGENTS.md — entry file for AI agents

You are an AI agent working in this repo. **`README.md` § Architecture and § Governance bind you** — read them first. Then your role file:

- **Maintainer** (Claude) → `CLAUDE.md` — the operating manual and the controller for any report change.
- **Contributor** (external fetch agent; currently Perplexity) → [`PERPLEXITY.md`](PERPLEXITY.md) — the job card and working agreement. If it says no job is queued, do nothing.
- **Council members** → you receive a sealed seat packet; you never read or edit the repo.

`HUMAN.md` is human-owned: propose changes only on request, never edit without the Author's explicit approval. Never edit anything under `reports/` directly. When the user says "update the report", the Maintainer follows `CLAUDE.md` § The controller, in order, honoring its ask-gate and cost-gate.

## Commit attribution

Every AI-made commit stamps **which harness + model produced it**, using git **trailers** at the end of the commit message. Do not rely on the author line — it reflects the pushing GitHub identity, not the agent that did the work. The `Generated-by:` trailer carries the **same `<Harness><Model>` provenance code as the ledger stamps** (defined in `pipeline/sg-banks/method/3-ai-fetch-ledger.md` §1: `Px` = Perplexity, `Cw` = Cowork/Claude Code, `Gk` = Grok app; e.g. `PxGPT5.6`, `CwClOpus4.8`), so `git log` and the in-file stamps speak one vocabulary.

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

Name the model that **actually did the work, printed at run time** (never a generic "4.x", never a configured or menu-label name); if a run mixes models, record the predominant one — same rule as the ledger stamps. Together with the data files' in-row stamps this gives two provenance records — trailers on every commit, stamps inside the files.

## File naming convention

Method files are `pipeline/<slug>/method/<stage>-<actor>-<name>` so **alphabetical order = pipeline order** across the 8 stages (stage table in `CLAUDE.md`). The **actor** names who performs the step: `ai` = an AI model following the .md as its SOP · `script` = a deterministic program, no AI (each .py pairs with a same-stem `.md` spec). Root docs are uppercase (`README.md`, `CLAUDE.md`, `AGENTS.md`, `HUMAN.md`, `PERPLEXITY.md`, `IDEAS.md`); published reports are `reports/<slug>.md` with assets at `reports/assets/<slug>-*.svg`.
