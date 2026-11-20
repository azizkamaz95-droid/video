#!/usr/bin/env python3
"""Test objectif d'une prononciation : synthétise des variantes d'un mot (collé / IPA) dans des phrases NEUTRES et les fait
retranscrire par AssemblyAI (une phrase neutre ne laisse pas le modèle de langue « deviner » le bon mot).

usage: voice_probe.py "<mot>" "<ipa1>|T:<réécriture>" ["<ipa2>" ...] [--ctx "phrase avec {W}" ...]
Affiche, pour chaque variante (glue, puis chaque IPA), ce que l'oreille d'un transcripteur comprend. Ne remplace pas l'écoute
de l'utilisateur, mais élimine les lectures franchement fausses (« le fort », « tain »).
"""
import base64, json, os, subprocess, sys, tempfile, time, urllib.request

args = [a for a in sys.argv[1:]]
reps, hit = 1, None
if "--reps" in args:
    i = args.index("--reps"); reps = int(args[i + 1]); del args[i:i + 2]
if "--hit" in args:
    i = args.index("--hit"); hit = args[i + 1]; del args[i:i + 2]
ctx = []
if "--ctx" in args:
    i = args.index("--ctx"); ctx = args[i + 1:]; args = args[:i]
word, ipas = args[0], args[1:]
ctx = ctx or ["Écoute bien ce mot : {W}.", "Lui, {W}, et puis rien."]
key = os.environ["GOOGLE_CLOUD_API_KEY"]; akey = os.environ["ASSEMBLYAI_API_KEY"]
VOICE = "fr-FR-Chirp3-HD-Iapetus"
here = os.path.dirname(os.path.abspath(__file__))
T = tempfile.mkdtemp()


def tts(text, pron=None):
    inp = {"text": text}
    ver = "v1"
    if pron:
        inp["customPronunciations"] = {"pronunciations": pron}; ver = "v1beta1"
    body = {"input": inp, "voice": {"languageCode": "fr-FR", "name": VOICE}, "audioConfig": {"audioEncoding": "LINEAR16", "sampleRateHertz": 24000}}
    req = urllib.request.Request(f"https://texttospeech.googleapis.com/{ver}/text:synthesize?key={key}", data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    return base64.b64decode(json.loads(urllib.request.urlopen(req).read())["audioContent"])


def asr(wav):
    def call(path, data=None, raw=False):
        h = {"authorization": akey}
        if data is not None and not raw:
            data = json.dumps(data).encode(); h["content-type"] = "application/json"
        r = urllib.request.Request("https://api.assemblyai.com/v2" + path, data=data, headers=h, method="POST" if data is not None else "GET")
        return json.loads(urllib.request.urlopen(r).read())
    up = call("/upload", open(wav, "rb").read(), raw=True)["upload_url"]
    job = call("/transcript", {"audio_url": up, "language_code": "fr", "punctuate": True, "format_text": True})
    while True:
        res = call(f"/transcript/{job['id']}")
        if res["status"] in ("completed", "error"):
            return res.get("text") or res.get("error")
        time.sleep(2)


variants = [("collé", word.replace("'", "", 1), None)] + [((f"texte {p[2:]}", p[2:], None) if p.startswith("T:") else (f"ipa {p}", word, [{"phrase": word, "phoneticEncoding": "PHONETIC_ENCODING_IPA", "pronunciation": p}])) for p in ipas]
import re
for label, w, pron in variants:
    ok = n = 0
    for c in ctx:
        for _ in range(reps):
            text = c.replace("{W}", w)
            try:
                f = os.path.join(T, "x.wav"); open(f, "wb").write(tts(text, pron))
            except Exception as e:
                print(f"{label:22s} | refusé par l'API ({e})"); break
            r = asr(f); n += 1
            good = bool(re.search(hit, r, re.I)) if hit else None
            ok += bool(good)
            if reps == 1 or not hit:
                print(f"{label:22s} | {text:45s} -> {r}")
    if hit and n:
        print(f"== {label:22s} : {ok}/{n} lu comme « {hit} »")
