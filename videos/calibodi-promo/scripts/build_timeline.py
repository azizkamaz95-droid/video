#!/usr/bin/env python3
"""Rebuild timeline.json (scene windows + per-word cue times) from assets/voice/voice_meta.json."""
import json
import os

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCENES = [
    # (id, start, duration, voice lead-in)
    ("01-chaos", 0.0, 8.0, 0.6), ("02-declic", 8.0, 3.0, 0.3), ("03-reveal", 11.0, 5.5, 0.6),
    ("04-sport", 16.5, 8.5, 0.35), ("05-nutrition", 25.0, 10.0, 0.35), ("06-recup", 35.0, 6.5, 0.35),
    ("07-hydratation", 41.5, 5.0, 0.35), ("08-connecte", 46.5, 8.0, 0.35), ("09-cta", 54.5, 8.5, 0.4),
]

meta = json.load(open(os.path.join(PROJECT, "assets", "voice", "voice_meta.json")))
out = {"bpm": 120, "bar_offset": 1.0, "total": 63.0, "scenes": []}
for i, (sid, start, dur, lead) in enumerate(SCENES, 1):
    m = meta[str(i)]
    assert start + lead + m["duration"] < start + dur, f"{sid}: voice overruns its scene"
    out["scenes"].append({
        "id": sid, "frame": i, "start": start, "duration": dur,
        "vo_start": round(start + lead, 3), "vo_local": lead, "vo_file": m["file"], "vo_duration": m["duration"],
        "words": [{"w": w["word"], "t": round(lead + w["start"], 3)} for w in m["words"]],
    })
json.dump(out, open(os.path.join(PROJECT, "timeline.json"), "w"), ensure_ascii=False, indent=1)
print("timeline.json:", ", ".join(f'{s["id"]} vo {s["vo_local"]}→{round(s["vo_local"] + s["vo_duration"], 2)}s' for s in out["scenes"][-1:]))
