#!/usr/bin/env python3
"""Word-level French transcription with Google Cloud Speech-to-Text (sync API, audio split under 60 s).

usage: transcribe_google.py <audio> <out.json> [split_seconds ...]
Writes {"duration": s, "words": [{"word", "start", "end"}], "text": "..."}.
"""
import base64
import json
import os
import subprocess
import sys
import urllib.request

audio, out = sys.argv[1], sys.argv[2]
cuts = [float(x) for x in sys.argv[3:]]
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", audio],
                           capture_output=True, text=True).stdout)
bounds = [0.0] + cuts + [dur]
key = os.environ["GOOGLE_CLOUD_API_KEY"]
words = []
for a, b in zip(bounds[:-1], bounds[1:]):
    flac = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(a), "-to", str(b), "-i", audio, "-ac", "1", "-ar", "16000", "-f", "flac", "-"],
                          capture_output=True, check=True).stdout
    body = {
        "config": {"encoding": "FLAC", "sampleRateHertz": 16000, "languageCode": "fr-FR", "model": "latest_long",
                   "enableWordTimeOffsets": True, "enableAutomaticPunctuation": True},
        "audio": {"content": base64.b64encode(flac).decode()},
    }
    req = urllib.request.Request(f"https://speech.googleapis.com/v1/speech:recognize?key={key}", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        res = json.loads(r.read())
    for result in res.get("results", []):
        for w in result["alternatives"][0].get("words", []):
            sec = lambda t: float(t.rstrip("s"))
            words.append({"word": w["word"], "start": round(a + sec(w["startTime"]), 3), "end": round(a + sec(w["endTime"]), 3)})
json.dump({"duration": round(dur, 3), "words": words, "text": " ".join(w["word"] for w in words)}, open(out, "w"), ensure_ascii=False, indent=1)
print(f"{len(words)} words, {dur:.1f}s")
