#!/usr/bin/env python3
"""Narrate a script with Google TTS, one sentence at a time, with controlled pauses.

usage: tts_script.py <episode_dir>
Reads  source/script.json {"voice", "rate", "lead", "sentences": [{"id", "text", "pause", "say"?, "rate"?}]}
       ("say" overrides what is spoken, "rate" overrides the speaking rate of one sentence)
Writes assets/voice/voice.wav (48 kHz mono, -16 LUFS), assets/voice/segments.json (start/end per sentence)
and a words.json skeleton (script words, timed later by align_words.py --transcript ...).
Key: GOOGLE_CLOUD_API_KEY in the environment.
"""
import base64
import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.request

import numpy as np

EP = os.path.abspath(sys.argv[1])
S = json.load(open(os.path.join(EP, "source/script.json")))
SR = 48000
key = os.environ["GOOGLE_CLOUD_API_KEY"]
cache = os.path.join(EP, "source/tts-cache")
os.makedirs(cache, exist_ok=True)


def spoken(text):
    # Chirp3 voices derail on French guillemets (« c'est l'âge » came out as gibberish): never send quote marks.
    # Elisions: with either apostrophe the voice often leaves a gap before the vowel (« n' était », « l' âge »).
    # Glue the elided letter to a lowercase next word for the voice only (« nétait », « lâge »); captions keep the
    # real spelling. Acronyms stay apart (« L'OMS »). Checked by transcription: every word comes back correct.
    for a, b in (("«", ""), ("»", ""), ("“", ""), ("”", ""), ("’", "'"), ("\u00a0", " ")):
        text = text.replace(a, b)
    text = re.sub(r"\b([cdjlmnstCDJLMNST]|[Qq]u|[Jj]usqu|[Ll]orsqu|[Pp]uisqu)'(?=[a-zàâäéèêëîïôöùûüœ])", r"\1", text)
    return " ".join(text.split())


def synth(text, rate=None):
    rate = rate or S["rate"]
    text = spoken(text)
    name = os.path.join(cache, hashlib.sha1(f"{S['voice']}|{rate}|{text}".encode()).hexdigest()[:16] + ".wav")
    if not os.path.exists(name):
        body = {"input": {"text": text}, "voice": {"languageCode": "fr-FR", "name": S["voice"]},
                "audioConfig": {"audioEncoding": "LINEAR16", "sampleRateHertz": SR, "speakingRate": rate}}
        req = urllib.request.Request(f"https://texttospeech.googleapis.com/v1/text:synthesize?key={key}",
                                     data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
        open(name, "wb").write(base64.b64decode(json.loads(urllib.request.urlopen(req).read())["audioContent"]))
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", name, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                                     capture_output=True, check=True).stdout, np.float32).astype(float)
    # trim the synthesizer's leading / trailing silence and breath noise (keep 40 ms before the voice)
    env = 20 * np.log10(np.sqrt(np.convolve(x ** 2, np.ones(960) / 960, "same")) + 1e-9)
    loud = np.where(env > env.max() - 32)[0]
    a, b = max(0, loud[0] - int(0.04 * SR)), min(len(x), loud[-1] + int(0.08 * SR))
    y = x[a:b].copy()
    # the synthesizer sometimes leaves a long breath inside one call ("Fait numéro deux. … Beaucoup"):
    # shorten every inner silence longer than max_gap down to max_gap (cut in its middle, short crossfade)
    gap = S.get("max_gap", 0.5)
    e = env[a:b]
    quiet = e < e.max() - 34
    runs, i = [], 0
    while i < len(quiet):
        if quiet[i]:
            j = i
            while j < len(quiet) and quiet[j]:
                j += 1
            if j - i > gap * SR and i > 0 and j < len(quiet):
                runs.append((i, j))
            i = j
        else:
            i += 1
    for i, j in reversed(runs):
        keep = int(gap * SR / 2)
        f = int(0.015 * SR)
        head, tail = y[:i + keep], y[j - keep:]
        head[-f:] = head[-f:] * np.linspace(1, 0, f) + tail[:f] * np.linspace(0, 1, f)
        y = np.concatenate([head, tail[f:]])
    n = int(0.01 * SR)
    y[:n] *= np.linspace(0, 1, n)
    y[-n:] *= np.linspace(1, 0, n)
    return y


parts, segs, t = [np.zeros(int(S.get("lead", 0.2) * SR))], [], S.get("lead", 0.2)
for s in S["sentences"]:
    x = synth(s.get("say", s["text"]), s.get("rate"))  # "say" = what the voice reads (numbers spelled out), "text" = captions
    segs.append({"id": s["id"], "text": s["text"], "start": round(t, 3), "end": round(t + len(x) / SR, 3)})
    parts += [x, np.zeros(int(s["pause"] * SR))]
    t += len(x) / SR + s["pause"]
parts.append(np.zeros(int(0.3 * SR)))
v = np.concatenate(parts).astype(np.float32)
os.makedirs(os.path.join(EP, "assets/voice"), exist_ok=True)
raw = os.path.join(EP, "assets/voice/.raw.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", raw], input=v.tobytes(), check=True)
meas = subprocess.run(["ffmpeg", "-i", raw, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
lufs = float([l for l in meas.splitlines() if l.strip().startswith("I:")][-1].split()[1])
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", f"volume={-16 - lufs:.2f}dB,alimiter=limit=0.79:level=false",
                "-ar", str(SR), os.path.join(EP, "assets/voice/voice.wav")], check=True)
os.remove(raw)
dur = round(len(v) / SR, 3)
json.dump({"duration": dur, "segments": segs}, open(os.path.join(EP, "assets/voice/segments.json"), "w"), ensure_ascii=False, indent=1)
toks, glue_next = [], False
for w in " ".join(s["text"] for s in S["sentences"]).split():
    if toks and all(c in ":;!?…»%.," for c in w):  # French spaced punctuation (and "55 %") sticks to its word
        toks[-1] += "\u00a0" + w
    elif glue_next:
        toks[-1] += "\u00a0" + w
    else:
        toks.append(w)
    glue_next = w == "«"  # an opening guillemet sticks to the next word
words = [{"i": i, "word": w, "start": 0.0, "end": 0.0} for i, w in enumerate(toks)]
json.dump({"duration": dur, "words": words}, open(os.path.join(EP, "assets/voice/words.json"), "w"), ensure_ascii=False, indent=1)
print(f"{len(segs)} sentences, {dur:.2f}s, {len(words)} words")
