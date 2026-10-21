#!/usr/bin/env python3
"""Write the scenes of « Ton métabolisme ne ralentit pas à 40 ans » (compositions/scenes/*.html).

v3.1 look: Cobalt background that is never empty (ghost words drifting, set in build_v3.py), real footage in white
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


# ------------------------------------------------------------------ f01 hook: a match catches fire on « ÇA »
scene("f01-hook", 0.0, 1.80, """
#f01-l1 { position: absolute; left: 70px; top: 250px; color: #fff; }
#f01-l2 { position: absolute; left: 70px; top: 410px; color: #fff; }
#f01-l3 { position: absolute; left: 60px; top: 380px; font-size: 330px; }
""", lambda s: f"""
<div class="full"><div class="kb" id="f01-kb">{s.vid("match", 0, 1.80)}</div></div>
<div id="f01-l1" class="h1 shadowed" data-fit="940">Je parie que</div>
<div id="f01-l2" class="h1 shadowed" data-fit="940">tu ne savais pas</div>
<div id="f01-l3" class="h1"><span class="mk" id="f01-mk"><i></i><span>ÇA.</span></span></div>
""", """
K3.kb(tl, at, "#f01-kb", 0, 1.8, 1.0, 1.14);
K3.words(tl, at, W("f01-l1"), [0.26, 0.42, 0.66]);
K3.words(tl, at, W("f01-l2"), [0.74, 0.82, 0.90, 1.14]);
// the match catches fire on « ÇA »: the question is thrown off the top, ÇA lands in the flash
tl.fromTo(["#f01-l1", "#f01-l2"], { y: 0, opacity: 1 }, { y: -500, opacity: 0, duration: 0.22, ease: "power3.in", immediateRender: false }, at(1.26));
K3.slam(tl, at, "#f01-l3", 1.30, { from: 2.6, r: -4 });
K3.marker(tl, at, "#f01-mk", 1.42, 0.16);
K3.wobble(tl, at, "#f01-l3", 1.5, 2, 3);
""")

# ------------------------------------------------------------------ f02 « Ton métabolisme ne ralentit pas à 30… 40… 50 »
scene("f02-age", 1.80, 6.00, """
#f02-t1 { position: absolute; left: 70px; top: 220px; }
#f02-t2 { position: absolute; left: 60px; top: 330px; }
#f02-t3 { position: absolute; left: 70px; top: 500px; }
#f02-win { left: 120px; top: 660px; width: 840px; height: 460px; rotate: -3deg; }
#f02-note { position: absolute; left: 640px; top: 600px; font-size: 76px; color: var(--yel); rotate: -6deg; }
#f02-b { opacity: 0; }
#f02-lab { left: 50%; top: 1020px; font-size: 76px; translate: -50% 0; }
""", lambda s: f"""
<div id="f02-t1" class="h2">Ton</div>
<div id="f02-t2" class="h1" data-fit="960">MÉTABOLISME</div>
<div id="f02-t3" class="h2" data-fit="940"><span class="w">ne </span><span class="w">ralentit </span><span class="mk" id="f02-mk"><i></i><span>PAS</span></span></div>
<div class="win" id="f02-win"><div class="kb" id="f02-wk">{s.vid("fire", 1.80, 3.30)}</div></div>
<div id="f02-note" class="hand">= ton moteur</div>
<div class="full" id="f02-b"><div class="kb" id="f02-bk">
  <div class="slot" style="left:0">{s.vid("cand-3", 3.25, 4.10)}{s.vid("cand-4", 4.10, 5.02)}{s.vid("cand-5", 5.02, 6.00)}</div>
  <div class="slot" style="left:540px">{s.vid("cand-0", 3.25, 6.00)}</div>
  <div class="lab white" id="f02-lab">ne ralentit PAS</div>
</div></div>
""", """
K3.words(tl, at, W("f02-t1"), [1.86]);
K3.slam(tl, at, "#f02-t2", 1.94, { from: 2.2, r: -2 });
K3.toss(tl, at, "#f02-win", 2.05, { dx: 0, dy: 900, r0: -12 });
K3.kb(tl, at, "#f02-wk", 2.05, 3.3, 1.2, 1.0);
K3.write(tl, at, "#f02-note", 2.45, 0.4);
K3.words(tl, at, W("f02-t3"), [2.58, 2.69, 3.06]);
K3.marker(tl, at, "#f02-mk", 3.1, 0.14);
// hard cut to the birthday candles: 30… 40… 50
K3.cut(tl, at, "#f02-b", 3.25, true);
K3.cut(tl, at, ["#f02-t1", "#f02-t2", "#f02-t3", "#f02-win", "#f02-note"], 3.25, false);
K3.kb(tl, at, "#f02-bk", 3.25, 6.0, 1.0, 1.08);
K3.pop(tl, at, "#f02-lab", 3.45, { from: 0.5, r0: -6 });
""")

# ------------------------------------------------------------------ f03 the study: lab footage + paper card + calories burnt
scene("f03-etude", 6.00, 9.05, """
#f03-win { left: 60px; top: 240px; width: 960px; height: 600px; rotate: -2deg; }
#f03-card { left: 80px; top: 700px; width: 540px; height: 330px; rotate: -4deg; }
#f03-card .tape { left: 180px; top: -22px; rotate: 3deg; }
#f03-lab { position: absolute; left: 40px; top: 36px; font-family: "Montserrat", sans-serif; font-weight: 800; font-size: 30px; letter-spacing: .26em; color: #d63a2f; }
#f03-yr { position: absolute; left: 32px; top: 74px; font-size: 170px; }
#f03-sci { position: absolute; left: 44px; top: 250px; font-size: 56px; }
#f03-fire { left: 610px; top: 690px; width: 420px; height: 420px; }
#f03-c1 { left: 640px; top: 760px; font-size: 76px; rotate: -5deg; }
#f03-c2 { left: 700px; top: 860px; font-size: 76px; rotate: 3deg; }
#f03-src { position: absolute; left: 70px; top: 1100px; }
""", lambda s: f"""
<div class="win" id="f03-win"><div class="kb" id="f03-wk">{s.vid("lab", 6.0, 9.05)}</div></div>
<div class="paper" id="f03-card"><i class="tape"></i><div id="f03-lab">ÉTUDE</div><div id="f03-yr" class="h1">2021</div><div id="f03-sci" class="hand">publiée dans Science</div></div>
<div class="win round" id="f03-fire"><div class="kb" id="f03-fk">{s.vid("fire", 8.0, 9.05, ms=2)}</div></div>
<div class="lab" id="f03-c1">calories</div>
<div class="lab white" id="f03-c2">brûlées</div>
<div id="f03-src" class="foot">Source : Pontzer et al., Science, 2021</div>
""", """
K3.enter(tl, at, "#f03", 6.0);
K3.kb(tl, at, "#f03-wk", 6.0, 9.05, 1.18, 1.0, -30, 30);
K3.drop(tl, at, "#f03-card", 6.11, 0);
K3.slam(tl, at, "#f03-yr", 6.3, { from: 2.2 });
K3.write(tl, at, "#f03-sci", 7.15, 0.6);
K3.write(tl, at, "#f03-src", 7.4, 0.5);
K3.toss(tl, at, "#f03-fire", 8.0, { dx: 600, dy: 100, r0: 30 });
K3.kb(tl, at, "#f03-fk", 8.0, 9.05, 1.25, 1.0);
K3.slam(tl, at, "#f03-c1", 8.11, { from: 2.2, r: -5 });
K3.slam(tl, at, "#f03-c2", 8.43, { from: 2.2, r: 3 });
K3.exit(tl, at, "#f03", 8.83);
""")

# ------------------------------------------------------------------ f04 full bleed crowd: « plus de 6 400 personnes »
scene("f04-foule", 9.05, 10.80, """
#f04-a { left: 70px; top: 360px; font-size: 76px; }
#f04-n { left: 56px; top: 470px; font-size: 250px; font-variant-numeric: tabular-nums; }
#f04-p { left: 70px; top: 790px; font-size: 120px; }
""", lambda s: f"""
<div class="full"><div class="kb" id="f04-kb">{s.vid("crowd", 9.05, 10.80)}</div></div>
<div class="lab white" id="f04-a">plus de</div>
<div class="lab" id="f04-n"><span id="f04-num">0</span></div>
<div class="lab white" id="f04-p">PERSONNES</div>
""", """
K3.kb(tl, at, "#f04-kb", 9.05, 10.8, 1.16, 1.0);
K3.pop(tl, at, "#f04-a", 9.06, { from: 0.4, r0: -8 });
K3.pop(tl, at, "#f04-n", 9.12, { from: 0.4, r0: 6 });
K3.count(tl, at, W("f04-num"), 0, 6400, 9.15, 0.75);
K3.slam(tl, at, "#f04-p", 9.95, { from: 2.4, r: -3 });
""")

# ------------------------------------------------------------------ f05 globe « 29 pays » + « de 8 jours à 95 ans »
scene("f05-monde", 10.80, 13.75, """
#f05-globe { left: 230px; top: 220px; width: 620px; height: 620px; }
#f05-pays { left: 50%; top: 760px; font-size: 140px; translate: -50% 0; }
#f05-a { position: absolute; left: 70px; top: 960px; }
#f05-b { position: absolute; right: 70px; top: 960px; }
#f05-ru { position: absolute; left: 70px; top: 1060px; width: 940px; height: 60px; overflow: visible; }
""", lambda s: f"""
<div class="win round" id="f05-globe"><div class="kb" id="f05-gk">{s.vid("globe", 10.80, 13.75)}</div></div>
<div class="lab" id="f05-pays">29 PAYS</div>
<div id="f05-a" class="h2">8 jours</div>
<div id="f05-b" class="h2">95 ans</div>
<svg id="f05-ru" viewBox="0 0 940 60"><path id="f05-rl" class="doodle yel" d="M10 30 L930 30" /><path id="f05-rt" class="doodle" style="stroke-width:6" d="M10 10 V50 M195 18 V42 M380 18 V42 M565 18 V42 M750 18 V42 M930 10 V50" /></svg>
""", """
K3.enter(tl, at, "#f05", 10.8);
K3.kb(tl, at, "#f05-gk", 10.8, 13.75, 1.0, 1.08);
K3.slam(tl, at, "#f05-pays", 10.91, { from: 2.4, r: -3 });
K3.pop(tl, at, "#f05-a", 12.15, { from: 0.4, r0: -8 });
K3.draw(tl, at, "#f05-rl", 12.2, 0.4, "power2.inOut");
K3.draw(tl, at, "#f05-rt", 12.25, 0.4, "none");
K3.pop(tl, at, "#f05-b", 12.58, { from: 0.4, r0: 8 });
K3.exit(tl, at, "#f05", 13.52);
""")

# ------------------------------------------------------------------ f06 the curve: flat from 20 to 60
# chart coordinates: x = 90 + age/95*840 ; y = 620 - (v-60)*1.76 with v = energy in % of an adult (size-adjusted)
scene("f06-courbe", 13.75, 17.95, """
#f06-t { position: absolute; left: 70px; top: 210px; }
#f06-card { left: 50px; top: 350px; width: 980px; height: 760px; rotate: -1deg; }
#f06-svg { position: absolute; left: 0; top: 0; width: 980px; height: 720px; overflow: visible; }
#f06-y { position: absolute; left: 34px; top: 36px; font-family: "Montserrat", sans-serif; font-weight: 700; font-size: 26px; color: #555; letter-spacing: .04em; }
#f06-plate { left: 600px; top: 560px; font-size: 110px; background: var(--red); color: #fff; rotate: -8deg; }
#f06-bb { position: absolute; left: 120px; top: 120px; font-size: 52px; color: #d63a2f; rotate: -6deg; }
#f06-src { position: absolute; left: 40px; top: 716px; }
""", """
<div id="f06-t" class="h2">Résultat ?</div>
<div class="paper" id="f06-card">
  <div id="f06-y">MÉTABOLISME (à taille égale)</div>
  <svg id="f06-svg" viewBox="0 0 980 720">
    <rect id="f06-band" x="267" y="70" width="354" height="570" fill="#FFC93C" opacity=".55" />
    <path d="M90 640 L930 640" stroke="#141414" stroke-width="5" fill="none" />
    <g font-family="Montserrat" font-weight="700" font-size="28" fill="#555" text-anchor="middle">
      <text x="90" y="680">0</text><text x="444" y="680">40</text><text x="797" y="680">80</text><text x="930" y="680">95 ans</text>
    </g>
    <g font-family="Montserrat" font-weight="900" font-size="46" fill="#141414" text-anchor="middle">
      <text id="f06-a20" x="267" y="690">20</text><text id="f06-a60" x="621" y="690">60</text>
    </g>
    <path id="f06-curve" class="doodle" style="stroke:#141414;stroke-width:9" d="M90 444 C 92 300, 95 228, 99 224 C 120 222, 150 330, 190 380 C 225 420, 250 444, 267 444 L 621 444 C 700 452, 830 515, 930 550" />
    <path id="f06-flat" fill="none" stroke="#2B59C3" stroke-width="18" stroke-linecap="round" d="M267 444 L621 444" />
  </svg>
  <div id="f06-bb" class="hand">bébés ↓</div>
  <div id="f06-src" class="foot">Pontzer et al., Science, 2021 · dépense d'énergie ajustée à la taille du corps</div>
</div>
<div class="lab" id="f06-plate">PLATE.</div>
""", """
K3.enter(tl, at, "#f06", 13.75);
K3.words(tl, at, W("f06-t"), [13.80, 13.98]);
K3.drop(tl, at, "#f06-card", 13.9, 0, { y: -160 });
K3.draw(tl, at, "#f06-curve", 14.2, 0.85, "power1.inOut");
K3.write(tl, at, "#f06-bb", 14.45, 0.35);
tl.fromTo("#f06-band", { scaleX: 0, transformOrigin: "0% 50%" }, { scaleX: 1, duration: 0.4, ease: "power2.out" }, at(15.10));
K3.pop(tl, at, "#f06-a20", 15.32, { from: 0.3, r0: 0 });
K3.pop(tl, at, "#f06-a60", 15.56, { from: 0.3, r0: 0 });
K3.draw(tl, at, "#f06-flat", 16.84, 0.4, "power2.out");
K3.slam(tl, at, "#f06-plate", 17.42, { from: 2.6, r: -8 });
tl.fromTo("#f06-card", { scale: 1 }, { scale: 1.04, duration: 3.6, ease: "none", immediateRender: false }, at(14.1));
K3.exit(tl, at, "#f06", 17.72);
""")

# ------------------------------------------------------------------ f07 « À corps égal, tu brûles autant à 55 ans qu'à 25 »
scene("f07-corps", 17.95, 21.95, """
#f07-t { position: absolute; left: 70px; top: 210px; }
#f07-n { position: absolute; left: 76px; top: 330px; font-size: 66px; color: var(--yel); rotate: -3deg; }
#f07-w1 { left: 50px; top: 440px; width: 440px; height: 600px; rotate: -3deg; }
#f07-w2 { left: 590px; top: 440px; width: 440px; height: 600px; rotate: 3deg; }
#f07-l1 { left: 110px; top: 930px; font-size: 96px; rotate: -4deg; }
#f07-l2 { left: 650px; top: 930px; font-size: 96px; rotate: 3deg; }
#f07-eq { position: absolute; left: 470px; top: 640px; width: 140px; height: 120px; overflow: visible; }
""", lambda s: f"""
<div id="f07-t" class="h2" data-fit="940">À corps égal</div>
<div id="f07-n" class="hand">même muscle, même graisse</div>
<div class="win" id="f07-w1"><div class="kb" id="f07-k1">{s.vid("fire", 17.95, 21.95)}</div></div>
<div class="win" id="f07-w2"><div class="kb" id="f07-k2">{s.vid("fire", 17.96, 21.95, ms=3)}</div></div>
<svg id="f07-eq" viewBox="0 0 140 120"><path id="f07-eqp" class="doodle yel" style="stroke-width:20" d="M14 38 C 50 34, 90 40, 126 36 M14 84 C 50 80, 90 86, 126 82" /></svg>
<div class="lab" id="f07-l1">55 ans</div>
<div class="lab" id="f07-l2">25 ans</div>
""", """
K3.enter(tl, at, "#f07", 17.95);
K3.words(tl, at, W("f07-t"), [17.98, 18.12, 18.30]);
K3.write(tl, at, "#f07-n", 18.6, 0.6);
K3.toss(tl, at, "#f07-w1", 18.35, { dx: -700, dy: 200, r0: -30 });
K3.toss(tl, at, "#f07-w2", 18.5, { dx: 700, dy: 200, r0: 30 });
K3.kb(tl, at, "#f07-k1", 18.35, 21.95, 1.2, 1.0);
K3.kb(tl, at, "#f07-k2", 18.5, 21.95, 1.2, 1.0);
K3.draw(tl, at, "#f07-eqp", 19.58, 0.3);
K3.slam(tl, at, "#f07-l1", 19.97, { from: 2.4, r: -4 });
K3.slam(tl, at, "#f07-l2", 21.04, { from: 2.4, r: 3 });
K3.exit(tl, at, "#f07", 21.72);
""")

# ------------------------------------------------------------------ f08 « Il ne recommence à baisser qu'après 60 ans »
scene("f08-soixante", 21.95, 24.80, """
#f08-t1 { position: absolute; left: 70px; top: 300px; }
#f08-t2 { position: absolute; left: 70px; top: 420px; }
#f08-arr { position: absolute; left: 700px; top: 560px; width: 300px; height: 460px; overflow: visible; }
#f08-b { opacity: 0; }
#f08-lab { left: 50%; top: 1020px; font-size: 90px; translate: -50% 0; }
""", lambda s: f"""
<div id="f08-t1" class="h2" data-fit="940">Il ne recommence</div>
<div id="f08-t2" class="h2" data-fit="940">à baisser…</div>
<svg id="f08-arr" viewBox="0 0 300 460"><path id="f08-ap" class="doodle yel" style="stroke-width:16" d="M60 20 C 120 140, 120 260, 190 420 M120 380 L190 424 L232 350" /></svg>
<div class="full" id="f08-b"><div class="kb" id="f08-bk">
  <div class="slot" style="left:0">{s.vid("cand-6", 23.30, 24.80)}</div>
  <div class="slot" style="left:540px">{s.vid("cand-0", 23.30, 24.80, ms=1)}</div>
  <div class="lab" id="f08-lab">APRÈS 60 ANS</div>
</div></div>
""", """
K3.enter(tl, at, "#f08", 21.95);
K3.words(tl, at, W("f08-t1"), [22.07, 22.21, 22.32]);
K3.words(tl, at, W("f08-t2"), [22.79, 22.85]);
K3.draw(tl, at, "#f08-ap", 22.85, 0.4);
K3.cut(tl, at, "#f08-b", 23.30, true);
K3.kb(tl, at, "#f08-bk", 23.30, 24.8, 1.0, 1.08);
K3.slam(tl, at, "#f08-lab", 23.45, { from: 2.4, r: -3 });
""")

# ------------------------------------------------------------------ f09 « Et doucement : environ 0,7 % par an »
scene("f09-lent", 24.80, 27.95, """
#f09-t { position: absolute; left: 70px; top: 210px; }
#f09-n { left: 60px; top: 340px; font-size: 200px; font-variant-numeric: tabular-nums; }
#f09-p { position: absolute; left: 76px; top: 590px; }
#f09-svg { position: absolute; left: 0; top: 0; width: 1080px; height: 1150px; overflow: visible; }
#f09-a60 { position: absolute; left: 230px; top: 980px; }
#f09-a95 { position: absolute; left: 820px; top: 980px; white-space: nowrap; }
#f09-note { position: absolute; left: 610px; top: 650px; font-size: 62px; color: var(--yel); rotate: -5deg; }
""", """
<div id="f09-t" class="h2">Et doucement :</div>
<div class="lab" id="f09-n"><span id="f09-num">−0,0 %</span></div>
<div id="f09-p" class="h2">par an</div>
<svg id="f09-svg" viewBox="0 0 1080 1150">
  <path d="M90 960 L1000 960" stroke="rgba(255,255,255,.5)" stroke-width="5" fill="none" />
  <path id="f09-line" class="doodle yel" style="stroke-width:14" d="M90 790 L 300 790 C 520 800, 760 850, 980 900" />
</svg>
<div id="f09-a60" class="h3">60 ans</div>
<div id="f09-a95" class="h3">95 ans</div>
<div id="f09-note" class="hand">vers 90 ans : −26 %</div>
""", """
K3.enter(tl, at, "#f09", 24.8);
K3.words(tl, at, W("f09-t"), [24.85, 24.93]);
K3.draw(tl, at, "#f09-line", 25.0, 1.7, "none");
K3.pop(tl, at, "#f09-a60", 25.1, { from: 0.4, r0: 0 });
K3.pop(tl, at, "#f09-a95", 26.5, { from: 0.4, r0: 0 });
K3.pop(tl, at, "#f09-n", 25.75, { from: 0.4, r0: -6 });
K3.count(tl, at, W("f09-num"), 0, 0.7, 26.14, 0.5, (v) => "−" + v.toFixed(1).replace(".", ",") + " %");
K3.words(tl, at, W("f09-p"), [27.26, 27.44]);
K3.write(tl, at, "#f09-note", 26.9, 0.6);
K3.exit(tl, at, "#f09", 27.72);
""")

# ------------------------------------------------------------------ f10 « Et tu sais qui a le métabolisme le plus rapide ? »
scene("f10-rapide", 27.95, 31.05, """
#f10-t1 { position: absolute; left: 70px; top: 210px; }
#f10-t2 { position: absolute; left: 60px; top: 334px; }
#f10-t3 { position: absolute; left: 70px; top: 490px; }
#f10-g { position: absolute; left: 190px; top: 680px; width: 700px; height: 400px; overflow: visible; }
.f10-q { position: absolute; font-size: 150px; color: var(--yel); }
#f10-q1 { left: 70px; top: 760px; rotate: -14deg; } #f10-q2 { left: 900px; top: 700px; rotate: 12deg; }
""", """
<div id="f10-t1" class="h2" data-fit="940">Qui a le</div>
<div id="f10-t2" class="h1" data-fit="960">MÉTABOLISME</div>
<div id="f10-t3" class="h2" data-fit="940"><span class="w">le </span><span class="w">plus </span><span class="mk" id="f10-mk"><i></i><span>rapide ?</span></span></div>
<svg id="f10-g" viewBox="0 0 700 400">
  <path id="f10-arc" class="doodle" style="stroke-width:16" d="M70 360 A 280 280 0 0 1 630 360" />
  <path id="f10-red" fill="none" stroke="#FF5A4E" stroke-width="16" stroke-linecap="round" d="M548 162 A 280 280 0 0 1 630 360" />
  <path class="doodle" style="stroke-width:8" d="M110 250 L136 262 M200 140 L214 164 M350 92 V120 M500 140 L486 164 M590 250 L564 262" />
  <g id="f10-needle"><path d="M350 360 L350 130" stroke="#FFC93C" stroke-width="18" stroke-linecap="round" /><circle cx="350" cy="360" r="30" fill="#FFC93C" /></g>
  <text x="640" y="250" font-family="Montserrat" font-weight="900" font-size="44" fill="#FF5A4E">MAX</text>
</svg>
<div class="f10-q hand" id="f10-q1">?</div>
<div class="f10-q hand" id="f10-q2">?</div>
""", """
K3.enter(tl, at, "#f10", 27.95);
K3.words(tl, at, W("f10-t1"), [28.46, 28.64, 28.70]);
K3.slam(tl, at, "#f10-t2", 28.78, { from: 2.2, r: -2 });
K3.words(tl, at, W("f10-t3"), [29.38, 29.51, 29.62]);
K3.marker(tl, at, "#f10-mk", 29.7, 0.16);
K3.draw(tl, at, "#f10-arc", 28.2, 0.6);
K3.draw(tl, at, "#f10-red", 28.6, 0.3);
tl.fromTo("#f10-needle", { rotation: -80, svgOrigin: "350 360" }, { rotation: 40, duration: 0.9, ease: "power2.inOut" }, at(28.4));
tl.fromTo("#f10-needle", { rotation: 40 }, { rotation: 88, duration: 0.35, ease: "back.out(3)", immediateRender: false, svgOrigin: "350 360" }, at(29.62));
tl.fromTo("#f10-needle", { rotation: 88 }, { rotation: 80, duration: 0.08, ease: "sine.inOut", yoyo: true, repeat: 7, immediateRender: false, svgOrigin: "350 360" }, at(30.0));
K3.pop(tl, at, "#f10-q1", 29.9, { from: 0.3, r0: -40, r: -14 });
K3.pop(tl, at, "#f10-q2", 30.05, { from: 0.3, r0: 40, r: 12 });
K3.bob(tl, at, ".f10-q", 30.3, 31.05, 16, 0.35);
""")

# ------------------------------------------------------------------ f11 « Les bébés » (full bleed) then « +50 % »
scene("f11-bebes", 31.05, 35.95, """
#f11-l1 { left: 60px; top: 360px; font-size: 160px; }
#f11-l2 { left: 70px; top: 580px; font-size: 80px; }
#f11-b { position: absolute; inset: 0; opacity: 0; background: var(--bg); }
#f11-n { left: 60px; top: 250px; font-size: 230px; font-variant-numeric: tabular-nums; }
#f11-t { position: absolute; left: 70px; top: 540px; }
#f11-win { left: 520px; top: 660px; width: 470px; height: 470px; }
#f11-eg { position: absolute; left: 76px; top: 700px; font-size: 76px; color: var(--yel); rotate: -5deg; }
#f11-src { position: absolute; left: 70px; top: 1100px; }
""", lambda s: f"""
<div class="full"><div class="kb" id="f11-kb">{s.vid("baby", 31.05, 32.55)}</div></div>
<div class="lab" id="f11-l1">LES BÉBÉS.</div>
<div class="lab white" id="f11-l2">vers 1 an</div>
<div id="f11-b">
  <div class="lab" id="f11-n"><span id="f11-num">+0 %</span></div>
  <div id="f11-t" class="h3" data-fit="940">de plus qu'un adulte</div>
  <div class="win round" id="f11-win"><div class="kb" id="f11-wk">{s.vid("baby-wide", 32.55, 35.95, ms=0.2)}</div></div>
  <div id="f11-eg" class="hand">à taille égale</div>
  <div id="f11-src" class="foot">Dépense d'énergie ajustée à la taille du corps · Pontzer et al., 2021</div>
</div>
""", """
K3.kb(tl, at, "#f11-kb", 31.05, 32.55, 1.2, 1.0);
K3.slam(tl, at, "#f11-l1", 31.11, { from: 2.6, r: -3 });
K3.pop(tl, at, "#f11-l2", 31.83, { from: 0.4, r0: 8, r: 2 });
K3.cut(tl, at, "#f11-b", 32.55, true);
K3.cut(tl, at, ["#f11-l1", "#f11-l2"], 32.55, false);
K3.toss(tl, at, "#f11-win", 32.6, { dx: 600, dy: 300, r0: 30 });
K3.kb(tl, at, "#f11-wk", 32.6, 35.95, 1.25, 1.0);
K3.pop(tl, at, "#f11-n", 33.1, { from: 0.4, r0: -6 });
K3.count(tl, at, W("f11-num"), 0, 50, 33.2, 0.55, (v) => "+" + Math.round(v) + " %");
K3.words(tl, at, W("f11-t"), [33.87, 34.0, 34.24, 34.42]);
K3.write(tl, at, "#f11-eg", 34.96, 0.5);
K3.write(tl, at, "#f11-src", 35.1, 0.4);
K3.exit(tl, at, "#f11", 35.72);
""")

# ------------------------------------------------------------------ f12 « Alors pourquoi on prend du poids à 40 ans ? Probablement pas… »
scene("f12-quarante", 35.95, 39.85, """
#f12-t1 { position: absolute; left: 70px; top: 300px; }
#f12-t2 { position: absolute; left: 70px; top: 420px; }
#f12-q { position: absolute; left: 780px; top: 560px; font-size: 360px; color: var(--yel); rotate: 10deg; }
#f12-b { opacity: 0; }
#f12-lab { left: 50%; top: 1020px; font-size: 100px; translate: -50% 0; }
#f12-c { position: absolute; inset: 0; opacity: 0; background: var(--bg); }
#f12-c1 { position: absolute; left: 60px; top: 280px; }
#f12-c2 { position: absolute; left: 60px; top: 450px; font-size: 230px; }
#f12-c3 { position: absolute; left: 70px; top: 720px; }
#f12-c4 { position: absolute; left: 70px; top: 810px; }
#f12-st { position: absolute; left: 50px; top: 830px; width: 780px; height: 120px; overflow: visible; }
""", lambda s: f"""
<div id="f12-t1" class="h2" data-fit="940">Alors pourquoi</div>
<div id="f12-t2" class="h2" data-fit="940">on prend du poids</div>
<div id="f12-q" class="hand">?</div>
<div class="full" id="f12-b"><div class="kb" id="f12-bk">
  <div class="slot" style="left:0">{s.vid("cand-4", 37.05, 37.90, ms=1)}</div>
  <div class="slot" style="left:540px">{s.vid("cand-0", 37.05, 37.90, ms=2)}</div>
  <div class="lab" id="f12-lab">À 40 ANS ?</div>
</div></div>
<div id="f12-c">
  <div id="f12-c1" class="h1" data-fit="960">PROBABLEMENT</div>
  <div id="f12-c2" class="h1"><span class="mk" id="f12-mk"><i></i><span>PAS</span></span></div>
  <div id="f12-c3" class="h3">à cause du</div>
  <div id="f12-c4" class="h2" data-fit="900">métabolisme.</div>
  <svg id="f12-st" viewBox="0 0 780 120"><path id="f12-sp" class="doodle red" style="stroke-width:16" d="M10 80 C 200 50, 450 76, 770 30" /></svg>
</div>
""", """
K3.enter(tl, at, "#f12", 35.95);
K3.words(tl, at, W("f12-t1"), [36.02, 36.24]);
K3.words(tl, at, W("f12-t2"), [36.50, 36.57, 36.76, 36.89]);
K3.pop(tl, at, "#f12-q", 36.7, { from: 0.3, r0: -30, r: 10 });
K3.cut(tl, at, "#f12-b", 37.05, true);
K3.cut(tl, at, ["#f12-t1", "#f12-t2", "#f12-q"], 37.05, false);
K3.kb(tl, at, "#f12-bk", 37.05, 37.9, 1.0, 1.06);
K3.slam(tl, at, "#f12-lab", 37.13, { from: 2.4, r: -3 });
K3.cut(tl, at, "#f12-c", 37.90, true);
K3.slam(tl, at, "#f12-c1", 37.93, { from: 2.2, r: -2 });
K3.slam(tl, at, "#f12-c2", 38.49, { from: 2.6, r: -4 });
K3.marker(tl, at, "#f12-mk", 38.6, 0.14);
K3.words(tl, at, W("f12-c3"), [38.59, 38.65, 38.89]);
K3.words(tl, at, W("f12-c4"), [38.97]);
K3.draw(tl, at, "#f12-sp", 39.3, 0.25);
K3.exit(tl, at, "#f12", 39.62);
""")

# ------------------------------------------------------------------ f13 « la vie change : on bouge moins, on mange un peu plus, on perd du muscle »
scene("f13-vie", 39.85, 45.30, """
#f13-t1 { position: absolute; left: 70px; top: 200px; }
#f13-t2 { position: absolute; left: 70px; top: 270px; }
.f13-r { position: absolute; left: 70px; width: 600px; }
#f13-r1 { top: 470px; } #f13-r2 { top: 660px; } #f13-r3 { top: 850px; }
#f13-s1 { left: 660px; top: 430px; width: 380px; height: 194px; rotate: -12deg; }
#f13-s2 { left: 640px; top: 600px; width: 240px; height: 192px; rotate: 8deg; }
#f13-s3 { left: 830px; top: 650px; width: 210px; height: 170px; rotate: -10deg; }
#f13-s4 { left: 690px; top: 830px; width: 330px; height: 247px; rotate: 6deg; }
#f13-n { position: absolute; left: 80px; top: 975px; font-size: 66px; color: var(--yel); rotate: -3deg; }
""", """
<div id="f13-t1" class="h3">Plutôt parce que</div>
<div id="f13-t2" class="h2" data-fit="940">la vie change :</div>
<div class="f13-r h2" id="f13-r1" data-fit="580">on bouge moins</div>
<div class="f13-r h2" id="f13-r2" data-fit="580">on mange plus…</div>
<div class="f13-r h2" id="f13-r3" data-fit="580">on perd du muscle</div>
<div class="stk" id="f13-s1"><img src="assets/objects/obj-remote.png" alt="télécommande" /></div>
<div class="stk" id="f13-s2"><img src="assets/objects/obj-chips.png" alt="chips" /></div>
<div class="stk" id="f13-s3"><img src="assets/objects/obj-donut.png" alt="donut" /></div>
<div class="stk" id="f13-s4"><img src="assets/objects/obj-dumbbell.png" alt="haltères" /></div>
<div id="f13-n" class="hand">… si on ne s'entraîne pas</div>
""", """
K3.enter(tl, at, "#f13", 39.85);
K3.words(tl, at, W("f13-t1"), [39.94, 40.26, 40.42]);
K3.words(tl, at, W("f13-t2"), [40.53, 40.66, 40.74, 40.80]);
K3.words(tl, at, W("f13-r1"), [41.48, 41.62, 41.86]);
K3.toss(tl, at, "#f13-s1", 41.55, { dx: 700, dy: -100, r0: 40, r: -12 });
K3.words(tl, at, W("f13-r2"), [42.44, 42.50, 42.77]);
K3.toss(tl, at, "#f13-s2", 42.5, { dx: 700, dy: 60, r0: 50, r: 8 });
K3.toss(tl, at, "#f13-s3", 42.7, { dx: 600, dy: 160, r0: -50, r: -10 });
K3.words(tl, at, W("f13-r3"), [43.16, 43.24, 43.38, 43.55, 43.66]);
K3.toss(tl, at, "#f13-s4", 43.4, { dx: 700, dy: 200, r0: 30, r: 6 });
// the muscle « drops »: the dumbbells sag and shrink
tl.fromTo("#f13-s4", { scale: 1, rotation: 6, y: 0 }, { scale: 0.72, rotation: 24, y: 70, duration: 0.5, ease: "power2.in", immediateRender: false }, at(44.33));
K3.write(tl, at, "#f13-n", 44.12, 0.7);
K3.bob(tl, at, "#f13-s1", 42.1, 45.0, 10, 0.8);
K3.bob(tl, at, "#f13-s2", 43.2, 45.0, 12, 0.7);
K3.exit(tl, at, "#f13", 45.07);
""")

# ------------------------------------------------------------------ f14 yellow cut « La bonne nouvelle ? Tout ça, tu le contrôles. »
scene("f14-bonne", 45.30, 47.95, """
#f14 .h1, #f14 .h2 { color: var(--dark); }
#f14-t1 { position: absolute; left: 70px; top: 260px; }
#f14-t2 { position: absolute; left: 60px; top: 370px; }
#f14-t3 { position: absolute; left: 70px; top: 620px; }
#f14-t4 { position: absolute; left: 60px; top: 770px; }
#f14-t4 .mk > i { background: #fff; }
#f14-ck { position: absolute; left: 780px; top: 520px; width: 240px; height: 200px; overflow: visible; }
""", """
<div id="f14-t1" class="h2">La bonne</div>
<div id="f14-t2" class="h1" data-fit="960">nouvelle ?</div>
<div id="f14-t3" class="h2" data-fit="940">Tout ça, tu le</div>
<div id="f14-t4" class="h1" data-fit="960"><span class="mk" id="f14-mk"><i></i><span>CONTRÔLES.</span></span></div>
<svg id="f14-ck" viewBox="0 0 240 200"><path id="f14-cp" class="doodle" style="stroke:#141414;stroke-width:22" d="M20 110 L 90 180 L 226 22" /></svg>
""", """
K3.words(tl, at, W("f14-t1"), [45.39, 45.55]);
K3.slam(tl, at, "#f14-t2", 45.71, { from: 2.2, r: -2 });
K3.words(tl, at, W("f14-t3"), [46.59, 46.75, 46.91, 46.99]);
K3.slam(tl, at, "#f14-t4", 47.09, { from: 2.4, r: -3 });
K3.marker(tl, at, "#f14-mk", 47.2, 0.16);
K3.draw(tl, at, "#f14-cp", 47.25, 0.3);
""")

# ------------------------------------------------------------------ f15 three moves: walk / lift / track (hard cuts)
scene("f15-tips", 47.95, 52.45, """
.f15-p { position: absolute; inset: 0; opacity: 0; }
#f15-p1 { opacity: 1; }
#f15-p3 { background: var(--bg); }
.f15-p .badge { left: 70px; top: 250px; }
.f15-p .lab { left: 210px; top: 250px; font-size: 110px; }
#f15-x2 { left: 80px; top: 420px; font-size: 64px; }
#f15-ph { left: 330px; top: 420px; width: 420px; height: 720px; rotate: 4deg; }
#f15-cal { left: 210px; top: 250px; }
""", lambda s: f"""
<div class="f15-p" id="f15-p1">
  <div class="full"><div class="kb" id="f15-k1">{s.vid("walk", 47.95, 49.55)}</div></div>
  <div class="badge" id="f15-b1">1</div><div class="lab" id="f15-l1">MARCHE PLUS</div>
</div>
<div class="f15-p" id="f15-p2">
  <div class="full"><div class="kb" id="f15-k2">{s.vid("gym", 49.55, 51.20)}</div></div>
  <div class="badge" id="f15-b2">2</div><div class="lab" id="f15-l2">MUSCU</div>
  <div class="lab white" id="f15-x2">pour garder ton muscle</div>
</div>
<div class="f15-p" id="f15-p3">
  <div class="phone" id="f15-ph"><img src="assets/app/nutrition.jpg" alt="écran calories CaliBodi" /></div>
  <div class="badge" id="f15-b3">3</div><div class="lab" id="f15-cal" data-fit="780">SUIS TES CALORIES</div>
</div>
""", """
K3.kb(tl, at, "#f15-k1", 47.95, 49.55, 1.18, 1.0);
K3.pop(tl, at, "#f15-b1", 48.0, { from: 0.2, r0: -60 });
K3.slam(tl, at, "#f15-l1", 48.04, { from: 2.2, r: -3 });
K3.cut(tl, at, "#f15-p1", 49.55, false);
K3.cut(tl, at, "#f15-p2", 49.55, true);
K3.kb(tl, at, "#f15-k2", 49.55, 51.2, 1.18, 1.0);
K3.pop(tl, at, "#f15-b2", 49.6, { from: 0.2, r0: 60 });
K3.slam(tl, at, "#f15-l2", 49.67, { from: 2.2, r: 2 });
K3.pop(tl, at, "#f15-x2", 50.2, { from: 0.5, r0: -6, r: -2 });
K3.cut(tl, at, "#f15-p2", 51.20, false);
K3.cut(tl, at, "#f15-p3", 51.20, true);
K3.toss(tl, at, "#f15-ph", 51.22, { dx: 0, dy: 1000, r0: -10, r: 0 });
K3.pop(tl, at, "#f15-b3", 51.3, { from: 0.2, r0: -60 });
K3.slam(tl, at, "#f15-cal", 51.57, { from: 2.2, r: -3 });
""")

# ------------------------------------------------------------------ f16 CaliBodi: calories + programme in one place
scene("f16-app", 52.45, 55.85, """
#f16-logo { position: absolute; left: 70px; top: 214px; width: 124px; height: 124px; border-radius: 28px; box-shadow: 0 10px 24px rgba(0,0,0,.25); }
#f16-name { position: absolute; left: 220px; top: 226px; }
#f16-p1 { left: 110px; top: 400px; width: 352px; height: 690px; rotate: -5deg; }
#f16-p2 { left: 600px; top: 380px; width: 352px; height: 690px; rotate: 5deg; }
.f16-st { position: absolute; padding: 6px 22px 10px; background: var(--paper); border-radius: 8px; box-shadow: 0 8px 18px rgba(0,0,0,.25); font-size: 64px; color: #d63a2f; white-space: nowrap; }
#f16-s1 { left: 80px; top: 960px; rotate: -6deg; } #f16-s2 { left: 570px; top: 940px; rotate: 4deg; }
#f16-loop { position: absolute; left: 40px; top: 350px; width: 1000px; height: 790px; overflow: visible; }
""", """
<img id="f16-logo" src="assets/brand/icon-512.png" alt="CaliBodi" />
<div id="f16-name" class="h2">CaliBodi</div>
<div class="phone" id="f16-p1"><img src="assets/app/nutrition.jpg" alt="écran nutrition" /></div>
<div class="phone" id="f16-p2"><img src="assets/app/fitness.jpg" alt="écran programme" /></div>
<svg id="f16-loop" viewBox="0 0 1000 790" preserveAspectRatio="none"><path id="f16-lp" class="doodle yel" style="stroke-width:10" d="M120 60 C 300 0, 760 0, 930 70 C 1010 200, 1000 560, 930 720 C 760 790, 260 790, 80 720 C 0 560, 0 200, 80 90 C 100 70, 140 56, 190 50" /></svg>
<div class="f16-st hand" id="f16-s1">tes calories</div>
<div class="f16-st hand" id="f16-s2">ton programme</div>
""", """
K3.enter(tl, at, "#f16", 52.45);
K3.pop(tl, at, "#f16-logo", 52.53, { from: 0.2, r0: -30 });
K3.slam(tl, at, "#f16-name", 52.66, { from: 2.2, r: 0 });
tl.fromTo("#f16-p1", { y: 900, rotation: -10 }, { y: 0, rotation: 0, duration: 0.45, ease: "back.out(1.2)" }, at(53.1));
tl.fromTo("#f16-p2", { y: 900, rotation: 10 }, { y: 0, rotation: 0, duration: 0.45, ease: "back.out(1.2)" }, at(53.25));
K3.pop(tl, at, "#f16-s1", 53.9, { from: 0.4, r0: -16 });
tl.fromTo("#f16-p1", { scale: 1 }, { scale: 1.05, duration: 0.14, ease: "power2.out", yoyo: true, repeat: 1, immediateRender: false }, at(53.9));
K3.pop(tl, at, "#f16-s2", 54.54, { from: 0.4, r0: 16 });
tl.fromTo("#f16-p2", { scale: 1 }, { scale: 1.05, duration: 0.14, ease: "power2.out", yoyo: true, repeat: 1, immediateRender: false }, at(54.54));
K3.draw(tl, at, "#f16-lp", 55.0, 0.42);
K3.exit(tl, at, "#f16", 55.62);
""")

# ------------------------------------------------------------------ f17 call to action + « c'est l'âge » crossed out + end card
scene("f17-cta", 55.85, 68.62, """
#f17-a { position: absolute; left: 0; top: 0; width: 1080px; height: 1150px; }
.f17-row { position: absolute; left: 60px; width: 960px; height: 230px; }
#f17-r1 { top: 220px; } #f17-r2 { top: 470px; } #f17-r3 { top: 860px; }
.f17-ic { position: absolute; left: 0; top: 10px; width: 180px; height: 180px; border-radius: 50%; background: var(--paper); box-shadow: 0 12px 26px rgba(0,0,0,.25); }
.f17-ic svg { position: absolute; left: 28px; top: 28px; width: 124px; height: 124px; overflow: visible; }
.f17-ic .doodle { stroke: var(--dark); }
.f17-row .h2 { position: absolute; left: 220px; top: 14px; }
.f17-row .hand { position: absolute; left: 226px; top: 122px; font-size: 58px; color: var(--yel); white-space: nowrap; }
#f17-bub { left: 300px; top: 700px; font-size: 70px; rotate: -3deg; }
#f17-x { position: absolute; left: 290px; top: 670px; width: 560px; height: 170px; overflow: visible; }
#f17-b { position: absolute; left: 0; top: 0; width: 1080px; height: 1150px; }
#f17-logo { position: absolute; left: 400px; top: 230px; width: 280px; height: 280px; border-radius: 62px; box-shadow: 0 18px 40px rgba(0,0,0,.3); }
#f17-name { position: absolute; left: 0; width: 1080px; top: 540px; text-align: center; }
#f17-thx { position: absolute; left: 0; width: 1080px; top: 700px; text-align: center; font-size: 170px; color: var(--yel); rotate: -4deg; }
#f17-force { position: absolute; left: 0; width: 1080px; top: 930px; text-align: center; }
""", """
<div id="f17-a">
  <div class="f17-row" id="f17-r1">
    <div class="f17-ic"><svg viewBox="0 0 140 140"><path id="f17-hf" d="M70 124 C 30 96, 6 70, 10 42 C 14 18, 44 6, 70 34 C 96 6, 126 18, 130 42 C 134 70, 110 96, 70 124 Z" fill="#FF5A4E" /><path id="f17-hp" class="doodle" style="stroke-width:8" d="M70 124 C 30 96, 6 70, 10 42 C 14 18, 44 6, 70 34 C 96 6, 126 18, 130 42 C 134 70, 110 96, 70 124 Z" /></svg></div>
    <div class="h2" id="f17-t1">Like</div>
    <div class="hand" id="f17-n1">si tu accusais ton métabolisme…</div>
  </div>
  <div class="f17-row" id="f17-r2">
    <div class="f17-ic"><svg viewBox="0 0 140 140"><path id="f17-sp" class="doodle" style="stroke-width:9" d="M14 120 C 20 70, 50 44, 104 44 M84 18 L 122 44 L 84 72" /></svg></div>
    <div class="h2" id="f17-t2"><span class="mk" id="f17-mk2"><i></i><span>Partage</span></span></div>
    <div class="hand" id="f17-n2">à quelqu'un qui dit toujours :</div>
  </div>
  <div class="bubble" id="f17-bub">« c'est l'âge »</div>
  <svg id="f17-x" viewBox="0 0 560 170"><path id="f17-xp" class="doodle red" style="stroke-width:18" d="M20 20 L 540 150 M540 20 L 20 150" /></svg>
  <div class="f17-row" id="f17-r3">
    <div class="f17-ic"><svg viewBox="0 0 140 140"><path id="f17-pl" class="doodle red" style="stroke-width:14" d="M70 18 V122 M18 70 H122" /></svg></div>
    <div class="h2" id="f17-t3" data-fit="720"><span class="mk" id="f17-mk3"><i></i><span>Abonne-toi</span></span></div>
    <div class="hand" id="f17-n3">1 fait fitness vérifié / jour</div>
  </div>
</div>
<div id="f17-b">
  <img id="f17-logo" src="assets/brand/icon-512.png" alt="CaliBodi" />
  <div id="f17-name" class="h1">CaliBodi</div>
  <div id="f17-thx" class="hand">Merci !</div>
  <div id="f17-force" class="h3"><span class="w">ça nous donne beaucoup de </span><span class="mk" id="f17-mk4"><i></i><span>force</span></span></div>
</div>
""", """
K3.enter(tl, at, "#f17", 55.85);
// « Mets un like si tu accusais ton métabolisme… »
K3.pop(tl, at, "#f17-r1 .f17-ic", 55.98, { from: 0.3, r0: -20 });
K3.draw(tl, at, "#f17-hp", 56.0, 0.26);
tl.fromTo("#f17-hf", { scale: 0, svgOrigin: "70 70" }, { scale: 1, duration: 0.3, ease: "back.out(3)" }, at(56.19));
K3.slam(tl, at, "#f17-t1", 56.19, { from: 2.2, r: -2 });
K3.write(tl, at, "#f17-n1", 56.6, 0.9);
tl.fromTo("#f17-r1 .f17-ic", { scale: 1 }, { scale: 1.12, duration: 0.12, ease: "power2.out", yoyo: true, repeat: 3, immediateRender: false }, at(57.22));
// « …et partage à quelqu'un qui dit toujours « c'est l'âge » »
tl.fromTo("#f17-r1", { opacity: 1 }, { opacity: 0.4, duration: 0.2, ease: "none", immediateRender: false }, at(58.2));
K3.pop(tl, at, "#f17-r2 .f17-ic", 58.24, { from: 0.3, r0: 20 });
K3.draw(tl, at, "#f17-sp", 58.3, 0.3);
K3.slam(tl, at, "#f17-t2", 58.39, { from: 2.2, r: -2 });
K3.marker(tl, at, "#f17-mk2", 58.5, 0.18);
K3.write(tl, at, "#f17-n2", 58.73, 0.8);
K3.pop(tl, at, "#f17-bub", 60.48, { from: 0.3, r0: -12, r: -3 });
K3.draw(tl, at, "#f17-xp", 61.17, 0.25);
K3.wobble(tl, at, "#f17-bub", 61.45, 3, 3);
// « Abonne-toi : chaque jour, un nouveau fait fitness vérifié. »
tl.fromTo(["#f17-r2", "#f17-bub", "#f17-x"], { opacity: 1 }, { opacity: 0.4, duration: 0.2, ease: "none", immediateRender: false }, at(61.75));
K3.pop(tl, at, "#f17-r3 .f17-ic", 61.8, { from: 0.3, r0: -20 });
K3.draw(tl, at, "#f17-pl", 61.82, 0.24);
K3.slam(tl, at, "#f17-t3", 61.86, { from: 2.2, r: -2 });
K3.marker(tl, at, "#f17-mk3", 62.0, 0.18);
K3.write(tl, at, "#f17-n3", 62.97, 1.6);
tl.fromTo("#f17-r3 .f17-ic", { scale: 1 }, { scale: 1.12, duration: 0.12, ease: "power2.out", yoyo: true, repeat: 1, immediateRender: false }, at(64.81));
// end card « Merci, ça nous donne beaucoup de force ! »
tl.fromTo("#f17-a", { y: 0, opacity: 1 }, { y: -600, opacity: 0, duration: 0.26, ease: "power3.in", immediateRender: false }, at(65.45));
K3.pop(tl, at, "#f17-logo", 65.69, { from: 0.2, r0: -40, ease: "back.out(2.6)" });
K3.slam(tl, at, "#f17-name", 65.8, { from: 2, r: 0 });
K3.write(tl, at, "#f17-thx", 65.75, 0.5);
K3.words(tl, at, W("f17-force"), [66.02, 66.13, 66.34, 66.50, 66.74, 66.82]);
K3.marker(tl, at, "#f17-mk4", 66.9, 0.18);
tl.fromTo("#f17-b", { scale: 1 }, { scale: 1.05, duration: 2.9, ease: "none", immediateRender: false }, at(65.7));
""")

# canonical colour treatments (persisted by the HyperFrames CLI into data-color-grading)
import json, subprocess
GRADES = [("f15-tips", "#f15-v2", {"adjust": {"exposure": -0.35, "highlights": -0.3}})]   # bright gym wall behind white captions
for sid, sel, g in GRADES:
    subprocess.run(["npx", "hyperframes", "media-treatment", "--project", EP, "--file", f"compositions/scenes/{sid}.html",
                    "--selector", sel, "--grading", json.dumps(g), "--apply", "--json"], check=True, capture_output=True)
print("scenes written:", len(SC))
