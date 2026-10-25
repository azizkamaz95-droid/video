# Shot list of « Physique ou argent ? C'est le physique. », read by build_v4.py (exec'd after its defaults). Global times in seconds.
# Each shot: (id, clip, start, end, transition in, accent html, accent css, accent js). Footage: objects, places,
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
SHOTS = [
    ("s1", "cash1", 0.00, 2.60, None, *acc(
        lab("s1", "p", "PHYSIQUE", "left: 70px; top: 300px; font-size: 150px;", 0.18),
        tag("s1", "o", "OU", f"{C} top: 500px; font-size: 110px; color: #fff;", 0.74),
        lab("s1", "a", "ARGENT ?", "left: 200px; top: 650px; font-size: 140px;", 0.76, white=True))),
    ("s2", "barre1", 2.60, 5.20, "flash", *acc(
        big("s2", "l", "C'EST LE<br>PHYSIQUE.", f"{C} top: 230px; font-size: 150px; color: #FFC93C; white-space: normal; line-height: .95; {SH}", 2.86),
        lab("s2", "n", "3 PREUVES", "left: 300px; top: 1250px; font-size: 100px;", 4.19))),
    ("s3", "profil1", 5.20, 8.60, "zoom", *acc(
        tag("s3", "l", "N°3", "left: 120px; top: 360px; font-size: 150px; color: #fff;", 5.40),
        big("s3", "q", "?", f"left: 600px; top: 180px; font-size: 520px; color: #FFC93C; {SH}", 5.99, out=7.1))),
    ("s4", "cafe", 8.60, 12.20, "whip", *acc(
        lab("s4", "f", "FAIT N°1", "left: 70px; top: 230px; font-size: 120px;", 8.69, out=9.7),
        big("s4", "n", "10 000", f"{C} top: 330px; font-size: 230px; color: #FFC93C; {SH}", 9.93),
        tag("s4", "t", "PERSONNES EN SPEED DATING", f"{C} top: 590px; font-size: 56px; letter-spacing: .03em; color: #fff;", 11.07),
        src("s4", "Kurzban & Weeden, Evolution and Human Behavior, 2005", 9.0))),
    ("s5", "sablier", 12.20, 16.45, "zoom", *acc(
        big("s5", "n", "3 MIN", f"{C} top: 300px; font-size: 260px; color: #FFC93C; {SH}", 12.31),
        tag("s5", "t", "PAR RENCONTRE", f"{C} top: 560px; font-size: 76px; letter-spacing: .05em; color: #fff;", 12.71),
        tag("s5", "r", "QUI TU VEUX REVOIR ?", f"{C} top: 690px; font-size: 64px; color: #fff;", 14.88))),
    ("s6", "barre2", 16.45, 18.65, "flash", *acc(
        lab("s6", "c", "CHOIX : LE PHYSIQUE", "left: 60px; top: 260px; font-size: 78px;", 17.08))),
    ("s7", "dollars", 18.65, 21.10, "whip", *acc(
        lab("s7", "s", "LE SALAIRE ?", "left: 70px; top: 260px; font-size: 120px;", 18.81, white=True),
        lab("s7", "z", "PRESQUE AUCUN EFFET", "left: 60px; top: 430px; font-size: 74px;", 19.97))),
    ("s8", "archives", 21.10, 25.30, "flash", *acc(
        lab("s8", "f", "FAIT N°2", "left: 70px; top: 230px; font-size: 120px;", 21.22, out=22.4),
        tag("s8", "t", "PHOTOS DE CORPS<br>D'HOMMES", "left: 70px; top: 380px; font-size: 96px; color: #fff; white-space: normal; line-height: .95;", 23.55),
        src("s8", "Sell, Lukaszewski & Townsley, Proceedings of the Royal Society B, 2017", 21.6))),
    ("s9", "barre3", 25.30, 29.90, "zoom", *acc(
        tag("s9", "q", "AVOIR L'AIR FORT", f"{C} top: 250px; font-size: 92px; color: #fff;", 26.70),
        big("s9", "n", "+70 %", f"{C} top: 380px; font-size: 230px; color: #FFC93C; {SH}", 28.69))),
    ("s10", "barre4", 29.90, 32.85, "whip", *acc(
        big("s10", "z", "0 FEMME", f"{C} top: 250px; font-size: 170px; color: #FFC93C; {SH}", 30.31),
        tag("s10", "t", "N'A PRÉFÉRÉ<br>LES PLUS FAIBLES", f"{C} top: 450px; font-size: 76px; color: #fff; white-space: normal; line-height: 1;", 31.02))),
    ("s11", "orage", 32.85, 35.65, "flash", *acc(
        tag("s11", "k", "FAIT N°", f"{C} top: 250px; font-size: 110px; color: #fff;", 32.94),
        big("s11", "n", "3", f"{C} top: 330px; font-size: 640px; color: #FFC93C; {SH}", 33.42))),
    ("s12", "cash2", 35.65, 41.30, "zoom", *acc(
        tag("s12", "a", "AVANT LA SOIRÉE :", "left: 70px; top: 250px; font-size: 76px; color: #fff;", 35.78),
        bubble("s12", "b", "« L'ARGENT,<br>C'EST IMPORTANT »", "left: 70px; top: 370px;", 37.97),
        src("s12", "Eastwick & Finkel, Journal of Personality and Social Psychology, 2008", 36.0))),
    ("s13", "latte", 41.30, 44.10, "whip", *acc(
        big("s13", "n", "DIRE ≠ CHOISIR", f"{C} top: 300px; font-size: 130px; color: #fff; {SH}", 42.27))),
    ("s14", "profil2", 44.10, 47.40, "zoom", *acc(
        lab("s14", "d", "ELLES DISENT : L'ARGENT", "left: 60px; top: 260px; font-size: 70px;", 44.36, white=True),
        lab("s14", "c", "ELLES CHOISISSENT : LE PHYSIQUE", "left: 60px; top: 390px; font-size: 56px;", 45.73))),
    ("s15", "alliances", 47.40, 53.40, "whip", *acc(
        tag("s15", "r", "RELATION LONGUE :<br>D'AUTRES CHOSES COMPTENT", f"{C} top: 260px; font-size: 64px; color: #fff; white-space: normal; line-height: 1.05;", 48.77),
        lab("s15", "p", "1ER PAS = LE PHYSIQUE", "left: 70px; top: 520px; font-size: 74px;", 51.38))),
    ("s16", "bras", 53.40, 58.25, "zoom", *acc(
        big("s16", "t", "ÇA SE TRAVAILLE", f"{C} top: 250px; font-size: 110px; color: #fff; {SH}", 55.08),
        lab("s16", "e", "ENTRAÎNEMENT", "left: 80px; top: 420px; font-size: 76px;", 56.14),
        lab("s16", "s", "SOMMEIL", "left: 80px; top: 530px; font-size: 76px;", 56.69, white=True),
        lab("s16", "a", "ALIMENTATION", "left: 80px; top: 640px; font-size: 76px;", 57.18))),
    ("s17", "mains2", 58.25, 61.95, "flash", *acc(
        tag("s17", "q", "LES FILLES,<br>C'EST VRAI OU FAUX ?", f"{C} top: 250px; font-size: 84px; color: #fff; white-space: normal; line-height: 1;", 58.48),
        lab("s17", "vr", "VRAI", "left: 110px; top: 520px; font-size: 130px;", 59.26),
        lab("s17", "x", "FAUX", "left: 600px; top: 520px; font-size: 130px;", 59.74, white=True))),
    ("s18", "ville3", 61.95, 68.15, "whip", *acc(
        ('<div class="ic2" id="s18-ic"><svg viewBox="0 0 140 140"><path d="M14 120 C 20 70, 50 44, 104 44 M84 18 L 122 44 L 84 72" fill="none" stroke="#141414" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" /></svg></div>',
         "#s18-ic { position: absolute; left: 70px; top: 250px; width: 170px; height: 170px; border-radius: 50%; background: #fff; box-shadow: 0 14px 30px rgba(0,0,0,.4); }"
         "#s18-ic svg { position: absolute; left: 25px; top: 25px; width: 120px; height: 120px; overflow: visible; }",
         'tl.fromTo("#s18-ic",{scale:0,rotation:-40},{scale:1,rotation:0,duration:.35,ease:"back.out(2.4)"},at(62.07));'
         'tl.fromTo("#s18-ic",{opacity:1},{opacity:0,duration:.2,ease:"none",immediateRender:false},at(64.9));'),
        lab("s18", "p", "PARTAGE", "left: 270px; top: 270px; font-size: 120px;", 62.07, out=64.9),
        tag("s18", "q", "À UN POTE QUI PENSE<br>QUE L'ARGENT SUFFIT", f"{C} top: 470px; font-size: 64px; color: #fff; white-space: normal; line-height: 1.05;", 63.19),
        ("", "", 'tl.fromTo("#s18-q",{opacity:1},{opacity:0,duration:.2,ease:"none",immediateRender:false},at(64.9));'),
        lab("s18", "a", "ABONNE-TOI", "left: 70px; top: 260px; font-size: 140px;", 65.14),
        big("s18", "h", "18H", f"{C} top: 470px; font-size: 300px; color: #FFC93C; {SH}", 67.23),
        tag("s18", "j", "1 VIDÉO CHAQUE JOUR", f"{C} top: 780px; font-size: 70px; letter-spacing: .04em; color: #fff;", 65.94))),
    ("s19", "ville4", 68.15, D, "zoom", *acc(
        ('<div class="phone" id="s19-p1"><img src="assets/app/fitness.jpg" alt="écran entraînements CaliBodi" /></div>'
         '<div class="phone" id="s19-p2"><img src="assets/app/sleep.jpg" alt="écran sommeil CaliBodi" /></div>'
         '<div class="phone" id="s19-p3"><img src="assets/app/nutrition.jpg" alt="écran alimentation CaliBodi" /></div>'
         '<div id="s19-end"><img id="s19-logo" src="assets/brand/icon-512.png" alt="CaliBodi" /><div class="big" id="s19-name">CaliBodi</div>'
         '<div class="lab" id="s19-url">calibodi.com</div><div class="tag" id="s19-st">Play Store · App Store</div></div>',
         ".phone { position: absolute; top: 300px; width: 320px; height: 640px; padding: 12px; background: #141414; border-radius: 48px; box-shadow: 0 30px 60px rgba(0,0,0,.6); }"
         ".phone img { width: 100%; height: 100%; border-radius: 38px; object-fit: cover; object-position: top; display: block; }"
         "#s19-p1 { left: 40px; rotate: -6deg; } #s19-p2 { left: 380px; top: 270px; } #s19-p3 { left: 720px; rotate: 6deg; }"
         "#s19-end { position: absolute; inset: 0; opacity: 0; }"
         "#s19-logo { position: absolute; left: 400px; top: 250px; width: 280px; height: 280px; border-radius: 62px; box-shadow: 0 20px 50px rgba(0,0,0,.5); }"
         "#s19-name { left: 0; width: 1080px; top: 570px; text-align: center; font-size: 150px; color: #fff; text-shadow: 0 16px 50px rgba(0,0,0,.7); }"
         "#s19-url { left: 230px; top: 760px; font-size: 100px; }"
         "#s19-st { left: 0; width: 1080px; top: 910px; text-align: center; font-size: 56px; color: #fff; }",
         'tl.fromTo("#s19-p1",{y:1300,rotation:-30},{y:0,rotation:0,duration:.45,ease:"back.out(1.4)"},at(68.99));'
         'tl.fromTo("#s19-p2",{y:1300},{y:0,duration:.45,ease:"back.out(1.4)"},at(70.10));'
         'tl.fromTo("#s19-p3",{y:1300,rotation:30},{y:0,rotation:0,duration:.45,ease:"back.out(1.4)"},at(70.76));'
         'tl.fromTo(["#s19-p1","#s19-p2","#s19-p3"],{opacity:1,y:0},{opacity:0,y:-900,duration:.3,ease:"power3.in",immediateRender:false},at(71.65));'
         'tl.fromTo("#s19-end",{opacity:0},{opacity:1,duration:.1,ease:"none"},at(71.87));'
         'tl.fromTo("#s19-logo",{scale:0,rotation:-40},{scale:1,rotation:0,duration:.45,ease:"back.out(2.6)"},at(71.9));'
         'tl.fromTo("#s19-name",{scale:2.4,opacity:0},{scale:1,opacity:1,duration:.26,ease:"power4.out"},at(72.32));'
         'tl.fromTo("#s19-url",{scale:2.4,opacity:0,rotation:-6},{scale:1,opacity:1,rotation:-3,duration:.24,ease:"power4.out"},at(73.12));'
         'tl.fromTo("#s19-st",{y:40,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(73.5));'),)),
]
PUNCH = [(0.18, 1.05), (0.76, 1.06), (2.94, 1.08), (4.19, 1.05), (5.99, 1.05), (8.69, 1.06), (9.93, 1.07), (12.31, 1.06), (17.77, 1.07),
         (19.97, 1.07), (21.22, 1.06), (26.70, 1.06), (28.69, 1.08), (30.31, 1.07), (33.42, 1.10), (37.97, 1.05), (42.27, 1.07),
         (45.73, 1.06), (51.38, 1.06), (55.08, 1.05), (59.26, 1.05), (59.74, 1.05), (62.07, 1.05), (65.14, 1.06), (67.23, 1.07),
         (72.32, 1.05), (73.12, 1.06)]
SHAKE = [2.94, 33.42, 45.73]
POSES = [(0.18, "curieux"), (2.75, "pointe"), (4.19, "trois"), (5.80, "curieux"), (7.17, "pointe"), (8.69, "un"), (9.93, "explique"),
         (16.56, "pouce"), (18.81, "non"), (21.22, "deux"), (22.51, "explique"), (26.70, "biceps"), (28.69, "choc"), (30.31, "pouce"),
         (32.94, "trois"), (34.14, "pointe"), (35.78, "explique"), (37.97, "sceptique"), (41.41, "curieux"), (44.22, "sceptique"),
         (45.73, "pointe"), (47.50, "explique"), (51.22, "pouce"), (53.55, "biceps"), (57.18, "nutrition"), (58.37, "curieux"),
         (60.46, "pointe"), (62.07, "pouce"), (65.14, "biceps"), (68.25, "app"), (71.87, "pouce")]
KW = {"physique", "argent", "physique.", "trois", "preuves", "surprendre", "bout", "10", "000", "speed", "dating", "minutes", "revoir",
      "salaire", "aucun", "fort", "70", "aucune", "faibles", "promis", "l'argent", "important", "choix", "yeux", "physique", "travaille",
      "entraînement", "sommeil", "alimentation", "vrai", "faux", "commentaire", "partage", "suffit", "abonne-toi", "18h", "calibodi", "calibodicom"}
CHAPTERS = [0.0, 8.69, 21.22, 32.94]
