#!/usr/bin/env python3
"""Build the persistent layers of the v2 short: index.html, bg, calix, captions, fx.

Scenes (compositions/scenes/*.html) are hand-authored; this script wires them in and generates
everything that is driven by data (voice timings, pose list, section colors, cut list).
"""
import json
import math
import os
import re
import unicodedata

EP = os.path.dirname(os.path.abspath(__file__))
W, H, D = 1080, 1920, 62.0
words = json.load(open(os.path.join(EP, "assets/voice/words.json")))
WORDS = words["words"]

SCENES = [
    ("f01-hook", 0.00, 2.95), ("f02-faux", 2.95, 3.84), ("f03-trempe", 3.84, 8.40), ("f04-pourquoi", 8.40, 9.60),
    ("f05-refroidissement", 9.60, 14.33), ("f06-sueur", 14.33, 18.10), ("f07-balance", 18.10, 21.45),
    ("f08-eau", 21.45, 23.30), ("f09-different", 23.30, 26.45), ("f10-rehydrate", 26.45, 30.10),
    ("f11-eviter", 30.10, 36.45), ("f12-deshydratation", 36.45, 38.62), ("f13-cles", 38.62, 46.25),
    ("f14-bienvenue", 46.25, 53.50), ("f15-cta", 53.50, 62.00),
]

# section colors for the background glows: (start, palette)
SECTIONS = [(0.0, "heat"), (2.95, "red"), (3.84, "water"), (8.40, "heat"), (9.60, "water"), (18.10, "heat"),
            (21.45, "water"), (30.10, "red"), (38.62, "green"), (46.25, "brand")]

# Calix: (time, pose). None = leaves the frame (slides down); next pose after None slides back up.
POSES = [
    (0.30, "sceptique"), (2.98, "non"), (3.86, "explique"), (6.67, "choc"), (8.45, "curieux"), (9.45, None),
    (18.15, "curieux"), (20.13, "pointe"), (21.50, "explique"), (23.34, "enerve"), (24.86, "non"), (26.50, "hydratation"),
    (28.95, "pouce"), (30.18, "explique"), (31.12, "non"), (33.08, "choc"), (35.30, "enerve"), (36.50, "fatigue"),
    (38.67, "explique"), (40.52, "pointe"), (41.74, "un"), (42.94, "deux"), (44.32, "trois"), (46.38, "pouce"),
    (48.40, "app"), (50.80, "biceps"), (51.76, "nutrition"), (53.54, "pouce"), (55.98, "pointe"), (57.10, "app"),
    (59.62, "biceps"),
]

SHAKES = [(2.98, 16), (24.86, 10), (37.55, 8)]
FLASH = [(2.95, "red"), (8.40, "white"), (9.60, "white"), (21.45, "white"), (30.10, "white"), (38.62, "white"), (46.25, "white")]
STREAK = [3.84, 14.33, 18.10, 23.30, 26.45, 36.45, 53.50]
GLITCH = [2.98, 37.55]

COL = {"heat": "#FF6B35", "red": "#FF2D55", "water": "#00D4FF", "green": "#00FF87"}
KW = {
    "#FF6B35": ["graisse", "transpires", "transpirer", "température", "chaleur", "chauds", "excessive", "calibodi", "force"],
    "#FF2D55": ["faux", "attention", "déshydrater", "mythe", "abonne-toi"],
    "#00D4FF": ["trempé", "eau", "d'eau", "sueur", "refroidissement", "réhydrates", "transpiration"],
    "#00FF87": ["durablement", "alimentation", "activité", "physique", "régularité", "utiles", "vérifiés", "partage"],
}


def r(x):
    return round(x, 3)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def norm(w):
    w = unicodedata.normalize("NFC", w.lower())
    return re.sub(r"[^\w'’-]", "", w)


KWMAP = {k: c for c, ks in KW.items() for k in ks}


def kw_color(w):
    n = norm(w)
    return KWMAP.get(n) or KWMAP.get(n.rstrip("s"))


class Rand:  # small deterministic PRNG (mulberry32 in python)
    def __init__(self, seed):
        self.a = seed & 0xFFFFFFFF

    def __call__(self):
        self.a = (self.a + 0x6D2B79F5) & 0xFFFFFFFF
        t = self.a
        t = ((t ^ (t >> 15)) * (t | 1)) & 0xFFFFFFFF
        t ^= (t + (((t ^ (t >> 7)) * (t | 61)) & 0xFFFFFFFF)) & 0xFFFFFFFF
        return ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296


def sub_file(cid, style, body, js):
    return f"""<!doctype html>
<html lang="fr">
  <head><meta charset="UTF-8" /></head>
  <body>
    <template>
      <link rel="stylesheet" href="assets/style/kit.css" />
      <style>
        #root {{ position: absolute; inset: 0; overflow: hidden; }}
{style}
      </style>
      <div id="root" data-composition-id="{cid}" data-width="{W}" data-height="{H}" data-duration="{D}">
{body}
      </div>
      <script>
        (function () {{
          const tl = gsap.timeline({{ paused: true }});
{js}
          window.__timelines["{cid}"] = tl;
        }})();
      </script>
    </template>
  </body>
</html>
"""


# ------------------------------------------------------------------ background world
def build_bg():
    rnd = Rand(7)
    parts, pjs = [], []
    for i in range(34):
        x, y = rnd() * 1180 - 50, rnd() * 2100 - 100
        z = -700 + rnd() * 900
        s = 4 + rnd() * 9
        rise = 260 + rnd() * 420
        drift = (rnd() - 0.5) * 160
        a = 0.25 + rnd() * 0.45
        parts.append(f'<i class="pt" id="bg-p{i}" style="width:{s:.1f}px;height:{s:.1f}px;opacity:{a:.2f}"></i>')
        pjs.append(f'tl.fromTo("#bg-p{i}",{{x:{x:.0f},y:{y:.0f},z:{z:.0f}}},{{x:{x + drift:.0f},y:{y - rise:.0f},z:{z:.0f},duration:{D},ease:"none"}},0);')
    glows = []
    for name, c in COL.items():
        glows.append(f'<div class="glow-set" id="bg-{name}"{' style="opacity:1"' if name == SECTIONS[0][1] else ''}><b class="g1" style="background:radial-gradient(closest-side,{c}55,{c}00)"></b>'
                     f'<b class="g2" style="background:radial-gradient(closest-side,{c}40,{c}00)"></b></div>')
    # brand = heat + red + water together
    js = list(pjs)
    js.append(f'tl.fromTo("#bg-floor",{{backgroundPosition:"0px 0px"}},{{backgroundPosition:"0px {int(D * 150)}px",duration:{D},ease:"none"}},0);')
    for name in COL:
        js.append(f'tl.fromTo("#bg-{name} .g1",{{x:-60,y:-40}},{{x:80,y:60,duration:7,ease:"sine.inOut",yoyo:true,repeat:{int(D // 7) - 1}}},0);')
        js.append(f'tl.fromTo("#bg-{name} .g2",{{x:50,y:30}},{{x:-70,y:-50,duration:9,ease:"sine.inOut",yoyo:true,repeat:{int(D // 9) - 1}}},0);')
    # section crossfades
    on = {n: 0.0 for n in COL}
    on[SECTIONS[0][1]] = 1.0  # first section is lit from CSS
    for i, (t, pal) in enumerate(SECTIONS):
        if t == 0:
            continue
        want = {"heat": 0, "red": 0, "water": 0, "green": 0}
        if pal == "brand":
            want.update(heat=0.75, red=0.45, water=0.45)
        else:
            want[pal] = 1.0
            if pal == "red":
                want["heat"] = 0.35
        for n in COL:
            if want[n] != on[n]:
                js.append(f'tl.fromTo("#bg-{n}",{{opacity:{on[n]}}},{{opacity:{want[n]},duration:.45,ease:"power1.inOut",immediateRender:false}},{r(t - 0.15)});')
                on[n] = want[n]
    style = """
        #bg { position:absolute; inset:0; background:#0A0A0F; perspective:1200px; perspective-origin:50% 38%; }
        #bg-floor { position:absolute; left:-760px; top:900px; width:2600px; height:2400px; transform-origin:50% 0%;
          transform: rotateX(76deg);
          background-image: linear-gradient(rgba(244,241,236,.13) 3px, transparent 3px), linear-gradient(90deg, rgba(244,241,236,.13) 3px, transparent 3px);
          background-size: 150px 150px;
          -webkit-mask-image: linear-gradient(to bottom, transparent 0%, #000 22%, #000 70%, transparent 100%);
          mask-image: linear-gradient(to bottom, transparent 0%, #000 22%, #000 70%, transparent 100%); }
        #bg-horizon { position:absolute; left:0; right:0; top:840px; height:260px; background: radial-gradient(50% 50% at 50% 50%, rgba(244,241,236,.10), rgba(244,241,236,0)); }
        .glow-set { position:absolute; inset:0; opacity:0; }
        .glow-set b { position:absolute; display:block; border-radius:50%; }
        .glow-set .g1 { left:-260px; top:120px; width:1100px; height:1100px; }
        .glow-set .g2 { left:380px; top:820px; width:1200px; height:1200px; }
        #bg-parts { position:absolute; left:0; top:0; width:1080px; height:1920px; }
        .pt { position:absolute; left:0; top:0; display:block; border-radius:50%; background:#F4F1EC; box-shadow:0 0 14px rgba(255,190,150,.8); }
"""
    body = f"""        <div id="bg">
          <div class="glow-set-wrap">{''.join(glows)}</div>
          <div id="bg-horizon"></div>
          <div id="bg-floor"></div>
          <div id="bg-parts" class="p3d">{''.join(parts)}</div>
        </div>"""
    return sub_file("bg", style, body, "\n".join("          " + j for j in js))


# ------------------------------------------------------------------ Calix sticker
def build_calix():
    poses = sorted({p for _, p in POSES if p})
    imgs = "".join(f'<img class="pose" id="cx-{p}" src="assets/calix/calix-{p}.png" alt="" />' for p in poses)
    js = []
    cur, visible, flip = None, False, 0
    for t, p in POSES:
        if p is None:
            js.append(f'tl.fromTo("#cx-pos",{{y:0,rotation:-2}},{{y:760,rotation:6,duration:.38,ease:"power3.in",immediateRender:false}},{r(t)});')
            visible = False
            continue
        if not visible:
            if cur:
                js.append(f'tl.set("#cx-{cur}",{{opacity:0}},{r(t - 0.01)});')
            js.append(f'tl.set("#cx-{p}",{{opacity:1}},{r(t - 0.01)});')
            js.append(f'tl.fromTo("#cx-pos",{{y:760,rotation:7}},{{y:0,rotation:-2,duration:.55,ease:"back.out(1.5)",immediateRender:{"true" if t < 0.5 else "false"}}},{r(t - 0.05)});')
            visible = True
        else:
            # alternate a sticker flip (3D) and a slap pop so swaps never feel mechanical
            if flip % 2 == 0:
                js.append(f'tl.fromTo("#cx-flip",{{rotationY:0}},{{rotationY:90,duration:.08,ease:"power2.in",immediateRender:false}},{r(t - 0.08)});')
                js.append(f'tl.set("#cx-{cur}",{{opacity:0}},{r(t)});tl.set("#cx-{p}",{{opacity:1}},{r(t)});')
                js.append(f'tl.fromTo("#cx-flip",{{rotationY:-90}},{{rotationY:0,duration:.22,ease:"back.out(2)",immediateRender:false}},{r(t)});')
            else:
                js.append(f'tl.set("#cx-{cur}",{{opacity:0}},{r(t)});tl.set("#cx-{p}",{{opacity:1}},{r(t)});')
                js.append(f'tl.fromTo("#cx-pop",{{scale:.9,rotation:-4}},{{scale:1,rotation:0,duration:.3,ease:"back.out(2.6)",immediateRender:false}},{r(t)});')
            flip += 1
        cur = p
    style = """
        #cx-pos { position:absolute; left:-30px; top:1290px; width:740px; height:740px; transform-origin:50% 100%; perspective:900px; }
        #cx-flip, #cx-pop { position:absolute; inset:0; transform-origin:50% 60%; }
        #cx-flip { transform-style:preserve-3d; }
        .pose { position:absolute; inset:0; width:100%; height:100%; opacity:0; }
"""
    body = f'        <div id="cx-pos" data-layout-allow-overflow><div id="cx-flip"><div id="cx-pop">{imgs}</div></div></div>'
    return sub_file("calix", style, body, "\n".join("          " + j for j in js))


# ------------------------------------------------------------------ captions
def build_captions():
    groups, cur = [], []
    for i, w in enumerate(WORDS):
        cur.append(w)
        nxt = WORDS[i + 1] if i + 1 < len(WORDS) else None
        chars = sum(len(x["word"]) + 1 for x in cur)
        gap = (nxt["start"] - w["end"]) if nxt else 0
        punct = w["word"][-1] in ",.?:!…"
        if not nxt or punct or len(cur) >= 3 or chars >= 15 or gap > 0.25 or (nxt and chars + len(nxt["word"]) > 18):
            groups.append(cur)
            cur = []
    html, js = [], []
    for g, grp in enumerate(groups):
        t0 = grp[0]["start"] - 0.03
        t1 = groups[g + 1][0]["start"] - 0.03 if g + 1 < len(groups) else D - 0.1
        t1 = min(t1, grp[-1]["end"] + 0.9)
        spans = []
        for w in grp:
            c = kw_color(w["word"])
            cls = f' class="kw" style="color:{c}"' if c else ""
            spans.append(f'<span id="cw{w["i"]}"{cls}>{esc(w["word"])}</span>')
        html.append(f'<div class="cg" id="cg{g}"><p>{"".join(spans)}</p></div>')
        js.append(f'tl.set("#cg{g}",{{opacity:1}},{r(t0)});tl.fromTo("#cg{g}",{{y:16,scale:.92}},{{y:0,scale:1,duration:.16,ease:"back.out(2.2)",immediateRender:false}},{r(t0)});tl.set("#cg{g}",{{opacity:0}},{r(t1)});')
        for w in grp:
            js.append(f'tl.fromTo("#cw{w["i"]}",{{opacity:.45}},{{opacity:1,duration:.05,ease:"none",immediateRender:false}},{r(w["start"])});')
            if kw_color(w["word"]):
                js.append(f'tl.fromTo("#cw{w["i"]}",{{scale:1}},{{scale:1.14,duration:.06,ease:"power2.out",immediateRender:false}},{r(w["start"])});')
                js.append(f'tl.fromTo("#cw{w["i"]}",{{scale:1.14}},{{scale:1,duration:.2,ease:"back.out(2)",immediateRender:false}},{r(w["start"] + 0.06)});')
    style = """
        .cg { position:absolute; left:50px; width:860px; top:1128px; height:170px; display:flex; align-items:center; justify-content:center; opacity:0; }
        .cg p { display:block; width:100%; text-align:center; font-family:"Montserrat",sans-serif; font-weight:900; font-size:62px; line-height:1.05;
                letter-spacing:-.02em; color:#F4F1EC;
                text-shadow: 0 5px 0 #0A0A0F, 0 -2px 0 #0A0A0F, 3px 0 0 #0A0A0F, -3px 0 0 #0A0A0F, 0 0 30px rgba(0,0,0,.9); }
        .cg span { display:inline-block; margin:0 .13em; opacity:.45; }
"""
    return sub_file("captions", style, "\n".join("        " + h for h in html), "\n".join("          " + j for j in js)), len(groups)


# ------------------------------------------------------------------ fx (grain, vignette, cut accents)
def build_fx():
    js = []
    # grain: deterministic jump every 1/12 s from the frame index
    js.append(f'const gp={{f:0}};tl.fromTo(gp,{{f:0}},{{f:{int(D * 12)},duration:{D},ease:"none",onUpdate:()=>{{const k=Math.floor(gp.f);'
              f'const a=(k*7919)%512,b=(k*104729)%512;document.getElementById("fx-grain").style.backgroundPosition=a+"px "+b+"px";}}}},0);')
    body = ['<div id="fx-grain"></div>', '<div id="fx-vig"></div>']
    for i, (t, c) in enumerate(FLASH):
        body.append(f'<div class="fl fl-{c}" id="fx-f{i}"></div>')
        js.append(f'tl.fromTo("#fx-f{i}",{{opacity:{0.85 if c == "red" else 0.6}}},{{opacity:0,duration:{0.3 if c == "red" else 0.18},ease:"power2.out",immediateRender:false}},{r(t)});')
    for i, t in enumerate(STREAK):
        body.append(f'<div class="st" id="fx-s{i}"></div>')
        js.append(f'tl.fromTo("#fx-s{i}",{{x:-1500,opacity:1}},{{x:1700,opacity:1,duration:.32,ease:"power2.inOut",immediateRender:false}},{r(t - 0.16)});')
        js.append(f'tl.set("#fx-s{i}",{{opacity:0}},{r(t + 0.17)});')
    rnd = Rand(11)
    for i, t in enumerate(GLITCH):
        for k in range(6):
            y, h = int(rnd() * 1700) + 100, int(20 + rnd() * 90)
            body.append(f'<div class="gb" id="fx-g{i}-{k}" style="top:{y}px;height:{h}px"></div>')
            dx = int((rnd() - 0.5) * 220)
            t0 = t + k * 0.025
            js.append(f'tl.fromTo("#fx-g{i}-{k}",{{opacity:.9,x:{dx}}},{{opacity:0,x:{-dx},duration:.09,ease:"steps(3)",immediateRender:false}},{r(t0)});')
    style = """
        #fx-grain { position:absolute; inset:0; background:url(assets/fx/grain.png) repeat; background-size:512px 512px; opacity:.16; mix-blend-mode:overlay; }
        #fx-vig { position:absolute; inset:0; background: radial-gradient(120% 90% at 50% 45%, rgba(0,0,0,0) 55%, rgba(0,0,0,.55) 100%); }
        .fl { position:absolute; inset:0; opacity:0; }
        .fl-white { background:#F4F1EC; mix-blend-mode:screen; }
        .fl-red { background: radial-gradient(70% 60% at 50% 40%, rgba(255,45,85,.95), rgba(120,0,25,.9)); mix-blend-mode:screen; }
        .st { position:absolute; left:0; top:-300px; width:520px; height:2600px; opacity:0; transform-origin:50% 50%;
              background: linear-gradient(90deg, rgba(255,255,255,0), rgba(255,236,220,.55) 45%, rgba(255,255,255,.9) 50%, rgba(255,236,220,.55) 55%, rgba(255,255,255,0));
              mix-blend-mode:screen; rotate:14deg; }
        .gb { position:absolute; left:-60px; width:1200px; opacity:0; mix-blend-mode:screen;
              background: linear-gradient(90deg, rgba(255,45,85,.0), rgba(255,45,85,.55) 30%, rgba(0,212,255,.55) 60%, rgba(0,212,255,0)); }
"""
    return sub_file("fx", style, "\n".join("        " + b for b in body), "\n".join("          " + j for j in js))


# ------------------------------------------------------------------ index
def build_index():
    hosts = [f'<div id="el-bg" data-composition-id="bg" data-composition-src="compositions/bg.html" data-start="0" data-duration="{D}" data-track-index="0" data-track-kind="graphics" data-width="{W}" data-height="{H}"></div>']
    for k, (sid, a, b) in enumerate(SCENES):
        hosts.append(f'<div id="el-{sid}" data-composition-id="{sid}" data-composition-src="compositions/scenes/{sid}.html" data-start="{a}" '
                     f'data-duration="{r(b - a)}" data-track-index="{1 + k % 2}" data-track-kind="graphics" data-width="{W}" data-height="{H}"></div>')
    hosts.append(f'<div id="el-calix" data-composition-id="calix" data-composition-src="compositions/calix.html" data-start="0" data-duration="{D}" data-track-index="3" data-track-kind="graphics" data-width="{W}" data-height="{H}"></div>')
    aud = [f'<audio id="voice" src="assets/voice/voice.wav" data-start="0" data-duration="{words["duration"]}" data-track-index="10" data-volume="1"></audio>']
    for n, ti in (("music", 11), ("sfx", 12)):
        if os.path.exists(os.path.join(EP, f"assets/audio/{n}.wav")):
            aud.append(f'<audio id="{n}" src="assets/audio/{n}.wav" data-start="0" data-duration="{D}" data-track-index="{ti}" data-volume="1"></audio>')
    js = []
    for t, amp in SHAKES:
        seq = [(1, -0.6), (-0.8, 0.9), (0.7, -0.5), (-0.5, 0.6), (0.4, -0.3), (-0.25, 0.2), (0.12, -0.1), (0, 0)]
        prev = (0, 0)
        for k, (dx, dy) in enumerate(seq):
            js.append(f'tl.fromTo("#shake",{{x:{prev[0] * amp:.1f},y:{prev[1] * amp:.1f}}},{{x:{dx * amp:.1f},y:{dy * amp:.1f},duration:.035,ease:"none",immediateRender:false}},{r(t + k * 0.035)});')
            prev = (dx, dy)
    return f"""<!doctype html>
<html lang="fr" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <title>Calix #1 v2 — Transpirer fait-il perdre de la graisse ?</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <link rel="stylesheet" href="assets/style/kit.css" />
    <style>
      * {{ margin:0; padding:0; box-sizing:border-box; }}
      html, body {{ width:{W}px; height:{H}px; overflow:hidden; background:#0A0A0F; }}
      #root {{ position:relative; width:100%; height:100%; overflow:hidden; background:#0A0A0F; }}
      #shake {{ position:absolute; inset:0; }}
      [data-composition-id="main"] div[data-composition-src] {{ position:absolute; inset:0; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{D}" data-width="{W}" data-height="{H}">
      <div id="shake">
        {(chr(10) + "        ").join(hosts)}
      </div>
      <div id="el-captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{D}" data-track-index="4" data-track-kind="captions" data-width="{W}" data-height="{H}"></div>
      <div id="el-fx" data-composition-id="fx" data-composition-src="compositions/fx.html" data-start="0" data-duration="{D}" data-track-index="5" data-track-kind="graphics" data-width="{W}" data-height="{H}"></div>
      {(chr(10) + "      ").join(aud)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      {(chr(10) + "      ").join(js)}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""


os.makedirs(os.path.join(EP, "compositions/scenes"), exist_ok=True)
open(os.path.join(EP, "compositions/bg.html"), "w").write(build_bg())
open(os.path.join(EP, "compositions/calix.html"), "w").write(build_calix())
cap, ng = build_captions()
open(os.path.join(EP, "compositions/captions.html"), "w").write(cap)
open(os.path.join(EP, "compositions/fx.html"), "w").write(build_fx())
open(os.path.join(EP, "index.html"), "w").write(build_index())
missing = [s for s, _, _ in SCENES if not os.path.exists(os.path.join(EP, f"compositions/scenes/{s}.html"))]
print(f"built index + bg + calix + captions ({ng} groups) + fx · {len(SCENES)} scenes wired · missing: {missing}")
