#!/usr/bin/env python3
"""Synthesize SCRIPT.md lines with Google Cloud TTS (v1beta1) and capture word timings via SSML marks."""
import base64
import html
import json
import os
import re
import subprocess
import sys
import urllib.request

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOICE = os.environ.get("TTS_VOICE", "fr-FR-Neural2-D")
PITCH = float(os.environ.get("TTS_PITCH", "-3"))
RATE = float(os.environ.get("TTS_RATE", "1.04"))
OUT_DIR = os.path.join(PROJECT, "assets", "voice")

PAUSES = {"…": 600, ".": 380, "?": 420, ":": 240, ",": 120}


def parse_script(path):
    lines = []
    for block in re.split(r"^## ", open(path, encoding="utf-8").read(), flags=re.M)[1:]:
        m = re.match(r"Line (\d+) — (.+?) \(Frame (\d+)\)", block)
        spoken = [l[4:] for l in block.splitlines() if l.startswith("    ") and l.strip()]
        lines.append({"line": int(m.group(1)), "label": m.group(2), "frame": int(m.group(3)), "text": " ".join(spoken).strip()})
    return lines


def to_ssml(text):
    words = text.split()
    parts = []
    for i, w in enumerate(words):
        parts.append(f'<mark name="w{i}"/>{html.escape(w)}')
        tail = w[-1]
        if tail in PAUSES and i < len(words) - 1:
            parts.append(f'<break time="{PAUSES[tail]}ms"/>')
    parts.append(f'<mark name="w{len(words)}"/>')
    return "<speak>" + " ".join(parts) + "</speak>", words


def synth(ssml):
    key = os.environ["GOOGLE_CLOUD_API_KEY"]
    payload = {
        "input": {"ssml": ssml},
        "voice": {"languageCode": "fr-FR", "name": VOICE},
        "audioConfig": {"audioEncoding": "LINEAR16", "sampleRateHertz": 24000, "pitch": PITCH, "speakingRate": RATE},
        "enableTimePointing": ["SSML_MARK"],
    }
    req = urllib.request.Request(
        f"https://texttospeech.googleapis.com/v1beta1/text:synthesize?key={key}",
        data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    lines = parse_script(os.path.join(PROJECT, "SCRIPT.md"))
    only = set(int(x) for x in sys.argv[1:]) if len(sys.argv) > 1 else None
    meta_path = os.path.join(OUT_DIR, "voice_meta.json")
    meta = json.load(open(meta_path)) if os.path.exists(meta_path) else {}
    for ln in lines:
        if only and ln["line"] not in only:
            continue
        ssml, words = to_ssml(ln["text"])
        res = synth(ssml)
        wav = os.path.join(OUT_DIR, f"vo-{ln['frame']:02d}.raw.wav")
        open(wav, "wb").write(base64.b64decode(res["audioContent"]))
        marks = {tp["markName"]: tp["timeSeconds"] for tp in res.get("timepoints", [])}
        out = os.path.join(OUT_DIR, f"vo-{ln['frame']:02d}.wav")
        # trim leading/trailing silence, keep a short natural tail, light loudness normalisation
        subprocess.run([
            "ffmpeg", "-v", "error", "-y", "-i", wav, "-af",
            "silenceremove=start_periods=1:start_threshold=-50dB,areverse,silenceremove=start_periods=1:start_threshold=-50dB,areverse,"
            "highpass=f=70,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120,loudnorm=I=-16:TP=-1.5:LRA=7",
            "-ar", "48000", "-ac", "1", out,
        ], check=True)
        lead = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", wav], capture_output=True, text=True).stdout)
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out], capture_output=True, text=True).stdout)
        # word marks are relative to the untrimmed file: shift by the leading silence we removed
        probe = subprocess.run(["ffmpeg", "-v", "info", "-i", wav, "-af", "silencedetect=n=-50dB:d=0.02", "-f", "null", "-"], capture_output=True, text=True).stderr
        m = re.search(r"silence_start: 0(?:\.0+)?\s.*?silence_end: ([\d.]+)", probe, flags=re.S)
        offset = float(m.group(1)) if m else 0.0
        wt = []
        for i, w in enumerate(words):
            s = marks.get(f"w{i}")
            e = marks.get(f"w{i+1}")
            if s is None:
                continue
            wt.append({"word": w, "start": round(max(0.0, s - offset), 3), "end": round(max(0.0, (e if e is not None else s + 0.3) - offset), 3)})
        os.remove(wav)
        meta[str(ln["frame"])] = {"frame": ln["frame"], "label": ln["label"], "text": ln["text"], "file": f"assets/voice/vo-{ln['frame']:02d}.wav", "duration": round(dur, 3), "words": wt}
        print(f"frame {ln['frame']:02d} {dur:5.2f}s ({len(words)} words) raw={lead:.2f}s lead_trim={offset:.2f}s")
    meta = dict(sorted(meta.items(), key=lambda kv: int(kv[0])))
    json.dump(meta, open(meta_path, "w"), ensure_ascii=False, indent=1)
    print("total", round(sum(v["duration"] for v in meta.values()), 2), "s")


if __name__ == "__main__":
    main()
