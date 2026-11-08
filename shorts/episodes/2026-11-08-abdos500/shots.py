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
                f'<g class="ih" id="{sid}-h{i}" opacity="0">{shape("#B6F23B")}</g></g>' for i in range(n))
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
# Shot list of « 500 abdos », read by build_v4.py. Global times in seconds (voice of 2026-11-07).
# Footage: paths, forests, a city skyline, hikers seen from behind (no women, no faces, no logos).
A = "#B6F23B"
SHOTS = [
    ("s1", "abs3d", 0.00, 4.90, None, *acc(
        tag("s1", "a", "TU PEUX FAIRE", f"{C} top: 250px; font-size: 72px; color: #fff;", 0.20),
        big("s1", "n", "500", f"{C} top: 330px; font-size: 420px; color: {A}; {SH}", 0.66),
        lab("s1", "d", "ABDOS PAR JOUR", "left: 130px; top: 770px; font-size: 96px;", 1.07, white=True),
        lab("s1", "m", "LE MÊME VENTRE", "left: 150px; top: 910px; font-size: 92px;", 3.63))),
    ("s2", "kb1", 4.90, 6.10, "whip", *acc(
        lab("s2", "p", "POURQUOI", "left: 200px; top: 290px; font-size: 112px;", 5.15),
        big("s2", "q", "?", f"left: 400px; top: 470px; font-size: 560px; color: {A}; {SH}", 5.31))),
    ("s3", "ventre", 6.10, 11.00, "zoom", *acc(
        tag("s3", "a", "TRAVAILLER TES ABDOS", f"{C} top: 250px; font-size: 62px; color: #fff;", 6.50, out=8.4),
        lab("s3", "b", "NE BRÛLE PAS", "left: 130px; top: 330px; font-size: 100px;", 8.60),
        lab("s3", "g", "LA GRAISSE", "left: 230px; top: 510px; font-size: 140px;", 9.08, white=True),
        tag("s3", "d", "JUSTE AU-DESSUS", f"{C} top: 730px; font-size: 76px; color: #fff;", 10.14))),
    ("s4", "cordes", 11.00, 15.80, "flash", *acc(
        tag("s4", "a", "TU RENFORCES", f"{C} top: 250px; font-size: 90px; color: #fff;", 11.25, out=12.6),
        lab("s4", "m", "TES MUSCLES", "left: 190px; top: 400px; font-size: 104px;", 11.74, out=12.6),
        tag("s4", "c", "TON CORPS NE CHOISIT PAS", f"{C} top: 250px; font-size: 62px; color: #fff;", 13.00),
        lab("s4", "o", "OÙ PERDRE", "left: 250px; top: 380px; font-size: 120px;", 14.14, white=True),
        lab("s4", "g", "SA GRAISSE", "left: 200px; top: 560px; font-size: 130px;", 14.94))),
    ("s5", "abs3d2", 15.80, 19.00, "zoom", *acc(
        tag("s5", "a", "POUR PERDRE DU VENTRE", f"{C} top: 250px; font-size: 62px; color: #fff;", 16.00),
        lab("s5", "m", "MASSE GRASSE", "left: 150px; top: 400px; font-size: 118px;", 17.83),
        lab("s5", "g", "GLOBALE", "left: 280px; top: 580px; font-size: 140px;", 18.31, white=True))),
    ("s6", "salade", 19.00, 20.10, "whip", *acc(
        lab("s6", "a", "ALIMENTATION", "left: 120px; top: 300px; font-size: 108px;", 19.13),
        tag("s6", "b", "ADAPTÉE", f"{C} top: 470px; font-size: 100px; color: #fff;", 19.69))),
    ("s7", "cordes2", 20.10, 21.00, "flash", *acc(
        lab("s7", "m", "MUSCULATION", "left: 140px; top: 300px; font-size: 112px;", 20.19, white=True))),
    ("s8", "kb2", 21.00, 22.70, "whip", *acc(
        lab("s8", "a", "ACTIVITÉ", "left: 250px; top: 300px; font-size: 140px;", 21.05),
        tag("s8", "b", "PHYSIQUE RÉGULIÈRE", f"{C} top: 490px; font-size: 70px; color: #fff;", 21.52))),
    ("s9", "corde", 22.70, 25.50, "zoom", *acc(
        tag("s9", "a", "DIS-MOI", f"{C} top: 250px; font-size: 96px; color: #fff;", 23.04),
        lab("s9", "c", "COMBIEN D'ABDOS", "left: 130px; top: 400px; font-size: 84px;", 23.76),
        lab("s9", "j", "PAR JOUR", "left: 280px; top: 560px; font-size: 110px;", 24.81, white=True),
        big("s9", "q", "?", f"left: 760px; top: 600px; font-size: 380px; color: {A}; {SH}", 24.97))),
    ("s10", "cordes3", 25.50, 29.40, "flash", *acc(
        ('<div class="ic2" id="s10-ic"><svg viewBox="0 0 140 140"><path d="M14 120 C 20 70, 50 44, 104 44 M84 18 L 122 44 L 84 72" fill="none" stroke="#141414" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" /></svg></div>',
         "#s10-ic { position: absolute; left: 70px; top: 250px; width: 170px; height: 170px; border-radius: 50%; background: #fff; box-shadow: 0 14px 30px rgba(0,0,0,.4); }"
         "#s10-ic svg { position: absolute; left: 25px; top: 25px; width: 120px; height: 120px; overflow: visible; }",
         'tl.fromTo("#s10-ic",{scale:0,rotation:-40},{scale:1,rotation:0,duration:.35,ease:"back.out(2.4)"},at(25.77));'),
        lab("s10", "p", "PARTAGE", "left: 270px; top: 270px; font-size: 130px;", 25.77),
        tag("s10", "q", "AVEC TON POTE QUI FAIT", f"{C} top: 470px; font-size: 60px; color: #fff;", 26.89),
        big("s10", "n", "200", f"{C} top: 560px; font-size: 330px; color: {A}; {SH}", 27.45),
        lab("s10", "c", "CRUNCHS", "left: 300px; top: 890px; font-size: 110px;", 27.74, white=True))),
    ("s11", "fin", 29.40, D, "zoom", *acc(
        ('<div id="s11-end"><img id="s11-logo" src="assets/brand/icon-512.png" alt="CaliBodi" /><div class="big" id="s11-name">CaliBodi</div>'
         '<div class="lab" id="s11-url">calibodi.com</div><div class="tag" id="s11-st">Play Store · App Store</div></div>',
         "#s11-end { position: absolute; inset: 0; }"
         "#s11-logo { position: absolute; left: 400px; top: 330px; width: 280px; height: 280px; border-radius: 62px; box-shadow: 0 20px 50px rgba(0,0,0,.5); }"
         "#s11-name { left: 0; width: 1080px; top: 650px; text-align: center; font-size: 150px; color: #fff; text-shadow: 0 16px 50px rgba(0,0,0,.7); }"
         "#s11-url { left: 230px; top: 840px; font-size: 100px; }"
         "#s11-st { left: 0; width: 1080px; top: 990px; text-align: center; font-size: 56px; color: #fff; }",
         'tl.fromTo("#s11-logo",{scale:0,rotation:-40},{scale:1,rotation:0,duration:.45,ease:"back.out(2.6)"},at(29.50));'
         'tl.fromTo("#s11-name",{scale:2.4,opacity:0},{scale:1,opacity:1,duration:.26,ease:"power4.out"},at(29.70));'
         'tl.fromTo("#s11-url",{scale:2.4,opacity:0,rotation:-6},{scale:1,opacity:1,rotation:-3,duration:.24,ease:"power4.out"},at(30.15));'
         'tl.fromTo("#s11-st",{y:40,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(30.55));'))),
]
PUNCH = [(0.66, 1.09), (1.07, 1.05), (5.31, 1.08), (8.60, 1.06), (9.08, 1.07), (11.74, 1.05), (14.94, 1.07), (17.83, 1.06),
         (19.13, 1.05), (20.19, 1.06), (21.05, 1.06), (24.97, 1.07), (25.77, 1.05), (27.45, 1.08), (29.70, 1.05)]
SHAKE = [0.66, 14.94]
POSES = [(0.18, "choc"), (4.90, "curieux"), (6.20, "explique"), (11.10, "sceptique"), (15.90, "pointe"), (19.10, "nutrition"),
         (20.15, "biceps"), (21.05, "pointe"), (22.80, "curieux"), (25.60, "pointe"), (29.50, "app"), (30.60, "pouce")]
KW = {"500", "abdos", "ventre", "pourquoi", "graisse", "muscles", "corps", "choisit", "masse", "grasse", "globale",
      "alimentation", "musculation", "activité", "combien", "200", "crunchs", "calibodi", "calibodicom", "partage"}
CHAPTERS = [0.0, 6.1, 15.8, 22.7]
