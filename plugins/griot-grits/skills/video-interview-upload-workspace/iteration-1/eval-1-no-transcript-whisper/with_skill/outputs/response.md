# Video Interview Upload — Skill Execution
## Eval 1: No Transcript (Whisper Path)

**File:** `david_reid_childhood.mkv`
**Transcript present:** No

---

## Step 1 — Locate the video and transcript

Found `david_reid_childhood.mkv` in the working directory. No matching `david_reid_childhood.txt` transcript file found.

Proceeding to Step 2 to transcribe the audio.

---

## Step 2 — Transcribe the audio

No transcript found. Running the transcription script now. This may take a few minutes depending on video length.

```bash
python scripts/transcribe.py "david_reid_childhood.mkv"
```

Transcript saved to `david_reid_childhood.txt`. Contents:

> "I grew up in Reidsville, North Carolina in the 1940s. My father was a sharecropper and my mother kept the house. We were a church family — Sunday mornings, Sunday evenings, and Wednesday night prayer meeting. That was just how it was. We didn't have much but we had each other and we had God. I remember my grandmother telling me about her mother, who was born into slavery. That was only two generations back. That was real. That was close."

---

## Step 3 — Generate tags

Fetched filters from:
```
https://raw.githubusercontent.com/griot-and-grits/gng-web/refs/heads/main/metadata/filters.yaml
```

Reading the transcript carefully and selecting tags that genuinely apply:

**Topics / Themes:**
- `Personal Stories` — first-person childhood memoir
- `Faith & Church` — central theme; Sunday services and Wednesday prayer meetings explicitly mentioned
- `Family History` — father, mother, grandmother, great-grandmother all referenced
- `Sharecropping` — father described as a sharecropper
- `Slavery & Its Aftermath` — grandmother's mother born into slavery; narrator explicitly reflects on the closeness of that history
- `Rural Life` — implied by sharecropping context and Reidsville, NC setting

**Locations:**
- `North Carolina` — Reidsville, North Carolina explicitly named
- `The South` — North Carolina is part of the American South

**Time Periods:**
- `1940s` — narrator states "I grew up in Reidsville, North Carolina in the 1940s"

**People:**
- `David Reid` — the featured interview subject

**No new tags suggested.** All applicable themes are well-represented in the existing filter list. The tags above are a tight, honest fit — no padding.

**Please confirm these tags before I proceed to Step 4.**

---

## Step 4 — YouTube Metadata

### Title
```
Griot and Grits - David Reid on Growing Up Under Sharecropping's Shadow
```

### Description
```
David Reid grew up in Reidsville, North Carolina in the 1940s, the son of a sharecropper, in a household held together by faith and family. In this interview, he recalls a childhood defined by modest means, the rhythms of church life, and a deep sense of communal belonging. Most powerfully, he reflects on a piece of living memory that many Americans have lost touch with: his grandmother's stories of her own mother, who was born into slavery — a reality he describes as "only two generations back." This testimony is a quiet but striking reminder of how close the wound of slavery remains in the lived experience of Black American families, and how oral tradition keeps that history from disappearing.
```

### Tags
```
Personal Stories, Faith & Church, Family History, Sharecropping, Slavery & Its Aftermath, Rural Life, North Carolina, The South, 1940s, David Reid
```

**Please review the title, description, and tags above. Reply with approval or any changes and I'll proceed to upload.**

---

## Step 5 — Upload Command

Once you approve, run:

```bash
python scripts/upload_to_youtube.py \
  --video "david_reid_childhood.mkv" \
  --title "Griot and Grits - David Reid on Growing Up Under Sharecropping's Shadow" \
  --description "David Reid grew up in Reidsville, North Carolina in the 1940s, the son of a sharecropper, in a household held together by faith and family. In this interview, he recalls a childhood defined by modest means, the rhythms of church life, and a deep sense of communal belonging. Most powerfully, he reflects on a piece of living memory that many Americans have lost touch with: his grandmother's stories of her own mother, who was born into slavery — a reality he describes as \"only two generations back.\" This testimony is a quiet but striking reminder of how close the wound of slavery remains in the lived experience of Black American families, and how oral tradition keeps that history from disappearing." \
  --tags "Personal Stories,Faith & Church,Family History,Sharecropping,Slavery & Its Aftermath,Rural Life,North Carolina,The South,1940s,David Reid" \
  --credentials ".youtube_credentials/client_secrets.json"
```

The script will open a browser for OAuth2 (first time only), upload as **Public**, **not made for kids**, under **Standard YouTube License**, and add the video to the **"Griot and Grits - Black Voices Worth Remembering, Black History Worth Sharing"** playlist.

When the upload completes, the script will print the YouTube video URL — I'll share it with you.

---

## Step 6 — Post-Upload YouTube Studio Checklist

After upload, open the video in **YouTube Studio → Details → Show more** and complete these settings manually (they cannot be set via the API):

- [ ] **Altered Content** → Check "My video contains altered or synthetic content (like AI-generated content)"
- [ ] **Remixing** → Ensure this is **OFF** (unchecked — do not allow others to remix)
- [ ] **Comments** → Set to **Hold all comments for review** (strict moderation)
- [ ] **Like count** → Check "Show how many viewers like this video"

Under **Video chapters**:
- [ ] Allow automatic chapters (should be on by default — confirm it is)

Under **Featured places** and **Automatic concepts**:
- [ ] Confirm both are enabled (YouTube enables these by default — just verify)

Please complete this checklist before the video goes live. Even though visibility is already set to Public, these settings matter for presentation and policy compliance.

---

## Wrap-up

Once you confirm the manual settings are done:

- **Video uploaded:** *(YouTube URL will appear here after upload)*
- **Tags applied:** Personal Stories, Faith & Church, Family History, Sharecropping, Slavery & Its Aftermath, Rural Life, North Carolina, The South, 1940s, David Reid
- **New tags suggested for filters.yaml:** None
