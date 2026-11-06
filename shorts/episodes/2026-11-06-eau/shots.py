# Shot list of « Combien de litres d'eau par jour », read by build_v4.py (exec'd after its defaults). Global times in seconds.
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
ML = "white-space: normal; line-height: 1;"
SHOTS = [
    ("s1", "verse", 0.00, 4.05, None, *acc(
        big("s1", "a", "1,5 L", f"{C} top: 330px; font-size: 330px; color: #FF6B35; {SH}", 0.69, out=2.3),
        big("s1", "b", "2 L", f"{C} top: 330px; font-size: 420px; color: #FF6B35; {SH}", 2.42, out=3.3),
        big("s1", "c", "3 L", f"{C} top: 330px; font-size: 420px; color: #FF6B35; {SH}", 3.38),
        tag("s1", "t", "D'EAU PAR JOUR", f"{C} top: 250px; font-size: 76px; letter-spacing: .04em; color: #fff;", 1.09))),
    ("s2", "bouteille", 4.05, 6.55, "zoom", *acc(
        lab("s2", "a", "AUCUN CHIFFRE", "left: 120px; top: 250px; font-size: 110px;", 4.67),
        lab("s2", "b", "PAS POUR TOUT LE MONDE", "left: 60px; top: 420px; font-size: 70px;", 5.39, white=True))),
    ("s3", "vagues", 6.55, 9.55, "flash", *acc(
        lab("s3", "p", "3 PREUVES", "left: 200px; top: 250px; font-size: 130px;", 6.99),
        lab("s3", "l", "LA DERNIÈRE ?", "left: 120px; top: 440px; font-size: 100px;", 8.20, white=True),
        big("s3", "q", "!", f"left: 700px; top: 560px; font-size: 460px; color: #FF6B35; {SH}", 8.84))),
    ("s4", "plage", 9.55, 14.95, "whip", *acc(
        lab("s4", "f", "PREUVE 1", "left: 70px; top: 230px; font-size: 120px;", 9.96, out=11.1),
        tag("s4", "t", "EN FRANCE : L'ANSES", f"{C} top: 250px; font-size: 76px; color: #fff;", 11.24),
        big("s4", "n", "1,5–2 L", f"{C} top: 380px; font-size: 250px; color: #FF6B35; {SH}", 12.80),
        tag("s4", "j", "PAR JOUR", f"{C} top: 660px; font-size: 80px; color: #fff;", 14.37),
        src("s4", "Anses, fiche « Eau en bouteille ou eau du robinet »", 10.3))),
    ("s5", "rocher", 14.95, 17.0, "zoom", *acc(
        tag("s5", "a", "C'EST JUSTE", f"{C} top: 250px; font-size: 90px; color: #fff;", 15.31),
        lab("s5", "m", "UNE MOYENNE", "left: 130px; top: 400px; font-size: 110px;", 15.7))),
    ("s6", "grotte", 17.0, 21.3, "flash", *acc(
        lab("s6", "f", "PREUVE 2", "left: 70px; top: 230px; font-size: 120px;", 17.18, out=18.3),
        tag("s6", "e", "EN EUROPE : L'EFSA", f"{C} top: 250px; font-size: 74px; color: #fff;", 18.34),
        big("s6", "n", "2 L", f"{C} top: 380px; font-size: 400px; color: #FF6B35; {SH}", 20.06),
        lab("s6", "w", "FEMMES", "left: 330px; top: 800px; font-size: 100px;", 20.78, white=True),
        src("s6", "EFSA, avis scientifique, 2010", 17.6))),
    ("s7", "coucher", 21.3, 23.2, "whip", *acc(
        big("s7", "n", "2,5 L", f"{C} top: 330px; font-size: 360px; color: #FF6B35; {SH}", 21.67),
        lab("s7", "h", "HOMMES", "left: 300px; top: 760px; font-size: 100px;", 22.64, white=True))),
    ("s8", "concombre", 23.2, 26.0, "zoom", *acc(
        tag("s8", "a", "CES LITRES COMPTENT", f"{C} top: 250px; font-size: 76px; color: #fff;", 23.43),
        lab("s8", "n", "L'EAU DE LA NOURRITURE", "left: 40px; top: 400px; font-size: 70px;", 24.60))),
    ("s9", "globe", 26.0, 31.1, "flash", *acc(
        lab("s9", "f", "PREUVE 3", "left: 70px; top: 230px; font-size: 120px;", 26.0, out=27.3),
        big("s9", "a", "5 600", f"{C} top: 270px; font-size: 300px; color: #141414;", 28.40),
        tag("s9", "b", "PERSONNES", f"{C} top: 570px; font-size: 80px; color: #141414;", 29.29),
        big("s9", "c", "23", f"{C} top: 700px; font-size: 280px; color: #141414;", 29.93),
        tag("s9", "d", "PAYS", f"{C} top: 960px; font-size: 90px; color: #141414;", 30.41),
        src("s9", "Yamada et al., Science, 2022", 26.5))),
    ("s10", "cascade", 31.1, 34.1, "whip", *acc(
        tag("s10", "a", "L'EAU DU CORPS RENOUVELÉE", f"{C} top: 250px; font-size: 62px; color: #fff;", 31.61),
        big("s10", "n", "1 À 6 L", f"{C} top: 360px; font-size: 270px; color: #FF6B35; {SH}", 32.27),
        tag("s10", "j", "PAR JOUR", f"{C} top: 650px; font-size: 80px; color: #fff;", 33.22))),
    ("s11", "neon", 34.1, 37.2, "zoom", *acc(
        lab("s11", "s", "SPORTIFS", "left: 80px; top: 250px; font-size: 120px;", 34.29),
        big("s11", "n", "+1 L", f"{C} top: 420px; font-size: 360px; color: #fff; {SH}", 35.80))),
    ("s12", "gouttes", 37.2, 39.9, "flash", *acc(
        lab("s12", "n", "DONC NON", "left: 200px; top: 250px; font-size: 130px;", 37.39),
        tag("s12", "m", "PAS DE CHIFFRE MAGIQUE", f"{C} top: 460px; font-size: 66px; color: #fff;", 38.83))),
    ("s13", "desert", 39.9, 43.6, "whip", *acc(
        tag("s13", "d", "ÇA DÉPEND DE TOI", f"{C} top: 240px; font-size: 90px; color: #fff;", 40.19),
        lab("s13", "c", "TON CORPS", "left: 90px; top: 420px; font-size: 100px;", 41.24),
        lab("s13", "s", "TON SPORT", "left: 90px; top: 580px; font-size: 100px;", 41.72, white=True),
        lab("s13", "k", "TON CLIMAT", "left: 90px; top: 740px; font-size: 100px;", 42.60))),
    ("s14", "lac", 43.6, 47.5, "zoom", *acc(
        tag("s14", "t", "ET TOI ?", f"{C} top: 240px; font-size: 130px; color: #FF6B35;", 43.74),
        tag("s14", "q", "TU BOIS COMBIEN<br>DE LITRES PAR JOUR ?", f"{C} top: 400px; font-size: 74px; color: #fff; {ML}", 44.28),
        lab("s14", "c", "COMMENTE", "left: 260px; top: 680px; font-size: 110px;", 46.61))),
    ("s15", "cote", 47.5, 50.0, "flash", *acc(
        ('<div class="ic2" id="s15-ic"><svg viewBox="0 0 140 140"><path d="M14 120 C 20 70, 50 44, 104 44 M84 18 L 122 44 L 84 72" fill="none" stroke="#141414" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" /></svg></div>',
         "#s15-ic { position: absolute; left: 70px; top: 250px; width: 170px; height: 170px; border-radius: 50%; background: #fff; box-shadow: 0 14px 30px rgba(0,0,0,.4); }"
         "#s15-ic svg { position: absolute; left: 25px; top: 25px; width: 120px; height: 120px; overflow: visible; }",
         'tl.fromTo("#s15-ic",{scale:0,rotation:-40},{scale:1,rotation:0,duration:.35,ease:"back.out(2.4)"},at(47.65));'),
        lab("s15", "p", "PARTAGE", "left: 270px; top: 270px; font-size: 120px;", 47.65),
        tag("s15", "q", "À QUELQU'UN QUI<br>COMPTE SES LITRES", f"{C} top: 470px; font-size: 70px; color: #fff; {ML}", 48.62))),
    ("s16", "ressac", 50.0, 52.8, "whip", *acc(
        lab("s16", "a", "ABONNE-TOI", "left: 70px; top: 260px; font-size: 140px;", 50.31),
        lab("s16", "j", "1 VIDÉO CHAQUE JOUR", "left: 80px; top: 480px; font-size: 62px;", 51.28, white=True))),
    ("s17", "fin", 52.80, D, "zoom", *acc(
        ('<div class="phone" id="s17-p1"><img src="assets/app/hydration.jpg" alt="écran hydratation CaliBodi" /></div>'
         '<div class="phone" id="s17-p2"><img src="assets/app/nutrition.jpg" alt="écran alimentation CaliBodi" /></div>'
         '<div class="phone" id="s17-p3"><img src="assets/app/fitness.jpg" alt="écran entraînements CaliBodi" /></div>'
         '<div id="s17-end"><img id="s17-logo" src="assets/brand/icon-512.png" alt="CaliBodi" /><div class="big" id="s17-name">CaliBodi</div>'
         '<div class="lab" id="s17-url">calibodi.com</div><div class="tag" id="s17-st">Play Store · App Store</div></div>',
         ".phone { position: absolute; top: 300px; width: 320px; height: 640px; padding: 12px; background: #141414; border-radius: 48px; box-shadow: 0 30px 60px rgba(0,0,0,.6); }"
         ".phone img { width: 100%; height: 100%; border-radius: 38px; object-fit: cover; object-position: top; display: block; }"
         "#s17-p1 { left: 40px; rotate: -6deg; } #s17-p2 { left: 380px; top: 270px; } #s17-p3 { left: 720px; rotate: 6deg; }"
         "#s17-end { position: absolute; inset: 0; opacity: 0; }"
         "#s17-logo { position: absolute; left: 400px; top: 250px; width: 280px; height: 280px; border-radius: 62px; box-shadow: 0 20px 50px rgba(0,0,0,.5); }"
         "#s17-name { left: 0; width: 1080px; top: 570px; text-align: center; font-size: 150px; color: #fff; text-shadow: 0 16px 50px rgba(0,0,0,.7); }"
         "#s17-url { left: 230px; top: 760px; font-size: 100px; }"
         "#s17-st { left: 0; width: 1080px; top: 910px; text-align: center; font-size: 56px; color: #fff; }",
         'tl.fromTo("#s17-p1",{y:1300,rotation:-30},{y:0,rotation:0,duration:.45,ease:"back.out(1.4)"},at(53.5));'
         'tl.fromTo("#s17-p2",{y:1300},{y:0,duration:.45,ease:"back.out(1.4)"},at(54.4));'
         'tl.fromTo("#s17-p3",{y:1300,rotation:30},{y:0,rotation:0,duration:.45,ease:"back.out(1.4)"},at(55.1));'
         'tl.fromTo(["#s17-p1","#s17-p2","#s17-p3"],{opacity:1,y:0},{opacity:0,y:-900,duration:.3,ease:"power3.in",immediateRender:false},at(55.85));'
         'tl.fromTo("#s17-end",{opacity:0},{opacity:1,duration:.1,ease:"none"},at(56.0));'
         'tl.fromTo("#s17-logo",{scale:0,rotation:-40},{scale:1,rotation:0,duration:.45,ease:"back.out(2.6)"},at(56.05));'
         'tl.fromTo("#s17-name",{scale:2.4,opacity:0},{scale:1,opacity:1,duration:.26,ease:"power4.out"},at(56.5));'
         'tl.fromTo("#s17-url",{scale:2.4,opacity:0,rotation:-6},{scale:1,opacity:1,rotation:-3,duration:.24,ease:"power4.out"},at(57.4));'
         'tl.fromTo("#s17-st",{y:40,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(57.8));'),)),
]
PUNCH = [(0.69, 1.07), (2.42, 1.07), (3.38, 1.08), (4.67, 1.06), (6.99, 1.05), (8.84, 1.07), (9.96, 1.06), (12.80, 1.07),
         (16.16, 1.07), (17.18, 1.06), (20.06, 1.08), (21.67, 1.08), (24.60, 1.06), (28.40, 1.07), (29.93, 1.07), (32.27, 1.08),
         (35.80, 1.09), (37.39, 1.07), (41.24, 1.05), (43.74, 1.05), (46.61, 1.06), (47.65, 1.05), (50.31, 1.06), (56.50, 1.05), (57.40, 1.06)]
SHAKE = [3.38, 8.84, 35.80]
POSES = [(0.18, "curieux"), (2.5, "choc"), (4.1, "non"), (6.67, "trois"), (9.96, "un"), (11.3, "explique"), (15.0, "sceptique"),
         (17.18, "deux"), (18.4, "explique"), (21.4, "pointe"), (23.3, "nutrition"), (26.0, "trois"), (27.5, "explique"),
         (31.2, "choc"), (34.2, "biceps"), (37.4, "non"), (40.0, "pointe"), (43.7, "curieux"), (47.6, "pointe"),
         (50.1, "pouce"), (53.0, "explique"), (56.0, "app"), (57.6, "pouce")]
KW = {"litre", "litres", "eau", "chiffres", "trois", "preuves", "surprendre", "anses", "europe", "nourriture", "5", "600", "23",
      "renouvelle", "sportifs", "magique", "dépend", "corps", "sport", "climat", "combien", "commentaire", "partage", "abonne-toi",
      "hydratation", "calories", "calibodi", "calibodicom"}
CHAPTERS = [0.0, 9.96, 17.18, 26.0]
