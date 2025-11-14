#!/usr/bin/env python3
"""
Generate single-page PDFs with multiple semi-transparent image layers
to benchmark compositing / blending performance.

Requires: pip install reportlab pillow numpy
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image
import numpy as np, io, os

# Register embedded font
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
pdfmetrics.registerFont(TTFont("DejaVuSans", FONT_PATH))

# Number of layers (increasing compositing load)
LAYER_COUNTS = [1, 2, 5, 10, 20, 40, 80, 160]
OUTDIR = "pdf_benchmarks_compositing"
os.makedirs(OUTDIR, exist_ok=True)

def make_random_png(size=800, alpha=128):
    """Return RGBA PNG bytes of random colors with given transparency."""
    arr = np.random.randint(0, 255, (size, size, 3), dtype=np.uint8)
    a = np.full((size, size, 1), alpha, dtype=np.uint8)
    rgba = np.concatenate([arr, a], axis=2)
    img = Image.fromarray(rgba, "RGBA")
    buf = io.BytesIO()
    img.save(buf, format="PNG", compress_level=0)
    buf.seek(0)
    return buf

# Prepare a few random layer sources so we don't regenerate each time
layer_sources = [make_random_png(alpha=a) for a in (80, 100, 120, 140)]

for layers in LAYER_COUNTS:
    fname = os.path.join(OUTDIR, f"composite_{layers:03d}_layers.pdf")
    print(f"Creating {fname} ...")

    c = canvas.Canvas(fname, pagesize=A4)
    c.setFont("DejaVuSans", 14)
    c.drawString(72, 800, f"Benchmark PDF — {layers} transparent layers")
    c.drawString(72, 780, "Tests compositing / blending performance.")
    base_x, base_y, w = 72, 100, 450

    # Draw layered images with slight offsets
    for i in range(layers):
        img = ImageReader(layer_sources[i % len(layer_sources)])
        dx = (i % 8) * 3
        dy = (i % 8) * 3
        c.saveState()
        c.translate(base_x + dx, base_y + dy)
        c.drawImage(img, 0, 0, width=w, preserveAspectRatio=True, mask='auto')
        c.restoreState()

    c.showPage()
    c.save()

print("Compositing-load benchmark PDFs created in:", OUTDIR)
