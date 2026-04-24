---
name: video-interview.upload
description: Use this skill to upload a Griot and Grits interview video to YouTube. Triggers when the user is ready to upload a video, has a metadata.json ready, wants to publish an interview to the channel, or says things like "upload this video", "publish to YouTube", "upload to the channel", "the metadata is ready, let's upload". Use this skill after running video-interview.create-metadata. Also triggers if the user just wants to upload and already has the title, description, and tags ready.
---

# Video Interview — Upload to YouTube

Uploads a prepared Griot and Grits interview to YouTube using a `metadata.json` file (produced by the **video-interview.create-metadata** skill), then guides you through the post-upload settings in YouTube Studio.

## What you'll need

- A `<video_basename>.metadata.json` file in the video directory (run **video-interview.create-metadata** first if you don't have one)
- YouTube OAuth2 credentials (see `references/setup_guide.md` for first-time setup)
- Python with required packages installed

---

## Step 0 — Resolve working directory and credentials

Check for a `.env` file in the current directory or any path the user passed. If found, load it — it may define `GNG_VIDEO_INPUT_DIR` and `GNG_YOUTUBE_CREDENTIALS`. A template lives at `references/env.template`.

Resolve the video folder:
1. Explicit path in the skill call
2. `GNG_VIDEO_INPUT_DIR` from `.env` or shell environment
3. Current working directory

Resolve the credentials path:
- Use `GNG_YOUTUBE_CREDENTIALS` if set
- Otherwise default to `<video_dir>/.youtube_credentials/client_secrets.json`

Tell the user which directory and credentials path are being used.

---

## Step 1 — Load metadata

Look for `<video_basename>.metadata.json` in the working directory. The base name comes from the video file (`interview.mp4` → `interview.metadata.json`).

If the user passed a specific video file path, look for that file's matching `.metadata.json`.

**If the metadata file is missing:** tell the user to run **video-interview.create-metadata** first to generate it. Alternatively, if the user already has a title, description, and tag list handy, ask if they'd like to provide them directly and skip the file.

Once loaded, show the user the title, description, and tags and ask for final confirmation before uploading. This is the last chance to make changes.

---

## Step 2 — Upload to YouTube

Check whether the resolved credentials path from Step 0 exists.

---

### Option A — Credentials present (API upload)

Run the upload script:

```bash
python scripts/upload_to_youtube.py \
  --video "<video_file_path>" \
  --title "<approved_title>" \
  --description "<approved_description>" \
  --tags "<comma_separated_tags>" \
  --credentials "<resolved_credentials_path>"
```

The script opens a browser for OAuth2 on first run (or reuses the cached token), uploads as **Public**, **not made for kids**, **Standard YouTube License**, and adds the video to the **"Griot and Grits - Black Voices Worth Remembering, Black History Worth Sharing"** playlist. When complete it prints the YouTube video URL — share it with the user, then proceed to Step 3.

---

### Option B — No credentials (manual upload guide)

Tell the user credentials aren't set up yet (point them to `references/setup_guide.md` for the one-time setup), then walk them through uploading manually. Present the metadata in clearly labelled copy-paste blocks:

---

**Go to:** https://studio.youtube.com → **Create** → **Upload videos** → select `<video_filename>`

While the file uploads, fill in the details:

**Title** (copy exactly):
```
<approved_title>
```

**Description** (copy exactly):
```
<approved_description>
```

**Tags** — in the Tags field, add each of these:
```
<tag_1>
<tag_2>
...
```

**Audience:** Select **"No, it's not made for kids"**

Click **More options**:
- **License:** Standard YouTube License
- **Category:** People & Blogs (or leave as-is)

Click **Next** through Checks, then on the **Visibility** screen:
- Set to **Public**
- Add to playlist: **"Griot and Grits - Black Voices Worth Remembering, Black History Worth Sharing"**

Click **Save**. Copy the video URL from the confirmation screen and share it here.

---

## Step 3 — Final settings in YouTube Studio

After the upload completes, open the video in YouTube Studio → **Details** tab → **Show more** and complete these settings (they can't be set during upload):

- [ ] **Altered Content** → Check "My video contains altered or synthetic content (like AI-generated content)"
- [ ] **Remixing** → Ensure this is **OFF** (unchecked — do not allow others to remix)
- [ ] **Comments** → Set to **Hold all comments for review** (strict moderation)
- [ ] **Like count** → Check "Show how many viewers like this video"

Under **Video chapters**:
- [ ] Allow automatic chapters (should be on by default — confirm it is)

Under **Featured places** and **Automatic concepts**:
- [ ] Confirm both are enabled (YouTube enables these by default)

Show the user this checklist and remind them to complete it before the video goes live.

---

## Wrap-up

Once the user confirms the manual settings are done, summarize:

- Video uploaded: [YouTube URL]
- Tags applied: [list]

If the metadata.json contained `new_tag_suggestions`, ask whether the user wants to add them to filters.yaml now or later.
