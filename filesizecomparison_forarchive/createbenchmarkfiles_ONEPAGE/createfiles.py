#!/usr/bin/env python3
"""
Benchmark PDFs with identical rendering content but different file sizes.
Use this to test I/O and parsing performance independently of rendering load.

Requires: pip install reportlab pillow numpy
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image
import numpy as np, io, os

# --- Configuration -----------------------------------------------------------
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
TARGET_SIZES_MB = [0.01, 0.1, 1, 5, 10, 50, 100]
OUTDIR = "pdf_benchmarks_uniform"
# -----------------------------------------------------------------------------


# Register embeddable font
pdfmetrics.registerFont(TTFont("DejaVuSans", FONT_PATH))

# Make a small constant random image (same for all files)
def make_reference_image(size=800):
    arr = np.random.randint(0, 255, (size, size, 3), dtype=np.uint8)
    img = Image.fromarray(arr, "RGB")
    buf = io.BytesIO()
    img.save(buf, format="PNG", compress_level=0)
    buf.seek(0)
    return buf

ref_img = make_reference_image()

# Generate files
os.makedirs(OUTDIR, exist_ok=True)
for size_mb in TARGET_SIZES_MB:
    fname = os.path.join(OUTDIR, f"bench_image_{size_mb:.2f}MB.pdf")
    print(f"Creating {fname} ...")

    c = canvas.Canvas(fname, pagesize=A4)
    c.setFont("DejaVuSans", 16)
    c.drawString(72, 800, f"Benchmark PDF — uniform load, target {size_mb} MB")
    c.drawString(72, 780, "Rendering identical, only file size scales.")
    c.drawImage(ImageReader(ref_img), 72, 100, width=450,
                preserveAspectRatio=True, mask='auto')
    c.showPage()
    c.save()

    # Pad to target size
    target_bytes = int(size_mb * 1024 * 1024)
    current_bytes = os.path.getsize(fname)
    pad = target_bytes - current_bytes
    if pad > 0:
        with open(fname, "ab") as f:
            # Valid but ignorable PDF comment stream
            f.write(b"\n%% BENCHMARK PADDING\n")
            f.write(b"%" * pad)

print("Uniform benchmark PDFs created in:", OUTDIR)
