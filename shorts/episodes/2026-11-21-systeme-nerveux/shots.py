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
                f'<g class="ih" id="{sid}-h{i}" opacity="0">{shape("#FFD60A")}</g></g>' for i in range(n))
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
A = "#FFD60A"


def T(sid, name, text, top, size, t, out=None):
    return tag(sid, name, text, f"{C} top: {top}px; font-size: {size}px; color: #fff;", t, out)


def L(sid, name, text, left, top, size, t, white=False, out=None):
    return lab(sid, name, text, f"left: {left}px; top: {top}px; font-size: {size}px;", t, white=white, out=out)


# Shot list of « système nerveux » (voix du 2026-11-21). Silhouettes à contre-jour (pas de visage), cerveau et neurones en 3D, microscope.
SHOTS = [
    ("s1", "s1", 0.00, 3.50, None, *acc(
        T("s1", "a", "TU VIENS DE COMMENCER", 210, 64, 0.34),
        L("s1", "b", "LA MUSCULATION", 100, 360, 84, 1.09, white=True),
        T("s1", "c", "EN QUELQUES SEMAINES", 560, 60, 2.42))),
    ("s2", "s2", 3.50, 5.50, "whip", *acc(
        T("s2", "a", "DÉJÀ À SOULEVER", 200, 78, 3.95),
        L("s2", "b", "PLUS LOURD", 80, 380, 120, 4.83))),
    ("s3", "s3", 5.50, 9.10, "zoom", *acc(
        T("s3", "a", "TES MUSCLES", 210, 100, 5.83),
        L("s3", "b", "PRESQUE PAS", 50, 380, 112, 7.40),
        L("s3", "c", "VISUELLEMENT", 100, 560, 96, 8.12, white=True))),
    ("s4", "s4", 9.10, 11.39, "flash", *acc(
        L("s4", "a", "COMMENT", 140, 300, 150, 9.89, white=True),
        T("s4", "b", "C'EST POSSIBLE ?", 520, 80, 10.29))),
    ("s5", "s5", 11.39, 14.00, "whip", *acc(
        T("s5", "a", "LA RÉPONSE", 210, 100, 11.50),
        L("s5", "b", "SYSTÈME", 200, 380, 130, 12.70),
        L("s5", "c", "NERVEUX", 280, 560, 130, 13.02, white=True))),
    ("s6", "s6", 14.00, 19.00, "zoom", *acc(
        T("s6", "a", "QUAND TU DÉBUTES", 200, 80, 14.06, out=15.10),
        L("s6", "b", "TON CERVEAU", 80, 200, 110, 15.35),
        L("s6", "c", "TES NERFS", 160, 380, 120, 16.02, white=True),
        T("s6", "d", "APPRENNENT", 560, 96, 16.33),
        L("s6", "e", "MIEUX COMMANDER", 80, 740, 84, 17.47, white=True),
        T("s6", "f", "TES MUSCLES", 920, 80, 18.16))),
    ("s7", "s7", 19.00, 21.60, "flash", *acc(
        T("s7", "a", "ILS AMÉLIORENT", 200, 90, 19.30),
        L("s7", "b", "RECRUTEMENT", 90, 330, 110, 19.80),
        L("s7", "c", "UNITÉS MOTRICES", 60, 520, 88, 20.50, white=True))),
    ("s8", "s8", 21.60, 24.55, "whip", *acc(
        T("s8", "a", "C'EST-À-DIRE", 210, 100, 21.69, out=22.30),
        L("s8", "b", "GROUPES DE FIBRES", 90, 210, 72, 22.33, white=True),
        T("s8", "c", "MUSCULAIRES", 400, 100, 23.01),
        L("s8", "d", "ACTIVÉS", 250, 580, 120, 23.55))),
    ("s9", "s9", 24.55, 25.56, "zoom", *acc(
        L("s9", "a", "UN EFFORT", 100, 380, 130, 24.68))),
    ("s10", "s10", 25.56, 29.00, "flash", *acc(
        L("s10", "a", "RÉSULTAT", 120, 210, 140, 25.66, white=True),
        T("s10", "b", "DAVANTAGE DE", 420, 100, 27.79),
        L("s10", "c", "FORCE", 280, 560, 190, 28.36))),
    ("s11", "s11", 29.00, 31.99, "whip", *acc(
        T("s11", "a", "PARFOIS AVANT MÊME", 200, 70, 29.08),
        T("s11", "b", "QUE TES MUSCLES", 320, 84, 30.04),
        L("s11", "c", "VISIBLEMENT", 100, 500, 110, 30.52, white=True),
        L("s11", "d", "GROSSI", 250, 700, 150, 31.08))),
    ("s12", "s12", 31.99, 37.75, "zoom", *acc(
        src("s12", "Del Vecchio et coll., J Physiol, 2019 (4 semaines d'entraînement)", 34.20),
        T("s12", "a", "PAS UNE SIMPLE", 210, 90, 32.53, out=33.90),
        L("s12", "b", "THÉORIE", 280, 380, 130, 33.01, out=33.90),
        T("s12", "c", "DES CHERCHEURS", 210, 90, 34.05),
        L("s12", "d", "4 SEMAINES", 60, 380, 130, 36.38, white=True),
        T("s12", "e", "D'ENTRAÎNEMENT", 560, 80, 36.94))),
    ("s13", "s13", 37.75, 41.55, "flash", *acc(
        T("s13", "a", "MAIS ATTENTION", 210, 90, 38.18),
        T("s13", "b", "CELA NE SIGNIFIE PAS", 330, 60, 38.95),
        L("s13", "c", "TES MUSCLES", 80, 450, 110, 40.11),
        L("s13", "d", "TRAVAILLENT", 120, 630, 100, 40.56, white=True))),
    ("s14", "s14", 41.55, 45.65, "whip", *acc(
        L("s14", "a", "DÉVELOPPEMENT", 100, 230, 90, 41.76),
        L("s14", "b", "TRÈS TÔT", 280, 420, 120, 43.04, white=True),
        T("s14", "c", "EN PARALLÈLE", 600, 90, 43.69),
        T("s14", "d", "ADAPTATIONS NERVEUSES", 740, 60, 44.34))),
    ("s15", "s15", 45.65, 49.55, "zoom", *acc(
        T("s15", "a", "LA PROCHAINE FOIS", 210, 70, 46.98),
        L("s15", "b", "PLUS LOURD", 80, 380, 120, 48.18, white=True),
        T("s15", "c", "SOUVIENS-TOI", 560, 90, 49.23))),
    ("s16", "s16", 49.55, 54.45, "flash", *acc(
        L("s16", "a", "UNE CHOSE", 160, 230, 120, 49.79, out=50.55),
        T("s16", "b", "TU NE CONSTRUIS PAS", 210, 64, 50.83, out=52.40),
        L("s16", "c", "TES MUSCLES", 80, 380, 110, 51.55, white=True, out=52.40),
        T("s16", "d", "TU APPRENDS", 210, 100, 52.62),
        L("s16", "e", "À MIEUX LES UTILISER", 60, 380, 64, 53.28, white=True))),
    ("s17", "s17", 54.45, D, "flash", *acc(
        ('<div id="s17-end"><div class="tag" id="s17-ab">ABONNE-TOI</div><div class="tag" id="s17-nv">UNE NOUVELLE VIDÉO CHAQUE JOUR</div>'
         '<img id="s17-logo" src="assets/brand/icon-512.png" alt="CaliBodi" /><div class="big" id="s17-name">CaliBodi</div>'
         '<div class="lab" id="s17-url">calibodi.com</div><div class="tag" id="s17-st">Play Store · App Store</div></div>',
         "#s17-end { position: absolute; inset: 0; }"
         "#s17-ab { left: 0; width: 1080px; top: 190px; text-align: center; font-size: 84px; color: #fff; }"
         "#s17-nv { left: 0; width: 1080px; top: 300px; text-align: center; font-size: 46px; color: #fff; }"
         "#s17-logo { position: absolute; left: 400px; top: 410px; width: 280px; height: 280px; border-radius: 62px; box-shadow: 0 20px 50px rgba(0,0,0,.5); }"
         "#s17-name { left: 0; width: 1080px; top: 720px; text-align: center; font-size: 150px; color: #fff; text-shadow: 0 16px 50px rgba(0,0,0,.7); }"
         "#s17-url { left: 230px; top: 880px; font-size: 100px; }"
         "#s17-st { left: 0; width: 1080px; top: 1015px; text-align: center; font-size: 56px; color: #fff; }",
         'tl.fromTo("#s17-ab",{y:50,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(54.80));'
         'tl.fromTo("#s17-nv",{y:50,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(55.36));'
         'tl.fromTo("#s17-logo",{scale:0,rotation:-40},{scale:1,rotation:0,duration:.45,ease:"back.out(2.6)"},at(57.00));'
         'tl.fromTo("#s17-name",{scale:2.4,opacity:0},{scale:1,opacity:1,duration:.26,ease:"power4.out"},at(57.00));'
         'tl.fromTo("#s17-url",{scale:2.4,opacity:0,rotation:-6},{scale:1,opacity:1,rotation:-3,duration:.24,ease:"power4.out"},at(57.76));'
         'tl.fromTo("#s17-st",{y:40,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(58.50));'))),
]
PUNCH = [(0.34, 1.07), (1.09, 1.06), (4.83, 1.07), (7.40, 1.07), (9.89, 1.08), (12.70, 1.08), (15.35, 1.06), (16.02, 1.06),
         (19.80, 1.07), (22.33, 1.06), (24.68, 1.07), (28.36, 1.08), (30.52, 1.06), (33.01, 1.06), (36.38, 1.07), (40.56, 1.06),
         (43.04, 1.07), (48.18, 1.07), (51.55, 1.06), (53.28, 1.07), (57.00, 1.05)]
SHAKE = [12.70]
POSES = [(0.20, "biceps"), (5.60, "sceptique"), (9.20, "curieux"), (11.50, "explique"), (14.10, "explique"), (19.10, "pointe"),
         (25.60, "biceps"), (29.10, "sceptique"), (32.00, "curieux"), (38.10, "non"), (41.70, "explique"), (46.00, "pointe"),
         (52.60, "pouce"), (54.80, "app"), (57.90, "pouce")]
KW = {"muscles", "musculation", "lourd", "cerveau", "nerfs", "nerveux", "système", "unités", "motrices", "fibres", "force", "théorie",
      "chercheurs", "quatre", "semaines", "développement", "utiliser", "apprends", "construis", "calibodi", "calibodicom", "grossi", "effort"}
CHAPTERS = [0.0, 11.39, 31.99]
