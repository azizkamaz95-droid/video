#!/usr/bin/env python3
"""Build the persistent layers of a v3 short ("human editor" look): index.html, bg, calix, captions, fx.

v3 = flat background colour (one per episode), ink typography (Montserrat + Caveat handwriting), paper cards,
marker highlights, hand-drawn strokes, camera punch-ins. Scenes (compositions/scenes/*.html) are hand-authored;
this script wires them and generates everything driven by data (voice timings, poses, colour cuts, punches).
"""
import json
import os
import re
import unicodedata

EP = os.path.dirname(os.path.abspath(__file__))
W, H, D = 1080, 1920, 74.0
words = json.load(open(os.path.join(EP, "assets/voice/words.json")))
WORDS = words["words"]

BG = "#FFC93C"          # Soleil (episodes rotate Soleil / Cobalt / Corail)
INK = "#141414"

SCENES = [
    ("f01-hook", 0.00, 4.30), ("f02-milliers", 4.30, 7.20), ("f03-etude", 7.20, 12.32), ("f04-total", 12.32, 15.22),
    ("f05-zones", 15.22, 24.28), ("f06-taille", 24.28, 26.70), ("f07-fou", 26.70, 27.80), ("f08-jambe", 27.80, 36.94),
    ("f09-bras", 36.94, 40.42), ("f10-partout", 40.42, 45.74), ("f11-meta", 45.74, 50.86), ("f12-abdos", 50.86, 54.52),
    ("f13-solution", 54.52, 60.48), ("f14-app", 60.48, 63.74), ("f15-cta", 63.74, 74.00),
]

# Calix sticker (bottom-left): (time, pose); None = drops out of frame
POSES = [
    (0.20, "pointe"), (1.85, None), (6.00, "pointe"), (7.35, "explique"), (13.95, "choc"), (15.37, "curieux"),
    (22.09, "explique"), (24.52, "sceptique"), (25.64, "non"), (26.66, None), (27.89, "explique"), (33.57, "sceptique"),
    (35.28, "non"), (37.03, "curieux"), (39.62, "choc"), (40.56, "explique"), (45.95, "pointe"), (48.75, "non"),
    (51.08, "biceps"), (52.68, "non"), (54.69, "curieux"), (56.87, "nutrition"), (58.30, "biceps"), (59.68, "endormi"),
    (60.10, "abdos"), (61.43, "app"), (63.92, "pouce"), (65.77, "pointe"), (67.87, "explique"), (70.99, "biceps"),
]

# camera punch-ins on the whole picture (time, scale): a quick push in, then a slow release
PUNCH = [(1.30, 1.09), (2.99, 1.05), (5.15, 1.05), (13.98, 1.10), (18.56, 1.05), (26.03, 1.06), (35.28, 1.05),
         (39.84, 1.12), (43.21, 1.05), (47.54, 1.05), (53.90, 1.06), (59.91, 1.06), (64.13, 1.05), (70.99, 1.06)]

# full-frame colour cuts: (start, end, background, caption colour)
CUTS = [(26.70, 27.80, "#141414", "#FFFFFF"), (39.60, 40.42, "#2B59C3", "#FFFFFF")]

# caption keywords get a marker box
KW = {"ça", "fondre", "milliers", "prouver", "treize", "5", "004", "fesses", "autant", "bougé", "fou", "seule", "aucun",
      "bras", "partout", "forces", "confirme", "fort", "apparaître", "déficit", "sommeil", "calibodi", "like", "partage",
      "abonne-toi", "force"}


def r(x):
    return round(x, 3)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def norm(w):
    w = unicodedata.normalize("NFC", w.lower())
    return re.sub(r"[^\w'’-]", "", w)


def sub_file(cid, style, body, js):
    fonts = open(os.path.join(EP, "assets/style/fonts-inline.css")).read().strip()
    return f"""<!doctype html>
<html lang="fr">
  <head><meta charset="UTF-8" /></head>
  <body>
    <template>
      <style>
{fonts}
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


# ------------------------------------------------------------------ background: flat colour + colour cuts
def build_bg():
    body = [f'        <div id="bg-base" style="position:absolute;inset:0;background:{BG}"></div>']
    js = []
    for i, (a, b, col, _) in enumerate(CUTS):
        body.append(f'        <div class="cut" id="bg-c{i}" style="background:{col}"></div>')
        js.append(f'tl.fromTo("#bg-c{i}",{{opacity:0}},{{opacity:1,duration:.04,ease:"none",immediateRender:false}},{r(a)});')
        js.append(f'tl.fromTo("#bg-c{i}",{{opacity:1}},{{opacity:0,duration:.04,ease:"none",immediateRender:false}},{r(b - 0.04)});')
    style = "        .cut { position:absolute; inset:0; opacity:0; }"
    return sub_file("bg", style, "\n".join(body), "\n".join("          " + j for j in js))


# ------------------------------------------------------------------ Calix sticker (jump-cut swaps, no 3D flips)
def build_calix():
    poses = sorted({p for _, p in POSES if p})
    imgs = "".join(f'<img class="pose" id="cx-{p}" src="assets/calix/calix-{p}.png" alt="" />' for p in poses)
    js, cur, visible, k = [], None, False, 0
    for t, p in POSES:
        if p is None:
            js.append(f'tl.fromTo("#cx-pos",{{y:0,rotation:-3}},{{y:820,rotation:8,duration:.3,ease:"power3.in",immediateRender:false}},{r(t)});')
            visible = False
            continue
        if not visible:
            if cur:
                js.append(f'tl.set("#cx-{cur}",{{opacity:0}},{r(t - 0.01)});')
            js.append(f'tl.set("#cx-{p}",{{opacity:1}},{r(t - 0.01)});')
            js.append(f'tl.fromTo("#cx-pos",{{y:820,rotation:10}},{{y:0,rotation:-3,duration:.42,ease:"back.out(1.6)",immediateRender:{"true" if t < 0.5 else "false"}}},{r(t - 0.04)});')
            visible = True
        else:
            rot = -6 if k % 2 == 0 else 5
            js.append(f'tl.set("#cx-{cur}",{{opacity:0}},{r(t)});tl.set("#cx-{p}",{{opacity:1}},{r(t)});')
            js.append(f'tl.fromTo("#cx-pop",{{scale:1.1,rotation:{rot}}},{{scale:1,rotation:0,duration:.28,ease:"back.out(2.4)",immediateRender:false}},{r(t)});')
            k += 1
        cur = p
    style = """
        #cx-pos { position:absolute; left:-40px; top:1286px; width:740px; height:740px; transform-origin:50% 100%; }
        #cx-pop { position:absolute; inset:0; transform-origin:45% 80%; }
        .pose { position:absolute; inset:0; width:100%; height:100%; opacity:0; }
"""
    body = f'        <div id="cx-pos" data-layout-allow-overflow><div id="cx-pop">{imgs}</div></div>'
    return sub_file("calix", style, body, "\n".join("          " + j for j in js))


# ------------------------------------------------------------------ captions (CapCut-like: ink words, marker on keywords)
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
            if norm(w["word"]) in KW:
                spans.append(f'<span class="cw kw" id="cw{w["i"]}"><i></i><b>{esc(w["word"])}</b></span>')
            else:
                spans.append(f'<span class="cw" id="cw{w["i"]}">{esc(w["word"])}</span>')
        html.append(f'<div class="cg" id="cg{g}"><p>{"".join(spans)}</p></div>')
        js.append(f'tl.set("#cg{g}",{{opacity:1}},{r(t0)});tl.fromTo("#cg{g}",{{y:18,scale:.94}},{{y:0,scale:1,duration:.14,ease:"back.out(2.4)",immediateRender:false}},{r(t0)});tl.set("#cg{g}",{{opacity:0}},{r(t1)});')
        for w in grp:
            js.append(f'tl.fromTo("#cw{w["i"]}",{{opacity:.38}},{{opacity:1,duration:.05,ease:"none",immediateRender:false}},{r(w["start"])});')
            if norm(w["word"]) in KW:
                js.append(f'tl.fromTo("#cw{w["i"]} > i",{{scaleX:0}},{{scaleX:1,duration:.16,ease:"power2.out",immediateRender:false}},{r(w["start"])});')
                js.append(f'tl.fromTo("#cw{w["i"]}",{{scale:1}},{{scale:1.12,duration:.07,ease:"power2.out",immediateRender:false}},{r(w["start"])});')
                js.append(f'tl.fromTo("#cw{w["i"]}",{{scale:1.12}},{{scale:1,duration:.2,ease:"back.out(2)",immediateRender:false}},{r(w["start"] + 0.07)});')
    for a, b, _, col in CUTS:
        js.append(f'tl.fromTo("#capwrap",{{color:"{INK}"}},{{color:"{col}",duration:.02,ease:"none",immediateRender:false}},{r(a)});')
        js.append(f'tl.fromTo("#capwrap",{{color:"{col}"}},{{color:"{INK}",duration:.02,ease:"none",immediateRender:false}},{r(b - 0.04)});')
    style = f"""
        #capwrap {{ position:absolute; inset:0; color:{INK}; }}
        .cg {{ position:absolute; left:70px; width:940px; top:1150px; height:150px; display:flex; align-items:center; justify-content:center; opacity:0; }}
        .cg p {{ display:block; width:100%; text-align:center; font-family:"Montserrat",sans-serif; font-weight:800; font-size:60px; line-height:1.1; letter-spacing:-.02em; }}
        .cw {{ display:inline-block; margin:0 .12em; opacity:.38; position:relative; }}
        .kw {{ padding:0 .12em; }}
        .kw > i {{ position:absolute; left:0; right:0; top:.08em; bottom:.02em; background:#FFFFFF; border-radius:.1em; transform-origin:0% 50%; transform:scaleX(0); }}
        .kw > b {{ position:relative; font-weight:800; color:{INK}; }}
"""
    body = '        <div id="capwrap">' + "".join(html) + "</div>"
    return sub_file("captions", style, body, "\n".join("          " + j for j in js)), len(groups)


# ------------------------------------------------------------------ fx: paper grain
def build_fx():
    js = [f'const gp={{f:0}};tl.fromTo(gp,{{f:0}},{{f:{int(D * 12)},duration:{D},ease:"none",onUpdate:()=>{{const k=Math.floor(gp.f);'
          f'const a=(k*7919)%512,b=(k*104729)%512;document.getElementById("fx-grain").style.backgroundPosition=a+"px "+b+"px";}}}},0);']
    style = "        #fx-grain { position:absolute; inset:0; background:url(assets/fx/grain.png) repeat; background-size:512px 512px; opacity:.09; mix-blend-mode:multiply; }"
    return sub_file("fx", style, '        <div id="fx-grain"></div>', "\n".join("          " + j for j in js))


# ------------------------------------------------------------------ index
def build_index():
    fonts = open(os.path.join(EP, "assets/style/fonts-inline.css")).read()
    hosts = []
    for k, (sid, a, b) in enumerate(SCENES):
        if not os.path.exists(os.path.join(EP, f"compositions/scenes/{sid}.html")):
            continue  # scene not written yet (work in progress)
        hosts.append(f'<div id="el-{sid}" data-composition-id="{sid}" data-composition-src="compositions/scenes/{sid}.html" data-start="{a}" '
                     f'data-duration="{r(b - a)}" data-track-index="{1 + k % 2}" data-track-kind="graphics" data-width="{W}" data-height="{H}"></div>')
    hosts.append(f'<div id="el-calix" data-composition-id="calix" data-composition-src="compositions/calix.html" data-start="0" data-duration="{D}" data-track-index="3" data-track-kind="graphics" data-width="{W}" data-height="{H}"></div>')
    aud = [f'<audio id="voice" src="assets/voice/voice.wav" data-start="0" data-duration="{words["duration"]}" data-track-index="10" data-volume="1"></audio>']
    for n, ti in (("music", 11), ("sfx", 12)):
        if os.path.exists(os.path.join(EP, f"assets/audio/{n}.wav")):
            aud.append(f'<audio id="{n}" src="assets/audio/{n}.wav" data-start="0" data-duration="{D}" data-track-index="{ti}" data-volume="1"></audio>')
    js = []
    for t, s in PUNCH:
        js.append(f'tl.fromTo("#cam",{{scale:1}},{{scale:{s},duration:.11,ease:"power2.out",immediateRender:false}},{r(t - 0.03)});')
        js.append(f'tl.fromTo("#cam",{{scale:{s}}},{{scale:1,duration:.75,ease:"power2.inOut",immediateRender:false}},{r(t + 0.12)});')
    return f"""<!doctype html>
<html lang="fr" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <title>Calix #3 — Les abdos ne font pas fondre ton ventre</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <script src="assets/style/kit3.js"></script>
    <link rel="stylesheet" href="assets/style/kit3.css" />
    <style>
{fonts}
      * {{ margin:0; padding:0; box-sizing:border-box; }}
      html, body {{ width:{W}px; height:{H}px; overflow:hidden; background:{BG}; }}
      #root {{ position:relative; width:100%; height:100%; overflow:hidden; background:{BG}; }}
      #cam {{ position:absolute; inset:0; transform-origin:50% 42%; }}
      [data-composition-id="main"] div[data-composition-src] {{ position:absolute; inset:0; }}
      .hf-font-a {{ font-family:"Montserrat"; font-weight:900; }} .hf-font-b {{ font-family:"Caveat"; font-weight:700; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{D}" data-width="{W}" data-height="{H}">
      <div id="el-bg" data-composition-id="bg" data-composition-src="compositions/bg.html" data-start="0" data-duration="{D}" data-track-index="0" data-track-kind="graphics" data-width="{W}" data-height="{H}"></div>
      <div id="cam">
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


# every scene carries the @font-face block inline (the linter and the render compiler read inline styles only)
def inject_fonts():
    fonts = open(os.path.join(EP, "assets/style/fonts-inline.css")).read().strip()
    block = "/* fonts:begin */\n" + fonts + "\n/* fonts:end */"
    for sid, _, _ in SCENES:
        f = os.path.join(EP, f"compositions/scenes/{sid}.html")
        if not os.path.exists(f):
            continue
        s = open(f).read()
        if "/* fonts:begin */" in s:
            s = re.sub(r"/\* fonts:begin \*/.*?/\* fonts:end \*/", lambda m: block, s, flags=re.S)
        else:
            s = s.replace("<style>\n", "<style>\n" + block + "\n", 1)
        open(f, "w").write(s)


inject_fonts()
open(os.path.join(EP, "compositions/bg.html"), "w").write(build_bg())
open(os.path.join(EP, "compositions/calix.html"), "w").write(build_calix())
cap, ng = build_captions()
open(os.path.join(EP, "compositions/captions.html"), "w").write(cap)
open(os.path.join(EP, "compositions/fx.html"), "w").write(build_fx())
open(os.path.join(EP, "index.html"), "w").write(build_index())
missing = [s for s, _, _ in SCENES if not os.path.exists(os.path.join(EP, f"compositions/scenes/{s}.html"))]
print(f"built index + bg + calix + captions ({ng} groups) + fx · {len(SCENES)} scenes wired · missing: {missing}")
