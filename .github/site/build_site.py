#!/usr/bin/env python3
"""Build-Site — deterministic static site generator for hmhc-reports.

Renders the published reports (reports.json -> reports/<slug>/) plus each
series' workflow dashboard (pipeline/<slug>/meta/health.json + gaps.json)
and data views (CSVs as sortable tables) into _site/ as self-contained
static HTML. No timestamps, no network, no frameworks: same inputs in,
same site out. Deployed by .github/workflows/pages.yml; _site/ is never
committed.

Usage:  python3 .github/site/build_site.py        # build into _site/
Spec:   .github/site/build-site.md
Deps:   pip install markdown
"""
import csv, html, json, shutil, sys
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parents[2]
SITE_DIR = Path(__file__).resolve().parent
OUT = ROOT / "_site"

MD = markdown.Markdown(extensions=["tables"], output_format="html5")


def md_to_html(text: str) -> str:
    MD.reset()
    return MD.convert(text)


def page(title: str, body: str, root: str, active: str = "") -> str:
    """Wrap body in the site chrome. `root` is the relative prefix to the site root."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<link rel="stylesheet" href="{root}style.css">
</head>
<body>
<header><div class="wrap headrow"><a class="brand" href="{root}index.html">HMHC&nbsp;Reports</a><nav><a href="{root}index.html">Reports</a> <a href="https://github.com/hmhc-ai/hmhc-reports">GitHub</a></nav></div></header>
<main class="wrap">
{body}
</main>
<footer><div class="wrap">Source of record: <a href="https://github.com/hmhc-ai/hmhc-reports">hmhc-ai/hmhc-reports</a> — every number, method file, and revision is version-controlled. <strong>This is not financial advice.</strong> It is a demonstration of the use of AI in business analysis.</div></footer>
<script>
document.querySelectorAll("table.sortable th").forEach((th, i) => {{
  th.style.cursor = "pointer";
  th.addEventListener("click", () => {{
    const tb = th.closest("table").tBodies[0];
    const rows = Array.from(tb.rows);
    const dir = th.dataset.dir === "a" ? -1 : 1;
    th.dataset.dir = dir === 1 ? "a" : "d";
    rows.sort((r1, r2) => {{
      const a = r1.cells[i]?.innerText.trim() ?? "", b = r2.cells[i]?.innerText.trim() ?? "";
      const na = parseFloat(a.replace(/[^0-9.+-]/g, "")), nb = parseFloat(b.replace(/[^0-9.+-]/g, ""));
      if (!isNaN(na) && !isNaN(nb)) return dir * (na - nb);
      return dir * a.localeCompare(b);
    }});
    rows.forEach(r => tb.appendChild(r));
  }});
}});
</script>
</body>
</html>
"""


def csv_table(path: Path, max_rows=None) -> str:
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    if not rows:
        return "<p>Empty file.</p>"
    head, body = rows[0], rows[1:]
    shown = body if max_rows is None else body[:max_rows]
    out = ['<div class="scroll"><table class="sortable"><thead><tr>']
    out += [f"<th>{html.escape(h)}</th>" for h in head]
    out.append("</tr></thead><tbody>")
    for r in shown:
        out.append("<tr>" + "".join(f"<td>{html.escape(c)}</td>" for c in r) + "</tr>")
    out.append("</tbody></table></div>")
    if max_rows is not None and len(body) > max_rows:
        out.append(f"<p class='muted'>Showing first {max_rows} of {len(body)} rows — full file on GitHub.</p>")
    return "".join(out)


def build_report_page(slug: str, rpath: str, meta: dict) -> None:
    body_md = (ROOT / rpath / "report.md").read_text(encoding="utf-8")
    body = md_to_html(body_md)
    header = (
        f'<p class="crumbs"><a href="../index.html">Reports</a> / {html.escape(meta["title"])}</p>'
        f'<p class="meta-line">Version <strong>{html.escape(meta["current_version"])}</strong>'
        f' · last updated {html.escape(meta["last_updated"])}'
        f' · <a href="dashboard.html">workflow dashboard</a> · <a href="data.html">data</a></p>'
    )
    (OUT / slug).mkdir(parents=True, exist_ok=True)
    (OUT / slug / "index.html").write_text(
        page(meta["title"], header + f'<article class="report">{body}</article>', "../", "report"),
        encoding="utf-8")
    assets = ROOT / rpath / "assets"
    if assets.is_dir():
        shutil.copytree(assets, OUT / slug / "assets", dirs_exist_ok=True)


def stat(label: str, value, sub: str = "") -> str:
    subline = f'<div class="sub">{sub}</div>' if sub else ""
    return f'<div class="stat"><div class="value">{value}</div><div class="label">{label}</div>{subline}</div>'


def build_dashboard_page(slug: str, meta: dict) -> None:
    hp = ROOT / "pipeline" / slug / "meta" / "health.json"
    gp = ROOT / "pipeline" / slug / "meta" / "gaps.json"
    if not hp.exists():
        return
    h = json.loads(hp.read_text(encoding="utf-8"))
    comp, conf = h.get("completeness", {}), h.get("confidence", {})
    score = conf.get("retriever_scorecard", {})

    tiles = '<div class="stats">' + "".join([
        stat("questions answered", f'{comp.get("questions_answered", "?")}/{comp.get("questions_total", "?")}'),
        stat("ledger fill", f'{comp.get("ledger_filled_pct", "?")}%',
             f'{comp.get("ledger_filled", "?")} of {comp.get("ledger_rows", "?")} rows'),
        stat("dual-verified", f'{conf.get("dual_verified_pct_of_filled", "?")}%',
             f'{conf.get("single_retriever_rows", "?")} rows single-retriever'),
        stat("cross-model agreement", f'{score.get("agreement_pct", "?")}%',
             f'{score.get("agree_within_half_pct", "?")}/{score.get("both_filled_numeric", "?")} within 0.5%'),
    ]) + "</div>"

    qrows = "".join(
        f'<tr><td>{q["id"]}</td><td>{html.escape(q["topic"])}</td>'
        f'<td><span class="pill {q["status"].split()[0]}">{html.escape(q["status"])}</span></td>'
        f'<td class="muted">{html.escape(q["depends_on"])}</td></tr>'
        for q in comp.get("questions", []))
    qtable = ('<h2>Key questions</h2><div class="scroll"><table><thead><tr><th>Q</th><th>Topic</th>'
              '<th>Status</th><th>Depends on</th></tr></thead><tbody>' + qrows + "</tbody></table></div>")

    g = json.loads(gp.read_text(encoding="utf-8")) if gp.exists() else {}
    grows = ""
    for key, item in g.items():
        if not isinstance(item, dict) or "priority" not in item:
            continue
        grows += (f'<tr><td>P{item["priority"]}</td><td><code>{html.escape(key)}</code></td>'
                  f'<td>{item.get("count", "")}</td><td class="muted">{html.escape(str(item.get("note", "")))}</td></tr>')
    gtable = ('<h2>Smart-update worklist (gaps)</h2><div class="scroll"><table><thead><tr><th>Priority</th>'
              '<th>Gap</th><th>Rows</th><th>Note</th></tr></thead><tbody>' + grows + "</tbody></table></div>") if grows else ""

    body = (
        f'<p class="crumbs"><a href="../index.html">Reports</a> / <a href="index.html">{html.escape(meta["title"])}</a> / Dashboard</p>'
        f'<h1>Workflow dashboard</h1>'
        f'<p class="meta-line">Pipeline health for <strong>{html.escape(slug)}</strong> at version {html.escape(str(h.get("version", "?")))} '
        f'— generated from <code>meta/health.json</code> and <code>meta/gaps.json</code>, themselves CI-verified pipeline outputs.</p>'
        + tiles + qtable + gtable)
    (OUT / slug / "dashboard.html").write_text(page(f'{meta["title"]} — dashboard', body, "../", "dashboard"), encoding="utf-8")


def build_data_page(slug: str, meta: dict) -> None:
    ddir = ROOT / "pipeline" / slug / "data"
    sections = []
    for name, cap in (("peers.csv", None), ("flows.csv", None), ("ledger.csv", 100)):
        p = ddir / name
        if p.exists():
            gh = f"https://github.com/hmhc-ai/hmhc-reports/blob/main/pipeline/{slug}/data/{name}"
            sections.append(f'<h2><code>{name}</code> <a class="muted small" href="{gh}">raw ↗</a></h2>'
                            + csv_table(p, cap))
    bmk = ddir / "benchmarks.md"
    if bmk.exists():
        sections.append('<h2>Generated benchmarks (<code>benchmarks.md</code>)</h2>'
                        + md_to_html(bmk.read_text(encoding="utf-8")))
    body = (
        f'<p class="crumbs"><a href="../index.html">Reports</a> / <a href="index.html">{html.escape(meta["title"])}</a> / Data</p>'
        f'<h1>Working data</h1><p class="meta-line">Click a column header to sort. Every row carries its source and a '
        f'provenance stamp naming the harness + model that retrieved it.</p>' + "".join(sections))
    (OUT / slug / "data.html").write_text(page(f'{meta["title"]} — data', body, "../", "data"), encoding="utf-8")


def build_index(entries: list) -> None:
    cards = ""
    for e in entries:
        m = e["meta"]
        cards += f"""<a class="card" href="{e["slug"]}/index.html">
<h2>{html.escape(m["title"])}</h2>
<p class="subtitle">{html.escape(m.get("subtitle", ""))}</p>
<p>{html.escape(m.get("summary", ""))}</p>
<p class="meta-line">{html.escape(m.get("status", ""))} · v{html.escape(m.get("current_version", ""))} · updated {html.escape(m.get("last_updated", ""))}</p>
</a>"""
    body = f"""<h1>HMHC Reports</h1>
<p class="lede">Source-graded business analysis produced by a documented, AI-run pipeline — every number reconciled,
every method file versioned, every build CI-verified. The repository is the report.</p>
<div class="cards">{cards}</div>"""
    (OUT / "index.html").write_text(page("HMHC Reports", body, "", "home"), encoding="utf-8")


def main() -> int:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    shutil.copy(SITE_DIR / "style.css", OUT / "style.css")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")

    index = json.loads((ROOT / "reports.json").read_text(encoding="utf-8"))
    entries = []
    for r in index.get("reports", []):
        meta = json.loads((ROOT / r["path"] / "meta.json").read_text(encoding="utf-8"))
        build_report_page(r["slug"], r["path"], meta)
        build_dashboard_page(r["slug"], meta)
        build_data_page(r["slug"], meta)
        entries.append({"slug": r["slug"], "meta": meta})
    build_index(entries)
    n = sum(1 for f in OUT.rglob("*") if f.is_file())
    print(f"wrote {OUT} ({n} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
