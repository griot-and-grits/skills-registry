---
name: video-interview.create-social-media-post
description: Use this skill to generate branded social media content for a Griot and Grits interview video — including a captivating Instagram/Facebook caption and a branded thumbnail image. Triggers when the user wants to share an interview on social media, create an Instagram or Facebook post, generate social content from an interview, promote a video on social platforms, or says things like "create a social media post for this interview", "make an Instagram post", "generate a Facebook post", "create social content", "promote this on Instagram", "make a post for this video", or "I need to share this interview". Always use this skill after running video-interview.create-metadata — the metadata file is the primary input. Use this skill anytime the user wants to post, promote, or share a Griot and Grits interview on any social platform.
---

# Video Interview — Create Social Media Post

Transforms a Griot and Grits interview metadata file into a ready-to-post social media package: a culturally resonant caption (for Instagram, Facebook, or both) and a branded thumbnail image derived from the video. The output lands in the same `output/` folder as the metadata file.

## What you'll need

- A `<video_basename>_<timestamp>.md` metadata file (from **video-interview.create-metadata**)
- The original video file (for thumbnail extraction) — OR a YouTube thumbnail URL if already uploaded
- Python with Pillow and ffmpeg installed (for image creation — see below)

---

## Step 0 — Resolve working directory and locate metadata

Check for a `.env` file. Load `GNG_VIDEO_INPUT_DIR` and `GNG_OUTPUT_DIR` if present.

Resolve paths using the same priority order as the metadata skill:

1. Explicit path in the skill call
2. Environment variables
3. Current working directory

Look for the most recent `*.md` file in the output directory that follows the `<basename>_<YYYYMMDD-HHMMSS>.md` naming pattern. If multiple exist, ask the user which to use.

Tell the user which metadata file and video file are being used.

---

## Step 1 — Parse the metadata

Read the metadata `.md` file and extract:

- **Interviewees** — names of the people interviewed
- **Description** — the 2-4 sentence synopsis
- **Tags** — canonical tags (themes, places, historical events)
- **Historical context** — years and locations from the interview
- **YouTube title** — the full `Griot and Grits - ...` title
- **YouTube description** — for extracting the story richness
- **YouTube video URL / ID** — look for it in the `videoUrl` field in the YAML block (e.g., `https://www.youtube.com/watch?v=XXXXXXXXXXX`). Extract the video ID — you'll use it for thumbnail download in Step 3. If the user passed a YouTube URL in the skill call, use that instead.
- **Griot and Grits collection link** — the interviewee's direct page on griotandgrits.org (e.g., `https://griotandgrits.org/collection?video=XXXXXXXXX`). This link is used as the primary watch CTA in the text message and as the "link in bio" destination for Instagram. Check if the user has provided it. If not, ask before proceeding — it is required for the text message output.

Also load the `.metadata.json` file if present — it's the compact version and can supplement.

After parsing, identify the most emotionally specific details from the description and historical context:
- A precise age or year ("she was 7 years old when…", "Washington, NC — 1942")
- A concrete sensory or physical detail ("being chased home from the corner store", "losing her eyelashes on an unfamiliar gas stove")
- A name or figure they looked up to ("Joe Louis", "Jackie Robinson")
- A turning point or journey (Great Migration, moving North, leaving home)

These specific details are the raw material for the caption. Generic phrases don't earn shares — specific moments do.

---

## Step 2 — Generate the caption

The goal of this post is not just to attract new followers — it's to reach the people who already know and love the person being interviewed. When the interviewee's family sees this post, they should feel compelled to share it. When someone from their hometown or neighborhood recognizes the story, they should tag their cousins. Write for the people closest to the story first. Their shares will reach everyone else.

### Brand voice

Griot and Grits preserves Black voices and Black history. The tone is reverent but alive — not academic, not performative. Think of how an elder in the community would tell someone "you need to hear this story." The language should feel like it belongs to the people whose stories are being told.

Draw on:
- The interviewee's name and their specific story — lead with the person, not a theme
- Concrete details from the description: exact ages, years, places, objects, people they mentioned (a gas stove, a corner store, Joe Louis — these are real and they land)
- The reader's own cultural memory — images that resonate across generations of Black American experience
- Pride and deep respect for the person — they gave their time and their truth

### Caption structure

Write for Instagram first (Facebook can use the same text). The first 125 characters are the hook — everything before "...more" — so lead with the line that earns the tap.

```
[HOOK — 1-2 short lines using the interviewee's name and one vivid detail
 from their story. Name them in the first or second line. Make it feel like
 a moment, not a headline.]

[STORY SETUP — 2-3 lines. Paint the picture: where they were born, what they
 moved through, what they carry. Use years and places. Make it specific enough
 that someone from that time and place recognizes it.]

[SHARE INVITATION — 1-2 lines. Explicitly invite the reader to share.
 Address the community who knows this story: "If your family made this journey…",
 "Tag someone who needs to hear this.", "Share this so their voice travels further."
 This line is not optional — every post must have it.]

[WATCH CTA — 1 line. Drive to the website or YouTube link.]

[DONATE ASK — 2 lines. Flows naturally from the emotional weight of the story.
 Frame it as a way to keep stories like this one alive — not as a general charity
 pitch. Use the $20/month figure and the give link. Example form:
 "Help us preserve the next story. $20/month keeps one voice alive for generations."
 "give.griotandgrits.org"]

[blank line]
[HASHTAGS — 20–28 tags]
```

Keep the total caption under 2,200 characters. The copy above the hashtags should land within 450 characters — tight, punchy, earned. The donate ask should feel like a natural extension of the emotional moment, not an afterthought tacked onto the end.

### Caption writing guidelines

- **Name the person early.** Don't bury them in the third line. They are the story.
- **Specificity earns shares.** "She was 7 years old when her mother came back for her" hits harder than "her family moved North." Use what's in the description.
- **Write to the family, not the algorithm.** The person being interviewed likely has family, church members, and neighbors who will see this. Make them proud. Make them want to show it to someone.
- **The share invitation must be explicit.** Don't hint at it. Say it directly: "Tag someone," "Share this," "If you know someone who made this journey." Adjust the language to fit the story, but always include it.
- **No corporate language.** Avoid: "Learn more about," "Check out," "Discover," "Don't miss." Replace with: "Watch," "Hear," "See why," or simple imperatives.
- **Let the story breathe.** Line breaks at emotional pauses. White space is part of the rhythm.
- **Cultural phrases** that feel authentic (use only what fits the interview): references to the ancestors, the Great Migration, the church, the land, the hands that worked it.
- **The donate ask earns its place.** It should arrive after the emotional peak — after the story, after the share invitation — so the reader already feels the weight of what's at stake. Frame it around the mission: one story, one voice, preserved for generations. The $20/month figure is specific because specificity makes the ask real. The link is https://give.griotandgrits.org/

### Sharing language examples (adapt to the story)

- "If your family made this same journey — share this."
- "Tag someone who needs to hear Miss [Name]'s story. 🙏🏾"
- "Someone in your family lived this. Tag them."
- "Share this so [Name]'s voice travels further than this post."
- "If you know [Name] — tag them. Let them see how far their story reaches."
- "This is the Great Migration, one family at a time. Share it forward."

### Donate ask examples (adapt to the story, always include the link and $20/month figure)

- "Help us preserve the next story.\n$20/month keeps one voice alive for generations. → give.griotandgrits.org"
- "Stories like [Name]'s deserve to last forever.\nSupport the mission for $20/month. give.griotandgrits.org"
- "If this story moved you — help us save the next one.\n$20/month. One story. Preserved for generations. give.griotandgrits.org"
- "This work takes resources. $20/month from you means one more voice — one more family's story — saved forever.\ngive.griotandgrits.org"

### Hashtag strategy

Always include these brand hashtags:
```
#GriotAndGrits #BlackVoicesWorthRemembering #BlackHistory #OralHistory
```

Then derive 16–24 more from the metadata. Pull from:
- The interviewee's name (`#AnnEMoore`, `#IreneClark`) — always include
- Tags in the metadata file (convert to hashtag form: "Family History" → `#FamilyHistory`)
- Locations from historical context (`#Brownsville`, `#Brooklyn`, `#NorthCarolina`)
- Named historical figures or events mentioned in the description (`#GreatMigration`, `#JoeLouis`, `#JackieRobinson`)
- Broad discovery tags: `#BlackStories`, `#AncestorVoices`, `#BlackAmerica`, `#AfricanAmerican`, `#BlackHeritage`
- Theme-specific (only if it actually fits): `#BlackWomen`, `#BlackFamily`, `#BlackMigration`, `#SegregationEra`, `#ShareOurStories`

Avoid irrelevant trending hashtags. Every tag should relate to the content or the brand.

### Platform variants

Generate both variants by default:

**Instagram version** — Caption as described above. The donate ask sits just before the hashtag block, after the watch CTA. Keep it to two lines — the link on its own line so it's tappable. Hashtags in the same post, separated by a blank line.

**Facebook version** — Same core copy but slightly expanded — one or two more lines of story context, since Facebook audiences read more. Embed the YouTube link directly in the post body (not just "link in bio"). For the donate ask, add one more sentence of context about the mission: "Every $20/month preserves one story — one voice — for the people who come after us." Include the give link as a clickable URL. Reduce hashtags to 5–8 most relevant. Make the share invitation even more direct: Facebook's share mechanics mean explicitly asking people to share or tag actually works better here.

**Text message version** — A short, warm message someone can forward to family over SMS or iMessage. Aim for under 400 characters (2–3 SMS segments). No hashtags. No marketing language. Write it the way you'd text a cousin: "Hey, you need to see this."

This message could be sent by anyone — a family member, a supporter, a volunteer. Write it so it sounds like a text from a friend who genuinely cares: warm, direct, no formality. The video is the hook, but the **main ask is $20/month** to help keep this work going.

Structure:
```
[Name + one vivid hook — 1 casual sentence, like you're telling someone about it over the phone]
[Griot and Grits collection link — griotandgrits.org/collection?video=XXXXX
 This is the primary watch CTA in the text message. Do NOT use the YouTube link here —
 we want to drive traffic to the G&G site, not YouTube.]
[Blank line]
[Donate ask — personal but not founder-specific. Frame it as caring about the mission:
 "This work needs our support." $20/month = one story preserved per month.
 give.griotandgrits.org]
[Forward nudge — short and warm]
```

The donate ask should sound like a friend encouraging another friend to support something meaningful — not a nonprofit mailer. Two things must come through clearly:

1. **This is free for the Black community.** Griot and Grits preserves these stories at no cost to the people sharing them. That generosity is part of the ask — "we do this free, but we need your help to keep doing it."

2. **There is urgency right now.** In the current climate — with Black history being banned from schools, erased from textbooks, and stripped from institutions — the work of preserving these voices is not just meaningful, it's necessary. The message should carry that weight without being preachy. A single line is enough: let the reader feel it.

Keep the total message tight. The urgency should make it feel more important, not longer.

Present all three to the user and ask for approval or changes before saving.

---

## Step 3 — Create the branded thumbnail image

Create a 1080×1080 px branded image suitable for Instagram and Facebook.

**Order of preference for the source image — check these in order:**
1. YouTube thumbnail (preferred if the video is already uploaded)
2. Local video file (extract a frame)
3. User-provided image file

### Option A — YouTube video already uploaded (preferred)

If a YouTube video ID was found in Step 1, download the highest-quality thumbnail available:

```bash
python scripts/create_social_image.py \
  --youtube-id "<video_id>" \
  --name "<interviewee_name>" \
  --title "<short_subtitle_from_youtube_title>" \
  --output "<output_dir>/<video_basename>_social.jpg"
```

The script tries `maxresdefault.jpg` first (1280×720, best quality), then falls back to `hqdefault.jpg` (480×360) if the high-res version isn't available. These are standard YouTube thumbnail URLs:
- `https://img.youtube.com/vi/<VIDEO_ID>/maxresdefault.jpg`
- `https://img.youtube.com/vi/<VIDEO_ID>/hqdefault.jpg`

### Option B — Local video file

If no YouTube ID is available but the video file is present:

```bash
python scripts/create_social_image.py \
  --video "<video_file_path>" \
  --name "<interviewee_name>" \
  --title "<short_subtitle_from_youtube_title>" \
  --output "<output_dir>/<video_basename>_social.jpg"
```

The script extracts a frame at 15% of the video duration (typically past the opening slate, with the subject on camera).

### Option C — Image file provided

```bash
python scripts/create_social_image.py \
  --image "<thumbnail_image_path>" \
  --name "<interviewee_name>" \
  --title "<short_subtitle_from_youtube_title>" \
  --output "<output_dir>/<video_basename>_social.jpg"
```

### Option D — No source available

Tell the user the image step requires either a YouTube video ID, the local video file, or an existing thumbnail image. Offer to complete the caption step only and have them add the image manually.

### What the script does (all options)

1. Loads or downloads the source image
2. Center-crops to 1080×1080
3. Applies a dark gradient overlay at the bottom third
4. Adds the "GRIOT & GRITS" wordmark in gold at the top-left, with the tagline "Black Voices Worth Remembering" at the top-right
5. Adds the interviewee's name in bold white near the bottom, with a gold accent bar on the left edge
6. Adds a short subtitle line in cream text below the name

If Pillow is not installed:
```bash
pip install Pillow
```

---

## Step 4 — Save outputs

Save to the output directory (same as the metadata file's directory):

- `<video_basename>_instagram.txt` — the Instagram caption (ready to copy-paste)
- `<video_basename>_facebook.txt` — the Facebook caption
- `<video_basename>_text.txt` — the SMS/text message version
- `<video_basename>_social.jpg` — the branded thumbnail image

Confirm the saved file paths to the user. For each output, give one line on how to use it:
- **Instagram** — upload `_social.jpg` + paste `_instagram.txt`. Update bio link to the video page on griotandgrits.org.
- **Facebook** — upload `_social.jpg` + paste `_facebook.txt`. The YouTube link is already in the body.
- **Text message** — open `_text.txt`, copy, and send to family. Encourage them to forward it.

---

## Wrap-up

Tell the user the files are ready and share the paths. Offer a quick reminder:

- **Instagram:** Post the image + caption. Use "link in bio" and update the bio link to the video page on griotandgrits.org.
- **Facebook:** Post image + caption with the YouTube link embedded directly in the post body.
- **YouTube community tab** (optional): A shorter version of the hook (first 2 lines only) works well as a community post to drive views.
