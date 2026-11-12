# Footage: objects, places, clocks, feet and bikes (no women, no faces).
# hands and figures seen from behind only (no women, no faces, nothing sexual).


def src(sid, text, t):
    """small source line under the progress bar"""
    return (f'<div class="src" id="{sid}-src">Source : {text}</div>', "",
            f'tl.fromTo("#{sid}-src",{{opacity:0}},{{opacity:1,duration:.3,ease:"none"}},at({t}));')


def man(fill):
    return (f'<circle cx="50" cy="22" r="17" fill="{fill}" />'
            f'<path d="M20 96 V64 C20 47 33 42 50 42 C67 42 80 47 80 64 V96 Z" fill="{fill}" />')


def doc(fill):
    return (f'<path d="M18 4 H62 L84 26 V96 H18 Z" fill="{fill}" />'
            f'<path d="M30 44 H72 M30 58 H72 M30 72 H60" stroke="#141414" stroke-width="6" stroke-linecap="round" opacity=".5" />')


def row(sid, shape, n, hi, cell, y, fill="rgba(255,255,255,.35)"):
    """n icons in a row centred on the frame; the first `hi` light up (ids #sid-i0…)"""
    x0 = (1080 - n * cell) / 2
    g = "".join(f'<g transform="translate({x0 + i * cell:.0f} 0) scale({cell / 100 * .9:.3f})"><g class="ic" id="{sid}-i{i}">{shape(fill)}</g>'
                f'<g class="ih" id="{sid}-h{i}" opacity="0">{shape("#9B6BFF")}</g></g>' for i in range(n))
    return f'<svg class="row" id="{sid}-row" viewBox="0 0 1080 {cell}" style="top:{y}px;height:{cell}px">{g}</svg>'


def hi_js(sid, n, t, stagger=.08):
    ids = ",".join(f'"#{sid}-h{i}"' for i in range(n))
    return f'tl.fromTo([{ids}],{{opacity:0,scale:.3,transformOrigin:"50% 50%"}},{{opacity:1,scale:1,duration:.2,ease:"back.out(3)",stagger:{stagger}}},at({t}));'


def acc(*parts):
    """merge accent pieces (html, css, js)"""
    return "".join(p[0] for p in parts), "".join(p[1] for p in parts), "".join(p[2] for p in parts)


def lab(sid, name, text, css, t, white=False, out=None):
    js = f'tl.fromTo("#{sid}-{name}",{{scale:2.4,opacity:0,rotation:-6}},{{scale:1,opacity:1,rotation:-3,duration:.24,ease:"power4.out"}},at({t}));'
    if out:
        js += f'tl.fromTo("#{sid}-{name}",{{opacity:1}},{{opacity:0,duration:.2,ease:"none",immediateRender:false}},at({out}));'
    return (f'<div class="lab{" white" if white else ""}" id="{sid}-{name}">{text}</div>', f"#{sid}-{name} {{ {css} }}", js)


def big(sid, name, text, css, t, out=None):
    js = f'tl.fromTo("#{sid}-{name}",{{scale:2.8,opacity:0}},{{scale:1,opacity:1,duration:.26,ease:"power4.out"}},at({t}));'
    if out:
        js += f'tl.fromTo("#{sid}-{name}",{{opacity:1}},{{opacity:0,duration:.2,ease:"none",immediateRender:false}},at({out}));'
    return (f'<div class="big" id="{sid}-{name}">{text}</div>', f"#{sid}-{name} {{ {css} }}", js)


def tag(sid, name, text, css, t, out=None):
    js = f'tl.fromTo("#{sid}-{name}",{{y:50,opacity:0}},{{y:0,opacity:1,duration:.3,ease:"back.out(2)"}},at({t}));'
    if out:
        js += f'tl.fromTo("#{sid}-{name}",{{opacity:1}},{{opacity:0,duration:.2,ease:"none",immediateRender:false}},at({out}));'
    return (f'<div class="tag" id="{sid}-{name}">{text}</div>', f"#{sid}-{name} {{ {css} }}", js)


def sources(sid, text, t):
    return src(sid, text, t)


def bubble(sid, name, text, css, t):
    return (f'<div class="bub" id="{sid}-{name}">{text}</div>',
            f"#{sid}-{name} {{ position: absolute; {css} padding: 22px 40px 28px; border-radius: 40px; background: #fff; color: #141414; font-family: \"Montserrat\", sans-serif; font-weight: 900; font-size: 64px; line-height: 1.02; box-shadow: 0 18px 40px rgba(0,0,0,.45); }}",
            f'tl.fromTo("#{sid}-{name}",{{scale:0,rotation:-10,transformOrigin:"20% 100%"}},{{scale:1,rotation:-2,duration:.35,ease:"back.out(2.4)"}},at({t}));')


C = "left: 0; width: 1080px; text-align: center;"
SH = "text-shadow: 0 20px 60px rgba(0,0,0,.65);"
ML = "white-space: normal; line-height: 1;"
# Shot list of « proteines », read by build_v4.py. Global times in seconds (voice of 2026-11-13).
# Footage: gym (man seen from behind), shaker + dumbbells photo, blender with powder, eggs, chicken, clocks, milkshake photo (no women, no faces, no logos).
A = "#9B6BFF"
SHOTS = [
    ("s1", "dos1", 0.00, 2.40, None, *acc(
        tag("s1", "a", "TU TERMINES", f"{C} top: 250px; font-size: 80px; color: #fff;", 0.18),
        lab("s1", "b", "TA SÉANCE", "left: 200px; top: 380px; font-size: 120px;", 0.82))),
    ("s2", "barre", 2.40, 4.47, "whip", *acc(
        tag("s2", "a", "TES PROTÉINES", f"{C} top: 250px; font-size: 80px; color: #fff;", 2.42),
        lab("s2", "b", "MUSCLES ?", "left: 200px; top: 380px; font-size: 120px;", 3.58))),
    ("s3", "horloge", 4.47, 7.88, "zoom", *acc(
        tag("s3", "a", "TU SAIS QUOI ?", f"{C} top: 250px; font-size: 80px; color: #fff;", 4.51, out=5.5),
        tag("s3", "b", "PAS DU TOUT", f"{C} top: 250px; font-size: 84px; color: #fff;", 6.43),
        lab("s3", "c", "PRESSÉ", "left: 250px; top: 400px; font-size: 140px;", 6.91))),
    ("s4", "oeuf1", 7.88, 10.30, "flash", *acc(
        tag("s4", "a", "ON T'A SOUVENT DIT", f"{C} top: 250px; font-size: 62px; color: #fff;", 7.97),
        big("s4", "n", "30", f"left: 330px; top: 420px; font-size: 330px; color: {A}; {SH}", 9.80),
        lab("s4", "m", "MINUTES", "left: 230px; top: 760px; font-size: 110px;", 10.12, white=True))),
    ("s5", "dos2", 10.30, 12.75, "whip", *acc(
        tag("s5", "a", "APRÈS LE SPORT", f"{C} top: 250px; font-size: 76px; color: #fff;", 10.38),
        lab("s5", "b", "MUSCLE", "left: 250px; top: 400px; font-size: 140px;", 11.76))),
    ("s6", "lait", 12.75, 15.11, "zoom", *acc(
        tag("s6", "a", "POURTANT", f"{C} top: 250px; font-size: 90px; color: #fff;", 12.77),
        lab("s6", "b", "PAS AUSSI SIMPLE", "left: 100px; top: 400px; font-size: 72px;", 13.99))),
    ("s7", "poulet", 15.11, 17.90, "flash", *acc(
        tag("s7", "a", "TON CORPS CONTINUE", f"{C} top: 250px; font-size: 62px; color: #fff;", 15.17),
        lab("s7", "b", "PROTÉINES", "left: 180px; top: 380px; font-size: 110px;", 16.62),
        lab("s7", "c", "RÉPARER", "left: 250px; top: 560px; font-size: 120px;", 17.34, white=True))),
    ("s8", "decoupe", 17.90, 20.61, "whip", *acc(
        tag("s8", "a", "CONSTRUIRE", f"{C} top: 250px; font-size: 90px; color: #fff;", 18.06),
        lab("s8", "b", "TES MUSCLES", "left: 150px; top: 380px; font-size: 110px;", 18.57),
        tag("s8", "c", "APRÈS TA SÉANCE", f"{C} top: 560px; font-size: 66px; color: #fff;", 19.28))),
    ("s9", "blender", 20.61, 23.60, "zoom", *acc(
        tag("s9", "a", "CE QUI COMPTE", f"{C} top: 250px; font-size: 78px; color: #fff;", 20.71),
        lab("s9", "b", "SURTOUT", "left: 250px; top: 380px; font-size: 130px;", 21.11),
        lab("s9", "c", "LA QUANTITÉ", "left: 150px; top: 560px; font-size: 100px;", 21.94, white=True))),
    ("s10", "shaker", 23.60, 27.04, "flash", *acc(
        tag("s10", "a", "SUR TOUTE LA JOURNÉE", f"{C} top: 250px; font-size: 54px; color: #fff;", 23.84),
        lab("s10", "b", "SHAKER", "left: 250px; top: 380px; font-size: 140px;", 25.41),
        lab("s10", "c", "RÉPÉTITION", "left: 180px; top: 580px; font-size: 100px;", 26.56, white=True))),
    ("s11", "stress", 27.04, 30.20, "whip", *acc(
        tag("s11", "a", "ARRÊTE DE STRESSER", f"{C} top: 250px; font-size: 62px; color: #fff;", 28.43),
        lab("s11", "b", "30 MINUTES", "left: 200px; top: 400px; font-size: 110px;", 29.38))),
    ("s12", "dos3", 30.20, 32.43, "zoom", *acc(
        tag("s12", "a", "CONCENTRE-TOI", f"{C} top: 250px; font-size: 84px; color: #fff;", 30.27),
        lab("s12", "b", "RÉGULARITÉ", "left: 150px; top: 400px; font-size: 110px;", 31.24))),
    ("s13", "oeuf2", 32.43, 36.51, "flash", *acc(
        tag("s13", "a", "TU MANGES", f"{C} top: 250px; font-size: 84px; color: #fff;", 32.77),
        lab("s13", "b", "JUSTE APRÈS", "left: 150px; top: 380px; font-size: 100px;", 33.68),
        tag("s13", "c", "TA SÉANCE", f"{C} top: 560px; font-size: 76px; color: #fff;", 34.07),
        lab("s13", "d", "PLUSIEURS HEURES ?", "left: 90px; top: 720px; font-size: 62px;", 35.52, white=True))),
    ("s14", "fin", 36.51, D, "whip", *acc(
        ('<div id="s14-end"><div class="tag" id="s14-ab">ABONNE-TOI</div><div class="tag" id="s14-nv">UN CONSEIL CHAQUE JOUR</div>'
         '<img id="s14-logo" src="assets/brand/icon-512.png" alt="CaliBodi" /><div class="big" id="s14-name">CaliBodi</div>'
         '<div class="lab" id="s14-url">calibodi.com</div><div class="tag" id="s14-st">Play Store · App Store</div></div>',
         "#s14-end { position: absolute; inset: 0; }"
         "#s14-ab { left: 0; width: 1080px; top: 190px; text-align: center; font-size: 84px; color: #fff; }"
         "#s14-nv { left: 0; width: 1080px; top: 300px; text-align: center; font-size: 52px; color: #fff; }"
         "#s14-logo { position: absolute; left: 400px; top: 410px; width: 280px; height: 280px; border-radius: 62px; box-shadow: 0 20px 50px rgba(0,0,0,.5); }"
         "#s14-name { left: 0; width: 1080px; top: 720px; text-align: center; font-size: 150px; color: #fff; text-shadow: 0 16px 50px rgba(0,0,0,.7); }"
         "#s14-url { left: 230px; top: 880px; font-size: 100px; }"
         "#s14-st { left: 0; width: 1080px; top: 1015px; text-align: center; font-size: 56px; color: #fff; }",
         'tl.fromTo("#s14-ab",{y:50,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(36.80));'
         'tl.fromTo("#s14-nv",{y:50,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(37.30));'
         'tl.fromTo("#s14-logo",{scale:0,rotation:-40},{scale:1,rotation:0,duration:.45,ease:"back.out(2.6)"},at(37.90));'
         'tl.fromTo("#s14-name",{scale:2.4,opacity:0},{scale:1,opacity:1,duration:.26,ease:"power4.out"},at(38.50));'
         'tl.fromTo("#s14-url",{scale:2.4,opacity:0,rotation:-6},{scale:1,opacity:1,rotation:-3,duration:.24,ease:"power4.out"},at(39.04));'
         'tl.fromTo("#s14-st",{y:40,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(39.80));'))),
]
PUNCH = [(0.82, 1.07), (3.58, 1.07), (6.91, 1.08), (9.80, 1.09), (11.76, 1.07), (13.99, 1.06), (16.62, 1.06), (18.57, 1.06),
         (21.11, 1.07), (25.41, 1.07), (29.38, 1.06), (31.24, 1.07), (35.52, 1.06), (38.50, 1.05)]
SHAKE = [9.80, 25.41]
POSES = [(0.20, "choc"), (4.50, "curieux"), (7.90, "sceptique"), (10.40, "biceps"), (12.80, "non"), (15.20, "explique"),
         (18.00, "biceps"), (20.70, "pointe"), (23.70, "nutrition"), (27.10, "non"), (30.30, "pouce"), (32.50, "curieux"),
         (36.80, "app"), (38.40, "pouce")]
KW = {"séance", "protéines", "muscles", "muscle", "pressé", "30", "minutes", "simple", "réparer", "quantité", "shaker", "répétition",
      "stresser", "régularité", "heures", "calibodi", "calibodicom"}
CHAPTERS = [0.0, 7.88, 15.11, 23.60, 32.43]
