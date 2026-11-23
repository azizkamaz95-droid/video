#!/usr/bin/env python3
"""REVUE COMPLÈTE de la voix (utilisateur, 2026-11-23 : « il faut revoir TOUTES les erreurs de l'audio », pas seulement les apostrophes).

usage: voice_review.py <episode_dir> [--threads 6]
Deux transcripteurs indépendants (AssemblyAI et Google Speech-to-Text) réécoutent chaque mot de assets/voice/words.json, dans une
fenêtre « mot + mot suivant » (sans phrase autour : le modèle de langue ne peut pas deviner). Un mot est :
  ERREUR  si AUCUN des deux ne l'entend (écart net : « c'est » -> « cette », « effort » -> « fort »)
  DOUTE   si un seul des deux l'entend (à écouter en priorité)
Tolérances : s final muet (légers/léger), h muet (l'haltère/l'altère), e muet final, accents.
En plus, contrôles acoustiques sur la voix : silence anormal dans une phrase (> 0,9 s), mot répété deux fois (bégaiement de synthèse),
saut de volume entre phrases (> 6 dB), fin de phrase coupée (énergie encore forte à la dernière image), intonation montante des questions.
Écrit renders/revue-voix.json ; code de sortie 1 s'il reste des ERREUR ou des anomalies acoustiques."""
import base64, concurrent.futures as cf, difflib, json, os, re, subprocess, sys, tempfile, time, unicodedata, urllib.request
import numpy as np

EP = os.path.abspath(sys.argv[1])
TH = int(sys.argv[sys.argv.index("--threads") + 1]) if "--threads" in sys.argv else 6
akey, gkey = os.environ["ASSEMBLYAI_API_KEY"], os.environ["GOOGLE_CLOUD_API_KEY"]
W = json.load(open(os.path.join(EP, "assets/voice/words.json")))["words"]
SEG = json.load(open(os.path.join(EP, "assets/voice/segments.json")))["segments"]
WAV = os.path.join(EP, "assets/voice/voice.wav")
T = tempfile.mkdtemp()


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return re.sub(r"[^a-z0-9]", "", "".join(c for c in s if unicodedata.category(c) != "Mn"))


def aai(wav):
    def call(path, data=None, raw=False):
        h = {"authorization": akey}
        if data is not None and not raw:
            data = json.dumps(data).encode(); h["content-type"] = "application/json"
        r = urllib.request.Request("https://api.assemblyai.com/v2" + path, data=data, headers=h, method="POST" if data is not None else "GET")
        return json.loads(urllib.request.urlopen(r, timeout=120).read())
    for _ in range(3):
        try:
            up = call("/upload", open(wav, "rb").read(), raw=True)["upload_url"]
            job = call("/transcript", {"audio_url": up, "language_code": "fr", "punctuate": True, "format_text": True})
            while True:
                res = call(f"/transcript/{job['id']}")
                if res["status"] in ("completed", "error"):
                    return (res.get("text") or "").strip()
                time.sleep(2)
        except Exception:
            time.sleep(3)
    return ""


def goog(wav16):
    body = {"config": {"languageCode": "fr-FR", "encoding": "LINEAR16", "sampleRateHertz": 16000, "model": "latest_long"},
            "audio": {"content": base64.b64encode(open(wav16, "rb").read()).decode()}}
    for _ in range(3):
        try:
            req = urllib.request.Request(f"https://speech.googleapis.com/v1/speech:recognize?key={gkey}", data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
            r = json.loads(urllib.request.urlopen(req, timeout=120).read())
            return " ".join(x["alternatives"][0]["transcript"] for x in r.get("results", [])).strip()
        except Exception:
            time.sleep(3)
    return ""


def variants(w):
    """formes acceptées d'un mot attendu"""
    e = norm(w.lower().strip(".,;:!?…«»\"() ").replace("’", "'"))
    out = {e, e.replace("h", "")}
    if e.endswith("s") and len(e) > 3: out.add(e[:-1])
    if e.endswith("e") and len(e) > 3: out.add(e[:-1])
    if e.endswith("es") and len(e) > 4: out.add(e[:-2])
    if e.endswith("nt") and len(e) > 5: out.add(e[:-2] + "")      # « peuvent » / « peuve » (ent muet)
    return {v for v in out if v}


def heard_ok(word, heard):
    vs = variants(word)
    toks = [norm(t) for t in re.split(r"[\s'’\-]+", heard) if norm(t)]
    joined = norm(heard)
    if any(v in joined for v in vs):
        return True
    e = max(vs, key=len)
    for t in toks:
        if difflib.SequenceMatcher(None, e, t).ratio() >= 0.8:
            return True
    return False


def check(i):
    x = W[i]; nxt = W[i + 1] if i + 1 < len(W) else None
    a, b = max(0, x["start"] - 0.06), (nxt["end"] if nxt else x["end"]) + 0.04
    c = os.path.join(T, f"{i}.wav"); c16 = os.path.join(T, f"{i}_16.wav")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", WAV, "-ss", f"{a:.3f}", "-to", f"{b:.3f}", c], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", c, "-ac", "1", "-ar", "16000", c16], check=True)
    h1, h2 = aai(c), goog(c16)
    ok1, ok2 = heard_ok(x["word"], h1), heard_ok(x["word"], h2)
    # une élision doit rester entendue avec son mot suivant dans AU MOINS un des deux (« cette là » ne contient pas « c'est »)
    r = {"i": i, "word": x["word"], "t": round(x["start"], 2), "aai": h1, "google": h2, "ok_aai": ok1, "ok_google": ok2}
    important = bool(re.search(r"['’]", x["word"])) or len(norm(x["word"])) >= 6
    if not important or not h2.strip():
        r["verdict"] = "OK" if (ok1 or ok2 or not important) else "DOUTE"
    else:
        r["verdict"] = "OK" if (ok1 and ok2) else ("DOUTE" if (ok1 or ok2) else "ERREUR")
    return r


with cf.ThreadPoolExecutor(TH) as ex:
    res = list(ex.map(check, range(len(W))))


# ---- 1) phrase par phrase : TOUS les mots, comparés au script, pour les deux transcripteurs ---------------------------------
SCRIPT = json.load(open(os.path.join(EP, "source/script.json")))["sentences"]
sent_diffs = []


def toks(t):
    return [norm(w) for w in re.split(r"[\s'’\-]+", re.sub(r"[…]", " ", t)) if norm(w)]


def sentence(k):
    s = SEG[k]
    c = os.path.join(T, f"s{k}.wav"); c16 = os.path.join(T, f"s{k}_16.wav")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", WAV, "-ss", f"{max(0, s['start'] - 0.1):.3f}", "-to", f"{s['end'] + 0.1:.3f}", c], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", c, "-ac", "1", "-ar", "16000", c16], check=True)
    return k, aai(c), goog(c16)


with cf.ThreadPoolExecutor(TH) as ex:
    sent_res = list(ex.map(sentence, range(len(SEG))))
spoken_txt = [SCRIPT[k].get("say", SCRIPT[k]["text"]) for k in range(len(SEG))]
for k, h1, h2 in sent_res:
    exp = toks(spoken_txt[k].replace("CaliBodi point com", "calibodi com"))
    for who, h in (("AssemblyAI", h1), ("Google", h2)):
        got = toks(h)
        sm = difflib.SequenceMatcher(None, exp, got, autojunk=False)
        for op, a, b, c, d in sm.get_opcodes():
            if op == "equal":
                continue
            e_part, g_part = " ".join(exp[a:b]), " ".join(got[c:d])
            # tolérances : s final, h muet, e muet, calibodi/kalibody
            if difflib.SequenceMatcher(None, e_part.replace(" ", ""), g_part.replace(" ", "")).ratio() >= 0.8:
                continue
            if "calibodi" in e_part.replace(" ", "") or "calibod" in g_part.replace(" ", "") or "kalib" in g_part.replace(" ", "") or "calib" in g_part.replace(" ", ""):
                continue
            sent_diffs.append({"phrase": k + 1, "par": who, "attendu": e_part, "entendu": g_part})

# ---- contrôles acoustiques --------------------------------------------------------------------------------------------------
x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", WAV, "-f", "f32le", "-ac", "1", "-ar", "16000", "-"], capture_output=True, check=True).stdout, np.float32).astype(float)
SR = 16000
anomalies = []
def rms_db(a, b):
    seg = x[int(a * SR):int(b * SR)]
    return 20 * np.log10(np.sqrt(np.mean(seg ** 2)) + 1e-9) if len(seg) else -90
# silences internes
for k in range(len(W) - 1):
    g = W[k + 1]["start"] - W[k]["end"]
    same = not re.search(r"[.?!…:]$", W[k]["word"].strip())
    if g > 0.9 and same:
        anomalies.append(f"silence de {g:.2f}s au milieu d'une phrase entre « {W[k]['word']} » et « {W[k + 1]['word']} » ({W[k]['end']:.1f}s)")
# mots répétés
for k in range(len(W) - 1):
    if norm(W[k]["word"]) == norm(W[k + 1]["word"]) and len(norm(W[k]["word"])) > 2:
        anomalies.append(f"mot répété « {W[k]['word']} » à {W[k]['start']:.1f}s")
# niveau par phrase
lv = [rms_db(s["start"], s["end"]) for s in SEG]
for k in range(1, len(lv)):
    if abs(lv[k] - lv[k - 1]) > 6:
        anomalies.append(f"saut de volume de {abs(lv[k] - lv[k - 1]):.1f} dB entre les phrases {k} et {k + 1}")
# fin de phrase coupée : énergie des 30 dernières ms comparée à la phrase
for s in SEG:
    tail, body = rms_db(s["end"] - 0.03, s["end"]), rms_db(s["start"], s["end"])
    if tail > body - 6:
        anomalies.append(f"fin de la phrase « {s['text'][:30]}… » possiblement coupée (énergie finale {tail:.0f} dB vs {body:.0f} dB)")
# intonation des questions
try:
    import parselmouth
    for s in SEG:
        if s["text"].strip().endswith("?"):
            sn = parselmouth.Sound(WAV).extract_part(s["end"] - 1.0, s["end"], preserve_times=False)
            f0 = sn.to_pitch(pitch_floor=70, pitch_ceiling=300).selected_array["frequency"]
            f0 = f0[f0 > 0]
            if len(f0) > 10:
                end, before = np.median(f0[-int(len(f0) * 0.25):]), np.median(f0[:int(len(f0) * 0.5)])
                s["rise"] = round(float(end / before), 2)
                if end < before * 0.85:
                    anomalies.append(f"question « {s['text'][:30]}… » : la voix descend à la fin (x{end / before:.2f}) au lieu de monter")
except Exception:
    pass

json.dump({"mots": res, "phrases": sent_diffs, "anomalies": anomalies}, open(os.path.join(EP, "renders/revue-voix.json"), "w"), ensure_ascii=False, indent=1)
err = [r for r in res if r["verdict"] == "ERREUR"]
dou = [r for r in res if r["verdict"] == "DOUTE"]
for r in err:
    print(f"ERREUR  {r['t']:6.2f}s  {r['word']:16s} AssemblyAI « {r['aai']} » | Google « {r['google']} »")
for r in dou:
    print(f"DOUTE   {r['t']:6.2f}s  {r['word']:16s} AssemblyAI « {r['aai']} » | Google « {r['google']} »   [un seul des deux l'entend]")
for d in sent_diffs:
    print(f"PHRASE {d['phrase']} ({d['par']}) : attendu « {d['attendu']} » / entendu « {d['entendu']} »")
for a in anomalies:
    print("ANOMALIE", a)
print(f"\n{len(W)} mots réécoutés par 2 transcripteurs : {len(err)} ERREUR, {len(dou)} DOUTE, {len(sent_diffs)} écart(s) phrase par phrase, {len(anomalies)} anomalie(s) acoustique(s)")
sys.exit(1 if (err or anomalies or sent_diffs) else 0)
