# Skills Marketplace Design

**Date:** 2026-04-19
**Project:** griot-and-grits/skills-registry
**Status:** Approved

## Overview

Set up `skills-registry` as a Claude Code skills marketplace in the official plugin system format. All Griot and Grits skills are bundled into a single installable plugin (`griot-grits`) served from one marketplace endpoint (the GitHub repo itself).

## Repository Structure

```
skills-registry/
├── .claude-plugin/
│   └── marketplace.json                ← marketplace index (the endpoint)
├── plugins/
│   └── griot-grits/                    ← single bundled plugin
│       ├── .claude-plugin/
│       │   └── plugin.json             ← plugin metadata
│       └── skills/
│           └── <skill-name>/
│               └── SKILL.md            ← one directory per skill
├── README.md
└── LICENSE
```

## File Contents

### `.claude-plugin/marketplace.json`

```json
{
  "$schema": "https://anthropic.com/claude-code/marketplace.schema.json",
  "name": "griot-grits",
  "description": "Griot and Grits skill collection for Claude Code",
  "owner": {
    "name": "Griot and Grits",
    "email": "sherard@griotandgrits.org"
  },
  "plugins": [
    {
      "name": "griot-grits",
      "description": "All Griot and Grits skills for Claude Code",
      "category": "productivity",
      "source": "./plugins/griot-grits",
      "homepage": "https://github.com/griot-and-grits/skills-registry"
    }
  ]
}
```

### `plugins/griot-grits/.claude-plugin/plugin.json`

```json
{
  "name": "griot-grits",
  "description": "Griot and Grits skill collection for Claude Code",
  "author": {
    "name": "Griot and Grits",
    "email": "sherard@griotandgrits.org"
  }
}
```

### `plugins/griot-grits/skills/<skill-name>/SKILL.md`

Each skill is a directory containing a single `SKILL.md` with YAML frontmatter:

```markdown
---
name: skill-name
description: Use when the user asks to... [trigger conditions]
version: 1.0.0
---

# Skill content here
```

**Frontmatter fields:**
- `name` (required): Skill identifier, matches directory name
- `description` (required): Trigger conditions — tells Claude when to invoke this skill
- `version` (optional): Semantic version

## Install Flow

Anyone using skills from this registry runs:

```bash
claude plugins marketplace add github:griot-and-grits/skills-registry
claude plugins install griot-grits
```

To add a new skill: create `plugins/griot-grits/skills/<skill-name>/SKILL.md` and commit.

## Decisions

- **Single plugin vs. per-skill plugins:** All skills bundled in `griot-grits` for simplicity. The marketplace structure allows adding more plugins later without restructuring.
- **Marketplace vs. direct install:** Marketplace approach chosen to match the official plugin ecosystem format and allow future catalog expansion.
