#!/usr/bin/env python3
"""
Upload a video to the Griot and Grits YouTube channel.

Usage:
    python upload_to_youtube.py \
        --video <path> \
        --title <title> \
        --description <description> \
        --tags <comma,separated,tags> \
        --credentials <path_to_client_secrets.json>

Settings applied automatically:
    - Visibility: Public
    - Made for kids: No
    - License: Standard YouTube License
    - Playlist: Griot and Grits - Black Voices Worth Remembering, Black History Worth Sharing

Settings that must be configured manually in YouTube Studio after upload:
    - Altered Content flag
    - Remixing: OFF
    - Comments: Hold all for review
    - Show like count
"""

import argparse
import os
import sys
import pickle

PLAYLIST_NAME = "Griot and Grits - Black Voices Worth Remembering, Black History Worth Sharing"
TOKEN_CACHE = ".youtube_credentials/token.pickle"
SCOPES = ["https://www.googleapis.com/auth/youtube.upload",
          "https://www.googleapis.com/auth/youtube"]


def get_authenticated_service(credentials_path: str):
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build
    except ImportError:
        print(
            "Missing packages. Run:\n"
            "  pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib",
            file=sys.stderr,
        )
        sys.exit(1)

    creds = None
    if os.path.exists(TOKEN_CACHE):
        with open(TOKEN_CACHE, "rb") as f:
            creds = pickle.load(f)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        os.makedirs(os.path.dirname(TOKEN_CACHE), exist_ok=True)
        with open(TOKEN_CACHE, "wb") as f:
            pickle.dump(creds, f)

    return build("youtube", "v3", credentials=creds)


def find_playlist_id(youtube, playlist_name: str) -> str | None:
    request = youtube.playlists().list(part="snippet", mine=True, maxResults=50)
    while request:
        response = request.execute()
        for item in response.get("items", []):
            if item["snippet"]["title"] == playlist_name:
                return item["id"]
        request = youtube.playlists().list_next(request, response)
    return None


def upload_video(youtube, video_path: str, title: str, description: str, tags: list[str]) -> str:
    try:
        from googleapiclient.http import MediaFileUpload
    except ImportError:
        print("Missing google-api-python-client", file=sys.stderr)
        sys.exit(1)

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": "22",  # People & Blogs
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False,
            "license": "youtube",
        },
    }

    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
    print(f"Uploading: {os.path.basename(video_path)}")
    print("This may take several minutes depending on file size and connection speed...")

    request = youtube.videos().insert(part=",".join(body.keys()), body=body, media_body=media)

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            progress = int(status.progress() * 100)
            print(f"  Upload progress: {progress}%", end="\r")

    video_id = response["id"]
    print(f"\nUpload complete. Video ID: {video_id}")
    return video_id


def add_to_playlist(youtube, video_id: str, playlist_id: str):
    youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {"kind": "youtube#video", "videoId": video_id},
            }
        },
    ).execute()
    print(f"Added to playlist: {PLAYLIST_NAME}")


def main():
    parser = argparse.ArgumentParser(description="Upload a video to Griot and Grits YouTube channel")
    parser.add_argument("--video", required=True, help="Path to video file")
    parser.add_argument("--title", required=True, help="YouTube video title")
    parser.add_argument("--description", required=True, help="YouTube video description")
    parser.add_argument("--tags", required=True, help="Comma-separated tags")
    parser.add_argument("--credentials", default=".youtube_credentials/client_secrets.json",
                        help="Path to client_secrets.json")
    args = parser.parse_args()

    if not os.path.exists(args.video):
        print(f"Error: video file not found: {args.video}", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(args.credentials):
        print(
            f"Error: credentials not found at {args.credentials}\n"
            "See references/setup_guide.md for instructions on setting up YouTube API access.",
            file=sys.stderr,
        )
        sys.exit(1)

    tags = [t.strip() for t in args.tags.split(",") if t.strip()]

    youtube = get_authenticated_service(args.credentials)

    playlist_id = find_playlist_id(youtube, PLAYLIST_NAME)
    if not playlist_id:
        print(
            f"Warning: playlist '{PLAYLIST_NAME}' not found on this account. "
            "The video will be uploaded but not added to the playlist.",
        )

    video_id = upload_video(youtube, args.video, args.title, args.description, tags)

    if playlist_id:
        add_to_playlist(youtube, video_id, playlist_id)

    url = f"https://www.youtube.com/watch?v={video_id}"
    print(f"\nVideo URL: {url}")
    print("\n--- MANUAL STEPS REQUIRED IN YOUTUBE STUDIO ---")
    print(f"Open: https://studio.youtube.com/video/{video_id}/edit")
    print("  [ ] Altered Content → check 'My video contains altered or synthetic content'")
    print("  [ ] Remixing        → ensure this is OFF (unchecked)")
    print("  [ ] Comments        → set to 'Hold all comments for review'")
    print("  [ ] Like count      → check 'Show how many viewers like this video'")
    print("  [ ] Auto chapters   → confirm enabled")
    print("  [ ] Featured places → confirm enabled")
    print("  [ ] Auto concepts   → confirm enabled")

    return url


if __name__ == "__main__":
    main()
