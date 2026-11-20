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
                f'<g class="ih" id="{sid}-h{i}" opacity="0">{shape("#FF8A1F")}</g></g>' for i in range(n))
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
A = "#FF8A1F"


def T(sid, name, text, top, size, t, out=None):
    return tag(sid, name, text, f"{C} top: {top}px; font-size: {size}px; color: #fff;", t, out)


def L(sid, name, text, left, top, size, t, white=False, out=None):
    return lab(sid, name, text, f"left: {left}px; top: {top}px; font-size: {size}px;", t, white=white, out=out)


# Shot list of « protéines » (voix du 2026-11-20). Images : entraînement vu de profil / de dos (pas de visage), aliments, anatomie 3D.
SHOTS = [
    ("s1", "s1", 0.00, 2.85, None, *acc(
        L("s1", "a", "TU T'ENTRAÎNES DUR", 60, 210, 76, 0.34),
        L("s1", "b", "PAS DE MUSCLE ?", 90, 400, 96, 1.38, white=True))),
    ("s2", "s2", 2.85, 7.79, "whip", *acc(
        T("s2", "a", "TES SÉANCES", 210, 96, 3.00, out=4.35),
        L("s2", "b", "SÉRIEUSES", 220, 400, 120, 3.63, out=4.35),
        T("s2", "c", "TU TRANSPIRES", 210, 100, 4.43, out=5.80),
        L("s2", "d", "TU DONNES TOUT", 120, 400, 80, 5.15, white=True, out=5.80),
        T("s2", "e", "TON PHYSIQUE NE CHANGE", 210, 60, 6.02),
        L("s2", "f", "PRESQUE PAS ?", 90, 380, 92, 6.75))),
    ("s3", "s3", 7.79, 10.37, "zoom", *acc(
        T("s3", "a", "ET SI LE PROBLÈME", 210, 84, 8.00),
        T("s3", "b", "NE VENAIT PAS DE", 330, 70, 8.66),
        L("s3", "c", "TON ENTRAÎNEMENT ?", 70, 450, 76, 9.26, white=True))),
    ("s4", "s4", 10.37, 13.55, "flash", *acc(
        L("s4", "a", "ON PARLE SOUVENT DES", 50, 200, 60, 10.45, white=True),
        L("s4", "b", "EXERCICES", 200, 330, 110, 11.10),
        L("s4", "c", "SÉRIES", 330, 520, 110, 11.81, white=True),
        L("s4", "d", "RÉPÉTITIONS", 120, 700, 100, 12.45))),
    ("s5", "s5", 13.55, 17.03, "whip", *acc(
        T("s5", "a", "MAIS ON OUBLIE", 210, 84, 13.66, out=15.50),
        L("s5", "b", "L'ESSENTIEL", 120, 380, 112, 14.57, out=15.50),
        T("s5", "c", "CE QUE TU", 210, 90, 15.58),
        L("s5", "d", "MANGES", 250, 380, 150, 15.98, white=True))),
    ("s6", "s6", 17.03, 18.75, "zoom", *acc(
        T("s6", "a", "TES MUSCLES", 210, 100, 17.10),
        L("s6", "b", "SE DÉVELOPPER", 120, 400, 80, 17.83))),
    ("s7", "s7", 18.75, 20.60, "flash", *acc(
        T("s7", "a", "TON CORPS A BESOIN DE", 210, 70, 18.79),
        L("s7", "b", "PROTÉINES", 150, 380, 130, 19.67))),
    ("s8", "s8", 20.60, 23.90, "whip", *acc(
        L("s8", "a", "RÉPARER", 280, 230, 130, 20.64),
        T("s8", "b", "ET CONSTRUIRE", 420, 100, 21.36),
        T("s8", "c", "LES TISSUS", 600, 100, 21.92),
        L("s8", "d", "MUSCULAIRES", 140, 760, 100, 22.24, white=True),
        T("s8", "e", "APRÈS L'EFFORT", 930, 80, 22.98))),
    ("s9", "s9", 23.90, 27.30, "zoom", *acc(
        L("s9", "a", "ET NON", 280, 230, 150, 24.12),
        T("s9", "b", "PAS FORCÉMENT BESOIN", 430, 66, 24.97),
        L("s9", "c", "POUDRES", 150, 600, 120, 25.93, white=True),
        L("s9", "d", "COMPLÉMENTS", 100, 780, 100, 26.41))),
    ("s10", "s10", 27.30, 27.82, None, *acc(
        L("s10", "a", "ŒUFS", 300, 400, 170, 27.50))),
    ("s11", "s11", 27.82, 28.40, None, *acc(
        L("s11", "a", "POISSON", 200, 400, 150, 27.86, white=True))),
    ("s12", "s12", 28.40, 29.50, None, *acc(
        T("s12", "a", "PRODUITS", 300, 110, 28.58),
        L("s12", "b", "LAITIERS", 150, 460, 140, 28.85))),
    ("s13", "s13", 29.50, 30.22, None, *acc(
        L("s13", "a", "LÉGUMINEUSES", 70, 400, 100, 29.62, white=True))),
    ("s14", "s14", 30.22, 32.45, None, *acc(
        L("s14", "a", "VIANDE", 260, 380, 160, 30.41),
        T("s14", "b", "DÉJÀ T'EN APPORTER", 640, 78, 30.91))),
    ("s15", "s15", 32.45, 34.30, "flash", *acc(
        T("s15", "a", "AVANT DE CHANGER", 210, 90, 33.01),
        L("s15", "b", "TON PROGRAMME", 70, 400, 92, 33.79, white=True))),
    ("s16", "s16", 34.30, 36.80, "zoom", *acc(
        T("s16", "a", "REGARDE AUSSI", 210, 100, 34.35),
        L("s16", "b", "TON ASSIETTE", 100, 400, 96, 35.81))),
    ("s17", "s17", 36.80, 41.66, "whip", *acc(
        L("s17", "a", "DIS-MOI", 280, 230, 130, 36.92, out=38.30),
        T("s17", "b", "EN COMMENTAIRE", 420, 100, 37.32, out=38.30),
        T("s17", "c", "ATTENTION À TES", 210, 90, 38.78, out=40.20),
        L("s17", "d", "PROTÉINES ?", 150, 400, 120, 39.41, white=True, out=40.20),
        T("s17", "e", "OU TU MANGES", 210, 100, 40.37),
        L("s17", "f", "AU HASARD ?", 120, 400, 96, 40.87))),
    ("s18", "s18", 41.66, D, "flash", *acc(
        ('<div id="s18-end"><div class="tag" id="s18-ab">ABONNE-TOI</div><div class="tag" id="s18-nv">UNE NOUVELLE VIDÉO CHAQUE JOUR</div>'
         '<img id="s18-logo" src="assets/brand/icon-512.png" alt="CaliBodi" /><div class="big" id="s18-name">CaliBodi</div>'
         '<div class="lab" id="s18-url">calibodi.com</div><div class="tag" id="s18-st">Play Store · App Store</div></div>',
         "#s18-end { position: absolute; inset: 0; }"
         "#s18-ab { left: 0; width: 1080px; top: 190px; text-align: center; font-size: 84px; color: #fff; }"
         "#s18-nv { left: 0; width: 1080px; top: 300px; text-align: center; font-size: 46px; color: #fff; }"
         "#s18-logo { position: absolute; left: 400px; top: 410px; width: 280px; height: 280px; border-radius: 62px; box-shadow: 0 20px 50px rgba(0,0,0,.5); }"
         "#s18-name { left: 0; width: 1080px; top: 720px; text-align: center; font-size: 150px; color: #fff; text-shadow: 0 16px 50px rgba(0,0,0,.7); }"
         "#s18-url { left: 230px; top: 880px; font-size: 100px; }"
         "#s18-st { left: 0; width: 1080px; top: 1015px; text-align: center; font-size: 56px; color: #fff; }",
         'tl.fromTo("#s18-ab",{y:50,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(41.80));'
         'tl.fromTo("#s18-nv",{y:50,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(42.38));'
         'tl.fromTo("#s18-logo",{scale:0,rotation:-40},{scale:1,rotation:0,duration:.45,ease:"back.out(2.6)"},at(44.55));'
         'tl.fromTo("#s18-name",{scale:2.4,opacity:0},{scale:1,opacity:1,duration:.26,ease:"power4.out"},at(44.55));'
         'tl.fromTo("#s18-url",{scale:2.4,opacity:0,rotation:-6},{scale:1,opacity:1,rotation:-3,duration:.24,ease:"power4.out"},at(45.15));'
         'tl.fromTo("#s18-st",{y:40,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(45.80));'))),
]
PUNCH = [(0.34, 1.07), (1.38, 1.06), (3.63, 1.06), (5.15, 1.07), (6.75, 1.06), (9.26, 1.07), (11.10, 1.06), (12.45, 1.07),
         (14.57, 1.08), (15.98, 1.07), (17.83, 1.06), (19.67, 1.07), (24.12, 1.07), (25.93, 1.06), (27.50, 1.07), (28.85, 1.06),
         (30.41, 1.07), (33.79, 1.06), (35.81, 1.07), (39.41, 1.06), (40.87, 1.07), (44.55, 1.05)]
SHAKE = [14.57]
POSES = [(0.20, "biceps"), (3.00, "fatigue"), (6.00, "sceptique"), (7.90, "choc"), (10.50, "explique"), (15.60, "nutrition"),
         (18.90, "biceps"), (20.70, "explique"), (24.00, "non"), (27.40, "pointe"), (32.60, "curieux"), (34.40, "pointe"),
         (36.90, "curieux"), (41.80, "app"), (44.90, "pouce")]
KW = {"t'entraînes", "muscle", "muscles", "essentiel", "manges", "protéines", "poudres", "compléments", "œufs", "poisson", "laitiers",
      "légumineuses", "viande", "assiette", "programme", "hasard", "calibodi", "calibodicom", "entraînement"}
CHAPTERS = [0.0, 10.37, 23.90]
