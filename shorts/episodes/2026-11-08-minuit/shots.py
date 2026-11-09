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
                f'<g class="ih" id="{sid}-h{i}" opacity="0">{shape("#FFC93C")}</g></g>' for i in range(n))
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
# Shot list of « minuit », read by build_v4.py. Global times in seconds (voice of 2026-11-07).
# Footage: paths, forests, a city skyline, hikers seen from behind (no women, no faces, no logos).
A = "#FFC93C"
SHOTS = [
    ("s1", "lune", 0.00, 3.50, None, *acc(
        tag("s1", "a", "TU TE COUCHES", f"{C} top: 250px; font-size: 76px; color: #fff;", 0.18),
        big("s1", "n", "MINUIT", f"{C} top: 340px; font-size: 250px; color: {A}; {SH}", 0.58),
        lab("s1", "s", "TOUS LES SOIRS ?", "left: 150px; top: 640px; font-size: 90px;", 0.82, white=True))),
    ("s2", "cabane", 3.50, 8.50, "zoom", *acc(
        tag("s2", "a", "TU AS DÉJÀ ENTENDU", f"{C} top: 250px; font-size: 62px; color: #fff;", 3.72, out=5.4),
        lab("s2", "b", "1 H AVANT MINUIT", "left: 110px; top: 280px; font-size: 92px;", 5.73),
        tag("s2", "w", "VAUT", f"{C} top: 450px; font-size: 90px; color: #fff;", 6.91),
        lab("s2", "c", "2 H APRÈS MINUIT", "left: 110px; top: 580px; font-size: 92px;", 7.07, white=True))),
    ("s3", "nuages", 8.50, 9.60, "flash", *acc(
        tag("s3", "a", "C'EST", f"{C} top: 250px; font-size: 90px; color: #fff;", 8.60),
        big("s3", "n", "FAUX", f"{C} top: 350px; font-size: 290px; color: {A}; {SH}", 8.76))),
    ("s4", "brume", 9.60, 13.30, "whip", *acc(
        tag("s4", "a", "MAIS ATTENTION", f"{C} top: 250px; font-size: 84px; color: #fff;", 9.82, out=10.9),
        lab("s4", "t", "UNE VÉRITÉ", "left: 200px; top: 330px; font-size: 130px;", 11.33),
        tag("s4", "c", "DERRIÈRE CETTE CROYANCE", f"{C} top: 520px; font-size: 56px; color: #fff;", 11.73))),
    ("s5", "reveil", 13.30, 16.60, "zoom", *acc(
        tag("s5", "a", "TON CORPS", f"{C} top: 250px; font-size: 96px; color: #fff;", 13.49),
        lab("s5", "h", "HORLOGE BIOLOGIQUE", "left: 90px; top: 400px; font-size: 74px;", 14.31))),
    ("s6", "rayons", 16.60, 18.60, "whip", *acc(
        lab("s6", "l", "LUMIÈRE DU JOUR", "left: 100px; top: 280px; font-size: 90px;", 16.73),
        lab("s6", "o", "L'OBSCURITÉ", "left: 200px; top: 440px; font-size: 100px;", 17.41, white=True))),
    ("s7", "fenetre", 18.60, 23.40, "flash", *acc(
        tag("s7", "a", "DORMIR LA JOURNÉE", f"{C} top: 250px; font-size: 76px; color: #fff;", 19.11),
        lab("s7", "p", "PAS PARFAITEMENT", "left: 110px; top: 400px; font-size: 90px;", 20.79),
        lab("s7", "n", "SOMMEIL NOCTURNE", "left: 100px; top: 570px; font-size: 90px;", 22.35, white=True))),
    ("s8", "ville", 23.40, 26.50, "zoom", *acc(
        tag("s8", "a", "TU TE COUCHES TRÈS TARD", f"{C} top: 250px; font-size: 56px; color: #fff;", 24.00),
        lab("s8", "l", "ET TU TE LÈVES TÔT", "left: 90px; top: 380px; font-size: 80px;", 25.62))),
    ("s9", "reveil2", 26.50, 29.60, "whip", *acc(
        lab("s9", "d", "DETTE DE SOMMEIL", "left: 90px; top: 280px; font-size: 86px;", 27.21),
        tag("s9", "r", "TA RÉCUPÉRATION", f"{C} top: 450px; font-size: 80px; color: #fff;", 28.74))),
    ("s10", "traces", 29.60, 32.10, "flash", *acc(
        lab("s10", "h", "TES HORMONES", "left: 150px; top: 300px; font-size: 100px;", 29.80, white=True),
        lab("s10", "p", "TES PERFORMANCES", "left: 110px; top: 460px; font-size: 80px;", 30.50))),
    ("s11", "lune2", 32.10, 35.00, "zoom", *acc(
        tag("s11", "a", "LE PROBLÈME", f"{C} top: 250px; font-size: 96px; color: #fff;", 32.91),
        lab("s11", "m", "PAS MINUIT", "left: 200px; top: 400px; font-size: 130px;", 33.65))),
    ("s12", "cafe", 35.00, 38.60, "whip", *acc(
        lab("s12", "d", "DORMIR TROP PEU", "left: 110px; top: 280px; font-size: 84px;", 35.48),
        tag("s12", "r", "DÉRÉGLER", f"{C} top: 450px; font-size: 90px; color: #fff;", 36.69),
        lab("s12", "b", "TON RYTHME", "left: 220px; top: 570px; font-size: 100px;", 37.09, white=True))),
    ("s13", "aube", 38.60, 41.70, "flash", *acc(
        tag("s13", "a", "DIS-MOI EN COMMENTAIRE", f"{C} top: 250px; font-size: 60px; color: #fff;", 38.86, out=40.3),
        lab("s13", "h", "À QUELLE HEURE", "left: 120px; top: 380px; font-size: 100px;", 40.47),
        lab("s13", "c", "TU TE COUCHES", "left: 150px; top: 540px; font-size: 90px;", 40.79, white=True),
        big("s13", "q", "?", f"left: 740px; top: 640px; font-size: 380px; color: {A}; {SH}", 41.03))),
    ("s14", "himalaya", 41.70, 44.10, "whip", *acc(
        ('<div class="ic2" id="s14-ic"><svg viewBox="0 0 140 140"><path d="M14 120 C 20 70, 50 44, 104 44 M84 18 L 122 44 L 84 72" fill="none" stroke="#141414" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" /></svg></div>',
         "#s14-ic { position: absolute; left: 70px; top: 250px; width: 170px; height: 170px; border-radius: 50%; background: #fff; box-shadow: 0 14px 30px rgba(0,0,0,.4); }"
         "#s14-ic svg { position: absolute; left: 25px; top: 25px; width: 120px; height: 120px; overflow: visible; }",
         'tl.fromTo("#s14-ic",{scale:0,rotation:-40},{scale:1,rotation:0,duration:.35,ease:"back.out(2.4)"},at(41.99));'),
        lab("s14", "p", "PARTAGE", "left: 270px; top: 270px; font-size: 130px;", 41.99),
        tag("s14", "q", "AVEC TON AMI QUI SE COUCHE TARD", f"{C} top: 470px; font-size: 48px; color: #fff;", 42.64))),
    ("s15", "fin", 44.10, D, "zoom", *acc(
        ('<div id="s15-end"><div class="tag" id="s15-ab">ABONNE-TOI</div><div class="tag" id="s15-nv">UNE NOUVELLE VIDÉO CHAQUE JOUR</div>'
         '<img id="s15-logo" src="assets/brand/icon-512.png" alt="CaliBodi" /><div class="big" id="s15-name">CaliBodi</div>'
         '<div class="lab" id="s15-url">calibodi.com</div><div class="tag" id="s15-st">Play Store · App Store</div></div>',
         "#s15-end { position: absolute; inset: 0; }"
         "#s15-ab { left: 0; width: 1080px; top: 190px; text-align: center; font-size: 84px; color: #fff; }"
         "#s15-nv { left: 0; width: 1080px; top: 300px; text-align: center; font-size: 46px; color: #fff; }"
         "#s15-logo { position: absolute; left: 400px; top: 410px; width: 280px; height: 280px; border-radius: 62px; box-shadow: 0 20px 50px rgba(0,0,0,.5); }"
         "#s15-name { left: 0; width: 1080px; top: 720px; text-align: center; font-size: 150px; color: #fff; text-shadow: 0 16px 50px rgba(0,0,0,.7); }"
         "#s15-url { left: 230px; top: 880px; font-size: 100px; }"
         "#s15-st { left: 0; width: 1080px; top: 990px; text-align: center; font-size: 56px; color: #fff; }",
         'tl.fromTo("#s15-ab",{y:50,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(44.34));'
         'tl.fromTo("#s15-nv",{y:50,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(45.13));'
         'tl.fromTo("#s15-logo",{scale:0,rotation:-40},{scale:1,rotation:0,duration:.45,ease:"back.out(2.6)"},at(45.60));'
         'tl.fromTo("#s15-name",{scale:2.4,opacity:0},{scale:1,opacity:1,duration:.26,ease:"power4.out"},at(46.20));'
         'tl.fromTo("#s15-url",{scale:2.4,opacity:0,rotation:-6},{scale:1,opacity:1,rotation:-3,duration:.24,ease:"power4.out"},at(46.58));'
         'tl.fromTo("#s15-st",{y:40,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(47.20));'))),
]
PUNCH = [(0.58, 1.08), (0.82, 1.05), (5.73, 1.06), (7.07, 1.06), (8.76, 1.10), (11.33, 1.06), (14.31, 1.05), (16.73, 1.05),
         (20.79, 1.05), (27.21, 1.07), (30.50, 1.06), (33.65, 1.07), (35.48, 1.06), (40.47, 1.06), (41.99, 1.05), (46.20, 1.05)]
SHAKE = [8.76, 27.21]
POSES = [(0.18, "curieux"), (3.54, "explique"), (8.60, "non"), (9.82, "pointe"), (13.49, "explique"), (16.73, "pointe"),
         (19.11, "sceptique"), (23.45, "sceptique"), (27.21, "fatigue"), (29.80, "pointe"), (32.20, "explique"),
         (35.48, "pointe"), (38.80, "curieux"), (41.99, "pointe"), (44.40, "app"), (46.60, "pouce")]
KW = {"minuit", "faux", "vérité", "horloge", "biologique", "lumière", "obscurité", "nocturne", "dette", "récupération",
      "hormones", "performances", "problème", "trop", "peu", "rythme", "commentaire", "partage", "ami", "calibodi", "calibodicom",
      "heure", "couches", "tard", "sommeil"}
CHAPTERS = [0.0, 8.5, 13.3, 23.4, 32.1]
