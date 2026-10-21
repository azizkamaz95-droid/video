#!/usr/bin/env python3
"""Cut out a pose whose 'transparent' background is a baked-in grey/white checkerboard.

usage: key_checker.py <source.png> <out_rgba.png> [round_px=90]
The checker is keyed by flood fill from the border (neutral pixels at the two checker tones only), so
bright scenery inside the picture (pillow, sheets) survives. Edges that touch the picture border
(scenery cut by the frame) get rounded corners, so the sticker reads as a die-cut shape.
"""
import sys

import numpy as np
from PIL import Image
from scipy.ndimage import binary_dilation, binary_fill_holes, gaussian_filter, label

src = np.asarray(Image.open(sys.argv[1]).convert("RGB")).astype(np.float32)
R = int(sys.argv[3]) if len(sys.argv) > 3 else 90
h, w, _ = src.shape
mx, mn = src.max(axis=2), src.min(axis=2)
neutral = (mx - mn) < 14
tone = neutral & (mn > 188)
lab, _ = label(tone)
seeds = set(np.unique(np.concatenate([lab[0], lab[:, 0], lab[:, -1]]))) - {0}
bg = np.isin(lab, list(seeds))
# anti-aliased checker pixels next to the keyed area (neutral, light) belong to the background too
for _ in range(3):
    ring = binary_dilation(bg) & ~bg & neutral & (mn > 170)
    bg |= ring
fg = binary_fill_holes(~bg)
# drop specks
lab2, n = label(fg)
sizes = np.bincount(lab2.ravel())
keep = np.zeros_like(fg)
for i in range(1, n + 1):
    if sizes[i] > 400:
        keep |= lab2 == i
fg = keep

# rounded corners where the scenery touches the picture border (right and bottom edges)
yy, xx = np.mgrid[0:h, 0:w]
inset = 6
x1, y1 = w - 1 - inset, h - 1 - inset
shape = (xx <= x1) & (yy <= y1)
for cx, cy in [(x1 - R, y1 - R), (inset + R, y1 - R)]:
    corner = ((xx > cx) if cx > w / 2 else (xx < cx)) & (yy > cy)
    shape &= ~corner | ((xx - cx) ** 2 + (yy - cy) ** 2 <= R * R)
shape &= xx >= inset
fg &= shape

a = gaussian_filter(fg.astype(np.float32), 0.7)  # soft 1-px edge
out = np.dstack([src, np.clip(a, 0, 1) * 255]).astype(np.uint8)
Image.fromarray(out, "RGBA").save(sys.argv[2], optimize=True)
print("ok", sys.argv[2], "fg", round(float(fg.mean()), 3))
