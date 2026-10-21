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
W, H, D = 1080, 1920, 68.62
words = json.load(open(os.path.join(EP, "assets/voice/words.json")))
WORDS = words["words"]

BG = "#2B59C3"          # Cobalt (episodes rotate Soleil / Cobalt / Corail)
INK = "#FFFFFF"         # caption colour on the background
DARK = "#141414"
YEL = "#FFC93C"

SCENES = [
    ("f01-hook", 0.00, 1.80), ("f02-age", 1.80, 6.00), ("f03-etude", 6.00, 9.05), ("f04-foule", 9.05, 10.80),
    ("f05-monde", 10.80, 13.75), ("f06-courbe", 13.75, 17.95), ("f07-corps", 17.95, 21.95), ("f08-soixante", 21.95, 24.80),
    ("f09-lent", 24.80, 27.95), ("f10-rapide", 27.95, 31.05), ("f11-bebes", 31.05, 35.95), ("f12-quarante", 35.95, 39.85),
    ("f13-vie", 39.85, 45.30), ("f14-bonne", 45.30, 47.95), ("f15-tips", 47.95, 52.45), ("f16-app", 52.45, 55.85),
    ("f17-cta", 55.85, 68.62),
]

# Calix sticker (bottom-left): (time, pose); None = drops out of frame
POSES = [
    (0.20, "pointe"), (1.86, "explique"), (3.25, "choc"), (5.09, "non"), (6.11, "explique"), (9.15, "choc"), (10.91, "curieux"),
    (13.80, "explique"), (17.42, "pouce"), (18.12, "explique"), (22.07, "sceptique"), (23.41, "non"), (26.14, "explique"),
    (28.08, "curieux"), (31.11, "choc"), (33.20, "pointe"), (36.02, "sceptique"), (37.13, "choc"), (38.49, "non"),
    (40.74, "explique"), (41.62, "fatigue"), (42.50, "nutrition"), (43.38, "non"), (45.39, "pouce"), (47.09, "biceps"),
    (48.04, "un"), (49.67, "deux"), (51.73, "trois"), (52.66, "app"), (55.98, "pouce"), (58.39, "pointe"), (61.86, "explique"),
    (65.69, "biceps"),
]

# camera punch-ins on the whole picture (time, scale): a quick push in, then a slow release
PUNCH = [(1.30, 1.08), (3.30, 1.05), (4.17, 1.05), (5.09, 1.06), (9.95, 1.06), (10.91, 1.04), (17.42, 1.08), (26.14, 1.06),
         (31.11, 1.08), (33.20, 1.06), (37.13, 1.06), (39.00, 1.05), (47.09, 1.07), (48.04, 1.04), (49.67, 1.04), (51.73, 1.04),
         (56.19, 1.05), (61.17, 1.06), (66.82, 1.06)]

# full-frame colour cuts: (start, end, background, caption colour)
CUTS = [(45.30, 47.95, "#FFC93C", "#141414", "#FFFFFF")]   # (start, end, background, caption colour, keyword box)

# giant ghost words drifting behind each section (the background is never empty nor still)
MARQUEE = [(0.0, 6.0, "MÉTABOLISME"), (6.0, 13.75, "ÉTUDE 2021"), (13.75, 27.95, "20 – 60 ANS"), (27.95, 35.95, "BÉBÉS"),
           (35.95, 45.30, "40 ANS ?"), (47.95, 55.85, "BOUGE · MUSCU · CALORIES"), (55.85, D, "CALIBODI")]

# caption keywords get a marker box
KW = {"ça", "trente", "quarante", "cinquante", "2021", "calories", "6", "400", "29", "95", "plate", "autant", "60", "doucement",
      "07", "bébés", "50", "40", "probablement", "muscle", "contrôles", "marche", "muscu", "calibodi", "like", "partage", "l'âge",
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
    rows = [(40, 1, 55), (680, -1, 70), (1320, 1, 85)]
    # one set of rows for the whole video; a single proxy tween drives word, drift and fades (seek-safe: pure function of t)
    for k, (top, d, v) in enumerate(rows):
        body.append(f'        <div class="mq" id="mq{k}" style="top:{top}px" aria-hidden="true" data-layout-allow-overflow></div>')
    secs = json.dumps([[a, b, ("  " + w + "  ·") * 10] for a, b, w in MARQUEE], ensure_ascii=False)
    rws = json.dumps([[d, v] for _, d, v in rows])
    js.append(f'const MQ={secs},RW={rws},mq=[0,1,2].map(k=>document.getElementById("mq"+k)),mp={{t:0}};')
    js.append('const mqUpd=()=>{const t=mp.t;const s=MQ.find(x=>t>=x[0]&&t<x[1]);'
              'mq.forEach((el,k)=>{if(!s){el.style.opacity=0;return;}if(el.dataset.w!==s[2]){el.textContent=s[2];el.dataset.w=s[2];}'
              'const o=Math.max(0,Math.min(1,(t-s[0])/0.2,(s[1]-t)/0.12));el.style.opacity=o;'
              'el.style.transform="translateX("+(-2600+RW[k][0]*RW[k][1]*t).toFixed(1)+"px)";});};')
    js.append(f'tl.fromTo(mp,{{t:0}},{{t:{D},duration:{D},ease:"none",onUpdate:mqUpd}},0);mqUpd();')
    for i, (a, b, col, *_) in enumerate(CUTS):
        body.append(f'        <div class="cut" id="bg-c{i}" style="background:{col}"></div>')
        js.append(f'tl.fromTo("#bg-c{i}",{{opacity:0}},{{opacity:1,duration:.04,ease:"none",immediateRender:false}},{r(a)});')
        js.append(f'tl.fromTo("#bg-c{i}",{{opacity:1}},{{opacity:0,duration:.04,ease:"none",immediateRender:false}},{r(b - 0.04)});')
    style = """        .cut { position:absolute; inset:0; opacity:0; }
        .mq { position:absolute; left:0; white-space:pre; font-family:"Montserrat",sans-serif; font-weight:900; font-size:300px; line-height:1;
              letter-spacing:-.04em; color:rgba(255,255,255,.075); opacity:0; }"""
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
    for a, b, _, col, box in CUTS:
        js.append(f'tl.fromTo("#capwrap",{{color:"{INK}"}},{{color:"{col}",duration:.02,ease:"none",immediateRender:false}},{r(a)});')
        js.append(f'tl.fromTo("#capwrap",{{color:"{col}"}},{{color:"{INK}",duration:.02,ease:"none",immediateRender:false}},{r(b - 0.04)});')
        js.append(f'tl.fromTo(".kw > i",{{backgroundColor:"{YEL}"}},{{backgroundColor:"{box}",duration:.02,ease:"none",immediateRender:false}},{r(a)});')
        js.append(f'tl.fromTo(".kw > i",{{backgroundColor:"{box}"}},{{backgroundColor:"{YEL}",duration:.02,ease:"none",immediateRender:false}},{r(b - 0.04)});')
        js.append(f'tl.fromTo("#capwrap p",{{textShadow:"0 3px 14px rgba(0,0,0,.35)"}},{{textShadow:"0 0 0 rgba(0,0,0,0)",duration:.02,ease:"none",immediateRender:false}},{r(a)});')
        js.append(f'tl.fromTo("#capwrap p",{{textShadow:"0 0 0 rgba(0,0,0,0)"}},{{textShadow:"0 3px 14px rgba(0,0,0,.35)",duration:.02,ease:"none",immediateRender:false}},{r(b - 0.04)});')
    style = f"""
        #capwrap {{ position:absolute; inset:0; color:{INK}; }}
        .cg {{ position:absolute; left:70px; width:940px; top:1150px; height:150px; display:flex; align-items:center; justify-content:center; opacity:0; }}
        .cg p {{ display:block; width:100%; text-align:center; font-family:"Montserrat",sans-serif; font-weight:800; font-size:60px; line-height:1.1; letter-spacing:-.02em; text-shadow:0 3px 14px rgba(0,0,0,.35); }}
        .cw {{ display:inline-block; margin:0 .12em; opacity:.38; position:relative; }}
        .kw {{ padding:0 .12em; }}
        .kw > i {{ position:absolute; left:0; right:0; top:.08em; bottom:.02em; background:{YEL}; border-radius:.1em; transform-origin:0% 50%; transform:scaleX(0); }}
        .kw > b {{ position:relative; font-weight:800; color:{DARK}; text-shadow:none; }}
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
        js.append(f'tl.fromTo("#cam",{{scale:{s}}},{{scale:1,duration:.68,ease:"power2.inOut",immediateRender:false}},{r(t + 0.12)});')
    return f"""<!doctype html>
<html lang="fr" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <title>Calix #4 — Ton métabolisme ne ralentit pas à 40 ans</title>
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
