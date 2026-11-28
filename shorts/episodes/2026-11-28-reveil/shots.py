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
A = "#35C7FF"


def T(sid, name, text, top, size, t, out=None):
    return tag(sid, name, text, f"{C} top: {top}px; font-size: {size}px; color: #fff;", t, out)


def L(sid, name, text, left, top, size, t, white=False, out=None):
    return lab(sid, name, text, f"left: {left}px; top: {top}px; font-size: {size}px;", t, white=white, out=out)


A = "#35C7FF"
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
    ("s1", None, [("TU REPOUSSES", 0.29), ("TON RÉVEIL", 0.82), ("3 OU 4 FOIS", 1.22), ("CHAQUE MATIN ?", 2.02)]),
    ("s2", "whip", [("DORMIR", 4.19), ("5 MINUTES", 4.51), ("DE PLUS…", 5.07)]),
    ("s3", "zoom", [("TU TE LÈVES", 5.95), ("COMPLÈTEMENT", 6.19), ("DANS LE BROUILLARD ?", 6.76)]),
    ("s4", "flash", [("NE VENAIT PAS", 8.52), ("SEULEMENT", 8.92), ("DU NOMBRE D'HEURES", 9.32), ("QUE TU DORS ?", 9.97)]),
    ("s5", "whip", [("TU TE RÉVEILLES", 11.25), ("À DES HEURES", 11.91), ("TRÈS DIFFÉRENTES", 12.37), ("CHAQUE JOUR", 13.02)]),
    ("s6", "zoom", [("TON HORLOGE", 14.06), ("BIOLOGIQUE", 14.54), ("MAL À GARDER", 15.50), ("UN RYTHME RÉGULIER", 16.32)]),
    ("s7", "flash", [("RÉSULTAT :", 17.67), ("CERTAINS MATINS", 18.71), ("PLUS FATIGUÉ", 20.40), ("QUE D'AUTRES", 21.04)]),
    ("s8", "whip", [("UNE ASTUCE", 22.82), ("À TESTER", 23.53), ("DÈS DEMAIN", 23.93)]),
    ("s9", "zoom", [("PENDANT 1 SEMAINE", 25.05), ("TE LEVER", 26.74), ("MÊME HEURE", 27.62)]),
    ("s10", "flash", [("MÊME LE", 28.58), ("WEEK-END", 28.87), ("ÉVITE", 30.12), ("LES GROS DÉCALAGES", 30.51)]),
    ("s11", "whip", [("DÈS QUE", 32.13), ("TU TE LÈVES", 32.60), ("OUVRE LES VOLETS", 33.58), ("EXPOSE-TOI", 34.54), ("À LA LUMIÈRE", 35.13)]),
    ("s12", "zoom", [("CETTE LUMIÈRE", 36.53), ("AIDE TON CERVEAU", 37.19), ("À COMPRENDRE", 37.83), ("LA JOURNÉE COMMENCE", 38.55)]),
    ("s13", "flash", [("RÉGULER", 40.54), ("TON RYTHME", 40.94), ("VEILLE-SOMMEIL", 41.42)]),
    ("s14", "whip", [("AUTRE", 42.88), ("PETIT CONSEIL", 43.11)]),
    ("s15", "zoom", [("ÉVITE DE RESTER", 44.25), ("10 MINUTES", 45.03), ("À REPOUSSER", 45.53), ("TON RÉVEIL", 46.08)]),
    ("s16", "flash", [("PRÉPARE", 47.04), ("TES AFFAIRES", 47.68), ("LA VEILLE", 48.16)]),
    ("s17", "whip", [("TON TÉLÉPHONE", 49.21), ("ASSEZ LOIN", 49.79), ("TE LEVER", 50.36)]),
    ("s18", "zoom", [("PAS FORCÉMENT", 51.86), ("CHAMPION", 52.92), ("DU RÉVEIL", 53.38), ("DU JOUR AU LENDEMAIN", 53.78)]),
    ("s19", "flash", [("MAIS PARFOIS", 54.91), ("COMMENCER", 55.87), ("TA JOURNÉE", 56.35), ("PAS BESOIN", 57.19), ("DE TE FORCER", 57.80)]),
    ("s20", "whip", [("SURTOUT", 59.40), ("BESOIN", 59.72), ("UN RYTHME", 61.10), ("PLUS RÉGULIER", 61.49)]),
]
import json as _j
_S = _j.load(open(os.path.join(EP, "source/shotplan.json")))
BOUNDS = [(a, b) for sid, src, a, b, ss in _S][:20]
SHOTS = [(sid, sid, a, b, tr, *mk(sid, items, b)) for (sid, tr, items), (a, b) in zip(PLAN, BOUNDS)]
SHOTS.append(("s21", "s21", 62.60, D, "zoom", *acc(
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
     'tl.fromTo("#s21-ab",{y:50,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(62.87));'
     'tl.fromTo("#s21-nv",{y:50,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(63.59));'
     'tl.fromTo("#s21-logo",{scale:0,rotation:-40},{scale:1,rotation:0,duration:.45,ease:"back.out(2.6)"},at(65.20));'
     'tl.fromTo("#s21-name",{scale:2.4,opacity:0},{scale:1,opacity:1,duration:.26,ease:"power4.out"},at(65.62));'
     'tl.fromTo("#s21-url",{scale:2.4,opacity:0,rotation:-6},{scale:1,opacity:1,rotation:-3,duration:.24,ease:"power4.out"},at(66.19));'
     'tl.fromTo("#s21-st",{y:40,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(66.80));'))))
PUNCH = [(0.29, 1.06), (1.22, 1.07), (4.51, 1.07), (6.76, 1.07), (9.32, 1.06), (11.97, 1.06), (14.54, 1.07), (16.35, 1.06), (18.71, 1.06),
         (20.56, 1.07), (22.82, 1.06), (27.62, 1.06), (28.87, 1.07), (33.58, 1.07), (36.77, 1.06), (41.42, 1.07), (45.03, 1.07),
         (47.68, 1.06), (49.79, 1.06), (52.98, 1.07), (56.51, 1.06), (59.72, 1.06), (61.49, 1.07), (65.62, 1.05)]
SHAKE = [1.22, 52.98]
POSES = [(0.20, "fatigue"), (3.05, "endormi"), (5.35, "fatigue"), (7.85, "curieux"), (11.10, "explique"), (14.05, "explique"),
         (17.65, "fatigue"), (22.05, "pouce"), (25.00, "pointe"), (28.60, "pointe"), (32.05, "explique"), (36.55, "pouce"),
         (39.95, "explique"), (42.75, "pointe"), (44.30, "non"), (47.05, "pouce"), (49.05, "pointe"), (51.65, "sceptique"),
         (54.90, "pouce"), (59.25, "explique"), (62.85, "app"), (65.30, "pouce")]
KW = {"réveil", "matin", "matins", "minutes", "brouillard", "problème", "heures", "horloge", "biologique", "rythme", "régulier",
      "fatigué", "astuce", "demain", "semaine", "heure", "week-end", "volets", "lumière", "cerveau", "journée", "veille-sommeil",
      "dix", "téléphone", "champion", "lendemain", "corps", "calibodi", "calibodicom", "calibodi.com", "repousses", "dors"}
CHAPTERS = [0.0, 22.00, 42.70]
