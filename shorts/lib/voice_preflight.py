#!/usr/bin/env python3
"""Contrôle avant génération de la voix : aucun mot à risque non validé à l'oreille.

usage: voice_preflight.py <episode_dir>                 liste les mots à risque et leur statut (code 1 s'il en reste à tester)
       voice_preflight.py <episode_dir> --test          fabrique renders/test-prononciations.mp3 (plusieurs écritures par mot à tester)
       voice_preflight.py --set "c'était=ipa:setɛ"      enregistre le choix validé par l'utilisateur (raw | glue | ipa:<IPA> | respell:<texte>)
Mots à risque : apostrophes (c'est, n'est…), noms avec trait d'union (Manpo-kei), chiffres restés en chiffres. Les noms propres
au milieu d'une phrase sont signalés (à écouter). Le registre est lib/voice_validated.json."""
import base64, json, os, re, subprocess, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REG = os.path.join(HERE, "voice_validated.json")
reg = json.load(open(REG))
if "--set" in sys.argv:
    k, v = sys.argv[sys.argv.index("--set") + 1].split("=", 1)
    mode, _, val = v.partition(":")
    assert mode in ("raw", "glue", "ipa", "respell", "typo"), mode
    reg["tokens"][k.lower()] = {"mode": mode, **({"value": val} if val else {})}
    json.dump(reg, open(REG, "w"), ensure_ascii=False, indent=1)
    print("enregistré :", k.lower(), reg["tokens"][k.lower()])
    sys.exit(0)
EP = os.path.abspath(sys.argv[1])
S = json.load(open(os.path.join(EP, "source/script.json")))
VAL = reg["tokens"]
PRON = {k: v for k, v in json.load(open(os.path.join(HERE, "pronunciations.json"))).items() if not k.startswith("_")}
WORD = r"[\wÀ-ÿœ]"
risky, props, digits = {}, set(), []
for s in S["sentences"]:
    t = s.get("say", s["text"]).replace("’", "'").replace("[pause short]", "")
    if re.search(r"\d", t):
        digits.append(s["id"])
    for w in re.findall(rf"{WORD}+'{WORD}+|[A-ZÀ-Ý]{WORD}*-{WORD}+", t):
        risky.setdefault(w.lower(), s)
    for m in re.finditer(rf"(?<=[a-zà-ÿ,;:] )[A-ZÀ-Ý]{WORD}+", t):
        if m.group(0) not in ("CaliBodi",):
            props.add(m.group(0))
bad = [w for w in risky if w not in VAL]
print(f"{os.path.basename(EP)} : {len(risky)} mot(s) à risque")
for w in sorted(risky):
    v = VAL.get(w)
    print(f"  {'OK ' if v else 'À TESTER'}  {w}" + (f"  ({v['mode']}{' ' + v['value'] if 'value' in v else ''})" if v else ""))
if digits:
    print("  ERREUR : chiffres dans le texte lu (à écrire en toutes lettres) :", ", ".join(digits)); bad.append("chiffres")
if props:
    print("  à écouter (noms propres) :", ", ".join(sorted(props)))
if "--test" in sys.argv and bad:
    import numpy as np
    key = os.environ["GOOGLE_CLOUD_API_KEY"]; SR = 24000

    def tts(text, pron=None):
        inp = {"text": text}
        if pron:
            inp["customPronunciations"] = {"pronunciations": [{"phrase": p, "phoneticEncoding": "PHONETIC_ENCODING_IPA", "pronunciation": i} for p, i in pron]}
        body = {"input": inp, "voice": {"languageCode": "fr-FR", "name": S["voice"]}, "audioConfig": {"audioEncoding": "LINEAR16", "sampleRateHertz": SR}}
        req = urllib.request.Request(f"https://texttospeech.googleapis.com/{'v1beta1' if pron else 'v1'}/text:synthesize?key={key}", data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
        try:
            return np.frombuffer(base64.b64decode(json.loads(urllib.request.urlopen(req).read())["audioContent"])[44:], dtype="<i2").astype(float) / 32768
        except urllib.error.HTTPError:
            return None
    out, menu, gap = [np.zeros(int(0.3 * SR))], [], lambda d: np.zeros(int(d * SR))
    nums = ["un", "deux", "trois", "quatre", "cinq"]
    for n, w in enumerate([w for w in bad if w != "chiffres"], 1):
        s = risky[w]; text = s.get("say", s["text"]).replace("’", "'").replace("[pause short]", "")
        sent = next((x.strip() for x in re.split(r"(?<=[.!?])\\s+", text) if w in x.lower().replace("’", "'")), text)
        variants = [("tel quel", sent, None)]
        ipa = (PRON.get(w) or PRON.get(w.lower()))
        if ipa:
            variants.append((f"IPA {ipa}", sent, [(re.search(re.escape(w), sent, re.I).group(0), ipa)]))
        if "'" in w:
            variants.append(("apostrophe collée", re.sub(re.escape(w), w.replace("'", "", 1), sent, flags=re.I), None))
            variants.append(("apostrophe typographique", re.sub(re.escape(w), w.replace("'", "’"), sent, flags=re.I), None))
        else:
            a, b = w.split("-", 1)
            variants.append(("deux mots", re.sub(re.escape(w), f"{a} {b}", sent, flags=re.I), None))
            variants.append(("collé", re.sub(re.escape(w), a + b, sent, flags=re.I), None))
            variants.append(("IPA manpokei", sent, [(re.search(re.escape(w), sent, re.I).group(0), "mɑ̃pokei")]))
            variants.append(("IPA manpokɛ", sent, [(re.search(re.escape(w), sent, re.I).group(0), "mɑ̃pokɛ")]))
        out += [tts(f"Série {nums[n - 1]}."), gap(0.5)]
        for k, (label, t, pron) in enumerate(variants):
            a = tts(t, pron)
            if a is None:
                continue
            out += [tts(f"Version {nums[k]}."), gap(0.25), a, gap(0.9)]
            menu.append((n, k + 1, w, label))
        out.append(gap(0.7))
    path = os.path.join(EP, "renders/test-prononciations.mp3")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "-", "-b:a", "128k", path],
                   input=(np.clip(np.concatenate([x for x in out if x is not None]), -1, 1) * 32767).astype("<i2").tobytes(), check=True)
    print("\\ntest écrit :", path)
    for m in menu:
        print("  série %d version %d : %s (%s)" % m)
sys.exit(1 if bad else 0)
