# SG Banks — Benchmarks (generated artifact)

*Artifact: `pipeline/sg-banks/data/benchmarks.md` — sole output of `pipeline/sg-banks/method/code/build_benchmarks.py`. Inputs: reconciled `data/ledger.csv` (SG banks), `data/peers.csv`, `data/flows.csv`. Rerun the script to regenerate; same inputs in, same output out.*

## Monetization (Frame Q5)

Levels in each bank's local reporting currency (bn, never FX-converted); the four ratio columns are within-bank, indexed to HSBC = 100, so currencies cancel. OR = Other Revenue = total revenue − NII.

| Bank | NII (lc bn) | OR (lc bn) | NII_vDep | OR_vDep | OR_vCA | total_vCA | Top Other-Revenue (% of total revenue) |
|---|---:|---:|---:|---:|---:|---:|---|
| DBS | S$14.5 | S$8.4 | 122 | 73 | 75 | 100 | net fee & commission 21.4% · net trading income 14.7% · net income from investment securities 0.4% |
| OCBC | S$9.2 | S$5.5 | 110 | 68 | 70 | 91 | fees & commissions 16.5% · trading income 11.5% · life & general insurance income 7.3% |
| UOB | S$9.4 | S$4.5 | 113 | 56 | 70 | 106 | net fee & commission 18.6% · other non-interest income 13.6% · 3rd n/d |
| HSBC | US$34.8 | US$33.5 | 100 | 100 | 100 | 100 | trading/FV income 28.8% · net fee income 19.5% · insurance service revenue 4.7% |
| UBS | US$7.7 | US$41.8 | 50 | 283 | 74 | 43 | net fee & commission income 56.3% · other net income from FI at FVTPL (trading) 28.3% · 3rd n/d |
| JPMorgan Chase | US$95.4 | US$87.0 | 192 | 181 | 116 | 119 | asset management fees 11.1% · investment banking fees ~5.6% · card income 2.6% |
| Bank of America | US$60.1 | US$53.0 | 153 | 140 | 76 | 80 | asset management fees 13.8% · investment banking fees 5.9% · service charges 5.7% |
| Standard Chartered | US$6.0 | US$15.0 | 58 | 151 | 151 | 103 | net trading & other income 51.3% · net fees & commission 20.3% (reported basis) |
| China Merchants Bank | RMB215.6 | RMB121.9 | 113 | 66 | 44 | 60 | net fee & commission income 22.3% · other net non-interest income ~13.8% |
| RBC | C$33.0 | C$33.6 | 115 | 122 | 108 | 105 | investment management & custodial fees 16.0% · mutual fund revenue 7.6% · trading revenue 4.7% |

*As-stated NIM (context only — denominator conventions differ per bank, not comparable as an index): DBS 2.01 · OCBC 1.91 · UOB 1.89 · HSBC 1.59 · UBS n/d · JPMorgan Chase 2.50 · Bank of America 2.01 · Standard Chartered 2.03 · China Merchants Bank 1.87 · RBC 1.62.*

*Implied SG Other-Revenue uplift at index-bank parity (OR_vDep gap × deposits — under the thesis, under-monetization of an already-attracted base is optionality): DBS +S$3.0bn (+13% of revenue) · OCBC +S$2.6bn (+18% of revenue) · UOB +S$3.5bn (+26% of revenue).*

*NII_vDep = NII ÷ customer deposits · OR_vDep = OR ÷ customer deposits · OR_vCA = OR ÷ client assets · total_vCA = total revenue ÷ client assets (CA = customer deposits + wealth AUM) — AUM definitions differ per bank; read the vDep and vCA lenses together.*

## Relative valuation (Frame Q6)

Four indexes vs HSBC = 100; req %/yr = required outperformance, (premium ratio)^(1/5) − 1 per year (5-yr convergence). Px = local per-share price with its as-of date — the staleness marker. P/CA = price ÷ client assets.

| Bank | Px (as-of) | P/CA | req %/yr | P/Rev | req %/yr | P/E | req %/yr | P/B | req %/yr |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| DBS | S$71.96 (2026-07-20) | 175 | +11.9% | 175 | +11.8% | 112 | +2.3% | 169 | +11.0% |
| OCBC | S$28.60 (2026-07-20) | 157 | +9.4% | 172 | +11.5% | 105 | +0.9% | 122 | +4.0% |
| UOB | S$42.60 (2026-07-20) | 106 | +1.1% | 100 | -0.0% | 91 | -1.9% | 83 | -3.8% |
| HSBC | GBX 1527.00 (2026-07-23) | 100 | +0.0% | 100 | +0.0% | 100 | +0.0% | 100 | +0.0% |
| UBS | CHF 42.89 (2026-07-23) | 27 | -22.9% | 63 | -8.7% | 125 | +4.6% | 101 | +0.2% |
| JPMorgan Chase | US$ 348.21 (2026-07-22) | 119 | +3.5% | 99 | -0.1% | 98 | -0.3% | 145 | +7.8% |
| Bank of America | US$ 60.42 (2026-07-20) | 59 | -10.1% | 73 | -6.0% | 84 | -3.4% | 80 | -4.5% |
| Standard Chartered | GBX 2100.00 (2026-07-03) | 56 | -11.0% | 54 | -11.5% | 69 | -7.1% | 71 | -6.7% |
| China Merchants Bank | RMB 37.73 (2026-07-06) | 33 | -19.7% | 55 | -11.2% | 38 | -17.4% | 43 | -15.7% |
| RBC | C$ 293.67 (2026-07-23) | 126 | +4.8% | 120 | +3.7% | 121 | +4.0% | 167 | +10.8% |

*P/CA = market cap ÷ client assets (customer deposits + wealth AUM) · P/Rev = market cap ÷ total revenue · P/E = market cap ÷ net profit · P/B = market cap ÷ book equity. SG market cap = current dated price × FY25 shares outstanding, from the ledger.*

## Wealth-hub capital flows (Frame Q2)

| WealthHub | Non-res US$tn | 5y-CAGR | FY25 % | FY24 % | FY23 % | FY22 % |
|---|---:|---:|---:|---:|---:|---:|
| Hong Kong | 2.9 | 6.7% | +7.4 | +12.5 | +9.1 | -4.3 |
| Singapore | 2.1 | 11.8% | +10.5 | +11.8 | +13.3 | +0.0 |
| Switzerland | 2.9 | 3.9% | +7.4 | +3.8 | +8.3 | -4.0 |
| UAE | 0.7 | n/r | +3.0 | +16.7 | +20.0 | n/r |
| United Kingdom | 1.0 | n/r | +0.0 | +11.1 | +0.0 | n/r |
| United States | 1.6 | 12.2% | +6.7 | +15.4 | +18.2 | +0.0 |
| *Global — all centres* | 15.7 | n/r | +9.0 | +9.1 | n/r | n/r |

**Key stats (2025):** global net wealth incl. real assets **US$550tn** · global financial wealth **US$333tn** · cross-border ("offshore") pool **US$15.7tn = 4.7% of financial wealth** (2.9% of net wealth) — the mobile slice the hubs compete for. The share moves slowly; policy and convenience shifts show up first as reallocation between hubs (the columns above), not expansion of the pool.

*Definition — cross-border (non-resident) wealth: **financial** wealth booked in a centre by clients who are not residents of that country. Each hub's own residents' onshore wealth is excluded — which is why the United States shows only US$1.6tn here: that is foreign clients' money booked in the US (top source region: Central & South America), not Americans' wealth. Real assets, including directly held real estate, are outside the measure — BCG's 2026 report puts global financial wealth at ~US$333tn and total net wealth incl. real assets at ~US$550tn, so the US$15.7tn cross-border pool is ≈5% of world financial wealth. Single source family: BCG Global Wealth Report booking-centre series (US$tn as printed; levels rounded to 0.1tn, so derived YoY cells can differ from BCG's stated growth rates — read the 5y trend, not single-year cells). UK basis is UK-mainland from 2022 (earlier vintages not comparable → `n/r`); UAE included as a flow competitor only (outside the bank peer set). The Global row is BCG's printed world total — the share denominator: Singapore = 12.9% of global cross-border wealth in 2023 (1.7/13.2) rising to 13.4% in 2025 (2.1/15.7). Regulator series (MAS/SFC/SBA), in their own currencies, live in `data/flows.csv` as separate measures and are never mixed into this comparison.*
