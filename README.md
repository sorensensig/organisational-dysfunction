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

Two ways: install it as a plugin (recommended — you get updates by pulling the repo), or just copy the skill folder in.

### Option 1 — Install as a plugin (recommended)

A "marketplace" in Claude Code is just a Git repo that lists installable plugins. You point Claude Code at this repo once, then install the plugin from it. Run these inside Claude Code:

1. **Add this repo as a marketplace** (do this once):
   ```
   /plugin marketplace add sorensensig/organisational-dysfunction
   ```
2. **Install the plugin** from it:
   ```
   /plugin install organisational-dysfunction@sorensen-skills
   ```
   The format is `plugin-name@marketplace-name` — here the plugin is `organisational-dysfunction` and the marketplace is `sorensen-skills`.
3. If the skill isn't active immediately, **restart Claude Code** (or run `/reload-plugins`).

**Prefer clicking to typing?** Just run `/plugin` to open the manager: go to the **Marketplaces** tab and add `sorensensig/organisational-dysfunction`, then the **Discover** tab, pick **organisational-dysfunction**, and press Enter to install.

Once installed, the skill activates **automatically** whenever you describe an org/team dysfunction — you don't invoke it by name.

- **Check it's installed:** `/plugin` → **Installed** tab.
- **Uninstall:** `/plugin uninstall organisational-dysfunction@sorensen-skills`
- **Remove the marketplace entirely:** `/plugin marketplace remove sorensen-skills`

### Option 2 — Copy the skill folder (simplest, no plugin system)

```bash
git clone https://github.com/sorensensig/organisational-dysfunction
cp -r organisational-dysfunction/skills/organisational-dysfunction ~/.claude/skills/
```

Restart Claude Code and you're done.

### Team / scripted setup (optional)

To have a whole team pick it up automatically, add this to the project's `.claude/settings.json` (they'll be prompted to trust and install it):

```json
{
  "extraKnownMarketplaces": {
    "sorensen-skills": {
      "source": { "source": "github", "repo": "sorensensig/organisational-dysfunction" }
    }
  },
  "enabledPlugins": {
    "organisational-dysfunction@sorensen-skills": true
  }
}
```

## Attribution

The references **synthesise and paraphrase** [Trond Hjorteland](https://www.linkedin.com/in/trondhjort/)'s publicly posted series through the OST framing he uses — they are not verbatim copies. For his own words, see his article [**"Organisational Dysfunction of the Day — full list"**](https://www.linkedin.com/pulse/organisational-dysfunction-day-full-list-trond-hjorteland-gxrze/) on LinkedIn (which links every individual post) and his forthcoming (2026) book.

Each reference file also notes its source dysfunction number; the corresponding original post can be found via the full-list article above.
