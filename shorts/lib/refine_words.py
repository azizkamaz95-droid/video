#!/usr/bin/env python3
"""Snap word starts to the real speech onsets in the edited voice.

usage: refine_words.py <episode_dir>

Safety net after align_words.py. Google's word offsets are coarse (100 ms) and, after a kept breath, often start the next word at the end
of the previous one. When a word "starts" in silence, move its start to where the speech actually comes
back (never past its own end or the next word's start). Edits assets/voice/words.json in place and keeps
Google's original [start, end] as "google". Safe to run twice.
"""
import json
import os
import subprocess
import sys

import numpy as np
from scipy.ndimage import uniform_filter1d

EP = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
SR = 48000
wpath = os.path.join(EP, "assets/voice/words.json")
data = json.load(open(wpath))
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(EP, "assets/voice/voice.wav"), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                     capture_output=True, check=True).stdout
v = np.frombuffer(raw, np.float32).astype(float)
db = 20 * np.log10(np.sqrt(uniform_filter1d(v ** 2, int(0.02 * SR))[::480] + 1e-12))  # 10 ms frames
SILENT, SPEECH = -40.0, -32.0

W = data["words"]
for w in W:  # always restart from Google's own timings, so running this twice changes nothing
    w.setdefault("google", [w.pop("start_google", w["start"]), w["end"]])
    w["start"], w["end"] = w["google"]
moved = []
for i, w in enumerate(W):
    s0 = w["start"]
    f = int(round(s0 * 100))
    # a silent stretch (>= 80 ms under -40 dB) beginning within 250 ms of the start = the word hasn't begun yet
    q = next((k for k in range(f, min(f + 26, len(db) - 8)) if (db[k:k + 8] < SILENT).all()), None)
    if q is None or w["end"] <= (q + 8) / 100:  # the word ends before that silence: it was said before it
        continue
    limit = min(w["end"], W[i + 1]["google"][0] if i + 1 < len(W) else w["end"]) + 0.1
    g = q
    while g + 3 < len(db) and g / 100 < limit and not (db[g:g + 3] > SPEECH).all():
        g += 1
    nxt = W[i + 1]["google"][0] if i + 1 < len(W) else 1e9
    if g / 100 >= limit or g + 3 >= len(db):  # no speech in the word's own slot
        continue
    new = round(max(g / 100 - 0.02, s0), 3)  # 20 ms lead so the caption lands with the attack
    if new - s0 < 0.05 or new >= nxt - 0.02:  # never pass the next word
        continue
    w["start"] = new
    w["end"] = round(max(w["end"], new + 0.12), 3)
    moved.append((w["word"], s0, new))

# Google tends to squeeze the last phrase: stretch it onto the real last stretch of speech
loud = db > -30
runs = [k for k in range(len(db) - 3) if loud[k:k + 3].all()]
if runs:
    speech_end = (runs[-1] + 3) / 100
    e = int(speech_end * 100)
    while e > 8 and not (db[e - 8:e] < SILENT).all():
        e -= 1                                   # walk back to the last real silence
    island = e / 100
    k = next((j for j, w in enumerate(W) if w["start"] >= island - 0.1), len(W))
    if k < len(W) and speech_end - W[-1]["end"] > 0.15:
        a0, b0 = W[k]["start"], W[-1]["end"]
        a1 = max(a0, island)
        for w in W[k:]:
            w["start"] = round(a1 + (w["start"] - a0) * (speech_end - a1) / (b0 - a0), 3)
            w["end"] = round(a1 + (w["end"] - a0) * (speech_end - a1) / (b0 - a0), 3)
        moved.append((f"[last {len(W) - k} words stretched]", b0, speech_end))

json.dump(data, open(wpath, "w"), ensure_ascii=False, indent=1)
print(f"{len(moved)} word starts moved onto the speech")
for word, a, b in moved:
    print(f"  {word:16s} {a:6.2f} -> {b:6.2f}")
