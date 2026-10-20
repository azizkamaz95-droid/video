#!/usr/bin/env python3
"""Remove the white halo a white-background cutout leaves: choke the matte and un-mix white from edge pixels.

usage: clean_cutout.py <original.jpg|png> <cutout_rgba.png> <out.png> [choke_px]
"""
import subprocess
import sys

import numpy as np
from scipy.ndimage import gaussian_filter, minimum_filter


def load(path, channels):
    w, h = map(int, subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=width,height", "-of", "csv=p=0", path],
                                   capture_output=True, text=True).stdout.strip().split(",")[:2])
    fmt = "rgba" if channels == 4 else "rgb24"
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "rawvideo", "-pix_fmt", fmt, "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(h, w, channels).astype(np.float32), w, h


src, w, h = load(sys.argv[1], 3)
cut, _, _ = load(sys.argv[2], 4)
choke = int(sys.argv[4]) if len(sys.argv) > 4 else 2

a0 = cut[..., 3] / 255.0
a = minimum_filter(a0, size=2 * choke + 1)
a = np.clip(gaussian_filter(a, 0.8), 0, 1)
a = np.minimum(a, a0)

# un-mix the white background from partially covered pixels
cov = np.clip(a0, 0.08, 1.0)[..., None]
rgb = (src - (1 - cov) * 255.0) / cov
edge = (a0 < 0.995)[..., None]
rgb = np.where(edge, rgb, src)
# pull remaining light fringe toward the local interior colour
inner = gaussian_filter(src * a0[..., None], (3, 3, 0)) / np.maximum(gaussian_filter(a0, 3), 1e-3)[..., None]
lum = rgb.mean(axis=2, keepdims=True)
fringe = ((a < 0.9) & (a > 0.02))[..., None] & (lum > 200)
rgb = np.where(fringe, inner, rgb)

# near-white, low-saturation pixels in the outer band are leftover background: drop them
band = (minimum_filter(a0, size=13) < 0.5) & (a > 0)
ghost = band & (src.mean(axis=2) > 205) & ((src.max(axis=2) - src.min(axis=2)) < 40)
rgb = np.where(ghost[..., None], inner * 0.85, rgb)
a = np.where(ghost, a * 0.35, a)
a = np.clip(gaussian_filter(a, 0.9), 0, 1)

out = np.dstack([np.clip(rgb, 0, 255), a * 255]).astype(np.uint8)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{w}x{h}", "-i", "-", sys.argv[3]],
               input=out.tobytes(), check=True)
print("ok", sys.argv[3])
