#!/usr/bin/env python3
"""Write the scenes of « Éjaculation précoce : 3 faits » (compositions/scenes/*.html).

v3.1 look: Corail background that is never empty (ghost words drifting, set in build_v3.py), real footage in white
frames or full bleed with hard cuts, object stickers thrown in, white type, yellow marker, paper cards.
Every time below is a GLOBAL time (seconds in the voice); at() converts it to the scene's local time.
Run build_v3.py afterwards (it injects the fonts and wires the scenes).
"""
import os

EP = os.path.dirname(os.path.abspath(__file__))


def r(x):
    return round(x, 3)


class Scene:
    def __init__(self, sid, a, b):
        self.sid, self.a, self.b = sid, a, b
        self.p = sid.split("-")[0]           # id prefix, e.g. f01
        self.track = 0

    def vid(self, name, g0, g1, ms=0, cls=""):
        """framework-managed footage, visible from global g0 to g1 (local timing inside the scene)"""
        self.track += 1
        m = f' data-media-start="{ms}"' if ms else ""
        c = f' {cls}' if cls else ""
        return (f'<video id="{self.p}-v{self.track}" class="clip{c}" src="assets/clips/{name}.mp4" muted playsinline data-start="{r(max(0, g0 - self.a))}" '
                f'data-duration="{r(g1 - g0)}"{m} data-track-index="{self.track}"></video>')

    def write(self, css, html, js):
        out = f"""<!doctype html>
<html lang="fr">
  <head><meta charset="UTF-8" /></head>
  <body>
    <template>
      <link rel="stylesheet" href="assets/style/kit3.css" />
      <style>
        #root {{ position: absolute; inset: 0; overflow: hidden; }}
{css}
      </style>
      <div id="root" data-composition-id="{self.sid}" data-width="1080" data-height="1920" data-duration="{r(self.b - self.a)}">
        <div class="scene" id="{self.p}">
{html}
        </div>
      </div>
      <script>
        (function () {{
          const ID = "{self.sid}", at = K3.T({self.a});
          const W = (id) => document.getElementById(id);
          const build = () => {{
            const R = document.getElementById("{self.p}");
            K3.fit(R);
            const tl = gsap.timeline({{ paused: true }});
{js}
            window.__timelines[ID] = tl;
          }};
          document.fonts.ready.then(build);
        }})();
      </script>
    </template>
  </body>
</html>
"""
        open(os.path.join(EP, f"compositions/scenes/{self.sid}.html"), "w").write(out)


def ind(s, n):
    return "\n".join((" " * n + line) if line.strip() else line for line in s.strip("\n").split("\n"))


SC = []


def scene(sid, a, b, css, html, js):
    s = Scene(sid, a, b)
    h = html(s) if callable(html) else html
    s.write(ind(css, 8), ind(h, 10), ind(js, 12))
    SC.append(sid)


D = 79.2
YEL, DARK, COB = "#FFC93C", "#141414", "#1F3FA0"


def man(fill):
    """one pictogram man in a 100 x 100 box"""
    return (f'<circle cx="50" cy="22" r="17" fill="{fill}" />'
            f'<path d="M20 96 V64 C20 47 33 42 50 42 C67 42 80 47 80 64 V96 Z" fill="{fill}" />')


def men(pid, cols, n, cell, base="rgba(255,255,255,.38)", hi=YEL):
    """grid of n men: a base layer and a highlight layer (#pid-h{i}, hidden) to light up"""
    out = []
    for i in range(n):
        x, y, k = (i % cols) * cell, (i // cols) * cell, cell / 100
        out.append(f'<g transform="translate({x} {y}) scale({k:.3f})"><g class="mb" id="{pid}-b{i}">{man(base)}</g>'
                   f'<g class="mh" id="{pid}-h{i}" opacity="0">{man(hi)}</g></g>')
    return "".join(out)


def ids(pid, kind, rng):
    return "[" + ",".join(f'"#{pid}-{kind}{i}"' for i in rng) + "]"


def stopwatch(pid, size):
    ticks = "".join(f'<path d="M100 20 V34" transform="rotate({a} 100 112)" stroke="#141414" stroke-width="{6 if a % 90 == 0 else 3}" />' for a in range(0, 360, 30))
    return (f'<svg id="{pid}" viewBox="0 0 200 220" width="{size}" height="{size * 1.1:.0f}">'
            f'<rect x="88" y="0" width="24" height="18" rx="4" fill="#141414" /><rect x="94" y="14" width="12" height="12" fill="#141414" />'
            f'<circle cx="100" cy="112" r="92" fill="#FFFDF6" stroke="#141414" stroke-width="10" />{ticks}'
            f'<g id="{pid}-hand"><path d="M100 112 V36" stroke="{COB}" stroke-width="7" stroke-linecap="round" /></g>'
            f'<circle cx="100" cy="112" r="9" fill="#141414" /></svg>')


# ------------------------------------------------------------------ f01 hook: alarm clock by the pillow
scene("f01-hook", 0.0, 1.85, """
#f01-l1 { position: absolute; left: 70px; top: 330px; }
#f01-l2 { position: absolute; left: 60px; top: 500px; font-size: 190px; }
""", lambda s: f"""
<div class="full"><div class="kb" id="f01-kb">{s.vid("alarm", 0, 1.85)}</div></div>
<div id="f01-l1" class="h1 shadowed" data-fit="940">ÉJACULATION</div>
<div id="f01-l2" class="h1"><span class="mk" id="f01-mk"><i></i><span>PRÉCOCE</span></span></div>
""", """
K3.kb(tl, at, "#f01-kb", 0, 1.85, 1.0, 1.16);
K3.slam(tl, at, "#f01-l1", 0.19, { from: 2.4, r: -2 });
K3.slam(tl, at, "#f01-l2", 0.90, { from: 2.6, r: -4 });
K3.marker(tl, at, "#f01-mk", 1.0, 0.16);
K3.wobble(tl, at, "#f01-l2", 1.2, 2, 3);
""")

# ------------------------------------------------------------------ f02 « Trois faits… les deux premiers vont te rassurer, le troisième… reste jusqu'au bout »
scene("f02-trois", 1.85, 9.25, """
#f02-t { position: absolute; left: 70px; top: 200px; font-size: 190px; }
#f02-sub { position: absolute; left: 76px; top: 400px; font-size: 76px; }
.f02-c { top: 540px; width: 300px; height: 400px; }
#f02-c1 { left: 50px; rotate: -5deg; } #f02-c2 { left: 390px; rotate: 2deg; top: 520px; } #f02-c3 { left: 730px; rotate: 6deg; }
.f02-c .h1 { position: absolute; left: 0; right: 0; top: 70px; text-align: center; font-size: 200px; }
.f02-c svg { position: absolute; left: 70px; top: 270px; width: 160px; height: 110px; overflow: visible; }
#f02-q { position: absolute; inset: 0; border-radius: 10px; background: var(--yel); opacity: 0; }
#f02-q .h1 { top: 60px; font-size: 260px; }
#f02-sur { left: 470px; top: 960px; font-size: 64px; background: #fff; rotate: -6deg; }
#f02-bar { position: absolute; left: 70px; top: 1060px; width: 940px; height: 26px; border-radius: 13px; background: rgba(255,255,255,.3); overflow: hidden; }
#f02-fill { position: absolute; inset: 0; background: #fff; transform-origin: 0% 50%; transform: scaleX(0); }
#f02-end { position: absolute; left: 600px; top: 960px; font-size: 70px; }
""", """
<div id="f02-t" class="h1"><span class="mk" id="f02-mk"><i></i><span>3</span></span> FAITS</div>
<div id="f02-sub" class="hand">que presque personne ne te dit…</div>
<div class="paper f02-c" id="f02-c1"><div class="h1">1</div><svg viewBox="0 0 160 110"><path id="f02-k1" class="doodle" style="stroke:#1F3FA0;stroke-width:16" d="M14 58 L 58 100 L 146 10" /></svg></div>
<div class="paper f02-c" id="f02-c2"><div class="h1">2</div><svg viewBox="0 0 160 110"><path id="f02-k2" class="doodle" style="stroke:#1F3FA0;stroke-width:16" d="M14 58 L 58 100 L 146 10" /></svg></div>
<div class="paper f02-c" id="f02-c3"><div class="h1">3</div><div id="f02-q" data-layout-allow-overlap><div class="h1">?</div></div></div>
<div class="lab" id="f02-sur">va te surprendre</div>
<div id="f02-bar"><div id="f02-fill"></div></div>
<div id="f02-end" class="hand">jusqu'au bout →</div>
""", """
K3.slam(tl, at, "#f02-t", 1.94, { from: 2.4, r: -3 });
K3.marker(tl, at, "#f02-mk", 2.1, 0.14);
K3.write(tl, at, "#f02-sub", 2.42, 1.0);
K3.drop(tl, at, "#f02-c1", 2.5, 0, { y: -300 });
K3.drop(tl, at, "#f02-c2", 2.7, 0, { y: -300 });
K3.drop(tl, at, "#f02-c3", 2.9, 0, { y: -300 });
// « Les deux premiers vont te rassurer » : 1 and 2 get a tick
tl.fromTo(["#f02-c1", "#f02-c2"], { scale: 1 }, { scale: 1.08, duration: 0.14, ease: "power2.out", yoyo: true, repeat: 1, immediateRender: false }, at(4.43));
K3.draw(tl, at, "#f02-k1", 5.13, 0.2);
K3.draw(tl, at, "#f02-k2", 5.25, 0.2);
// « Le troisième va te surprendre » : 3 comes forward, turns yellow
tl.fromTo(["#f02-c1", "#f02-c2"], { opacity: 1 }, { opacity: 0.45, duration: 0.2, ease: "none", immediateRender: false }, at(6.1));
tl.fromTo("#f02-c3", { scale: 1, x: 0 }, { scale: 1.22, x: -40, duration: 0.3, ease: "back.out(2)", immediateRender: false }, at(6.11));
tl.fromTo("#f02-q", { opacity: 0 }, { opacity: 1, duration: 0.08, ease: "none" }, at(6.5));
K3.wobble(tl, at, "#f02-c3", 6.6, 4, 5);
K3.pop(tl, at, "#f02-sur", 6.79, { from: 0.4, r0: -16, r: -6 });
// « Reste jusqu'au bout » : the progress bar runs to the end
tl.fromTo("#f02-sur", { opacity: 1 }, { opacity: 0, duration: 0.12, ease: "none", immediateRender: false }, at(7.8));
tl.fromTo("#f02-fill", { scaleX: 0 }, { scaleX: 1, duration: 1.1, ease: "power2.inOut" }, at(7.88));
K3.write(tl, at, "#f02-end", 8.2, 0.5);
K3.exit(tl, at, "#f02", 9.03);
""")

# ------------------------------------------------------------------ f03 « Fait numéro un. Combien de temps dure un rapport ? »
scene("f03-fait1", 9.25, 12.2, """
#f03-lab { left: 70px; top: 210px; font-size: 120px; }
#f03-q1 { position: absolute; left: 70px; top: 390px; }
#f03-q2 { position: absolute; left: 70px; top: 500px; }
#f03-win { left: 140px; top: 650px; width: 800px; height: 420px; rotate: -3deg; }
#f03-qm { position: absolute; left: 860px; top: 600px; font-size: 200px; color: var(--yel); rotate: 10deg; }
""", lambda s: f"""
<div class="lab" id="f03-lab">FAIT N°1</div>
<div id="f03-q1" class="h2" data-fit="940">Combien de temps</div>
<div id="f03-q2" class="h2" data-fit="940">dure un rapport ?</div>
<div class="win" id="f03-win"><div class="kb" id="f03-wk">{s.vid("clocks", 9.25, 12.2)}</div></div>
<div id="f03-qm" class="hand">?</div>
""", """
K3.enter(tl, at, "#f03", 9.25);
K3.slam(tl, at, "#f03-lab", 9.40, { from: 2.4, r: -3 });
K3.toss(tl, at, "#f03-win", 9.75, { dx: 0, dy: 900, r0: -12, r: 0 });
K3.kb(tl, at, "#f03-wk", 9.75, 12.2, 1.2, 1.0);
K3.words(tl, at, W("f03-q1"), [10.37, 10.72, 10.85]);
K3.words(tl, at, W("f03-q2"), [11.09, 11.35, 11.36, 11.4]);
K3.pop(tl, at, "#f03-qm", 11.45, { from: 0.3, r0: -30, r: 10 });
K3.wobble(tl, at, "#f03-qm", 11.7, 6, 3);
K3.exit(tl, at, "#f03", 11.98);
""")

# ------------------------------------------------------------------ f04 the study: 500 couples, a stopwatch
scene("f04-etude", 12.2, 15.5, """
#f04-win { left: 60px; top: 200px; width: 960px; height: 520px; rotate: -2deg; }
#f04-card { left: 80px; top: 640px; width: 620px; height: 400px; rotate: -3deg; }
#f04-card .tape { left: 220px; top: -22px; rotate: 3deg; }
#f04-lab { position: absolute; left: 44px; top: 36px; font-family: "Montserrat", sans-serif; font-weight: 800; font-size: 30px; letter-spacing: .26em; color: #d63a2f; }
#f04-n { position: absolute; left: 36px; top: 76px; font-size: 190px; font-variant-numeric: tabular-nums; }
#f04-c { position: absolute; left: 44px; top: 250px; font-size: 76px; }
#f04-ch { position: absolute; left: 48px; top: 330px; font-size: 52px; }
#f04-sw { position: absolute; left: 730px; top: 700px; }
#f04-src { position: absolute; left: 70px; top: 1080px; }
""", lambda s: f"""
<div class="win" id="f04-win"><div class="kb" id="f04-wk">{s.vid("write", 12.2, 15.5)}</div></div>
<div class="paper" id="f04-card"><i class="tape"></i><div id="f04-lab">ÉTUDE · 5 PAYS</div><div id="f04-n" class="h1"><span id="f04-num">0</span></div><div id="f04-c" class="h2">couples</div><div id="f04-ch" class="hand">au chronomètre</div></div>
<div id="f04-swb">{stopwatch("f04-sw", 290)}</div>
<div id="f04-src" class="foot">Source : Waldinger et al., Journal of Sexual Medicine, 2005</div>
""", """
K3.enter(tl, at, "#f04", 12.2);
K3.kb(tl, at, "#f04-wk", 12.2, 15.5, 1.15, 1.0, -20, 20);
K3.drop(tl, at, "#f04-card", 13.3, 0);
K3.count(tl, at, W("f04-num"), 0, 500, 13.45, 0.5);
K3.pop(tl, at, "#f04-c", 13.98, { from: 0.4, r0: -6 });
K3.toss(tl, at, "#f04-sw", 14.4, { dx: 500, dy: 200, r0: 50 });
tl.fromTo("#f04-sw-hand", { rotation: 0, svgOrigin: "100 112" }, { rotation: 720, duration: 1.0, ease: "none" }, at(14.5));
K3.write(tl, at, "#f04-ch", 14.54, 0.5);
K3.write(tl, at, "#f04-src", 13.0, 0.6);
K3.exit(tl, at, "#f04", 15.28);
""")

# ------------------------------------------------------------------ f05 « Résultat : environ 5 minutes » (the seconds hand runs 5 laps)
scene("f05-cinq", 15.5, 17.75, """
#f05-t { position: absolute; left: 70px; top: 200px; }
#f05-swb { position: absolute; left: 240px; top: 300px; }
#f05-lab { left: 170px; top: 800px; font-size: 170px; }
#f05-src { position: absolute; left: 70px; top: 1080px; }
""", f"""
<div id="f05-t" class="h2">Résultat :</div>
<div id="f05-swb">{stopwatch("f05-sw", 600)}</div>
<div class="lab" id="f05-lab">≈ 5 MIN</div>
<div id="f05-src" class="foot">médiane : 5,4 min (Waldinger et al., 2005)</div>
""", """
K3.words(tl, at, W("f05-t"), [15.66]);
K3.pop(tl, at, "#f05-swb", 15.6, { from: 0.5, r0: -12 });
tl.fromTo("#f05-sw-hand", { rotation: 0, svgOrigin: "100 112" }, { rotation: 1800, duration: 1.1, ease: "power2.inOut" }, at(15.7));
K3.slam(tl, at, "#f05-lab", 16.74, { from: 2.6, r: -4 });
K3.wobble(tl, at, "#f05-swb", 16.8, 3, 3);
K3.write(tl, at, "#f05-src", 17.0, 0.4);
K3.exit(tl, at, "#f05", 17.55);
""")

# ------------------------------------------------------------------ f06 « Et ça varie énormément d'un homme à l'autre »
DOTS = [80, 120, 150, 190, 230, 280, 330, 390, 450, 520, 600, 690, 790, 880]
scene("f06-varie", 17.75, 20.1, """
#f06-t1 { position: absolute; left: 70px; top: 220px; }
#f06-t2 { position: absolute; left: 60px; top: 370px; }
#f06-card { left: 50px; top: 600px; width: 980px; height: 420px; rotate: -1deg; }
#f06-svg { position: absolute; left: 0; top: 0; width: 980px; height: 420px; overflow: visible; }
#f06-a { position: absolute; left: 40px; top: 250px; font-size: 90px; }
#f06-b { position: absolute; right: 40px; top: 250px; font-size: 90px; }
#f06-src { position: absolute; left: 40px; top: 370px; }
""", """
<div id="f06-t1" class="h2">ça varie</div>
<div id="f06-t2" class="h1" data-fit="960"><span class="mk" id="f06-mk"><i></i><span>ÉNORMÉMENT</span></span></div>
<div class="paper" id="f06-card">
  <svg id="f06-svg" viewBox="0 0 980 420">
    <path id="f06-line" class="doodle" style="stroke:#141414;stroke-width:8" d="M80 160 L900 160" />
    """ + "".join(f'<circle class="f06-d" cx="{x}" cy="160" r="20" fill="#1F3FA0" />' for x in DOTS) + """
  </svg>
  <div id="f06-a" class="h2">33 s</div>
  <div id="f06-b" class="h2">44 min</div>
  <div id="f06-src" class="foot">durées mesurées chez les 500 couples · Waldinger 2005</div>
</div>
""", """
K3.words(tl, at, W("f06-t1"), [17.91, 18.07]);
K3.slam(tl, at, "#f06-t2", 18.49, { from: 2.4, r: -3 });
K3.marker(tl, at, "#f06-mk", 18.6, 0.16);
K3.drop(tl, at, "#f06-card", 18.2, 0, { y: -200 });
K3.draw(tl, at, "#f06-line", 18.6, 0.6, "power2.inOut");
tl.fromTo(".f06-d", { scale: 0, transformOrigin: "50% 50%" }, { scale: 1, duration: 0.2, ease: "back.out(3)", stagger: 0.045 }, at(18.65));
K3.pop(tl, at, "#f06-a", 18.95, { from: 0.4, r0: -10 });
K3.pop(tl, at, "#f06-b", 19.29, { from: 0.4, r0: 10 });
K3.exit(tl, at, "#f06", 19.9);
""")

# ------------------------------------------------------------------ f07 fact 2: 100 men, 30 lit (self-report) then only 6 (medical definition)
scene("f07-fait2", 20.1, 32.4, """
#f07-lab { left: 70px; top: 200px; font-size: 110px; }
#f07-bub { left: 640px; top: 300px; font-size: 52px; rotate: 3deg; }
#f07-grid { position: absolute; left: 60px; top: 420px; width: 600px; height: 600px; overflow: visible; }
.f07-p { left: 690px; top: 470px; font-size: 140px; }
#f07-h30 { position: absolute; left: 696px; top: 640px; width: 360px; font-size: 64px; white-space: normal; }
#f07-def { left: 680px; top: 860px; width: 360px; height: 150px; rotate: 4deg; }
#f07-def .hand { position: absolute; left: 24px; top: 20px; font-size: 54px; color: #141414; }
#f07-h6 { position: absolute; left: 696px; top: 640px; width: 360px; font-size: 64px; }
.f07-src { position: absolute; left: 60px; top: 1070px; }
#f07-s2 { opacity: 0; }
""", """
<div class="lab" id="f07-lab">FAIT N°2</div>
<div class="bubble" id="f07-bub">trop rapide ?</div>
<svg id="f07-grid" viewBox="0 0 600 600">""" + men("f07", 10, 100, 60) + """</svg>
<div class="lab f07-p" id="f07-p30">30 %</div>
<div id="f07-h30" class="hand">disaient jouir trop vite</div>
<div class="paper" id="f07-def"><div class="hand">définition des médecins</div></div>
<div class="lab f07-p" id="f07-p6">6 %</div>
<div id="f07-h6" class="hand">vraiment concernés</div>
<div class="foot f07-src" id="f07-s1">≈ 30 % : enquête nationale américaine (1992)</div>
<div class="foot f07-src" id="f07-s2">≈ 6 % : définition médicale (ISSM), enquête en ligne américaine (2011)</div>
""", """
K3.enter(tl, at, "#f07", 20.1);
K3.slam(tl, at, "#f07-lab", 20.24, { from: 2.4, r: -3 });
// « Beaucoup d'hommes pensent avoir ce problème »
tl.fromTo("#f07 .mb", { opacity: 0, scale: 0.4, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: 0.16, ease: "back.out(2)", stagger: 0.006 }, at(21.44));
K3.pop(tl, at, "#f07-bub", 22.0, { from: 0.3, r0: -12, r: 3 });
// « environ 30 % disaient jouir trop vite »
tl.fromTo(""" + ids("f07", "h", range(30)) + """, { opacity: 0, scale: 0.4, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: 0.14, ease: "back.out(2.4)", stagger: 0.012 }, at(25.05));
K3.slam(tl, at, "#f07-p30", 25.05, { from: 2.4, r: -4 });
K3.write(tl, at, "#f07-h30", 25.45, 0.8);
K3.write(tl, at, "#f07-s1", 25.5, 0.5);
// « Mais selon la définition des médecins… seulement 6 % »
tl.fromTo("#f07-bub", { opacity: 1 }, { opacity: 0, duration: 0.15, ease: "none", immediateRender: false }, at(26.9));
K3.drop(tl, at, "#f07-def", 27.38, 4, { y: -200 });
tl.fromTo(""" + ids("f07", "h", range(29, 5, -1)) + """, { opacity: 1 }, { opacity: 0, duration: 0.1, ease: "none", stagger: 0.014, immediateRender: false }, at(29.06));
K3.cut(tl, at, ["#f07-p30", "#f07-h30", "#f07-s1"], 29.41, false);
K3.cut(tl, at, "#f07-s2", 29.41, true);
K3.slam(tl, at, "#f07-p6", 29.41, { from: 2.6, r: -4 });
K3.write(tl, at, "#f07-h6", 30.5, 0.5);
tl.fromTo(""" + ids("f07", "h", range(6)) + """, { scale: 1 }, { scale: 1.25, duration: 0.14, ease: "power2.out", yoyo: true, repeat: 3, transformOrigin: "50% 50%", immediateRender: false }, at(29.5));
K3.exit(tl, at, "#f07", 32.2);
""")

# ------------------------------------------------------------------ f08 yellow cut « Tu n'as donc peut-être pas de problème. »
scene("f08-ok", 32.4, 34.85, """
#f08 .h1, #f08 .h2 { color: var(--dark); }
#f08-t1 { position: absolute; left: 70px; top: 260px; }
#f08-t2 { position: absolute; left: 60px; top: 395px; }
#f08-t3 { position: absolute; left: 70px; top: 580px; }
#f08-t4 { position: absolute; left: 60px; top: 700px; }
#f08-t4 .mk > i { background: #fff; }
#f08-ck { position: absolute; left: 790px; top: 470px; width: 240px; height: 200px; overflow: visible; }
""", """
<div id="f08-t1" class="h2">Tu n'as donc</div>
<div id="f08-t2" class="h1" data-fit="960">PEUT-ÊTRE</div>
<div id="f08-t3" class="h2">PAS DE</div>
<div id="f08-t4" class="h1" data-fit="960"><span class="mk" id="f08-mk"><i></i><span>PROBLÈME.</span></span></div>
<svg id="f08-ck" viewBox="0 0 240 200"><path id="f08-cp" class="doodle" style="stroke:#141414;stroke-width:22" d="M20 110 L 90 180 L 226 22" /></svg>
""", """
K3.words(tl, at, W("f08-t1"), [32.51, 32.57, 32.74]);
K3.slam(tl, at, "#f08-t2", 32.98, { from: 2.2, r: -2 });
K3.words(tl, at, W("f08-t3"), [33.47, 33.63]);
K3.slam(tl, at, "#f08-t4", 33.71, { from: 2.4, r: -3 });
K3.marker(tl, at, "#f08-mk", 33.85, 0.16);
K3.draw(tl, at, "#f08-cp", 34.0, 0.3);
""")

# ------------------------------------------------------------------ f09 dark cut « Fait numéro trois. Celui que je t'ai promis. »
scene("f09-fait3", 34.85, 37.6, """
#f09-k { position: absolute; left: 0; width: 1080px; top: 230px; text-align: center; font-size: 110px; }
#f09-n { position: absolute; left: 0; width: 1080px; top: 330px; text-align: center; font-size: 640px; line-height: 1; color: var(--yel); }
#f09-p { position: absolute; left: 0; width: 1080px; top: 970px; text-align: center; font-size: 80px; color: var(--yel); }
#f09-flash { position: absolute; inset: 0; background: #fff; opacity: 0; }
""", """
<div id="f09-k" class="h2">FAIT N°</div>
<div id="f09-n" class="h1">3</div>
<div id="f09-p" class="hand">celui que je t'ai promis</div>
<div id="f09-flash"></div>
""", """
K3.words(tl, at, W("f09-k"), [34.91, 35.02]);
tl.fromTo("#f09-flash", { opacity: 0 }, { opacity: 0.85, duration: 0.04, ease: "none" }, at(35.37));
tl.fromTo("#f09-flash", { opacity: 0.85 }, { opacity: 0, duration: 0.3, ease: "power2.out", immediateRender: false }, at(35.41));
K3.slam(tl, at, "#f09-n", 35.39, { from: 3, r: -6 });
K3.wobble(tl, at, "#f09-n", 35.7, 3, 3);
K3.write(tl, at, "#f09-p", 36.19, 0.7);
tl.fromTo("#f09-n", { scale: 1 }, { scale: 1.08, duration: 1.6, ease: "none", immediateRender: false }, at(35.9));
""")

# ------------------------------------------------------------------ f10 doctors tested pelvic-floor exercises (drawn diagram, no body footage)
scene("f10-bassin", 37.6, 41.0, """
#f10-win { left: 60px; top: 200px; width: 960px; height: 460px; rotate: -2deg; }
#f10-med { left: 100px; top: 580px; font-size: 76px; background: #fff; rotate: -4deg; }
#f10-card { left: 90px; top: 560px; width: 900px; height: 500px; rotate: 1deg; }
#f10-svg { position: absolute; left: 0; top: 0; width: 900px; height: 500px; overflow: visible; }
#f10-ex { position: absolute; left: 40px; top: 30px; font-size: 72px; }
#f10-lab { left: 230px; top: 380px; font-size: 64px; rotate: -2deg; }
#f10-src { position: absolute; left: 70px; top: 1080px; }
""", lambda s: f"""
<div class="win" id="f10-win"><div class="kb" id="f10-wk">{s.vid("xray", 37.6, 41.0)}</div></div>
<div class="lab" id="f10-med">des médecins</div>
<div class="paper" id="f10-card">
  <div id="f10-ex" class="hand">exercices</div>
  <svg id="f10-svg" viewBox="0 0 900 500">
    <path id="f10-bowl" class="doodle" style="stroke:#141414;stroke-width:12" d="M210 90 C 190 200, 260 330, 450 350 C 640 330, 710 200, 690 90" />
    <g id="f10-hm"><path id="f10-hp" fill="none" stroke="#FFC93C" stroke-width="34" stroke-linecap="round" d="M290 270 C 360 330, 540 330, 610 270" /></g>
    <path id="f10-ar" class="doodle" style="stroke:#1F3FA0;stroke-width:10" d="M450 250 V150 M415 185 L450 150 L485 185" />
  </svg>
  <div class="lab" id="f10-lab">MUSCLES DU BASSIN</div>
</div>
<div id="f10-src" class="foot">Source : Pastore et al., Therapeutic Advances in Urology, 2014</div>
""", """
K3.enter(tl, at, "#f10", 37.6);
K3.kb(tl, at, "#f10-wk", 37.6, 41.0, 1.15, 1.0);
K3.pop(tl, at, "#f10-med", 37.91, { from: 0.4, r0: -14, r: -4 });
// « …des exercices pour les muscles du bassin »
K3.drop(tl, at, "#f10-card", 38.84, 1, { y: 700 });
K3.write(tl, at, "#f10-ex", 39.09, 0.4);
K3.draw(tl, at, "#f10-bowl", 39.2, 0.4);
K3.draw(tl, at, "#f10-hp", 39.5, 0.3);
K3.slam(tl, at, "#f10-lab", 39.83, { from: 2.2, r: -2 });
// contract / relax: the muscle hammock lifts twice
tl.fromTo("#f10-hm", { y: 0 }, { y: -50, duration: 0.25, ease: "power2.out", yoyo: true, repeat: 3, immediateRender: false }, at(40.0));
K3.draw(tl, at, "#f10-ar", 40.0, 0.25);
K3.write(tl, at, "#f10-src", 38.9, 0.6);
K3.exit(tl, at, "#f10", 40.82);
""")

# ------------------------------------------------------------------ f11 40 men, 12 weeks → 33 out of 40
scene("f11-quarante", 41.0, 47.95, """
.f11-l { left: 60px; top: 205px; font-size: 100px; }
#f11-cal { position: absolute; left: 70px; top: 360px; width: 940px; height: 70px; }
.f11-w { position: absolute; top: 0; width: 66px; height: 66px; border-radius: 10px; background: var(--paper); box-shadow: 0 6px 14px rgba(0,0,0,.2); }
.f11-w svg { position: absolute; inset: 8px; overflow: visible; }
#f11-sem { position: absolute; left: 760px; top: 222px; font-size: 68px; rotate: -4deg; }
#f11-grid { position: absolute; left: 100px; top: 470px; width: 880px; height: 550px; overflow: visible; }
#f11-ok { position: absolute; left: 70px; top: 360px; font-size: 76px; opacity: 0; }
#f11-src { position: absolute; left: 70px; top: 1070px; }
""", """
<div class="lab f11-l" id="f11-l40"><span id="f11-num">0</span> HOMMES</div>
<div id="f11-cal">""" + "".join(f'<div class="f11-w" style="left:{i * 78}px"><svg viewBox="0 0 50 50"><path id="f11-t{i}" class="doodle" style="stroke:#1F3FA0;stroke-width:9" d="M6 26 L 20 40 L 44 8" /></svg></div>' for i in range(12)) + """</div>
<div id="f11-sem" class="hand">12 semaines</div>
<svg id="f11-grid" viewBox="0 0 880 550">""" + men("f11", 8, 40, 110) + """</svg>
<div class="lab f11-l" id="f11-l33">33 SUR 40</div>
<div id="f11-ok" class="hand">contrôlaient mieux leur éjaculation</div>
<div id="f11-src" class="foot">Pastore 2014 · 40 hommes · rééducation du plancher pelvien</div>
""", """
K3.enter(tl, at, "#f11", 41.0);
K3.slam(tl, at, "#f11-l40", 41.08, { from: 2.2, r: -3 });
K3.count(tl, at, W("f11-num"), 0, 40, 41.1, 0.5);
tl.fromTo("#f11 .mb", { opacity: 0, scale: 0.4, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: 0.16, ease: "back.out(2)", stagger: 0.012 }, at(41.2));
// « pendant 12 semaines »: the weeks get ticked off
tl.fromTo(".f11-w", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.18, ease: "back.out(2)", stagger: 0.03 }, at(42.2));
""" + "\n".join(f'K3.draw(tl, at, "#f11-t{i}", {42.55 + i * 0.07:.2f}, 0.12);' for i in range(12)) + """
K3.write(tl, at, "#f11-sem", 42.52, 0.5);
K3.write(tl, at, "#f11-src", 42.0, 0.5);
// « À la fin, 33 hommes sur 40… »
tl.fromTo(["#f11-cal", "#f11-sem"], { opacity: 1 }, { opacity: 0, duration: 0.15, ease: "none", immediateRender: false }, at(44.4));
K3.cut(tl, at, "#f11-l40", 44.6, false);
K3.slam(tl, at, "#f11-l33", 44.6, { from: 2.4, r: -3 });
tl.fromTo(""" + ids("f11", "h", range(33)) + """, { opacity: 0, scale: 0.4, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: 0.14, ease: "back.out(2.4)", stagger: 0.022 }, at(44.65));
tl.set("#f11-ok", { opacity: 1 }, at(46.13));
K3.write(tl, at, "#f11-ok", 46.13, 0.9);
K3.exit(tl, at, "#f11", 47.75);
""")

# ------------------------------------------------------------------ f12 « 30 secondes → 2 minutes et demie. Sans médicament. »
scene("f12-duree", 47.95, 52.5, """
#f12-t { position: absolute; left: 70px; top: 200px; }
#f12-card { left: 60px; top: 340px; width: 960px; height: 420px; rotate: -1deg; }
.f12-r { position: absolute; left: 40px; font-family: "Montserrat", sans-serif; font-weight: 900; font-size: 40px; letter-spacing: .12em; color: #555; }
#f12-r1 { top: 40px; } #f12-r2 { top: 220px; }
.f12-b { position: absolute; left: 40px; height: 80px; border-radius: 14px; transform-origin: 0% 50%; }
#f12-b1 { top: 100px; width: 150px; background: #c9c3b8; }
#f12-b2 { top: 280px; width: 750px; background: var(--yel); box-shadow: inset 0 0 0 4px #141414; }
.f12-v { position: absolute; font-size: 76px; color: #141414; }
#f12-n1 { left: 214px; top: 100px; } #f12-n2 { left: 560px; top: 168px; font-size: 92px; color: #d63a2f; rotate: -4deg; }
#f12-pw { left: 560px; top: 800px; width: 460px; height: 300px; rotate: 4deg; }
#f12-x { position: absolute; left: 560px; top: 790px; width: 460px; height: 320px; overflow: visible; }
#f12-sm { left: 60px; top: 880px; font-size: 76px; rotate: -3deg; }
""", lambda s: f"""
<div id="f12-t" class="h2">Leur durée</div>
<div class="paper" id="f12-card">
  <div class="f12-r" id="f12-r1">AVANT</div><div class="f12-b" id="f12-b1"></div><div class="hand f12-v" id="f12-n1">30 s</div>
  <div class="f12-r" id="f12-r2">APRÈS 12 SEMAINES</div><div class="f12-b" id="f12-b2"></div><div class="hand f12-v" id="f12-n2">2 min 30</div>
</div>
<div class="win" id="f12-pw"><div class="kb" id="f12-pk">{s.vid("pills", 51.2, 52.5)}</div></div>
<svg id="f12-x" viewBox="0 0 460 320"><path id="f12-xp" class="doodle" style="stroke:#141414;stroke-width:20" d="M30 30 L 430 290 M430 30 L 30 290" /></svg>
<div class="lab" id="f12-sm">SANS MÉDICAMENT</div>
""", """
K3.enter(tl, at, "#f12", 47.95);
K3.words(tl, at, W("f12-t"), [48.13, 48.37]);
K3.drop(tl, at, "#f12-card", 48.5, 0, { y: -200 });
K3.pop(tl, at, "#f12-r1", 48.9, { from: 0.6, r0: 0 });
tl.fromTo("#f12-b1", { scaleX: 0 }, { scaleX: 1, duration: 0.3, ease: "power2.out" }, at(49.25));
K3.pop(tl, at, "#f12-n1", 49.57, { from: 0.4, r0: -10 });
K3.pop(tl, at, "#f12-r2", 49.9, { from: 0.6, r0: 0 });
tl.fromTo("#f12-b2", { scaleX: 0 }, { scaleX: 1, duration: 0.6, ease: "power2.inOut" }, at(50.04));
K3.slam(tl, at, "#f12-n2", 50.47, { from: 2.4, r: -4 });
// « Sans médicament. »
K3.toss(tl, at, "#f12-pw", 51.2, { dx: 600, dy: 200, r0: 30, r: 0 });
K3.kb(tl, at, "#f12-pk", 51.2, 52.5, 1.2, 1.0);
K3.draw(tl, at, "#f12-xp", 51.45, 0.25);
K3.slam(tl, at, "#f12-sm", 51.38, { from: 2.4, r: -3 });
K3.exit(tl, at, "#f12", 52.3);
""")

# ------------------------------------------------------------------ f13 caution: small study, 13 seen again at 6 months
scene("f13-prudence", 52.5, 59.45, """
#f13-tri { position: absolute; left: 70px; top: 200px; width: 190px; height: 170px; overflow: visible; }
#f13-t { position: absolute; left: 290px; top: 230px; }
#f13-lab { left: 70px; top: 430px; font-size: 120px; }
#f13-card { left: 70px; top: 620px; width: 940px; height: 420px; rotate: -1deg; }
#f13-grid { position: absolute; left: 40px; top: 40px; width: 860px; height: 86px; overflow: visible; }
#f13-rev { position: absolute; left: 40px; top: 150px; font-size: 64px; }
#f13-mg { position: absolute; left: 40px; top: 250px; width: 130px; height: 130px; overflow: visible; }
#f13-big { position: absolute; left: 190px; top: 270px; font-size: 64px; }
#f13-src { position: absolute; left: 70px; top: 1070px; }
""", """
<svg id="f13-tri" viewBox="0 0 190 170"><path d="M95 10 L 182 160 L 8 160 Z" fill="#FFC93C" stroke="#141414" stroke-width="10" stroke-linejoin="round" /><path d="M95 60 V112" stroke="#141414" stroke-width="16" stroke-linecap="round" /><circle cx="95" cy="138" r="9" fill="#141414" /></svg>
<div id="f13-t" class="h2">Attention :</div>
<div class="lab" id="f13-lab">PETITE ÉTUDE</div>
<div class="paper" id="f13-card">
  <svg id="f13-grid" viewBox="0 0 860 86">""" + men("f13", 20, 40, 43, base="#c9c3b8", hi=COB) + """</svg>
  <div id="f13-rev" class="h3">13 sur 40 revus à 6 mois</div>
  <svg id="f13-mg" viewBox="0 0 130 130"><circle cx="54" cy="54" r="40" fill="none" stroke="#141414" stroke-width="12" /><path d="M84 84 L 120 120" stroke="#141414" stroke-width="16" stroke-linecap="round" /></svg>
  <div id="f13-big" class="hand">il faut des études plus grandes</div>
</div>
<div id="f13-src" class="foot">Pastore et al., 2014 · étude sans groupe témoin</div>
""", """
K3.enter(tl, at, "#f13", 52.5);
K3.pop(tl, at, "#f13-tri", 52.63, { from: 0.3, r0: -20 });
K3.wobble(tl, at, "#f13-tri", 52.9, 6, 5);
K3.words(tl, at, W("f13-t"), [52.63]);
K3.slam(tl, at, "#f13-lab", 54.06, { from: 2.4, r: -3 });
K3.drop(tl, at, "#f13-card", 54.6, 0, { y: -200 });
tl.fromTo("#f13 .mb", { opacity: 0 }, { opacity: 1, duration: 0.1, ease: "none", stagger: 0.008 }, at(54.7));
// « seulement 13 hommes ont été revus 6 mois plus tard »
tl.fromTo(""" + ids("f13", "h", range(13)) + """, { opacity: 0, scale: 0.4, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: 0.14, ease: "back.out(2.4)", stagger: 0.03 }, at(55.5));
K3.pop(tl, at, "#f13-rev", 56.55, { from: 0.6, r0: -3 });
// « Il faut des études plus grandes »
K3.pop(tl, at, "#f13-mg", 57.85, { from: 0.3, r0: -40 });
K3.write(tl, at, "#f13-big", 58.07, 0.8);
tl.fromTo("#f13-mg", { scale: 1 }, { scale: 1.3, duration: 0.2, ease: "power2.out", yoyo: true, repeat: 1, immediateRender: false }, at(58.55));
K3.write(tl, at, "#f13-src", 55.0, 0.5);
K3.exit(tl, at, "#f13", 59.28);
""")

# ------------------------------------------------------------------ f14 « Si ça te gêne vraiment, parles-en à un médecin. »
scene("f14-medecin", 59.45, 62.55, """
#f14-h { position: absolute; left: 70px; top: 300px; font-size: 84px; color: #fff; }
#f14-a { left: 70px; top: 420px; font-size: 130px; }
#f14-b { left: 70px; top: 590px; font-size: 110px; }
""", lambda s: f"""
<div class="full"><div class="kb" id="f14-kb">{s.vid("xray", 59.45, 62.55, ms=4.4)}</div></div>
<div id="f14-h" class="hand shadowed">si ça te gêne vraiment,</div>
<div class="lab" id="f14-a">PARLES-EN</div>
<div class="lab white" id="f14-b">à un médecin</div>
""", """
K3.kb(tl, at, "#f14-kb", 59.45, 62.55, 1.0, 1.14);
K3.write(tl, at, "#f14-h", 59.59, 0.8);
K3.slam(tl, at, "#f14-a", 60.96, { from: 2.4, r: -3 });
K3.slam(tl, at, "#f14-b", 61.55, { from: 2.4, r: 2 });
""")

# ------------------------------------------------------------------ f15 the question: 1, 2 or 3?
scene("f15-question", 62.55, 68.35, """
#f15-t1 { position: absolute; left: 70px; top: 200px; }
#f15-t2 { position: absolute; left: 60px; top: 310px; }
#f15-t3 { position: absolute; left: 70px; top: 470px; }
.f15-c { top: 620px; width: 300px; height: 340px; }
#f15-c1 { left: 50px; rotate: -5deg; } #f15-c2 { left: 390px; rotate: 2deg; top: 600px; } #f15-c3 { left: 730px; rotate: 6deg; }
.f15-c .badge { left: 90px; top: -50px; }
.f15-c .h2 { position: absolute; left: 0; right: 0; top: 110px; text-align: center; font-size: 72px; white-space: nowrap; }
.f15-c .hand { position: absolute; left: 0; right: 0; top: 220px; text-align: center; font-size: 46px; }
#f15-bub { left: 200px; top: 1010px; font-size: 56px; }
""", """
<div id="f15-t1" class="h2">Quel fait te</div>
<div id="f15-t2" class="h1" data-fit="960"><span class="mk" id="f15-mk"><i></i><span>SURPREND</span></span></div>
<div id="f15-t3" class="h2">le plus ?</div>
<div class="paper f15-c" id="f15-c1"><div class="badge">1</div><div class="h2">≈ 5 min</div><div class="hand">la durée moyenne</div></div>
<div class="paper f15-c" id="f15-c2"><div class="badge">2</div><div class="h2">6 %</div><div class="hand">vraiment concernés</div></div>
<div class="paper f15-c" id="f15-c3"><div class="badge">3</div><div class="h2">33/40</div><div class="hand">sans médicament</div></div>
<div class="bubble" id="f15-bub">Réponds : 1, 2 ou 3</div>
""", """
K3.enter(tl, at, "#f15", 62.55);
K3.words(tl, at, W("f15-t1"), [62.64, 62.80, 63.04]);
K3.slam(tl, at, "#f15-t2", 63.16, { from: 2.2, r: -3 });
K3.marker(tl, at, "#f15-mk", 63.3, 0.16);
K3.words(tl, at, W("f15-t3"), [63.52, 63.60]);
K3.drop(tl, at, "#f15-c1", 64.62, 0, { y: -260 });
K3.drop(tl, at, "#f15-c2", 65.33, 0, { y: -260 });
K3.drop(tl, at, "#f15-c3", 66.05, 0, { y: -260 });
K3.pop(tl, at, "#f15-bub", 66.89, { from: 0.3, r0: -10, r: -2 });
K3.wobble(tl, at, "#f15-bub", 67.62, 3, 3);
K3.exit(tl, at, "#f15", 68.15);
""")

# ------------------------------------------------------------------ f16 share / subscribe, the app, end card calibodi.com
scene("f16-cta", 68.35, D, """
#f16-a { position: absolute; left: 0; top: 0; width: 1080px; height: 1150px; }
.f16-row { position: absolute; left: 60px; width: 960px; height: 230px; }
#f16-r1 { top: 260px; } #f16-r2 { top: 620px; }
.f16-ic { position: absolute; left: 0; top: 10px; width: 180px; height: 180px; border-radius: 50%; background: var(--paper); box-shadow: 0 12px 26px rgba(0,0,0,.25); }
.f16-ic svg { position: absolute; left: 28px; top: 28px; width: 124px; height: 124px; overflow: visible; }
.f16-ic .doodle { stroke: var(--dark); }
.f16-row .h2 { position: absolute; left: 220px; top: 14px; }
.f16-row .hand { position: absolute; left: 226px; top: 122px; font-size: 58px; color: var(--yel); white-space: nowrap; }
#f16-b { position: absolute; left: 0; top: 0; width: 1080px; height: 1150px; opacity: 0; }
.f16-ph { top: 300px; width: 320px; height: 620px; }
#f16-p1 { left: 40px; rotate: -6deg; } #f16-p2 { left: 380px; top: 280px; } #f16-p3 { left: 720px; rotate: 6deg; }
.f16-pl { position: absolute; top: 950px; width: 360px; text-align: center; font-size: 62px; }
#f16-l1 { left: 20px; } #f16-l2 { left: 360px; } #f16-l3 { left: 700px; }
#f16-c { position: absolute; left: 0; top: 0; width: 1080px; height: 1150px; opacity: 0; }
#f16-logo { position: absolute; left: 400px; top: 230px; width: 280px; height: 280px; border-radius: 62px; box-shadow: 0 18px 40px rgba(0,0,0,.3); }
#f16-name { position: absolute; left: 0; width: 1080px; top: 540px; text-align: center; }
#f16-url { left: 225px; top: 740px; font-size: 96px; }
#f16-st { position: absolute; left: 0; width: 1080px; top: 900px; text-align: center; font-size: 64px; color: #fff; }
""", """
<div id="f16-a">
  <div class="f16-row" id="f16-r1">
    <div class="f16-ic"><svg viewBox="0 0 140 140"><path id="f16-sp" class="doodle" style="stroke-width:9" d="M14 120 C 20 70, 50 44, 104 44 M84 18 L 122 44 L 84 72" /></svg></div>
    <div class="h2"><span class="mk" id="f16-mk1"><i></i><span>Partage</span></span></div>
    <div class="hand" id="f16-n1">à quelqu'un qui doit l'entendre</div>
  </div>
  <div class="f16-row" id="f16-r2">
    <div class="f16-ic"><svg viewBox="0 0 140 140"><path id="f16-pl" class="doodle" style="stroke-width:14;stroke:#1F3FA0" d="M70 18 V122 M18 70 H122" /></svg></div>
    <div class="h2" data-fit="720"><span class="mk" id="f16-mk2"><i></i><span>Abonne-toi</span></span></div>
    <div class="hand" id="f16-n2">3 faits vérifiés, chaque jour</div>
  </div>
</div>
<div id="f16-b">
  <div class="phone f16-ph" id="f16-p1"><img src="assets/app/fitness.jpg" alt="écran entraînements CaliBodi" /></div>
  <div class="phone f16-ph" id="f16-p2"><img src="assets/app/sleep.jpg" alt="écran sommeil CaliBodi" /></div>
  <div class="phone f16-ph" id="f16-p3"><img src="assets/app/nutrition.jpg" alt="écran alimentation CaliBodi" /></div>
  <div class="hand f16-pl" id="f16-l1">entraînements</div>
  <div class="hand f16-pl" id="f16-l2">sommeil</div>
  <div class="hand f16-pl" id="f16-l3">alimentation</div>
</div>
<div id="f16-c">
  <img id="f16-logo" src="assets/brand/icon-512.png" alt="CaliBodi" />
  <div id="f16-name" class="h1">CaliBodi</div>
  <div class="lab" id="f16-url">calibodi.com</div>
  <div id="f16-st" class="hand">Play Store · App Store</div>
</div>
""", """
K3.enter(tl, at, "#f16", 68.35);
// « Partage cette vidéo à quelqu'un qui doit l'entendre, et abonne-toi. »
K3.pop(tl, at, "#f16-r1 .f16-ic", 68.45, { from: 0.3, r0: -20 });
K3.draw(tl, at, "#f16-sp", 68.5, 0.3);
K3.slam(tl, at, "#f16-r1 .h2", 68.5, { from: 2.2, r: -2 });
K3.marker(tl, at, "#f16-mk1", 68.65, 0.18);
K3.write(tl, at, "#f16-n1", 69.56, 0.9);
tl.fromTo("#f16-r1", { opacity: 1 }, { opacity: 0.4, duration: 0.2, ease: "none", immediateRender: false }, at(70.9));
K3.pop(tl, at, "#f16-r2 .f16-ic", 70.95, { from: 0.3, r0: 20 });
K3.draw(tl, at, "#f16-pl", 71.0, 0.24);
K3.slam(tl, at, "#f16-r2 .h2", 71.02, { from: 2.2, r: -2 });
K3.marker(tl, at, "#f16-mk2", 71.15, 0.18);
K3.write(tl, at, "#f16-n2", 71.3, 0.6);
// « Pour suivre tes entraînements, ton sommeil et ton alimentation… »
tl.fromTo("#f16-a", { y: 0, opacity: 1 }, { y: -600, opacity: 0, duration: 0.26, ease: "power3.in", immediateRender: false }, at(71.85));
K3.cut(tl, at, "#f16-b", 72.1, true);
K3.toss(tl, at, "#f16-p1", 72.6, { dx: -600, dy: 600, r0: -30, r: 0 });
K3.write(tl, at, "#f16-l1", 72.77, 0.5);
K3.toss(tl, at, "#f16-p2", 73.62, { dx: 0, dy: 900, r0: 20, r: 0 });
K3.write(tl, at, "#f16-l2", 73.79, 0.4);
K3.toss(tl, at, "#f16-p3", 74.28, { dx: 600, dy: 600, r0: 30, r: 0 });
K3.write(tl, at, "#f16-l3", 74.45, 0.5);
// « …découvre CaliBodi sur calibodi.com »
tl.fromTo("#f16-b", { y: 0, opacity: 1 }, { y: -700, opacity: 0, duration: 0.26, ease: "power3.in", immediateRender: false }, at(75.62));
K3.cut(tl, at, "#f16-c", 75.85, true);
K3.pop(tl, at, "#f16-logo", 75.9, { from: 0.2, r0: -40, ease: "back.out(2.6)" });
K3.slam(tl, at, "#f16-name", 76.25, { from: 2, r: 0 });
K3.slam(tl, at, "#f16-url", 77.05, { from: 2.4, r: -3 });
K3.write(tl, at, "#f16-st", 77.6, 0.6);
tl.fromTo("#f16-c", { scale: 1 }, { scale: 1.05, duration: 3.3, ease: "none", immediateRender: false }, at(75.9));
""")

# canonical colour treatments (persisted by the HyperFrames CLI into data-color-grading)
import json, subprocess
GRADES = [("f14-medecin", "#f14-v1", {"adjust": {"exposure": -0.3, "highlights": -0.35}})]   # bright X-ray light box behind the labels
for sid, sel, g in GRADES:
    subprocess.run(["npx", "hyperframes", "media-treatment", "--project", EP, "--file", f"compositions/scenes/{sid}.html",
                    "--selector", sel, "--grading", json.dumps(g), "--apply", "--json"], check=True, capture_output=True)
print("scenes written:", len(SC))
