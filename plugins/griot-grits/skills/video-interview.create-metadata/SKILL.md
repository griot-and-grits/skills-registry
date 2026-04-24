---
name: video-interview.create-metadata
description: Use this skill to generate publication-ready metadata for a Griot and Grits video interview across all three platforms: the Griot and Grits website, YouTube, and Spreaker podcast. Triggers when the user wants to prepare or generate metadata for a new interview video, process an interview before publishing, create tags or descriptions from a transcript, or says things like "generate metadata for this video", "process this interview", "prepare this for publishing", "I have a new interview ready", or "what tags should I use". Always use this skill for any Griot and Grits content preparation workflow — run this before the upload skill.
---

# Video Interview — Create Metadata

Analyzes a Griot and Grits interview transcript to produce a complete metadata file for all three publishing platforms: the Griot and Grits website, YouTube, and Spreaker. The output is a single timestamped Markdown file in an `output/` folder, organized into four sections: master metadata, then one section per platform.

## What you'll need

- A `.mp4` or `.mkv` video file, OR a `.txt` transcript with the same base name
- Python with Whisper + ffmpeg installed (only needed if transcribing — see below)

---

## Step 0 — Resolve the working directory

Check for a `.env` file in both the current directory and any path the user passed. If found, load it. A template lives at `references/env.template`.

Resolve these three paths using the priority order below:

**Video directory** (where `.mp4` / `.mkv` files live):
1. Explicit file/folder path in the skill call
2. `GNG_VIDEO_INPUT_DIR` from `.env` or shell environment
3. Current working directory

**Transcript directory** (where `.txt` transcript files live):
1. `GNG_TRANSCRIPT_DIR` from `.env` or shell environment
2. Same as the video directory

**Output directory** (where the metadata `.md` file is saved):
1. `GNG_OUTPUT_DIR` from `.env` or shell environment
2. `<video_dir>/output/`

**Working directory** (for the `.metadata.json` the upload skill reads):
- Same as the video directory

Tell the user which input and output directories are being used before proceeding.

---

## Step 1 — Fetch reference files

Fetch both files from GitHub:

**filters.yaml** — tag and people name authority:
```
https://raw.githubusercontent.com/griot-and-grits/gng-web/refs/heads/main/metadata/filters.yaml
```
If the fetch fails, fall back to `references/filters.yaml`.

**videos.yaml** — authoritative format example for the website YAML output:
```
https://raw.githubusercontent.com/griot-and-grits/gng-web/refs/heads/main/metadata/videos.yaml
```
If the fetch fails, fall back to `references/videos.yaml`. Use this file as the structural reference when generating the website section in Step 6 — match its field names, ordering, and types exactly.

---

## Step 2 — Locate the video and transcript

Look in the transcript directory (resolved in Step 0) for a transcript file with the same base name as the video. Supported formats, checked in order:

- `.txt` — plain text, use directly
- `.doc` — legacy Word format; extract with `antiword "<file>"` (install: `sudo dnf install antiword` or `sudo apt install antiword`)
- `.docx` — modern Word format; extract with `python -c "import docx; print('\n'.join(p.text for p in docx.Document('<file>').paragraphs))"` (install: `pip install python-docx`)

If the user mentioned a specific filename, use that. If multiple video files exist, ask which one.

- **Transcript found:** extract its text and use it — skip Step 3.
- **No transcript:** proceed to Step 3.

---

## Step 3 — Transcribe (if needed)

Run the transcription script:

```bash
python scripts/transcribe.py "<video_file_path>"
```

This extracts audio with ffmpeg and runs Whisper locally, saving the transcript to `<video_basename>.txt` in the same directory. Warn the user it may take a few minutes.

If the script fails because Whisper or ffmpeg is missing:
```
pip install openai-whisper
# ffmpeg: https://ffmpeg.org/download.html (or: brew install ffmpeg / apt install ffmpeg)
```

---

## Step 4 — Get video duration

Run ffprobe to get the duration of the video file:

```bash
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "<video_file_path>"
```

Convert the seconds output to `M:SS` or `MM:SS` format (e.g., `8:12`, `12:56`) to match the videos.yaml convention. If ffprobe is not installed or the command fails, leave the duration field blank — do not estimate from transcript timestamps. The user will fill it in manually.

---

## Step 5 — Generate master metadata

Read the transcript carefully and extract or derive all of the following. This is the single source of truth — the platform sections in the output file are all derived from these fields.

**Title**
Generate three components from the transcript — a **core subtitle**, a **contextual verb**, and a **chapter number** — which all three platform titles are assembled from.

*Core subtitle:* Read the transcript and generate a short, specific phrase capturing the main subject (e.g., `"Growing Up with Faith, Family, and Southern Traditions"`, `"Roots, Work, and Quiet Strength"`). The website title uses this directly.

*Chapter number:* Infer from the video filename (e.g., `chpt 1` → `One`, `chpt 2` → `Two`). Convert the numeral to its ordinal word form. If the chapter cannot be determined from the filename, ask the user before proceeding.

The website title is assembled from these components in Step 6. The YouTube and Spreaker titles are generated independently — see Step 6.

**Interviewees**
A list of everyone being interviewed (not the interviewer). Use the names as they identify themselves in the transcript. If a name can be matched to the `people` section of filters.yaml, use the exact name from the file.

**Description**
Read the transcript file and apply this prompt to generate the description: "Based on this interview transcription, create a concise 1-paragraph synopsis (2-4 sentences) that captures the main themes and subject matter of this interview." Always derive this from the transcript — do not summarize from other metadata fields.

**Duration**
Use the value from Step 4.

**Historical Context**
Read the transcript and apply this prompt to extract historical context as a structured YAML list:

> From the interview transcript, extract all historical context as a structured list. Each entry must follow this exact format:
> ```
> - year: <four-digit year or null if not explicitly stated>
>   location:
>     name: <place name as stated or clearly implied in the transcript>
>     coordinates: [<latitude or null>, <longitude or null>]
> ```
>
> Rules:
> - Only include years explicitly mentioned or directly inferable from the transcript.
> - If year is null, exclude the field from the entry entirely.
> - Locations must be real places referenced in the transcript.
> - Use a geocoding service or lookup to get accurate latitude and longitude for each location name. Do not guess coordinates.
> - If coordinates cannot be determined, set them to null.
> - Do not add information not supported by the transcript.
> - List entries in chronological order. If only a decade is known, use the first year of that decade (e.g., 1940s → 1940). If no year can be determined, omit the year field and include only the location.
> - Keep the final output valid YAML.

**Tags**
Generate two tag lists from the transcript — one canonical, one SEO-expanded.

*Canonical tags (for the website):* Search filters.yaml and select every tag that genuinely fits the interview content. Copy each name character-for-character from the `name` field — no paraphrasing. Cast a wide net here: if a tag is relevant, include it. Beyond the matched tags, think about what's in the transcript that filters.yaml doesn't cover. If there are strong, recurring themes or subjects that deserve a canonical tag, recommend them as new additions — these should be added to both `filters.yaml` and `videos.yaml`. Present new suggestions separately from the confirmed list so the user can decide.

*SEO tags (for YouTube and Spreaker):* Go beyond the filters.yaml list to generate search-optimized terms drawn from the transcript. Think about how someone on YouTube or a podcast app would actually search for this content — include specific names, events, places, historical terms, and thematic phrases they might type. Mix broad terms (high search volume) with specific ones (lower competition, higher intent). Include variations and related phrases. Aim for 15–25 tags for YouTube; these will be trimmed to single-word form for Spreaker.

**People**
Select people from the `people` section of filters.yaml who are actually featured or interviewed in the video. Copy names exactly as written in the file. Do not include people who are merely mentioned in passing.

---

Once all fields are drafted, present the full master metadata to the user and ask for confirmation or changes before proceeding. This is the right moment for the user to correct names, add context they know that isn't in the transcript, or adjust anything that doesn't look right.

---

## Step 6 — Derive platform sections

From the confirmed master metadata, produce the three platform-specific sections. These don't require further user confirmation unless something looks off.

**Griot and Grits Website**
Output a single YAML entry matching the structure in `references/videos.yaml` (or the freshly fetched copy). Use the master metadata to populate each field. Fields that are not yet known at metadata-generation time should be left as empty strings or null — they will be filled in after upload:

- `id` — YouTube video ID (not yet known — leave as `""`)
- `thumbnail` — leave as `""`
- `videoUrl` — leave as `""`
- `podcastUrl` — omit the field entirely until a Spreaker URL exists
- `featured` — default to `false`
- `createdDate` — use the current date/time in ISO 8601 format (e.g., `"2026-04-23T19:54:28Z"`)
- `duration` — use the value from Step 4; if blank, leave as `""`

All other fields (title, interviewees, description, historicalContext, tags, people) come directly from the master metadata. The `title` field uses the website format: `"{Name} — Chapter {Number}: {Core Subtitle}"` — e.g., `"Irene Clark — Chapter Two: Confronting the Stereotypes of Africa"`. The historicalContext list must use the exact YAML structure from the format reference — `year` (omitted if unknown), `location.name`, and `location.coordinates`.

**YouTube**
- **Title:** Generate the most compelling version of the title body independently from the website title — don't just reformat the website title. The body can take whatever structure sounds best, such as:
  - `{Name} {Verb} {Core Subtitle}` — e.g., `"David E. Reid Reflects on Growing Up with Faith, Family, and Southern Traditions"`
  - `{Core Subtitle} with {Name}` — e.g., `"Roots, Work, and Quiet Strength with Rickey Thomas"`
  - Or any other natural phrasing that fits the content
  Prefix with `"Griot and Grits - "`. The body must be identical to the Spreaker title body.
- **Description:** Use the master description directly, followed by this license footer:
  ```
  License: This video is licensed under Creative Commons Attribution–NonCommercial–NoDerivatives 4.0 (CC BY‑NC‑ND 4.0).
  Learn more: https://creativecommons.org/licenses/by-nc-nd/4.0/
  Permissions: If you would like to request permission for uses not allowed under this license (including commercial use, edits, remixes, or redistribution), please contact Griot and Grits at info@griotandgrits.org
  ```
- **Tags:** Use the SEO tags generated in Step 5. Multi-word phrases are fine and preferred — YouTube matches tags against search queries, so specific phrases like `"Black history oral history"`, `"slave castles Ghana"`, or `"African American genealogy"` outperform single generic words. Include the interviewee's name, channel name (`Griot and Grits`), and any well-known proper nouns from the interview.

**Spreaker**
- **Title:** `"Quick Bites - "` + the same title body generated for YouTube. The two titles are always identical except for the prefix.
- **Description:** Use the master description directly, followed by this license footer:
  ```
  License: This video is licensed under Creative Commons Attribution–NonCommercial–NoDerivatives 4.0 (CC BY‑NC‑ND 4.0).
  Learn more: https://creativecommons.org/licenses/by-nc-nd/4.0/
  Permissions: If you would like to request permission for uses not allowed under this license (including commercial use, edits, remixes, or redistribution), please contact Griot and Grits at info@griotandgrits.org
  ```
- **Tags:** Single-word only, derived from the SEO tag list. Take the most search-meaningful single word from each phrase (e.g., `"Black history oral history"` → `History`, `"slave castles Ghana"` → `Ghana`). Prioritize words that people actually use when searching for podcasts on this topic. Aim for 10–15 distinct single-word tags.

---

## Step 7 — Save the output file

Create the output directory if it doesn't exist (resolved in Step 0). Save the file as:

```
<output_dir>/<video_basename>_<YYYYMMDD-HHMMSS>.md
```

Use the current date and time for the timestamp (e.g., `clark_interview_20260423-143022.md`).

The file should follow this structure exactly:

```markdown
# [Master Title]
Generated: YYYY-MM-DD HH:MM:SS
Video: <video_filename>

---

## Metadata

**Title:** ...
**Interviewees:** ...
**Description:**

...

**Duration:** HH:MM:SS
**Historical Context:**
- [Place name] — [Lat, Lon] — [Years/Era]
- ...
**Tags:** tag1, tag2, ...
**People:** name1, name2, ...

---

## Griot and Grits Website

```yaml
- id: ""
  thumbnail: ""
  title: ...
  interviewees:
    - ...
  description: ...
  duration: "MM:SS"
  createdDate: "YYYY-MM-DDTHH:MM:SSZ"
  videoUrl: ""
  featured: false
  historicalContext:
    - year: YYYY
      location:
        name: ...
        coordinates: [lat, lon]
  tags:
    - ...
  people:
    - ...
```

---

## YouTube

**Title:** Griot and Grits - ...
**Description:**

...

**Tags:** tag1, tag2, ...

---

## Spreaker

**Title:** ...
**Description:**

...

**Tags:** word1, word2, ...

---
```

Confirm the saved file path to the user.

---

## Wrap-up

Tell the user the output file path and that they can now run the **video-interview.upload** skill to publish to YouTube.

If new tag suggestions were identified during Step 5, ask whether the user wants to add them to filters.yaml now or later.

Also save a `<video_basename>.metadata.json` file in the working directory containing just the YouTube fields — the upload skill uses this to avoid re-parsing the markdown:

```json
{
  "video_file": "<absolute_path_to_video>",
  "title": "<youtube_title>",
  "description": "<youtube_description>",
  "tags": ["tag1", "tag2"],
  "new_tag_suggestions": []
}
```
