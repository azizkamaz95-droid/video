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
                f'<g class="ih" id="{sid}-h{i}" opacity="0">{shape("#FF6B35")}</g></g>' for i in range(n))
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
A = "#FF6B35"


def T(sid, name, text, top, size, t, out=None):
    return tag(sid, name, text, f"{C} top: {top}px; font-size: {size}px; color: #fff;", t, out)


def L(sid, name, text, left, top, size, t, white=False, out=None):
    return lab(sid, name, text, f"left: {left}px; top: {top}px; font-size: {size}px;", t, white=white, out=out)


# Épisode « envies du soir » (voix du 2026-11-26). Plats, frigo, horloges, villes au crépuscule, mains qui coupent ; aucun visage, aucune femme.
A = "#FF6B35"
TOPS = [210, 420, 620, 810]


def fit(text, maxs=130, width=960):
    return int(max(50, min(maxs, width / (0.70 * len(text)))))


def mk(sid, items, shot_end):
    """items: [(text, t)] ; texts cycle over 4 rows, a row reused hides its previous text. kinds alternate accent/white/centre."""
    parts = []
    last = {}
    rows = []
    for i, (text, t) in enumerate(items):
        row = i % 4
        rows.append(row)
    # out time of item i = start of the next item sharing its row (else none)
    for i, (text, t) in enumerate(items):
        row = rows[i]
        out = next((items[j][1] for j in range(i + 1, len(items)) if rows[j] == row), None)
        size = fit(text, 130 if i % 3 != 2 else 110)
        top = TOPS[row]
        name = f"w{i}"
        if i % 3 == 2:
            parts.append(T(sid, name, text, top, size, t, out=out))
        else:
            left = max(30, int((1080 - 0.70 * size * len(text) - 60) / 2))
            parts.append(L(sid, name, text, left, top, size, t, white=(i % 3 == 1), out=out))
    return acc(*parts)


PLAN = [
    ("s1", None, [("TU MANGES", 0.29), ("LE SOIR", 0.58), ("RASSASIÉ", 1.86)]),
    ("s2", "whip", [("ET POURTANT", 3.06), ("UNE HEURE", 3.96), ("PLUS TARD", 4.42)]),
    ("s3", "zoom", [("DÉJÀ ENVIE", 5.07), ("DE RETOURNER", 5.63), ("À LA CUISINE ?", 6.19)]),
    ("s4", "flash", [("TU CROIS ?", 7.47), ("MANQUE", 8.35), ("DE VOLONTÉ ?", 8.63)]),
    ("s5", "whip", [("MAIS ATTENDS", 9.56), ("LE PROBLÈME", 10.76), ("COMMENCE", 11.40), ("AVANT LE DÎNER", 12.06)]),
    ("s6", "zoom", [("TA JOURNÉE", 13.97), ("MANGER", 14.37), ("TROP PEU", 14.69)]),
    ("s7", "flash", [("SAUTER", 15.70), ("UN REPAS", 15.90), ("PETITES", 17.41), ("PORTIONS", 17.73)]),
    ("s8", "whip", [("TON CORPS", 18.70), ("RÉCLAMER", 19.50), ("DE L'ÉNERGIE", 20.38), ("LE SOIR", 20.94)]),
    ("s9", "zoom", [("LE PIÈGE", 22.23), ("COMPENSER", 23.83), ("SUPPRIMER", 24.39), ("LA NOURRITURE", 25.46), ("LE LENDEMAIN", 26.15)]),
    ("s10", "flash", [("UNE ASTUCE", 27.86), ("TOUTE SIMPLE", 28.32), ("À TESTER", 28.80)]),
    ("s11", "whip", [("DEMAIN", 29.93), ("UNIQUEMENT", 31.71), ("TON DÎNER", 32.42), ("À MIDI", 33.65)]),
    ("s12", "zoom", [("TON REPAS", 34.91), ("PROTÉINES", 36.19)]),
    ("s13", "flash", [("FIBRES", 37.88), ("UNE PORTION", 38.68), ("TE RASSASIE", 39.20), ("VRAIMENT ?", 39.68)]),
    ("s14", "whip", [("PAR EXEMPLE", 40.87), ("ŒUFS", 42.23)]),
    ("s15", "zoom", [("POULET", 42.78)]),
    ("s16", "flash", [("LENTILLES", 43.74)]),
    ("s17", "whip", [("TOFU", 44.46)]),
    ("s18", "zoom", [("LÉGUMES", 45.75)]),
    ("s19", "flash", [("FÉCULENTS", 46.95)]),
    ("s20", "whip", [("ET SURTOUT", 48.07), ("NE CHERCHE PAS", 48.99), ("TE COUCHER", 49.60), ("EN AYANT FAIM", 50.09), ("PERDRE DU POIDS", 50.80)]),
    ("s21", "zoom", [("PARFOIS", 52.65), ("TES ENVIES", 54.19), ("DU SOIR", 54.49)]),
    ("s22", "flash", [("LA SOLUTION", 55.46), ("PAS MANGER MOINS", 56.26), ("MIEUX NOURRIR", 57.74), ("TON CORPS", 58.43), ("TOUTE LA JOURNÉE", 58.91)]),
]
BOUNDS = [(0.00, 2.90), (2.90, 5.05), (5.05, 7.30), (7.30, 9.50), (9.50, 13.20), (13.20, 15.65), (15.65, 18.50), (18.50, 22.00),
          (22.00, 27.20), (27.20, 29.90), (29.90, 34.50), (34.50, 37.85), (37.85, 40.65), (40.65, 42.70), (42.70, 43.70), (43.70, 44.40),
          (44.40, 45.70), (45.70, 46.90), (46.90, 48.00), (48.00, 52.30), (52.30, 55.38), (55.38, 59.90)]
SHOTS = [(sid, sid, a, b, tr, *mk(sid, items, b)) for (sid, tr, items), (a, b) in zip(PLAN, BOUNDS)]
SHOTS.append(("s23", "s23", 59.90, D, "whip", *acc(
    ('<div id="s23-end"><div class="tag" id="s23-ab">ABONNE-TOI</div><div class="tag" id="s23-nv">UNE NOUVELLE VIDÉO CHAQUE JOUR</div>'
     '<img id="s23-logo" src="assets/brand/icon-512.png" alt="CaliBodi" /><div class="big" id="s23-name">CaliBodi</div>'
     '<div class="lab" id="s23-url">calibodi.com</div><div class="tag" id="s23-st">Play Store · App Store</div></div>',
     "#s23-end { position: absolute; inset: 0; }"
     "#s23-ab { left: 0; width: 1080px; top: 190px; text-align: center; font-size: 84px; color: #fff; }"
     "#s23-nv { left: 0; width: 1080px; top: 300px; text-align: center; font-size: 46px; color: #fff; }"
     "#s23-logo { position: absolute; left: 400px; top: 410px; width: 280px; height: 280px; border-radius: 62px; box-shadow: 0 20px 50px rgba(0,0,0,.5); }"
     "#s23-name { left: 0; width: 1080px; top: 720px; text-align: center; font-size: 150px; color: #fff; text-shadow: 0 16px 50px rgba(0,0,0,.7); }"
     "#s23-url { left: 230px; top: 880px; font-size: 100px; }"
     "#s23-st { left: 0; width: 1080px; top: 1015px; text-align: center; font-size: 56px; color: #fff; }",
     'tl.fromTo("#s23-ab",{y:50,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(60.13));'
     'tl.fromTo("#s23-nv",{y:50,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(60.86));'
     'tl.fromTo("#s23-logo",{scale:0,rotation:-40},{scale:1,rotation:0,duration:.45,ease:"back.out(2.6)"},at(62.50));'
     'tl.fromTo("#s23-name",{scale:2.4,opacity:0},{scale:1,opacity:1,duration:.26,ease:"power4.out"},at(62.95));'
     'tl.fromTo("#s23-url",{scale:2.4,opacity:0,rotation:-6},{scale:1,opacity:1,rotation:-3,duration:.24,ease:"power4.out"},at(63.46));'
     'tl.fromTo("#s23-st",{y:40,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(64.20));'))))
PUNCH = [(0.29, 1.06), (1.86, 1.07), (3.96, 1.06), (6.19, 1.07), (8.63, 1.07), (10.76, 1.06), (12.06, 1.06), (14.69, 1.07), (17.73, 1.06),
         (20.38, 1.07), (22.23, 1.08), (25.46, 1.06), (27.86, 1.06), (33.65, 1.07), (36.19, 1.07), (39.68, 1.06), (42.23, 1.08),
         (43.74, 1.06), (44.46, 1.06), (46.95, 1.06), (50.09, 1.07), (54.49, 1.06), (56.26, 1.07), (58.91, 1.06), (62.95, 1.05)]
SHAKE = [22.23, 50.09]
POSES = [(0.20, "curieux"), (2.95, "sceptique"), (5.10, "curieux"), (7.35, "sceptique"), (9.55, "explique"), (13.25, "non"),
         (15.70, "non"), (18.55, "choc"), (22.05, "non"), (27.25, "pouce"), (29.95, "pointe"), (34.55, "explique"), (37.90, "nutrition"),
         (40.70, "nutrition"), (43.75, "pouce"), (48.05, "non"), (52.35, "explique"), (55.40, "pouce"), (59.95, "app"), (62.50, "pouce")]
KW = {"soir", "rassasié", "cuisine", "volonté", "problème", "dîner", "peu", "repas", "portions", "énergie", "piège", "compenser",
      "nourriture", "astuce", "midi", "protéines", "fibres", "rassasie", "œufs", "poulet", "lentilles", "tofu", "légumes", "féculents",
      "faim", "poids", "envies", "solution", "nourrir", "corps", "journée", "calibodi", "calibodicom", "calibodi.com"}
CHAPTERS = [0.0, 27.20, 48.00]
