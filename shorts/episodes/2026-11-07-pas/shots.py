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
                f'<g class="ih" id="{sid}-h{i}" opacity="0">{shape("#FF3D81")}</g></g>' for i in range(n))
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
# Shot list of « Les 10 000 pas », read by build_v4.py. Global times in seconds (voice of 2026-11-07).
# Footage: paths, forests, a city skyline, hikers seen from behind (no women, no faces, no logos).
A = "#FF3D81"
SHOTS = [
    ("s1", "marche", 0.00, 4.10, None, *acc(
        tag("s1", "a", "SI TU FAIS", f"{C} top: 250px; font-size: 80px; color: #fff;", 0.30),
        big("s1", "n", "10 000", f"{C} top: 340px; font-size: 270px; color: {A}; {SH}", 0.70),
        lab("s1", "d", "PAS PAR JOUR", "left: 220px; top: 650px; font-size: 100px;", 1.05, white=True),
        lab("s1", "i", "INDISPENSABLE ?", "left: 110px; top: 810px; font-size: 84px;", 2.60))),
    ("s2", "cerf", 4.10, 6.70, "whip", *acc(
        tag("s2", "a", "POUR ÊTRE EN BONNE SANTÉ", f"{C} top: 250px; font-size: 56px; color: #fff;", 4.15, out=5.0),
        lab("s2", "s", "UNE SURPRISE", "left: 110px; top: 330px; font-size: 100px;", 5.10),
        big("s2", "q", "!", f"left: 700px; top: 520px; font-size: 460px; color: {A}; {SH}", 5.90))),
    ("s3", "skytree1", 6.70, 10.90, "zoom", *acc(
        tag("s3", "a", "D'OÙ VIENT CE CHIFFRE ?", f"{C} top: 250px; font-size: 62px; color: #fff;", 6.85, out=8.2),
        lab("s3", "j", "JAPON", "left: 300px; top: 300px; font-size: 170px;", 8.40),
        big("s3", "n", "1965", f"{C} top: 520px; font-size: 330px; color: {A}; {SH}", 9.30),
        src("s3", "Yamasa (Manpo-kei, 1965) · I-Min Lee, Harvard", 7.0))),
    ("s4", "skytree2", 10.90, 14.40, "flash", *acc(
        tag("s4", "a", "UNE ENTREPRISE", f"{C} top: 250px; font-size: 80px; color: #fff;", 11.00),
        lab("s4", "p", "PODOMÈTRE", "left: 200px; top: 380px; font-size: 140px;", 12.50),
        lab("s4", "m", "MANPO-KEI", "left: 150px; top: 580px; font-size: 120px;", 13.40, white=True))),
    ("s5", "cascade", 14.40, 17.90, "whip", *acc(
        tag("s5", "s", "SIGNIFIE", f"{C} top: 250px; font-size: 80px; color: #fff;", 14.60, out=16.2),
        tag("s5", "c", "COMPTEUR DE", f"{C} top: 250px; font-size: 80px; color: #fff;", 16.30),
        big("s5", "n", "10 000", f"{C} top: 360px; font-size: 270px; color: {A}; text-shadow: 0 0 50px rgba(0,0,0,.95), 0 10px 30px rgba(0,0,0,.9);", 17.00),
        lab("s5", "p", "PAS", "left: 400px; top: 680px; font-size: 120px;", 17.30, white=True))),
    ("s6", "chemin", 17.90, 22.50, "zoom", *acc(
        tag("s6", "a", "C'ÉTAIT AVANT TOUT", f"{C} top: 250px; font-size: 66px; color: #fff;", 18.00),
        lab("s6", "u", "UNE CAMPAGNE", "left: 150px; top: 380px; font-size: 100px;", 18.70),
        lab("s6", "m", "MARKETING", "left: 130px; top: 540px; font-size: 118px;", 19.30, white=True),
        tag("s6", "n", "PAS UNE RECOMMANDATION", f"{C} top: 780px; font-size: 56px; color: #fff;", 20.60),
        lab("s6", "d", "MÉDICALE", "left: 280px; top: 880px; font-size: 100px;", 21.50))),
    ("s7", "coucher", 22.50, 27.20, "whip", *acc(
        tag("s7", "a", "MAIS ATTENTION", f"{C} top: 250px; font-size: 80px; color: #fff;", 22.80),
        lab("s7", "m", "MARCHER", "left: 250px; top: 400px; font-size: 150px;", 24.80),
        lab("s7", "b", "BIEN AU CONTRAIRE", "left: 110px; top: 590px; font-size: 80px;", 26.10, white=True))),
    ("s8", "barres", 27.20, 31.80, "flash", *acc(
        lab("s8", "e", "ÉTUDE 2025", "left: 200px; top: 230px; font-size: 130px;", 27.80),
        big("s8", "n", "57", f"{C} top: 400px; font-size: 420px; color: {A}; {SH}", 30.50),
        tag("s8", "t", "ÉTUDES", f"{C} top: 800px; font-size: 90px; color: #fff;", 31.10),
        src("s8", "Ding et al., The Lancet Public Health, 2025", 27.6))),
    ("s9", "foret", 31.80, 36.50, "zoom", *acc(
        big("s9", "n", "7 000", f"{C} top: 280px; font-size: 300px; color: {A}; {SH}", 32.30),
        tag("s9", "t", "PAS PAR JOUR", f"{C} top: 610px; font-size: 80px; color: #fff;", 33.00),
        lab("s9", "b", "DÉJÀ DES BÉNÉFICES", "left: 90px; top: 760px; font-size: 80px;", 33.80, white=True),
        src("s9", "7 000 pas contre 2 000 : 47 % de mortalité en moins, toutes causes (Ding et al., The Lancet Public Health, 2025)", 32.0))),
    ("s10", "randonnee", 36.50, 38.70, "whip", *acc(
        tag("s10", "a", "LES BÉNÉFICES", f"{C} top: 250px; font-size: 80px; color: #fff;", 36.80),
        lab("s10", "b", "COMMENCENT AVANT", "left: 110px; top: 400px; font-size: 80px;", 37.70, white=True))),
    ("s11", "foret2", 38.70, 44.40, "flash", *acc(
        tag("s11", "a", "MON CONSEIL", f"{C} top: 250px; font-size: 90px; color: #fff;", 39.50, out=40.8),
        big("s11", "n", "2 000", f"{C} top: 300px; font-size: 300px; color: {A}; {SH}", 41.30),
        tag("s11", "t", "PAS AUJOURD'HUI", f"{C} top: 640px; font-size: 70px; color: #fff;", 41.70),
        lab("s11", "d", "PAS 10 000 DEMAIN", "left: 90px; top: 770px; font-size: 80px;", 43.40, white=True))),
    ("s12", "arbres", 44.40, 47.00, "zoom", *acc(
        tag("s12", "a", "AUGMENTE", f"{C} top: 250px; font-size: 100px; color: #fff;", 44.60),
        lab("s12", "p", "PROGRESSIVEMENT", "left: 80px; top: 410px; font-size: 78px;", 45.10))),
    ("s13", "escalier", 47.00, 51.20, "whip", *acc(
        lab("s13", "e", "LES ESCALIERS", "left: 160px; top: 250px; font-size: 100px;", 47.40),
        lab("s13", "m", "APRÈS MANGER", "left: 200px; top: 410px; font-size: 100px;", 48.30, white=True),
        lab("s13", "r", "RÉGULIER", "left: 220px; top: 600px; font-size: 150px;", 50.40))),
    ("s14", "montagne", 51.20, 55.80, "flash", *acc(
        tag("s14", "a", "RETIENS BIEN ÇA", f"{C} top: 250px; font-size: 80px; color: #fff;", 51.60, out=52.5),
        tag("s14", "b", "TON CORPS", f"{C} top: 250px; font-size: 100px; color: #fff;", 52.60),
        lab("s14", "c", "NE COMPTE PAS", "left: 190px; top: 390px; font-size: 100px;", 53.10, white=True),
        tag("s14", "r", "IL RÉCOMPENSE", f"{C} top: 560px; font-size: 70px; color: #fff;", 54.30),
        lab("s14", "e", "TES EFFORTS", "left: 200px; top: 660px; font-size: 120px;", 55.10))),
    ("s15", "parc", 55.80, 60.20, "whip", *acc(
        ('<div class="ic2" id="s15-ic"><svg viewBox="0 0 140 140"><path d="M14 120 C 20 70, 50 44, 104 44 M84 18 L 122 44 L 84 72" fill="none" stroke="#141414" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" /></svg></div>',
         "#s15-ic { position: absolute; left: 70px; top: 250px; width: 170px; height: 170px; border-radius: 50%; background: #fff; box-shadow: 0 14px 30px rgba(0,0,0,.4); }"
         "#s15-ic svg { position: absolute; left: 25px; top: 25px; width: 120px; height: 120px; overflow: visible; }",
         'tl.fromTo("#s15-ic",{scale:0,rotation:-40},{scale:1,rotation:0,duration:.35,ease:"back.out(2.4)"},at(56.80));'),
        lab("s15", "p", "PARTAGE", "left: 270px; top: 270px; font-size: 130px;", 56.80),
        tag("s15", "q", "À QUELQU'UN QUI SE FORCE<br>À FAIRE 10 000 PAS", f"{C} top: 470px; font-size: 60px; color: #fff; {ML}", 58.00))),
    ("s16", "fin", 60.20, D, "zoom", *acc(
        ('<div id="s16-end"><img id="s16-logo" src="assets/brand/icon-512.png" alt="CaliBodi" /><div class="big" id="s16-name">CaliBodi</div>'
         '<div class="lab" id="s16-url">calibodi.com</div><div class="tag" id="s16-st">Play Store · App Store</div>'
         '<div class="tag" id="s16-oe">ON EST ENSEMBLE !</div></div>',
         "#s16-end { position: absolute; inset: 0; }"
         "#s16-logo { position: absolute; left: 400px; top: 330px; width: 280px; height: 280px; border-radius: 62px; box-shadow: 0 20px 50px rgba(0,0,0,.5); }"
         "#s16-name { left: 0; width: 1080px; top: 650px; text-align: center; font-size: 150px; color: #fff; text-shadow: 0 16px 50px rgba(0,0,0,.7); }"
         "#s16-url { left: 230px; top: 840px; font-size: 100px; }"
         "#s16-st { left: 0; width: 1080px; top: 990px; text-align: center; font-size: 56px; color: #fff; }"
         "#s16-oe { left: 0; width: 1080px; top: 200px; text-align: center; font-size: 84px; color: #fff; }",
         'tl.fromTo("#s16-logo",{scale:0,rotation:-40},{scale:1,rotation:0,duration:.45,ease:"back.out(2.6)"},at(60.40));'
         'tl.fromTo("#s16-name",{scale:2.4,opacity:0},{scale:1,opacity:1,duration:.26,ease:"power4.out"},at(61.30));'
         'tl.fromTo("#s16-url",{scale:2.4,opacity:0,rotation:-6},{scale:1,opacity:1,rotation:-3,duration:.24,ease:"power4.out"},at(62.00));'
         'tl.fromTo("#s16-st",{y:40,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(62.40));'
         'tl.fromTo("#s16-oe",{y:50,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(62.90));'))),
]
PUNCH = [(0.70, 1.08), (1.05, 1.05), (5.10, 1.05), (5.90, 1.08), (8.40, 1.06), (9.30, 1.08), (12.50, 1.06), (13.40, 1.06),
         (17.00, 1.08), (19.30, 1.07), (24.80, 1.06), (30.50, 1.08), (32.30, 1.09), (33.80, 1.05), (41.30, 1.08), (45.10, 1.05),
         (50.40, 1.07), (53.10, 1.05), (55.10, 1.06), (56.80, 1.06), (61.30, 1.05), (62.00, 1.06)]
SHAKE = [5.90, 19.30]
POSES = [(0.18, "curieux"), (4.30, "pointe"), (5.10, "choc"), (6.80, "curieux"), (8.40, "explique"), (11.00, "explique"),
         (17.95, "non"), (22.80, "pointe"), (25.60, "pouce"), (27.40, "explique"), (32.30, "pouce"), (36.80, "curieux"),
         (38.80, "pointe"), (44.60, "biceps"), (47.40, "pointe"), (50.40, "pouce"), (51.60, "explique"), (55.90, "pointe"),
         (60.40, "app"), (62.70, "pouce")]
KW = {"10", "000", "japon", "1965", "manpo-kei", "marketing", "médicale", "57", "7", "bénéfices", "2", "progressivement",
      "régulier", "chiffres", "efforts", "partage", "calibodi", "calibodicom", "ensemble", "surprise", "indispensable", "compteur"}
CHAPTERS = [0.0, 6.7, 22.5, 38.7]
