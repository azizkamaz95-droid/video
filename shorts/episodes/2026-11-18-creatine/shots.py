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
                f'<g class="ih" id="{sid}-h{i}" opacity="0">{shape("#FF4FA3")}</g></g>' for i in range(n))
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
# Shot list of « etirements » (voix du 2026-11-17). Musculation vue de dos / silhouettes, sans visage.
A = "#FF4FA3"
SHOTS = [
    ("s1", "a1", 0.00, 6.20, None, *acc(
        tag("s1", "a", "JAMBES TENDUES", f"{C} top: 200px; font-size: 84px; color: #fff;", 2.90),
        big("s1", "n", "30", f"{C} top: 330px; font-size: 380px; color: {A}; {SH}", 3.78),
        lab("s1", "b", "SECONDES", "left: 280px; top: 740px; font-size: 100px;", 4.02, white=True))),
    ("s2", "b1", 6.20, 8.40, "whip", *acc(
        lab("s2", "a", "TE PROTÈGE", "left: 200px; top: 300px; font-size: 110px;", 7.31),
        tag("s2", "b", "VRAIMENT ?", f"{C} top: 500px; font-size: 110px; color: #fff;", 7.79))),
    ("s3", "c1", 8.40, 14.10, "zoom", *acc(
        src("s3", "Behm et coll., Applied Physiology, Nutrition, and Metabolism, 2016", 10.9),
        tag("s3", "a", "ÉTIREMENTS STATIQUES", f"{C} top: 220px; font-size: 66px; color: #fff;", 10.35),
        lab("s3", "b", "PAS UNE GARANTIE", "left: 100px; top: 400px; font-size: 90px;", 12.28),
        tag("s3", "c", "CONTRE LES BLESSURES", f"{C} top: 620px; font-size: 66px; color: #fff;", 13.00))),
    ("s4", "d1", 14.10, 19.20, "flash", *acc(
        tag("s4", "a", "LONGS ET SEULS", f"{C} top: 220px; font-size: 84px; color: #fff;", 15.03),
        lab("s4", "b", "TEMPORAIREMENT", "left: 100px; top: 400px; font-size: 86px;", 17.40),
        lab("s4", "c", "− DE FORCE", "left: 250px; top: 600px; font-size: 120px;", 18.20, white=True))),
    ("s5", "e1", 19.20, 21.80, "whip", *acc(
        tag("s5", "a", "ALORS ?", f"{C} top: 220px; font-size: 120px; color: #fff;", 19.58),
        lab("s5", "b", "À LA PLACE ?", "left: 200px; top: 430px; font-size: 110px;", 20.80))),
    ("s6", "f1", 21.80, 29.40, "flash", *acc(
        tag("s6", "a", "ÉCHAUFFEMENT", f"{C} top: 220px; font-size: 90px; color: #fff;", 23.25),
        lab("s6", "b", "PROGRESSIF", "left: 180px; top: 380px; font-size: 110px;", 23.65),
        tag("s6", "c", "MARCHE RAPIDE", f"{C} top: 580px; font-size: 70px; color: #fff;", 24.69),
        tag("s6", "d", "ROTATIONS DES BRAS", f"{C} top: 690px; font-size: 70px; color: #fff;", 25.66),
        tag("s6", "e", "MOUVEMENTS DES JAMBES", f"{C} top: 800px; font-size: 64px; color: #fff;", 26.78))),
    ("s7", "g1", 29.40, 37.30, "zoom", *acc(
        tag("s7", "a", "ÉTIREMENTS STATIQUES", f"{C} top: 220px; font-size: 66px; color: #fff;", 29.93),
        lab("s7", "b", "UTILES", "left: 290px; top: 380px; font-size: 130px;", 32.09),
        tag("s7", "c", "POUR LA SOUPLESSE", f"{C} top: 620px; font-size: 72px; color: #fff;", 33.12),
        lab("s7", "d", "PAS SYSTÉMATIQUE", "left: 100px; top: 780px; font-size: 82px;", 35.20, white=True))),
    ("s8", "h1", 37.30, 40.30, "whip", *acc(
        tag("s8", "a", "ET TOI ?", f"{C} top: 220px; font-size: 120px; color: #fff;", 37.71),
        lab("s8", "b", "AVANT", "left: 120px; top: 410px; font-size: 130px;", 38.83),
        lab("s8", "c", "OU APRÈS ?", "left: 330px; top: 590px; font-size: 120px;", 39.31, white=True))),
    ("s9", "fin", 40.30, D, "flash", *acc(
        ('<div id="s9-end"><div class="tag" id="s9-ab">ABONNE-TOI</div><div class="tag" id="s9-nv">UNE NOUVELLE VIDÉO CHAQUE JOUR</div>'
         '<img id="s9-logo" src="assets/brand/icon-512.png" alt="CaliBodi" /><div class="big" id="s9-name">CaliBodi</div>'
         '<div class="lab" id="s9-url">calibodi.com</div><div class="tag" id="s9-st">Play Store · App Store</div></div>',
         "#s9-end { position: absolute; inset: 0; }"
         "#s9-ab { left: 0; width: 1080px; top: 190px; text-align: center; font-size: 84px; color: #fff; }"
         "#s9-nv { left: 0; width: 1080px; top: 300px; text-align: center; font-size: 46px; color: #fff; }"
         "#s9-logo { position: absolute; left: 400px; top: 410px; width: 280px; height: 280px; border-radius: 62px; box-shadow: 0 20px 50px rgba(0,0,0,.5); }"
         "#s9-name { left: 0; width: 1080px; top: 720px; text-align: center; font-size: 150px; color: #fff; text-shadow: 0 16px 50px rgba(0,0,0,.7); }"
         "#s9-url { left: 230px; top: 880px; font-size: 100px; }"
         "#s9-st { left: 0; width: 1080px; top: 1015px; text-align: center; font-size: 56px; color: #fff; }",
         'tl.fromTo("#s9-ab",{y:50,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(40.65));'
         'tl.fromTo("#s9-nv",{y:50,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(41.42));'
         'tl.fromTo("#s9-logo",{scale:0,rotation:-40},{scale:1,rotation:0,duration:.45,ease:"back.out(2.6)"},at(43.18));'
         'tl.fromTo("#s9-name",{scale:2.4,opacity:0},{scale:1,opacity:1,duration:.26,ease:"power4.out"},at(43.18));'
         'tl.fromTo("#s9-url",{scale:2.4,opacity:0,rotation:-6},{scale:1,opacity:1,rotation:-3,duration:.24,ease:"power4.out"},at(43.84));'
         'tl.fromTo("#s9-st",{y:40,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(44.50));'))),
]
PUNCH = [(3.78, 1.09), (7.31, 1.06), (10.35, 1.06), (12.28, 1.07), (18.20, 1.09), (23.25, 1.06), (32.09, 1.07), (38.83, 1.06), (43.84, 1.05)]
SHAKE = [18.20]
POSES = [(0.20, "curieux"), (6.30, "sceptique"), (8.50, "non"), (14.20, "choc"), (19.60, "curieux"), (22.00, "explique"),
         (29.50, "pouce"), (37.40, "curieux"), (42.40, "app"), (44.00, "pouce")]
KW = {"étirements", "statiques", "jambes", "secondes", "protège", "vraiment", "garantie", "blessures", "force", "maximale",
      "échauffement", "progressif", "souplesse", "calibodi", "calibodicom", "30", "avant", "après"}
CHAPTERS = [0.0, 8.40, 21.80]
