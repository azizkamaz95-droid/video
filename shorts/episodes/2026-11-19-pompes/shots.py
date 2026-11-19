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
                f'<g class="ih" id="{sid}-h{i}" opacity="0">{shape("#5B8CFF")}</g></g>' for i in range(n))
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
# Shot list of « creatine » (voix du 2026-11-18). Mixeur de poudre, eau versée, dos de pratiquants de musculation.
A = "#5B8CFF"
SHOTS = [
    ("s1", "s1", 0.00, 4.30, None, *acc(
        tag("s1", "a", "CRÉATINE", f"{C} top: 200px; font-size: 110px; color: #fff;", 1.09),
        lab("s1", "b", "BALANCE", "left: 280px; top: 380px; font-size: 100px;", 2.34, white=True),
        big("s1", "n", "+1 KG", f"{C} top: 560px; font-size: 230px; color: {A}; {SH}", 3.39))),
    ("s2", "s2", 4.30, 6.70, "whip", *acc(
        big("s2", "n", "PANIQUE", f"{C} top: 420px; font-size: 170px; color: #fff; {SH}", 4.67),
        lab("s2", "b", "DU GRAS ?", "left: 270px; top: 760px; font-size: 120px;", 5.96))),
    ("s3", "s3", 6.70, 9.40, "zoom", *acc(
        tag("s3", "a", "ATTENDS", f"{C} top: 220px; font-size: 130px; color: #fff;", 6.86),
        lab("s3", "b", "PAS FORCÉMENT", "left: 110px; top: 440px; font-size: 100px;", 8.05))),
    ("s4", "s4", 9.40, 14.10, "flash", *acc(
        tag("s4", "a", "CRÉATINE", f"{C} top: 190px; font-size: 90px; color: #fff;", 9.73),
        big("s4", "n", "POIDS ↑", f"{C} top: 330px; font-size: 200px; color: {A}; {SH}", 10.86),
        tag("s4", "b", "MAIS PAS", f"{C} top: 650px; font-size: 90px; color: #fff;", 12.06),
        lab("s4", "c", "MASSE GRAISSEUSE", "left: 110px; top: 790px; font-size: 78px;", 12.90, white=True))),
    ("s5", "s5", 14.10, 19.00, "whip", *acc(
        src("s5", "Kreider et coll., J. Int. Soc. Sports Nutr., 2017 (position de l'ISSN sur la créatine)", 15.3),
        tag("s5", "a", "POURQUOI ?", f"{C} top: 210px; font-size: 130px; color: #fff;", 14.31),
        lab("s5", "b", "STOCKAGE D'EAU", "left: 140px; top: 420px; font-size: 86px;", 16.72),
        tag("s5", "c", "DANS LES MUSCLES", f"{C} top: 620px; font-size: 76px; color: #fff;", 18.08))),
    ("s6", "s6", 19.00, 24.10, "flash", *acc(
        tag("s6", "a", "RÉSULTAT", f"{C} top: 210px; font-size: 110px; color: #fff;", 19.29),
        lab("s6", "b", "BALANCE ↑", "left: 230px; top: 400px; font-size: 110px;", 20.49),
        tag("s6", "c", "PAS DE GRAS", f"{C} top: 620px; font-size: 100px; color: #fff;", 22.85))),
    ("s7", "s7", 24.10, 29.50, "zoom", *acc(
        tag("s7", "a", "ASSOCIÉE À", f"{C} top: 200px; font-size: 76px; color: #fff;", 24.52),
        lab("s7", "b", "MUSCULATION", "left: 170px; top: 360px; font-size: 100px;", 25.50),
        tag("s7", "c", "MASSE MUSCULAIRE", f"{C} top: 600px; font-size: 80px; color: #fff;", 28.28))),
    ("s8", "s8", 29.50, 36.70, "whip", *acc(
        tag("s8", "a", "NE JUGE PAS", f"{C} top: 200px; font-size: 100px; color: #fff;", 30.08),
        lab("s8", "b", "LE CHIFFRE", "left: 260px; top: 360px; font-size: 100px;", 32.14),
        tag("s8", "c", "SUR LA BALANCE", f"{C} top: 560px; font-size: 76px; color: #fff;", 32.54),
        lab("s8", "d", "PROGRESSION", "left: 180px; top: 690px; font-size: 100px;", 34.39, white=True),
        tag("s8", "e", "ÉVOLUTION PHYSIQUE", f"{C} top: 850px; font-size: 70px; color: #fff;", 35.45))),
    ("s9", "s9", 36.70, 40.40, "flash", *acc(
        tag("s9", "a", "EN COMMENTAIRE", f"{C} top: 200px; font-size: 76px; color: #fff;", 37.37),
        lab("s9", "b", "CRÉATINE", "left: 250px; top: 380px; font-size: 110px;", 38.89),
        tag("s9", "c", "= GROSSIR ?", f"{C} top: 580px; font-size: 100px; color: #fff;", 39.37))),
    ("s10", "s10", 40.40, D, "flash", *acc(
        ('<div id="s10-end"><div class="tag" id="s10-ab">ABONNE-TOI</div><div class="tag" id="s10-nv">UNE NOUVELLE VIDÉO CHAQUE JOUR</div>'
         '<img id="s10-logo" src="assets/brand/icon-512.png" alt="CaliBodi" /><div class="big" id="s10-name">CaliBodi</div>'
         '<div class="lab" id="s10-url">calibodi.com</div><div class="tag" id="s10-st">Play Store · App Store</div></div>',
         "#s10-end { position: absolute; inset: 0; }"
         "#s10-ab { left: 0; width: 1080px; top: 190px; text-align: center; font-size: 84px; color: #fff; }"
         "#s10-nv { left: 0; width: 1080px; top: 300px; text-align: center; font-size: 46px; color: #fff; }"
         "#s10-logo { position: absolute; left: 400px; top: 410px; width: 280px; height: 280px; border-radius: 62px; box-shadow: 0 20px 50px rgba(0,0,0,.5); }"
         "#s10-name { left: 0; width: 1080px; top: 720px; text-align: center; font-size: 150px; color: #fff; text-shadow: 0 16px 50px rgba(0,0,0,.7); }"
         "#s10-url { left: 230px; top: 880px; font-size: 100px; }"
         "#s10-st { left: 0; width: 1080px; top: 1015px; text-align: center; font-size: 56px; color: #fff; }",
         'tl.fromTo("#s10-ab",{y:50,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(40.70));'
         'tl.fromTo("#s10-nv",{y:50,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(41.72));'
         'tl.fromTo("#s10-logo",{scale:0,rotation:-40},{scale:1,rotation:0,duration:.45,ease:"back.out(2.6)"},at(43.55));'
         'tl.fromTo("#s10-name",{scale:2.4,opacity:0},{scale:1,opacity:1,duration:.26,ease:"power4.out"},at(43.55));'
         'tl.fromTo("#s10-url",{scale:2.4,opacity:0,rotation:-6},{scale:1,opacity:1,rotation:-3,duration:.24,ease:"power4.out"},at(44.31));'
         'tl.fromTo("#s10-st",{y:40,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(45.00));'))),
]
PUNCH = [(1.09, 1.07), (3.39, 1.09), (4.67, 1.07), (9.73, 1.06), (10.86, 1.08), (16.72, 1.07), (20.49, 1.07), (25.50, 1.07), (34.39, 1.07), (38.89, 1.06), (44.31, 1.05)]
SHAKE = [4.67]
POSES = [(0.20, "curieux"), (4.50, "choc"), (6.90, "pointe"), (9.60, "explique"), (14.30, "sceptique"), (19.20, "explique"),
         (24.30, "biceps"), (29.70, "pouce"), (36.90, "curieux"), (42.90, "app"), (44.40, "pouce")]
KW = {"créatine", "balance", "kilo", "gras", "poids", "graisseuse", "eau", "muscles", "musculation", "musculaire", "progression",
      "résultats", "grossir", "forcément", "calibodi", "calibodicom"}
CHAPTERS = [0.0, 9.40, 24.10]
