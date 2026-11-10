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
                f'<g class="ih" id="{sid}-h{i}" opacity="0">{shape("#3DE0C0")}</g></g>' for i in range(n))
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
# Shot list of « sucre », read by build_v4.py. Global times in seconds (voice of 2026-11-07).
# Footage: paths, forests, a city skyline, hikers seen from behind (no women, no faces, no logos).
A = "#3DE0C0"
SHOTS = [
    ("s1", "cookies", 0.00, 4.06, None, *acc(
        tag("s1", "a", "TU CROIS QUE", f"{C} top: 250px; font-size: 72px; color: #fff;", 0.18),
        lab("s1", "b", "VOLONTÉ", "left: 220px; top: 340px; font-size: 130px;", 1.14),
        tag("s1", "c", "TU N'ARRIVES PAS", f"{C} top: 600px; font-size: 72px; color: #fff;", 2.21),
        lab("s1", "d", "LE SUCRE ?", "left: 250px; top: 700px; font-size: 120px;", 3.14, white=True))),
    ("s2", "cafe2", 4.06, 6.31, "whip", *acc(
        tag("s2", "a", "ET SI LE PROBLÈME", f"{C} top: 250px; font-size: 64px; color: #fff;", 4.18),
        lab("s2", "b", "PLUS COMPLIQUÉ", "left: 160px; top: 380px; font-size: 84px;", 5.14),
        big("s2", "q", "?", f"left: 720px; top: 560px; font-size: 420px; color: {A}; {SH}", 5.54))),
    ("s3", "cacao", 6.31, 8.30, "zoom", *acc(
        lab("s3", "a", "TRÈS SUCRÉ", "left: 200px; top: 300px; font-size: 130px;", 7.47))),
    ("s4", "myrtilles", 8.30, 11.44, "flash", *acc(
        tag("s4", "a", "TON CERVEAU", f"{C} top: 250px; font-size: 90px; color: #fff;", 8.51),
        lab("s4", "b", "SYSTÈME DE RÉCOMPENSE", "left: 90px; top: 400px; font-size: 62px;", 9.71, white=True))),
    ("s5", "fraises", 11.44, 14.53, "whip", *acc(
        lab("s5", "a", "PLAISIR", "left: 250px; top: 300px; font-size: 150px;", 12.03),
        tag("s5", "b", "ENVIE DE RECOMMENCER", f"{C} top: 520px; font-size: 64px; color: #fff;", 13.09))),
    ("s6", "myrtilles2", 14.53, 18.76, "zoom", *acc(
        tag("s6", "a", "MAIS ATTENTION", f"{C} top: 250px; font-size: 84px; color: #fff;", 14.77, out=16.0),
        lab("s6", "b", "PAS UNE DROGUE", "left: 100px; top: 380px; font-size: 96px;", 16.14),
        tag("s6", "c", "AU SENS MÉDICAL", f"{C} top: 560px; font-size: 72px; color: #fff;", 17.03))),
    ("s7", "cafe", 18.76, 21.00, "whip", *acc(
        tag("s7", "a", "CE QUE TU DOIS", f"{C} top: 250px; font-size: 70px; color: #fff;", 19.25),
        lab("s7", "b", "RETENIR", "left: 250px; top: 360px; font-size: 150px;", 19.73))),
    ("s8", "four", 21.00, 23.20, "flash", *acc(
        lab("s8", "a", "PRODUITS TRÈS SUCRÉS", "left: 90px; top: 300px; font-size: 68px;", 22.05, white=True))),
    ("s9", "cookies3", 23.20, 26.31, "zoom", *acc(
        tag("s9", "a", "PLUS DIFFICILE", f"{C} top: 250px; font-size: 84px; color: #fff;", 23.73),
        lab("s9", "b", "DE RÉSISTER", "left: 220px; top: 380px; font-size: 110px;", 24.64),
        tag("s9", "c", "AUX ENVIES", f"{C} top: 560px; font-size: 84px; color: #fff;", 25.51))),
    ("s10", "patisserie", 26.31, 29.00, "whip", *acc(
        lab("s10", "a", "LA PROCHAINE FOIS", "left: 100px; top: 250px; font-size: 80px;", 27.10, white=True),
        tag("s10", "b", "ENVIE DE SUCRE", f"{C} top: 400px; font-size: 90px; color: #fff;", 28.00))),
    ("s11", "cacao2", 29.00, 32.59, "flash", *acc(
        tag("s11", "a", "DEMANDE-TOI", f"{C} top: 250px; font-size: 90px; color: #fff;", 29.03, out=30.0),
        lab("s11", "b", "VRAIMENT FAIM", "left: 150px; top: 330px; font-size: 100px;", 30.40, white=True),
        lab("s11", "c", "OU JUSTE UNE ENVIE ?", "left: 100px; top: 500px; font-size: 68px;", 31.38))),
    ("s12", "cookies2", 32.59, 36.89, "zoom", *acc(
        tag("s12", "a", "DIS-MOI EN COMMENTAIRE", f"{C} top: 250px; font-size: 60px; color: #fff;", 32.73, out=34.0),
        big("s12", "n", "7", f"left: 380px; top: 280px; font-size: 420px; color: {A}; {SH}", 34.74),
        lab("s12", "j", "JOURS", "left: 330px; top: 700px; font-size: 120px;", 35.06),
        tag("s12", "s", "SANS SUCRE AJOUTÉ", f"{C} top: 860px; font-size: 64px; color: #fff;", 35.22))),
    ("s13", "fin", 36.89, D, "whip", *acc(
        ('<div id="s13-end"><div class="tag" id="s13-ab">ABONNE-TOI</div><div class="tag" id="s13-nv">UNE NOUVELLE VIDÉO CHAQUE JOUR</div>'
         '<img id="s13-logo" src="assets/brand/icon-512.png" alt="CaliBodi" /><div class="big" id="s13-name">CaliBodi</div>'
         '<div class="lab" id="s13-url">calibodi.com</div><div class="tag" id="s13-st">Play Store · App Store</div></div>',
         "#s13-end { position: absolute; inset: 0; }"
         "#s13-ab { left: 0; width: 1080px; top: 190px; text-align: center; font-size: 84px; color: #fff; }"
         "#s13-nv { left: 0; width: 1080px; top: 300px; text-align: center; font-size: 46px; color: #fff; }"
         "#s13-logo { position: absolute; left: 400px; top: 410px; width: 280px; height: 280px; border-radius: 62px; box-shadow: 0 20px 50px rgba(0,0,0,.5); }"
         "#s13-name { left: 0; width: 1080px; top: 720px; text-align: center; font-size: 150px; color: #fff; text-shadow: 0 16px 50px rgba(0,0,0,.7); }"
         "#s13-url { left: 230px; top: 880px; font-size: 100px; }"
         "#s13-st { left: 0; width: 1080px; top: 1015px; text-align: center; font-size: 56px; color: #fff; }",
         'tl.fromTo("#s13-ab",{y:50,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(37.01));'
         'tl.fromTo("#s13-nv",{y:50,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(37.87));'
         'tl.fromTo("#s13-logo",{scale:0,rotation:-40},{scale:1,rotation:0,duration:.45,ease:"back.out(2.6)"},at(38.40));'
         'tl.fromTo("#s13-name",{scale:2.4,opacity:0},{scale:1,opacity:1,duration:.26,ease:"power4.out"},at(39.00));'
         'tl.fromTo("#s13-url",{scale:2.4,opacity:0,rotation:-6},{scale:1,opacity:1,rotation:-3,duration:.24,ease:"power4.out"},at(39.40));'
         'tl.fromTo("#s13-st",{y:40,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(40.00));'))),
]
PUNCH = [(1.14, 1.08), (5.54, 1.08), (7.47, 1.06), (9.71, 1.05), (12.03, 1.07), (16.14, 1.08), (19.73, 1.06), (22.05, 1.05),
         (24.64, 1.05), (28.00, 1.05), (30.40, 1.06), (34.74, 1.09), (39.00, 1.05)]
SHAKE = [16.14, 34.74]
POSES = [(0.18, "curieux"), (4.10, "sceptique"), (6.40, "nutrition"), (8.50, "curieux"), (11.50, "explique"), (14.60, "non"),
         (18.80, "pointe"), (21.05, "nutrition"), (23.30, "sceptique"), (26.40, "pointe"), (29.10, "curieux"),
         (32.80, "pointe"), (38.40, "app"), (39.40, "pouce")]
KW = {"sucre", "volonté", "compliqué", "sucré", "cerveau", "récompense", "plaisir", "drogue", "médical", "retenir", "difficile",
      "résister", "envies", "envie", "faim", "commentaire", "jours", "ajouté", "calibodi", "calibodicom", "7"}
CHAPTERS = [0.0, 6.31, 14.53, 26.31]
