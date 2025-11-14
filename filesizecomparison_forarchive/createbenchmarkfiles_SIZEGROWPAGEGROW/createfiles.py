#!/usr/bin/env python3
"""
Generate multi-page benchmark PDFs with embedded fonts.
All pages have identical content; file size scales with total page count.

Requires: pip install reportlab pillow numpy
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image
import numpy as np, io, os

# ---------------------------------------------------------------------------
# Configuration


 = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
pdfmetrics.registerFont(TTFont("DejaVuSans", FONT_PATH))

TARGET_SIZES_MB = [0.01, 0.1, 1, 5, 10, 50, 100, 200]#, 500]
TARGET_TOTAL_PAGES = [1, 2, 10, 50, 100, 500, 1000, 2000]#^, 5000]
OUTDIR = "pdf_benchmarks_multipage"
os.makedirs(OUTDIR, exist_ok=True)
# ---------------------------------------------------------------------------


def make_reference_image(size=800):
    arr = np.random.randint(0, 255, (size, size, 3), dtype=np.uint8)
    from io import BytesIO
    buf = BytesIO()
    Image.fromarray(arr, "RGB").save(buf, format="PNG", compress_level=0)
    buf.seek(0)
    return buf

ref_img = ImageReader(make_reference_image())


for size_mb, total_pages in zip(TARGET_SIZES_MB, TARGET_TOTAL_PAGES):
    fname = os.path.join(OUTDIR, f"multipage_{total_pages:04d}_pages_{size_mb:.2f}MB.pdf")
    print(f"Creating {fname} ({total_pages} pages, target ~{size_mb} MB)...")

    c = canvas.Canvas(fname, pagesize=A4)
    c.setFont("DejaVuSans", 14)

    for page in range(1, total_pages + 1):
        c.drawString(72, 800, f"Benchmark PDF — page {page}/{total_pages}")
        c.drawString(72, 780, "Identical layout on every page.")
        c.drawImage(ref_img, 72, 100, width=450,
                    preserveAspectRatio=True, mask='auto')
        c.showPage()

    c.save()

    # optional padding to reach target MB
    target_bytes = int(size_mb * 1024 * 1024)
    current_bytes = os.path.getsize(fname)
    pad = target_bytes - current_bytes
    if pad > 0:
        with open(fname, "ab") as f:
            f.write(b"\n%%PADDING\n")
            f.write(b"%" * pad)

print("Multi-page benchmark PDFs created in:", OUTDIR)
 
