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
                f'<g class="ih" id="{sid}-h{i}" opacity="0">{shape("#FFB000")}</g></g>' for i in range(n))
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
A = "#FFB000"


def T(sid, name, text, top, size, t, out=None):
    return tag(sid, name, text, f"{C} top: {top}px; font-size: {size}px; color: #fff;", t, out)


def L(sid, name, text, left, top, size, t, white=False, out=None):
    return lab(sid, name, text, f"left: {left}px; top: {top}px; font-size: {size}px;", t, white=white, out=out)


# Shot list de « respiration » (voix du 2026-11-24). Poumons et squelettes 3D, silhouettes, électrocardiogramme, brume ; aucune personne identifiable.
SHOTS = [
    ("s1", "s1", 0.00, 3.80, None, *acc(
        T("s1", "a", "TU BLOQUES", 210, 100, 0.29),
        L("s1", "b", "TA RESPIRATION", 70, 400, 100, 0.61, white=True),
        L("s1", "c", "POMPES", 80, 600, 100, 1.54),
        L("s1", "d", "SQUATS", 300, 760, 100, 1.94, white=True))),
    ("s2", "s2", 3.80, 6.90, "whip", *acc(
        L("s2", "a", "ATTENTION", 130, 210, 120, 3.80, white=True),
        L("s2", "b", "TES EFFORTS", 100, 420, 100, 5.70))),
    ("s3", "s3", 6.90, 11.70, "zoom", *acc(
        L("s3", "a", "EXERCICE DIFFICILE", 40, 210, 80, 7.24, white=True),
        L("s3", "b", "RETIENNENT", 120, 420, 120, 9.55),
        L("s3", "c", "LEUR SOUFFLE", 90, 600, 100, 10.83, white=True))),
    ("s4", "s4", 11.70, 15.00, "flash", *acc(
        T("s4", "a", "TOUT LEUR CORPS", 210, 80, 12.35),
        L("s4", "b", "OUBLIENT", 130, 400, 130, 13.09, white=True),
        T("s4", "c", "DE RESPIRER", 600, 100, 13.91))),
    ("s5", "s5", 15.00, 18.70, "whip", *acc(
        T("s5", "a", "LA PLUPART", 210, 90, 16.04),
        L("s5", "b", "DES EXERCICES", 90, 400, 100, 16.54, white=True),
        T("s5", "c", "UNE RÈGLE SIMPLE", 600, 78, 17.77))),
    ("s6", "s6", 18.70, 23.40, "zoom", *acc(
        L("s6", "a", "EXPIRE", 200, 210, 140, 18.78, out=20.15),
        T("s6", "b", "QUAND TU POUSSES", 210, 78, 20.20),
        L("s6", "c", "INSPIRE", 180, 600, 140, 21.74, white=True),
        T("s6", "d", "AU RETOUR", 800, 90, 22.53))),
    ("s7", "s7", 23.40, 28.30, "flash", *acc(
        T("s7", "a", "SUR UNE POMPE", 210, 90, 24.31),
        L("s7", "b", "EXPIRE", 80, 400, 110, 24.95, white=True),
        T("s7", "c", "QUAND TU REPOUSSES", 600, 66, 25.68),
        L("s7", "d", "INSPIRE", 150, 780, 110, 26.63),
        T("s7", "e", "TU REDESCENDS", 960, 70, 27.34))),
    ("s8", "s8", 28.30, 35.20, "whip", *acc(
        L("s8", "a", "POURQUOI ?", 150, 210, 120, 28.38, white=True, out=29.45),
        T("s8", "b", "RESPIRER", 210, 100, 29.53, out=30.0),
        T("s8", "c", "RÉGULIÈREMENT", 210, 78, 30.05),
        L("s8", "d", "MIEUX GÉRER", 100, 400, 100, 31.38, white=True),
        T("s8", "e", "TON EFFORT", 600, 110, 32.16),
        L("s8", "f", "TON SOUFFLE", 150, 800, 110, 34.23))),
    ("s9", "s9", 35.20, 39.70, "zoom", *acc(
        L("s9", "a", "ATTENTION", 140, 210, 120, 35.29, white=True),
        T("s9", "b", "PRATIQUANTS", 420, 90, 36.24),
        L("s9", "c", "EXPÉRIMENTÉS", 70, 600, 100, 36.82),
        L("s9", "d", "VOLONTAIREMENT", 60, 800, 80, 38.33, white=True))),
    ("s10", "s10", 39.70, 43.60, "flash", *acc(
        L("s10", "a", "MANŒUVRE", 120, 210, 120, 39.72, white=True),
        T("s10", "b", "DE VALSALVA", 420, 100, 40.33),
        T("s10", "c", "STABILISER LE TRONC", 620, 66, 41.46),
        L("s10", "d", "EFFORTS LOURDS", 80, 800, 90, 42.58))),
    ("s11", "s11", 43.60, 50.10, "whip", *acc(
        T("s11", "a", "MAÎTRISE", 210, 110, 44.86),
        L("s11", "b", "PRÉCAUTIONS", 80, 400, 100, 45.71, white=True),
        T("s11", "c", "HYPERTENSION", 600, 100, 47.14),
        L("s11", "d", "CARDIOVASCULAIRES", 30, 800, 70, 48.76))),
    ("s12", "s12", 50.10, 56.00, "zoom", *acc(
        T("s12", "a", "LA PROCHAINE FOIS", 210, 80, 50.61, out=51.95),
        L("s12", "b", "NE COMPTE PAS", 100, 210, 90, 52.05, white=True, out=52.80),
        L("s12", "c", "TES RÉPÉTITIONS", 60, 210, 90, 52.85, out=53.85),
        T("s12", "d", "FAIS ATTENTION", 210, 90, 53.99, out=54.70),
        L("s12", "e", "À TA RESPIRATION", 40, 400, 90, 54.78, white=True))),
    ("s13", "s13", 56.00, 61.00, "flash", *acc(
        T("s13", "a", "BIEN S'ENTRAÎNER", 210, 80, 56.65),
        L("s13", "b", "SAVOIR POUSSER", 70, 400, 90, 58.04, white=True),
        L("s13", "c", "SAVOIR RESPIRER", 60, 620, 100, 59.62))),
    ("s14", "s14", 61.00, D, "whip", *acc(
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
         'tl.fromTo("#s14-ab",{y:50,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(61.01));'
         'tl.fromTo("#s14-nv",{y:50,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(62.12));'
         'tl.fromTo("#s14-logo",{scale:0,rotation:-40},{scale:1,rotation:0,duration:.45,ease:"back.out(2.6)"},at(63.97));'
         'tl.fromTo("#s14-name",{scale:2.4,opacity:0},{scale:1,opacity:1,duration:.26,ease:"power4.out"},at(64.67));'
         'tl.fromTo("#s14-url",{scale:2.4,opacity:0,rotation:-6},{scale:1,opacity:1,rotation:-3,duration:.24,ease:"power4.out"},at(65.30));'
         'tl.fromTo("#s14-st",{y:40,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(66.00));'))),
]
PUNCH = [(0.61, 1.06), (1.94, 1.07), (5.70, 1.06), (9.55, 1.07), (13.09, 1.08), (17.77, 1.06), (20.20, 1.06), (24.95, 1.07),
         (26.63, 1.07), (31.38, 1.06), (32.16, 1.07), (36.82, 1.06), (40.33, 1.07), (45.71, 1.06), (47.14, 1.07), (52.40, 1.06),
         (54.90, 1.06), (59.62, 1.07), (64.67, 1.05)]
SHAKE = [13.09]
POSES = [(0.20, "curieux"), (3.80, "pointe"), (7.00, "explique"), (12.00, "non"), (15.10, "explique"), (18.80, "pouce"),
         (24.00, "biceps"), (28.40, "curieux"), (35.30, "pointe"), (39.80, "explique"), (44.00, "sceptique"), (50.20, "pointe"),
         (56.20, "pouce"), (61.10, "app"), (63.90, "pouce")]
KW = {"respiration", "pompes", "squats", "efforts", "souffle", "corps", "respirer", "règle", "simple", "expire", "inspire",
      "pousses", "soulèves", "repousses", "redescends", "régulièrement", "effort", "attention", "pratiquants", "expérimentés",
      "manœuvre", "valsalva", "tronc", "lourds", "maîtrise", "précautions", "hypertension", "cardiovasculaires", "répétitions",
      "pousser", "calibodi", "calibodicom"}
CHAPTERS = [0.0, 15.0, 35.2]
