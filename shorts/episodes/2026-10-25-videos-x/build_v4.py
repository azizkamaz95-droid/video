#!/usr/bin/env python3
"""v4 « cinéma » look for a Calix short: full-bleed graded footage, whip / zoom transitions, big centred captions
(one to two words, active word in yellow), a story-style progress bar, Calix always alive (breathing + bob).

usage: build_v4.py [end_seconds]     (end_seconds renders only the opening, e.g. 12.4 for a style test)
Scenes are described in SHOTS below (global times, seconds in the voice). Writes index.html and compositions/*.
"""
import json
import os
import re
import sys
import unicodedata

EP = os.path.dirname(os.path.abspath(__file__))
W, H = 1080, 1920
words = json.load(open(os.path.join(EP, "assets/voice/words.json")))
FULL = round(words["duration"] + 0.7, 2)
D = float(sys.argv[1]) if len(sys.argv) > 1 else FULL
WORDS = [w for w in words["words"] if w["start"] < D - 0.05]
FONTS = open(os.path.join(EP, "assets/style/fonts-inline.css")).read().strip()
YEL, DARK = "#FFC93C", "#141414"

# shots: (id, clip, start, end, transition into the shot, accent html, accent css, accent js)
X = 0.06  # overlap kept on each side of a cut so the transition has two pictures to work with
SHOTS = [
    ("s1", "scroll", 0.00, 2.05, None,
     '<div class="big" id="s1-x">X</div>',
     "#s1-x { left: 0; width: 1080px; top: 300px; text-align: center; font-size: 780px; color: #FFC93C; opacity: .92; text-shadow: 0 30px 80px rgba(0,0,0,.65); }",
     'tl.fromTo("#s1-x",{scale:2.4,opacity:0,rotation:-8},{scale:1,opacity:.92,rotation:0,duration:.22,ease:"power4.out"},at(0.75));'
     'tl.fromTo("#s1-x",{scale:1},{scale:1.08,duration:.8,ease:"none",immediateRender:false},at(0.97));'
     'tl.fromTo("#s1-x",{opacity:.92,filter:"blur(0px)"},{opacity:0,filter:"blur(16px)",duration:.25,ease:"power2.in",immediateRender:false},at(1.55));'),
    ("s2", "chambre", 2.05, 5.05, "whip",
     '<div class="big" id="s2-n">3</div><div class="tag" id="s2-t">FAITS</div>',
     "#s2-n { left: 0; width: 1080px; top: 170px; text-align: center; font-size: 560px; color: #FFC93C; text-shadow: 0 20px 60px rgba(0,0,0,.6); }"
     "#s2-t { left: 0; width: 1080px; top: 720px; text-align: center; font-size: 96px; letter-spacing: .3em; color: #fff; }",
     'tl.fromTo("#s2-n",{scale:3,opacity:0},{scale:1,opacity:1,duration:.25,ease:"power4.out"},at(2.90));'
     'tl.fromTo("#s2-t",{y:60,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(3.14));'
     'tl.fromTo(["#s2-n","#s2-t"],{opacity:1},{opacity:.0,duration:.3,ease:"none",immediateRender:false},at(4.4));'),
    ("s3", "silhouette", 5.05, 8.55, "zoom",
     '<div class="big" id="s3-q">?</div><div class="tag" id="s3-l">N°3</div>',
     "#s3-q { left: 560px; top: 180px; font-size: 520px; color: #FFC93C; text-shadow: 0 20px 60px rgba(0,0,0,.6); }"
     "#s3-l { left: 120px; top: 360px; font-size: 150px; color: #fff; }",
     'tl.fromTo("#s3-l",{x:-200,opacity:0},{x:0,opacity:1,duration:.3,ease:"power3.out"},at(5.31));'
     'tl.fromTo("#s3-q",{scale:0,rotation:-40},{scale:1,rotation:8,duration:.4,ease:"back.out(2.4)"},at(6.11));'
     'tl.fromTo("#s3-q",{rotation:8},{rotation:-6,duration:.5,ease:"sine.inOut",yoyo:true,repeat:2,immediateRender:false},at(6.5));'
     'tl.fromTo(["#s3-q","#s3-l"],{opacity:1},{opacity:0,duration:.2,ease:"none",immediateRender:false},at(7.1));'),
    ("s4", "mains", 8.55, D, "flash",
     '<div class="lab" id="s4-f">FAIT N°1</div>',
     "#s4-f { left: 70px; top: 230px; font-size: 120px; }",
     'tl.fromTo("#s4-f",{scale:2.6,opacity:0,rotation:-6},{scale:1,opacity:1,rotation:-3,duration:.24,ease:"power4.out"},at(8.75));'
     'tl.fromTo("#s4-f",{x:0},{x:-1200,duration:.25,ease:"power3.in",immediateRender:false},at(9.8));'),
]
# camera accents on the whole picture: (time, scale) push-ins + a shake on « contrôle »
PUNCH = [(0.75, 1.07), (1.62, 1.04), (2.90, 1.06), (6.11, 1.05), (7.95, 1.04), (8.75, 1.07), (10.44, 1.08)]
SHAKE = [10.44]
POSES = [(0.20, "choc"), (2.90, "trois"), (5.15, "curieux"), (7.23, "pointe"), (8.75, "un"), (9.96, "explique")]
KW = {"x", "masturbation", "trois", "personne", "surprendre", "bout", "un", "contrôle", "vraiment"}
CHAPTERS = [0.0, 8.75]   # fact starts shown as notches on the progress bar (the full video adds 2 and 3)


def r(x):
    return round(x, 3)


def norm(w):
    return re.sub(r"[^\w'’-]", "", unicodedata.normalize("NFC", w.lower()))


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def sub(cid, dur, style, body, js):
    return f"""<!doctype html>
<html lang="fr">
  <head><meta charset="UTF-8" /></head>
  <body>
    <template>
      <style>
{FONTS}
        #root {{ position: absolute; inset: 0; overflow: hidden; }}
{style}
      </style>
      <div id="root" data-composition-id="{cid}" data-width="{W}" data-height="{H}" data-duration="{r(dur)}">
{body}
      </div>
      <script>
        (function () {{
          const build = () => {{
            const tl = gsap.timeline({{ paused: true }});
{js}
            window.__timelines["{cid}"] = tl;
          }};
          document.fonts.ready.then(build);
        }})();
      </script>
    </template>
  </body>
</html>
"""


BASE_CSS = """        .big, .tag, .lab { position: absolute; font-family: "Montserrat", sans-serif; font-weight: 900; letter-spacing: -.04em; line-height: .9; white-space: nowrap; }
        .tag { text-shadow: 0 8px 30px rgba(0,0,0,.7); }
        .lab { display: inline-block; padding: .06em .22em .1em; border-radius: .1em; background: #FFC93C; color: #141414; box-shadow: 0 18px 40px rgba(0,0,0,.45); }
        .shot { position: absolute; inset: 0; overflow: hidden; background: #000; }
        .kb { position: absolute; inset: 0; }
        .kb video { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
        .shade { position: absolute; inset: 0; background: linear-gradient(180deg, rgba(0,0,0,.35) 0%, rgba(0,0,0,0) 30%, rgba(0,0,0,0) 55%, rgba(0,0,0,.55) 100%); }"""


def build_shot(k, sid, clip, a, b, trans, acc_html, acc_css, acc_js):
    start = max(0, a - X)
    end = min(D, b + X) if k < len(SHOTS) - 1 else D
    dur = end - start
    js = [f"const at=(t)=>+Math.max(0,t-{start}).toFixed(3);"]
    # slow push-in on every shot (Ken Burns), alternating direction
    s0, s1 = (1.0, 1.12) if k % 2 == 0 else (1.12, 1.0)
    js.append(f'tl.fromTo("#{sid}-kb",{{scale:{s0}}},{{scale:{s1},duration:{r(dur)},ease:"none"}},0);')
    # transition into this shot
    if trans == "whip":
        js.append(f'tl.fromTo("#{sid}",{{x:520,filter:"blur(22px)"}},{{x:0,filter:"blur(0px)",duration:.24,ease:"power3.out"}},0);')
    elif trans == "zoom":
        js.append(f'tl.fromTo("#{sid}",{{scale:.55,opacity:0,filter:"blur(18px)"}},{{scale:1,opacity:1,filter:"blur(0px)",duration:.26,ease:"power3.out"}},0);')
    elif trans == "flash":
        js.append(f'tl.fromTo("#{sid}",{{scale:1.25,filter:"brightness(3) blur(10px)"}},{{scale:1,filter:"brightness(1) blur(0px)",duration:.3,ease:"power2.out"}},0);')
    # transition out of this shot (matches the next shot's entry)
    if k < len(SHOTS) - 1:
        nxt = SHOTS[k + 1][4]
        t_out = r(b - X - start)
        if nxt == "whip":
            js.append(f'tl.fromTo("#{sid}",{{x:0,filter:"blur(0px)"}},{{x:-520,filter:"blur(22px)",duration:.12,ease:"power3.in",immediateRender:false}},{t_out});')
        elif nxt == "zoom":
            js.append(f'tl.fromTo("#{sid}",{{scale:1,filter:"blur(0px)"}},{{scale:1.8,filter:"blur(18px)",duration:.12,ease:"power3.in",immediateRender:false}},{t_out});')
        elif nxt == "flash":
            js.append(f'tl.fromTo("#{sid}",{{filter:"brightness(1)"}},{{filter:"brightness(3)",duration:.12,ease:"power2.in",immediateRender:false}},{t_out});')
    js.append(acc_js.replace(";", ";\n"))
    body = (f'        <div class="shot" id="{sid}"><div class="kb" id="{sid}-kb">'
            f'<video id="{sid}-v" class="clip" src="assets/clips/{clip}.mp4" muted playsinline data-start="0" data-duration="{r(dur)}" data-track-index="1"></video>'
            f'</div><div class="shade"></div>{acc_html}</div>')
    css = BASE_CSS + "\n        " + acc_css.replace("}", "}\n        ")
    return start, dur, sub(sid, dur, css, body, "\n".join("            " + j for j in js if j.strip()))


def build_captions():
    groups, cur = [], []
    for i, w in enumerate(WORDS):
        cur.append(w)
        nxt = WORDS[i + 1] if i + 1 < len(WORDS) else None
        chars = sum(len(x["word"]) + 1 for x in cur)
        gap = (nxt["start"] - w["end"]) if nxt else 0
        if not nxt or w["word"][-1] in ",.?:!…" or len(cur) >= 2 or gap > 0.25 or (nxt and chars + len(nxt["word"]) > 14):
            groups.append(cur)
            cur = []
    html, js = [], []
    for g, grp in enumerate(groups):
        t0 = grp[0]["start"] - 0.03
        t1 = min(groups[g + 1][0]["start"] - 0.03 if g + 1 < len(groups) else D - 0.05, grp[-1]["end"] + 0.6)
        spans = "".join(f'<span class="cw{" kw" if norm(w["word"]) in KW else ""}" id="cw{w["i"]}">{esc(w["word"].upper())}</span>' for w in grp)
        html.append(f'<div class="cg" id="cg{g}"><p>{spans}</p></div>')
        js.append(f'tl.set("#cg{g}",{{opacity:1}},{r(t0)});tl.fromTo("#cg{g}",{{scale:.7,y:30}},{{scale:1,y:0,duration:.16,ease:"back.out(3)",immediateRender:false}},{r(t0)});tl.set("#cg{g}",{{opacity:0}},{r(t1)});')
        for w in grp:
            js.append(f'tl.fromTo("#cw{w["i"]}",{{color:"#FFFFFF",scale:1}},{{color:"{YEL}",scale:1.12,duration:.06,ease:"power2.out",immediateRender:false}},{r(w["start"])});')
            js.append(f'tl.fromTo("#cw{w["i"]}",{{scale:1.12}},{{scale:1,duration:.18,ease:"back.out(2)",immediateRender:false}},{r(w["start"] + 0.06)});')
            if norm(w["word"]) not in KW:   # ordinary words go back to white when the next word starts
                nx = next((x for x in WORDS if x["i"] == w["i"] + 1), None)
                if nx and nx["i"] in [x["i"] for x in grp]:
                    js.append(f'tl.fromTo("#cw{w["i"]}",{{color:"{YEL}"}},{{color:"#FFFFFF",duration:.05,ease:"none",immediateRender:false}},{r(nx["start"])});')
    style = """        .cg { position: absolute; left: 60px; width: 960px; top: 1040px; height: 240px; display: flex; align-items: center; justify-content: center; opacity: 0; }
        .cg p { width: 100%; text-align: center; font-family: "Montserrat", sans-serif; font-weight: 900; font-size: 104px; line-height: 1.02; letter-spacing: -.03em;
                color: #fff; -webkit-text-stroke: 12px #141414; paint-order: stroke fill; text-shadow: 0 10px 34px rgba(0,0,0,.6); }
        .cw { display: inline-block; margin: 0 .1em; color: #fff; }"""
    return sub("captions", D, style, '        <div id="capwrap">' + "".join(html) + "</div>", "\n".join("            " + j for j in js)), len(groups)


def build_calix():
    poses = sorted({p for _, p in POSES})
    imgs = "".join(f'<img class="pose" id="cx-{p}" src="assets/calix/calix-{p}.png" alt="" />' for p in poses)
    js = [f'tl.set("#cx-{POSES[0][1]}",{{opacity:1}},0);',
          'tl.fromTo("#cx-pos",{y:700,rotation:12},{y:0,rotation:-3,duration:.42,ease:"back.out(1.6)"},0.12);',
          # always alive: breathing and a slow bob, for the whole video
          f'tl.fromTo("#cx-br",{{scaleY:1,scaleX:1}},{{scaleY:1.018,scaleX:.992,duration:.7,ease:"sine.inOut",yoyo:true,repeat:{int(D / 0.7)}}},0);',
          f'tl.fromTo("#cx-bob",{{y:0,rotation:0}},{{y:-12,rotation:1.2,duration:1.3,ease:"sine.inOut",yoyo:true,repeat:{int(D / 1.3)}}},0);']
    cur = POSES[0][1]
    for k, (t, p) in enumerate(POSES[1:]):
        js.append(f'tl.set("#cx-{cur}",{{opacity:0}},{r(t)});tl.set("#cx-{p}",{{opacity:1}},{r(t)});')
        js.append(f'tl.fromTo("#cx-pop",{{scaleX:1.12,scaleY:.9,rotation:{-6 if k % 2 else 5}}},{{scaleX:1,scaleY:1,rotation:0,duration:.32,ease:"elastic.out(1.1,.5)",immediateRender:false}},{r(t)});')
        cur = p
    style = """        #cx-pos { position: absolute; left: -30px; top: 1370px; width: 620px; height: 620px; transform-origin: 50% 100%; }
        #cx-bob, #cx-br, #cx-pop { position: absolute; inset: 0; transform-origin: 45% 100%; }
        .pose { position: absolute; inset: 0; width: 100%; height: 100%; opacity: 0; }"""
    body = f'        <div id="cx-pos" data-layout-allow-overflow><div id="cx-bob"><div id="cx-br"><div id="cx-pop">{imgs}</div></div></div></div>'
    return sub("calix", D, style, body, "\n".join("            " + j for j in js))


def build_hud():
    # story-style progress bar across the top with a notch at each fact
    notches = "".join(f'<i style="left:{c / FULL * 100:.2f}%"></i>' for c in CHAPTERS[1:])
    body = f'        <div id="pb"><div id="pb-fill"></div>{notches}</div>'
    style = """        #pb { position: absolute; left: 40px; right: 40px; top: 46px; height: 10px; border-radius: 5px; background: rgba(255,255,255,.28); overflow: hidden; }
        #pb-fill { position: absolute; inset: 0; background: #FFC93C; transform-origin: 0% 50%; }
        #pb i { position: absolute; top: 0; width: 6px; height: 10px; background: rgba(20,20,20,.7); }"""
    js = [f'tl.fromTo("#pb-fill",{{scaleX:0}},{{scaleX:{r(D / FULL)},duration:{r(D)},ease:"none"}},0);']
    return sub("hud", D, style, body, "\n".join("            " + j for j in js))


def build_fx():
    js = [f'const gp={{f:0}};tl.fromTo(gp,{{f:0}},{{f:{int(D * 12)},duration:{r(D)},ease:"none",onUpdate:()=>{{const k=Math.floor(gp.f);'
          f'document.getElementById("fx-grain").style.backgroundPosition=((k*7919)%512)+"px "+((k*104729)%512)+"px";}}}},0);']
    style = "        #fx-grain { position: absolute; inset: 0; background: url(assets/fx/grain.png) repeat; background-size: 512px 512px; opacity: .06; mix-blend-mode: overlay; }"
    return sub("fx", D, style, '        <div id="fx-grain"></div>', "\n".join("            " + j for j in js))


os.makedirs(os.path.join(EP, "compositions/scenes"), exist_ok=True)
hosts = []
for k, s in enumerate(SHOTS):
    start, dur, html = build_shot(k, *s)
    open(os.path.join(EP, f"compositions/scenes/{s[0]}.html"), "w").write(html)
    hosts.append(f'<div id="el-{s[0]}" data-composition-id="{s[0]}" data-composition-src="compositions/scenes/{s[0]}.html" data-start="{r(start)}" '
                 f'data-duration="{r(dur)}" data-track-index="{1 + k % 2}" data-track-kind="graphics" data-width="{W}" data-height="{H}"></div>')
cap, ng = build_captions()
for name, html in (("captions", cap), ("calix", build_calix()), ("hud", build_hud()), ("fx", build_fx())):
    open(os.path.join(EP, f"compositions/{name}.html"), "w").write(html)

aud = [f'<audio id="voice" src="assets/voice/voice.wav" data-start="0" data-duration="{r(min(D, words["duration"]))}" data-track-index="10" data-volume="1"></audio>']
for n, ti in (("music", 11), ("sfx", 12)):
    if os.path.exists(os.path.join(EP, f"assets/audio/{n}.wav")):
        aud.append(f'<audio id="{n}" src="assets/audio/{n}.wav" data-start="0" data-duration="{r(D)}" data-track-index="{ti}" data-volume="1"></audio>')
js = []
for t, s in PUNCH:
    js.append(f'tl.fromTo("#cam",{{scale:1}},{{scale:{s},duration:.1,ease:"power2.out",immediateRender:false}},{r(t - 0.03)});')
    js.append(f'tl.fromTo("#cam",{{scale:{s}}},{{scale:1,duration:.6,ease:"power2.inOut",immediateRender:false}},{r(t + 0.1)});')
for t in SHAKE:
    js.append(f'tl.fromTo("#cam",{{x:0,y:0}},{{x:14,y:-8,duration:.04,ease:"none",yoyo:true,repeat:7,immediateRender:false}},{r(t)});')
layer = lambda cid, ti, kind="graphics": (f'<div id="el-{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" data-start="0" '
                                         f'data-duration="{r(D)}" data-track-index="{ti}" data-track-kind="{kind}" data-width="{W}" data-height="{H}"></div>')
index = f"""<!doctype html>
<html lang="fr" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <title>Calix #6 — Vidéos X, masturbation : 3 faits</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
{FONTS}
      * {{ margin:0; padding:0; box-sizing:border-box; }}
      html, body {{ width:{W}px; height:{H}px; overflow:hidden; background:#000; }}
      #root {{ position:relative; width:100%; height:100%; overflow:hidden; background:#000; }}
      #cam {{ position:absolute; inset:0; transform-origin:50% 45%; }}
      [data-composition-id="main"] div[data-composition-src] {{ position:absolute; inset:0; }}
      .hf-font-a {{ font-family:"Montserrat"; font-weight:900; }} .hf-font-b {{ font-family:"Caveat"; font-weight:700; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{r(D)}" data-width="{W}" data-height="{H}">
      <div id="cam">
        {(chr(10) + "        ").join(hosts)}
      </div>
      {layer("fx", 3)}
      {layer("calix", 4)}
      {layer("captions", 5, "captions")}
      {layer("hud", 6)}
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
open(os.path.join(EP, "index.html"), "w").write(index)
print(f"v4 built · {D}s of {FULL}s · {len(SHOTS)} shots · {ng} caption groups")

# canonical cinema grade on every shot (persisted by the CLI as data-color-grading)
import subprocess
GRADE = {"preset": "deep-contrast", "intensity": 0.7, "details": {"vignette": 0.35, "grain": 0.12}}
LIFT = {"s3": {"exposure": 0.45, "shadows": 0.25}}   # the riverbank silhouette is very dark under the contrast preset
for sid, *_ in SHOTS:
    g = dict(GRADE, adjust=LIFT[sid]) if sid in LIFT else GRADE
    subprocess.run(["npx", "--yes", "hyperframes@0.8.181", "media-treatment", "--project", EP, "--file", f"compositions/scenes/{sid}.html",
                    "--selector", f"#{sid}-v", "--grading", json.dumps(g), "--apply", "--json"], check=True, capture_output=True)
print("graded:", ", ".join(s[0] for s in SHOTS))
