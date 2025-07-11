#!/usr/bin/env python3
"""
GIF-to-ASCII converter that keeps the GIF's aspect ratio.

Requires:
    pip install pillow pyperclip
"""

from pathlib import Path
from PIL import Image
import pyperclip
import sys

# ───── CONFIG ─────
HERE = Path(__file__).parent.resolve()

GIF_DIR   = HERE / "gifs"      # folder with your .gif files
MAX_WIDTH = 130                # caps the ASCII art width (columns)
CHAR_RATIO = 0.55              # roughly: char-height / char-width

PALETTE = " .,:;+*?%$#@"       # darkest → lightest
# PALETTE = " .,:;+*?%$#@"     # lightest → darkest
# PALETTE = " .:-=+*#%@"

LEVELS  = len(PALETTE) - 1

# ───── LET USER PICK A GIF ─────
gif_files = sorted(GIF_DIR.glob("*.gif"))
if not gif_files:
    sys.exit(f"❌ No .gif files found in {GIF_DIR}")

print("Available GIFs")
print("==============")
for idx, path in enumerate(gif_files, 1):
    print(f"{idx:>3}. {path.name}")

while True:
    try:
        choice = int(input(f"\nPick a GIF (1-{len(gif_files)}): "))
        if 1 <= choice <= len(gif_files):
            GIF_PATH = gif_files[choice - 1]
            print(f"\n✅ Using {GIF_PATH.name}\n")
            break
        print("Number out of range, try again.")
    except ValueError:
        print("Please enter a valid number.")

# ───── FRAME HANDLER ─────
def gif_frames(gif_path):
    """Yield every frame of a GIF as PIL RGBA images (transparency→black)."""
    im = Image.open(gif_path)
    try:
        while True:
            yield im.convert("RGBA")
            im.seek(im.tell() + 1)
    except EOFError:
        return

# ───── ASCII CONVERTER ─────
def calc_target_size(orig_w, orig_h):
    """
    Return (target_w, target_h) so that:
      • width ≤ MAX_WIDTH
      • aspect ratio of pixels is preserved
      • char-cells are ≈ CHAR_RATIO as tall as they are wide
    """
    scale = min(1.0, MAX_WIDTH / orig_w)        # shrink if wider than MAX_WIDTH
    w = int(orig_w * scale)
    h = int(orig_h * scale * CHAR_RATIO)
    return max(1, w), max(1, h)

def frame_to_ascii(img, target_w, target_h):
    """Resize an image and convert it to ASCII text."""
    img = img.resize((target_w, target_h), Image.BICUBIC).convert("L")

    ascii_lines = []
    for y in range(img.height):
        row = []
        for x in range(img.width):
            pixel = img.getpixel((x, y))
            level = pixel * LEVELS // 255
            row.append(PALETTE[int(level)])
        ascii_lines.append("".join(row))

    return "\n".join(ascii_lines)

# ───── MAIN ─────
# Open once to get total frame count
with Image.open(GIF_PATH) as im:
    total_frames = getattr(im, "n_frames", None)
    if total_frames is None:
        total_frames = sum(1 for _ in gif_frames(GIF_PATH))

print(f"🔄 Converting {total_frames} frame(s) to ASCII…")

# Determine size once (first frame = safest)
first_frame = next(gif_frames(GIF_PATH))
TARGET_W, TARGET_H = calc_target_size(*first_frame.size)

ascii_frames = []
# Process first frame
ascii_frames.append(frame_to_ascii(first_frame, TARGET_W, TARGET_H))
print(f"  ✓ Frame 1/{total_frames}")

# Process the rest
for idx, frame in enumerate(gif_frames(GIF_PATH), start=2):
    ascii_frames.append(frame_to_ascii(frame, TARGET_W, TARGET_H))
    print(f"  ✓ Frame {idx}/{total_frames}")

if not ascii_frames:
    sys.exit("❌ No frames found in GIF.")

print("✅ All frames converted!\n")

# Quick preview
print(f"[preview] {TARGET_W}x{TARGET_H} characters\n")
print(ascii_frames[0][:120] + "...\n")

# Join frames & copy to clipboard
full_output = f"\n\n".join(ascii_frames) + "\n"
pyperclip.copy(full_output)

print(f"✅ Copied {len(ascii_frames)} ASCII frame(s) "
      f"({len(full_output):,} characters) to clipboard.")

# ───── WRITE TO FILE ─────
output_file = HERE / "frames.txt"

try:
    with output_file.open("w", encoding="utf-8") as f:
        f.write(full_output)
    print(f"📝 Saved output to {output_file.name} ({output_file.stat().st_size:,} bytes)")
except Exception as e:
    print(f"❌ Failed to write to {output_file.name}: {e}")
