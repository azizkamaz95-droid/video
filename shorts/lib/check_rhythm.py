#!/usr/bin/env python3
"""Contrôle du rythme d'un montage (règle : rien ne reste plus de ~3 s sans qu'un nouvel élément apparaisse à l'écran).

usage: check_rhythm.py <episode_dir> [--max 3.0]
Lit shots.py (plans + dates des éléments qui apparaissent), les recale sur la voix actuelle comme build_v4.py, et signale
les trous (durée sans nouvel élément) trop longs, ainsi que les plans trop longs. Ne modifie rien."""
import bisect, json, os, re, sys

EP = os.path.abspath(sys.argv[1])
MAX = float(sys.argv[sys.argv.index("--max") + 1]) if "--max" in sys.argv else 3.0
words = json.load(open(os.path.join(EP, "assets/voice/words.json")))
FULL = round(words["duration"] + 0.7, 2)
ns = {"D": FULL}
exec(open(os.path.join(EP, "shots.py")).read(), ns)
SHOTS = ns["SHOTS"]
old = os.path.join(EP, "source/segments-v1.json")
if os.path.exists(old):
    o = json.load(open(old)); n = json.load(open(os.path.join(EP, "assets/voice/segments.json")))
    pairs = [(0.0, 0.0)]
    for a, b in zip(o["segments"], n["segments"]):
        pairs += [(a["start"], b["start"]), (a["end"], b["end"])]
    pairs.append((o["duration"] + 0.7, FULL))
    xs, ys = [], []
    for x, y in pairs:
        if not xs or (x > xs[-1] and y >= ys[-1]):
            xs.append(x); ys.append(y)

    def T(t):
        i = min(max(bisect.bisect_right(xs, t) - 1, 0), len(xs) - 2)
        return ys[i] + (t - xs[i]) * (ys[i + 1] - ys[i]) / (xs[i + 1] - xs[i])
else:
    T = lambda t: t
bad, total = [], 0
for sid, clip, a, b, tr, h, c, j in SHOTS:
    a, b = T(a), (FULL if b == ns["D"] else T(b))
    cues = sorted({T(float(x)) for x in re.findall(r"at\(([\d.]+)\)", j)})
    pts = [a] + [x for x in cues if a <= x <= b] + [b]
    gaps = [(pts[i + 1] - pts[i], pts[i]) for i in range(len(pts) - 1)]
    g, t0 = max(gaps)
    total += 1
    if g > MAX:
        bad.append((sid, clip, round(t0, 1), round(g, 1), round(b - a, 1)))
print(f"{os.path.basename(EP)} : {total} plans, durée {FULL:.1f} s, seuil {MAX} s")
if not bad:
    print("OK : aucun trou plus long que le seuil.")
for sid, clip, t0, g, dur in bad:
    print(f"  ! plan {sid} ({clip}) : {g} s sans nouvel élément à partir de {t0} s (plan de {dur} s) -> ajouter un mot clé, un chiffre ou un zoom")
