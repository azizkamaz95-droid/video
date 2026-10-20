#!/usr/bin/env python3
"""Turn Calix cutouts into stickers: thick white outline + soft drop shadow, baked into the PNG.

usage: make_sticker.py <cutout_dir> <out_dir> [outline_px=16]
Every pose keeps the same canvas (cutout size + padding) so poses swap in place.
"""
import glob
import os
import sys

import numpy as np
from PIL import Image, ImageFilter
from scipy.ndimage import distance_transform_edt, gaussian_filter

src, out = sys.argv[1], sys.argv[2]
R = int(sys.argv[3]) if len(sys.argv) > 3 else 16
PAD = R + 30
os.makedirs(out, exist_ok=True)
for p in sorted(glob.glob(os.path.join(src, "calix-*.png"))):
    im = Image.open(p).convert("RGBA")
    w, h = im.size
    canvas = Image.new("RGBA", (w + 2 * PAD, h + 2 * PAD), (0, 0, 0, 0))
    canvas.paste(im, (PAD, PAD), im)
    a = np.asarray(canvas)[..., 3].astype(float) / 255
    # outline: distance from the silhouette, anti-aliased edge at R px
    dist = distance_transform_edt(a < 0.5)
    ring = np.clip(R + 0.5 - dist, 0, 1)
    ring = gaussian_filter(ring, 0.6)
    # soft shadow under the sticker, offset down-right
    sh = gaussian_filter(np.maximum(ring, a), 9)
    sh = np.roll(np.roll(sh, 10, axis=0), 6, axis=1) * 0.45
    base = np.zeros((*a.shape, 4))
    base[..., 3] = sh  # black shadow
    white = np.zeros((*a.shape, 4)); white[..., :3] = 1; white[..., 3] = np.maximum(ring, a)
    # composite: shadow < white outline < character
    def over(top, bot):
        ao = top[..., 3:] + bot[..., 3:] * (1 - top[..., 3:])
        co = (top[..., :3] * top[..., 3:] + bot[..., :3] * bot[..., 3:] * (1 - top[..., 3:])) / np.maximum(ao, 1e-6)
        return np.concatenate([co, ao], -1)
    char = np.asarray(canvas).astype(float) / 255
    res = over(char, over(white, base))
    Image.fromarray((np.clip(res, 0, 1) * 255).astype(np.uint8)).save(os.path.join(out, os.path.basename(p)), optimize=True)
    print(os.path.basename(p))
