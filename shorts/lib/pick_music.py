#!/usr/bin/env python3
"""Choisit la musique de fond d'une vidéo en alternant les pistes de shorts/music/catalog.json.

usage: pick_music.py <episode_dir> --energy <1-5> [--set <nom>] [--dry]
Règle : l'énergie de la musique suit le sujet (1 très calme … 5 dramatique, voir PLAYBOOK §8). On garde les pistes à
±1 niveau de l'énergie demandée (l'écart le plus faible d'abord), jamais celle des deux dernières vidéos, puis la
piste utilisée le moins récemment (jamais utilisée = prioritaire). Copie le mp3 dans <episode>/assets/music/, met à jour plan.json (music_file, music_loop) et
enregistre le choix dans music/history.json (à committer).
"""
import json, os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
MUS = os.path.join(HERE, "..", "music")
EP = os.path.abspath(sys.argv[1])
force = sys.argv[sys.argv.index("--set") + 1] if "--set" in sys.argv else None
dry = "--dry" in sys.argv
cat = {t["name"]: t for t in json.load(open(os.path.join(MUS, "catalog.json")))["tracks"]}
hist = json.load(open(os.path.join(MUS, "history.json")))
used = [n for _, n in hist["used"]]
if force:
    name = force
else:
    if "--energy" not in sys.argv:
        sys.exit("indique l'énergie du sujet : --energy 1..5 (voir PLAYBOOK §8)")
    target = int(sys.argv[sys.argv.index("--energy") + 1])
    last = {n: max([i for i, u in enumerate(used) if u == n], default=-1) for n in cat}
    banned = set(used[-2:])
    cands = [n for n in cat if n not in banned and abs(cat[n]["energy"] - target) <= 1]
    if not cands:                                  # nothing close and fresh: take the closest energy not just used
        cands = [n for n in cat if n not in banned] or list(cat)
    name = min(cands, key=lambda n: (abs(cat[n]["energy"] - target), last[n], list(cat).index(n)))
t = cat[name]
print(f"musique choisie : {name} (énergie {t['energy']}, {t['mood']}) · boucle {t['loop']} · {t['source']}")
if dry:
    sys.exit()
os.makedirs(os.path.join(EP, "assets/music"), exist_ok=True)
shutil.copy(os.path.join(MUS, t["file"]), os.path.join(EP, "assets/music", t["file"]))
plan = json.load(open(os.path.join(EP, "plan.json")))
plan["music_file"] = "assets/music/" + t["file"]
plan["music_loop"] = t["loop"]
plan.setdefault("music_lufs", -25.0)
json.dump(plan, open(os.path.join(EP, "plan.json"), "w"), indent=1, ensure_ascii=False)
ep = os.path.basename(EP)
hist["used"] = [u for u in hist["used"] if u[0] != ep] + [[ep, name]]
json.dump(hist, open(os.path.join(MUS, "history.json"), "w"), indent=1, ensure_ascii=False)
