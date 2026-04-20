---
name: video-interview-upload
description: Use this skill when processing a new Griot and Grits video interview for publication. Triggers when the user mentions uploading an interview, processing a new video, has a .mp4 or .mkv file to publish, wants to upload to YouTube for Griot and Grits, needs to generate tags or a YouTube description from an interview, or says things like "I have a new interview", "process this video", "upload to the channel", "new episode ready". Always use this skill for any Griot and Grits video publishing workflow.
---

# Video Interview Upload — Griot and Grits

Processes a new video interview from raw file to published YouTube video, including transcription, tag generation, and upload.

## What you'll need

- A `.mp4` or `.mkv` video file (or a `.txt` transcript if you already have one)
- YouTube OAuth2 credentials (see `references/setup_guide.md` if this is your first time)
- Python with required packages installed (see setup guide)

The working directory should be your video-processing folder.

---

## Step 1 — Locate the video and transcript

Look in the current directory for:
- A `.mp4` or `.mkv` file — this is the video to upload
- A `.txt` file with the same base name as the video (e.g., `interview.mp4` → `interview.txt`) — this is a pre-existing transcript

If the user mentions a specific filename, use that. If multiple video files exist, ask which one.

**If a `.txt` transcript file exists:** use it directly — skip Step 2.

**If no transcript exists:** proceed to Step 2.

---

## Step 2 — Transcribe the audio (if needed)

Run the transcription script:

```bash
python scripts/transcribe.py "<video_file_path>"
```

This extracts audio with ffmpeg and runs Whisper locally. It saves the transcript to `<video_basename>.txt` in the same directory. Tell the user it may take a few minutes depending on video length.

If the script fails because whisper or ffmpeg isn't installed, show the user this:
```
pip install openai-whisper
# ffmpeg: https://ffmpeg.org/download.html (or: brew install ffmpeg / apt install ffmpeg)
```

---

## Step 3 — Generate tags

Fetch the current filter list:
```
https://raw.githubusercontent.com/griot-and-grits/gng-web/refs/heads/main/metadata/filters.yaml
```

Read the transcript carefully. Select tags from the fetched list that genuinely apply — think about themes, locations, people, historical periods, and topics that a researcher or viewer might use to find this video.

**Rules:**
- Only include tags that clearly fit — don't pad the list
- For the `people` section: include a person only if they are actually featured/interviewed in the video
- New tags: only suggest additions if a tag is so obviously essential that its absence from the list is a clear gap. Set a high bar — if in doubt, don't add it. If you do suggest a new tag, mark it clearly so the user can decide whether to add it to filters.yaml

Present the selected tags to the user and confirm before proceeding.

---

## Step 4 — Generate YouTube metadata

Based on the transcript, generate:

**Title:** Always starts with `"Griot and Grits - "`. Keep it short and compelling — 6 to 10 words after the prefix. Name the person if they're a featured subject. Reference the most striking or specific topic from the interview, not a generic summary.

Good: `Griot and Grits - Mrs. Clark Talks Black Prisoner Cadavers`
Too generic: `Griot and Grits - Interview About Medical History`

**Description:** One paragraph (4–6 sentences). Summarize who is speaking, what they discuss, why it matters, and what time period or location it covers. Write for someone discovering this video cold — give them enough to know if this story is relevant to their research or interests. Don't use bullet points.

**Tags:** Use the confirmed tags from Step 3 as the YouTube tags list.

Show the user the title, description, and tags together and ask for approval or changes before uploading.

---

## Step 5 — Upload to YouTube

Once the user approves the metadata, run the upload script:

```bash
python scripts/upload_to_youtube.py \
  --video "<video_file_path>" \
  --title "<approved_title>" \
  --description "<approved_description>" \
  --tags "<comma_separated_tags>" \
  --credentials ".youtube_credentials/client_secrets.json"
```

The script will:
- Open a browser for OAuth2 the first time (or reuse cached token)
- Upload the video as **Public**, **not made for kids**, with **Standard YouTube License**
- Add it to the **"Griot and Grits - Black Voices Worth Remembering, Black History Worth Sharing"** playlist

When the upload completes, the script prints the YouTube video URL. Share it with the user.

---

## Step 6 — Manual settings in YouTube Studio

After upload, the user must configure these settings manually in YouTube Studio — they cannot be set via the API:

Open the video in YouTube Studio → **Details** tab, then **Show more**:

- [ ] **Altered Content** → Check "My video contains altered or synthetic content (like AI-generated content)"
- [ ] **Remixing** → Ensure this is **OFF** (unchecked — do not allow others to remix)
- [ ] **Comments** → Set to **Hold all comments for review** (strict moderation)
- [ ] **Like count** → Check "Show how many viewers like this video"

Under **Video chapters**:
- [ ] Allow automatic chapters (should be on by default)

Under **Featured places** and **Automatic concepts**:
- [ ] Confirm both are enabled (YouTube enables these by default)

Show the user this checklist and remind them to complete it before the video goes live (even though visibility is already set to Public, these settings matter for presentation and policy compliance).

---

## Wrap-up

Once the user confirms the manual settings are done, summarize what was completed:

- Video uploaded: [YouTube URL]
- Tags applied: [list]
- Any new tags suggested for filters.yaml: [list, or "none"]

If new tags were suggested, ask the user whether they want to add them to filters.yaml now or later.
