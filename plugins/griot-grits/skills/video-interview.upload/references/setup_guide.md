# YouTube API Setup Guide (One-Time)

Complete these steps once before your first upload.

## 1. Create a Google Cloud Project

1. Go to https://console.cloud.google.com/
2. Click **New Project** → name it `griot-and-grits` → Create
3. Make sure the new project is selected in the top dropdown

## 2. Enable the YouTube Data API v3

1. In the left menu → **APIs & Services** → **Library**
2. Search for `YouTube Data API v3`
3. Click it → **Enable**

## 3. Create OAuth2 Credentials

1. **APIs & Services** → **Credentials** → **Create Credentials** → **OAuth client ID**
2. If prompted to configure the consent screen:
   - User type: **External**
   - App name: `Griot and Grits Upload`
   - Support email: your email
   - Save and continue through the rest (defaults are fine)
   - On the **Test users** screen, add your Google account email
3. Back to Create OAuth client ID:
   - Application type: **Desktop app**
   - Name: `griot-and-grits-uploader`
   - Click **Create**
4. Click **Download JSON** on the confirmation dialog
5. Rename the downloaded file to `client_secrets.json`
6. Move it into `.youtube_credentials/` inside your video-processing folder:
   ```
   video-processing/
   └── .youtube_credentials/
       └── client_secrets.json
   ```

## 4. Install Required Python Packages

```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib openai-whisper
```

Also install ffmpeg if not already present:
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Windows: download from https://ffmpeg.org/download.html
```

## 5. First Run — Authorize Access

The first time you run `upload_to_youtube.py`, it will open a browser window asking you to authorize access to the Griot and Grits YouTube account. Sign in with the Griot and Grits Google account and click Allow. The token is saved to `.youtube_credentials/token.pickle` so you won't need to do this again.

## Video Processing Folder Structure

```
video-processing/
├── .youtube_credentials/
│   ├── client_secrets.json     ← from Google Cloud Console
│   └── token.pickle            ← created automatically after first auth
├── <interview-name>.mp4        ← drop new videos here
└── <interview-name>.txt        ← optional pre-existing transcript
```
