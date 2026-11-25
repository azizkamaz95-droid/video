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
                f'<g class="ih" id="{sid}-h{i}" opacity="0">{shape("#00D68F")}</g></g>' for i in range(n))
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
A = "#00D68F"


def T(sid, name, text, top, size, t, out=None):
    return tag(sid, name, text, f"{C} top: {top}px; font-size: {size}px; color: #fff;", t, out)


def L(sid, name, text, left, top, size, t, white=False, out=None):
    return lab(sid, name, text, f"left: {left}px; top: {top}px; font-size: {size}px;", t, white=white, out=out)


# Shot list de « cinq minutes » (voix du 2026-11-25). Réveil, jambes qui marchent, chat, porte, cerveau 3D, horloges, mains qui lacent une chaussure, bouton START ; aucun visage.
SHOTS = [
    ("s1", "s1", 0.00, 2.75, None, *acc(
        L("s1", "a", "TU REPOUSSES", 100, 210, 110, 0.29, white=True),
        L("s1", "b", "TOUJOURS", 200, 400, 110, 0.66),
        L("s1", "c", "BON POUR TOI", 90, 600, 100, 1.70, white=True))),
    ("s2", "s2", 2.75, 5.80, "whip", *acc(
        T("s2", "a", "MARCHER", 210, 130, 3.47),
        L("s2", "b", "MIEUX MANGER", 100, 400, 100, 3.90, white=True),
        T("s2", "c", "REPRENDRE LE SPORT", 600, 70, 4.59))),
    ("s3", "s3", 5.80, 8.25, "zoom", *acc(
        L("s3", "a", "TU FINIS ENCORE", 90, 210, 80, 6.04, white=True, out=6.70),
        L("s3", "b", "REMETTRE", 100, 210, 120, 6.76),
        L("s3", "c", "À DEMAIN ?", 160, 420, 120, 7.26, white=True))),
    ("s4", "s4", 8.25, 11.70, "flash", *acc(
        L("s4", "a", "LE PROBLÈME ?", 90, 210, 100, 8.61, white=True),
        L("s4", "b", "PAS TON MANQUE", 60, 420, 90, 9.90),
        L("s4", "c", "DE MOTIVATION ?", 40, 620, 90, 10.38, white=True))),
    ("s5", "s5", 11.70, 16.45, "whip", *acc(
        T("s5", "a", "UNE TÂCHE", 210, 100, 12.24, out=14.55),
        L("s5", "b", "IMPORTANTE", 130, 400, 110, 13.05, white=True, out=14.55),
        T("s5", "c", "OU DIFFICILE", 600, 100, 13.59, out=14.55),
        T("s5", "d", "TON CERVEAU", 210, 110, 14.80),
        L("s5", "e", "L'ÉVITER", 200, 400, 130, 15.46, white=True))),
    ("s6", "s6", 16.45, 20.68, "zoom", *acc(
        T("s6", "a", "LE CONFORT", 210, 100, 17.45),
        L("s6", "b", "IMMÉDIAT", 150, 400, 120, 17.95, white=True),
        T("s6", "c", "UN BÉNÉFICE", 600, 90, 18.57, out=19.65),
        L("s6", "d", "PLUS TARD", 160, 600, 110, 19.70))),
    ("s7", "s7", 20.68, 24.43, "flash", *acc(
        T("s7", "a", "UNE ASTUCE", 210, 100, 21.56),
        L("s7", "b", "TOUTE SIMPLE", 100, 400, 100, 22.03, white=True),
        T("s7", "c", "DÈS AUJOURD'HUI", 600, 84, 23.23))),
    ("s8", "s8", 24.43, 29.10, "whip", *acc(
        L("s8", "a", "AU LIEU DE TE DIRE", 40, 210, 66, 24.61, white=True, out=25.55),
        L("s8", "b", "DEMAIN", 200, 210, 120, 25.64),
        L("s8", "c", "SÉANCE DE SPORT", 60, 420, 80, 26.53, white=True),
        L("s8", "d", "30 MINUTES", 140, 620, 120, 27.41))),
    ("s9", "s9", 29.10, 31.94, "zoom", *acc(
        T("s9", "a", "JE VAIS JUSTE", 210, 80, 29.25, out=29.65),
        T("s9", "b", "METTRE MES", 210, 100, 29.69),
        L("s9", "c", "CHAUSSURES", 80, 420, 120, 30.06, white=True),
        L("s9", "d", "5 MINUTES", 200, 620, 120, 30.70))),
    ("s10", "s10", 31.94, 36.73, "flash", *acc(
        L("s10", "a", "C'EST TOUT", 150, 210, 120, 32.14, white=True, out=32.75),
        L("s10", "b", "ÇA PEUT FONCTIONNER ?", 30, 210, 66, 33.38, white=True),
        L("s10", "c", "RÉDUIS", 220, 420, 130, 34.74),
        L("s10", "d", "LA DIFFICULTÉ DE DÉPART", 20, 620, 62, 35.19, white=True))),
    ("s11", "s11", 36.73, 40.20, "whip", *acc(
        L("s11", "a", "LE PLUS DUR", 100, 210, 120, 37.35, white=True, out=38.35),
        L("s11", "b", "PAS CONTINUER", 60, 210, 100, 38.43, out=38.95),
        L("s11", "c", "COMMENCER", 110, 420, 120, 39.12, white=True))),
    ("s12", "s12", 40.20, 43.30, "zoom", *acc(
        T("s12", "a", "CINQ MINUTES", 210, 100, 40.84),
        L("s12", "b", "ARRÊTER", 200, 400, 130, 41.70, white=True),
        T("s12", "c", "TU PEUX", 600, 100, 42.25))),
    ("s13", "s13", 43.30, 46.49, "flash", *acc(
        T("s13", "a", "DÉJÀ FAIT", 210, 110, 43.69),
        L("s13", "b", "QUELQUE CHOSE", 70, 400, 100, 44.09, white=True),
        T("s13", "c", "REPOUSSÉ", 600, 110, 44.78))),
    ("s14", "s14", 46.49, 51.42, "whip", *acc(
        L("s14", "a", "LA PROCHAINE FOIS", 40, 210, 78, 47.06, white=True, out=47.65),
        L("s14", "b", "TU BLOQUES", 150, 210, 110, 47.70, out=48.25),
        L("s14", "c", "NE CHERCHE PAS", 60, 210, 90, 48.34, white=True),
        L("s14", "d", "À TE MOTIVER", 120, 420, 100, 49.02),
        L("s14", "e", "TOUTE LA TÂCHE", 80, 620, 100, 50.19, white=True))),
    ("s15", "s15", 51.42, 56.74, "zoom", *acc(
        T("s15", "a", "LE PREMIER PAS", 210, 100, 52.44),
        L("s15", "b", "TELLEMENT FACILE", 40, 400, 90, 53.40, white=True),
        T("s15", "c", "PLUS DE RAISON", 600, 90, 54.92),
        L("s15", "d", "DE LE REPOUSSER", 40, 800, 90, 55.76))),
    ("s16", "s16", 56.74, D, "flash", *acc(
        ('<div id="s16-end"><div class="tag" id="s16-ab">ABONNE-TOI</div><div class="tag" id="s16-nv">UNE NOUVELLE VIDÉO CHAQUE JOUR</div>'
         '<img id="s16-logo" src="assets/brand/icon-512.png" alt="CaliBodi" /><div class="big" id="s16-name">CaliBodi</div>'
         '<div class="lab" id="s16-url">calibodi.com</div><div class="tag" id="s16-st">Play Store · App Store</div></div>',
         "#s16-end { position: absolute; inset: 0; }"
         "#s16-ab { left: 0; width: 1080px; top: 190px; text-align: center; font-size: 84px; color: #fff; }"
         "#s16-nv { left: 0; width: 1080px; top: 300px; text-align: center; font-size: 46px; color: #fff; }"
         "#s16-logo { position: absolute; left: 400px; top: 410px; width: 280px; height: 280px; border-radius: 62px; box-shadow: 0 20px 50px rgba(0,0,0,.5); }"
         "#s16-name { left: 0; width: 1080px; top: 720px; text-align: center; font-size: 150px; color: #fff; text-shadow: 0 16px 50px rgba(0,0,0,.7); }"
         "#s16-url { left: 230px; top: 880px; font-size: 100px; }"
         "#s16-st { left: 0; width: 1080px; top: 1015px; text-align: center; font-size: 56px; color: #fff; }",
         'tl.fromTo("#s16-ab",{y:50,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(56.78));'
         'tl.fromTo("#s16-nv",{y:50,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(57.66));'
         'tl.fromTo("#s16-logo",{scale:0,rotation:-40},{scale:1,rotation:0,duration:.45,ease:"back.out(2.6)"},at(59.35));'
         'tl.fromTo("#s16-name",{scale:2.4,opacity:0},{scale:1,opacity:1,duration:.26,ease:"power4.out"},at(59.97));'
         'tl.fromTo("#s16-url",{scale:2.4,opacity:0,rotation:-6},{scale:1,opacity:1,rotation:-3,duration:.24,ease:"power4.out"},at(60.60));'
         'tl.fromTo("#s16-st",{y:40,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(61.30));'))),
]
PUNCH = [(0.66, 1.06), (3.47, 1.07), (3.90, 1.06), (6.76, 1.07), (7.26, 1.07), (10.79, 1.06), (13.05, 1.06), (14.80, 1.07),
         (15.46, 1.07), (17.95, 1.06), (19.70, 1.06), (22.03, 1.06), (25.64, 1.07), (27.41, 1.07), (30.06, 1.06), (30.70, 1.07),
         (34.74, 1.07), (39.12, 1.07), (40.84, 1.06), (41.70, 1.06), (44.09, 1.06), (44.78, 1.07), (48.34, 1.06), (49.02, 1.06),
         (52.44, 1.07), (55.76, 1.06), (59.97, 1.05)]
SHAKE = [7.26]
POSES = [(0.20, "sceptique"), (2.80, "pointe"), (5.90, "non"), (8.30, "curieux"), (11.80, "explique"), (16.50, "explique"),
         (20.70, "pouce"), (24.50, "pointe"), (29.20, "pouce"), (32.00, "explique"), (36.80, "pointe"), (40.30, "pouce"),
         (43.40, "biceps"), (46.60, "pointe"), (51.50, "pouce"), (56.80, "app"), (59.50, "pouce")]
KW = {"repousses", "toujours", "marcher", "manger", "sport", "remettre", "demain", "problème", "motivation", "tâche",
      "importante", "difficile", "cerveau", "éviter", "confort", "immédiat", "bénéfice", "astuce", "simple", "aujourd'hui",
      "trente", "chaussures", "cinq", "minutes", "réduis", "difficulté", "dur", "continuer", "commencer", "arrêter", "repoussais",
      "bloques", "motiver", "premier", "facile", "repousser", "calibodi", "calibodicom"}
CHAPTERS = [0.0, 20.68, 36.73]
