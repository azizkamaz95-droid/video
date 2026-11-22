#!/usr/bin/env python3
"""Choisit, PAR TEST OBJECTIF, la façon de faire dire chaque élision d'un script (utilisateur, 2026-11-22 : « n'était » lu « N, était »).

usage: elision_select.py <episode_dir> [--force] [--reps 3]
Pour chaque mot à apostrophe du script (n'était, l'effort, t'en, c'est-à-dire…) qui n'a pas été validé à l'oreille, teste dans SA phrase :
  - « collé » : apostrophe supprimée, accents gardés (n'était -> nétait ; l'effort -> leffort)
  - « ipa »   : prononciation calculée par espeak (lib/g2p.py) imposée à la voix (n'était -> netɛ)
Chaque variante est synthétisée --reps fois (la voix varie d'une prise à l'autre), le mot est découpé dans la voix et retranscrit SEUL
(sans contexte, le modèle de langue ne peut pas corriger). Une prise est FAUSSE si :
  - la lettre est lue seule (« N était », « D énergie ») : c'est l'erreur que l'utilisateur répète depuis des semaines ;
  - le radical n'est pas entendu en entier (« l'effort » entendu « fort ») ;
  - (cas listés dans word_check.ACCEPT) la lecture n'est pas l'une de celles attendues (« t'en » entendu « Tenez »).
La variante qui réussit le plus de prises est enregistrée dans voice_validated.json (respell = collé, ou ipa) avec "tested".
Moins de 2 prises sur 3 réussies : le mot est signalé « À ÉCOUTER ». Les mots validés à l'oreille par l'utilisateur ne sont jamais touchés."""
import base64, json, os, re, subprocess, sys, tempfile, time, unicodedata, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import g2p

EP = os.path.abspath(sys.argv[1])
FORCE = "--force" in sys.argv
REPS = int(sys.argv[sys.argv.index("--reps") + 1]) if "--reps" in sys.argv else 3
key, akey = os.environ["GOOGLE_CLOUD_API_KEY"], os.environ["ASSEMBLYAI_API_KEY"]
S = json.load(open(os.path.join(EP, "source/script.json")))
REGP = os.path.join(HERE, "voice_validated.json")
REG = json.load(open(REGP))
VAL = REG["tokens"]
ACCEPT = {"t'en": ["tant", "t'en", "temps", "tan", "tend"]}
ELI = re.compile(r"^(?:[cdjlmnst]|qu|jusqu|lorsqu|puisqu)['’][a-zàâäéèêëîïôöùûüœ]+$", re.I)
CLITIC = re.compile(r"^(?:[cdjlmnst]|qu|jusqu|lorsqu|puisqu)$", re.I)


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return re.sub(r"[^a-z]", "", "".join(c for c in s if unicodedata.category(c) != "Mn"))


def tts(text, pron=None):
    inp, ver = {"text": text}, "v1"
    if pron:
        inp["customPronunciations"] = {"pronunciations": pron}; ver = "v1beta1"
    body = {"input": inp, "voice": {"languageCode": "fr-FR", "name": S["voice"]}, "audioConfig": {"audioEncoding": "LINEAR16", "sampleRateHertz": 24000}}
    req = urllib.request.Request(f"https://texttospeech.googleapis.com/{ver}/text:synthesize?key={key}", data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    return base64.b64decode(json.loads(urllib.request.urlopen(req).read())["audioContent"])


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
            return res
        time.sleep(2)


def other_glue(text, keep):
    """le reste de la phrase : les autres élisions sont collées (contexte neutre)"""
    def f(m):
        w = m.group(0)
        return w if w.lower() == keep.lower() else w.replace("'", "", 1)
    return re.sub(r"\b(?:[cdjlmnst]|[Qq]u|[Jj]usqu|[Ll]orsqu|[Pp]uisqu)'[\wàâäéèêëîïôöùûüœ]+", f, text)


def one_take(sentence, tok, variant, pron):
    """retourne (ok, entendu)"""
    words = sentence.replace("’", "'").split()
    idx = next(i for i, w in enumerate(words) if w.strip(".,;:!?…").lower() == tok.lower())
    prev_w = norm(words[idx - 1]) if idx > 0 else None
    next_w = norm(words[idx + 1]) if idx + 1 < len(words) else None
    text = other_glue(sentence.replace("’", "'"), tok)
    text = re.sub(re.escape(tok), variant, text, count=1, flags=re.I)
    T = tempfile.mkdtemp(); f = os.path.join(T, "x.wav"); open(f, "wb").write(tts(text, pron))
    aw = asr(f)["words"]
    nw = [norm(w["text"]) for w in aw]
    a = 0.0
    b = None
    if prev_w:
        j = next((k for k, x in enumerate(nw) if x == prev_w), None)
        if j is None:
            return None, "(mot précédent introuvable)"
        a = aw[j]["end"] / 1000 - 0.02
    if next_w:
        j2 = next((k for k, x in enumerate(nw) if x == next_w and aw[k]["start"] / 1000 >= a), None)
        if j2 is None:
            return None, "(mot suivant introuvable)"
        b = aw[j2]["start"] / 1000 + 0.02
    c = os.path.join(T, "c.wav")
    # le mot ET le suivant : avec le mot suivant, le transcripteur rend « N était pas » (lettre lue seule) ou « n'était pas » (correct)
    j3 = next((k for k, x in enumerate(nw) if x == next_w and aw[k]["start"] / 1000 >= a), None) if next_w else None
    b = (aw[j3]["end"] / 1000 + 0.03) if j3 is not None else None
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", f, "-ss", str(max(0, a))] + (["-to", str(b)] if b else []) + [c]
    subprocess.run(cmd, check=True)
    heard = (asr(c).get("text") or "").strip()
    clit, stem = re.split(r"['’]", tok.lower(), maxsplit=1)
    h = heard.lower()
    letter_read = bool(re.match(rf"^\W*{re.escape(clit)}\s+[a-zàâäéèêëîïôöùûüœ]", h)) and not re.match(rf"^\W*{re.escape(clit)}['’]", h)
    if letter_read:
        return False, heard
    first = norm(heard.split()[0]) if heard.split() else ""
    if tok.lower() in ACCEPT:
        return first in {norm(x) for x in ACCEPT[tok.lower()]}, heard
    expected = norm(clit + stem) + (next_w or "")
    import difflib
    ratio = difflib.SequenceMatcher(None, expected, norm(heard)).ratio()
    return ratio >= 0.8, heard


todo = {}
for s in S["sentences"]:
    t = s.get("say", s["text"]).replace("’", "'")
    for w in re.findall(r"[\wÀ-ÿœ]+'[\wÀ-ÿœ]+", t):
        wl = w.lower()
        v = VAL.get(wl)
        if not ELI.match(w) or "-" in w:
            continue
        if v and not v.get("auto") and not FORCE:      # validé à l'oreille par l'utilisateur : on n'y touche pas
            continue
        if v and v.get("tested") and not FORCE:
            continue
        todo.setdefault(wl, (w, t))
print(f"{len(todo)} élision(s) à tester :", ", ".join(todo))
bad = []
for wl, (w, sent) in todo.items():
    glue = w.replace("'", "", 1)
    ipa = g2p.ipa(w)
    cands = [("collé", glue, None)]
    if ipa:
        cands.append(("ipa", w, [{"phrase": w, "phoneticEncoding": "PHONETIC_ENCODING_IPA", "pronunciation": ipa.replace(" ", "")}]))
    best = None
    for name, variant, pron in cands:
        res = [one_take(sent, w, variant, pron) for _ in range(REPS)]
        okn = sum(1 for ok, _ in res if ok)
        print(f"  {w:14s} {name:6s} {okn}/{REPS}   " + " | ".join(h for _, h in res))
        if best is None or okn > best[0]:
            best = (okn, name, variant, pron)
    okn, name, variant, pron = best
    if name == "collé":
        VAL[wl] = {"mode": "respell", "value": glue, "auto": True, "tested": f"collé {okn}/{REPS}"}
    else:
        VAL[wl] = {"mode": "ipa", "value": pron[0]["pronunciation"], "auto": True, "tested": f"ipa {okn}/{REPS}"}
    print(f"  => {w} : {name} ({okn}/{REPS})" + ("   ⚠ À ÉCOUTER (moins de 2 prises sur 3 réussies)" if okn < 2 else ""))
    if okn < 2:
        bad.append(w)
    json.dump(REG, open(REGP, "w"), ensure_ascii=False, indent=1)
print("à écouter en priorité :", ", ".join(bad) if bad else "aucun")
sys.exit(1 if bad else 0)
