# Organisational Dysfunction

|  |  |
|---|---|
| **Creator** | Sigurd Sæther Sørensen |
| **Based on** | Trond Hjorteland — *Organisational Dysfunction of the Day* ([full list](https://www.linkedin.com/pulse/organisational-dysfunction-day-full-list-trond-hjorteland-gxrze/)) |
| **Framework** | Open sociotechnical systems theory (DP1 / DP2) |
| **Contents** | 1 skill · 61 dysfunctions |
| **Version** | 0.2.0 |

A Claude Code plugin of org-design knowledge for diagnosing the recurring ways organisations and teams get stuck — and what to actually do about them.

It packages **59 named dysfunctions** from Trond Hjorteland's *"Organisational Dysfunction of the Day"* series, all read through the same lens: **open sociotechnical systems theory (OST)** and its DP1 (top-down bureaucracy) vs DP2 (self-managing teams) distinction.

## What's inside

One sharp, cleanly-triggering skill — `organisational-dysfunction` — built on Anthropic's progressive-disclosure pattern:

- **`SKILL.md`** — the always-loaded router. Holds the shared DP1/DP2 lens once, plus an index of all 59 dysfunctions grouped by theme.
- **`references/NN-*.md`** — one lean file per dysfunction: how it shows up, the sociotechnical diagnosis (the *why*), and concrete remedies. Claude reads only the one(s) that match.

## When it triggers

Whenever someone describes a workplace or team problem that smells structural rather than personal: stuck or slow decisions, hollow agile ceremonies (standups, retros, OKRs, DORA, Team Topologies), disengagement or "quiet quitting", a "frozen middle", stalled change initiatives, AI dropped into a broken process, or blame aimed at people instead of the system.

## Installation

How you install depends on which Claude you use. Pick your surface below. In every case the skill then activates **automatically** when you describe an org/team dysfunction — you never call it by name.

> **Two words worth knowing:** a **skill** is the unit of knowledge (a `SKILL.md` folder). A **plugin** is a bundle you install from a **marketplace** — which is just a Git repo that lists plugins. This repo is both: it contains the skill *and* acts as a one-plugin marketplace named `sorensen-skills`.

### Claude Code (terminal, VS Code, JetBrains)

Run these inside Claude Code:

1. **Add this repo as a marketplace** (once):
   ```
   /plugin marketplace add sorensensig/organisational-dysfunction
   ```
2. **Install the plugin:**
   ```
   /plugin install organisational-dysfunction@sorensen-skills
   ```
   (Format is `plugin-name@marketplace-name`.)
3. If it's not active immediately, **restart Claude Code** (or run `/reload-plugins`).

Prefer clicking? Run **`/plugin`** → **Marketplaces** tab → add `sorensensig/organisational-dysfunction` → **Discover** tab → pick **organisational-dysfunction** → Enter.
Uninstall: `/plugin uninstall organisational-dysfunction@sorensen-skills` · remove marketplace: `/plugin marketplace remove sorensen-skills`.

**No-marketplace alternative** (also works for the local Claude Desktop app, which reads the same folder):
```bash
git clone https://github.com/sorensensig/organisational-dysfunction
cp -r organisational-dysfunction/skills/organisational-dysfunction ~/.claude/skills/
```

### Claude Cowork

1. Open the **Cowork** tab → **Customize** → **Plugins**.
2. Under **Personal plugins**, click **+** → **Add marketplace** → **Add from a repository**, and enter:
   `https://github.com/sorensensig/organisational-dysfunction`
3. Back on the **Plugins** tab, **Browse plugins**, find **organisational-dysfunction**, and click **Install**.

### Claude.ai (web) & Claude Desktop app

These use the **Skills** feature — you upload the packaged skill.

1. **Enable code execution first** (Skills require it):
   - **Free / Pro / Max:** Settings → **Capabilities** → turn on **"Code execution and file creation"**.
   - **Team / Enterprise:** an admin enables it under **Organization settings → Skills**.
2. **Download the packaged skill:** [**organisational-dysfunction-skill.zip**](https://github.com/sorensensig/organisational-dysfunction/releases/latest) (from the latest release).
3. Go to **Customize → Skills**, click **+** → **Create skill** → **Upload a skill**, and select the ZIP.

Skills uploaded this way are per-user and don't sync to other surfaces.
*(To build the ZIP yourself: `cd skills && zip -r organisational-dysfunction-skill.zip organisational-dysfunction` — the folder must sit at the ZIP's root.)*

### Team / scripted setup (Claude Code)

To have a team pick it up automatically, add this to the project's `.claude/settings.json` (members are prompted to trust and install it):

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

## Changelog

New entries are appended automatically by the update pipeline (`loop/pipeline.md`) as Trond publishes them. Newest first.

### 0.2.0 — 2026-07-02
- Added **#60 The output nobody owned** and **#61 Rearranging the furniture** (59 → 61 dysfunctions). Generated via the auto-update pipeline; both passed the targeted routing/triggering test.

### 0.1.0 — 2026-06-30
- Initial release: 59 dysfunctions as one umbrella skill (router `SKILL.md` + `references/`), plus the eval/loop harness and the autoresearch-style tuning loop.
