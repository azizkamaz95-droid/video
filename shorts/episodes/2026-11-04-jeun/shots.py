# Shot list of « Sport à jeun », read by build_v4.py (exec'd after its defaults). Global times in seconds.
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
ML = "white-space: normal; line-height: 1;"
SHOTS = [
    ("s1", "reveil", 0.00, 3.60, None, *acc(
        lab("s1", "a", "SPORT À JEUN", "left: 60px; top: 250px; font-size: 118px;", 0.58),
        big("s1", "n", "?", f"{C} top: 430px; font-size: 520px; color: #35C7FF; {SH}", 1.35),
        lab("s1", "d", "PAS MIEUX", "left: 250px; top: 880px; font-size: 120px;", 2.83, white=True))),
    ("s2", "ciel", 3.60, 7.40, "zoom", *acc(
        lab("s2", "p", "3 PREUVES", "left: 200px; top: 250px; font-size: 130px;", 4.51),
        lab("s2", "l", "LA DERNIÈRE ?", "left: 120px; top: 440px; font-size: 100px;", 5.80, white=True),
        big("s2", "q", "!", f"left: 700px; top: 560px; font-size: 460px; color: #35C7FF; {SH}", 6.36))),
    ("s3", "plage2", 7.40, 11.70, "flash", *acc(
        lab("s3", "f", "PREUVE 1", "left: 70px; top: 230px; font-size: 120px;", 7.56, out=8.8),
        big("s3", "n", "20", f"{C} top: 300px; font-size: 360px; color: #35C7FF; {SH}", 8.93),
        lab("s3", "t", "JEUNES FEMMES · 4 SEMAINES", "left: 60px; top: 690px; font-size: 56px;", 9.33, white=True),
        src("s3", "Schoenfeld et al., J. Int. Soc. Sports Nutr., 2014", 7.9))),
    ("s4", "plat", 11.70, 16.30, "whip", *acc(
        lab("s4", "a", "10 À JEUN", "left: 90px; top: 250px; font-size: 118px;", 12.0),
        lab("s4", "b", "10 APRÈS MANGER", "left: 90px; top: 410px; font-size: 100px;", 13.19, white=True),
        tag("s4", "r", "MÊME RÉGIME", f"{C} top: 600px; font-size: 90px; color: #fff;", 14.95))),
    ("s5", "lac", 16.30, 19.00, "zoom", *acc(
        tag("s5", "r", "RÉSULTAT :", f"{C} top: 250px; font-size: 100px; color: #fff;", 16.56),
        big("s5", "e", "=", f"{C} top: 380px; font-size: 420px; color: #35C7FF; {SH}", 17.60),
        lab("s5", "g", "MÊME PERTE DE GRAS", "left: 70px; top: 800px; font-size: 80px;", 18.30))),
    ("s6", "livres", 19.00, 24.30, "flash", *acc(
        lab("s6", "f", "PREUVE 2", "left: 70px; top: 230px; font-size: 120px;", 19.29, out=20.5),
        big("s6", "a", "5", f"left: 120px; top: 300px; font-size: 330px; color: #35C7FF; {SH}", 21.62),
        tag("s6", "b", "ÉTUDES", f"left: 380px; top: 420px; font-size: 100px; color: #fff;", 21.88),
        big("s6", "c", "96", f"left: 120px; top: 640px; font-size: 330px; color: #35C7FF; {SH}", 22.74),
        tag("s6", "d", "PERSONNES", f"left: 440px; top: 780px; font-size: 90px; color: #fff;", 23.39),
        src("s6", "Hackett et Hagstrom, J. Funct. Morphol. Kinesiol., 2017", 19.6))),
    ("s7", "micro", 24.30, 26.30, "zoom", *acc(
        tag("s7", "a", "L'ÉCART SUR LE GRAS", f"{C} top: 250px; font-size: 74px; color: #fff;", 24.46),
        lab("s7", "m", "MINUSCULE", "left: 170px; top: 400px; font-size: 130px;", 25.31))),
    ("s8", "neon", 26.30, 30.50, "whip", *acc(
        lab("s8", "f", "PREUVE 3", "left: 70px; top: 230px; font-size: 120px;", 26.36, out=27.5),
        lab("s8", "j", "À JEUN", "left: 70px; top: 250px; font-size: 130px;", 28.12),
        tag("s8", "g", "PLUS DE GRAS BRÛLÉ", f"{C} top: 440px; font-size: 76px; color: #fff;", 28.68),
        tag("s8", "s", "PENDANT LA SÉANCE", f"{C} top: 560px; font-size: 76px; color: #fff;", 29.24))),
    ("s9", "cafe", 30.50, 34.80, "flash", *acc(
        big("s9", "q", "COMBIEN ?", f"{C} top: 300px; font-size: 200px; color: #fff; {SH}", 30.84, out=31.9),
        big("s9", "n", "3 G", f"{C} top: 280px; font-size: 520px; color: #35C7FF; {SH}", 32.12),
        tag("s9", "t", "MOINS QU'UNE<br>CUILLÈRE À CAFÉ", f"{C} top: 780px; font-size: 78px; color: #fff; {ML}", 33.17),
        src("s9", "Vieira et al., British Journal of Nutrition, 2016", 30.6))),
    ("s10", "plage", 34.80, 37.30, "zoom", *acc(
        tag("s10", "a", "À LA FIN", f"{C} top: 250px; font-size: 90px; color: #fff;", 35.40),
        lab("s10", "r", "RIEN NE CHANGE", "left: 120px; top: 400px; font-size: 100px;", 36.16))),
    ("s11", "aube", 37.30, 42.50, "whip", *acc(
        lab("s11", "j", "TA JOURNÉE ENTIÈRE", "left: 60px; top: 240px; font-size: 80px;", 38.62),
        lab("s11", "c", "CALORIES", "left: 90px; top: 420px; font-size: 100px;", 39.98, white=True),
        lab("s11", "s", "SOMMEIL", "left: 90px; top: 580px; font-size: 100px;", 41.02),
        lab("s11", "e", "ENTRAÎNEMENT", "left: 90px; top: 740px; font-size: 100px;", 41.60, white=True))),
    ("s12", "fraises", 42.50, 45.30, "flash", *acc(
        tag("s12", "a", "À JEUN OU NON", f"{C} top: 250px; font-size: 90px; color: #fff;", 42.64),
        lab("s12", "c", "TON CHOIX", "left: 220px; top: 420px; font-size: 130px;", 43.74))),
    ("s13", "alarme", 45.30, 49.20, "whip", *acc(
        tag("s13", "t", "ET TOI ?", f"{C} top: 240px; font-size: 130px; color: #35C7FF;", 45.52),
        tag("s13", "q", "À JEUN OU<br>APRÈS MANGER ?", f"{C} top: 400px; font-size: 80px; color: #fff; {ML}", 45.99),
        lab("s13", "c", "COMMENTE", "left: 260px; top: 680px; font-size: 110px;", 48.23))),
    ("s14", "plat2", 49.20, 51.95, "zoom", *acc(
        ('<div class="ic2" id="s14-ic"><svg viewBox="0 0 140 140"><path d="M14 120 C 20 70, 50 44, 104 44 M84 18 L 122 44 L 84 72" fill="none" stroke="#141414" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" /></svg></div>',
         "#s14-ic { position: absolute; left: 70px; top: 250px; width: 170px; height: 170px; border-radius: 50%; background: #fff; box-shadow: 0 14px 30px rgba(0,0,0,.4); }"
         "#s14-ic svg { position: absolute; left: 25px; top: 25px; width: 120px; height: 120px; overflow: visible; }",
         'tl.fromTo("#s14-ic",{scale:0,rotation:-40},{scale:1,rotation:0,duration:.35,ease:"back.out(2.4)"},at(49.35));'),
        lab("s14", "p", "PARTAGE", "left: 270px; top: 270px; font-size: 120px;", 49.35),
        tag("s14", "q", "À UN AMI QUI S'ENTRAÎNE<br>À JEUN", f"{C} top: 470px; font-size: 64px; color: #fff; {ML}", 50.51))),
    ("s15", "lac2", 51.95, 54.30, "flash", *acc(
        lab("s15", "a", "ABONNE-TOI", "left: 70px; top: 260px; font-size: 140px;", 52.17),
        lab("s15", "j", "1 VIDÉO CHAQUE JOUR", "left: 80px; top: 480px; font-size: 62px;", 53.22, white=True))),
    ("s16", "fin", 54.30, D, "zoom", *acc(
        ('<div class="phone" id="s16-p1"><img src="assets/app/dashboard.jpg" alt="tableau de bord CaliBodi" /></div>'
         '<div class="phone" id="s16-p2"><img src="assets/app/fitness.jpg" alt="écran entraînements CaliBodi" /></div>'
         '<div class="phone" id="s16-p3"><img src="assets/app/sleep.jpg" alt="écran sommeil CaliBodi" /></div>'
         '<div id="s16-end"><img id="s16-logo" src="assets/brand/icon-512.png" alt="CaliBodi" /><div class="big" id="s16-name">CaliBodi</div>'
         '<div class="lab" id="s16-url">calibodi.com</div><div class="tag" id="s16-st">Play Store · App Store</div></div>',
         ".phone { position: absolute; top: 300px; width: 320px; height: 640px; padding: 12px; background: #141414; border-radius: 48px; box-shadow: 0 30px 60px rgba(0,0,0,.6); }"
         ".phone img { width: 100%; height: 100%; border-radius: 38px; object-fit: cover; object-position: top; display: block; }"
         "#s16-p1 { left: 40px; rotate: -6deg; } #s16-p2 { left: 380px; top: 270px; } #s16-p3 { left: 720px; rotate: 6deg; }"
         "#s16-end { position: absolute; inset: 0; opacity: 0; }"
         "#s16-logo { position: absolute; left: 400px; top: 250px; width: 280px; height: 280px; border-radius: 62px; box-shadow: 0 20px 50px rgba(0,0,0,.5); }"
         "#s16-name { left: 0; width: 1080px; top: 570px; text-align: center; font-size: 150px; color: #fff; text-shadow: 0 16px 50px rgba(0,0,0,.7); }"
         "#s16-url { left: 230px; top: 760px; font-size: 100px; }"
         "#s16-st { left: 0; width: 1080px; top: 910px; text-align: center; font-size: 56px; color: #fff; }",
         'tl.fromTo("#s16-p1",{y:1300,rotation:-30},{y:0,rotation:0,duration:.45,ease:"back.out(1.4)"},at(54.95));'
         'tl.fromTo("#s16-p2",{y:1300},{y:0,duration:.45,ease:"back.out(1.4)"},at(55.90));'
         'tl.fromTo("#s16-p3",{y:1300,rotation:30},{y:0,rotation:0,duration:.45,ease:"back.out(1.4)"},at(56.60));'
         'tl.fromTo(["#s16-p1","#s16-p2","#s16-p3"],{opacity:1,y:0},{opacity:0,y:-900,duration:.3,ease:"power3.in",immediateRender:false},at(57.55));'
         'tl.fromTo("#s16-end",{opacity:0},{opacity:1,duration:.1,ease:"none"},at(57.70));'
         'tl.fromTo("#s16-logo",{scale:0,rotation:-40},{scale:1,rotation:0,duration:.45,ease:"back.out(2.6)"},at(57.75));'
         'tl.fromTo("#s16-name",{scale:2.4,opacity:0},{scale:1,opacity:1,duration:.26,ease:"power4.out"},at(58.16));'
         'tl.fromTo("#s16-url",{scale:2.4,opacity:0,rotation:-6},{scale:1,opacity:1,rotation:-3,duration:.24,ease:"power4.out"},at(58.95));'
         'tl.fromTo("#s16-st",{y:40,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(59.45));'),)),
]
PUNCH = [(0.58, 1.06), (1.35, 1.07), (2.83, 1.08), (4.51, 1.05), (5.80, 1.05), (6.36, 1.07), (7.56, 1.06), (8.93, 1.07),
         (12.0, 1.06), (13.19, 1.06), (17.60, 1.07), (19.29, 1.06), (21.62, 1.07), (22.74, 1.07), (25.31, 1.08), (26.36, 1.06),
         (28.12, 1.06), (30.84, 1.06), (32.12, 1.10), (36.16, 1.07), (38.62, 1.05), (41.02, 1.05), (43.74, 1.06), (45.52, 1.05),
         (48.23, 1.06), (49.35, 1.05), (52.17, 1.06), (58.16, 1.05), (58.95, 1.06)]
SHAKE = [2.83, 6.36, 32.12]
POSES = [(0.18, "curieux"), (2.83, "non"), (3.80, "pointe"), (5.64, "choc"), (7.56, "un"), (8.93, "explique"), (11.9, "sceptique"),
         (16.5, "pouce"), (19.29, "deux"), (20.6, "explique"), (24.46, "curieux"), (26.36, "trois"), (27.6, "pointe"),
         (30.6, "sceptique"), (32.12, "choc"), (34.9, "non"), (37.4, "explique"), (42.64, "pouce"), (45.52, "curieux"),
         (49.35, "pointe"), (52.1, "pouce"), (54.45, "explique"), (57.9, "app"), (59.5, "pouce")]
KW = {"jeun", "sport", "maigrir", "mieux", "trois", "preuves", "surprendre", "20", "4", "dix", "même", "régime", "gras", "5",
      "96", "minuscule", "brûles", "3", "grammes", "cuillère", "rien", "journée", "calories", "sommeil", "entraînement",
      "choisis", "commentaire", "partage", "abonne-toi", "calibodi", "calibodicom"}
CHAPTERS = [0.0, 7.56, 19.29, 26.36]
