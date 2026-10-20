#!/usr/bin/env python3
"""Word-level French transcription with AssemblyAI (millisecond word timings, no 60 s limit).

usage: transcribe_assemblyai.py <audio> <out.json>
Reads the key from the ASSEMBLYAI_API_KEY environment variable (never put it in the code).
Writes the same format as avatar/transcribe_google.py: {"duration": s, "words": [{"word", "start", "end"}], "text"}.
"""
import json
import os
import subprocess
import sys
import time
import urllib.request

API = "https://api.assemblyai.com/v2"
audio, out = sys.argv[1], sys.argv[2]
key = os.environ["ASSEMBLYAI_API_KEY"]


def call(path, data=None, raw=False):
    headers = {"authorization": key}
    if data is not None and not raw:
        data = json.dumps(data).encode()
        headers["content-type"] = "application/json"
    req = urllib.request.Request(API + path, data=data, headers=headers, method="POST" if data is not None else "GET")
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())


dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", audio],
                           capture_output=True, text=True).stdout)
upload_url = call("/upload", open(audio, "rb").read(), raw=True)["upload_url"]
job = call("/transcript", {"audio_url": upload_url, "language_code": "fr", "punctuate": True, "format_text": True})
while True:
    res = call(f"/transcript/{job['id']}")
    if res["status"] in ("completed", "error"):
        break
    time.sleep(3)
if res["status"] == "error":
    sys.exit(f"AssemblyAI error: {res.get('error')}")
words = [{"word": w["text"], "start": round(w["start"] / 1000, 3), "end": round(w["end"] / 1000, 3)} for w in res["words"]]
json.dump({"duration": round(dur, 3), "words": words, "text": res.get("text", "")}, open(out, "w"), ensure_ascii=False, indent=1)
print(f"{len(words)} words, {dur:.1f}s")
