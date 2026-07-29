# IDEAS.md — improvement brainstorm (author ↔ Claude)

> **Ground rules:** this file is a shared scratchpad for improvement ideas — the author and Claude brainstorm here, refine wording, and park thoughts. **Nothing in this file is authorized for implementation.** An idea only becomes work when the author explicitly approves it, at which point it graduates into the proper channel (a frame amendment, an `UPDATE.md`-routed change, or a `PERPLEXITY.md` job) and its entry here is marked *graduated*. Agents other than Claude: read-only.
>
> Standing, already-agreed roadmap items are **not** duplicated here — they live in the registry (`pipeline/sg-banks/index.md` § Open questions): peers-history delta (required-vs-delivered outperformance), council scoring architecture + frame question refactor, 2Q26 refresh bundle, `meta/history.csv` version time series.

---

## Idea 1 — NII quality & expandability: loan book, capital headroom, and "toxicity" (status: brainstorm)

**Author's seed (2026-07-26):** the quality and expandability of NII / the loan book — touching the CET1 metric (or other capital ratios) and some metric for how reliable or toxic the lending book is, e.g. mortgage vs SME vs corporate bond vs interest-rate-exposed.

**Why it matters to the thesis:** Q5 established that SG banks already out-earn HSBC on NII per deposit (NII_vDep 110–122) while lagging on OR. That makes the *durability* of the NII engine a first-order question: an NII stream built on well-collateralized mortgages at a bank with CET1 headroom is worth more — and can *grow* more — than the same NII built on concentrated SME or rate-exposed exposure at a capital-constrained bank. Today the report treats NII as one number (split only by cyclicality, Q4); this idea decomposes its **quality** (how safe) and **expandability** (how much more the balance sheet could produce).

**Candidate metric set (three layers, per bank + peers where disclosed):**

1. **Expandability — capital headroom.** CET1 ratio (plus total capital ratio as secondary); distance to each bank's regulatory minimum + management target; implied additional lending capacity at current risk weights (headroom × RWA density → potential loan-book growth without new equity). Fully disclosed quarterly by all peers — cheap to fetch.
2. **Quality/"toxicity" — book composition.** Loan mix by segment: residential mortgage · SME/commercial · large corporate · consumer unsecured · CRE — each with a rough risk character (LTV-collateralized vs cyclical vs concentration-prone). Disclosure caveat: segmentation taxonomies differ per bank (same lesson as WealthAUM definitions — capture each bank's own labels verbatim, flag non-comparability).
3. **Realized quality — credit outcomes.** NPL ratio, credit cost (provisions ÷ avg loans, through-cycle avg + latest), coverage ratio; plus stated NII sensitivity to a ±100bp rate move (the "interest-rate-exposed" dimension — most banks disclose this in their Pillar 3/annual reports, which also ties back to Q4's cyclicality finding).

**Possible composite:** a per-bank "NII quality score" is tempting but risks false precision — better fit for the future council to opine on than for a formula. A more honest deterministic output: a compact table (CET1 + headroom · top-2 loan segments % · NPL · credit cost · NII ±100bp sensitivity) with the toxicity judgement left to the reader/council.

**Where it would live if approved:** most naturally a new frame question in group B (Monetization) — e.g. *"How durable and expandable is the NII engine?"* — or an internal-note extension of Q3. Data via a fetch-ledger delta (SG banks, ~5 metrics × 3 banks × recent FYs) + a fetch-peers delta (same metrics for the 7 peers); build_benchmarks gains the table. Worth deciding **after** the council/frame-refactor session, so the question count and criticality ratings settle together.

**Open questions to brainstorm:** period depth (latest FY only, or 5y history to see credit-cost cycles?) · include RWA density as its own column? · does the SME/CRE mix deserve a concentration flag (top-sector % of book)? · peer comparability of NII-sensitivity disclosures (assumptions differ by bank).

---

## Idea 2 — Council seat packets: author-run lab-native scoring sessions (status: brainstorm)

**Author's seed (2026-07-27):** run each council model independently in its own lab's app — Perplexity's Model Council proved not useful, or worse, deceptive for this (every requested seat self-reported Claude Opus 5 at run time; see `PERPLEXITY.md` Completed Job #4).

**The idea:** Claude prepares one self-contained **seat packet** per open seat (GPT · Grok · Gemini) — a single paste-able block containing the blind protocol, the rubric verbatim, `frame.md`, and the report body with the Conclusions region stripped, ending with the exact JSON schema to fill in and an instruction to print the model's runtime self-identification. The author pastes a packet into the lab's own app (ChatGPT / Grok / Gemini), pastes the JSON reply back to Claude, and Claude validates it against the SOP self-checks, stamps it, and commits it as `data/scores/<member>.json`.

**Why lab-native:** satisfies `write-scores.md` § Member identity & admissibility (verifiable identity, no routers, one seat per lab) with the author as the isolation guarantee — each app session sees only its packet, never another member's output.

**Open questions to brainstorm:** packet size vs app context/paste limits (report body is long — may need the packet as an attached file where apps allow it) · how the author confirms "latest knowledge-work model" in each app's model picker at run time · timing — seats should score **after** the pending frame v3 rewording lands, so every member scores the final wording once · whether a packet generator belongs in `method/` as a script module (deterministic: strip markers, concatenate, emit) or stays a manual Claude step for now.

---

## Idea 3 — Growth story: expansion by jurisdiction and product (status: brainstorm)

**Author's seed (2026-07-27):** as the whole concept of this valuation — and equities in general — is the growth story, gauge each SG bank by growth in jurisdiction and/or product: regional or global expansion plans and results, plus indications they are moving into large revenue areas such as x, y, z (placeholders to fill in).

**Why it matters to the thesis:** the thesis is a 10–15-year buy-and-hold, but the report currently measures *delivered* growth (deposits, AUM, income CAGRs) with Singapore as the geography. Q6 showed the price already demands +9–12%/yr outperformance — that gap can only be closed by growth vectors not yet in the run-rate: new jurisdictions and new products. Today the report is silent on *where incremental growth comes from*.

**Two axes, kept separately:**
1. **Jurisdiction.** Revenue/PBT and loan/AUM split by geography per bank (all three disclose segment geography: DBS's Greater China/South+Southeast Asia, OCBC's Greater China/Malaysia/Indonesia, UOB's ASEAN-4), growth per region, plus stated expansion moves and their delivered results (e.g. DBS India/Taiwan (Citi), OCBC Indonesia, UOB's Citi ASEAN consumer acquisition — buy-vs-build track record).
2. **Product.** Entry into large adjacent revenue pools — candidate x/y/z list to refine: bancassurance/insurance (OCBC-GE already), asset management, transaction banking / cash management, private credit, digital assets / tokenization (DBS Digital Exchange), regional consumer platforms. Each with disclosed revenue where available, else a stated-ambition flag.

**Discipline caveat (why this needs care):** "plans" are narrative, not data — the pipeline's edge is deterministic, source-graded numbers. The honest shape is a *delivered-growth-by-segment* table (hard numbers from segment disclosures) plus a short, dated "stated strategy" appendix clearly marked as management claims, never mixed into benchmark math. The council can then judge credibility; the tables never assert it.

**Where it would live if approved:** most naturally a new frame question in group A (the attraction/growth engine) — e.g. *"Where does the next decade of growth come from — which jurisdictions and products, and is delivery visible yet?"* Data via fetch-ledger delta (segment splits, 3 banks × ~5y) — segment taxonomies differ per bank (same verbatim-labels lesson as WealthAUM).

**Open questions to brainstorm:** finalize the x/y/z product list · geography granularity (bank-reported segments only, or normalize to a common region set?) · how to score "results" of an expansion (segment CAGR vs group CAGR? ROE of acquired units?) · does this fold into Idea 1's balance-sheet headroom (capacity to fund expansion) or stay separate?

---

## Idea 4 — Other-Revenue benchmark contamination: investment-banking mix (status: brainstorm)

**Author's seed (2026-07-27):** some of the OtherRevenue of the benchmark banks is investment banking (e.g. UBS, JPM) — so either pick better benchmarks or normalize somehow.

**Why it matters to the thesis:** this attacks the validity of Q5's headline finding. The SG banks' OR_vDep of 56–73 vs US peers at 140–181 is currently read as monetization headroom — but if a large slice of JPM/GS-class OR is investment-banking and markets revenue the SG banks structurally don't (and won't) pursue, then part of that gap is **not addressable headroom**, and the +13–26% revenue upside case in the current Q5 answer is overstated. Conversely, stripping IB would make the *wealth-fee* comparison (the pool the thesis actually cares about) sharper and possibly more favorable.

**Three candidate fixes (not mutually exclusive):**
1. **Decompose OR** into fee families from segment/fee-income disclosures — wealth/asset-management fees · cards/payments · trade/transaction · insurance · IB advisory+underwriting · trading/markets — and rerun the vCA/vDep ratios on the *addressable* subset (ex-IB, ex-markets). Most honest; heaviest fetch (taxonomies differ per bank, the WealthAUM lesson again).
2. **Re-tier the peer set:** flag each peer's OR as wealth-led (UBS — though its IB is still ~a fifth of revenue), universal/IB-heavy (JPM, BofA), or commercial-led (HSBC, RBC, CMB, ICBC), and benchmark SG banks primarily against the non-IB tier, keeping IB-heavy peers as context rows only.
3. **Cheap proxy normalization:** subtract each peer's disclosed IB + markets segment revenue from OR before computing ratios — one number per bank per year, far cheaper than full decomposition, gets ~80% of the correction.
The existing `Top Other-Revenue` column already hints at this (it names each bank's dominant OR source) — this idea turns that hint into arithmetic.

**Where it would live if approved:** an amendment to the Q5 method (frame wording change → author approval required) + a fetch-peers delta for the segment lines; `build_benchmarks.py` gains an ex-IB ratio column. Sequencing: fits naturally with the pending Q5 rewording in frame v3 ("gap headroom to grow into vs level peers mean-revert down to" — the ex-IB view answers exactly that).

**Open questions to brainstorm:** which fix (1/2/3) or combination · does trading/markets revenue count as "structurally unavailable" for SG banks (DBS has a real treasury/markets line)? · do we also need the mirror check on the SG side (how much of *their* OR is one-off/trading vs recurring fees)? · UBS classification (wealth-led but with IB — split it?).

---

*Add new ideas below with a number, a date-stamped author's seed, and status: brainstorm → refined → graduated / dropped.*
