# HUMAN.md — the author's charter

> **Human-owned — the single file containing everything the human wrote, for every report in this repo.** One section pair per report (`<slug> · Frame` + `<slug> · Style`). The author writes and approves this file; AI may *propose* wording on request but must never edit it without the author's explicit approval, and never silently regenerate it. Everything under `pipeline/` and `reports/` is agent-made. Scripts and council packets extract a report's Frame via its slug-scoped markers (`frame:<slug>:start` / `frame:<slug>:end`) — council members see the Frame only, never the Style section.

<!-- frame:sg-banks:start -->
## sg-banks · Frame

> This document contains the thesis and the key factors the report analyzes. The HUMAN authors and approves the file; the AGENT proposes wording. Each key factor is **scored in the report's Conclusions by a blind multi-model council** (per factor: performance −5…+5 vs the thesis · criticality `critical/high/medium/low` · a one-sentence comment per member; members may also **suggest missing factors**; protocol in `method/7-ai-write-scores.md`) — the reader draws their own conclusions from the members' answers. Each factor is **analyzed in full in the report's Supporting Data section** in the format specified below — the formats are MUST-includes; the Scope stage may propose and append *additional* analysis per factor, never replace these.

### Thesis
The Singapore banks — DBS, OCBC and UOB, as a group or individually — are a value buy-and-hold for the next 10–15 years.

### Key Factors

**A. Capital attraction — the primary factor**

1. **Client-asset growth** — CA = customer deposits + wealth AUM
   *(Format: `Bank_Metric: S$bn, CASA %, 5y-CAGR %, FY25 %, FY24 %, FY23 %, FY22 %` — metrics per bank: **Deposits**, **Wealth AUM**, and **Client Assets** = customer deposits + wealth AUM (internal note: included to see how consistent the various AUM/deposit/client-asset definitions are; "client assets" here is broader than the wealth-industry usage, which can exclude ordinary deposits — renamed from "Capital Base" 2026-07-25 to avoid collision with regulatory total capital). Each `FYxx %` = that FY's YoY growth; CASA % applies to the Deposits rows as the deposit-quality marker; "5y" = latest FY vs FY five years prior; latest-quarter YoY as a dated secondary where available.)*

2. **Wealth-hub capital flows** — Singapore vs the global cross-border pool
   *(Format: **one table** — `WealthHub | Non-res US$tn | 5y-CAGR % | FY25 % | FY24 % | FY23 % | FY22 %` — Singapore versus Hong Kong, Switzerland, and other relevant hubs, plus a **Global — all centres** row as the share denominator, so Singapore's share of the pool is readable from the table. Measure: **cross-border ("offshore") wealth** = financial wealth booked in a centre by **non-residents only** — each hub's own residents' onshore wealth and real assets (incl. directly held real estate) are excluded; state this definition wherever the table is published. Share comparisons come from a **single source family** (currently the BCG booking-centre series; never mix families in one comparison). Open the answer with a **Key stats** line sizing the market: global net wealth incl. real assets (US$tn) · global financial wealth (US$tn) · the offshore pool as a % of each — the mobile slice the hubs compete for, with a note that the share moves slowly and policy/convenience shifts show up first as reallocation between hubs (context measures `GlobalFinancialWealth` / `GlobalNetWealth` live in `data/flows.csv`, same source family). Cross-hub macro is reported in USD as sourced — per the currency principle: every series in its reporting currency, never FX-converted; the SG-bank series are SGD.)*

**B. Monetization — secondary (expected to follow attraction)**

3. **Income engines: NII & Other Revenue**
   *(Format: `Bank_Metric: S$bn, 5y-CAGR %, FY25 %, FY24 %, FY23 %, FY22 %` — metrics per bank: NII and OR. Each `FYxx %` = that FY's YoY growth. OR = total income − NII.)*

4. **NIM cyclicality & rate sensitivity**
   *(Format: **line chart** — group NIM per bank vs **3M SORA (FY avg)** and **effective Fed funds (FY avg)** (theoretical Fed → SORA → NIM transmission), FY2016–25 + latest, generated deterministically from the ledger (`method/5-script-build-charts.py` → `reports/assets/sg-banks-nim-vs-sora.svg`); plus one or two sentences on the swing — trough → peak → latest — and the group pattern.)*

5. **Client-asset monetization vs peers** — headroom vs mean-reversion
   *(Format: **one table**, SG banks + all peers, latest available FY:
   `Bank | NII (lc bn) | OR (lc bn) | NII_vDep | OR_vDep | OR_vCA | total_vCA | Top Other-Revenue categories (% of total revenue)`
   Levels first, in each bank's **local reporting currency** (`lc`; the SG rows are S$bn — never FX-converted, per the currency rule): NII = net interest income; OR = Other Revenue = total revenue − NII. Then four within-bank ratios, each **indexed to the index bank = 100** so currencies cancel:
   **`NII_vDep`** = NII ÷ customer deposits — rate-driven monetization of the sticky on-balance-sheet base.
   **`OR_vDep`** = OR ÷ customer deposits — non-NII monetization of the deposit base.
   **`OR_vCA`** = OR ÷ client assets — non-NII monetization of the full attracted base (client assets = customer deposits + wealth AUM).
   **`total_vCA`** = total revenue ÷ client assets — total monetization of the full base (formerly `Monetization_vCapitalBase`).
   The client-assets denominator deliberately sums deposits + AUM as a service base — a noted exception to the never-sum-for-attraction rule — and AUM definitions differ across banks and overlap deposits, so the vDep and vCA lenses are always read together. **State the implied SG Other-Revenue uplift at index-bank parity** (OR_vDep gap × deposits, and as % of revenue) — under the thesis, under-monetization of an already-attracted base is optionality, not only a deficiency. As-stated NIM per bank is footnote context only, not an index (denominator conventions differ; `n/d` where not disclosed, e.g. UBS). The last column is compact per bank — the top-3 non-NII categories of any significance, e.g. "insurance 23% · fees 19%"; `n/d` where a bank does not disclose the split. Benchmarks: the peer set below.)*

**C. Valuation**

6. **Valuation premium vs peers & required outperformance**
   *(Format: same peers and index bank as Q5; **four valuation indexes**, each indexed to the index bank = 100, using market cap and latest-FY denominators:
   **`P/CA`** = market cap ÷ client assets (customer deposits + wealth AUM) — valuation per unit of attracted capital, the primary-driver lens.
   **`P/Rev`** = market cap ÷ total revenue — valuation of monetization ability.
   **`P/E`** = market cap ÷ net profit — the standard earnings lens.
   **`P/B`** = market cap ÷ book equity — included as the banking convention, relevance viewed with skepticism.
   Required outperformance per index = (premium ratio)^(1/5) − 1 per year — the extra annual growth in that index's denominator (client assets / revenue / earnings / book) needed for multiples to converge to the index bank's within 5 years. Present as **one table**, SG banks + all peers:
   `Bank | Price (local ccy/share, as-of date) | P/CA | req %/yr | P/Rev | req %/yr | P/E | req %/yr | P/B | req %/yr`
   The Price column is the staleness/relevance marker: each bank's local per-share price with the date it was taken (the same dated market data behind its market cap). Comment on whether the spread between DBS, OCBC and UOB is justified by fundamentals.)*

### Benchmark peer set (used by factors 5 & 6)

**Selection criteria:** universal/commercial banks in the same category as the SG banks — large retail deposit bases **and** substantive wealth-management arms (wealth AUM ≳ US$500bn where disclosed) — drawn from distinct wealth-hub or major-banking jurisdictions. Pure investment banks and pure asset/wealth managers are excluded.

| Peer | Jurisdiction | Note |
|---|---|---|
| **HSBC** | Hong Kong / UK | **index bank = 100** — closest business model, competing wealth hub |
| UBS | Switzerland | Swiss-hub wealth giant |
| JPMorgan Chase | US | universal; caveat: large investment-banking share |
| Bank of America | US | commercial + Merrill wealth |
| Standard Chartered | UK / Asia hubs | Asia-footprint universal bank |
| China Merchants Bank | China | China's retail/wealth leader |
| RBC (Royal Bank of Canada) | Canada | Toronto-hub universal bank + top-tier global wealth arm; FY ends 31 Oct |

*Australia excluded (decided 2026-07-24, replacing Commonwealth Bank with RBC): all four Australian majors divested their wealth arms (CBA → Colonial First State, NAB → MLC, ANZ → IOOF/Zurich, Westpac → BT exit), so no Australian bank discloses a comparable wealth AUM — itself a finding: Australia's banks exited the wealth flywheel the SG banks are building.*

<!-- frame:sg-banks:end -->

---

## sg-banks · Style

> Formatting & marking rules the build must follow. **I own these rules; AI applies them.** Seeded from the report's existing conventions — refine as you like.

- **Currency:** every series in its reporting currency, never FX-converted. SG-bank series are SGD (no conversion, no ADRs); cross-hub macro in USD as sourced; peer financials in each bank's local reporting currency.
- **Number formats:** deposits & assets in billions (no decimals); revenue & profit in billions (1 decimal); margins and ratios as percentages.
- **Marking:** table cells carry a number, `n/r` (not retrieved), or `n/d` (not disclosed) only. Derived cells (ratios, CAGRs, valuations) are unmarked; each table gets a formula footnote.
- **Citations:** bracketed `[n]` markers (superscript substitute), keyed to a per-table or per-section source list. **No raw HTML** (`<sub>`, `<sup>`, …) in published files — the site renders pure markdown only; notes/footnotes are italic paragraphs under their table or answer.
- **Restatements / adjustments:** flagged in a footnote, never silently baked into a figure.
- **Tone:** neutral and descriptive — report the finding, don't sell it. Every report ends with "Not investment advice."
