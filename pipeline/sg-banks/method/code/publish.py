#!/usr/bin/env python3
"""Publish — one-command release bookkeeping for sg-banks.

Automates the mechanical parts of UPDATE.md Step 5, which were previously
six hand-edits per release:

  1. computes the next version (YYYY.MM.DD of today; -rN if same-day);
  2. updates reports/sg-banks/meta.json: current_version, last_updated,
     and refresh_note = THIS release's note + a pointer to the registry
     (the registry changelog is the canonical history — see UPDATE.md);
  3. inserts a changelog entry at the top of pipeline/sg-banks/index.md;
  4. appends a row to meta/history.csv (version, date, thesis score,
     questions answered, fill/confidence metrics from meta/health.json);
  5. runs every CI gate (docs lint + all --check modules) and fails loudly
     if any gate fails.

It does NOT commit, push, or tag: review the diff, commit with the usual
trailers, open the PR; the tag is auto-created on main by tag-version.yml.
Not a CI artifact generator (it uses today's date), so it has no --check
gate of its own; --dry-run previews without writing.

Usage:
  python3 pipeline/sg-banks/method/code/publish.py --desc "One-sentence release note." [--changelog "Rich changelog entry (defaults to --desc)"] [--dry-run]
"""
import argparse, csv, datetime, json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPO = ROOT.parents[1]
META = REPO / "reports" / "sg-banks" / "meta.json"
REGISTRY = ROOT / "index.md"
HISTORY = ROOT / "meta" / "history.csv"
HEALTH = ROOT / "meta" / "health.json"
REPORT = REPO / "reports" / "sg-banks" / "report.md"

GATES = [
    [sys.executable, str(REPO / ".github" / "scripts" / "docs_lint.py")],
    *[[sys.executable, str(ROOT / "method" / "code" / f"build_{m}.py"), "--check"]
      for m in ("tables", "charts", "benchmarks", "health", "gaps", "report_tables", "conclusions")],
]


def next_version(current: str, today: str) -> str:
    if not current.startswith(today):
        return today
    m = re.fullmatch(re.escape(today) + r"(?:-r(\d+))?", current)
    n = int(m.group(1)) if m and m.group(1) else 1
    return f"{today}-r{n + 1}"


def thesis_score() -> str:
    m = re.search(r"Thesis score: (\d+)/100", REPORT.read_text(encoding="utf-8"))
    return m.group(1) if m else "n/d"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--desc", required=True, help="one-sentence release note (goes in refresh_note)")
    ap.add_argument("--changelog", default=None, help="rich changelog entry body (defaults to --desc)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    today = datetime.date.today().strftime("%Y.%m.%d")
    date_iso = datetime.date.today().isoformat()
    meta = json.loads(META.read_text(encoding="utf-8"))
    ver = next_version(meta["current_version"], today)

    h = json.loads(HEALTH.read_text(encoding="utf-8"))
    comp, conf = h.get("completeness", {}), h.get("confidence", {})
    row = [ver, date_iso, thesis_score(),
           comp.get("questions_answered"), comp.get("questions_total"),
           comp.get("ledger_filled_pct"), conf.get("dual_verified_pct_of_filled"),
           conf.get("retriever_scorecard", {}).get("agreement_pct")]

    print(f"version : {meta['current_version']} -> {ver}")
    print(f"history : {row}")
    if args.dry_run:
        print("dry-run: no files written, gates not run")
        return 0

    meta["current_version"] = ver
    meta["last_updated"] = date_iso
    meta["pipeline"]["refresh_note"] = (
        f"{ver}: {args.desc} Full release history: pipeline/sg-banks/index.md (Changelog).")
    META.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    entry = f"- **{date_iso} (v{ver})** — {args.changelog or args.desc}\n\n"
    reg = REGISTRY.read_text(encoding="utf-8")
    anchor = "## Changelog\n\n"
    REGISTRY.write_text(reg.replace(anchor, anchor + entry, 1), encoding="utf-8")

    new_file = not HISTORY.exists()
    with open(HISTORY, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new_file:
            w.writerow(["version", "date", "thesis_score", "questions_answered", "questions_total",
                        "ledger_filled_pct", "dual_verified_pct_of_filled", "cross_model_agreement_pct"])
        w.writerow(row)

    for gate in GATES:
        r = subprocess.run(gate)
        if r.returncode != 0:
            sys.exit(f"GATE FAILED: {' '.join(gate)} — fix before committing the release")
    print(f"published bookkeeping for v{ver}: meta.json + registry changelog + history.csv; all gates pass.")
    print("Next: review the diff, commit with trailers, open the PR; the tag is auto-created on main after merge.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
