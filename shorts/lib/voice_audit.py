#!/usr/bin/env python3
"""Réécoute AUTOMATIQUE de toute la voix, mot à mot (utilisateur, 2026-11-22 : « tu réécoutes tout l'audio »).

usage: voice_audit.py <episode_dir> [--min 0.55] [--threads 8]
Chaque mot de assets/voice/words.json est découpé dans voice.wav (minutage de l'alignement) puis retranscrit SEUL par AssemblyAI : sans
phrase autour, le modèle de langue ne peut plus deviner le bon mot, il rend ce que la voix a vraiment dit. On compare au mot du script.
Signalé :
  LETTRE   une lettre lue seule (« N était », « D énergie »)
  ECART    le mot entendu ressemble trop peu au mot attendu (« l'effort » -> « fort », « t'en » -> « Tenez »)
  COURT    mot de moins de 4 lettres ou de 0,12 s : pas de verdict sûr (listé seulement s'il y a un écart net)
Écrit renders/audit-voix.json et affiche le rapport. Code de sortie 1 s'il reste des LETTRE ou des ECART."""
import concurrent.futures as cf, difflib, json, os, re, subprocess, sys, tempfile, time, unicodedata, urllib.request

EP = os.path.abspath(sys.argv[1])
MINR = float(sys.argv[sys.argv.index("--min") + 1]) if "--min" in sys.argv else 0.55
TH = int(sys.argv[sys.argv.index("--threads") + 1]) if "--threads" in sys.argv else 8
akey = os.environ["ASSEMBLYAI_API_KEY"]
W = json.load(open(os.path.join(EP, "assets/voice/words.json")))["words"]
WAV = os.path.join(EP, "assets/voice/voice.wav")
T = tempfile.mkdtemp()


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return re.sub(r"[^a-z0-9]", "", "".join(c for c in s if unicodedata.category(c) != "Mn"))


def call(path, data=None, raw=False):
    h = {"authorization": akey}
    if data is not None and not raw:
        data = json.dumps(data).encode(); h["content-type"] = "application/json"
    r = urllib.request.Request("https://api.assemblyai.com/v2" + path, data=data, headers=h, method="POST" if data is not None else "GET")
    return json.loads(urllib.request.urlopen(r, timeout=120).read())


def asr(wav):
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
    return "(échec ASR)"


def check(i):
    x = W[i]; raw = x["word"]
    exp = raw.lower().strip(".,;:!?…«»\"() ").replace("’", "'")
    # fenêtre = le mot ET le suivant (un mot isolé de 0,15 s fait « deviner » n'importe quoi au transcripteur : « peuvent » -> « par exemple »)
    nxt = W[i + 1] if i + 1 < len(W) else None
    a, b = max(0, x["start"] - 0.06), (nxt["end"] if nxt else x["end"]) + 0.04
    c = os.path.join(T, f"{i}.wav")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", WAV, "-ss", f"{a:.3f}", "-to", f"{b:.3f}", c], check=True)
    heard = asr(c)
    h = heard.lower()
    r = {"i": i, "word": raw, "t": round(x["start"], 2), "dur": round(x["end"] - x["start"], 2), "heard": heard}
    clit = re.split(r"['’]", exp, maxsplit=1)[0] if re.search(r"['’]", exp) and len(re.split(r"['’]", exp, maxsplit=1)[0]) <= 2 else None
    if clit and re.match(rf"^\W*{re.escape(clit)}\s+[a-zàâäéèêëîïôöùûüœ]", h) and not re.match(rf"^\W*{re.escape(clit)}['’]", h):
        r["flag"] = "LETTRE"; return r
    e, hh = norm(exp), norm(heard)
    if not e:
        return r
    nxt_w = norm(nxt["word"].lower().strip(".,;:!?…«»\"() ")) if nxt else ""
    ratio = difflib.SequenceMatcher(None, e + nxt_w, hh).ratio()
    contains = e in hh or (e.endswith("s") and len(e) > 4 and e[:-1] in hh)       # « légers » / « léger » : le s final ne s'entend pas
    r["ratio"] = round(ratio, 2)
    short = len(e) < 4 or r["dur"] < 0.12
    is_eli = bool(re.search(r"['’]", exp)) and "-" not in exp
    if is_eli:
        # une élision doit être entendue en entier : « c'est là » ne doit pas devenir « cette là » (le ratio seul serait trop indulgent)
        # (h muet : « l'haltère » se dit « l'altère », on compare donc sans les h)
        e0, h0 = e.replace("h", ""), hh.replace("h", "")
        if e0 not in h0 and difflib.SequenceMatcher(None, e0, h0[:len(e0) + 1]).ratio() < 0.85:
            r["flag"] = "ECART"
            r["eli"] = not re.search(r"['’]h", exp)     # « l'haltère » (h muet) : le transcripteur l'écrit « l'alter » ; la fenêtre élargie tranche
    elif not contains and ratio < 0.62:
        r["flag"] = "COURT" if short else "ECART"
    return r


with cf.ThreadPoolExecutor(TH) as ex:
    res = list(ex.map(check, range(len(W))))


def recheck(r):
    """2e chance des mots signalés : fenêtre élargie (mot précédent -> mot suivant). Les écarts dus à un minutage serré disparaissent ;
    ceux qui restent (« l'effort » -> « fort ») sont de vraies erreurs de voix."""
    i = r["i"]
    p = W[i - 1] if i > 0 else None
    n = W[i + 1] if i + 1 < len(W) else None
    a = max(0, (p["start"] if p else W[i]["start"]) - 0.05)
    b = (n["end"] if n else W[i]["end"]) + 0.05
    c = os.path.join(T, f"re{i}.wav")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", WAV, "-ss", f"{a:.3f}", "-to", f"{b:.3f}", c], check=True)
    heard = asr(c)
    e = norm(W[i]["word"].lower().strip(".,;:!?…«»\"() ").replace("’", "'"))
    r["heard_wide"] = heard
    if r.get("eli"):
        return r
    ee = e[:-1] if e.endswith("s") and len(e) > 4 else e
    if e and (e in norm(heard) or ee in norm(heard) or e.replace("h", "") in norm(heard).replace("h", "")):
        r["flag"] = None
    return r


with cf.ThreadPoolExecutor(TH) as ex:
    res = [r if r.get("flag") not in ("ECART",) else r for r in res]
    flagged = [r for r in res if r.get("flag") == "ECART"]
    list(ex.map(recheck, flagged))
json.dump(res, open(os.path.join(EP, "renders/audit-voix.json"), "w"), ensure_ascii=False, indent=1)
bad = [r for r in res if r.get("flag") in ("LETTRE", "ECART")]
short = [r for r in res if r.get("flag") == "COURT"]
for r in bad:
    print(f"{r['flag']:7s} {r['t']:6.2f}s  {r['word']:18s} -> « {r['heard']} »   (fenêtre large : « {r.get('heard_wide', '')} »)")
print(f"\n{len(W)} mots réécoutés : {len(bad)} à corriger, {len(short)} mots brefs douteux (sans verdict sûr)" + (": " + ", ".join(f"{r['word']}@{r['t']}" for r in short) if short else ""))
REG = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "voice_validated.json")))["tokens"]
listen = sorted({re.sub(r"[^\w'’-]", "", x["word"].lower()).replace("’", "'") for x in W
                 if re.search(r"['’]|-", x["word"]) and (not REG.get(re.sub(r"[^\w'’-]", "", x["word"].lower()).replace("’", "'")) or REG[re.sub(r"[^\w'’-]", "", x["word"].lower()).replace("’", "'")].get("auto"))})
print("À ÉCOUTER par l'utilisateur (jamais validés à l'oreille) :", ", ".join(listen) if listen else "aucun")
sys.exit(1 if bad else 0)
