# data/scores/ — blind council answer sheets

One `<member>.json` per council member per report version, produced under the blind protocol in
`../../method/ai/write-scores.md` (`<member>` = harness+model provenance code, e.g. `CwClFable5.json`,
`PxGPT5.6.json`). Aggregated deterministically by `../../method/code/build_conclusions.py` into
`../scorecard.md`. Sheets are never hand-edited: an invalid sheet is rejected and the member reruns.
Currently empty — the first council run awaits the author's authorization of the roster.
