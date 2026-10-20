#!/usr/bin/env python3
"""Union the human-segmentation matte with a white-background flood-fill key so held objects survive.

usage: keep_objects.py <original.jpg> <model_rgba.png> <out_rgba.png> [--dark-objects]
"""
import subprocess
import sys

import numpy as np
from scipy.ndimage import binary_dilation, gaussian_filter, label


def load(path, channels):
    w, h = map(int, subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=width,height", "-of", "csv=p=0", path],
                                   capture_output=True, text=True).stdout.strip().split(",")[:2])
    fmt = "rgba" if channels == 4 else "rgb24"
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "rawvideo", "-pix_fmt", fmt, "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(h, w, channels).astype(np.float32), w, h


src, w, h = load(sys.argv[1], 3)
model, _, _ = load(sys.argv[2], 4)

near_white = src.min(axis=2) >= 236
lab, n = label(near_white)
border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
bg = np.isin(lab, list(border))
bg = binary_dilation(bg, iterations=1)
fg = ~bg
if "--dark-objects" in sys.argv:
    fg &= ~near_white  # held object is not white: drop white background trapped between limbs
key = gaussian_filter(fg.astype(np.float32), 1.0)

a = np.maximum(model[..., 3] / 255.0, key)
out = np.dstack([src, a * 255]).astype(np.uint8)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{w}x{h}", "-i", "-", sys.argv[3]],
               input=out.tobytes(), check=True)
print("ok", sys.argv[3])
