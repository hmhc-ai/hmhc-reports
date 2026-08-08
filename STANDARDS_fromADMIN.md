# STANDARDS_fromADMIN.md — the org operating standard (vendored copy)

> **Read-only copy, vendored from `ming-admin/STANDARDS.md` — version
> 2026.08.08.** The ADMIN Maintainer is the ONLY writer of this file: it
> is replaced wholesale on each standards release, so any local edit
> will be lost — never edit it from this repo. It is binding here as-is,
> even if a newer version exists at the source. To propose a change, use
> this repo's `## Upstream (for admin)` section in `CLAUDE.md` (or raise
> it with the Owner if this repo has no entry file) — never edit this
> copy.

The **org-agnostic layer** of this runbook: the principles behind the
agentic way of working, role vocabulary, document standards, handoff
protocol, repo recipes, and the patterns this org has adopted and
proven. **Sanitized by construction** — no real access data, no
credentials, no personal detail; org, repo, and product names appear
only as examples. This file is the future public demonstrator and the
export for client-org engagements: hand a new org this file, keep its
own `ADMIN.md` for everything org-specific (registry, API register,
environments, access map).

Maintained in `ming-admin` by the org's Maintainer session. `ADMIN.md`
references this file instead of duplicating it; where the two disagree,
`ADMIN.md`'s org-specific decisions win inside this org. Sections are
referenced **by name** (headings are the anchors); numbering is not
load-bearing.

**Current version: 2026.08.08.** Every other org repo carries a
read-only copy, `STANDARDS_fromADMIN.md`, stamped with the version it
was cut from and replaced wholesale on each **standards release** — see
*Entry files & vendoring*.

---

# Foundations

## Section anatomy (a general guide for .md documents)

> **What:** the shape any `.md` section in the org may take. **Why:** so
> a reader — human or agent — can tell binding standard from unratified
> suggestion from history at a glance, and so a session adding content
> knows where it goes instead of appending it wherever it fits.
> **Style:** the guide governs itself — read this section as its own
> worked example. As the Owner put it (2026-08-07), this is *a general
> guide*, not a rigid template: the inclusion threshold matters more
> than the four-part shape.

A general guide for **all `.md` documents except `CHANGELOG.md`**. The
pattern fits wherever human × agent co-authorship is substantial — the
Owner-ideas → Maintainer-copywriter pattern — which includes
`HUMAN.md`. The changelog is the one exception because it is a
different kind of artifact: an **agent-intercommunication protocol and
tool** (append-only; the dated entry is its unit), not a co-authored
document.

Each section **or subsection** carries up to four components, in this
order — and every piece of content must clear a **threshold for
inclusion**: space is valuable, and below-threshold content is cut,
not footnoted.

1. **Meta quoteblock** (`>`) — optional, used selectively where
   elaboration earns its place: the **Maintainer's understanding of
   the what, the why, and the style** of the body content below — the
   interpretive frame that keeps future sessions faithful to intent.
   It is perfectly valid (often best) for that understanding to be
   anchored in provenance: *"as the Owner explicitly said …"*, with
   the date and status flags (*draft*, *adopted*, *interpretation
   unconfirmed*).
2. **Main body** — the substance: the Owner's ideas in tightened
   wording, elaborated where needed, conflicting points resolved. This
   is the only binding component.
3. **Maintainer suggestions** — clearly marked recommendations the
   Owner has not (yet) ratified. Sufficiently segmented from the
   Owner's points that the component is welcome even in `HUMAN.md`.
   Kept short; adopted suggestions move up into the body, rejected
   ones are deleted.
4. **Footnotes** — a small-text line at the section's end (`<sub>`)
   for history and asides: renames, superseded wording, minor caveats.
   Nothing binding lives in a footnote.

Most sections need only the body; add the other components when they
earn their place.

## Role vocabulary

| Role | Who | Owns |
|---|---|---|
| **Owner** | human | each repo's `HUMAN.md` charter + all policy decisions; the only actor whose files agents never edit unasked |
| **Maintainer** | the org's current favorite frontier agent | maintains the repo, integrates all other actors' work, reviews and merges |
| **Contributor** | any other tool or model | scoped execution only: its declared deliverable, in its declared lane, via a job card when one exists |
| **Council** | models consulted read-only | second opinions and blind scoring; output enters the repo only through Owner or Maintainer |

**Role ≠ access level.** Several agent brands may hold the same Write
access; the *role* says who integrates. Each repo names **one Maintainer
at a time** in its entry file — two integrators in one repo is how work
gets silently undone. A second frontier agent can be Maintainer of a
*different* repo, or work as a Contributor in its declared lane.

<sub>**Footnotes:** renamed 2026-08-06 — Maintainer was "Architect",
Contributor was "Runner", Council was "Advisor/Council". The vocabulary
originates in the org's most advanced pipeline repo; old names persist
in historical changelog entries.</sub>

## The root-doc set

> **What:** the four files every repo carries, and the bar a fifth must
> clear. **Why:** the Owner's explicit objective (2026-08-07) is to keep
> this set small — each additional root doc is another entry point,
> another file to keep current, and another place content can hide; the
> default answer to *"where does this go?"* is **a section inside one of
> the four**. **Style:** the table states purpose only; the closed-set
> rule below carries a worked example, because the hard part is
> reasoning about a borderline case, not reciting the list.

Standard per repo:

| File | Purpose |
|---|---|
| `README.md` | The **human landing page** GitHub renders: TLDR of what the repo is, the **architecture** of the product/workflow it contains (it is the product's introduction/summary), + a site map. Never the agent entry point, never a rulebook — it signposts. |
| `CLAUDE.md` (and other entry files) | Agent entry/routing — see *Entry files & vendoring*. |
| `CHANGELOG.md` | The **decision log**: dated entries with the *why*, newest first. |
| `HUMAN.md` | The owner's charter — **one per org context repo**; other repos point back to it rather than duplicating context. |
| `STANDARDS_fromADMIN.md` | **Read-only vendored copy of the org standard** (this document), version-stamped and replaced wholesale on each standards release. Admitted past the closed-set threshold via the **ownership exception**: it is admin-owned, and the local Maintainer never edits it — the same logic that admits `replit.md` as Replit-owned. |

Replit-backed repos add `replit.md` (the Contributor's context file) and
`NEXT_FOR_REPLIT.md` (the work-order file) — see *The Replit two-agent
pattern*.

**The set is closed by default.** Any additional root doc faces a
**very high threshold for inclusion**: first find a home for the
content in sections of the standard four. A new file is justified only
by the established exceptions — different **ownership** (the `HUMAN.md`
logic), different **lifecycle** (append-only logs, machine-read data),
or **harness mechanics** (files a tool auto-loads by fixed name).
Worked example — a future per-repo *learning-loop review* (a recurring
cadence of self-improvement questions: architecture, redundancy
removal, hardening, applying the paradigm principles, performance):
the **question set and cadence** are org-standard and belong in this
file; each run's **findings** are a dated `CHANGELOG.md` entry; the
resulting **actions** go to the repo's open-items list. It earns its
own file only if it accumulates machine-read state (scores, metrics
over time) — the lifecycle exception, not a convenience one.

**Why a CHANGELOG when git has history:** (a) decision-level entries
span multi-commit efforts and carry the *why*; (b) it's readable as a
plain file — git history isn't in an agent's context by default, and
shallow clones/squashes lose it; (c) it's cross-harness — some agents
read files, not git archaeology. Rule of thumb: one entry per decision
(not per commit), newest first. Skip changelogs only in throwaway or
single-author-single-agent repos.

<sub>**Footnotes:** planned (Owner, 2026-08-07): elaborate this section
into a per-doc template — the sections and subsections each root doc
MUST include.</sub>

---

# Principles of the agentic paradigm

> **What:** why an agentically-built product beats a traditionally-built
> one — stated from the **end user's** side (what the delivered report,
> dashboard, or workflow can do), never the builder's. **Why:** these
> are the reason for the paradigm shift and for this whole operating
> standard; the Owner explicitly corrected an earlier build-perspective
> draft to this framing (2026-08-07, same day the Cadence and
> Judgment-at-scale points were merged into one principle). **Style:**
> each entry names a *capability the product has*, not a technique the
> team uses; hard-capped at five so they stay memorable — currently
> four, one slot open. Names tightened by the Maintainer. Status:
> **draft**.

Why build with agents at all? Not (mainly) because building is cheaper —
because the **end product** (the report, dashboard, workflow) can do
things a traditionally-built, traditionally-staffed product cannot.
These advantages are the key reason for this paradigm shift, worth
leveraging now even though agent intelligence is still maturing: the
structure is designed so each upgraded agent — especially the
Maintainer — immediately lifts the whole system's performance.

1. **Learning loop** — the product records not only its output but the
   *why* and the *style* behind it (charters, method files, decision
   logs), so it can be analyzed and improved cycle over cycle — by
   agents as well as the Owner. The product gets better with use, not
   just with rebuilds.
2. **Customization** — interfaces and pipelines built to the exact
   need, not off-the-shelf compromises: a markets dashboard showing
   precisely the assets, comparables, and data its owner selected; a
   training site shaped around the athlete's specific current goal and
   injury-rehab cycle. Bespoke used to be enterprise-priced; agentically
   it is the default.
3. **Elastic capacity** — the product is no longer bounded by staff
   overhead: parallel agents scale analytical work up and down on
   demand. Two expressions of the same freedom:
   - **Cadence** — what was a monthly report becomes daily or
     on-demand, refreshed whenever the underlying data moves.
   - **Judgment at scale** — subjective analyst work as a standing
     capability: e.g. read the latest earnings reports, footnotes, and
     interviews; select the top 20 points; score each +5/−5 on
     criticality or a multifactor impact map. Mechanical-Turk-class
     *judgment* jobs become repeatable product features rather than
     special projects.
4. **Council** — the product carries independent multi-model
   recommendations and scoring as a built-in feature (proven in the
   reports pipeline): committee-grade second opinions per decision,
   without convening a committee.

<sub>**Footnotes:** working labels → adopted names: "Self improvement" →
Learning loop · "Curated" → Customization · "Recenty/Recency" +
"Subjective turk jobs" → merged into Elastic capacity (2026-08-07,
Owner + Maintainer; the shared root is freedom from staff overhead) ·
"Agent recommendations, Council" → Council. The first draft read the
principles from the build perspective; the Owner corrected to the
end-product function/advantage perspective the same day.</sub>

---

# Working protocols

## Handoff protocol

1. Every repo declares its **actors and lanes** in its entry file (who
   works there, writing where).
2. Work passes by **explicit written handoff** (chat note, PR
   description, or committed handover doc: what was done, current state,
   what the next actor should and shouldn't touch) — never by inference.
3. **The repo is the source of truth** — anything a future session needs
   must be committed; chat memory doesn't transfer between tools or
   sessions.
4. **CHANGELOG discipline** — non-trivial changes get a dated entry with
   the why; it's how one agent learns what another did.
5. **Repo-specific protocols override** this framework where needed.
6. Every AI commit carries provenance trailers:

   ```
   Generated-by: <Harness> (<model that actually ran>)
   Co-Authored-By: <the harness's standard co-author line>
   ```

   Name the model that **actually ran** (never a configured or
   menu-label name; for a mixed run, the predominant model). *Why:* the
   commit author line shows the pushing identity, not the agent — with
   several brands committing to the same repos, trailers make `git log`
   the cross-agent audit trail. *Known gap:* some harnesses restrict
   stamping exact model IDs; those commits carry the harness name only —
   acceptable, harness granularity still identifies the actor.
7. **Cost gates:** anything token/time/money expensive — live research
   runs, paid API sweeps — is **opt-in per run**, never triggered
   automatically. Staleness *flags* an expensive refresh; it never
   *runs* one. High-trust mode drops *process* gates, never *cost*
   gates.

## Entry files & vendoring

> **What:** the per-repo files agent harnesses auto-load, plus the two
> one-way channels that keep org standards flowing between repos.
> **Why:** a topical session is scoped to its own repo and **cannot read
> the admin doc** — so the rules binding it must be *copied to where it
> is* (downstream), and its org-level ideas must travel back by a
> declared route rather than by editing upward (upstream). Every rule
> below follows from that one constraint. **Style:** written to be
> obeyed by an agent that can see only its own repo — no rule here may
> depend on reading the canonical source.

Entry files exist only because agent harnesses auto-load them by fixed
name; they are **thin routing stubs, not rulebooks**:

| Harness | Auto-loads |
|---|---|
| Claude Code | `CLAUDE.md` |
| OpenAI-family tools (Codex, etc.) | `AGENTS.md` (de-facto standard for most other tools too) |
| Replit Agent | `replit.md` |

- An entry file states: what the repo is, who is Maintainer, the reading
  order, repo-specific lanes — plus a **condensed vendored copy of the
  org rules that bind in that repo**.
- When a non-Claude harness joins a repo, its `AGENTS.md` opens with
  "Read `CLAUDE.md` — it routes *all* agents", so the two never drift.
- **Each harness owns its entry file** — never rewrite another agent's
  (`replit.md` is the Replit Agent's; `CLAUDE.md` is Claude's). To make
  a convention stick on the other side, put it in the work-order file
  with an instruction that the other agent record it in *its own*
  context file.
- **Reading order for any agent entering a repo:** (1) entry file →
  (2) `README.md` → (3) context docs (`HUMAN.md` if present) →
  (4) recent `CHANGELOG.md` entries → (5) the org's admin doc if
  connected.
- **Vendored summaries:** each entry file's org-rules block is marked
  *maintained from the admin repo — propose changes there, don't edit
  here*. The **admin session is the only writer** of these blocks and
  proposes the cross-repo pass when the source changes. For a topical
  session the vendored copy **is binding** even though it can't read
  the canonical source.
- **Full-standard vendoring (standards releases):** beyond the
  condensed block, every repo carries a complete read-only copy of the
  org standard as `STANDARDS_fromADMIN.md` — safe to copy anywhere
  because the standard is sanitized by construction. The admin session
  is its **only writer**: on a periodic, owner-approved **standards
  release** it replaces every copy **wholesale** with the current
  version (date-stamped, e.g. 2026.08.08). Local edits are forbidden
  and will be lost at the next release; the copy is **binding as-is**
  in its repo even if a newer canonical version exists. Upward
  proposals go through the entry file's Upstream section, **never into
  the copy** — the copy must stay safely overwritable. Entry files
  point to the copy for the full standard and keep only the
  org-specific binding facts themselves.
- **Upstream sections:** each topical repo's entry file ends with an
  `## Upstream (for admin)` section where topical sessions park
  org-level ideas as dated bullets instead of acting on them. The admin
  session sweeps these when convened, decides with the Owner,
  integrates, and clears. Nothing org-level is ever *implemented* from
  a topical session.
- **Onboarding a new agent brand:** (a) Owner grants access (registry
  updated first); (b) the incumbent Maintainer prepares a handover
  package — condensed context, the new agent's lane and deliverables,
  commit conventions; (c) the new agent's first task is to read in
  order and **summarise its own lane back** before its first write —
  cheap proof the routing worked.

---

# Repo & governance recipes

## Repo recipe (defaults)

Every new repo, unless a decision says otherwise:

- **Private** · "Add a README" ticked (born with a working `main`).
  *Exception:* Replit-synced repos are **not** pre-created — see *The
  Replit two-agent pattern*.
- **Wikis OFF · Projects OFF** — docs live in the repo where agents
  read and version them. **Issues** are a per-mode decision: OFF in
  high-trust single-owner repos (in-repo TODO lists and Upstream
  sections are what agents actually read); ON where a repo's workflow
  genuinely tracks defects there.
- **Forking OFF** — no stray copies under other accounts.
- **PR creation: collaborators only** — no effect while private,
  safe-by-default at a public flip.
- **Merge commits ON, squash/rebase OFF** — one merge method, history
  stays truthful, provenance trailers survive. **Auto-delete merged
  branches ON. Auto-merge OFF** (a merge is a decision, not a trigger).
- **Agents get Write; Admin stays human-only.** Write covers everything
  an agent does day to day; Admin only widens what a stolen credential
  could do. Settings changes stay a human click-path task.
- **No LICENSE file until a public flip** — while private a license
  only grants others rights; at flip time it becomes a deliberate
  choice (docs may suit CC-BY over MIT; personal-data repos never flip
  as-is).
- Root docs per *The root-doc set*.

## Governance profiles

> **What:** named branch-rule stances, exactly one per repo. **Why:**
> naming them turns *"what gate does this repo have?"* into a lookup
> instead of a re-derivation, and — the point most easily missed —
> makes **high-trust a deliberate choice rather than an oversight**: a
> repo with no ruleset is that way on purpose, with a named substitute
> for the gate it omits. Do not assume a repo lacking a profile needs
> one; check the org's registry. **Style:** each profile states its
> mechanism *and* the risk control that stands in for what it doesn't
> enforce.

Branch rules live in one ruleset per repo on the default branch
(standard name: `main-pr-required`). Three profiles:

- **Profile A — baseline only.** Restrict deletions + block force
  pushes (both ruleset defaults), nothing else. For repos where an
  agent's designed lane is direct pushes to `main` (e.g. Replit-synced
  repos — the syncing agent typically can't sit on a bypass list, so
  it's Profile A or nothing there). The harness and the two-agent
  protocol are the risk control; the ruleset only guards against
  history rewrites and deletion.
- **Profile B — PRs required, one approval.** Baseline + require PR
  with **1 required approval**, merge-only, bypass for repo admins
  only (the Owner is never locked out). *Why 1 and not 0:* with 0 the
  author can merge their own PR — a *record* of change, not a *gate*.
  Either a repo needs no gate (A) or a real one (B).
- **Profile C — PRs required, Maintainer bypass.** Profile B + the
  Maintainer's team on the bypass list. For repos with one Maintainer
  but several other AI actors: Contributors can push branches and open
  PRs but physically cannot merge; the Maintainer merges reviewed PRs
  and pushes pipeline outputs directly. "The Contributor never merges"
  stops being a promise and becomes something GitHub enforces.

**High-trust mode** (a legitimate fourth stance, for single-owner orgs
with few agent identities): agents hold direct Write, **no rulesets**
(or agents on the bypass list), self-merge allowed, the Owner reviews
*after the fact* via `CHANGELOG.md` and git history. What keeps it
coherent is not branch protection but **docs as the contract**. Baseline
rules (Profile A) remain worth adding even here — they gate nothing
agents normally do.

Other ruleset toggles (status checks, signed commits, linear history,
deployments) are stricter policies adopted only where a repo has the
machinery to need them (e.g. required status checks on a repo with CI).

**Org settings that make this work** (once per org): 2FA required (the
human account must be the hard thing to steal); base member permission
**"No permission"** (every visible repo is an explicit grant — and the
first thing to check when an account "can't find" a repo); agent access
via either an **agents team** (one switch to pause/replace the
Maintainer everywhere) or direct per-repo grants (simpler at small
scale) — pick one mechanism and stay consistent.

---

# Proven patterns

## The Replit two-agent pattern

> **What:** the working agreement for a repo synced 1:1 to a Replit app,
> where a second agent builds in a hosted workspace. **Why:** every rule
> here was bought with a real failure — unrelated-history rebase weaves,
> both sides holding unpushed work, fixes patched in the workspace and
> lost at the next pull. Treat a deviation as expensive, not stylistic.
> **Style:** deliberately specific — exact cues, exact click-paths,
> exact file names — because ambiguity is precisely what breaks
> two-agent sync.

For a repo synced 1:1 to a Replit app (proven twice in this org's
history):

- **Repo birth:** the repo must be *born from the Replit workspace*
  (Replit authors the first history; owner sets private + app grant at
  creation). Pre-creating on GitHub gives two unrelated histories and
  rebase pain forever after. The Maintainer layers org docs on top via
  PR afterwards.
- **Lanes:** Replit Agent = **Contributor** (app/display code, direct
  to `main` from the workspace — its only direct-to-main lane; plus all
  environment work: secrets panes, restarts, publishing). The
  Maintainer handles features, logic, data plumbing, schema, anything
  with edge cases — via `claude/*` branches and PRs. Display formatting
  is the Contributor's; anything touching data files, schema, or metric
  semantics is the Maintainer's.
- **Sync ritual:** after every Maintainer merge the Owner clicks
  **Pull** (not Sync) in Replit's Git pane *before* new Replit work;
  Replit commits+pushes at the end of every Replit session; nobody
  force-pushes. The Maintainer ends every merge with the fixed cue
  **"✅ Merged — OK to Pull"** so the Owner always knows when Pull is
  due. (Replit Agent holds no GitHub credentials — the Pull click is
  always the Owner's.)
- **Handover file, not paste blocks:** the Maintainer overwrites
  `NEXT_FOR_REPLIT.md` at the repo root on every merge with the
  *current* work order (standing rules + tasks + verification values);
  the Owner's paste to Replit Agent is one fixed line: *"Read
  NEXT_FOR_REPLIT.md and execute it."* History stays in CHANGELOG/PRs,
  not in the file. End work orders with *"no code fixes — route
  failures back to the Maintainer"* so failures aren't patched in the
  workspace.
- **One-way data contract:** a display repo consumes only a curated
  dataset committed from its data/context repo (schema documented in
  the display repo's README, including UI-binding display rules). If
  the app needs richer data, the *exporter* changes — never the display
  side. One `HUMAN.md`, in the data/context repo; the display repo
  points back. App runtime secrets live in the platform's secrets pane,
  never in the repo; data-source keys never enter the platform at all.
- **Ops pitfalls worth codifying:** always `git fetch` before
  `checkout -B <branch> origin/<default>` (a stale remote-tracking ref
  silently bases work on old `main`); through a git proxy,
  `--force-with-lease` can fail with "stale info" even when safe —
  verify remote state, then use an explicit lease or `--force` on your
  own working branch only.
- **Owner exceptions to binding rules** (e.g. auth-gating waived for a
  dev URL): record as a dated interim exception in the binding doc
  *plus* a TODO in `HUMAN.md` — never silently violate, never silently
  obey.

## HUMAN.md authoring pattern

> **What:** how the Owner's charter is written, and by whom. **Why:**
> this is the boundary that makes every other freedom safe — agents move
> across the repo with little process precisely because intent is fenced
> into one file they may not rewrite. A single unasked edit here costs
> more trust than any code defect. **Style:** when in doubt, propose in
> chat or file it marked *unconfirmed* — never edit in place, never
> silently regenerate. Owner-reviewed v2 (2026-08-05), extended
> 2026-08-07 to admit a segmented Maintainer-suggestions component.

The load-bearing pattern of high agent autonomy: agents own everything
else freely precisely because the owner's intent is fenced off in one
human-owned file (thesis/goals, philosophy, binding constraints, style).
Authoring conventions (owner-reviewed, v2):

- Sticky headings; provenance and dates go in meta blockquotes *under*
  headings, not in the headings.
- The Maintainer acts as **copywriter only** on the Owner's content:
  edits on request, with grammar-level freedom but never new meaning;
  never edits unasked.
- *Section anatomy* applies here too: a clearly marked **Maintainer
  suggestions** component is welcome — it is sufficiently segmented
  from the Owner's points to preserve the ownership boundary.
- Implicit content an agent infers may be filed, but marked
  **unconfirmed-by-owner** until ratified.
- Per-section meta notes carry the owner's authoring preferences.
- Never implement from a `HUMAN.md` todo/ideas section unless asked in
  conversation — it's a parking lot, not a queue.

---

# Security & operations

## Environments & sessions

An *environment* is a saved cloud-workspace configuration (repos, network
allowlist, env vars); a *session* is one conversation in a fresh
temporary computer built from it — only what's pushed to a repo
survives. Standing pattern:

- **One admin hub** (the admin repo + others when cross-repo work needs
  them; **no keys**) — the all-seeing session for setup, policy, and
  vendored-summary sync.
- **One environment per topic** — only that topic's repo, only its
  keys, **Custom network access** limited to that topic's services.
  *Why:* if a key-holding environment can only reach the one service
  the key is for, a leak has almost nowhere to go — the cheapest real
  security available.
- Sessions coordinate through committed docs (*Handoff protocol* rule
  3), not shared chat memory.

## Secrets

1. **Never commit secrets to git** — no tokens, keys, or connection
   strings in any repo, private or not. Git never forgets, and any repo
   may one day go public as a demonstrator.
2. Keys live in the env vars of the one environment that needs them
   (accepted as visible-not-secret) or the hosting platform's secrets
   pane — never in a repo.
3. **Match the key to the stakes.** Low-stakes data key: env var is
   fine. Financial credentials: never in env vars — read-only exports,
   aggregator services, or manual uploads until a proper secrets answer
   exists.
4. **Rotate on suspicion** — prefer services with self-serve key
   regeneration.
