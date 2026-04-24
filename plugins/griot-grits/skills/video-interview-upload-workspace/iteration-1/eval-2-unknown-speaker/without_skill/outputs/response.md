# Processing: unknown_speaker.mp4 — Griot and Grits Upload Workflow

## Step 1 — Video File Located

- **Video file:** `unknown_speaker.mp4`
- **Transcript:** None found — proceeding to transcription.

---

## Step 2 — Transcribe the Audio

No transcript file (`unknown_speaker.txt`) was found alongside the video. Run the transcription script now:

```bash
python scripts/transcribe.py "unknown_speaker.mp4"
```

This will extract audio with ffmpeg and run Whisper locally, saving the transcript to `unknown_speaker.txt` in the same directory. Depending on the length of the video, this may take a few minutes.

If you hit missing-dependency errors:

```bash
pip install openai-whisper
# ffmpeg: https://ffmpeg.org/download.html  (or: brew install ffmpeg / apt install ffmpeg)
```

> **Note:** Because no transcript exists yet, the tags, title, and description below are drafted from the context you provided ("growing up in Brooklyn in the 1960s, working in the garment industry, neighborhood change after white flight"). Once the transcript is generated, review these drafts and adjust anything that doesn't match what the speaker actually says.

---

## Step 3 — Proposed Tags

> **Important:** Tags are normally selected from the live `filters.yaml` at  
> `https://raw.githubusercontent.com/griot-and-grits/gng-web/refs/heads/main/metadata/filters.yaml`  
> That file could not be fetched in this session. The tags below are proposed based on the interview content you described, using the tag categories and naming style from the skill documentation. Please cross-check against the current filters.yaml before uploading.

**Proposed tags (from existing filters, based on content):**

- Brooklyn
- New York City
- 1960s
- Personal Stories
- Work & Employment
- Racial Injustice
- Migration
- Community & Neighborhood
- Urban Life
- Black History

**Possible new tag to suggest (if not already in filters.yaml):**

- `Garment Industry` — the speaker's work in the garment industry is a specific and historically significant topic for Black labor history in New York. If this tag does not already exist, it is worth adding. **Flag for your review before adding to filters.yaml.**

**People tags:** The speaker is unidentified — do **not** add any entry to the `people` section.

> Please confirm or adjust this tag list before proceeding.

---

## Step 4 — YouTube Metadata

### Title

```
Griot and Grits - Brooklyn, the Garment Industry, and White Flight
```

### Description

```
In this Griot and Grits interview, an unidentified speaker recalls growing up in Brooklyn during the 1960s, offering a first-hand account of a neighborhood that was vibrant, working-class, and distinctly Black. They describe their years in the garment industry — a sector that employed large numbers of Black New Yorkers during that era — and reflect on the sweeping changes that reshaped their community in the wake of white flight. The interview captures the texture of daily life, labor, and loss that defined urban Black experience in mid-century New York. This oral history is an important record of a generation that witnessed the economic and demographic transformation of one of America's most iconic boroughs.
```

### Tags (comma-separated for upload script)

```
Brooklyn, New York City, 1960s, Personal Stories, Work & Employment, Racial Injustice, Migration, Community & Neighborhood, Urban Life, Black History, Garment Industry
```

> Please review the title, description, and tags above and confirm (or request changes) before the upload proceeds.

---

## Step 5 — Upload Command

Once you approve the metadata above, run:

```bash
python scripts/upload_to_youtube.py \
  --video "unknown_speaker.mp4" \
  --title "Griot and Grits - Brooklyn, the Garment Industry, and White Flight" \
  --description "In this Griot and Grits interview, an unidentified speaker recalls growing up in Brooklyn during the 1960s, offering a first-hand account of a neighborhood that was vibrant, working-class, and distinctly Black. They describe their years in the garment industry — a sector that employed large numbers of Black New Yorkers during that era — and reflect on the sweeping changes that reshaped their community in the wake of white flight. The interview captures the texture of daily life, labor, and loss that defined urban Black experience in mid-century New York. This oral history is an important record of a generation that witnessed the economic and demographic transformation of one of America's most iconic boroughs." \
  --tags "Brooklyn,New York City,1960s,Personal Stories,Work & Employment,Racial Injustice,Migration,Community & Neighborhood,Urban Life,Black History,Garment Industry" \
  --credentials ".youtube_credentials/client_secrets.json"
```

The script will:
- Open a browser for OAuth2 the first time (or reuse your cached token)
- Upload the video as **Public**, **not made for kids**, with **Standard YouTube License**
- Add it to the **"Griot and Grits - Black Voices Worth Remembering, Black History Worth Sharing"** playlist

When the upload finishes, the script will print the YouTube video URL — share that here.

---

## Step 6 — Manual Settings in YouTube Studio

After the upload, open the video in **YouTube Studio → Details tab → Show more** and complete the following:

- [ ] **Altered Content** — Check "My video contains altered or synthetic content (like AI-generated content)"
- [ ] **Remixing** — Ensure this is **OFF** (do not allow others to remix)
- [ ] **Comments** — Set to **Hold all comments for review** (strict moderation)
- [ ] **Like count** — Check "Show how many viewers like this video"

Under **Video chapters:**
- [ ] Confirm automatic chapters are enabled (on by default)

Under **Featured places** and **Automatic concepts:**
- [ ] Confirm both are enabled (YouTube enables these by default)

Complete this checklist before considering the video fully live, even though visibility is already set to Public.

---

## Wrap-up (to be completed after upload)

- **Video uploaded:** _(paste YouTube URL here once available)_
- **Tags applied:** Brooklyn, New York City, 1960s, Personal Stories, Work & Employment, Racial Injustice, Migration, Community & Neighborhood, Urban Life, Black History
- **New tag suggested for filters.yaml:** `Garment Industry` — confirm whether to add

**Regarding the new tag:** Do you want to add `Garment Industry` to `filters.yaml` now, or handle it later?
