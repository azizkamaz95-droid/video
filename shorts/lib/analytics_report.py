#!/usr/bin/env python3
"""Rapport de performance : classe les vidéos par multiple de la médiane et par taux d'interaction.
usage: analytics_report.py raw/tiktok-AAAA-MM-JJ.json [--min-jours 2]
Les relevés bruts viennent de Metricool (je les tire et les enregistre dans shorts/analytics/raw/). Ne compare que les vidéos
publiées depuis au moins N jours (les vues d'une vidéo récente ne sont pas terminées)."""
import json, statistics as st, sys, datetime as dt

raw = json.load(open(sys.argv[1]))
relevé = dt.date.fromisoformat(raw["source"].split("relevé du ")[1][:10])
mj = int(sys.argv[sys.argv.index("--min-jours") + 1]) if "--min-jours" in sys.argv else 2
V = [dict(zip(raw["champs"], v)) for v in raw["videos"]]
mature = [v for v in V if (relevé - dt.date.fromisoformat(v["publie"])).days >= mj]
med = st.median(v["vues"] for v in mature)
print(f"{raw['source']} · {len(V)} vidéos ({len(mature)} avec au moins {mj} jours) · médiane des vues : {med:.0f}")
print(f"{'multiple':>8} {'vues':>5} {'interact.':>9}  vidéo")
for v in sorted(mature, key=lambda v: -v["vues"]):
    inter = v["likes"] + v["commentaires"] + v["partages"]
    print(f"{v['vues'] / med:7.2f}x {v['vues']:5d} {100 * inter / max(v['vues'], 1):8.1f}%  {v['publie']} {v['titre']}")
vals = [v["vues"] / med for v in mature]
print(f"\nÉcart : de {min(vals):.2f}x à {max(vals):.2f}x la médiane.")
if max(vals) < 1.5:
    print("Aucune vidéo ne dépasse 1,5x la médiane : plateau. Le sujet ne change pas la diffusion, il faut agir sur ce qui décide de la diffusion (accroche, rétention, partages, compte).")
rec = [v for v in V if v not in mature]
if rec:
    print("Trop récentes pour juger : " + ", ".join(f"{v['titre']} ({v['vues']} vues)" for v in rec))
