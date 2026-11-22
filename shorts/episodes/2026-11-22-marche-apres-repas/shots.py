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
                f'<g class="ih" id="{sid}-h{i}" opacity="0">{shape("#7CFF6B")}</g></g>' for i in range(n))
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
A = "#7CFF6B"


def T(sid, name, text, top, size, t, out=None):
    return tag(sid, name, text, f"{C} top: {top}px; font-size: {size}px; color: #fff;", t, out)


def L(sid, name, text, left, top, size, t, white=False, out=None):
    return lab(sid, name, text, f"left: {left}px; top: {top}px; font-size: {size}px;", t, white=white, out=out)


# Shot list de « marche après le repas » (voix du 2026-11-22). Pas, sentiers, sang et anatomie en 3D, plats, laboratoire ; aucun visage.
SHOTS = [
    ("s1", "s1", 0.00, 3.45, None, *acc(
        T("s1", "a0", "LE MEILLEUR RÉFLEXE", 210, 64, 0.58, out=1.42),
        T("s1", "a", "APRÈS TON REPAS", 210, 84, 1.48),
        L("s1", "b", "LE CANAPÉ ?", 50, 400, 120, 3.31, white=True))),
    ("s2", "s2", 3.45, 5.65, "whip", *acc(
        T("s2", "a", "SIMPLEMENT", 210, 100, 4.30),
        L("s2", "b", "MARCHER ?", 100, 380, 130, 4.85))),
    ("s3", "s3", 5.65, 7.95, "zoom", *acc(
        T("s3", "a", "QUAND TU MANGES", 210, 78, 5.80),
        L("s3", "b", "GLUCIDES", 150, 380, 130, 7.00, white=True))),
    ("s4", "s4", 7.95, 10.00, "flash", *acc(
        L("s4", "a", "GLUCOSE", 180, 300, 140, 8.04),
        T("s4", "b", "DANS TON SANG", 520, 90, 9.17))),
    ("s5", "s5", 10.00, 12.80, "whip", *acc(
        L("s5", "a", "C'EST NORMAL", 90, 300, 100, 10.05, white=True),
        T("s5", "b", "CE QUI EST INTÉRESSANT", 520, 60, 11.83))),
    ("s6", "s6", 12.80, 15.85, "zoom", *acc(
        T("s6", "a", "TES MUSCLES", 210, 100, 12.86),
        L("s6", "b", "PEUVENT AIDER", 60, 380, 100, 13.42),
        T("s6", "c", "À UTILISER LE GLUCOSE", 560, 58, 14.11))),
    ("s7", "s7", 15.85, 18.65, "flash", *acc(
        L("s7", "a", "PAS BESOIN", 70, 230, 120, 16.88),
        T("s7", "b", "D'UNE SÉANCE DE SPORT", 420, 58, 17.28),
        L("s7", "c", "INTENSE", 250, 580, 140, 18.18, white=True))),
    ("s8", "s8", 18.65, 21.45, "whip", *acc(
        T("s8", "a", "LORSQU'ILS SE CONTRACTENT", 210, 52, 19.28),
        L("s8", "b", "PENDANT LA MARCHE", 90, 400, 72, 20.33, white=True))),
    ("s9", "s9", 21.45, 24.60, "zoom", *acc(
        T("s9", "a", "ILS FACILITENT", 210, 84, 21.61, out=22.50),
        L("s9", "b", "L'ENTRÉE DU GLUCOSE", 90, 210, 64, 22.57, white=True),
        T("s9", "c", "DANS LES CELLULES", 400, 70, 23.09),
        L("s9", "d", "MUSCULAIRES", 130, 560, 100, 23.62))),
    ("s10", "s10", 24.60, 27.00, "flash", *acc(
        L("s10", "a", "RÉSULTAT", 120, 210, 140, 24.66, white=True),
        T("s10", "b", "LA HAUSSE DU SUCRE", 400, 70, 25.55),
        T("s10", "c", "DANS LE SANG", 560, 90, 26.35))),
    ("s11", "s11", 27.00, 29.50, "whip", *acc(
        T("s11", "a", "APRÈS LE REPAS", 210, 90, 27.01),
        L("s11", "b", "MOINS IMPORTANTE", 100, 400, 74, 28.11, white=True))),
    ("s12", "s12", 29.50, 35.70, "zoom", *acc(
        src("s12", "Méta-analyse, Sports Medicine, 2023 (activité après le repas et glycémie)", 32.00),
        L("s12", "a", "PAS JUSTE UNE", 90, 210, 84, 29.81, out=31.30),
        L("s12", "b", "THÉORIE", 280, 380, 130, 30.60, out=31.30),
        L("s12", "c", "MÉTA-ANALYSE", 100, 210, 100, 31.56, white=True),
        L("s12", "d", "2023", 300, 380, 200, 32.77),
        L("s12", "e", "PLUSIEURS ESSAIS", 100, 600, 80, 34.37, white=True),
        L("s12", "f", "SCIENTIFIQUES", 100, 760, 80, 34.97))),
    ("s13", "s13", 35.70, 38.85, "flash", *acc(
        L("s13", "a", "BOUGER", 250, 230, 150, 36.54, white=True),
        T("s13", "b", "APRÈS MANGER", 420, 100, 36.80),
        L("s13", "c", "MIEUX LIMITER", 100, 600, 90, 38.17))),
    ("s14", "s14", 38.85, 41.00, "whip", *acc(
        L("s14", "a", "PICS DE GLYCÉMIE", 100, 230, 74, 38.87),
        T("s14", "b", "QUE RESTER", 420, 100, 39.67),
        L("s14", "c", "INACTIF", 230, 580, 150, 40.09, white=True))),
    ("s15", "s15", 41.00, 45.40, "zoom", *acc(
        src("s15", "Hashimoto et coll., Scientific Reports, 2025 (marche de 10 min après glucose)", 43.00),
        L("s15", "a", "MÊME UNE ÉTUDE", 80, 210, 84, 41.19, white=True),
        L("s15", "b", "2025", 300, 380, 200, 42.40),
        L("s15", "c", "EFFET POSITIF", 110, 600, 90, 44.02, white=True))),
    ("s16", "s16", 45.40, 47.95, "flash", *acc(
        L("s16", "a", "10 MINUTES", 60, 230, 130, 45.45),
        T("s16", "b", "DE MARCHE", 420, 110, 45.96),
        T("s16", "c", "APRÈS UNE PRISE DE GLUCOSE", 580, 46, 46.42))),
    ("s17", "s17", 47.95, 50.40, "whip", *acc(
        T("s17", "a", "LA PROCHAINE FOIS", 210, 70, 48.58),
        L("s17", "b", "TON REPAS", 200, 400, 130, 49.70, white=True))),
    ("s18", "s18", 50.40, 52.15, "zoom", *acc(
        T("s18", "a", "AVANT DE T'INSTALLER", 210, 62, 50.44),
        L("s18", "b", "LE CANAPÉ", 160, 400, 120, 51.38))),
    ("s19", "s19", 52.15, 54.00, "flash", *acc(
        T("s19", "a", "POURQUOI NE PAS", 210, 80, 52.19),
        L("s19", "b", "QUELQUES PAS ?", 90, 400, 84, 52.99, white=True))),
    ("s20", "s20", 54.00, 57.05, "whip", *acc(
        T("s20", "a", "TON CORPS", 210, 120, 54.13),
        L("s20", "b", "APPRÉCIER", 200, 380, 130, 55.11, white=True),
        L("s20", "c", "PETITE HABITUDE", 80, 580, 80, 55.74))),
    ("s21", "s21", 57.05, D, "flash", *acc(
        ('<div id="s21-end"><div class="tag" id="s21-ab">ABONNE-TOI</div><div class="tag" id="s21-nv">UNE NOUVELLE VIDÉO CHAQUE JOUR</div>'
         '<img id="s21-logo" src="assets/brand/icon-512.png" alt="CaliBodi" /><div class="big" id="s21-name">CaliBodi</div>'
         '<div class="lab" id="s21-url">calibodi.com</div><div class="tag" id="s21-st">Play Store · App Store</div></div>',
         "#s21-end { position: absolute; inset: 0; }"
         "#s21-ab { left: 0; width: 1080px; top: 190px; text-align: center; font-size: 84px; color: #fff; }"
         "#s21-nv { left: 0; width: 1080px; top: 300px; text-align: center; font-size: 46px; color: #fff; }"
         "#s21-logo { position: absolute; left: 400px; top: 410px; width: 280px; height: 280px; border-radius: 62px; box-shadow: 0 20px 50px rgba(0,0,0,.5); }"
         "#s21-name { left: 0; width: 1080px; top: 720px; text-align: center; font-size: 150px; color: #fff; text-shadow: 0 16px 50px rgba(0,0,0,.7); }"
         "#s21-url { left: 230px; top: 880px; font-size: 100px; }"
         "#s21-st { left: 0; width: 1080px; top: 1015px; text-align: center; font-size: 56px; color: #fff; }",
         'tl.fromTo("#s21-ab",{y:50,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(57.20));'
         'tl.fromTo("#s21-nv",{y:50,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(57.95));'
         'tl.fromTo("#s21-logo",{scale:0,rotation:-40},{scale:1,rotation:0,duration:.45,ease:"back.out(2.6)"},at(59.73));'
         'tl.fromTo("#s21-name",{scale:2.4,opacity:0},{scale:1,opacity:1,duration:.26,ease:"power4.out"},at(59.73));'
         'tl.fromTo("#s21-url",{scale:2.4,opacity:0,rotation:-6},{scale:1,opacity:1,rotation:-3,duration:.24,ease:"power4.out"},at(60.41));'
         'tl.fromTo("#s21-st",{y:40,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(61.20));'))),
]
PUNCH = [(1.48, 1.06), (3.31, 1.07), (4.85, 1.07), (7.00, 1.06), (8.04, 1.08), (10.05, 1.06), (13.42, 1.06), (16.88, 1.07),
         (18.18, 1.07), (20.33, 1.06), (22.57, 1.06), (24.66, 1.07), (28.11, 1.07), (30.60, 1.06), (32.77, 1.08), (36.54, 1.07),
         (38.17, 1.06), (40.09, 1.07), (42.40, 1.08), (45.45, 1.07), (49.70, 1.06), (51.38, 1.06), (52.99, 1.07), (55.11, 1.06),
         (59.73, 1.05)]
SHAKE = [8.04]
POSES = [(0.20, "sceptique"), (4.20, "pointe"), (5.80, "explique"), (10.00, "curieux"), (12.86, "biceps"), (15.90, "non"),
         (19.20, "explique"), (24.70, "choc"), (29.60, "sceptique"), (31.50, "explique"), (36.00, "pointe"), (41.10, "curieux"),
         (45.50, "pouce"), (48.20, "explique"), (52.20, "pointe"), (54.10, "pouce"), (57.20, "app"), (59.80, "pouce")]
KW = {"canapé", "marcher", "marche", "glucides", "glucose", "sang", "muscles", "musculaires", "cellules", "séance", "intense",
      "théorie", "méta-analyse", "2023", "2025", "pics", "glycémie", "inactif", "bouger", "dix", "minutes", "pas", "habitude",
      "résultat", "importante", "calibodi", "calibodicom", "repas"}
CHAPTERS = [0.0, 15.85, 29.50]
