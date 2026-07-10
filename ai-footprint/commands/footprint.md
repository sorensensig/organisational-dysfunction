---
description: Estimate this session's environmental footprint (CO2e + water, as ranges) from the transcript's token usage
allowed-tools: Bash(node:*)
---

Run the footprint report script and show the user its output:

```
node "${CLAUDE_PLUGIN_ROOT}/scripts/footprint.js" report $ARGUMENTS
```

Rules:

- Run it via Bash exactly as above (it makes no network calls; it only reads the local transcript JSONL). If the user passed an argument, it is a transcript path — forward it.
- Relay the script's markdown output **verbatim and in full** — including the ranges, the per-model table, the paper-sheet equivalents, and the disclaimer blockquote. Do not round further, do not collapse ranges into single numbers, do not drop the disclaimer.
- Do not add your own estimates or equivalents on top; the methodology lives in the script and the plugin README. If the user asks how the numbers are computed, point them to the "Methodology" section of the ai-footprint README (and its sources: claude-carbon, MIT, github.com/gwittebolle/claude-carbon; Jegham et al. 2025, arXiv:2505.09598).
- If the script reports that no transcript was found, tell the user they can pass the path explicitly: `/footprint ~/.claude/projects/<project>/<session>.jsonl`.
- Note the script auto-locates the *newest* transcript for the current project directory — if the user runs several sessions in the same folder at once, it may pick a sibling session. The report header names the file it used.
