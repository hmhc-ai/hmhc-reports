#!/usr/bin/env python3
"""Site-session scope guard: site/* branches may touch only the site module.

Run by the docs-lint workflow on pull requests whose head branch starts
with `site/` — the site/design session's branches (AGENTS.md § Golden
rules, "Site/design session scope"). Fails when any file changed relative
to origin/main falls outside the session's allowed surface:

  .github/site/**                 generator, spec, design system
  .github/workflows/pages.yml     Pages deploy workflow
  pipeline/sg-banks/index.md      registry changelog entries only

Everything else — reports/, the rest of pipeline/**, other workflows,
AGENTS.md itself — belongs to the analysis pipeline and is out of the
site session's write scope. Content flows one way: the pipeline produces
content, the site renders it.

Requires a checkout with origin/main available (fetch-depth: 0).
"""
import subprocess
import sys

ALLOWED_PREFIXES = (".github/site/",)
ALLOWED_FILES = {
    ".github/workflows/pages.yml",
    "pipeline/sg-banks/index.md",
}

changed = [
    line.strip()
    for line in subprocess.run(
        ["git", "diff", "--name-only", "origin/main...HEAD"],
        capture_output=True, text=True, check=True,
    ).stdout.splitlines()
    if line.strip()
]

violations = [
    f for f in changed
    if f not in ALLOWED_FILES and not f.startswith(ALLOWED_PREFIXES)
]

if violations:
    print("SITE SCOPE GUARD FAILED — site/* branches may only touch the site module:")
    for f in violations:
        print("  -", f)
    print("Allowed: .github/site/** · .github/workflows/pages.yml"
          " · pipeline/sg-banks/index.md (changelog entries)")
    sys.exit(1)
print(f"site scope guard OK ({len(changed)} changed file(s), all within the site module)")
