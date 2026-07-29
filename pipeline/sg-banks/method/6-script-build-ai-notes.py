#!/usr/bin/env python3
"""Build-AI-Notes — machine-oriented evidence appendix for the report.

Injects "Appendix E — AI reference data" between the <!-- ai-notes:start -->
/ <!-- ai-notes:end --> markers in reports/sg-banks.md: flat, unstyled dumps
of the evidence base so machine readers (council members scoring the report,
other AI analysts) work from the full data, not just the narrated subset.
Human readers are told they can stop before it.

Contents, all derived from the pipeline data files (no AI, no clocks):
  E.1  reconciled ledger — a compact projection (id, period, unit,
       reconciled value, reconciliation status) of data/ledger.csv
  E.2  data/peers.csv verbatim
  E.3  data/flows.csv verbatim
  E.4  open data gaps — counts + row ids from meta/gaps.json

Usage:  python3 pipeline/sg-banks/method/6-script-build-ai-notes.py [--check]
Spec:   pipeline/sg-banks/method/6-script-build-ai-notes.md
"""
import csv, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
GAPS = ROOT / "meta" / "gaps.json"
REPORT = ROOT.parents[1] / "reports" / "sg-banks.md"
START, END = "<!-- ai-notes:start -->", "<!-- ai-notes:end -->"

LEDGER_COLS = ["data_point_id", "period", "unit", "reconciled_value", "reconciliation_status"]


def ledger_projection() -> str:
    rows = list(csv.DictReader(open(DATA / "ledger.csv", newline="", encoding="utf-8")))
    out = [",".join(LEDGER_COLS)]
    for r in rows:
        out.append(",".join((r.get(c) or "").replace(",", ";") for c in LEDGER_COLS))
    return "\n".join(out)


def build() -> str:
    e = ["## Appendix E — AI reference data (machine-oriented)", "",
         "*This appendix is for **machine readers** — council members scoring this report under the blind protocol, "
         "and any other AI analyst. It is the full evidence base in flat form; nothing here is new relative to the "
         "tables above, and **human readers can stop before this point**. Generated deterministically by "
         "`method/6-script-build-ai-notes.py` from the pipeline data files (CI-verified); never hand-edited.*", "",
         "**Canonical definitions & principles.** Client assets (CA) = customer deposits + wealth AUM. "
         "Other Revenue (OR) = total income − NII. Currency principle: every series in its reporting currency, never "
         "FX-converted (SG banks = SGD; cross-hub macro = USD as sourced). Benchmark indices set the index bank "
         "HSBC = 100. Cross-border (\"offshore\") wealth = financial wealth booked by non-residents only. Cell "
         "marking: `n/r` = not retrieved · `n/d` = not disclosed; derived cells are unmarked.", "",
         "### E.1 Reconciled ledger (all series, FY2016–1Q2026)", "",
         "*Projection of `pipeline/sg-banks/data/ledger.csv` — full per-cell provenance (dual-retriever columns, "
         "sources, run stamps) lives in the file itself. Embedded commas are shown as `;`.*", "",
         "```csv", ledger_projection(), "```", "",
         "### E.2 Peer financials (`data/peers.csv`, verbatim)", "",
         "```csv", (DATA / "peers.csv").read_text(encoding="utf-8").rstrip("\n"), "```", "",
         "### E.3 Wealth-hub flows (`data/flows.csv`, verbatim)", "",
         "```csv", (DATA / "flows.csv").read_text(encoding="utf-8").rstrip("\n"), "```", "",
         "### E.4 Open data gaps (from `meta/gaps.json`)", ""]
    gaps = json.loads(GAPS.read_text(encoding="utf-8"))
    for key, g in gaps.items():
        if not isinstance(g, dict) or "rows" not in g:
            continue
        e.append(f"- **{key}** (P{g['priority']}, {g['count']} rows — {g['note']}): " + ", ".join(g["rows"]))
    e.append("")
    return "\n".join(e)


if __name__ == "__main__":
    rendered = build()
    rep = REPORT.read_text(encoding="utf-8")
    if START not in rep or END not in rep:
        sys.exit(f"MARKERS MISSING: {START} / {END} not found in {REPORT}")
    pre, rest = rep.split(START, 1)
    cur, post = rest.split(END, 1)
    new = pre + START + "\n" + rendered + "\n" + END + post
    if "--check" in sys.argv:
        if rep == new:
            print("CHECK OK: report AI-notes region reproducible from data files")
        else:
            sys.exit("CHECK FAIL: report AI-notes region stale — run 6-script-build-ai-notes.py")
    else:
        REPORT.write_text(new, encoding="utf-8")
        print(f"synced AI-notes region in {REPORT}")
