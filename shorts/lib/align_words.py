#!/usr/bin/env python3
"""Give the corrected words of an episode the timings of a fresh transcription of the *edited* voice.

usage: align_words.py <episode_dir> [--transcript existing.json] [split_seconds ...]

cut_silences.py remaps the memo's timings through the cuts, which drifts a little at every joint.
This re-transcribes assets/voice/voice.wav with Google (or reads --transcript), matches its tokens to
assets/voice/words.json (keeping our corrected spelling) and copies the timings over; words Google
missed get times interpolated from their neighbours. Run refine_words.py afterwards.
"""
import difflib
import json
import os
import re
import subprocess
import sys
import unicodedata

args = sys.argv[1:]
EP = os.path.abspath(args.pop(0))
tpath = None
if "--transcript" in args:
    k = args.index("--transcript")
    tpath = args[k + 1]
    del args[k:k + 2]
wpath = os.path.join(EP, "assets/voice/words.json")
data = json.load(open(wpath))
W = data["words"]

if tpath is None:
    tpath = os.path.join(EP, "source/transcript-edit-google.json")
    here = os.path.dirname(os.path.abspath(__file__))
    subprocess.run([sys.executable, os.path.join(here, "../../avatar/transcribe_google.py"), os.path.join(EP, "assets/voice/voice.wav"), tpath] + args,
                   check=True)
G = json.load(open(tpath))["words"]


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9']", "", s)


sm = difflib.SequenceMatcher(a=[norm(w["word"]) for w in W], b=[norm(g["word"]) for g in G], autojunk=False)
timed = [None] * len(W)
for a, b, n in sm.get_matching_blocks():
    for j in range(n):
        timed[a + j] = (G[b + j]["start"], G[b + j]["end"])
# also pair up equal-length replaced runs (e.g. a corrected spelling) one to one
for op, a0, a1, b0, b1 in sm.get_opcodes():
    if op == "replace" and a1 - a0 == b1 - b0:
        for j in range(a1 - a0):
            timed[a0 + j] = (G[b0 + j]["start"], G[b0 + j]["end"])

matched = sum(t is not None for t in timed)
for i, w in enumerate(W):
    if timed[i] is None:  # interpolate between the nearest timed neighbours
        p = next((j for j in range(i - 1, -1, -1) if timed[j]), None)
        q = next((j for j in range(i + 1, len(W)) if timed[j]), None)
        t0 = timed[p][1] if p is not None else 0.0
        t1 = timed[q][0] if q is not None else data["duration"]
        span = (q if q is not None else len(W)) - (p if p is not None else -1)
        k = i - (p if p is not None else -1)
        s = t0 + (t1 - t0) * (k - 1) / span
        timed[i] = (round(s, 3), round(s + (t1 - t0) / span, 3))
for w, (s, e) in zip(W, timed):
    w.pop("google", None)
    w["start"], w["end"] = s, e
json.dump(data, open(wpath, "w"), ensure_ascii=False, indent=1)
print(f"{matched}/{len(W)} words matched to the edited-voice transcription ({len(W) - matched} interpolated)")
