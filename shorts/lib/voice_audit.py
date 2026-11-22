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
    a, b = max(0, x["start"] - 0.03), x["end"] + 0.03
    if re.search(r"['’]", exp) and "-" not in exp and i + 1 < len(W):      # élision : on garde le mot suivant pour que « N était » soit visible
        b = W[i + 1]["end"] + 0.03
    c = os.path.join(T, f"{i}.wav")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", WAV, "-ss", f"{a:.3f}", "-to", f"{b:.3f}", c], check=True)
    heard = asr(c)
    h = heard.lower()
    r = {"i": i, "word": raw, "t": round(x["start"], 2), "dur": round(x["end"] - x["start"], 2), "heard": heard}
    clit = re.split(r"['’]", exp, maxsplit=1)[0] if re.search(r"['’]", exp) and len(re.split(r"['’]", exp, maxsplit=1)[0]) <= 2 else None
    if clit and re.match(rf"^\W*{re.escape(clit)}\s+[a-zàâäéèêëîïôöùûüœ]", h) and not re.match(rf"^\W*{re.escape(clit)}['’]", h):
        r["flag"] = "LETTRE"; return r
    e, hh = norm(exp), norm(heard)
    if b > x["end"] + 0.1:                                  # token + mot suivant
        e = norm(exp) + norm(W[i + 1]["word"].lower().strip(".,;:!?…«»\"() "))
    if not e:
        return r
    ratio = difflib.SequenceMatcher(None, e, hh).ratio()
    contains = e in hh
    r["ratio"] = round(ratio, 2)
    short = len(e) < 4 or r["dur"] < 0.12
    if not contains and ratio < MINR:
        r["flag"] = "COURT" if short else "ECART"
    return r


with cf.ThreadPoolExecutor(TH) as ex:
    res = list(ex.map(check, range(len(W))))
json.dump(res, open(os.path.join(EP, "renders/audit-voix.json"), "w"), ensure_ascii=False, indent=1)
bad = [r for r in res if r.get("flag") in ("LETTRE", "ECART")]
short = [r for r in res if r.get("flag") == "COURT"]
for r in bad:
    print(f"{r['flag']:7s} {r['t']:6.2f}s  {r['word']:18s} -> « {r['heard']} »")
print(f"\n{len(W)} mots réécoutés : {len(bad)} à corriger, {len(short)} mots brefs douteux (sans verdict sûr)" + (": " + ", ".join(f"{r['word']}@{r['t']}" for r in short) if short else ""))
sys.exit(1 if bad else 0)
