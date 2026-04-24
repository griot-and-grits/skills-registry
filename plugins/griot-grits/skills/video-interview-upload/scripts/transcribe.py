#!/usr/bin/env python3
"""
Transcribe a video file using local Whisper.
Extracts audio via ffmpeg, runs whisper, saves transcript as .txt beside the video.

Usage:
    python transcribe.py <video_file_path>
"""

import sys
import os
import subprocess
import tempfile


def transcribe(video_path: str) -> str:
    video_path = os.path.abspath(video_path)
    if not os.path.exists(video_path):
        print(f"Error: file not found: {video_path}", file=sys.stderr)
        sys.exit(1)

    base = os.path.splitext(video_path)[0]
    transcript_path = base + ".txt"

    if os.path.exists(transcript_path):
        print(f"Transcript already exists at: {transcript_path}")
        with open(transcript_path) as f:
            return f.read()

    print(f"Extracting audio from: {video_path}")
    with tempfile.TemporaryDirectory() as tmpdir:
        audio_path = os.path.join(tmpdir, "audio.wav")

        result = subprocess.run(
            ["ffmpeg", "-i", video_path, "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", audio_path],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print("ffmpeg error:", result.stderr, file=sys.stderr)
            sys.exit(1)

        print("Running Whisper transcription (this may take a few minutes)...")
        try:
            import whisper
        except ImportError:
            print("Whisper not installed. Run: pip install openai-whisper", file=sys.stderr)
            sys.exit(1)

        model = whisper.load_model("base")
        result = model.transcribe(audio_path)
        transcript = result["text"].strip()

    with open(transcript_path, "w") as f:
        f.write(transcript)

    print(f"Transcript saved to: {transcript_path}")
    return transcript


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python transcribe.py <video_file_path>", file=sys.stderr)
        sys.exit(1)

    text = transcribe(sys.argv[1])
    print("\n--- TRANSCRIPT ---")
    print(text)
