#!/usr/bin/env python3
"""Build a Calix TikTok short (HyperFrames project) from plan.json + assets/voice/words.json.

usage: build_short.py <episode_dir>
Writes index.html, compositions/stage.html, compositions/captions.html.
"""
import json
import os
import re
import subprocess
import sys

import numpy as np

EP = os.path.abspath(sys.argv[1])
plan = json.load(open(os.path.join(EP, "plan.json")))
W, H = plan.get("format", [1080, 1920])
words = json.load(open(os.path.join(EP, "assets/voice/words.json")))
D = round(words["duration"] + plan.get("tail", 0.6), 2)
PC = plan.get("pillar_color", "#FF6B35")
GZ = dict(left=72, top=250, width=936, height=480)

FONTS = "\n".join(
    [f'@font-face{{font-family:"Inter";font-weight:{w};font-style:normal;font-display:block;src:url("assets/fonts/Inter-{w}.woff2") format("woff2");}}' for w in (500, 600, 700, 800, 900)]
    + [f'@font-face{{font-family:"IBM Plex Mono";font-weight:{w};font-style:normal;font-display:block;src:url("assets/fonts/IBMPlexMono-{w}.woff2") format("woff2");}}' for w in (500, 600)])


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def r(x):
    return round(float(x), 3)


# ------------------------------------------------------------------ icons
ICON = {
    "thermo": '<svg viewBox="0 0 24 24"><path d="M14 4v10.54a4 4 0 1 1-4 0V4a2 2 0 0 1 4 0Z"/></svg>',
    "drop": '<svg viewBox="0 0 24 24"><path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5C6 11.1 5 13 5 15a7 7 0 0 0 7 7z"/></svg>',
    "wind": '<svg viewBox="0 0 24 24"><path d="M12.8 19.6A2 2 0 1 0 14 16H2"/><path d="M17.5 8a2.5 2.5 0 1 1 2 4H2"/><path d="M9.8 4.4A2 2 0 1 1 11 8H2"/></svg>',
    "flame": '<svg viewBox="0 0 24 24"><path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 0 0 2.5 2.5z"/></svg>',
    "x": '<svg viewBox="0 0 24 24"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>',
    "check": '<svg viewBox="0 0 24 24"><path d="M20 6 9 17l-5-5"/></svg>',
    "warn": '<svg viewBox="0 0 24 24"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>',
    "plus": '<svg viewBox="0 0 24 24"><path d="M5 12h14"/><path d="M12 5v14"/></svg>',
    "share": '<svg viewBox="0 0 24 24"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="m8.59 13.51 6.83 3.98"/><path d="m15.41 6.51-6.82 3.98"/></svg>',
    "down": '<svg viewBox="0 0 24 24"><path d="M12 5v14"/><path d="m19 12-7 7-7-7"/></svg>',
    "up": '<svg viewBox="0 0 24 24"><path d="m5 12 7-7 7 7"/><path d="M12 19V5"/></svg>',
}

DROP_PATH = "M12 2c-.5 2.5-2 4.9-4 6.5C6 10.1 5 12 5 14a7 7 0 0 0 14 0c0-2-1-3.9-3-5.5S12.5 4.5 12 2z"


class Block:
    def __init__(self):
        self.html, self.css, self.js = [], [], []


def seeded(n, seed):
    rng = np.random.default_rng(seed)
    return rng.random((n, 4))


def block_myth(b, p, i):
    k = f"b{i}"
    b.css.append(f"""
#{k} .kick {{ font-family:"IBM Plex Mono",monospace; font-weight:600; font-size:24px; letter-spacing:.16em; text-transform:uppercase; color:#FF6B35; }}
#{k} .ln {{ position:relative; height:94px; overflow:hidden; margin-top:6px; }}
#{k} .ln span {{ display:block; font-weight:900; font-size:86px; line-height:94px; letter-spacing:-.05em; white-space:nowrap; }}
#{k} .strike {{ position:absolute; left:-6px; top:50px; height:10px; border-radius:5px; background:#FF2D55; }}
#{k}-stamp {{ position:absolute; right:30px; top:150px; padding:6px 30px 10px; border:9px solid #FF2D55; border-radius:22px; color:#FF2D55; font-weight:900; font-size:150px; line-height:1; letter-spacing:-.03em; background:rgba(10,10,15,.55); box-shadow:0 0 60px rgba(255,45,85,.45); }}""")
    lines = "".join(f'<div class="ln"><span id="{k}-l{j}">{esc(t)}</span><i id="{k}-s{j}" class="strike" style="width:{min(900, int(len(t) * 47))}px"></i></div>' for j, (t, _) in enumerate(p["lines"]))
    b.html.append(f'<div class="kick" id="{k}-kick">{esc(p["kicker"])}</div>{lines}<div id="{k}-stamp">{esc(p["stamp"][0])}</div>')
    b.js.append(f'tl.fromTo("#{k}-kick",{{opacity:0,x:-20}},{{opacity:1,x:0,duration:.4,ease:"expo.out"}},{r(p["start"])});')
    for j, (_, t) in enumerate(p["lines"]):
        b.js.append(f'tl.fromTo("#{k}-l{j}",{{yPercent:110}},{{yPercent:0,duration:.55,ease:"expo.out"}},{r(t)});')
        b.js.append(f'tl.fromTo("#{k}-s{j}",{{scaleX:0}},{{scaleX:1,duration:.22,ease:"power3.out",transformOrigin:"0% 50%"}},{r(p["stamp"][1] + .06 + j * .05)});')
    st = p["stamp"][1]
    b.js.append(f'tl.fromTo("#{k}-stamp",{{scale:2.6,opacity:0,rotation:-4}},{{scale:1,opacity:1,rotation:-10,duration:.26,ease:"back.out(2.2)"}},{r(st)});')


def block_word_drops(b, p, i):
    k = f"b{i}"
    b.css.append(f"""
#{k}-w {{ position:absolute; left:0; right:0; top:90px; text-align:center; font-weight:900; font-size:190px; line-height:1; letter-spacing:-.05em; color:#00D4FF; text-shadow:0 0 60px rgba(0,212,255,.35); }}
#{k}-sub {{ position:absolute; left:0; right:0; top:330px; text-align:center; font-weight:800; font-size:64px; letter-spacing:-.03em; }}
#{k}-sub b {{ color:#FF6B35; }}
#{k} .dr {{ position:absolute; width:34px; height:44px; }}
#{k} .dr svg {{ width:34px; height:44px; fill:#00D4FF; opacity:.9; }}""")
    sub = esc(p["sub"][0]).replace("≠", "<b>≠</b>")
    drops = "".join(f'<div class="dr" id="{k}-d{j}" style="left:{int(40 + v[0] * 850)}px; top:-60px;"><svg viewBox="0 0 24 24"><path d="{DROP_PATH}"/></svg></div>' for j, v in enumerate(seeded(16, 3)))
    b.html.append(f'{drops}<div id="{k}-w">{esc(p["word"][0])}</div><div id="{k}-sub">{sub}</div>')
    t = p["word"][1]
    b.js.append(f'tl.fromTo("#{k}-w",{{scale:.6,opacity:0}},{{scale:1,opacity:1,duration:.45,ease:"back.out(2)"}},{r(t)});')
    for j, v in enumerate(seeded(16, 3)):
        b.js.append(f'tl.fromTo("#{k}-d{j}",{{y:0,opacity:0}},{{y:{int(420 + v[1] * 120)},opacity:1,duration:{r(.9 + v[2] * .5)},ease:"power2.in"}},{r(t + .05 + v[3] * 1.6)});')
        b.js.append(f'tl.to("#{k}-d{j}",{{opacity:0,duration:.2}},{r(t + .07 + v[3] * 1.6 + .9 + v[2] * .5)});')
    b.js.append(f'tl.fromTo("#{k}-sub",{{opacity:0,y:30}},{{opacity:1,y:0,duration:.45,ease:"expo.out"}},{r(p["sub"][1])});')


def block_banner(b, p, i):
    k = f"b{i}"
    b.css.append(f'#{k}-t {{ position:absolute; left:0; right:0; top:160px; text-align:center; font-weight:900; font-size:150px; line-height:1; letter-spacing:-.05em; color:#FF6B35; }}')
    b.html.append(f'<div id="{k}-t">{esc(p["text"][0])}</div>')
    b.js.append(f'tl.fromTo("#{k}-t",{{x:-260,skewX:-18,opacity:0}},{{x:0,skewX:0,opacity:1,duration:.32,ease:"expo.out"}},{r(p["text"][1])});')


def block_science(b, p, i):
    k = f"b{i}"
    b.css.append(f"""
#{k}-card {{ position:absolute; inset:0; border-radius:32px; background:#10101a; border:1px solid #262636; }}
#{k}-tag {{ position:absolute; right:26px; top:26px; padding:8px 14px; border:1px dashed #4a4a5c; border-radius:10px; font-family:"IBM Plex Mono",monospace; font-weight:600; font-size:16px; letter-spacing:.14em; text-transform:uppercase; color:#9a9aa8; }}
#{k}-title {{ position:absolute; left:40px; top:40px; font-weight:900; font-size:66px; letter-spacing:-.045em; }}
#{k}-strike {{ position:absolute; left:42px; top:128px; font-weight:700; font-size:34px; color:#9a9aa8; }}
#{k}-strike i {{ position:absolute; left:-4px; right:-4px; top:21px; height:5px; border-radius:3px; background:#FF2D55; display:block; }}
#{k}-eq {{ position:absolute; left:40px; top:182px; font-weight:900; font-size:46px; letter-spacing:-.03em; color:#00D4FF; }}
#{k} .st {{ position:absolute; top:276px; width:240px; text-align:center; }}
#{k} .st .ic {{ width:110px; height:110px; margin:0 auto; border-radius:50%; background:rgba(0,212,255,.12); border:2px solid rgba(0,212,255,.5); display:flex; align-items:center; justify-content:center; }}
#{k} .st .ic svg {{ width:56px; height:56px; fill:none; stroke:#00D4FF; stroke-width:2; stroke-linecap:round; stroke-linejoin:round; }}
#{k} .st .lb {{ margin-top:16px; font-family:"IBM Plex Mono",monospace; font-weight:600; font-size:21px; letter-spacing:.06em; color:#fff; }}
#{k} .ar {{ position:absolute; top:318px; font-weight:900; font-size:44px; color:#6a6a80; }}""")
    st = "".join(f'<div class="st" id="{k}-st{j}" style="left:{30 + j * 312}px"><div class="ic">{ICON[ic]}</div><div class="lb">{esc(lb)}</div></div>' for j, (ic, lb, _) in enumerate(p["steps"]))
    ar = "".join(f'<div class="ar" id="{k}-ar{j}" style="left:{258 + j * 312}px">→</div>' for j in range(len(p["steps"]) - 1))
    b.html.append(f'<div id="{k}-card"></div><div id="{k}-tag">{esc(p["tag"])}</div><div id="{k}-title">{esc(p["title"][0])}</div>'
                  f'<div id="{k}-strike">{esc(p["strike"][0])}<i id="{k}-sl"></i></div><div id="{k}-eq">{esc(p["equals"][0])}</div>{st}{ar}')
    b.js.append(f'tl.fromTo("#{k}-tag",{{opacity:0}},{{opacity:1,duration:.3}},{r(p["start"] + .1)});')
    b.js.append(f'tl.fromTo("#{k}-title",{{opacity:0,y:24}},{{opacity:1,y:0,duration:.45,ease:"expo.out"}},{r(p["title"][1])});')
    s = p["strike"][1]
    b.js.append(f'tl.fromTo("#{k}-strike",{{opacity:0,x:-20}},{{opacity:1,x:0,duration:.4,ease:"expo.out"}},{r(s)});')
    b.js.append(f'tl.fromTo("#{k}-sl",{{scaleX:0}},{{scaleX:1,duration:.3,ease:"power3.out",transformOrigin:"0% 50%"}},{r(s + .65)});')
    b.js.append(f'tl.fromTo("#{k}-eq",{{opacity:0,y:20}},{{opacity:1,y:0,duration:.45,ease:"expo.out"}},{r(p["equals"][1])});')
    for j, (_, _, t) in enumerate(p["steps"]):
        b.js.append(f'tl.fromTo("#{k}-st{j}",{{opacity:0,scale:.7}},{{opacity:1,scale:1,duration:.4,ease:"back.out(2)"}},{r(t)});')
        if j:
            b.js.append(f'tl.fromTo("#{k}-ar{j - 1}",{{opacity:0,x:-14}},{{opacity:1,x:0,duration:.3,ease:"power2.out"}},{r(t - .1)});')


def block_scale(b, p, i):
    k = f"b{i}"
    up = p["mode"] == "up"
    b.css.append(f"""
#{k}-sc {{ position:absolute; left:20px; top:60px; width:330px; height:360px; }}
#{k}-sc svg {{ width:330px; height:360px; }}
#{k}-disp {{ position:absolute; left:95px; top:72px; width:140px; height:66px; display:flex; align-items:center; justify-content:center; }}
#{k}-disp svg {{ width:48px; height:48px; fill:none; stroke:#00D4FF; stroke-width:2.6; stroke-linecap:round; stroke-linejoin:round; }}
#{k}-t {{ position:absolute; left:390px; top:58px; font-weight:900; font-size:64px; letter-spacing:-.045em; white-space:nowrap; }}
#{k}-a {{ position:absolute; left:392px; top:160px; display:flex; align-items:center; gap:14px; font-weight:800; font-size:44px; letter-spacing:-.03em; white-space:nowrap; }}
#{k}-a svg {{ width:48px; height:48px; fill:none; stroke:#FF6B35; stroke-width:2.6; stroke-linecap:round; stroke-linejoin:round; }}
#{k}-n {{ position:absolute; left:394px; top:236px; font-family:"IBM Plex Mono",monospace; font-weight:600; font-size:22px; letter-spacing:.1em; text-transform:uppercase; color:#9a9aa8; }}
#{k}-rv {{ position:absolute; left:390px; top:288px; font-weight:900; font-size:100px; letter-spacing:-.05em; color:#00D4FF; text-shadow:0 0 50px rgba(0,212,255,.35); white-space:nowrap; }}
#{k} .dr {{ position:absolute; width:30px; height:40px; }}
#{k} .dr svg {{ width:30px; height:40px; fill:#00D4FF; }}""")
    scale_svg = ('<svg viewBox="0 0 330 360"><rect x="10" y="10" width="310" height="330" rx="70" fill="#1b1b2a" stroke="#34344a" stroke-width="4"/>'
                 '<rect x="85" y="62" width="160" height="86" rx="18" fill="#07070c" stroke="#2c2c3e" stroke-width="3"/>'
                 '<rect x="60" y="300" width="70" height="16" rx="8" fill="#2c2c3e"/><rect x="200" y="300" width="70" height="16" rx="8" fill="#2c2c3e"/></svg>')
    drops = "".join(f'<div class="dr" id="{k}-d{j}" style="left:{150}px; top:{180}px;"><svg viewBox="0 0 24 24"><path d="{DROP_PATH}"/></svg></div>' for j in range(10))
    arrow = ICON["up" if up else "down"]
    rv = f'<div id="{k}-rv">{esc(p["reveal"][0])}</div>' if p.get("reveal") else ""
    b.html.append(f'<div id="{k}-sc">{scale_svg}<div id="{k}-disp">{arrow}</div></div>{drops}'
                  f'<div id="{k}-t">{esc(p["title"][0])}</div><div id="{k}-a">{arrow}<span>{esc(p["arrow"][0])}</span></div><div id="{k}-n">{esc(p["note"][0])}</div>{rv}')
    b.js.append(f'tl.fromTo("#{k}-sc",{{opacity:0,y:40,rotation:-4}},{{opacity:1,y:0,rotation:0,duration:.5,ease:"back.out(1.6)"}},{r(p["start"] + .05)});')
    b.js.append(f'tl.fromTo("#{k}-t",{{opacity:0,y:20}},{{opacity:1,y:0,duration:.4,ease:"expo.out"}},{r(p["title"][1])});')
    ta = p["arrow"][1]
    b.js.append(f'tl.fromTo("#{k}-a",{{opacity:0,x:-20}},{{opacity:1,x:0,duration:.4,ease:"expo.out"}},{r(ta)});')
    b.js.append(f'tl.fromTo("#{k}-disp",{{opacity:0,y:{18 if up else -18}}},{{opacity:1,y:0,duration:.4,ease:"back.out(2)"}},{r(ta)});')
    b.js.append(f'tl.fromTo("#{k}-n",{{opacity:0}},{{opacity:1,duration:.35}},{r(p["note"][1])});')
    td = p["drops"]
    for j, v in enumerate(seeded(10, 7 if up else 5)):
        dx, dy = int(-150 + v[0] * 330), int(-120 - v[1] * 160)
        if up:
            b.js.append(f'tl.fromTo("#{k}-d{j}",{{x:{dx},y:{dy - 140},opacity:0,scale:.8}},{{x:0,y:0,opacity:1,scale:.4,duration:{r(.55 + v[2] * .35)},ease:"power2.in"}},{r(td + v[3] * .7)});')
            b.js.append(f'tl.to("#{k}-d{j}",{{opacity:0,duration:.12}},{r(td + v[3] * .7 + .57 + v[2] * .35)});')
        else:
            b.js.append(f'tl.fromTo("#{k}-d{j}",{{x:0,y:0,opacity:0,scale:.4}},{{x:{dx},y:{dy},opacity:1,scale:1,duration:{r(.5 + v[2] * .3)},ease:"power2.out"}},{r(td + v[3] * .3)});')
            b.js.append(f'tl.to("#{k}-d{j}",{{opacity:0,duration:.25}},{r(td + v[3] * .3 + .52 + v[2] * .3)});')
    if p.get("reveal"):
        b.js.append(f'tl.fromTo("#{k}-rv",{{opacity:0,scale:.6}},{{opacity:1,scale:1,duration:.35,ease:"back.out(2.4)",transformOrigin:"0% 50%"}},{r(p["reveal"][1])});')


def block_versus(b, p, i):
    k = f"b{i}"
    b.css.append(f"""
#{k}-chip {{ position:absolute; left:50%; top:0; width:300px; margin-left:-150px; height:58px; border-radius:29px; background:#FF2D55; color:#0A0A0F; display:flex; align-items:center; justify-content:center; gap:10px; font-family:"IBM Plex Mono",monospace; font-weight:600; font-size:22px; letter-spacing:.16em; text-transform:uppercase; }}
#{k}-chip svg {{ width:26px; height:26px; fill:none; stroke:#0A0A0F; stroke-width:2.4; stroke-linecap:round; stroke-linejoin:round; }}
#{k} .cir {{ position:absolute; top:110px; width:300px; height:300px; border-radius:50%; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:10px; }}
#{k} .cir svg {{ width:80px; height:80px; fill:none; stroke-width:2; stroke-linecap:round; stroke-linejoin:round; }}
#{k} .cir span {{ font-weight:900; font-size:66px; letter-spacing:-.045em; }}
#{k}-L {{ left:40px; background:rgba(0,212,255,.12); border:3px solid #00D4FF; }}
#{k}-L svg {{ stroke:#00D4FF; }} #{k}-L span {{ color:#00D4FF; }}
#{k}-R {{ left:596px; background:rgba(255,107,53,.12); border:3px solid #FF6B35; }}
#{k}-R svg {{ stroke:#FF6B35; }} #{k}-R span {{ color:#FF6B35; }}
#{k}-sg {{ position:absolute; left:368px; top:150px; width:200px; text-align:center; font-weight:900; font-size:200px; line-height:1; color:#fff; }}""")
    b.html.append(f'<div id="{k}-chip">{ICON["warn"]}{esc(p["chip"][0])}</div>'
                  f'<div class="cir" id="{k}-L">{ICON["drop"]}<span>{esc(p["left"][0])}</span></div><div id="{k}-sg">≠</div>'
                  f'<div class="cir" id="{k}-R">{ICON["flame"]}<span>{esc(p["right"][0])}</span></div>')
    b.js.append(f'tl.fromTo("#{k}-L",{{opacity:0,scale:.6}},{{opacity:1,scale:1,duration:.45,ease:"back.out(1.8)"}},{r(p["left"][1])});')
    b.js.append(f'tl.fromTo("#{k}-chip",{{opacity:0,y:-20}},{{opacity:1,y:0,duration:.35,ease:"back.out(2)"}},{r(p["chip"][1])});')
    b.js.append(f'tl.fromTo("#{k}-sg",{{opacity:0,scale:2.4}},{{opacity:1,scale:1,duration:.3,ease:"back.out(2)"}},{r(p["sign"])});')
    b.js.append(f'tl.fromTo("#{k}-R",{{opacity:0,scale:.6}},{{opacity:1,scale:1,duration:.45,ease:"back.out(1.8)"}},{r(p["right"][1])});')


def block_list(b, p, i):
    k = f"b{i}"
    do = p["variant"] == "do"
    col = "#00FF87" if do else "#FF2D55"
    b.css.append(f"""
#{k}-t {{ position:absolute; left:0; top:0; width:900px; font-weight:900; font-size:{58 if do else 72}px; line-height:1.05; letter-spacing:-.045em; }}
#{k} .it {{ position:absolute; left:0; height:88px; display:flex; align-items:center; gap:22px; }}
#{k} .it .ic {{ width:76px; height:76px; border-radius:50%; flex:none; display:flex; align-items:center; justify-content:center; background:{col}22; border:3px solid {col}; font-weight:900; font-size:38px; color:{col}; }}
#{k} .it .ic svg {{ width:40px; height:40px; fill:none; stroke:{col}; stroke-width:3; stroke-linecap:round; stroke-linejoin:round; }}
#{k} .it span {{ font-weight:800; font-size:52px; letter-spacing:-.03em; white-space:nowrap; }}
#{k} .it .ck {{ width:44px; height:44px; flex:none; }}
#{k} .it .ck svg {{ width:44px; height:44px; fill:none; stroke:#00FF87; stroke-width:3.2; stroke-linecap:round; stroke-linejoin:round; }}
#{k}-w {{ position:absolute; left:0; top:360px; width:900px; height:96px; border-radius:24px; background:rgba(255,45,85,.14); border:2px solid #FF2D55; display:flex; align-items:center; gap:18px; padding:0 26px; }}
#{k}-w svg {{ width:46px; height:46px; fill:none; stroke:#FF2D55; stroke-width:2.4; stroke-linecap:round; stroke-linejoin:round; flex:none; }}
#{k}-w span {{ font-weight:800; font-size:42px; letter-spacing:-.02em; white-space:nowrap; }}
#{k}-w b {{ color:#00D4FF; font-weight:900; }}""")
    top0 = 160 if do else 120
    step = 102 if do else 110
    items = ""
    for j, (txt, _) in enumerate(p["items"]):
        ic = f"{j + 1}" if do else ICON["x"]
        ck = f'<div class="ck" id="{k}-c{j}">{ICON["check"]}</div>' if do else ""
        items += f'<div class="it" id="{k}-i{j}" style="top:{top0 + j * step}px"><div class="ic">{ic}</div><span>{esc(txt)}</span>{ck}</div>'
    warn = ""
    if p.get("warn"):
        t = esc(p["warn"][0])
        head, _, tail = t.partition(" : ")
        warn = f'<div id="{k}-w">{ICON["warn"]}<span>{head} : <b id="{k}-wb">{tail}</b></span></div>'
    b.html.append(f'<div id="{k}-t">{esc(p["title"][0])}</div>{items}{warn}')
    b.js.append(f'tl.fromTo("#{k}-t",{{opacity:0,y:24}},{{opacity:1,y:0,duration:.45,ease:"expo.out"}},{r(p["title"][1])});')
    for j, (_, t) in enumerate(p["items"]):
        b.js.append(f'tl.fromTo("#{k}-i{j}",{{opacity:0,x:-60}},{{opacity:1,x:0,duration:.45,ease:"expo.out"}},{r(t)});')
        if do:
            b.js.append(f'tl.fromTo("#{k}-c{j}",{{opacity:0,scale:0}},{{opacity:1,scale:1,duration:.3,ease:"back.out(3)"}},{r(t + .3)});')
    if p.get("warn"):
        b.js.append(f'tl.fromTo("#{k}-w",{{opacity:0,y:30}},{{opacity:1,y:0,duration:.45,ease:"expo.out"}},{r(p["warn"][1])});')
        b.js.append(f'tl.fromTo("#{k}-wb",{{opacity:.35}},{{opacity:1,duration:.25,ease:"none"}},{r(p["warn"][2])});')


def block_outro(b, p, i):
    k = f"b{i}"
    b.css.append(f"""
#{k}-ic {{ position:absolute; left:0; top:20px; width:150px; height:150px; border-radius:36px; overflow:hidden; box-shadow:0 0 70px rgba(255,90,60,.4); }}
#{k}-ic img {{ width:150px; height:150px; display:block; }}
#{k}-wm {{ position:absolute; left:180px; top:28px; height:140px; overflow:hidden; font-weight:900; font-size:128px; line-height:140px; letter-spacing:-.05em; white-space:nowrap; }}
#{k}-wm span {{ display:inline-block; }}
#{k}-chips {{ position:absolute; left:0; top:210px; width:900px; display:flex; flex-wrap:wrap; gap:14px; }}
#{k} .chip {{ height:62px; padding:0 24px; border-radius:31px; background:#15151f; border:1px solid #2c2c3a; display:flex; align-items:center; gap:12px; font-weight:700; font-size:32px; white-space:nowrap; }}
#{k} .chip i {{ width:14px; height:14px; border-radius:50%; display:block; }}
#{k}-tag {{ position:absolute; left:2px; top:380px; font-family:"IBM Plex Mono",monospace; font-weight:600; font-size:24px; letter-spacing:.12em; text-transform:uppercase; color:#C8C8D0; }}
#{k}-tag b {{ color:#00FF87; font-weight:600; }}
#{k}-tag i {{ font-style:normal; margin:0 .6em; }}
#{k}-cta {{ position:absolute; left:0; top:220px; width:900px; display:flex; gap:22px; }}
#{k} .btn {{ height:116px; border-radius:58px; display:flex; align-items:center; gap:16px; padding:0 40px; font-weight:900; font-size:50px; letter-spacing:-.03em; }}
#{k} .btn svg {{ width:46px; height:46px; fill:none; stroke-width:3; stroke-linecap:round; stroke-linejoin:round; }}
#{k}-b0 {{ background:linear-gradient(90deg,#FF2D55,#FF6B35); color:#0A0A0F; box-shadow:0 20px 60px rgba(255,60,70,.4); }}
#{k}-b0 svg {{ stroke:#0A0A0F; }}
#{k}-b1 {{ background:#15151f; border:2px solid #3a3a4c; color:#fff; }}
#{k}-b1 svg {{ stroke:#fff; }}""")
    chips = "".join(f'<div class="chip" id="{k}-c{j}"><i style="background:{c}; box-shadow:0 0 12px {c}"></i>{esc(t)}</div>' for j, (t, c, _) in enumerate(p["chips"]))
    wm = "".join(f'<span>{ch}</span>' for ch in "CaliBodi")
    (t0, _), (t1, _) = p["tagline"]
    cta = (f'<div class="btn" id="{k}-b0">{ICON["plus"]}{esc(p["cta"][0][0])}</div>'
           f'<div class="btn" id="{k}-b1">{ICON["share"]}{esc(p["cta"][1][0])}</div>')
    b.html.append(f'<div id="{k}-ic"><img src="assets/brand/icon-512.png" alt=""/></div><div id="{k}-wm">{wm}</div>'
                  f'<div id="{k}-chips">{chips}</div><div id="{k}-tag"><span id="{k}-t0">{esc(t0)}</span><span id="{k}-t1"><i>·</i><b>{esc(t1)}</b></span></div><div id="{k}-cta">{cta}</div>')
    b.js.append(f'tl.fromTo("#{k}-ic",{{scale:.2,rotation:-20,opacity:0}},{{scale:1,rotation:0,opacity:1,duration:.6,ease:"back.out(1.8)"}},{r(p["logo"])});')
    b.js.append(f'gsap.utils.toArray("#{k}-wm span").forEach((c,j)=>tl.fromTo(c,{{yPercent:105}},{{yPercent:0,duration:.55,ease:"expo.out"}},{r(p["word"])}+j*.035));')
    for j, (_, _, t) in enumerate(p["chips"]):
        b.js.append(f'tl.fromTo("#{k}-c{j}",{{opacity:0,y:20,scale:.85}},{{opacity:1,y:0,scale:1,duration:.35,ease:"back.out(2)"}},{r(t)});')
    b.js.append(f'tl.fromTo("#{k}-t0",{{opacity:0}},{{opacity:1,duration:.3}},{r(p["tagline"][0][1])});')
    b.js.append(f'tl.fromTo("#{k}-t1",{{opacity:0}},{{opacity:1,duration:.3}},{r(p["tagline"][1][1])});')
    tc = p["cta"][0][1]
    b.js.append(f'tl.to(["#{k}-chips","#{k}-tag"],{{opacity:0,y:-20,duration:.25,ease:"power2.in"}},{r(tc - .05)});')
    b.js.append(f'tl.fromTo("#{k}-b0",{{opacity:0,scale:.6}},{{opacity:1,scale:1,duration:.4,ease:"back.out(2)"}},{r(tc)});')
    b.js.append(f'tl.to("#{k}-b0",{{scale:.92,duration:.08,ease:"power2.in"}},{r(tc + .55)});')
    b.js.append(f'tl.to("#{k}-b0",{{scale:1,duration:.25,ease:"back.out(3)"}},{r(tc + .63)});')
    b.js.append(f'tl.fromTo("#{k}-b1",{{opacity:0,scale:.6}},{{opacity:1,scale:1,duration:.4,ease:"back.out(2)"}},{r(p["cta"][1][1])});')


BUILDERS = {"myth": block_myth, "word_drops": block_word_drops, "banner": block_banner, "science": block_science,
            "scale": block_scale, "versus": block_versus, "list": block_list, "outro": block_outro}


# ------------------------------------------------------------------ voice envelope for Calix
def voice_envelope(fps=30):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(EP, "assets/voice/voice.wav"), "-f", "f32le", "-ac", "1", "-ar", "48000", "-"],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.float32)
    hop = 48000 // fps
    n = int(D * fps) + 2
    env = np.zeros(n)
    for f in range(n):
        seg = x[f * hop:(f + 1) * hop]
        env[f] = np.sqrt(np.mean(seg ** 2)) if len(seg) else 0
    env = env / (np.percentile(env, 95) + 1e-9)
    env = np.clip(env, 0, 1)
    sm = np.zeros_like(env)
    for f in range(n):
        sm[f] = max(env[f], (sm[f - 1] * 0.72) if f else 0)
    return [round(v, 2) for v in sm]


# ------------------------------------------------------------------ stage composition
blocks_html, blocks_css, blocks_js = [], [], []
for i, p in enumerate(plan["blocks"]):
    b = Block()
    BUILDERS[p["type"]](b, p, i)
    blocks_html.append(f'<div class="gz" id="b{i}">{"".join(b.html)}</div>')
    blocks_css.extend(b.css)
    st, en = p["start"], p["end"]
    blocks_js.append(f'tl.fromTo("#b{i}",{{opacity:0,y:30}},{{opacity:1,y:0,duration:.3,ease:"power3.out"}},{r(st)});')
    if en < D - 0.05:
        blocks_js.append(f'tl.to("#b{i}",{{opacity:0,y:-24,duration:.22,ease:"power2.in"}},{r(en - .22)});')
    blocks_js.extend(b.js)

poses = sorted({ps for _, ps in plan["poses"]})
pose_imgs = "".join(f'<img class="pose" id="px-{ps}" src="assets/calix/calix-{ps}.png" alt=""/>' for ps in poses)
pose_js = []
prev = None
for j, (t, ps) in enumerate(plan["poses"]):
    if prev:
        pose_js.append(f'tl.set("#px-{prev}",{{opacity:0}},{r(t)});')
    pose_js.append(f'tl.set("#px-{ps}",{{opacity:1}},{r(t)});')
    if j:
        pose_js.append(f'tl.fromTo("#cx-pop",{{scale:.965,y:14}},{{scale:1,y:0,duration:.22,ease:"back.out(2)",immediateRender:false}},{r(t)});')
    prev = ps

cam_js = []
for j, (t, sc, x, y, du, ease) in enumerate(plan["camera"]):
    if j == 0:
        cam_js.append(f'tl.fromTo("#cx-cam",{{scale:{sc},x:{x},y:{y}}},{{scale:{sc},x:{x},y:{y},duration:.01,ease:"none"}},0);')
    else:
        cam_js.append(f'tl.to("#cx-cam",{{scale:{sc},x:{x},y:{y},duration:{max(du, .01)},ease:"{ease}"}},{r(t)});')

shake_js = []
jit = [(1, -.6), (-.9, .8), (.7, .9), (-1, -.5), (.8, -.9), (-.6, .7), (.5, -.4), (-.3, .3), (0, 0)]
for t, amp in plan["shakes"]:
    for j, (dx, dy) in enumerate(jit):
        f = 1 - j / len(jit)
        shake_js.append(f'tl.to("#shake",{{x:{round(dx * amp * f, 1)},y:{round(dy * amp * f, 1)},duration:.035,ease:"none"}},{r(t + j * .035)});')

env = voice_envelope()
idle_n = int(D / 3.2)

stage = f"""<template id="stage-template">
  <style>
{FONTS}
    #root {{ position:absolute; inset:0; overflow:hidden; font-family:"Inter",sans-serif; color:#fff; }}
    #st-bg {{ position:absolute; inset:0; background:#0A0A0F; }}
    #aura {{ position:absolute; left:-260px; top:620px; width:1600px; height:1500px; background:
      radial-gradient(closest-side at 50% 52%, {PC}55, {PC}00 100%),
      radial-gradient(closest-side at 32% 70%, rgba(255,107,53,.30), rgba(255,107,53,0) 100%); }}
    #grid {{ position:absolute; inset:0; background-image: linear-gradient(rgba(255,255,255,.035) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,.035) 1px, transparent 1px); background-size:72px 72px; }}
    #shake {{ position:absolute; inset:0; }}
    .gz {{ position:absolute; left:{GZ['left']}px; top:{GZ['top']}px; width:{GZ['width']}px; height:{GZ['height']}px; }}
    #cx-cam {{ position:absolute; left:40px; top:930px; width:1000px; height:1000px; transform-origin:50% 26%; }}
    #cx-talk, #cx-idle, #cx-pop {{ position:absolute; inset:0; transform-origin:50% 100%; }}
    .pose {{ position:absolute; left:0; top:0; width:1000px; height:1000px; opacity:0; }}
    #cx-shadow {{ position:absolute; left:120px; top:880px; width:760px; height:160px; border-radius:50%; background:radial-gradient(closest-side, rgba(0,0,0,.55), rgba(0,0,0,0)); }}
    #grain {{ position:absolute; inset:-40px; background-image:url("assets/fx/grain.png"); background-size:512px 512px; opacity:.07; mix-blend-mode:screen; }}
    #vig {{ position:absolute; inset:0; background:radial-gradient(130% 80% at 50% 50%, rgba(0,0,0,0) 60%, rgba(0,0,0,.5) 100%); }}
{"".join(blocks_css)}
  </style>
  <div id="root" data-composition-id="stage" data-width="{W}" data-height="{H}" data-duration="{D}">
    <div id="st-bg" class="clip" data-start="0" data-duration="{D}" data-track-index="0"></div>
    <div id="aura"></div>
    <div id="grid"></div>
    <div id="shake">
      <div id="cx-cam">
        <div id="cx-shadow"></div>
        <div id="cx-idle"><div id="cx-talk"><div id="cx-pop">{pose_imgs}</div></div></div>
      </div>
      {"".join(blocks_html)}
    </div>
    <div id="vig"></div>
    <div id="grain"></div>
  </div>
  <script>
    (function () {{
      const tl = gsap.timeline({{ paused: true }});
      const ENV = {json.dumps(env)};
      const talk = document.getElementById("cx-talk");
      const pr = {{ f: 0 }};
      tl.fromTo(pr, {{ f: 0 }}, {{ f: ENV.length - 1, duration: ENV.length / 30, ease: "none", onUpdate() {{
        const e = ENV[Math.round(pr.f)] || 0;
        talk.style.transform = "translateY(" + (-6 * e).toFixed(2) + "px) scale(" + (1 + 0.012 * e).toFixed(4) + ")";
      }} }}, 0);
      tl.fromTo("#cx-idle", {{ rotation: -0.6, y: 0 }}, {{ rotation: 0.6, y: -6, duration: 3.2, ease: "sine.inOut", yoyo: true, repeat: {max(0, idle_n - 1)}, transformOrigin: "50% 100%" }}, 0);
      tl.fromTo("#aura", {{ x: -40, scale: 1 }}, {{ x: 40, scale: 1.08, duration: 5.5, ease: "sine.inOut", yoyo: true, repeat: {max(0, int(D / 5.5) - 1)} }}, 0);
      tl.fromTo("#grain", {{ backgroundPosition: "0px 0px" }}, {{ backgroundPosition: "{int(D * 12 * 173)}px {int(D * 12 * 97)}px", duration: {D}, ease: "steps({int(D * 12)})" }}, 0);
      {"".join(pose_js)}
      {"".join(cam_js)}
      {"".join(shake_js)}
      {"".join(blocks_js)}
      window.__timelines["stage"] = tl;
    }})();
  </script>
</template>
"""

# ------------------------------------------------------------------ captions
KW = {}
for color, lst in plan.get("keywords", {}).items():
    for wd in lst:
        KW[wd.lower()] = color


def norm(wd):
    return re.sub(r"[^\wàâäéèêëîïôöùûüç'-]", "", wd.lower())


ws = words["words"]
groups, cur = [], []
for j, w in enumerate(ws):
    cur.append(w)
    nxt = ws[j + 1] if j + 1 < len(ws) else None
    chars = sum(len(x["word"]) + 1 for x in cur)
    gap = (nxt["start"] - w["end"]) if nxt else 9
    punct = w["word"][-1] in ",.?:!"
    if not nxt or punct or len(cur) >= 3 or chars >= 16 or gap > 0.25 or (nxt and chars + len(nxt["word"]) > 20):
        groups.append(cur)
        cur = []

KCOL = sorted(set(KW.values()))
cap_html, cap_js = [], []
for g, grp in enumerate(groups):
    t0 = grp[0]["start"]
    t1 = groups[g + 1][0]["start"] if g + 1 < len(groups) else D - 0.1
    spans = []
    for w in grp:
        n = norm(w["word"])
        col = KW.get(n) or KW.get(n.rstrip("s"))
        cls = f' class="kw k{KCOL.index(col)}"' if col else ""
        spans.append(f'<span id="cw{w["i"]}"{cls}>{esc(w["word"])}</span>')
    # word gaps come from span margins, not whitespace (the renderer drops spaces next to styled spans)
    cap_html.append(f'<div class="cg" id="cg{g}"><p>{"".join(spans)}</p></div>')
    cap_js.append(f'tl.set("#cg{g}",{{opacity:1}},{r(t0)});tl.fromTo("#cg{g}",{{scale:.9,y:10}},{{scale:1,y:0,duration:.14,ease:"back.out(2)"}},{r(t0)});tl.set("#cg{g}",{{opacity:0}},{r(t1)});')
    for w in grp:
        n = norm(w["word"])
        kw = KW.get(n) or KW.get(n.rstrip("s"))
        cap_js.append(f'tl.fromTo("#cw{w["i"]}",{{opacity:.42}},{{opacity:1,duration:.06,ease:"none",immediateRender:false}},{r(w["start"])});')
        if kw:
            # pop up then settle; both legs start from scale 1 so a backward seek never leaves the word enlarged
            cap_js.append(f'tl.fromTo("#cw{w["i"]}",{{scale:1}},{{scale:1.16,duration:.06,ease:"power2.out",immediateRender:false}},{r(w["start"])});')
            cap_js.append(f'tl.fromTo("#cw{w["i"]}",{{scale:1.16}},{{scale:1,duration:.2,ease:"back.out(2)",immediateRender:false}},{r(w["start"] + .06)});')

captions = f"""<template id="captions-template">
  <style>
{FONTS}
    #root {{ position:absolute; inset:0; overflow:hidden; font-family:"Inter",sans-serif; }}
    .cg {{ position:absolute; left:76px; width:820px; top:740px; height:190px; display:flex; align-items:center; justify-content:center; opacity:0;
          font-weight:900; font-size:70px; line-height:1.04; letter-spacing:-.025em; color:#fff; text-align:center;
          text-shadow: 0 4px 0 #0A0A0F, 0 -2px 0 #0A0A0F, 3px 0 0 #0A0A0F, -3px 0 0 #0A0A0F, 0 0 28px rgba(0,0,0,.85); }}
    .cg p {{ display:block; width:100%; text-align:center; }}
    .cg span {{ display:inline-block; margin:0 .14em; opacity:.42; }}
{"".join(f"    .cg .k{j} {{ color:{c}; }}" + chr(10) for j, c in enumerate(KCOL))}
  </style>
  <div id="root" data-composition-id="captions" data-width="{W}" data-height="{H}" data-duration="{D}">
    {"".join(cap_html)}
  </div>
  <script>
    (function () {{
      const tl = gsap.timeline({{ paused: true }});
      {"".join(cap_js)}
      window.__timelines["captions"] = tl;
    }})();
  </script>
</template>
"""

# ------------------------------------------------------------------ index
aud = []
aud.append(f'<audio id="voice" src="assets/voice/voice.wav" data-start="0" data-duration="{words["duration"]}" data-track-index="10" data-volume="1"></audio>')
if os.path.exists(os.path.join(EP, "assets/audio/music.wav")):
    aud.append(f'<audio id="music" src="assets/audio/music.wav" data-start="0" data-duration="{D}" data-track-index="11" data-volume="1"></audio>')
if os.path.exists(os.path.join(EP, "assets/audio/sfx.wav")):
    aud.append(f'<audio id="sfx" src="assets/audio/sfx.wav" data-start="0" data-duration="{D}" data-track-index="12" data-volume="1"></audio>')

index = f"""<!doctype html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <title>{esc(plan.get("title", "CaliBodi short"))}</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
{FONTS}
      * {{ margin:0; padding:0; box-sizing:border-box; }}
      html, body {{ width:{W}px; height:{H}px; overflow:hidden; background:#0A0A0F; }}
      #root {{ position:relative; width:100%; height:100%; overflow:hidden; background:#0A0A0F; }}
      [data-composition-id="main"] > div[data-composition-src] {{ position:absolute; inset:0; }}
      #base {{ position:absolute; inset:0; background:#0A0A0F; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{D}" data-width="{W}" data-height="{H}">
      <div id="base" class="clip" data-start="0" data-duration="{D}" data-track-index="0"></div>
      <div id="el-stage" data-composition-id="stage" data-composition-src="compositions/stage.html" data-start="0" data-duration="{D}" data-track-index="1" data-track-kind="graphics" data-width="{W}" data-height="{H}"></div>
      <div id="el-captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{D}" data-track-index="2" data-track-kind="captions" data-width="{W}" data-height="{H}"></div>
      {chr(10).join("      " + a for a in aud).strip()}
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""

os.makedirs(os.path.join(EP, "compositions"), exist_ok=True)
open(os.path.join(EP, "compositions/stage.html"), "w").write(stage)
open(os.path.join(EP, "compositions/captions.html"), "w").write(captions)
open(os.path.join(EP, "index.html"), "w").write(index)
print(f"built {plan.get('title')} · {D}s · {len(plan['blocks'])} blocks · {len(groups)} caption groups · {len(plan['poses'])} poses")
