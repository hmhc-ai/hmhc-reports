#!/usr/bin/env python3
"""Build-Conclusions — deterministic council scorecard assembly.

Aggregates the blind council answer sheets (data/scores/<member>.json,
Write-Scores outputs) into data/scorecard.md: an aggregate matrix per frame
question (median performance, range as the disagreement marker, criticality
consensus) followed by one compact block per member. No AI in the assembly:
insight lives upstream in the blind sheets; this step only validates,
sorts, and formats. With no sheets present it emits a deterministic
"no council run yet" placeholder.

Stage 2 (author-approved 2026-07-27): besides data/scorecard.md, the
scorecard is injected into reports/sg-banks.md between the
<!-- conclusions:start --> / <!-- conclusions:end --> markers — the
Conclusions section is now fully deterministic. With no sheets present
both targets carry a "no council run yet" placeholder.

Usage:  python3 pipeline/sg-banks/method/7-script-build-conclusions.py [--check]
Spec:   pipeline/sg-banks/method/7-script-build-conclusions.md
"""
import json, statistics, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCORES = ROOT / "data" / "scores"
HEALTH = ROOT / "meta" / "health.json"
OUT = ROOT / "data" / "scorecard.md"
REPORT = ROOT.parents[1] / "reports" / "sg-banks.md"
CSTART, CEND = "<!-- conclusions:start -->", "<!-- conclusions:end -->"

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
    sf = s.get("suggested_factors", [])
    if not isinstance(sf, list) or len(sf) > 3:
        errs.append("suggested_factors must be a list of at most 3 entries")
    else:
        for f in sf:
            if not (isinstance(f, dict) and f.get("name") and f.get("rationale")):
                errs.append("each suggested factor needs a name and a rationale")
    return errs


def fmt_perf(v: int) -> str:
    return f"+{v}" if v > 0 else str(v)


def core(sheets, qs, member_h: str) -> list:
    """The scorecard body (matrix + member blocks), heading level parameterized."""
    e = [f"Council of {len(sheets)}: " + " · ".join(f"`{s['member']}`" for s in sheets)
         + ". Each member scored **blind** (frame + report body only, prior Conclusions removed; protocol "
         "`method/7-ai-write-scores.md`). Performance = alignment with the thesis, −5…+5 · criticality = how "
         "decisive the factor is for the thesis. Disagreement ranges are shown deliberately — they are a signal.", ""]
    e += ["| Factor | Topic | Perf (median) | Range | Criticality (consensus) |", "|---|---|---:|---:|---|"]
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
        e += [f"{member_h} {s['member']} — {s['harness']} ({s['model']}) · {s['date']} · scored v{s['report_version']}", ""]
        for a in s["answers"]:
            e.append(f"- **{a['q']}** · {fmt_perf(a['performance'])} · {a['criticality']} — {a['comment']}")
        e.append(f"- **Thesis** · {fmt_perf(s['thesis']['performance'])} — {s['thesis']['comment']}")
        e.append("")
    suggestions = [(s["member"], f) for s in sheets for f in s.get("suggested_factors", [])]
    if suggestions:
        e += [f"{member_h} Council-suggested factors (not yet in the frame; adoption is the author's decision)", ""]
        for member, f in suggestions:
            e.append(f"- **{f['name']}** (`{member}`) — {f['rationale']}")
        e.append("")
    return e


def build() -> tuple:
    qs = questions()
    sheets = load_sheets()
    art = ["# SG Banks — Council scorecard (generated artifact)", "",
           "*Artifact: `pipeline/sg-banks/data/scorecard.md` — sole output of `pipeline/sg-banks/method/7-script-build-conclusions.py`, "
           "aggregating the blind council sheets in `data/scores/` (see `method/7-ai-write-scores.md` for the protocol and rubric).*", ""]
    if not sheets:
        placeholder = ["**No council run yet** — no sheets in `data/scores/`. The scorecard populates when Write-Scores runs.", ""]
        rep = ["## Conclusions — Council Scorecard", ""] + placeholder
        return "\n".join(art + placeholder), "\n".join(rep).rstrip()
    body = core(sheets, qs, "##")
    rep = ["## Conclusions — Council Scorecard", ""] + core(sheets, qs, "###") + [
        "*The council scores the frame's key factors; the full frame-format analysis is in Supporting Data below. "
        "Assembled deterministically by `method/7-script-build-conclusions.py`. Not investment advice.*"]
    return ("\n".join(art + body).rstrip() + "\n",
            "\n".join(rep).rstrip())


def report_region(rendered: str) -> tuple:
    rep = REPORT.read_text(encoding="utf-8")
    if CSTART not in rep or CEND not in rep:
        sys.exit(f"MARKERS MISSING: {CSTART} / {CEND} not found in {REPORT}")
    pre, rest = rep.split(CSTART, 1)
    cur, post = rest.split(CEND, 1)
    new = pre + CSTART + "\n" + rendered + "\n" + CEND + post
    return rep, new


if __name__ == "__main__":
    scorecard, rendered = build()
    rep_old, rep_new = report_region(rendered)
    if "--check" in sys.argv:
        ok_art = OUT.exists() and OUT.read_text(encoding="utf-8") == scorecard
        ok_rep = rep_old == rep_new
        if ok_art and ok_rep:
            print("CHECK OK: scorecard.md + report Conclusions reproducible from council sheets")
        else:
            sys.exit("CHECK FAIL: " + ("scorecard.md stale; " if not ok_art else "")
                     + ("report Conclusions region stale" if not ok_rep else "") + " — run build_conclusions.py")
    else:
        OUT.write_text(scorecard, encoding="utf-8")
        REPORT.write_text(rep_new, encoding="utf-8")
        print(f"wrote {OUT} and synced report Conclusions region")
