# Shot list of « Assis 8 h par jour », read by build_v4.py (exec'd after its defaults). Global times in seconds.
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
                f'<g class="ih" id="{sid}-h{i}" opacity="0">{shape("#3DE0C0")}</g></g>' for i in range(n))
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
    ("s1", "bureau", 0.00, 3.60, None, *acc(
        lab("s1", "a", "ASSIS", "left: 70px; top: 250px; font-size: 150px;", 0.67),
        big("s1", "n", "8 H", f"{C} top: 420px; font-size: 300px; color: #3DE0C0; {SH}", 0.80),
        tag("s1", "p", "PAR JOUR", f"{C} top: 730px; font-size: 80px; letter-spacing: .05em; color: #fff;", 1.46),
        lab("s1", "d", "DANGER ?", "left: 230px; top: 840px; font-size: 100px;", 2.83, white=True))),
    ("s2", "horloge", 3.60, 5.30, "zoom", *acc(
        lab("s2", "b", "BONNE NOUVELLE", "left: 70px; top: 300px; font-size: 100px;", 3.63))),
    ("s3", "spirale", 5.30, 10.30, "flash", *acc(
        lab("s3", "p", "3 PREUVES", "left: 250px; top: 230px; font-size: 120px;", 5.80),
        big("s3", "q", "?", f"left: 600px; top: 380px; font-size: 520px; color: #3DE0C0; {SH}", 7.48, out=8.5),
        lab("s3", "b", "RESTE JUSQU'AU BOUT", "left: 90px; top: 720px; font-size: 76px;", 8.64, white=True))),
    ("s4", "clavier", 10.30, 14.10, "whip", *acc(
        lab("s4", "f", "FAIT N°1", "left: 70px; top: 230px; font-size: 120px;", 10.29, out=11.4),
        big("s4", "n", "47", f"{C} top: 300px; font-size: 330px; color: #3DE0C0; {SH}", 12.78),
        tag("s4", "t", "ÉTUDES REGROUPÉES", f"{C} top: 640px; font-size: 74px; letter-spacing: .03em; color: #fff;", 13.28),
        src("s4", "Biswas et al., Annals of Internal Medicine, 2015", 10.6))),
    ("s5", "dos", 14.10, 20.50, "zoom", *acc(
        big("s5", "n", "+24 %", f"{C} top: 250px; font-size: 280px; color: #3DE0C0; {SH}", 16.16),
        tag("s5", "t", "DE RISQUE DE MOURIR", f"{C} top: 570px; font-size: 76px; color: #fff;", 17.07),
        lab("s5", "m", "MÊME SI TU FAIS DU SPORT", "left: 50px; top: 700px; font-size: 62px;", 18.81, white=True))),
    ("s6", "pieds", 20.50, 25.35, "flash", *acc(
        lab("s6", "f", "FAIT N°2", "left: 70px; top: 230px; font-size: 120px;", 20.57, out=21.7),
        big("s6", "n", "2 MIN", f"{C} top: 300px; font-size: 270px; color: #3DE0C0; {SH}", 23.55),
        tag("s6", "t", "TOUTES LES 20 MIN", f"{C} top: 600px; font-size: 76px; color: #fff;", 24.35),
        src("s6", "Dunstan et al., Diabetes Care, 2012", 20.9))),
    ("s7", "bureau2", 25.35, 29.15, "zoom", *acc(
        tag("s7", "r", "RÉSULTAT :", f"{C} top: 250px; font-size: 100px; color: #fff;", 25.39),
        lab("s7", "s", "MOINS DE SUCRE", "left: 100px; top: 400px; font-size: 84px;", 26.68),
        lab("s7", "i", "MOINS D'INSULINE", "left: 100px; top: 540px; font-size: 84px;", 27.24, white=True))),
    ("s8", "chaises", 29.15, 33.25, "whip", *acc(
        lab("s8", "b", "PETIT BÉMOL", "left: 160px; top: 250px; font-size: 110px;", 29.24),
        big("s8", "n", "19", f"{C} top: 420px; font-size: 300px; color: #3DE0C0; {SH}", 31.73),
        tag("s8", "p", "PERSONNES", f"{C} top: 720px; font-size: 84px; letter-spacing: .04em; color: #fff;", 32.21))),
    ("s9", "foule", 33.25, 38.35, "flash", *acc(
        tag("s9", "k", "FAIT N°", f"{C} top: 250px; font-size: 110px; color: #fff;", 33.25, out=36.1),
        big("s9", "n", "3", f"{C} top: 330px; font-size: 640px; color: #3DE0C0; {SH}", 33.81, out=36.1),
        big("s9", "m", "1 MILLION", f"{C} top: 300px; font-size: 190px; color: #3DE0C0; {SH}", 36.38),
        tag("s9", "t", "DE PERSONNES SUIVIES", f"{C} top: 530px; font-size: 68px; color: #fff;", 36.78),
        src("s9", "Ekelund et al., The Lancet, 2016", 33.8))),
    ("s10", "velo", 38.35, 43.75, "zoom", *acc(
        big("s10", "n", "60–75 MIN", f"{C} top: 290px; font-size: 168px; color: #3DE0C0; {SH}", 38.90),
        tag("s10", "t", "D'ACTIVITÉ PAR JOUR", f"{C} top: 520px; font-size: 70px; color: #fff;", 40.13),
        lab("s10", "a", "RISQUE ANNULÉ", "left: 200px; top: 650px; font-size: 90px;", 41.61))),
    ("s11", "meca", 43.75, 45.65, "flash", *acc(
        tag("s11", "q", "CHOQUANT ?", f"{C} top: 260px; font-size: 120px; color: #fff;", 43.84),
        lab("s11", "s", "PAS SI VITE.", "left: 220px; top: 420px; font-size: 120px;", 44.64))),
    ("s12", "salon", 45.65, 50.35, "zoom", *acc(
        tag("s12", "a", "DEVANT LA TÉLÉ", f"{C} top: 250px; font-size: 90px; color: #fff;", 45.76),
        big("s12", "n", "+5 H", f"{C} top: 380px; font-size: 250px; color: #3DE0C0; {SH}", 46.64),
        lab("s12", "r", "LE RISQUE RESTE", "left: 150px; top: 690px; font-size: 84px;", 48.97))),
    ("s13", "gratte", 50.35, 54.75, "whip", *acc(
        tag("s13", "o", "ÉTUDES D'OBSERVATION", f"{C} top: 250px; font-size: 70px; color: #fff;", 50.99),
        lab("s13", "l", "DES LIENS", "left: 200px; top: 400px; font-size: 110px;", 52.58),
        lab("s13", "p", "PAS DES PREUVES", "left: 110px; top: 560px; font-size: 94px;", 53.54, white=True))),
    ("s14", "escalier", 54.75, 57.35, "flash", *acc(
        tag("s14", "c", "CE QUI COMPTE :", f"{C} top: 250px; font-size: 90px; color: #fff;", 54.91),
        big("s14", "b", "BOUGER", f"{C} top: 380px; font-size: 200px; color: #3DE0C0; {SH}", 56.03),
        tag("s14", "j", "TOUS LES JOURS", f"{C} top: 620px; font-size: 80px; color: #fff;", 56.59))),
    ("s15", "velo2", 57.35, 60.95, "zoom", *acc(
        lab("s15", "m", "MARCHE RAPIDE", "left: 90px; top: 250px; font-size: 100px;", 57.40),
        lab("s15", "vl", "VÉLO", "left: 400px; top: 400px; font-size: 130px;", 58.28, white=True),
        lab("s15", "s", "PAS BESOIN DE SALLE", "left: 70px; top: 600px; font-size: 72px;", 59.57))),
    ("s16", "plage", 60.95, 65.35, "whip", *acc(
        tag("s16", "t", "ET TOI ?", f"{C} top: 240px; font-size: 130px; color: #3DE0C0;", 61.03),
        tag("s16", "q", "ASSIS COMBIEN<br>D'HEURES PAR JOUR ?", f"{C} top: 400px; font-size: 76px; color: #fff; {ML}", 61.99),
        lab("s16", "c", "COMMENTE", "left: 260px; top: 650px; font-size: 110px;", 64.31))),
    ("s17", "fin", 65.35, 70.65, "flash", *acc(
        ('<div class="ic2" id="s17-ic"><svg viewBox="0 0 140 140"><path d="M14 120 C 20 70, 50 44, 104 44 M84 18 L 122 44 L 84 72" fill="none" stroke="#141414" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" /></svg></div>',
         "#s17-ic { position: absolute; left: 70px; top: 250px; width: 170px; height: 170px; border-radius: 50%; background: #fff; box-shadow: 0 14px 30px rgba(0,0,0,.4); }"
         "#s17-ic svg { position: absolute; left: 25px; top: 25px; width: 120px; height: 120px; overflow: visible; }",
         'tl.fromTo("#s17-ic",{scale:0,rotation:-40},{scale:1,rotation:0,duration:.35,ease:"back.out(2.4)"},at(65.43));'
         'tl.fromTo("#s17-ic",{opacity:1},{opacity:0,duration:.2,ease:"none",immediateRender:false},at(68.4));'),
        lab("s17", "p", "PARTAGE", "left: 270px; top: 270px; font-size: 120px;", 65.43, out=68.4),
        tag("s17", "q", "À UN COLLÈGUE<br>DE BUREAU", f"{C} top: 470px; font-size: 76px; color: #fff; {ML}", 66.64, out=68.4),
        lab("s17", "a", "ABONNE-TOI", "left: 70px; top: 260px; font-size: 140px;", 68.66),
        tag("s17", "j", "1 VIDÉO CHAQUE JOUR", f"{C} top: 470px; font-size: 70px; letter-spacing: .04em; color: #fff;", 69.61))),
    ("s18", "coucher", 70.65, D, "zoom", *acc(
        ('<div class="phone" id="s18-p1"><img src="assets/app/dashboard.jpg" alt="tableau de bord CaliBodi" /></div>'
         '<div class="phone" id="s18-p2"><img src="assets/app/fitness.jpg" alt="écran entraînements CaliBodi" /></div>'
         '<div class="phone" id="s18-p3"><img src="assets/app/sleep.jpg" alt="écran sommeil CaliBodi" /></div>'
         '<div id="s18-end"><img id="s18-logo" src="assets/brand/icon-512.png" alt="CaliBodi" /><div class="big" id="s18-name">CaliBodi</div>'
         '<div class="lab" id="s18-url">calibodi.com</div><div class="tag" id="s18-st">Play Store · App Store</div></div>',
         ".phone { position: absolute; top: 300px; width: 320px; height: 640px; padding: 12px; background: #141414; border-radius: 48px; box-shadow: 0 30px 60px rgba(0,0,0,.6); }"
         ".phone img { width: 100%; height: 100%; border-radius: 38px; object-fit: cover; object-position: top; display: block; }"
         "#s18-p1 { left: 40px; rotate: -6deg; } #s18-p2 { left: 380px; top: 270px; } #s18-p3 { left: 720px; rotate: 6deg; }"
         "#s18-end { position: absolute; inset: 0; opacity: 0; }"
         "#s18-logo { position: absolute; left: 400px; top: 250px; width: 280px; height: 280px; border-radius: 62px; box-shadow: 0 20px 50px rgba(0,0,0,.5); }"
         "#s18-name { left: 0; width: 1080px; top: 570px; text-align: center; font-size: 150px; color: #fff; text-shadow: 0 16px 50px rgba(0,0,0,.7); }"
         "#s18-url { left: 230px; top: 760px; font-size: 100px; }"
         "#s18-st { left: 0; width: 1080px; top: 910px; text-align: center; font-size: 56px; color: #fff; }",
         'tl.fromTo("#s18-p1",{y:1300,rotation:-30},{y:0,rotation:0,duration:.45,ease:"back.out(1.4)"},at(71.56));'
         'tl.fromTo("#s18-p2",{y:1300},{y:0,duration:.45,ease:"back.out(1.4)"},at(72.68));'
         'tl.fromTo("#s18-p3",{y:1300,rotation:30},{y:0,rotation:0,duration:.45,ease:"back.out(1.4)"},at(73.47));'
         'tl.fromTo(["#s18-p1","#s18-p2","#s18-p3"],{opacity:1,y:0},{opacity:0,y:-900,duration:.3,ease:"power3.in",immediateRender:false},at(74.20));'
         'tl.fromTo("#s18-end",{opacity:0},{opacity:1,duration:.1,ease:"none"},at(74.45));'
         'tl.fromTo("#s18-logo",{scale:0,rotation:-40},{scale:1,rotation:0,duration:.45,ease:"back.out(2.6)"},at(74.50));'
         'tl.fromTo("#s18-name",{scale:2.4,opacity:0},{scale:1,opacity:1,duration:.26,ease:"power4.out"},at(74.80));'
         'tl.fromTo("#s18-url",{scale:2.4,opacity:0,rotation:-6},{scale:1,opacity:1,rotation:-3,duration:.24,ease:"power4.out"},at(75.61));'
         'tl.fromTo("#s18-st",{y:40,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(76.0));'),)),
]
PUNCH = [(0.80, 1.07), (2.83, 1.06), (4.19, 1.05), (5.80, 1.05), (7.48, 1.06), (10.29, 1.06), (12.78, 1.07), (16.16, 1.08),
         (18.81, 1.05), (20.57, 1.06), (23.55, 1.07), (26.68, 1.05), (31.73, 1.07), (33.81, 1.10), (36.38, 1.07), (38.90, 1.07),
         (41.61, 1.06), (43.84, 1.07), (44.64, 1.06), (46.64, 1.07), (52.58, 1.06), (56.03, 1.07), (58.28, 1.05), (61.03, 1.05),
         (65.43, 1.05), (68.66, 1.06), (74.80, 1.05), (75.61, 1.06)]
SHAKE = [2.83, 33.81, 43.84]
POSES = [(0.18, "curieux"), (2.83, "choc"), (3.63, "pouce"), (5.40, "trois"), (6.68, "pointe"), (10.29, "un"), (11.36, "explique"),
         (14.15, "sceptique"), (18.81, "choc"), (20.57, "deux"), (21.86, "explique"), (25.39, "pouce"), (29.24, "sceptique"),
         (33.25, "trois"), (34.53, "pointe"), (36.06, "explique"), (38.38, "biceps"), (43.84, "choc"), (44.64, "non"),
         (45.76, "sceptique"), (50.43, "explique"), (54.83, "pointe"), (57.33, "biceps"), (61.03, "curieux"), (65.43, "pointe"),
         (68.58, "pouce"), (70.82, "app"), (74.43, "pouce")]
KW = {"assis", "huit", "danger", "bonne", "nouvelle", "trois", "preuves", "surprendre", "bout", "47", "24", "sport", "2", "20",
      "sucre", "insuline", "19", "million", "60", "75", "annuler", "choquant", "vite", "télé", "5", "bouger", "vélo", "salle",
      "commentaire", "partage", "abonne-toi", "calibodi", "calibodicom"}
CHAPTERS = [0.0, 10.29, 20.57, 33.25]
