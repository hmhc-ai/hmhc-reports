#!/usr/bin/env python3
"""Build-Report-Tables — sync generated benchmark blocks into report.md.

The published report's Table 6 content is lifted verbatim from
data/benchmarks.md (the Build-Benchmarks output). Hand-copying it invited
transcription errors, so this module makes the lift mechanical: it rewrites
everything between the markers

    <!-- benchmarks:start -->  ...  <!-- benchmarks:end -->

in reports/sg-banks/report.md from the current data/benchmarks.md, applying
the report's fixed presentation transform (section headings dropped; the
flows heading becomes its lead-in sentence). Deterministic: same
benchmarks.md in, same report region out. CI runs --check on every PR.

Usage:  python3 pipeline/sg-banks/method/code/build_report_tables.py [--check]
Spec:   pipeline/sg-banks/method/code/build-report-tables.md
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BENCH = ROOT / "data" / "benchmarks.md"
REPORT = ROOT.parents[1] / "reports" / "sg-banks" / "report.md"
START, END = "<!-- benchmarks:start -->", "<!-- benchmarks:end -->"


def section(text: str, head: str, until: str | None) -> str:
    """Content of a '## head' section, heading line excluded, trimmed."""
    i = text.index(f"## {head}")
    body = text[i:]
    body = body[body.index("\n") + 1:]
    if until is not None:
        body = body[:body.index(f"## {until}")]
    return body.strip()


def generated_region() -> str:
    bm = BENCH.read_text(encoding="utf-8")
    q5 = section(bm, "Monetization (Frame Q5)", "Relative valuation (Frame Q6)")
    q6 = section(bm, "Relative valuation (Frame Q6)", "Wealth-hub capital flows (Frame Q2)")
    flows = section(bm, "Wealth-hub capital flows (Frame Q2)", None)
    flows = "Wealth-hub capital flows (Frame Q2) — cross-border wealth stock per hub:\n\n" + flows
    return q5 + "\n\n" + q6 + "\n\n" + flows


def main() -> int:
    report = REPORT.read_text(encoding="utf-8")
    if START not in report or END not in report:
        sys.exit(f"MARKERS MISSING: {START} / {END} not found in {REPORT}")
    pre, rest = report.split(START, 1)
    _, post = rest.split(END, 1)
    synced = pre + START + "\n" + generated_region() + "\n" + END + post
    if "--check" in sys.argv:
        if synced == report:
            print("CHECK OK: report Table 6 region matches benchmarks.md")
            return 0
        sys.exit("CHECK FAIL: report Table 6 region differs from benchmarks.md — run build_report_tables.py")
    REPORT.write_text(synced, encoding="utf-8")
    print(f"synced Table 6 region in {REPORT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
