#!/usr/bin/env python3
"""Build-Conclusions — deterministic council scorecard assembly.

Aggregates the blind council answer sheets (data/scores/<member>.json,
Write-Scores outputs) into data/scorecard.md: an aggregate matrix per frame
question (median performance, range as the disagreement marker, criticality
consensus) followed by one compact block per member. No AI in the assembly:
insight lives upstream in the blind sheets; this step only validates,
sorts, and formats. With no sheets present it emits a deterministic
"no council run yet" placeholder.

Stage note: output goes to data/scorecard.md only. Wiring the scorecard
into the report's Conclusions section awaits the author's approval of the
frame restructure (see method/ai/write-scores.md and IDEAS/registry).

Usage:  python3 pipeline/sg-banks/method/code/build_conclusions.py [--check]
Spec:   pipeline/sg-banks/method/code/build-conclusions.md
"""
import json, statistics, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCORES = ROOT / "data" / "scores"
HEALTH = ROOT / "meta" / "health.json"
OUT = ROOT / "data" / "scorecard.md"

CRIT = ["critical", "high", "medium", "low"]


def questions() -> list:
    h = json.loads(HEALTH.read_text(encoding="utf-8"))
    return [(q["id"], q["topic"]) for q in h.get("completeness", {}).get("questions", [])]


def load_sheets() -> list:
    sheets = []
    if SCORES.is_dir():
        for p in sorted(SCORES.glob("*.json")):
            s = json.loads(p.read_text(encoding="utf-8"))
            errs = validate(s, p.name)
            if errs:
                sys.exit("INVALID SHEET " + p.name + ":\n  - " + "\n  - ".join(errs))
            sheets.append(s)
    return sheets


def validate(s: dict, name: str) -> list:
    errs = []
    qids = [q for q, _ in questions()]
    got = [a.get("q") for a in s.get("answers", [])]
    if got != qids:
        errs.append(f"answers must cover exactly {qids} in order; got {got}")
    for a in s.get("answers", []):
        if not (isinstance(a.get("performance"), int) and -5 <= a["performance"] <= 5):
            errs.append(f"{a.get('q')}: performance must be an integer in [-5, 5]")
        if a.get("criticality") not in CRIT:
            errs.append(f"{a.get('q')}: criticality must be one of {CRIT}")
        if not a.get("comment"):
            errs.append(f"{a.get('q')}: comment required")
    t = s.get("thesis", {})
    if not (isinstance(t.get("performance"), int) and -5 <= t["performance"] <= 5):
        errs.append("thesis.performance must be an integer in [-5, 5]")
    for field in ("member", "harness", "model", "date", "report_version"):
        if not s.get(field):
            errs.append(f"missing field: {field}")
    if s.get("blind") is not True:
        errs.append("blind must be true")
    if s.get("member") != Path(name).stem:
        errs.append(f"member '{s.get('member')}' must match filename '{Path(name).stem}'")
    return errs


def fmt_perf(v: int) -> str:
    return f"+{v}" if v > 0 else str(v)


def build() -> str:
    qs = questions()
    sheets = load_sheets()
    e = ["# SG Banks — Council scorecard (generated artifact)", "",
         "*Artifact: `pipeline/sg-banks/data/scorecard.md` — sole output of `pipeline/sg-banks/method/code/build_conclusions.py`, "
         "aggregating the blind council sheets in `data/scores/` (see `method/ai/write-scores.md` for the protocol and rubric). "
         "Performance = alignment with the thesis, −5…+5. Criticality = how decisive the question is for the thesis. "
         "Range shows council disagreement — it is a signal, not noise.*", ""]
    if not sheets:
        e += ["**No council run yet** — no sheets in `data/scores/`. The scorecard populates when Write-Scores runs.", ""]
        return "\n".join(e)

    e += [f"Council of {len(sheets)}: " + " · ".join(f"`{s['member']}`" for s in sheets)
          + f" — scored against report v{sheets[0]['report_version']}.", "",
          "| Q | Topic | Perf (median) | Range | Criticality (consensus) |", "|---|---|---:|---:|---|"]
    for qid, topic in qs:
        vals = [next(a for a in s["answers"] if a["q"] == qid)["performance"] for s in sheets]
        crits = [next(a for a in s["answers"] if a["q"] == qid)["criticality"] for s in sheets]
        med = statistics.median(vals)
        med_s = fmt_perf(int(med)) if float(med).is_integer() else f"{med:+.1f}"
        rng = f"{fmt_perf(min(vals))}…{fmt_perf(max(vals))}" if min(vals) != max(vals) else "unanimous"
        cmode = max(CRIT, key=lambda c: (crits.count(c), -CRIT.index(c)))
        cs = cmode + ("" if all(c == cmode for c in crits) else f" ({' / '.join(sorted(set(crits), key=CRIT.index))})")
        e.append(f"| {qid} | {topic} | {med_s} | {rng} | {cs} |")
    tvals = [s["thesis"]["performance"] for s in sheets]
    tmed = statistics.median(tvals)
    tmed_s = fmt_perf(int(tmed)) if float(tmed).is_integer() else f"{tmed:+.1f}"
    e += [f"| — | **Thesis overall** | **{tmed_s}** | {fmt_perf(min(tvals))}…{fmt_perf(max(tvals))} | — |", ""]

    for s in sheets:
        e += [f"## {s['member']} — {s['harness']} ({s['model']}), {s['date']}", ""]
        for a in s["answers"]:
            e.append(f"- **{a['q']}** · {fmt_perf(a['performance'])} · {a['criticality']} — {a['comment']}")
        e.append(f"- **Thesis** · {fmt_perf(s['thesis']['performance'])} — {s['thesis']['comment']}")
        e.append("")
    return "\n".join(e).rstrip() + "\n"


if __name__ == "__main__":
    content = build()
    if "--check" in sys.argv:
        if OUT.exists() and OUT.read_text(encoding="utf-8") == content:
            print("CHECK OK: scorecard.md reproducible from council sheets")
        elif not OUT.exists():
            sys.exit("CHECK FAIL: data/scorecard.md missing — run build_conclusions.py")
        else:
            sys.exit("CHECK FAIL: committed scorecard.md differs from generated output")
    else:
        OUT.write_text(content, encoding="utf-8")
        print(f"wrote {OUT}")
