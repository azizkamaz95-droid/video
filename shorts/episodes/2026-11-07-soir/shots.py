# Shot list of « Manger après 20 h », read by build_v4.py (exec'd after its defaults). Global times in seconds.
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
                f'<g class="ih" id="{sid}-h{i}" opacity="0">{shape("#9B6BFF")}</g></g>' for i in range(n))
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
SHOTS = [
    ("s1", "horloge", 0.00, 4.00, None, *acc(
        tag("s1", "a", "TU NE MANGES PLUS APRÈS", f"{C} top: 250px; font-size: 66px; color: #fff;", 0.83),
        big("s1", "n", "20 H", f"{C} top: 340px; font-size: 400px; color: #9B6BFF; {SH}", 1.06),
        lab("s1", "d", "NE FAIT PAS MAIGRIR PLUS", "left: 50px; top: 840px; font-size: 62px;", 2.75, white=True))),
    ("s2", "fenetre", 4.00, 7.00, "zoom", *acc(
        lab("s2", "p", "3 PREUVES", "left: 200px; top: 250px; font-size: 130px;", 4.51),
        lab("s2", "l", "LA DERNIÈRE ?", "left: 120px; top: 440px; font-size: 100px;", 5.47, white=True),
        big("s2", "q", "!", f"left: 700px; top: 560px; font-size: 460px; color: #9B6BFF; {SH}", 6.12))),
    ("s3", "ville", 7.00, 11.50, "flash", *acc(
        lab("s3", "f", "PREUVE 1", "left: 70px; top: 230px; font-size: 120px;", 7.24, out=8.3),
        big("s3", "n", "139", f"{C} top: 300px; font-size: 400px; color: #9B6BFF; {SH}", 8.44),
        tag("s3", "t", "ADULTES EN OBÉSITÉ", f"{C} top: 700px; font-size: 70px; color: #fff;", 9.02),
        lab("s3", "m", "12 MOIS", "left: 330px; top: 820px; font-size: 100px;", 10.85, white=True),
        src("s3", "Liu et al., New England Journal of Medicine, 2022", 7.6))),
    ("s4", "chrono", 11.50, 16.00, "whip", *acc(
        tag("s4", "a", "MÊME LIMITE DE CALORIES", f"{C} top: 250px; font-size: 66px; color: #fff;", 11.73),
        tag("s4", "g", "UN GROUPE NE MANGEAIT QUE", f"{C} top: 340px; font-size: 56px; color: #fff;", 13.92),
        lab("s4", "h", "8 H À 16 H", "left: 190px; top: 480px; font-size: 140px;", 14.88))),
    ("s5", "vapeur", 16.00, 19.70, "zoom", *acc(
        tag("s5", "r", "RÉSULTAT :", f"{C} top: 250px; font-size: 100px; color: #fff;", 16.31),
        lab("s5", "d", "DIFFÉRENCE", "left: 230px; top: 420px; font-size: 120px;", 17.51),
        lab("s5", "s", "NON SIGNIFICATIVE", "left: 90px; top: 590px; font-size: 64px;", 18.56, white=True))),
    ("s6", "rue", 19.70, 23.50, "flash", *acc(
        lab("s6", "f", "PREUVE 2", "left: 70px; top: 230px; font-size: 120px;", 20.00, out=21.0),
        big("s6", "n", "116", f"{C} top: 300px; font-size: 400px; color: #9B6BFF; {SH}", 21.21),
        tag("s6", "t", "ADULTES EN SURPOIDS", f"{C} top: 700px; font-size: 70px; color: #fff;", 21.54),
        lab("s6", "m", "12 SEMAINES", "left: 250px; top: 820px; font-size: 100px;", 22.89, white=True),
        src("s6", "Lowe et al., JAMA Internal Medicine, 2020", 20.4))),
    ("s7", "ragout", 23.50, 28.00, "whip", *acc(
        lab("s7", "h", "MIDI À 20 H", "left: 170px; top: 300px; font-size: 130px;", 24.93),
        lab("s7", "r", "3 REPAS PAR JOUR", "left: 100px; top: 560px; font-size: 90px;", 26.75, white=True))),
    ("s8", "minuteur", 28.00, 31.30, "zoom", *acc(
        tag("s8", "a", "MÊME CONCLUSION", f"{C} top: 250px; font-size: 90px; color: #fff;", 28.35),
        lab("s8", "d", "PAS DE DIFFÉRENCE", "left: 110px; top: 420px; font-size: 76px;", 29.55),
        lab("s8", "s", "SIGNIFICATIVE", "left: 230px; top: 560px; font-size: 84px;", 30.06, white=True))),
    ("s9", "adn", 31.30, 34.70, "flash", *acc(
        lab("s9", "f", "PREUVE 3", "left: 70px; top: 230px; font-size: 120px;", 31.55, out=32.5),
        big("s9", "n", "16", f"{C} top: 300px; font-size: 460px; color: #9B6BFF; {SH}", 32.60),
        tag("s9", "t", "ADULTES", f"{C} top: 700px; font-size: 90px; color: #fff;", 32.85),
        lab("s9", "m", "EN LABORATOIRE", "left: 190px; top: 840px; font-size: 80px;", 33.67, white=True),
        src("s9", "Vujović et al., Cell Metabolism, 2022", 31.8))),
    ("s10", "legumes", 34.70, 38.30, "whip", *acc(
        lab("s10", "a", "MÊMES CALORIES", "left: 130px; top: 250px; font-size: 100px;", 34.92),
        lab("s10", "b", "MÊME SOMMEIL", "left: 130px; top: 410px; font-size: 100px;", 36.20, white=True),
        lab("s10", "c", "MÊME ACTIVITÉ", "left: 130px; top: 570px; font-size: 100px;", 37.34))),
    ("s11", "synth", 38.30, 40.90, "zoom", *acc(
        tag("s11", "a", "QUAND ILS MANGEAIENT TARD", f"{C} top: 250px; font-size: 62px; color: #fff;", 38.45),
        lab("s11", "f", "LA FAIM MONTAIT", "left: 140px; top: 420px; font-size: 84px;", 40.05))),
    ("s12", "ragout2", 40.90, 42.60, "flash", *acc(
        tag("s12", "a", "ET ILS BRÛLAIENT", f"{C} top: 250px; font-size: 80px; color: #fff;", 41.11),
        lab("s12", "m", "MOINS DE CALORIES", "left: 110px; top: 420px; font-size: 70px;", 41.81, white=True))),
    ("s13", "nuit", 42.60, 45.50, "whip", *acc(
        lab("s13", "a", "PETITE ÉTUDE", "left: 190px; top: 250px; font-size: 110px;", 42.78),
        big("s13", "n", "16", f"{C} top: 400px; font-size: 400px; color: #9B6BFF; {SH}", 44.46),
        tag("s13", "t", "PERSONNES", f"{C} top: 760px; font-size: 90px; color: #fff;", 44.70))),
    ("s14", "sablier", 45.50, 49.10, "zoom", *acc(
        tag("s14", "a", "L'HEURE", f"{C} top: 250px; font-size: 100px; color: #fff;", 46.09),
        lab("s14", "n", "NE DÉCIDE PAS", "left: 190px; top: 400px; font-size: 100px;", 46.46),
        tag("s14", "t", "LE TOTAL DE TA JOURNÉE", f"{C} top: 570px; font-size: 64px; color: #fff;", 47.51),
        lab("s14", "o", "OUI", "left: 400px; top: 690px; font-size: 140px;", 48.64, white=True))),
    ("s15", "assiette", 49.10, 53.20, "flash", *acc(
        tag("s15", "a", "LE SOIR", f"{C} top: 250px; font-size: 100px; color: #fff;", 49.59),
        lab("s15", "f", "LA FAIM PEUT MONTER", "left: 70px; top: 400px; font-size: 80px;", 50.39),
        lab("s15", "g", "ATTENTION AUX GRIGNOTAGES", "left: 40px; top: 560px; font-size: 56px;", 51.72, white=True))),
    ("s16", "ruelle", 53.20, 56.40, "whip", *acc(
        ('<div class="ic2" id="s16-ic"><svg viewBox="0 0 140 140"><path d="M14 120 C 20 70, 50 44, 104 44 M84 18 L 122 44 L 84 72" fill="none" stroke="#141414" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" /></svg></div>',
         "#s16-ic { position: absolute; left: 70px; top: 250px; width: 170px; height: 170px; border-radius: 50%; background: #fff; box-shadow: 0 14px 30px rgba(0,0,0,.4); }"
         "#s16-ic svg { position: absolute; left: 25px; top: 25px; width: 120px; height: 120px; overflow: visible; }",
         'tl.fromTo("#s16-ic",{scale:0,rotation:-40},{scale:1,rotation:0,duration:.35,ease:"back.out(2.4)"},at(53.46));'),
        lab("s16", "p", "ENVOIE", "left: 270px; top: 270px; font-size: 130px;", 53.46),
        tag("s16", "q", "À QUELQU'UN QUI NE MANGE<br>PLUS APRÈS 20 H", f"{C} top: 470px; font-size: 64px; color: #fff; {ML}", 54.27))),
    ("s17", "fin", 56.40, D, "zoom", *acc(
        ('<div id="s17-end"><img id="s17-logo" src="assets/brand/icon-512.png" alt="CaliBodi" /><div class="big" id="s17-name">CaliBodi</div>'
         '<div class="lab" id="s17-url">calibodi.com</div><div class="tag" id="s17-st">Play Store · App Store</div></div>',
         "#s17-end { position: absolute; inset: 0; }"
         "#s17-logo { position: absolute; left: 400px; top: 330px; width: 280px; height: 280px; border-radius: 62px; box-shadow: 0 20px 50px rgba(0,0,0,.5); }"
         "#s17-name { left: 0; width: 1080px; top: 650px; text-align: center; font-size: 150px; color: #fff; text-shadow: 0 16px 50px rgba(0,0,0,.7); }"
         "#s17-url { left: 230px; top: 840px; font-size: 100px; }"
         "#s17-st { left: 0; width: 1080px; top: 990px; text-align: center; font-size: 56px; color: #fff; }",
         'tl.fromTo("#s17-logo",{scale:0,rotation:-40},{scale:1,rotation:0,duration:.45,ease:"back.out(2.6)"},at(56.55));'
         'tl.fromTo("#s17-name",{scale:2.4,opacity:0},{scale:1,opacity:1,duration:.26,ease:"power4.out"},at(56.99));'
         'tl.fromTo("#s17-url",{scale:2.4,opacity:0,rotation:-6},{scale:1,opacity:1,rotation:-3,duration:.24,ease:"power4.out"},at(57.80));'
         'tl.fromTo("#s17-st",{y:40,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(58.3));'))),
]
PUNCH = [(1.06, 1.08), (2.75, 1.06), (4.51, 1.05), (6.12, 1.07), (7.24, 1.06), (8.44, 1.08), (11.73, 1.05), (14.88, 1.07),
         (17.51, 1.06), (20.00, 1.06), (21.21, 1.08), (24.93, 1.07), (29.55, 1.06), (31.55, 1.06), (32.60, 1.09), (35.00, 1.05),
         (40.05, 1.07), (41.81, 1.06), (44.46, 1.08), (46.46, 1.06), (50.39, 1.06), (53.46, 1.06), (56.99, 1.05), (57.80, 1.06)]
SHAKE = [1.06, 6.12, 40.05]
POSES = [(0.18, "curieux"), (2.5, "non"), (4.3, "pointe"), (5.5, "choc"), (7.24, "un"), (8.5, "explique"), (11.7, "sceptique"),
         (16.3, "pouce"), (20.0, "deux"), (21.3, "explique"), (28.3, "sceptique"), (31.55, "trois"), (32.9, "explique"),
         (38.4, "curieux"), (40.1, "choc"), (42.8, "sceptique"), (45.9, "pointe"), (48.7, "pouce"), (49.4, "nutrition"),
         (53.4, "pointe"), (56.6, "app"), (58.3, "pouce")]
KW = {"après", "20", "maigrir", "preuves", "surprendre", "139", "obésité", "12", "mois", "calories", "résultat", "significative",
      "116", "surpoids", "semaines", "midi", "repas", "16", "laboratoire", "sommeil", "activité", "tard", "faim", "montait",
      "brûlaient", "heure", "total", "journée", "grignotages", "envoie", "calibodi", "calibodicom"}
CHAPTERS = [0.0, 7.24, 20.0, 31.55]
