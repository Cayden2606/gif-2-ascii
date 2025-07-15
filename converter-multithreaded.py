#!/usr/bin/env python3
"""
GIF-to-ASCII converter that keeps the GIF's aspect ratio.
Optimized with multithreading and progress bar for large GIFs.

Requires:
    pip install pillow pyperclip
"""

from pathlib import Path
from PIL import Image
import pyperclip
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple

# ───── CONFIG ─────
HERE = Path(__file__).parent.resolve()

GIF_DIR   = HERE / "gifs"      # folder with your .gif files
MAX_WIDTH = 130                # caps the ASCII art width (columns)
CHAR_RATIO = 0.55              # roughly: char-height / char-width
MAX_WORKERS = 4                # number of threads (adjust based on your CPU)

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
def extract_all_frames(gif_path: Path) -> List[Tuple[int, Image.Image]]:
    """Extract all frames from GIF and return as list of (index, frame) tuples."""
    frames = []
    im = Image.open(gif_path)
    
    # Try to get total frame count first
    try:
        total_frames = im.n_frames
        print(f"📊 GIF has {total_frames} frames")
    except AttributeError:
        print("📊 Counting frames...")
        total_frames = None
    
    try:
        frame_idx = 0
        while True:
            print(f"\r🔍 Extracting frame {frame_idx + 1}" + 
                  (f"/{total_frames}" if total_frames else ""), end="", flush=True)
            
            # Convert to RGBA first, then make a copy to avoid issues with threading
            frame = im.convert("RGBA").copy()
            frames.append((frame_idx, frame))
            frame_idx += 1
            
            # Add a small delay every 50 frames to prevent hanging
            if frame_idx % 50 == 0:
                import time
                time.sleep(0.01)
            
            im.seek(im.tell() + 1)
    except EOFError:
        pass
    except Exception as e:
        print(f"\n❌ Error extracting frame {frame_idx}: {e}")
        if not frames:
            raise
    finally:
        im.close()
    
    print(f"\n✅ Extracted {len(frames)} frames")
    return frames

# ───── ASCII CONVERTER ─────
def calc_target_size(orig_w: int, orig_h: int) -> Tuple[int, int]:
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

def frame_to_ascii(frame_data: Tuple[int, Image.Image], target_w: int, target_h: int) -> Tuple[int, str]:
    """
    Resize an image and convert it to ASCII text.
    Returns (frame_index, ascii_string) to maintain order.
    """
    frame_idx, img = frame_data
    
    # Resize and convert to grayscale
    img = img.resize((target_w, target_h), Image.BICUBIC).convert("L")

    ascii_lines = []
    for y in range(img.height):
        row = []
        for x in range(img.width):
            pixel = img.getpixel((x, y))
            level = pixel * LEVELS // 255
            row.append(PALETTE[int(level)])
        ascii_lines.append("".join(row))

    return frame_idx, "\n".join(ascii_lines)

# ───── MAIN ─────
print("🔍 Extracting frames from GIF...")

# Check if GIF file exists and is readable
if not GIF_PATH.exists():
    sys.exit(f"❌ GIF file not found: {GIF_PATH}")

try:
    # Quick check if file is a valid image
    with Image.open(GIF_PATH) as test_img:
        print(f"📁 File size: {GIF_PATH.stat().st_size:,} bytes")
        print(f"📐 Dimensions: {test_img.size[0]}x{test_img.size[1]}")
        
    # Extract all frames at once
    all_frames = extract_all_frames(GIF_PATH)
    total_frames = len(all_frames)

except Exception as e:
    sys.exit(f"❌ Error reading GIF file: {e}")

if not all_frames:
    sys.exit("❌ No frames found in GIF.")

print(f"📊 Found {total_frames} frame(s)")

# Determine target size from first frame
TARGET_W, TARGET_H = calc_target_size(*all_frames[0][1].size)
print(f"🎯 Target ASCII size: {TARGET_W}x{TARGET_H} characters")

# Process frames with multithreading and progress bar
print(f"🔄 Converting frames to ASCII using {MAX_WORKERS} thread(s)...")

ascii_results = {}
completed_count = 0

def update_progress():
    """Simple progress display without tqdm"""
    global completed_count
    completed_count += 1
    percent = (completed_count / total_frames) * 100
    bar_length = 30
    filled_length = int(bar_length * completed_count // total_frames)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    print(f'\r🔄 Progress: |{bar}| {completed_count}/{total_frames} ({percent:.1f}%)', end='', flush=True)

with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    # Submit all frame conversion tasks
    futures = [
        executor.submit(frame_to_ascii, frame_data, TARGET_W, TARGET_H)
        for frame_data in all_frames
    ]
    
    # Process completed tasks with simple progress display
    for future in as_completed(futures):
        try:
            frame_idx, ascii_frame = future.result()
            ascii_results[frame_idx] = ascii_frame
            update_progress()
        except Exception as e:
            print(f"\n❌ Error processing frame: {e}")
            update_progress()

print()  # New line after progress bar

# Sort frames by index to maintain original order
ascii_frames = [ascii_results[i] for i in sorted(ascii_results.keys())]

print("✅ All frames converted!\n")

# Quick preview
print(f"[preview] {TARGET_W}x{TARGET_H} characters\n")
preview_text = ascii_frames[0]
print(preview_text[:min(500, len(preview_text))] + ("..." if len(preview_text) > 500 else "") + "\n")

# Join frames & copy to clipboard
print("📋 Preparing output...")
full_output = f"\n\n".join(ascii_frames) + "\n"

print("📋 Copying to clipboard...")
try:
    pyperclip.copy(full_output)
    print(f"✅ Copied {len(ascii_frames)} ASCII frame(s) "
          f"({len(full_output):,} characters) to clipboard.")
except Exception as e:
    print(f"⚠️  Failed to copy to clipboard: {e}")

# ───── WRITE TO FILE ─────
output_file = HERE / "frames.txt"

print("💾 Saving to file...")
try:
    with output_file.open("w", encoding="utf-8") as f:
        f.write(full_output)
    print(f"📝 Saved output to {output_file.name} ({output_file.stat().st_size:,} bytes)")
except Exception as e:
    print(f"❌ Failed to write to {output_file.name}: {e}")

print("\n🎉 Processing complete!")