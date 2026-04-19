# Griot and Grits Skills Registry

A Claude Code plugin marketplace containing the Griot and Grits skill collection.

## Installing

Add this marketplace to your Claude Code environment, then install the plugin:

```bash
claude plugins marketplace add github:griot-and-grits/skills-registry
claude plugins install griot-grits
```

## Adding a New Skill

1. Create a directory under `plugins/griot-grits/skills/<skill-name>/`
2. Add a `SKILL.md` file with the required frontmatter:

```markdown
---
name: skill-name
description: Use when the user asks to... [trigger conditions]
version: 1.0.0
---

# Skill content here
```

3. Commit and push — the skill is immediately available to anyone who has the plugin installed.

## Structure

```
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
```
