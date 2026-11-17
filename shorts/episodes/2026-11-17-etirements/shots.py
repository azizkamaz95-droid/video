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
                f'<g class="ih" id="{sid}-h{i}" opacity="0">{shape("#4DA3FF")}</g></g>' for i in range(n))
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
# Shot list of « courbatures » (voix du 2026-11-16). Musculation vue de dos / silhouettes, sans visage.
A = "#4DA3FF"
SHOTS = [
    ("s1", "pull1", 0.00, 3.30, None, *acc(
        tag("s1", "a", "GROSSE SÉANCE", f"{C} top: 190px; font-size: 88px; color: #fff;", 0.37),
        lab("s1", "b", "AUCUNE COURBATURE ?", "left: 60px; top: 520px; font-size: 80px;", 2.20))),
    ("s2", "dos1", 3.30, 5.40, "whip", *acc(
        lab("s2", "a", "VRAIMENT", "left: 250px; top: 300px; font-size: 120px;", 4.32),
        tag("s2", "b", "TRAVAILLÉ ?", f"{C} top: 500px; font-size: 100px; color: #fff;", 4.59))),
    ("s3", "banc1", 5.40, 10.80, "zoom", *acc(
        tag("s3", "a", "CE QUE BEAUCOUP IGNORENT", f"{C} top: 220px; font-size: 58px; color: #fff;", 7.07),
        lab("s3", "b", "DES MUSCLES", "left: 170px; top: 380px; font-size: 120px;", 9.00, out=9.70),
        lab("s3", "c", "SANS MAL", "left: 250px; top: 560px; font-size: 130px;", 9.74, white=True))),
    ("s4", "halt1", 10.80, 19.40, "flash", *acc(
        src("s4", "Schoenfeld et Contreras, Strength and Conditioning Journal, 2013", 15.66),
        tag("s4", "a", "COURBATURES", f"{C} top: 220px; font-size: 100px; color: #fff;", 11.24),
        lab("s4", "b", "EFFORT INHABITUEL", "left: 80px; top: 400px; font-size: 84px;", 12.70, out=15.40),
        lab("s4", "c", "NE MESURENT PAS", "left: 100px; top: 420px; font-size: 90px;", 15.66, white=True),
        tag("s4", "d", "TA SÉANCE", f"{C} top: 640px; font-size: 90px; color: #fff;", 17.74))),
    ("s5", "dos2", 19.40, 25.00, "whip", *acc(
        tag("s5", "a", "VOULOIR AVOIR MAL", f"{C} top: 220px; font-size: 70px; color: #fff;", 20.39),
        big("s5", "n", "TROP", f"{C} top: 330px; font-size: 230px; color: {A}; {SH}", 22.23),
        lab("s5", "m", "AU DÉTRIMENT", "left: 170px; top: 640px; font-size: 90px;", 23.26, white=True),
        tag("s5", "p", "DE TA RÉCUPÉRATION", f"{C} top: 800px; font-size: 76px; color: #fff;", 23.95))),
    ("s6", "pull2", 25.00, 31.70, "flash", *acc(
        tag("s6", "a", "LE VRAI INDICATEUR", f"{C} top: 220px; font-size: 76px; color: #fff;", 25.28),
        lab("s6", "b", "PROGRESSION", "left: 150px; top: 360px; font-size: 120px;", 26.24),
        tag("s6", "c", "+ DE RÉPÉTITIONS", f"{C} top: 560px; font-size: 74px; color: #fff;", 27.13),
        tag("s6", "d", "+ DE TECHNIQUE", f"{C} top: 670px; font-size: 74px; color: #fff;", 28.51),
        tag("s6", "e", "+ DE FORCE", f"{C} top: 780px; font-size: 74px; color: #fff;", 29.78))),
    ("s7", "banc2", 31.70, 35.80, "zoom", *acc(
        tag("s7", "a", "RETIENS", f"{C} top: 220px; font-size: 110px; color: #fff;", 32.22),
        lab("s7", "b", "PAS BESOIN DE SOUFFRIR", "left: 60px; top: 400px; font-size: 66px;", 33.49),
        tag("s7", "c", "POUR PROGRESSER", f"{C} top: 600px; font-size: 84px; color: #fff;", 34.78))),
    ("s8", "halt2", 35.80, 38.50, "whip", *acc(
        tag("s8", "a", "ET TOI ?", f"{C} top: 220px; font-size: 110px; color: #fff;", 36.08),
        tag("s8", "b", "CONTENT AVEC", f"{C} top: 380px; font-size: 84px; color: #fff;", 37.03),
        lab("s8", "c", "COURBATURES ?", "left: 120px; top: 520px; font-size: 100px;", 37.76))),
    ("s9", "fin", 38.50, D, "flash", *acc(
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
         'tl.fromTo("#s9-ab",{y:50,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(38.74));'
         'tl.fromTo("#s9-nv",{y:50,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(39.79));'
         'tl.fromTo("#s9-logo",{scale:0,rotation:-40},{scale:1,rotation:0,duration:.45,ease:"back.out(2.6)"},at(41.20));'
         'tl.fromTo("#s9-name",{scale:2.4,opacity:0},{scale:1,opacity:1,duration:.26,ease:"power4.out"},at(42.40));'
         'tl.fromTo("#s9-url",{scale:2.4,opacity:0,rotation:-6},{scale:1,opacity:1,rotation:-3,duration:.24,ease:"power4.out"},at(42.95));'
         'tl.fromTo("#s9-st",{y:40,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(43.55));'))),
]
PUNCH = [(0.37, 1.06), (2.50, 1.08), (4.59, 1.06), (9.91, 1.07), (12.70, 1.06), (15.66, 1.07), (22.41, 1.09), (26.24, 1.07), (33.49, 1.07), (37.76, 1.06), (42.40, 1.05)]
SHAKE = [22.41]
POSES = [(0.20, "sceptique"), (3.40, "curieux"), (5.60, "explique"), (11.10, "sceptique"), (19.50, "non"), (25.10, "biceps"),
         (32.10, "pointe"), (36.10, "curieux"), (41.20, "app"), (43.00, "pouce")]
KW = {"courbatures", "courbature", "mal", "muscles", "progression", "répétitions", "technique", "force", "récupération", "trop",
      "souffrir", "progresser", "séance", "travaillé", "calibodi", "calibodicom"}
CHAPTERS = [0.0, 11.0, 25.0]
