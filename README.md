# Organisational Dysfunction

|  |  |
|---|---|
| **Creator** | Sigurd Sæther Sørensen |
| **Based on** | Trond Hjorteland — *Organisational Dysfunction of the Day* ([full list](https://www.linkedin.com/pulse/organisational-dysfunction-day-full-list-trond-hjorteland-gxrze/)) |
| **Framework** | Open sociotechnical systems theory (DP1 / DP2) |
| **Contents** | 1 skill · 59 dysfunctions |
| **Version** | 0.1.0 |

A Claude Code plugin of org-design knowledge for diagnosing the recurring ways organisations and teams get stuck — and what to actually do about them.

It packages **59 named dysfunctions** from Trond Hjorteland's *"Organisational Dysfunction of the Day"* series, all read through the same lens: **open sociotechnical systems theory (OST)** and its DP1 (top-down bureaucracy) vs DP2 (self-managing teams) distinction.

## What's inside

One sharp, cleanly-triggering skill — `organisational-dysfunction` — built on Anthropic's progressive-disclosure pattern:

- **`SKILL.md`** — the always-loaded router. Holds the shared DP1/DP2 lens once, plus an index of all 59 dysfunctions grouped by theme.
- **`references/NN-*.md`** — one lean file per dysfunction: how it shows up, the sociotechnical diagnosis (the *why*), and concrete remedies. Claude reads only the one(s) that match.

## When it triggers

Whenever someone describes a workplace or team problem that smells structural rather than personal: stuck or slow decisions, hollow agile ceremonies (standups, retros, OKRs, DORA, Team Topologies), disengagement or "quiet quitting", a "frozen middle", stalled change initiatives, AI dropped into a broken process, or blame aimed at people instead of the system.

## Installation

This repository is a Claude Code plugin marketplace. Add it as a marketplace and install the `organisational-dysfunction` plugin, or drop the `skills/organisational-dysfunction` folder into your `~/.claude/skills/` directory.

## Attribution

The references **synthesise and paraphrase** [Trond Hjorteland](https://www.linkedin.com/in/trondhjort/)'s publicly posted series through the OST framing he uses — they are not verbatim copies. For his own words, see his article [**"Organisational Dysfunction of the Day — full list"**](https://www.linkedin.com/pulse/organisational-dysfunction-day-full-list-trond-hjorteland-gxrze/) on LinkedIn (which links every individual post) and his forthcoming (2026) book.

Each reference file also notes its source dysfunction number; the corresponding original post can be found via the full-list article above.
