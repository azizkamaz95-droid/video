#!/usr/bin/env python3
"""Clean a voice memo, shorten its silences, remap word timings.

usage: cut_silences.py <voice_in> <transcript.json> <episode_plan.json> <out_dir>

plan keys used: "corrections" {index: text}, "breath_after" [word indexes], optional "gap", "breath".
Writes <out_dir>/voice.wav (48 kHz mono, -16 LUFS) and <out_dir>/words.json.
"""
import json
import os
import re
import subprocess
import sys

import numpy as np

src, tpath, ppath, out = sys.argv[1:5]
os.makedirs(out, exist_ok=True)
plan = json.load(open(ppath))
SR = 48000
GAP = plan.get("gap", 0.14)
BREATH = plan.get("breath", 0.38)
LEAD, TAIL = 0.08, 0.30

# 1) clean: high-pass, gentle denoise, light compression
clean = os.path.join(out, "voice_clean.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-ac", "1", "-ar", str(SR), "-af",
                "highpass=f=80,afftdn=nr=10:nf=-42,equalizer=f=3200:t=q:w=1.2:g=2,"
                "acompressor=threshold=-24dB:ratio=3:attack=5:release=90:makeup=2", clean], check=True)
pcm = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", clean, "-f", "f32le", "-"], capture_output=True, check=True).stdout, np.float32)
dur = len(pcm) / SR

# 2) speech/silence map from the waveform
log = subprocess.run(["ffmpeg", "-i", clean, "-af", "silencedetect=n=-38dB:d=0.18", "-f", "null", "-"], capture_output=True, text=True).stderr
starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
sil = list(zip(starts, ends + [dur] * (len(starts) - len(ends))))

t = json.load(open(tpath))
words = t["words"]
for k, v in plan.get("corrections", {}).items():
    words[int(k)]["word"] = v
breath_idx = set(plan.get("breath_after", []))
ends_w = np.array([w["end"] for w in words])


def target_gap(s):
    """Pause length to keep for a silence starting at s: longer after a key sentence."""
    i = int(np.argmin(np.abs(ends_w - s)))
    if abs(ends_w[i] - s) < 0.6 and i in breath_idx:
        return BREATH
    return GAP


# keep-segments: everything except the trimmed part of each silence
first_speech = sil[0][1] if sil and sil[0][0] < 0.05 else 0.0
last_speech = sil[-1][0] if sil and sil[-1][1] >= dur - 0.05 else dur
keep = []
cur = max(0.0, first_speech - LEAD)
for s, e in sil:
    if s <= first_speech or e >= last_speech:
        continue
    g = target_gap(s)
    if e - s > g:
        keep.append((cur, s + g / 2))
        cur = e - g / 2
keep.append((cur, min(dur, last_speech + TAIL)))

# 3) assemble with 6 ms fades at every joint
fade = int(0.006 * SR)
parts, mapping, t_new = [], [], 0.0
for a, b in keep:
    seg = pcm[int(a * SR):int(b * SR)].copy()
    if len(seg) > 2 * fade:
        seg[:fade] *= np.linspace(0, 1, fade)
        seg[-fade:] *= np.linspace(1, 0, fade)
    parts.append(seg)
    mapping.append((a, b, t_new))
    t_new += len(seg) / SR
edited = np.concatenate(parts)


def remap(x):
    for a, b, n in mapping:
        if x < a:
            return n
        if x <= b:
            return n + (x - a)
    return t_new


# 4) loudness: static gain to -16 LUFS, peak-limited
raw = os.path.join(out, "voice_edit_raw.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", raw], input=edited.tobytes(), check=True)
meas = subprocess.run(["ffmpeg", "-i", raw, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
lufs = float([l for l in meas.splitlines() if l.strip().startswith("I:")][-1].split()[1])
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", f"volume={-16 - lufs:.2f}dB,alimiter=limit=0.79:level=false",
                "-ar", str(SR), os.path.join(out, "voice.wav")], check=True)
os.remove(raw)

mapped = []
for i, w in enumerate(words):
    s, e = remap(w["start"]), remap(w["end"])
    mapped.append({"i": i, "word": w["word"], "start": round(s, 3), "end": round(max(e, s + 0.08), 3)})
json.dump({"duration": round(t_new, 3), "source_duration": round(dur, 3), "segments": [[round(a, 3), round(b, 3)] for a, b in keep],
           "words": mapped}, open(os.path.join(out, "words.json"), "w"), ensure_ascii=False, indent=1)
print(f"source {dur:.2f}s -> edited {t_new:.2f}s ({len(keep)} segments, removed {dur - t_new:.2f}s)")
