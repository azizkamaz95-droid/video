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
                f'<g class="ih" id="{sid}-h{i}" opacity="0">{shape("#35C7FF")}</g></g>' for i in range(n))
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
# Shot list of « muscu-ado », read by build_v4.py. Global times in seconds (voice of 2026-11-11).
# Footage: kettlebell in a forest, sprouts, stairs, shoe laces, hoop, a bodybuilder seen from behind (no women, no faces, no logos).
A = "#35C7FF"
SHOTS = [
    ("s1", "kettle", 0.00, 4.07, None, *acc(
        tag("s1", "a", "ON T'A DÉJÀ DIT", f"{C} top: 250px; font-size: 72px; color: #fff;", 0.26),
        lab("s1", "b", "POIDS", "left: 300px; top: 340px; font-size: 150px;", 1.46),
        lab("s1", "c", "ADOLESCENT", "left: 130px; top: 540px; font-size: 100px;", 2.09, white=True),
        tag("s1", "d", "T'EMPÊCHER DE", f"{C} top: 720px; font-size: 64px; color: #fff;", 2.58),
        lab("s1", "e", "GRANDIR ?", "left: 120px; top: 820px; font-size: 120px;", 3.11))),
    ("s2", "escalier", 4.07, 6.36, "whip", *acc(
        tag("s2", "a", "C'EST UNE", f"{C} top: 250px; font-size: 72px; color: #fff;", 4.91),
        lab("s2", "b", "IDÉE REÇUE", "left: 110px; top: 380px; font-size: 110px;", 5.17))),
    ("s3", "arrosoir", 6.36, 9.60, "zoom", *acc(
        tag("s3", "a", "MUSCULATION", f"{C} top: 250px; font-size: 90px; color: #fff;", 6.55, out=7.55),
        tag("s3", "b", "BIEN ENCADRÉE", f"{C} top: 250px; font-size: 84px; color: #fff;", 7.64),
        lab("s3", "c", "ADAPTÉE À TON ÂGE", "left: 90px; top: 400px; font-size: 62px;", 8.88, white=True))),
    ("s4", "graine", 9.60, 11.63, "flash", *acc(
        tag("s4", "a", "NE BLOQUE PAS", f"{C} top: 250px; font-size: 84px; color: #fff;", 9.97),
        lab("s4", "b", "TA CROISSANCE", "left: 110px; top: 400px; font-size: 84px;", 10.53))),
    ("s5", "dos", 11.63, 14.40, "whip", *acc(
        tag("s5", "a", "RENFORCER", f"{C} top: 250px; font-size: 90px; color: #fff;", 12.89),
        lab("s5", "b", "MUSCLES", "left: 150px; top: 400px; font-size: 140px;", 13.45))),
    ("s6", "lacets", 14.40, 16.64, "zoom", *acc(
        big("s6", "a", "OS", f"left: 330px; top: 260px; font-size: 300px; color: {A}; {SH}", 14.54),
        tag("s6", "b", "CONDITION PHYSIQUE", f"{C} top: 640px; font-size: 60px; color: #fff;", 15.26))),
    ("s7", "tirage", 16.64, 18.80, "flash", *acc(
        tag("s7", "a", "MAIS ATTENTION", f"{C} top: 250px; font-size: 84px; color: #fff;", 16.79, out=17.8),
        lab("s7", "b", "TROP LOURD", "left: 140px; top: 380px; font-size: 100px;", 18.23))),
    ("s8", "carnet", 18.80, 20.00, "whip", *acc(
        tag("s8", "a", "NÉGLIGER LA", f"{C} top: 250px; font-size: 72px; color: #fff;", 18.96),
        lab("s8", "b", "TECHNIQUE", "left: 150px; top: 380px; font-size: 110px;", 19.52))),
    ("s9", "panier", 20.00, 23.39, "zoom", *acc(
        tag("s9", "a", "VOULOIR", f"{C} top: 250px; font-size: 84px; color: #fff;", 20.08, out=20.40),
        lab("s9", "b", "IMPRESSIONNER", "left: 60px; top: 360px; font-size: 80px;", 20.42, white=True),
        tag("s9", "c", "LES AUTRES", f"{C} top: 560px; font-size: 72px; color: #fff;", 21.14),
        lab("s9", "d", "BLESSURES", "left: 160px; top: 700px; font-size: 110px;", 22.17))),
    ("s10", "pousse", 23.39, 25.00, "flash", *acc(
        tag("s10", "a", "RETIENS BIEN ÇA", f"{C} top: 250px; font-size: 70px; color: #fff;", 23.85))),
    ("s11", "marche", 25.00, 28.40, "whip", *acc(
        lab("s11", "a", "PAS TON ÂGE", "left: 120px; top: 280px; font-size: 96px;", 25.12),
        tag("s11", "b", "QUI DOIT TE FAIRE PEUR", f"{C} top: 480px; font-size: 48px; color: #fff;", 25.78),
        lab("s11", "c", "N'IMPORTE COMMENT", "left: 60px; top: 640px; font-size: 60px;", 27.21, white=True))),
    ("s12", "lacets2", 28.40, 31.30, "zoom", *acc(
        tag("s12", "a", "DIS-MOI EN COMMENTAIRE", f"{C} top: 250px; font-size: 50px; color: #fff;", 28.83),
        lab("s12", "b", "TOI AUSSI ?", "left: 110px; top: 400px; font-size: 100px;", 30.20))),
    ("s13", "pousses", 31.30, 33.70, "flash", *acc(
        lab("s13", "a", "INTERDIT", "left: 130px; top: 280px; font-size: 130px;", 31.43),
        tag("s13", "b", "LA MUSCULATION", f"{C} top: 480px; font-size: 70px; color: #fff;", 31.82),
        lab("s13", "c", "TROP JEUNE ?", "left: 120px; top: 620px; font-size: 90px;", 32.90, white=True))),
    ("s14", "fin", 33.70, D, "whip", *acc(
        ('<div id="s14-end"><div class="tag" id="s14-ab">ABONNE-TOI</div><div class="tag" id="s14-nv">UNE NOUVELLE VIDÉO CHAQUE JOUR</div>'
         '<img id="s14-logo" src="assets/brand/icon-512.png" alt="CaliBodi" /><div class="big" id="s14-name">CaliBodi</div>'
         '<div class="lab" id="s14-url">calibodi.com</div><div class="tag" id="s14-st">Play Store · App Store</div></div>',
         "#s14-end { position: absolute; inset: 0; }"
         "#s14-ab { left: 0; width: 1080px; top: 190px; text-align: center; font-size: 84px; color: #fff; }"
         "#s14-nv { left: 0; width: 1080px; top: 300px; text-align: center; font-size: 46px; color: #fff; }"
         "#s14-logo { position: absolute; left: 400px; top: 410px; width: 280px; height: 280px; border-radius: 62px; box-shadow: 0 20px 50px rgba(0,0,0,.5); }"
         "#s14-name { left: 0; width: 1080px; top: 720px; text-align: center; font-size: 150px; color: #fff; text-shadow: 0 16px 50px rgba(0,0,0,.7); }"
         "#s14-url { left: 230px; top: 880px; font-size: 100px; }"
         "#s14-st { left: 0; width: 1080px; top: 1015px; text-align: center; font-size: 56px; color: #fff; }",
         'tl.fromTo("#s14-ab",{y:50,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(33.90));'
         'tl.fromTo("#s14-nv",{y:50,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(34.70));'
         'tl.fromTo("#s14-logo",{scale:0,rotation:-40},{scale:1,rotation:0,duration:.45,ease:"back.out(2.6)"},at(35.20));'
         'tl.fromTo("#s14-name",{scale:2.4,opacity:0},{scale:1,opacity:1,duration:.26,ease:"power4.out"},at(35.90));'
         'tl.fromTo("#s14-url",{scale:2.4,opacity:0,rotation:-6},{scale:1,opacity:1,rotation:-3,duration:.24,ease:"power4.out"},at(36.30));'
         'tl.fromTo("#s14-st",{y:40,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(36.90));'))),
]
PUNCH = [(0.98, 1.06), (2.09, 1.07), (5.17, 1.08), (10.53, 1.06), (13.45, 1.07), (15.26, 1.05), (18.23, 1.07), (22.17, 1.09),
         (25.63, 1.05), (27.21, 1.06), (32.90, 1.07), (35.90, 1.05)]
SHAKE = [22.17]
POSES = [(0.20, "choc"), (4.10, "sceptique"), (6.40, "explique"), (9.70, "pouce"), (11.70, "biceps"), (14.50, "biceps"),
         (16.70, "non"), (18.90, "explique"), (20.10, "choc"), (23.40, "pointe"), (25.10, "pouce"), (28.80, "pointe"),
         (34.90, "app"), (36.20, "pouce")]
KW = {"poids", "adolescent", "grandir", "idée", "reçue", "musculation", "croissance", "muscles", "os", "lourd", "technique",
      "blessures", "âge", "commentaire", "interdit", "jeune", "calibodi", "calibodicom"}
CHAPTERS = [0.0, 6.36, 16.64, 23.39]
