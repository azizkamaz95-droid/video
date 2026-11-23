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
                f'<g class="ih" id="{sid}-h{i}" opacity="0">{shape("#C9A7FF")}</g></g>' for i in range(n))
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
A = "#C9A7FF"


def T(sid, name, text, top, size, t, out=None):
    return tag(sid, name, text, f"{C} top: {top}px; font-size: {size}px; color: #fff;", t, out)


def L(sid, name, text, left, top, size, t, white=False, out=None):
    return lab(sid, name, text, f"left: {left}px; top: {top}px; font-size: {size}px;", t, white=white, out=out)


# Shot list de « pump musculaire » (voix du 2026-11-24). Anatomie 3D, cellules du sang, ballon et pompe, germination, lune, sablier, horloge ; aucune personne.
SHOTS = [
    ("s1", "s1", 0.00, 3.30, None, *acc(
        T("s1", "a", "TU REGARDES TES BRAS", 210, 62, 1.65),
        L("s1", "b", "DANS LE MIROIR", 90, 400, 100, 2.34, white=True))),
    ("s2", "s2", 3.30, 6.30, "whip", *acc(
        L("s2", "a", "SURPRISE", 150, 210, 130, 3.54),
        T("s2", "b", "BEAUCOUP PLUS GROS", 420, 70, 5.14))),
    ("s3", "s3", 6.30, 9.40, "zoom", *acc(
        T("s3", "a", "LE LENDEMAIN", 210, 100, 6.67),
        L("s3", "b", "EFFET PRESQUE DISPARU", 40, 420, 66, 7.65, white=True))),
    ("s4", "s4", 9.40, 12.30, "flash", *acc(
        T("s4", "a", "TU AS PERDU", 210, 90, 10.11),
        L("s4", "b", "TES MUSCLES ?", 90, 400, 110, 10.79, white=True),
        T("s4", "c", "PENDANT LA NUIT", 600, 70, 11.11))),
    ("s5", "s5", 12.30, 15.90, "whip", *acc(
        L("s5", "a", "PAS DU TOUT !", 100, 210, 100, 12.36, white=True),
        T("s5", "b", "LE PUMP", 420, 120, 14.33),
        L("s5", "c", "MUSCULAIRE", 150, 590, 110, 14.76, white=True))),
    ("s6", "s6", 15.90, 19.85, "zoom", *acc(
        T("s6", "a", "PENDANT L'ENTRAÎNEMENT", 210, 52, 16.19, out=17.05),
        L("s6", "b", "LE SANG", 200, 210, 130, 17.17, white=True),
        L("s6", "c", "AFFLUE", 220, 400, 140, 17.42),
        T("s6", "d", "VERS LES MUSCLES", 600, 70, 18.21))),
    ("s7", "s7", 19.85, 23.70, "flash", *acc(
        T("s7", "a", "TEMPORAIREMENT", 210, 70, 20.37),
        L("s7", "b", "LEUR VOLUME", 120, 400, 100, 21.16, white=True),
        T("s7", "c", "PLUS GONFLÉ", 600, 100, 22.78))),
    ("s8", "s8", 23.70, 27.50, "whip", *acc(
        L("s8", "a", "ATTENTION", 140, 210, 120, 24.04, out=25.30),
        L("s8", "b", "PAS UNE CROISSANCE", 80, 210, 68, 25.36),
        L("s8", "c", "INSTANTANÉE", 100, 420, 120, 26.32, white=True))),
    ("s9", "s9", 27.50, 31.00, "zoom", *acc(
        L("s9", "a", "HYPERTROPHIE", 60, 210, 100, 28.16, white=True),
        T("s9", "b", "DÉVELOPPEMENT", 420, 78, 29.59),
        L("s9", "c", "DE TES MUSCLES", 80, 600, 90, 30.26))),
    ("s10", "s10", 31.00, 34.10, "flash", *acc(
        T("s10", "a", "SE CONSTRUIT", 210, 100, 31.19, out=32.40),
        L("s10", "b", "ENTRAÎNEMENTS", 60, 210, 100, 32.81, white=True),
        T("s10", "c", "RÉGULIERS", 420, 130, 33.20))),
    ("s11", "s11", 34.10, 36.00, "whip", *acc(
        L("s11", "a", "RÉCUPÉRATION", 80, 210, 110, 34.33),
        T("s11", "b", "SUFFISANTE", 420, 110, 35.04))),
    ("s12", "s12", 36.00, 37.65, "zoom", *acc(
        L("s12", "a", "ALIMENTATION", 100, 210, 110, 36.10, white=True),
        T("s12", "b", "ADAPTÉE", 420, 130, 36.66))),
    ("s13", "s13", 37.65, 42.00, "flash", *acc(
        L("s13", "a", "INTÉRESSANT", 100, 210, 110, 38.42, white=True, out=39.40),
        T("s13", "b", "LE PUMP", 210, 110, 39.57),
        L("s13", "c", "MOTIVANT", 160, 400, 120, 40.28),
        T("s13", "d", "PAS FIABLE", 600, 100, 41.54))),
    ("s14", "s14", 42.00, 45.50, "whip", *acc(
        T("s14", "a", "INDICATEUR FIABLE", 210, 78, 42.17),
        L("s14", "b", "QUALITÉ DE TA SÉANCE", 40, 400, 66, 42.73, white=True),
        L("s14", "c", "FUTURS RÉSULTATS", 90, 600, 76, 44.17))),
    ("s15", "s15", 45.50, 49.80, "zoom", *acc(
        L("s15", "a", "BRAS ÉNORMES", 100, 210, 110, 46.74, white=True, out=47.55),
        T("s15", "b", "APRÈS LES POMPES", 210, 80, 47.63),
        L("s15", "c", "PROFITE DU MIROIR", 60, 420, 82, 48.42, white=True))),
    ("s16", "s16", 49.80, 53.00, "flash", *acc(
        T("s16", "a", "NE CONFONDS PAS", 210, 84, 50.02),
        L("s16", "b", "EFFET TEMPORAIRE", 60, 400, 90, 50.68, white=True),
        L("s16", "c", "MUSCLE GAGNÉ", 120, 600, 100, 51.72))),
    ("s17", "s17", 53.00, 57.60, "whip", *acc(
        T("s17", "a", "LE MUSCLE", 210, 110, 53.10),
        L("s17", "b", "SE CONSTRUIT", 100, 400, 110, 53.71, white=True),
        T("s17", "c", "AVEC LE TEMPS", 600, 100, 54.13),
        T("s17", "d", "QUELQUES MINUTES", 780, 80, 55.41),
        L("s17", "e", "DEVANT LE MIROIR", 90, 940, 80, 56.13, white=True))),
    ("s18", "s18", 57.60, D, "flash", *acc(
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
         'tl.fromTo("#s18-ab",{y:50,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(57.76));'
         'tl.fromTo("#s18-nv",{y:50,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(58.31));'
         'tl.fromTo("#s18-logo",{scale:0,rotation:-40},{scale:1,rotation:0,duration:.45,ease:"back.out(2.6)"},at(60.00));'
         'tl.fromTo("#s18-name",{scale:2.4,opacity:0},{scale:1,opacity:1,duration:.26,ease:"power4.out"},at(60.60));'
         'tl.fromTo("#s18-url",{scale:2.4,opacity:0,rotation:-6},{scale:1,opacity:1,rotation:-3,duration:.24,ease:"power4.out"},at(61.25));'
         'tl.fromTo("#s18-st",{y:40,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(61.95));'))),
]
PUNCH = [(2.34, 1.06), (3.54, 1.08), (5.47, 1.06), (7.65, 1.06), (10.79, 1.07), (14.33, 1.07), (17.42, 1.07), (21.16, 1.06),
         (22.94, 1.07), (25.50, 1.06), (26.32, 1.07), (28.16, 1.06), (30.26, 1.06), (32.81, 1.06), (33.20, 1.07), (34.33, 1.06),
         (36.10, 1.06), (39.57, 1.07), (40.28, 1.06), (42.17, 1.06), (44.17, 1.06), (46.74, 1.07), (48.90, 1.06), (50.68, 1.06),
         (51.72, 1.07), (54.60, 1.06), (56.49, 1.06), (60.60, 1.05)]
SHAKE = [3.54]
POSES = [(0.20, "curieux"), (3.54, "choc"), (6.50, "sceptique"), (9.50, "curieux"), (12.40, "pouce"), (13.40, "explique"),
         (16.00, "explique"), (20.00, "biceps"), (23.90, "pointe"), (27.60, "explique"), (31.20, "biceps"), (34.30, "curieux"),
         (36.10, "nutrition"), (37.80, "explique"), (42.10, "non"), (45.60, "pointe"), (49.90, "sceptique"), (53.10, "pouce"),
         (57.80, "app"), (60.00, "pouce")]
KW = {"bras", "miroir", "gros", "lendemain", "disparu", "muscles", "nuit", "pump", "musculaire", "sang", "afflue", "volume",
      "gonflé", "attention", "croissance", "instantanée", "hypertrophie", "développement", "entraînements", "réguliers",
      "récupération", "alimentation", "intéressant", "motivant", "fiable", "séance", "résultats", "énormes", "pompes",
      "temporaire", "gagné", "temps", "minutes", "calibodi", "calibodicom"}
CHAPTERS = [0.0, 12.3, 27.5]
