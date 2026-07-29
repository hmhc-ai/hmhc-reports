# data/scores/ — blind council answer sheets

One `<member>.json` per council member per report version, produced under the blind protocol in
`../../method/7-ai-write-scores.md` (`<member>` = harness+model provenance code, e.g. `CwClFable5.json`,
`PxGPT5.6.json`). Aggregated deterministically by `../../method/7-script-build-conclusions.py` into
`../scorecard.md`. Sheets are never hand-edited: an invalid sheet is rejected and the member reruns.

Admissibility (see the SOP § Member identity & admissibility): one seat per lab; model identity must be
verifiable (lab-native harness or pinned API model ID); sheets from multi-model routers (e.g. Perplexity
Model Council) are inadmissible — advisory context only, never committed here.

Seated: `CwClFable5.json` (Anthropic seat, Claude Code) · `GkGrok4.json` (xAI seat, Grok app — author-run
lab-native seat packet, 2026-07-29). Open seats: GPT · Gemini — to be filled the same way (see `PERPLEXITY.md`
Completed Job #4 for why Model Council could not fill them).
