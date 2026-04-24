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

## Step 3 — Tags

Filters loaded from `filters.yaml`. Reading the transcript carefully and selecting only tags that genuinely apply:

**From tags list:**
- `Personal Stories` — first-person testimony by a researcher describing fifteen years of investigation
- `Historical Events` — covers systematic practices from the early 1900s through mid-century
- `Historical Exploitation` — bodies of Black prisoners taken without family knowledge or consent
- `Racial Injustice` — the practice was explicitly racial and systematic
- `Prison System` — the victims were Black prisoners who died in custody
- `Medical History` — anatomy labs and medical schools are the central subject
- `Medical Ethics` — the practice was legal but ethically indefensible; families were never notified

**From people list:**
- `Irene Clark` — the featured interview subject

**Suggested new tags** (not currently in filters.yaml):
- `Historical Exploitation` is already in the list and covers the subject well
- No additional new tags required — the existing list maps cleanly to this content

---

## Step 4 — YouTube Metadata

### Title

```
Griot and Grits - Irene Clark on Black Prisoners' Bodies and Medical Schools
```

### Description

```
In this interview, researcher Irene Clark shares fifteen years of investigation into a systematic and largely unknown injustice: from the early 1900s and well into mid-century, the bodies of Black prisoners who died in custody were routinely donated — without family consent — to medical schools across the United States for use in anatomy labs. Clark documents that this practice occurred in at least a dozen states, was fully legal at the time, and was explicitly racial in its application. The families were never informed, and the bodies were never returned. Her testimony is a call to confront a buried chapter at the intersection of race, incarceration, and the history of American medicine — and a reminder that the documentary record exists for those willing to look.
```

### Tags

```
Personal Stories, Historical Events, Historical Exploitation, Racial Injustice, Prison System, Medical History, Medical Ethics, Irene Clark
```

---

## Step 5 — Upload Command

```bash
python scripts/upload_to_youtube.py \
  --video "irene_clark_cadavers.mp4" \
  --title "Griot and Grits - Irene Clark on Black Prisoners' Bodies and Medical Schools" \
  --description "In this interview, researcher Irene Clark shares fifteen years of investigation into a systematic and largely unknown injustice: from the early 1900s and well into mid-century, the bodies of Black prisoners who died in custody were routinely donated — without family consent — to medical schools across the United States for use in anatomy labs. Clark documents that this practice occurred in at least a dozen states, was fully legal at the time, and was explicitly racial in its application. The families were never informed, and the bodies were never returned. Her testimony is a call to confront a buried chapter at the intersection of race, incarceration, and the history of American medicine — and a reminder that the documentary record exists for those willing to look." \
  --tags "Personal Stories,Historical Events,Historical Exploitation,Racial Injustice,Prison System,Medical History,Medical Ethics,Irene Clark" \
  --credentials ".youtube_credentials/client_secrets.json"
```

The script will:
- Open a browser for OAuth2 on first run (or reuse cached token)
- Upload the video as **Public**, **not made for kids**, with **Standard YouTube License**
- Add it to the playlist: **"Griot and Grits - Black Voices Worth Remembering, Black History Worth Sharing"**

When the upload completes, the script will print the YouTube video URL.

---

## Step 6 — Post-Upload YouTube Studio Checklist

After the upload completes, open the video in **YouTube Studio → Details → Show more** and complete the following manually:

- [ ] **Altered Content** → Check "My video contains altered or synthetic content (like AI-generated content)"
- [ ] **Remixing** → Ensure this is **OFF** (unchecked — do not allow others to remix)
- [ ] **Comments** → Set to **Hold all comments for review** (strict moderation)
- [ ] **Like count** → Check "Show how many viewers like this video"

Under **Video chapters**:
- [ ] Allow automatic chapters (should be on by default — confirm it is)

Under **Featured places** and **Automatic concepts**:
- [ ] Confirm both are enabled (YouTube enables these by default — just verify)

Complete this checklist before the video goes live. Even though visibility is already set to Public, these settings matter for presentation and policy compliance.

---

## Wrap-up

Once the upload is complete and manual settings are confirmed:

- **Video uploaded:** *(YouTube URL will appear here after upload)*
- **Tags applied:** Personal Stories, Historical Events, Historical Exploitation, Racial Injustice, Prison System, Medical History, Medical Ethics, Irene Clark
- **New tags suggested for filters.yaml:** None — existing tags cover the content well
