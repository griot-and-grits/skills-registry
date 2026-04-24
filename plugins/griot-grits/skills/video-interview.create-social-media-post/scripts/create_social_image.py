#!/usr/bin/env python3
"""
Griot and Grits — Social Media Thumbnail Creator

Loads a source image from a YouTube video ID, local video file, or image path,
then composes a branded 1080x1080 image for Instagram/Facebook posts.

Usage:
    # From YouTube (preferred — downloads the official thumbnail):
    python create_social_image.py --youtube-id KZ7Hn5JAjwQ \
        --name "Ann E. Moore" \
        --title "From Little Washington to Brooklyn" \
        --output path/to/output.jpg

    # From local video file (extracts a frame):
    python create_social_image.py --video path/to/video.mp4 \
        --name "Rickey Thomas" \
        --title "Roots, Work, and Quiet Strength" \
        --output path/to/output.jpg

    # From an existing image file:
    python create_social_image.py --image path/to/thumb.jpg \
        --name "Irene Clark" \
        --title "Confronting the Stereotypes of Africa" \
        --output path/to/output.jpg
"""

import argparse
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
except ImportError:
    print("Pillow is required: pip install Pillow")
    sys.exit(1)

# ── Brand palette ──────────────────────────────────────────────────────────────
GOLD = (212, 175, 55)        # G&G brand gold
WHITE = (255, 255, 255)
CREAM = (245, 240, 232)
DARK = (20, 14, 8)           # Deep warm black
OVERLAY_COLOR = (20, 14, 8)  # Bottom gradient base

SIZE = (1080, 1080)

# ── Font resolution ────────────────────────────────────────────────────────────
FONT_CANDIDATES = [
    # Fedora / RHEL (this machine)
    "/usr/share/fonts/adwaita-sans-fonts/AdwaitaSans-Regular.ttf",
    "/usr/share/fonts/google-noto-vf/NotoSans[wght].ttf",
    "/usr/share/fonts/abattis-cantarell-vf-fonts/Cantarell-VF.otf",
    # Debian / Ubuntu
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
    # macOS
    "/System/Library/Fonts/Helvetica.ttc",
    # Windows
    "C:/Windows/Fonts/arialbd.ttf",
]

FONT_REGULAR_CANDIDATES = [
    "/usr/share/fonts/adwaita-sans-fonts/AdwaitaSans-Regular.ttf",
    "/usr/share/fonts/google-noto-vf/NotoSans[wght].ttf",
    "/usr/share/fonts/abattis-cantarell-vf-fonts/Cantarell-VF.otf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/usr/share/fonts/truetype/ubuntu/Ubuntu-R.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
    "C:/Windows/Fonts/arial.ttf",
]


def load_font(candidates: list[str], size: int) -> ImageFont.ImageFont:
    for path in candidates:
        if Path(path).exists():
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def extract_video_frame(video_path: str, position_pct: float = 0.15) -> Image.Image:
    """Extract a single frame from a video at `position_pct` of total duration."""
    # Get duration
    result = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            video_path,
        ],
        capture_output=True,
        text=True,
    )
    duration = float(result.stdout.strip())
    seek_time = duration * position_pct

    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
        tmp_path = tmp.name

    subprocess.run(
        [
            "ffmpeg", "-y",
            "-ss", str(seek_time),
            "-i", video_path,
            "-frames:v", "1",
            "-q:v", "2",
            tmp_path,
        ],
        capture_output=True,
        check=True,
    )
    return Image.open(tmp_path).convert("RGB")


def center_crop_square(img: Image.Image) -> Image.Image:
    w, h = img.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    return img.crop((left, top, left + side, top + side))


def apply_brand_overlay(
    img: Image.Image,
    name: str,
    title: str,
) -> Image.Image:
    """Composite the Griot & Grits branded overlay onto the image."""
    img = img.resize(SIZE, Image.LANCZOS)
    result = img.copy().convert("RGBA")

    # ── Fonts ──────────────────────────────────────────────────────────────────
    font_brand   = load_font(FONT_CANDIDATES, 34)
    font_name    = load_font(FONT_CANDIDATES, 72)
    font_title   = load_font(FONT_REGULAR_CANDIDATES, 38)
    font_tagline = load_font(FONT_REGULAR_CANDIDATES, 26)

    margin = 36

    # ── Measure text to size the bottom panel ─────────────────────────────────
    # Use a throw-away draw to measure before compositing
    measure = ImageDraw.Draw(Image.new("RGBA", SIZE))
    name_lines  = _wrap_text(name, font_name, SIZE[0] - margin * 2 - 12, measure)
    title_lines = _wrap_text(title, font_title, SIZE[0] - margin * 2 - 12, measure)[:2]

    name_block_h  = len(name_lines) * 82
    title_block_h = len(title_lines) * 48
    panel_h = name_block_h + title_block_h + margin * 3   # top padding + gap + bottom padding
    panel_top = SIZE[1] - panel_h

    # ── Bottom gradient (photo fades into panel) ───────────────────────────────
    grad_top = max(0, panel_top - 160)
    overlay = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for y in range(grad_top, panel_top):
        progress = (y - grad_top) / (panel_top - grad_top)
        alpha = int(180 * (progress ** 1.2))
        draw.line([(0, y), (SIZE[0], y)], fill=(*OVERLAY_COLOR, alpha))

    # ── Solid bottom panel ─────────────────────────────────────────────────────
    draw.rectangle([(0, panel_top), (SIZE[0], SIZE[1])], fill=(*DARK, 240))

    # ── Gold accent bar (left edge of panel) ──────────────────────────────────
    draw.rectangle([(0, panel_top), (7, SIZE[1])], fill=(*GOLD, 255))

    # ── Top brand bar ──────────────────────────────────────────────────────────
    bar_h = 64
    draw.rectangle([(0, 0), (SIZE[0], bar_h)], fill=(*DARK, 210))

    result = Image.alpha_composite(result, overlay)
    draw = ImageDraw.Draw(result)

    # ── Brand wordmark (top bar) ───────────────────────────────────────────────
    brand_text   = "GRIOT & GRITS"
    tagline_text = "Black Voices Worth Remembering"
    draw.text((margin, 15), brand_text, font=font_brand, fill=GOLD)

    tagline_bbox = draw.textbbox((0, 0), tagline_text, font=font_tagline)
    tagline_w = tagline_bbox[2] - tagline_bbox[0]
    draw.text(
        (SIZE[0] - tagline_w - margin, 19),
        tagline_text,
        font=font_tagline,
        fill=(*CREAM, 210),
    )

    # ── Interviewee name ──────────────────────────────────────────────────────
    text_x   = margin + 16       # indent past the gold bar
    name_y   = panel_top + margin
    for i, line in enumerate(name_lines):
        draw.text((text_x, name_y + i * 82), line, font=font_name, fill=WHITE)

    # ── Subtitle ───────────────────────────────────────────────────────────────
    title_y = name_y + name_block_h + 8
    for i, line in enumerate(title_lines):
        draw.text((text_x, title_y + i * 48), line, font=font_title, fill=(*CREAM, 230))

    return result.convert("RGB")


def _wrap_text(text: str, font: ImageFont.ImageFont, max_width: int, draw: ImageDraw.ImageDraw) -> list[str]:
    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = (current + " " + word).strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines or [text]


def download_youtube_thumbnail(video_id: str) -> Image.Image:
    """Download the best available YouTube thumbnail for the given video ID."""
    qualities = ["maxresdefault", "hqdefault", "sddefault", "default"]
    for quality in qualities:
        url = f"https://img.youtube.com/vi/{video_id}/{quality}.jpg"
        try:
            with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
                tmp_path = tmp.name
            urllib.request.urlretrieve(url, tmp_path)
            img = Image.open(tmp_path).convert("RGB")
            # YouTube returns a small black placeholder for missing qualities —
            # if the image is smaller than 200px wide, try the next quality.
            if img.width >= 200:
                print(f"  Downloaded YouTube thumbnail ({quality}): {url}")
                return img
        except Exception:
            continue
    raise RuntimeError(f"Could not download thumbnail for YouTube video ID: {video_id}")


def main():
    parser = argparse.ArgumentParser(description="Create Griot & Grits branded social image")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--youtube-id", help="YouTube video ID (downloads the official thumbnail)")
    source.add_argument("--video", help="Path to the interview video file (extracts a frame)")
    source.add_argument("--image", help="Path to an existing thumbnail image")
    parser.add_argument("--name", required=True, help="Interviewee name(s)")
    parser.add_argument("--title", required=True, help="Short subtitle from the interview title")
    parser.add_argument("--output", required=True, help="Output image path (.jpg or .png)")
    parser.add_argument(
        "--frame-pct",
        type=float,
        default=0.15,
        help="Video position (0.0–1.0) to extract frame from when using --video (default: 0.15)",
    )
    args = parser.parse_args()

    print(f"Loading source image...")
    if args.youtube_id:
        raw = download_youtube_thumbnail(args.youtube_id)
    elif args.video:
        raw = extract_video_frame(args.video, args.frame_pct)
        print(f"  Extracted frame at {args.frame_pct * 100:.0f}% of video duration")
    else:
        raw = Image.open(args.image).convert("RGB")
        print(f"  Loaded image: {args.image}")

    print("Cropping to square...")
    cropped = center_crop_square(raw)

    print("Applying Griot & Grits brand overlay...")
    branded = apply_brand_overlay(cropped, args.name, args.title)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # JPEG quality 92 gives great quality at ~200–400 KB
    save_kwargs = {"quality": 92, "optimize": True} if output_path.suffix.lower() in (".jpg", ".jpeg") else {}
    branded.save(str(output_path), **save_kwargs)
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()
