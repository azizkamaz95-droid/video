# Shot list of « Petit-déjeuner : on t'a menti », read by build_v4.py (exec'd after its defaults). Global times in seconds.
# Footage: food, objects, places, hands and men seen from behind only (no women, no faces).
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
                f'<g class="ih" id="{sid}-h{i}" opacity="0">{shape("#FFC93C")}</g></g>' for i in range(n))
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
    ("s1", "crepes", 0.00, 3.55, None, *acc(
        lab("s1", "p", "PETIT-DÉJ", "left: 70px; top: 300px; font-size: 150px;", 0.34),
        tag("s1", "q", "LE REPAS LE PLUS<br>IMPORTANT ?", f"{C} top: 520px; font-size: 92px; color: #fff; {ML}", 1.57))),
    ("s2", "reveil", 3.55, 5.60, "flash", *acc(
        big("s2", "n", "NON.", f"{C} top: 260px; font-size: 300px; color: #FFC93C; {SH}", 3.71),
        lab("s2", "t", "3 PREUVES", "left: 290px; top: 620px; font-size: 100px;", 4.67))),
    ("s3", "eclair", 5.60, 8.95, "zoom", *acc(
        tag("s3", "l", "N°3", "left: 120px; top: 360px; font-size: 150px; color: #fff;", 5.79),
        big("s3", "q", "?", f"left: 600px; top: 180px; font-size: 520px; color: #FFC93C; {SH}", 6.51, out=7.45),
        lab("s3", "b", "RESTE JUSQU'AU BOUT", "left: 90px; top: 700px; font-size: 76px;", 7.56))),
    ("s4", "docs", 8.95, 13.45, "whip", *acc(
        lab("s4", "f", "FAIT N°1", "left: 70px; top: 230px; font-size: 120px;", 9.08, out=10.25),
        big("s4", "n", "309", f"{C} top: 300px; font-size: 300px; color: #FFC93C; {SH}", 11.25),
        tag("s4", "a", "ADULTES", f"{C} top: 590px; font-size: 90px; letter-spacing: .03em; color: #fff;", 11.83),
        lab("s4", "w", "16 SEMAINES", "left: 230px; top: 730px; font-size: 100px;", 12.48),
        src("s4", "Dhurandhar et al., American Journal of Clinical Nutrition, 2014", 9.3))),
    ("s5", "oeuf", 13.45, 16.75, "zoom", *acc(
        lab("s5", "a", "GROUPE 1 : PETIT-DÉJ", "left: 60px; top: 260px; font-size: 76px;", 13.66),
        lab("s5", "b", "GROUPE 2 : RIEN", "left: 60px; top: 400px; font-size: 76px;", 15.76, white=True))),
    ("s6", "balance", 16.75, 20.05, "flash", *acc(
        tag("s6", "r", "RÉSULTAT :", f"{C} top: 250px; font-size: 100px; color: #fff;", 16.95),
        lab("s6", "z", "AUCUNE DIFFÉRENCE", "left: 90px; top: 400px; font-size: 72px;", 17.93),
        tag("s6", "p", "SUR LE POIDS", f"{C} top: 560px; font-size: 84px; color: #FFC93C;", 19.27))),
    ("s7", "archives", 20.05, 22.80, "whip", *acc(
        lab("s7", "f", "FAIT N°2", "left: 70px; top: 230px; font-size: 120px;", 20.27, out=21.15),
        big("s7", "n", "13 ÉTUDES", f"{C} top: 300px; font-size: 170px; color: #FFC93C; {SH}", 21.20),
        tag("s7", "t", "RASSEMBLÉES", f"{C} top: 500px; font-size: 80px; letter-spacing: .04em; color: #fff;", 22.03),
        src("s7", "Sievert et al., BMJ, 2019", 20.5))),
    ("s8", "pate", 22.80, 26.95, "zoom", *acc(
        tag("s8", "a", "AVEC PETIT-DÉJ :", f"{C} top: 250px; font-size: 90px; color: #fff;", 23.53),
        big("s8", "n", "+260", f"{C} top: 370px; font-size: 280px; color: #FFC93C; {SH}", 24.97),
        lab("s8", "k", "KCAL PAR JOUR", "left: 210px; top: 660px; font-size: 90px;", 25.61))),
    ("s9", "expresso", 26.95, 28.85, "whip", *acc(
        lab("s9", "m", "PAS PLUS MINCES", "left: 120px; top: 280px; font-size: 96px;", 27.38))),
    ("s10", "orage", 28.85, 31.60, "flash", *acc(
        tag("s10", "k", "FAIT N°", f"{C} top: 250px; font-size: 110px; color: #fff;", 28.98),
        big("s10", "n", "3", f"{C} top: 330px; font-size: 640px; color: #FFC93C; {SH}", 29.46))),
    ("s11", "ville", 31.60, 35.25, "zoom", *acc(
        tag("s11", "p", "PLUS DE", f"{C} top: 250px; font-size: 90px; color: #fff;", 32.80),
        big("s11", "n", "6 000", f"{C} top: 350px; font-size: 260px; color: #FFC93C; {SH}", 33.32),
        tag("s11", "a", "ADULTES", f"{C} top: 620px; font-size: 90px; letter-spacing: .03em; color: #fff;", 33.66),
        lab("s11", "y", "19 ANS DE SUIVI", "left: 170px; top: 760px; font-size: 96px;", 34.44),
        src("s11", "Rong et al., Journal of the American College of Cardiology, 2019", 31.9))),
    ("s12", "moniteur", 35.25, 38.30, "whip", *acc(
        lab("s12", "j", "JAMAIS DE PETIT-DÉJ", "left: 90px; top: 250px; font-size: 74px;", 36.08),
        big("s12", "n", "+87 %", f"{C} top: 400px; font-size: 280px; color: #FFC93C; {SH}", 37.33))),
    ("s13", "ecg", 38.30, 41.05, "flash", *acc(
        tag("s13", "r", "DE RISQUE DE MOURIR", f"{C} top: 330px; font-size: 80px; color: #fff;", 38.41),
        lab("s13", "c", "MALADIE DU CŒUR", "left: 110px; top: 480px; font-size: 80px;", 39.90))),
    ("s14", "montre", 41.05, 43.05, "zoom", *acc(
        tag("s14", "q", "CHOQUANT ?", f"{C} top: 260px; font-size: 120px; color: #fff;", 41.27),
        lab("s14", "s", "PAS SI VITE.", "left: 190px; top: 420px; font-size: 120px;", 42.15))),
    ("s15", "clope", 43.05, 45.90, "whip", *acc(
        tag("s15", "c", "LES CHERCHEURS<br>LE DISENT :", f"{C} top: 250px; font-size: 84px; color: #fff; {ML}", 43.27),
        lab("s15", "h", "D'AUTRES HABITUDES", "left: 90px; top: 470px; font-size: 72px;", 45.68))),
    ("s16", "burger", 45.90, 47.45, "flash", *acc(
        lab("s16", "m", "MOINS SAINES", "left: 140px; top: 300px; font-size: 110px;", 46.40))),
    ("s17", "tasse", 47.45, 49.35, "zoom", *acc(
        tag("s17", "p", "LE PETIT-DÉJ ?", f"{C} top: 250px; font-size: 100px; color: #fff;", 47.61),
        big("s17", "n", "PAS LA<br>CAUSE.", f"{C} top: 400px; font-size: 200px; color: #FFC93C; {ML} line-height: .9; {SH}", 48.49))),
    ("s18", "livre", 49.35, 54.30, "whip", *acc(
        lab("s18", "a", "ATTENTION", "left: 200px; top: 250px; font-size: 130px;", 49.63, white=True, out=50.7),
        tag("s18", "l", "DES LIENS", f"{C} top: 260px; font-size: 130px; color: #fff;", 50.98),
        lab("s18", "p", "PAS DES PREUVES", "left: 110px; top: 420px; font-size: 88px;", 51.70),
        lab("s18", "c", "ÉTUDES POIDS : COURTES", "left: 70px; top: 580px; font-size: 70px;", 53.63, white=True))),
    ("s19", "gym", 54.30, 57.25, "zoom", *acc(
        tag("s19", "c", "CE QUI COMPTE<br>VRAIMENT :", f"{C} top: 250px; font-size: 90px; color: #fff; {ML}", 54.59),
        lab("s19", "t", "LE TOTAL DE<br>TA JOURNÉE", f"left: 170px; top: 480px; font-size: 110px; {ML} text-align: center;", 55.88))),
    ("s20", "pompes", 57.25, 60.00, "flash", *acc(
        lab("s20", "k", "CALORIES", "left: 80px; top: 280px; font-size: 100px;", 57.41),
        lab("s20", "s", "SOMMEIL", "left: 80px; top: 410px; font-size: 100px;", 58.37, white=True),
        lab("s20", "e", "ENTRAÎNEMENT", "left: 80px; top: 540px; font-size: 100px;", 59.19))),
    ("s21", "cafe", 60.00, 63.55, "whip", *acc(
        tag("s21", "t", "ET TOI ?", f"{C} top: 240px; font-size: 130px; color: #FFC93C;", 60.30),
        tag("s21", "q", "PETIT-DÉJ<br>TOUS LES MATINS ?", f"{C} top: 400px; font-size: 84px; color: #fff; {ML}", 60.81),
        lab("s21", "o", "OUI", "left: 170px; top: 640px; font-size: 140px;", 62.71),
        lab("s21", "x", "NON", "left: 620px; top: 640px; font-size: 140px;", 62.96, white=True))),
    ("s22", "canal", 63.55, 70.35, "zoom", *acc(
        ('<div class="ic2" id="s22-ic"><svg viewBox="0 0 140 140"><path d="M14 120 C 20 70, 50 44, 104 44 M84 18 L 122 44 L 84 72" fill="none" stroke="#141414" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" /></svg></div>',
         "#s22-ic { position: absolute; left: 70px; top: 250px; width: 170px; height: 170px; border-radius: 50%; background: #fff; box-shadow: 0 14px 30px rgba(0,0,0,.4); }"
         "#s22-ic svg { position: absolute; left: 25px; top: 25px; width: 120px; height: 120px; overflow: visible; }",
         'tl.fromTo("#s22-ic",{scale:0,rotation:-40},{scale:1,rotation:0,duration:.35,ease:"back.out(2.4)"},at(63.67));'
         'tl.fromTo("#s22-ic",{opacity:1},{opacity:0,duration:.2,ease:"none",immediateRender:false},at(67.0));'),
        lab("s22", "p", "PARTAGE", "left: 270px; top: 270px; font-size: 120px;", 63.67, out=67.0),
        tag("s22", "q", "À QUELQU'UN QUI<br>NE SAUTE JAMAIS<br>SON PETIT-DÉJ", f"{C} top: 470px; font-size: 70px; color: #fff; {ML}", 64.71, out=67.0),
        lab("s22", "a", "ABONNE-TOI", "left: 70px; top: 260px; font-size: 140px;", 67.30),
        tag("s22", "j", "1 VIDÉO CHAQUE JOUR", f"{C} top: 470px; font-size: 70px; letter-spacing: .04em; color: #fff;", 68.18),
        big("s22", "h", "18H", f"{C} top: 640px; font-size: 300px; color: #FFC93C; {SH}", 69.53))),
    ("s23", "skyline", 70.35, D, "whip", *acc(
        ('<div class="phone" id="s23-p1"><img src="assets/app/nutrition.jpg" alt="écran alimentation CaliBodi" /></div>'
         '<div class="phone" id="s23-p2"><img src="assets/app/sleep.jpg" alt="écran sommeil CaliBodi" /></div>'
         '<div class="phone" id="s23-p3"><img src="assets/app/fitness.jpg" alt="écran entraînements CaliBodi" /></div>'
         '<div id="s23-end"><img id="s23-logo" src="assets/brand/icon-512.png" alt="CaliBodi" /><div class="big" id="s23-name">CaliBodi</div>'
         '<div class="lab" id="s23-url">calibodi.com</div><div class="tag" id="s23-st">Play Store · App Store</div></div>',
         ".phone { position: absolute; top: 300px; width: 320px; height: 640px; padding: 12px; background: #141414; border-radius: 48px; box-shadow: 0 30px 60px rgba(0,0,0,.6); }"
         ".phone img { width: 100%; height: 100%; border-radius: 38px; object-fit: cover; object-position: top; display: block; }"
         "#s23-p1 { left: 40px; rotate: -6deg; } #s23-p2 { left: 380px; top: 270px; } #s23-p3 { left: 720px; rotate: 6deg; }"
         "#s23-end { position: absolute; inset: 0; opacity: 0; }"
         "#s23-logo { position: absolute; left: 400px; top: 250px; width: 280px; height: 280px; border-radius: 62px; box-shadow: 0 20px 50px rgba(0,0,0,.5); }"
         "#s23-name { left: 0; width: 1080px; top: 570px; text-align: center; font-size: 150px; color: #fff; text-shadow: 0 16px 50px rgba(0,0,0,.7); }"
         "#s23-url { left: 230px; top: 760px; font-size: 100px; }"
         "#s23-st { left: 0; width: 1080px; top: 910px; text-align: center; font-size: 56px; color: #fff; }",
         'tl.fromTo("#s23-p1",{y:1300,rotation:-30},{y:0,rotation:0,duration:.45,ease:"back.out(1.4)"},at(71.38));'
         'tl.fromTo("#s23-p2",{y:1300},{y:0,duration:.45,ease:"back.out(1.4)"},at(72.18));'
         'tl.fromTo("#s23-p3",{y:1300,rotation:30},{y:0,rotation:0,duration:.45,ease:"back.out(1.4)"},at(73.00));'
         'tl.fromTo(["#s23-p1","#s23-p2","#s23-p3"],{opacity:1,y:0},{opacity:0,y:-900,duration:.3,ease:"power3.in",immediateRender:false},at(73.65));'
         'tl.fromTo("#s23-end",{opacity:0},{opacity:1,duration:.1,ease:"none"},at(73.87));'
         'tl.fromTo("#s23-logo",{scale:0,rotation:-40},{scale:1,rotation:0,duration:.45,ease:"back.out(2.6)"},at(73.9));'
         'tl.fromTo("#s23-name",{scale:2.4,opacity:0},{scale:1,opacity:1,duration:.26,ease:"power4.out"},at(74.32));'
         'tl.fromTo("#s23-url",{scale:2.4,opacity:0,rotation:-6},{scale:1,opacity:1,rotation:-3,duration:.24,ease:"power4.out"},at(75.20));'
         'tl.fromTo("#s23-st",{y:40,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(75.5));'),)),
]
PUNCH = [(0.34, 1.05), (1.57, 1.05), (3.71, 1.09), (4.67, 1.05), (6.51, 1.06), (9.08, 1.06), (11.25, 1.07), (12.48, 1.05), (15.76, 1.05),
         (17.93, 1.07), (20.27, 1.06), (21.20, 1.07), (24.97, 1.08), (27.38, 1.06), (29.46, 1.10), (33.32, 1.07), (36.08, 1.05),
         (37.33, 1.09), (39.90, 1.06), (42.15, 1.07), (46.40, 1.06), (48.49, 1.08), (51.70, 1.06), (55.88, 1.06),
         (59.19, 1.05), (62.71, 1.05), (67.30, 1.06), (69.53, 1.07), (74.32, 1.05), (75.20, 1.06)]
SHAKE = [3.71, 29.46, 37.33]
POSES = [(0.18, "curieux"), (3.71, "non"), (4.67, "trois"), (5.79, "pointe"), (9.08, "un"), (10.40, "explique"), (13.59, "nutrition"),
         (16.95, "explique"), (17.93, "sceptique"), (20.24, "deux"), (21.45, "explique"), (23.53, "nutrition"), (24.97, "choc"),
         (27.38, "non"), (28.98, "trois"), (30.27, "pointe"), (31.81, "explique"), (37.33, "choc"), (41.27, "curieux"), (42.15, "non"),
         (43.19, "explique"), (46.40, "sceptique"), (48.31, "non"), (49.63, "pointe"), (51.70, "sceptique"), (54.43, "explique"),
         (57.41, "nutrition"), (59.19, "biceps"), (60.30, "curieux"), (62.71, "pouce"), (63.67, "pointe"), (67.30, "pouce"),
         (70.58, "app"), (73.87, "pouce")]
KW = {"petit-déjeuner", "important", "non", "trois", "preuves", "surprendre", "bout", "309", "16", "semaines", "aucune", "différence",
      "13", "260", "calories", "maigrissent", "6", "000", "19", "87", "cœur", "vite", "cause", "liens", "courtes", "total", "journée",
      "oui", "partage", "abonne-toi", "18h", "calibodi", "calibodicom"}
CHAPTERS = [0.0, 9.08, 20.24, 28.98]
