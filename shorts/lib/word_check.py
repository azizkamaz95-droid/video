#!/usr/bin/env python3
"""Contrôle OBJECTIF des mots à risque dans la voix finale (utilisateur, 2026-11-20 : « l'effort » lu « le fort », « t'en » lu « tain »).

usage: word_check.py <episode_dir> [mot ...]
Pour chaque mot à risque (élisions, mots à trait d'union, plus ceux donnés en argument), découpe le mot dans assets/voice/voice.wav
(minutage de words.json) et le fait retranscrire par AssemblyAI SEUL, sans phrase autour : sans contexte, le modèle de langue ne peut
plus « deviner » le bon mot, il n'entend que ce que la voix a dit. « l'effort » lu « fort. » ou « t'en » lu « Tenez » sont alors visibles.
Verdict : OK si la transcription isolée contient le radical attendu (ou un homophone listé dans ACCEPT), sinon SUSPECT (code 1).
Ensuite : mettre "take": N+1 sur la phrase fautive dans source/script.json (nouvelle prise de la voix), relancer tts_script.py,
transcribe_assemblyai.py, align_words.py, puis ce contrôle, jusqu'à OK (6 prises au plus ; sinon IPA différente ou respell).
Ne remplace pas l'écoute de l'utilisateur : la liste « À ÉCOUTER » dit lesquels sont nouveaux (jamais validés à l'oreille)."""
import json, os, re, subprocess, sys, tempfile, time, unicodedata, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.abspath(sys.argv[1])
extra = sys.argv[2:]
akey = os.environ["ASSEMBLYAI_API_KEY"]
W = json.load(open(os.path.join(EP, "assets/voice/words.json")))["words"]
REG = json.load(open(os.path.join(HERE, "voice_validated.json")))["tokens"]
# homophones acceptés quand le radical n'est pas reconnaissable seul (clitiques)
# (comparaison EXACTE après normalisation : « Tenez » ne doit pas passer pour « t'en »). None = trop court pour un verdict isolé, à écouter.
ACCEPT = {"t'en": ["tant", "t'en", "temps", "tan", "tend"], "n'as": None, "qu'il": None, "qu'on": None, "d'un": None, "t'a": None,
          "j'ai": None, "c'est": None}


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return re.sub(r"[^a-z]", "", "".join(c for c in s if unicodedata.category(c) != "Mn"))


def call(path, data=None, raw=False):
    h = {"authorization": akey}
    if data is not None and not raw:
        data = json.dumps(data).encode(); h["content-type"] = "application/json"
    r = urllib.request.Request("https://api.assemblyai.com/v2" + path, data=data, headers=h, method="POST" if data is not None else "GET")
    return json.loads(urllib.request.urlopen(r).read())


def asr(wav):
    up = call("/upload", open(wav, "rb").read(), raw=True)["upload_url"]
    job = call("/transcript", {"audio_url": up, "language_code": "fr", "punctuate": True, "format_text": True})
    while True:
        res = call(f"/transcript/{job['id']}")
        if res["status"] in ("completed", "error"):
            return (res.get("text") or "").strip()
        time.sleep(2)


def risky(word):
    w = word.lower().strip(".,;:!?…«»\"()")
    return bool(re.match(r"^[\wàâäéèêëîïôöùûüœ]+['’-][\wàâäéèêëîïôöùûüœ]+$", w)) and not w.startswith("calibodi")


bad, listen = [], []
T = tempfile.mkdtemp()
for i, x in enumerate(W):
    raw = x["word"]; w = raw.lower().strip(".,;:!?…«»\"() ").replace("’", "'")
    if not (risky(raw) or w in [e.lower() for e in extra]):
        continue
    if re.match(r"^[\wàâäéèêëîïôöùûüœ]+-(moi|toi|lui|nous|vous|le|la|les|y|en)$", w):   # impératifs : lus tels quels, pas d'ambiguïté
        continue
    a, b = max(0, x["start"] - 0.04), x["end"] + 0.04
    c = os.path.join(T, f"{i}.wav")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", os.path.join(EP, "assets/voice/voice.wav"), "-ss", str(a), "-to", str(b), c], check=True)
    heard = asr(c)
    h = norm(heard)
    stem = re.sub(r"^(?:[cdjlmnst]|qu|jusqu|lorsqu|puisqu)'", "", w)           # l'effort -> effort
    if w in ACCEPT and ACCEPT[w] is None:                       # clitique trop bref pour un verdict sans contexte : à écouter
        print(f"court   {raw:18s} {x['start']:6.2f}s  isolé -> « {heard} »   [pas de verdict automatique : à écouter]"); listen.append(w); continue
    ok = (h in {norm(a_) for a_ in ACCEPT[w]}) if w in ACCEPT else False
    ok = ok or (len(norm(stem)) >= 5 and norm(stem) in h)        # radical assez long : il doit être entendu en entier
    if not ok and w not in ACCEPT and len(norm(stem)) < 5:       # clitique + mot très bref (n'ont, d'une…) : pas de verdict sûr sans contexte
        if norm(w) in h or norm(stem) in h:
            ok = True
        else:
            print(f"court   {raw:18s} {x['start']:6.2f}s  isolé -> « {heard} »   [mot bref : à écouter, pas de verdict automatique]"); listen.append(w); continue
    # « l'effort » entendu « fort » : le radical « effort » doit y être en entier
    v = REG.get(w, {})
    new = (not v) or v.get("auto") or v.get("mode") in ("glue", "g2p")
    print(f"{'OK     ' if ok else 'SUSPECT'} {raw:18s} {x['start']:6.2f}s  isolé -> « {heard} »" + ("   [à écouter : jamais validé à l'oreille]" if new else ""))
    if not ok:
        bad.append((raw, x["start"]))
    if new:
        listen.append(w)
print(f"\n{len(bad)} mot(s) suspect(s)." + (" À ÉCOUTER par l'utilisateur : " + ", ".join(sorted(set(listen))) if listen else ""))
sys.exit(1 if bad else 0)
