# Video Interview Upload — Griot and Grits
## Processing: `irene_clark_cadavers.mp4`

---

## Step 1 — Locate the video and transcript

- Video file: `irene_clark_cadavers.mp4` ✓
- Transcript file: `irene_clark_cadavers.txt` ✓ (pre-existing — skipping transcription)

---

## Step 2 — Transcription

Skipped — transcript already exists at `irene_clark_cadavers.txt`.

---

## Step 3 — Proposed Tags

The filters list was fetched from:
`https://raw.githubusercontent.com/griot-and-grits/gng-web/refs/heads/main/metadata/filters.yaml`

Based on a careful reading of the transcript, the following tags are proposed:

**Themes / Topics:**
- Medical History
- Medical Ethics
- Racial Injustice
- Criminal Justice
- Body Donation
- Systemic Racism
- Institutional Racism
- Research & Documentation

**Time Period:**
- Early 20th Century
- Mid-20th Century
- 1900s
- Jim Crow Era

**People (featured/interviewed):**
- Irene Clark

**Suggested new tags** (not in filters.yaml — please review before adding):
- `Black Prisoner Cadavers` — this is the precise subject of the interview and a critical research term. If this or a close equivalent is not already in filters.yaml, it is worth adding.
- `Non-Consensual Body Donation` — captures the specific injustice described; useful for researchers.

> Please confirm these tags before proceeding. Remove any that don't fit, and let me know whether to add the suggested new ones to `filters.yaml`.

---

## Step 4 — Proposed YouTube Metadata

### Title

```
Griot and Grits - Mrs. Clark on Black Prisoner Bodies and Medical Schools
```

### Description

```
In this interview, Irene Clark — a researcher with fifteen years of investigation into medical school practices — describes a systematic and largely unknown injustice: throughout the early 1900s and well into mid-century, the bodies of Black prisoners who died in custody were routinely donated to medical schools across the United States for use in anatomy labs, without the knowledge or consent of their families. This practice occurred in at least a dozen states and was not only widespread but fully legal at the time. The families were never informed, and the bodies were never returned. Clark explains that the documentary record is recoverable — the records exist — and that this history demands acknowledgment. This is an essential account for anyone researching the intersection of race, incarceration, and the history of American medicine.
```

### Tags (YouTube)

```
Medical History, Medical Ethics, Racial Injustice, Criminal Justice, Body Donation, Systemic Racism, Institutional Racism, Research & Documentation, Early 20th Century, Mid-20th Century, 1900s, Jim Crow Era, Irene Clark
```

> Please review the title, description, and tags above. Reply with approval or any changes and I will proceed to upload.

---

## Step 5 — Upload Command

Once you approve the metadata, run the following from your video-processing folder:

```bash
python scripts/upload_to_youtube.py \
  --video "irene_clark_cadavers.mp4" \
  --title "Griot and Grits - Mrs. Clark on Black Prisoner Bodies and Medical Schools" \
  --description "In this interview, Irene Clark — a researcher with fifteen years of investigation into medical school practices — describes a systematic and largely unknown injustice: throughout the early 1900s and well into mid-century, the bodies of Black prisoners who died in custody were routinely donated to medical schools across the United States for use in anatomy labs, without the knowledge or consent of their families. This practice occurred in at least a dozen states and was not only widespread but fully legal at the time. The families were never informed, and the bodies were never returned. Clark explains that the documentary record is recoverable — the records exist — and that this history demands acknowledgment. This is an essential account for anyone researching the intersection of race, incarceration, and the history of American medicine." \
  --tags "Medical History,Medical Ethics,Racial Injustice,Criminal Justice,Body Donation,Systemic Racism,Institutional Racism,Research & Documentation,Early 20th Century,Mid-20th Century,1900s,Jim Crow Era,Irene Clark" \
  --credentials ".youtube_credentials/client_secrets.json"
```

The script will:
- Open a browser for OAuth2 on first run (or reuse cached token)
- Upload the video as **Public**, **not made for kids**, with **Standard YouTube License**
- Add it to the playlist: **"Griot and Grits - Black Voices Worth Remembering, Black History Worth Sharing"**

When the upload completes, the script will print the YouTube video URL.

---

## Step 6 — Manual Settings in YouTube Studio

After the upload completes, open the video in YouTube Studio → **Details** tab → **Show more** and complete the following:

- [ ] **Altered Content** → Check "My video contains altered or synthetic content (like AI-generated content)"
- [ ] **Remixing** → Ensure this is **OFF** (unchecked — do not allow others to remix)
- [ ] **Comments** → Set to **Hold all comments for review** (strict moderation)
- [ ] **Like count** → Check "Show how many viewers like this video"

Under **Video chapters**:
- [ ] Allow automatic chapters (should be on by default)

Under **Featured places** and **Automatic concepts**:
- [ ] Confirm both are enabled (YouTube enables these by default)

> Complete these settings before the video goes live — even though visibility is already set to Public, these settings matter for presentation and policy compliance.

---

## Wrap-up

Once the upload is complete and manual settings are confirmed, here is what will have been accomplished:

- **Video uploaded:** [YouTube URL — printed by upload script]
- **Tags applied:** Medical History, Medical Ethics, Racial Injustice, Criminal Justice, Body Donation, Systemic Racism, Institutional Racism, Research & Documentation, Early 20th Century, Mid-20th Century, 1900s, Jim Crow Era, Irene Clark
- **New tags suggested for filters.yaml:** `Black Prisoner Cadavers`, `Non-Consensual Body Donation`

Would you like to add either of the suggested new tags to `filters.yaml` now?
