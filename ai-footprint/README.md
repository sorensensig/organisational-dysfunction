# AI Footprint

|  |  |
|---|---|
| **Creator** | Sigurd Sæther Sørensen |
| **Coefficients** | [claude-carbon](https://github.com/gwittebolle/claude-carbon) (MIT) · fit to [Jegham et al. 2025, arXiv:2505.09598](https://arxiv.org/abs/2505.09598) |
| **Contents** | 1 command (`/footprint`) · 1 statusline script · evals |
| **Dependencies** | None — plain Node stdlib, **zero network calls** |
| **Version** | 0.1.0 |

A Claude Code plugin that turns your session's token usage into an **order-of-magnitude environmental footprint estimate** — energy, CO2e, and water — **always shown as ranges, never point values**, because that is the honest precision of what anyone outside Anthropic can know.

> Order-of-magnitude estimate, not a measurement. Anthropic publishes no per-token energy data; coefficients are third-party benchmarks fit to Claude Sonnet on assumed AWS hardware. Published per-query figures span two orders of magnitude.

## What's inside

Everything is one auditable, dependency-free script — `scripts/footprint.js` — exposed two ways:

- **`/footprint`** — a slash command that reads the session transcript JSONL (per-request `input_tokens` / `output_tokens` / `cache_read_input_tokens` per model), aggregates it, and renders a report: total ranges, a per-model breakdown, and A4-paper-sheet equivalents.
- **Statusline** (optional) — the same engine in compact form, showing a running `CO2e ~x – y | water ~x – y (est)` estimate at the bottom of Claude Code as you work.

It reads only the local transcript file. No telemetry, no network, no packages — you can audit the whole thing in one sitting.

## Installation

1. **Add the store as a marketplace** (once):
   ```
   /plugin marketplace add sorensensig/ai-corner-store
   ```
2. **Install the plugin:**
   ```
   /plugin install ai-footprint@ai-corner-store
   ```
3. Restart Claude Code (or `/reload-plugins`), then run **`/footprint`** in any session.

### Statusline setup (optional)

Claude Code's status line is user-level configuration, so plugins can't switch it on for you. Copy the script somewhere stable and point your settings at it:

```bash
git clone https://github.com/sorensensig/ai-corner-store
cp ai-corner-store/ai-footprint/scripts/footprint.js ~/.claude/footprint.js
```

Then in `~/.claude/settings.json`:

```json
{
  "statusLine": {
    "type": "command",
    "command": "node ~/.claude/footprint.js statusline"
  }
}
```

The script reads the statusline JSON Claude Code passes on stdin, follows its `transcript_path`, and prints one compact line. (A copied file won't update itself — Watch → Releases on this repo to hear about new versions.)

## Methodology

The entire calculation, so you can check it — or dispute it.

**Formula.** For each model in the session transcript (deduplicated by API message id, since Claude Code writes one transcript line per content block):

```
kWh = [ (input_tokens + cache_creation_tokens) × C_in
        + cache_read_tokens × C_in × 0.08
        + output_tokens × C_out ] / 1,000,000

CO2e (g)          = kWh × 287     (AWS US, location-based grid intensity)
Water on-site (L) = kWh × 0.18    (AWS water-usage effectiveness — datacenter cooling)
Water off-site (L)= kWh × 2 – 3   (electricity-generation water, shown separately)
```

**Per-token energy coefficients** (kWh per million tokens) come from the [claude-carbon](https://github.com/gwittebolle/claude-carbon) project (MIT licence, © gwittebolle), which fit them to the measurements in [Jegham et al. 2025, *"How Hungry is AI?"* (arXiv:2505.09598)](https://arxiv.org/abs/2505.09598):

| model family | C_in (kWh/Mtok) | C_out (kWh/Mtok) | provenance |
|---|---|---|---|
| Haiku | 0.07 | 1.44 | 0.5× scaling of the Sonnet fit |
| Sonnet | 0.14 | 2.88 | fit to Jegham et al. measurements of Claude Sonnet |
| Opus | 0.27 | 5.76 | 2× extrapolation of the Sonnet fit |
| unknown model ids | 0.14 | 2.88 | Sonnet assumed, flagged in the report |

- **Cache reads** are billed ~10% of input price and skip prefill compute; following claude-carbon they are counted at **8% of the input coefficient**. Cache *writes* (`cache_creation_input_tokens`) are processed like fresh input and counted at the full input coefficient.
- **CO2e:** 287 g/kWh is an AWS US **location-based** grid-intensity figure (market-based figures, which credit renewable purchases, would be far lower — we deliberately use the physical grid mix).
- **Water:** on-site (~0.18 L/kWh, AWS's published WUE — evaporated in datacenter cooling) and off-site (~2–3 L/kWh — water consumed generating the electricity) are **different categories and are never summed** in the report; they're always labeled separately.
- **Ranges:** every displayed figure is the central estimate spanned by **÷3 to ×3** — roughly one order of magnitude, which is generous *given that published per-query energy figures for frontier LLMs span two*. Per-model central values are shown in the report only so you can reproduce the arithmetic.
- **Paper equivalents:** one A4 sheet ≈ **5 g CO2e** (lifecycle midpoint of common ~2–10 g estimates) and ≈ **10 L** lifecycle water (midpoint of published estimates). The sheet counts are derived from the range, so they are ranges too. The water comparison uses the off-site (generation) figure and says so.

**What this deliberately does not capture:** embodied emissions of the hardware, model training, Anthropic's actual hardware/utilization/PUE, datacenter location (grid intensity varies ~20× by region), or your subagents' transcripts (each session file is counted on its own).

> **Disclaimer (repeated on every report):** Order-of-magnitude estimate, not a measurement. Anthropic publishes no per-token energy data; coefficients are third-party benchmarks fit to Claude Sonnet on assumed AWS hardware. Published per-query figures span two orders of magnitude.

## Evals

`evals/` holds a hand-built fixture transcript (three models, a duplicated message id, cache reads, synthetic/no-usage noise lines) and hand-computed expected numbers. Run:

```bash
sh evals/check.sh
```

It verifies the full pipeline — parsing, message-id dedupe, per-model coefficients, cache-read discounting, range/equivalent arithmetic — and smoke-tests the statusline mode.

## Attribution

- Per-token coefficients: [**claude-carbon**](https://github.com/gwittebolle/claude-carbon), MIT licence, © gwittebolle. This plugin reimplements the coefficient table; no code is copied.
- Underlying measurements: Nidhal Jegham, Marwen Abdelatti, Lassad Elmoubarki, Abdeltawab Hendawi, *"How Hungry is AI? Benchmarking Energy, Water, and Carbon Footprint of LLM Inference"*, 2025, [arXiv:2505.09598](https://arxiv.org/abs/2505.09598).

## Changelog

### 0.1.0 — 2026-07-10
- Initial release: `/footprint` session report (totals, per-model breakdown, A4-paper equivalents — all as ranges), optional statusline script, methodology note, and the fixture-based math eval.
