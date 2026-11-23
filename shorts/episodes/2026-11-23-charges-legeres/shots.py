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
                f'<g class="ih" id="{sid}-h{i}" opacity="0">{shape("#FF8FA3")}</g></g>' for i in range(n))
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
A = "#FF8FA3"


def T(sid, name, text, top, size, t, out=None):
    return tag(sid, name, text, f"{C} top: {top}px; font-size: {size}px; color: #fff;", t, out)


def L(sid, name, text, left, top, size, t, white=False, out=None):
    return lab(sid, name, text, f"left: {left}px; top: {top}px; font-size: {size}px;", t, white=white, out=out)


# Shot list de « charges légères » (voix du 2026-11-23). Haltères et kettlebells vus de loin ou recadrés (aucun visage), barre et disques, anatomie 3D.
SHOTS = [
    ("s1", "s1", 0.00, 2.30, None, *acc(
        T("s1", "a", "ET SI JE TE DISAIS", 210, 70, 0.30),
        L("s1", "b", "DES MUSCLES", 90, 400, 92, 1.86, white=True))),
    ("s2", "s2", 2.30, 4.70, "whip", *acc(
        T("s2", "a", "HALTÈRES", 210, 120, 2.60),
        L("s2", "b", "TROP LÉGERS ?", 60, 400, 100, 3.98))),
    ("s3", "s3", 4.70, 8.80, "zoom", *acc(
        T("s3", "a", "POUR PRENDRE DU MUSCLE", 210, 62, 6.04),
        L("s3", "b", "TOUJOURS PLUS", 90, 400, 100, 7.72, white=True),
        L("s3", "c", "LOURD ?", 250, 580, 140, 8.20))),
    ("s4", "s4", 8.80, 12.00, "flash", *acc(
        T("s4", "a", "LES RECHERCHES", 210, 84, 9.60),
        L("s4", "b", "SCIENTIFIQUES", 90, 400, 90, 9.97, white=True),
        L("s4", "c", "UNE AUTRE HISTOIRE", 60, 600, 70, 11.03))),
    ("s5", "s5", 12.00, 15.90, "whip", *acc(
        src("s5", "Schoenfeld et coll., J Strength Cond Res, 2017 (charges légères et lourdes)", 13.30),
        T("s5", "a", "DES ÉTUDES", 210, 100, 12.39, out=13.45),
        L("s5", "b", "CHARGES LÉGÈRES", 70, 210, 84, 13.90, white=True),
        L("s5", "c", "CROISSANCE", 130, 420, 110, 15.10))),
    ("s6", "s6", 15.90, 19.25, "zoom", *acc(
        T("s6", "a", "COMPARABLE", 210, 110, 16.23),
        L("s6", "b", "CHARGES LOURDES", 70, 420, 90, 17.78, white=True))),
    ("s7", "s7", 19.25, 22.40, "flash", *acc(
        L("s7", "a", "ATTENTION", 120, 210, 130, 19.45),
        T("s7", "b", "UNE CONDITION", 420, 90, 20.74),
        L("s7", "c", "IMPORTANTE", 150, 580, 120, 21.30, white=True))),
    ("s8", "s8", 22.40, 25.00, "whip", *acc(
        T("s8", "a", "QUELQUES RÉPÉTITIONS", 210, 62, 22.73),
        L("s8", "b", "FACILES", 220, 400, 140, 23.61, white=True),
        L("s8", "c", "NE SUFFIT PAS", 90, 600, 100, 24.09))),
    ("s9", "s9", 25.00, 29.00, "zoom", *acc(
        T("s9", "a", "CHARGE LÉGÈRE", 210, 80, 25.46, out=26.90),
        L("s9", "b", "POUSSE TES SÉRIES", 60, 210, 80, 26.98, white=True),
        T("s9", "c", "PRÈS DE TES LIMITES", 420, 70, 28.35))),
    ("s10", "s10", 29.00, 31.65, "flash", *acc(
        L("s10", "a", "STIMULER", 150, 210, 130, 29.71, white=True),
        T("s10", "b", "TES MUSCLES", 420, 110, 30.91))),
    ("s11", "s11", 31.65, 36.25, "whip", *acc(
        T("s11", "a", "C'EST LÀ", 210, 110, 31.96, out=33.50),
        L("s11", "b", "INTÉRESSANT", 100, 400, 110, 32.62, white=True, out=33.50),
        L("s11", "c", "NE REGARDE PAS", 70, 210, 90, 34.08),
        T("s11", "d", "LE POIDS", 420, 120, 34.84),
        L("s11", "e", "SUR L'HALTÈRE", 100, 600, 90, 35.39, white=True))),
    ("s12", "s12", 36.25, 39.95, "zoom", *acc(
        T("s12", "a", "TENSION MÉCANIQUE", 210, 72, 37.41),
        L("s12", "b", "ET EFFORT", 190, 420, 130, 38.31, white=True))),
    ("s13", "s13", 39.95, 44.30, "flash", *acc(
        T("s13", "a", "DEVENIR PLUS FORT", 210, 78, 41.90, out=42.90),
        L("s13", "b", "MOUVEMENT PRÉCIS", 60, 210, 80, 43.14, white=True))),
    ("s14", "s14", 44.30, 46.50, "whip", *acc(
        T("s14", "a", "CHARGES LOURDES", 210, 80, 44.47),
        L("s14", "b", "UN AVANTAGE", 100, 420, 100, 45.45, white=True))),
    ("s15", "s15", 46.50, 52.60, "zoom", *acc(
        L("s15", "a", "RETIENS CECI", 100, 210, 110, 46.89, out=48.50),
        T("s15", "b", "POUR CONSTRUIRE", 210, 80, 48.64, out=49.95),
        L("s15", "c", "DU MUSCLE", 150, 400, 120, 49.12, white=True, out=50.20),
        T("s15", "d", "SOULEVER PLUS LOURD", 210, 66, 50.16),
        L("s15", "e", "N'EST PAS", 130, 400, 110, 51.08, white=True),
        L("s15", "f", "LA SEULE SOLUTION", 60, 580, 80, 51.69))),
    ("s16", "s16", 52.60, 56.25, "flash", *acc(
        T("s16", "a", "CE QUI COMPTE", 210, 90, 52.76, out=53.95),
        T("s16", "b", "DONNER À TES MUSCLES", 210, 62, 54.01, out=54.70),
        L("s16", "c", "UNE RAISON", 120, 210, 120, 54.93, white=True),
        L("s16", "d", "DE S'ADAPTER", 70, 420, 110, 55.25))),
    ("s17", "s17", 56.25, D, "whip", *acc(
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
         'tl.fromTo("#s17-ab",{y:50,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(56.44));'
         'tl.fromTo("#s17-nv",{y:50,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(57.16));'
         'tl.fromTo("#s17-logo",{scale:0,rotation:-40},{scale:1,rotation:0,duration:.45,ease:"back.out(2.6)"},at(59.45));'
         'tl.fromTo("#s17-name",{scale:2.4,opacity:0},{scale:1,opacity:1,duration:.26,ease:"power4.out"},at(59.60));'
         'tl.fromTo("#s17-url",{scale:2.4,opacity:0,rotation:-6},{scale:1,opacity:1,rotation:-3,duration:.24,ease:"power4.out"},at(60.25));'
         'tl.fromTo("#s17-st",{y:40,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(60.95));'))),
]
PUNCH = [(2.60, 1.07), (3.98, 1.06), (7.72, 1.06), (8.20, 1.07), (9.97, 1.06), (13.90, 1.06), (15.10, 1.07), (17.78, 1.06),
         (19.45, 1.08), (21.30, 1.06), (23.61, 1.07), (24.09, 1.06), (28.35, 1.07), (30.91, 1.06), (31.96, 1.06), (34.84, 1.08),
         (38.31, 1.06), (42.70, 1.07), (45.45, 1.07), (49.12, 1.06), (51.69, 1.07), (54.93, 1.06), (55.25, 1.07), (59.60, 1.05)]
SHAKE = [19.45]
POSES = [(0.20, "curieux"), (2.60, "pointe"), (4.90, "explique"), (9.00, "curieux"), (12.40, "explique"), (14.00, "biceps"),
         (16.20, "pouce"), (19.40, "pointe"), (22.50, "non"), (25.10, "biceps"), (29.70, "explique"), (31.90, "curieux"),
         (34.10, "non"), (36.50, "explique"), (40.10, "sceptique"), (44.50, "pointe"), (46.70, "explique"), (49.10, "biceps"),
         (52.70, "pouce"), (56.40, "app"), (59.60, "pouce")]
KW = {"muscles", "muscle", "haltères", "légers", "lourd", "lourdes", "recherches", "scientifiques", "études", "charges", "légères",
      "croissance", "comparable", "attention", "condition", "importante", "répétitions", "faciles", "limites", "stimuler",
      "poids", "haltère", "tension", "mécanique", "effort", "fort", "précis", "avantage", "retiens", "solution", "raison",
      "s'adapter", "calibodi", "calibodicom"}
CHAPTERS = [0.0, 12.0, 31.65]
