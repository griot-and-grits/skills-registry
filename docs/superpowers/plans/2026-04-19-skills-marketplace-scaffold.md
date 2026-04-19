# Skills Marketplace Scaffold Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Scaffold `skills-registry` as a Claude Code plugin marketplace with a single bundled `griot-grits` plugin.

**Architecture:** The repo root holds a `.claude-plugin/marketplace.json` that acts as the marketplace endpoint. A single plugin lives at `plugins/griot-grits/` with its own `.claude-plugin/plugin.json` and a `skills/` directory. Skills are added by creating `plugins/griot-grits/skills/<skill-name>/SKILL.md` files.

**Tech Stack:** JSON (marketplace/plugin metadata), Markdown with YAML frontmatter (skills), Git

---

## File Map

| Status | Path | Purpose |
|--------|------|---------|
| Create | `.claude-plugin/marketplace.json` | Marketplace index — the endpoint the harness fetches |
| Create | `plugins/griot-grits/.claude-plugin/plugin.json` | Plugin metadata for `griot-grits` |
| Create | `plugins/griot-grits/skills/example-skill/SKILL.md` | Example skill demonstrating correct format |
| Create | `README.md` | Usage instructions for marketplace consumers |

---

### Task 1: Create the marketplace index

**Files:**
- Create: `.claude-plugin/marketplace.json`

- [ ] **Step 1: Create the `.claude-plugin` directory and `marketplace.json`**

Create the file at `.claude-plugin/marketplace.json` with this exact content:

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

- [ ] **Step 2: Verify the file is valid JSON**

```bash
python3 -c "import json; json.load(open('.claude-plugin/marketplace.json')); print('valid')"
```

Expected output: `valid`

- [ ] **Step 3: Commit**

```bash
git add .claude-plugin/marketplace.json
git commit -m "feat: add marketplace.json endpoint"
```

---

### Task 2: Create the griot-grits plugin metadata

**Files:**
- Create: `plugins/griot-grits/.claude-plugin/plugin.json`

- [ ] **Step 1: Create the plugin directory structure and `plugin.json`**

Create the file at `plugins/griot-grits/.claude-plugin/plugin.json` with this exact content:

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

- [ ] **Step 2: Verify the file is valid JSON**

```bash
python3 -c "import json; json.load(open('plugins/griot-grits/.claude-plugin/plugin.json')); print('valid')"
```

Expected output: `valid`

- [ ] **Step 3: Commit**

```bash
git add plugins/griot-grits/.claude-plugin/plugin.json
git commit -m "feat: add griot-grits plugin metadata"
```

---

### Task 3: Add an example skill

**Files:**
- Create: `plugins/griot-grits/skills/example-skill/SKILL.md`

- [ ] **Step 1: Create the example skill**

Create the file at `plugins/griot-grits/skills/example-skill/SKILL.md` with this content:

```markdown
---
name: example-skill
description: Use this as a template when creating new Griot and Grits skills. Demonstrates the required SKILL.md format including frontmatter fields and content structure.
version: 1.0.0
---

# Example Skill

This file is a template for new Griot and Grits skills.

## When This Skill Applies

Describe the conditions under which Claude should invoke this skill. Be specific about trigger phrases, keywords, or task types.

## Instructions

Provide the actual guidance, steps, or content Claude should follow when this skill is active.
```

- [ ] **Step 2: Verify frontmatter is present**

```bash
head -6 plugins/griot-grits/skills/example-skill/SKILL.md
```

Expected output — the first line must be `---` and all three frontmatter fields must be present:
```
---
name: example-skill
description: Use this as a template...
version: 1.0.0
---
```

- [ ] **Step 3: Commit**

```bash
git add plugins/griot-grits/skills/example-skill/SKILL.md
git commit -m "feat: add example skill template"
```

---

### Task 4: Write the README

**Files:**
- Create: `README.md`

- [ ] **Step 1: Create `README.md`**

Create the file at `README.md` with this content:

```markdown
# Griot and Grits Skills Registry

A Claude Code plugin marketplace containing the Griot and Grits skill collection.

## Installing

Add this marketplace to your Claude Code environment, then install the plugin:

\`\`\`bash
claude plugins marketplace add github:griot-and-grits/skills-registry
claude plugins install griot-grits
\`\`\`

## Adding a New Skill

1. Create a directory under `plugins/griot-grits/skills/<skill-name>/`
2. Add a `SKILL.md` file with the required frontmatter:

\`\`\`markdown
---
name: skill-name
description: Use when the user asks to... [trigger conditions]
version: 1.0.0
---

# Skill content here
\`\`\`

3. Commit and push — the skill is immediately available to anyone who has the plugin installed.

## Structure

\`\`\`
skills-registry/
├── .claude-plugin/
│   └── marketplace.json        ← marketplace endpoint
├── plugins/
│   └── griot-grits/
│       ├── .claude-plugin/
│       │   └── plugin.json     ← plugin metadata
│       └── skills/
│           └── <skill-name>/
│               └── SKILL.md    ← one directory per skill
└── README.md
\`\`\`
```

- [ ] **Step 2: Commit**

```bash
git add README.md
git commit -m "docs: add README with install and contribution instructions"
```

---

### Task 5: Smoke-test the marketplace locally

- [ ] **Step 1: Verify repo structure matches the spec**

```bash
find . -not -path './.git/*' | sort
```

Expected output (order may vary):
```
.
./.claude-plugin
./.claude-plugin/marketplace.json
./LICENSE
./README.md
./docs
./docs/superpowers
./docs/superpowers/plans
./docs/superpowers/plans/2026-04-19-skills-marketplace-scaffold.md
./docs/superpowers/specs
./docs/superpowers/specs/2026-04-19-skills-marketplace-design.md
./plugins
./plugins/griot-grits
./plugins/griot-grits/.claude-plugin
./plugins/griot-grits/.claude-plugin/plugin.json
./plugins/griot-grits/skills
./plugins/griot-grits/skills/example-skill
./plugins/griot-grits/skills/example-skill/SKILL.md
```

- [ ] **Step 2: Confirm `source` path in marketplace.json resolves to the plugin directory**

```bash
python3 -c "
import json, os
m = json.load(open('.claude-plugin/marketplace.json'))
for p in m['plugins']:
    src = p['source']
    if src.startswith('./'):
        path = src[2:]
        exists = os.path.isdir(path)
        print(f'{src} -> {path}: {\"OK\" if exists else \"MISSING\"}')"
```

Expected output:
```
./plugins/griot-grits -> plugins/griot-grits: OK
```

- [ ] **Step 3: Commit the spec and plan docs if not already committed**

```bash
git add docs/
git commit -m "docs: add design spec and implementation plan"
```
