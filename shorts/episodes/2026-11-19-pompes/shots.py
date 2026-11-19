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
                f'<g class="ih" id="{sid}-h{i}" opacity="0">{shape("#1FD6C4")}</g></g>' for i in range(n))
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
# Shot list of « pompes » (voix du 2026-11-19). Pompes vues de profil, silhouette sur une plage ; trois cadrages et vitesses différents.
A = "#1FD6C4"
SHOTS = [
    ("s1", "s1", 0.00, 4.20, None, *acc(
        big("s1", "n", "20 · 30 · 50", f"{C} top: 200px; font-size: 170px; color: {A}; {SH}", 0.56),
        lab("s1", "b", "POMPES", "left: 300px; top: 420px; font-size: 120px;", 2.26, white=True),
        tag("s1", "c", "POUR LE MUSCLE ?", f"{C} top: 600px; font-size: 80px; color: #fff;", 3.42))),
    ("s2", "s2", 4.20, 7.80, "whip", *acc(
        tag("s2", "a", "+ DE RÉPÉTITIONS", f"{C} top: 210px; font-size: 90px; color: #fff;", 5.58),
        lab("s2", "b", "+ DE MUSCLE ?", "left: 150px; top: 400px; font-size: 92px;", 6.46))),
    ("s3", "s3", 7.80, 11.20, "zoom", *acc(
        tag("s3", "a", "ATTENTION", f"{C} top: 210px; font-size: 130px; color: #fff;", 8.05),
        lab("s3", "b", "L'ESSENTIEL ?", "left: 180px; top: 420px; font-size: 120px;", 10.04))),
    ("s4", "s4", 11.20, 17.70, "flash", *acc(
        src("s4", "Refalo et coll., Sports Medicine, 2023 (méta-analyse sur la proximité de l'échec)", 13.6),
        tag("s4", "a", "CE QUI COMPTE", f"{C} top: 210px; font-size: 96px; color: #fff;", 11.72),
        lab("s4", "b", "L'EFFORT", "left: 250px; top: 400px; font-size: 140px;", 15.11),
        tag("s4", "c", "ET TA CAPACITÉ À PROGRESSER", f"{C} top: 640px; font-size: 54px; color: #fff;", 16.14))),
    ("s5", "s5", 17.70, 23.50, "whip", *acc(
        tag("s5", "a", "30 POMPES FACILES", f"{C} top: 210px; font-size: 84px; color: #fff;", 18.22),
        lab("s5", "b", "SANS AUGMENTER", "left: 150px; top: 380px; font-size: 92px;", 19.54),
        tag("s5", "c", "LA DIFFICULTÉ", f"{C} top: 560px; font-size: 84px; color: #fff;", 19.98),
        lab("s5", "d", "PAS FORCÉMENT", "left: 200px; top: 720px; font-size: 100px;", 21.75, white=True),
        tag("s5", "e", "PROGRESSER INDÉFINIMENT", f"{C} top: 880px; font-size: 56px; color: #fff;", 22.15))),
    ("s6", "s6", 23.50, 33.10, "zoom", *acc(
        tag("s6", "a", "TROP FACILE ?", f"{C} top: 210px; font-size: 100px; color: #fff;", 25.12),
        lab("s6", "b", "+ DIFFICILE", "left: 240px; top: 380px; font-size: 120px;", 26.18),
        tag("s6", "c", "RALENTIS", f"{C} top: 580px; font-size: 96px; color: #fff;", 28.49),
        tag("s6", "d", "AMPLITUDE", f"{C} top: 700px; font-size: 96px; color: #fff;", 30.13),
        tag("s6", "e", "VARIANTE", f"{C} top: 820px; font-size: 96px; color: #fff;", 31.55))),
    ("s7", "s7", 33.10, 38.60, "flash", *acc(
        tag("s7", "a", "TON OBJECTIF", f"{C} top: 210px; font-size: 96px; color: #fff;", 33.57),
        lab("s7", "b", "PROGRESSIVEMENT", "left: 90px; top: 400px; font-size: 76px;", 37.02),
        lab("s7", "c", "PLUS FORT", "left: 230px; top: 580px; font-size: 140px;", 37.74, white=True))),
    ("s8", "s8", 38.60, 42.80, "whip", *acc(
        tag("s8", "a", "ET TOI ?", f"{C} top: 210px; font-size: 120px; color: #fff;", 39.03),
        lab("s8", "b", "50 FACILES", "left: 220px; top: 400px; font-size: 110px;", 39.92),
        lab("s8", "c", "15 DIFFICILES ?", "left: 100px; top: 590px; font-size: 100px;", 41.53, white=True))),
    ("s9", "s9", 42.80, D, "flash", *acc(
        ('<div id="s9-end"><div class="tag" id="s9-ab">ABONNE-TOI</div><div class="tag" id="s9-nv">UNE NOUVELLE VIDÉO CHAQUE JOUR</div>'
         '<img id="s9-logo" src="assets/brand/icon-512.png" alt="CaliBodi" /><div class="big" id="s9-name">CaliBodi</div>'
         '<div class="lab" id="s9-url">calibodi.com</div><div class="tag" id="s9-st">Play Store · App Store</div></div>',
         "#s9-end { position: absolute; inset: 0; }"
         "#s9-ab { left: 0; width: 1080px; top: 190px; text-align: center; font-size: 84px; color: #fff; }"
         "#s9-nv { left: 0; width: 1080px; top: 300px; text-align: center; font-size: 46px; color: #fff; }"
         "#s9-logo { position: absolute; left: 400px; top: 410px; width: 280px; height: 280px; border-radius: 62px; box-shadow: 0 20px 50px rgba(0,0,0,.5); }"
         "#s9-name { left: 0; width: 1080px; top: 720px; text-align: center; font-size: 150px; color: #fff; text-shadow: 0 16px 50px rgba(0,0,0,.7); }"
         "#s9-url { left: 230px; top: 880px; font-size: 100px; }"
         "#s9-st { left: 0; width: 1080px; top: 1015px; text-align: center; font-size: 56px; color: #fff; }",
         'tl.fromTo("#s9-ab",{y:50,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(43.07));'
         'tl.fromTo("#s9-nv",{y:50,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(43.62));'
         'tl.fromTo("#s9-logo",{scale:0,rotation:-40},{scale:1,rotation:0,duration:.45,ease:"back.out(2.6)"},at(46.08));'
         'tl.fromTo("#s9-name",{scale:2.4,opacity:0},{scale:1,opacity:1,duration:.26,ease:"power4.out"},at(46.08));'
         'tl.fromTo("#s9-url",{scale:2.4,opacity:0,rotation:-6},{scale:1,opacity:1,rotation:-3,duration:.24,ease:"power4.out"},at(46.70));'
         'tl.fromTo("#s9-st",{y:40,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(47.40));'))),
]
PUNCH = [(0.56, 1.07), (2.26, 1.08), (5.58, 1.07), (10.04, 1.08), (15.11, 1.08), (18.46, 1.07), (26.18, 1.07), (37.74, 1.08), (39.92, 1.06), (46.08, 1.05)]
SHAKE = [10.04]
POSES = [(0.20, "biceps"), (4.30, "sceptique"), (8.00, "choc"), (11.40, "explique"), (17.90, "sceptique"), (23.70, "pointe"),
         (33.40, "biceps"), (38.90, "curieux"), (45.30, "app"), (46.70, "pouce")]
KW = {"pompes", "répétitions", "muscle", "essentiel", "effort", "progresser", "faciles", "difficulté", "difficiles", "plus", "fort",
      "ralentis", "amplitude", "variante", "progressivement", "calibodi", "calibodicom", "30", "50", "15", "20"}
CHAPTERS = [0.0, 11.20, 23.50]
