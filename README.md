# Griot and Grits Skills Registry

A Claude Code plugin marketplace containing the Griot and Grits skill collection — tools for preserving Black voices and Black history, one interview at a time.

## Installing

Add this marketplace to your Claude Code environment, then install the plugin:

```bash
claude plugins marketplace add github:griot-and-grits/skills-registry
claude plugins install griot-grits
```

## Skills

### `video-interview.create-metadata`

Analyzes a Griot and Grits interview transcript and produces publication-ready metadata for all three publishing platforms: the G&G website, YouTube, and Spreaker. Output is a timestamped Markdown file plus a `.metadata.json` for the upload skill.

**Triggers when:** the user wants to generate metadata for a new interview, process a video before publishing, create tags or descriptions from a transcript, or says things like "generate metadata for this video", "process this interview", "prepare this for publishing".

**What it produces:**
- Interview title, description, tags, historical context, and people — derived from the transcript
- Platform-specific sections: website YAML, YouTube title/description/tags, Spreaker title/tags
- `<basename>.metadata.json` consumed by the upload skill

**Requires:** Python, Whisper + ffmpeg (only if transcribing), access to the video or transcript file

---

### `video-interview.upload`

Uploads a prepared Griot and Grits interview to YouTube using the `.metadata.json` produced by `video-interview.create-metadata`. Falls back to a step-by-step manual YouTube Studio guide when API credentials aren't present.

**Triggers when:** the user is ready to upload a video, has metadata ready, wants to publish to the channel, or says things like "upload this video", "publish to YouTube", "the metadata is ready, let's upload".

**What it produces:**
- YouTube upload via OAuth2 API (sets visibility, playlist, license, audience)
- Post-upload checklist for YouTube Studio settings (AI content disclosure, comment moderation, remixing)

**Requires:** Python, YouTube OAuth2 credentials (see `plugins/griot-grits/skills/video-interview.upload/references/setup_guide.md`)

---

### `video-interview.create-social-media-post`

Transforms interview metadata into a ready-to-post social media package: a culturally resonant Instagram caption, a Facebook caption, and a branded 1080×1080 thumbnail image. Captions are individual-first — written so the subject's family and community will want to share them.

**Triggers when:** the user wants to share an interview on social media, create an Instagram or Facebook post, or says things like "create a social media post", "make an Instagram post", "generate a Facebook post", "promote this on Instagram".

**What it produces:**
- `_instagram.txt` — short, punchy caption with the interviewee's name up front, specific story details, an explicit share invitation, a watch CTA, and a `$20/month` donate ask linking to `give.griotandgrits.org`
- `_facebook.txt` — expanded version with the YouTube link embedded and fuller story context
- `_social.jpg` — 1080×1080 branded image downloaded from the YouTube thumbnail with G&G gold wordmark, interviewee name, and subtitle overlaid

**Requires:** Python, Pillow (`pip install Pillow`), YouTube video ID or local video file

---

### `example-skill`

A template for creating new Griot and Grits skills. Demonstrates the required `SKILL.md` frontmatter format and content structure.

---

## Typical workflow

```
video-interview.create-metadata
        ↓
video-interview.upload
        ↓
video-interview.create-social-media-post
```

Run them in order after recording an interview. Each skill picks up where the previous one left off.

## Adding a New Skill

1. Create a directory under `plugins/griot-grits/skills/<skill-name>/`
2. Add a `SKILL.md` file with the required frontmatter:

```markdown
---
name: skill-name
description: Use when the user asks to... [trigger conditions]
---

# Skill content here
```

3. Commit and push — the skill is immediately available to anyone who has the plugin installed.

## Structure

```
skills-registry/
├── .claude-plugin/
│   └── marketplace.json                    ← marketplace endpoint
├── docs/                                   ← design specs and plans
├── plugins/
│   └── griot-grits/
│       ├── .claude-plugin/
│       │   └── plugin.json                 ← plugin metadata
│       └── skills/
│           ├── example-skill/
│           ├── video-interview.create-metadata/
│           │   ├── SKILL.md
│           │   ├── scripts/
│           │   │   └── transcribe.py
│           │   └── references/
│           │       ├── filters.yaml
│           │       ├── videos.yaml
│           │       └── env.template
│           ├── video-interview.upload/
│           │   ├── SKILL.md
│           │   ├── scripts/
│           │   │   └── upload_to_youtube.py
│           │   └── references/
│           │       ├── setup_guide.md
│           │       └── env.template
│           └── video-interview.create-social-media-post/
│               ├── SKILL.md
│               ├── scripts/
│               │   └── create_social_image.py
│               ├── references/
│               │   └── brand_guide.md
│               └── evals/
│                   └── evals.json
└── README.md
```
