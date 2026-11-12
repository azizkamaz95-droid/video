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
                f'<g class="ih" id="{sid}-h{i}" opacity="0">{shape("#FF4D4D")}</g></g>' for i in range(n))
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
# Shot list of « boissons », read by build_v4.py. Global times in seconds (voice of 2026-11-12).
# Footage: coffee beans and cups, stairs seen from the feet, a night bedroom, an alarm clock, vegetables, a far runner (no women, no faces, no logos).
A = "#FF4D4D"
SHOTS = [
    ("s1", "grains", 0.00, 3.87, None, *acc(
        tag("s1", "a", "TU BOIS DES", f"{C} top: 250px; font-size: 70px; color: #fff;", 0.18),
        lab("s1", "b", "BOISSONS", "left: 180px; top: 340px; font-size: 120px;", 0.66),
        lab("s1", "c", "ÉNERGISANTES", "left: 90px; top: 520px; font-size: 84px;", 0.99, white=True),
        tag("s1", "d", "AVANT TA SÉANCE", f"{C} top: 700px; font-size: 64px; color: #fff;", 1.64),
        lab("s1", "e", "D'ÉNERGIE ?", "left: 120px; top: 820px; font-size: 96px;", 2.91))),
    ("s2", "tasse", 3.87, 6.68, "whip", *acc(
        tag("s2", "a", "ATTENTION", f"{C} top: 250px; font-size: 96px; color: #fff;", 3.96),
        tag("s2", "b", "TU POURRAIS FAIRE UNE", f"{C} top: 400px; font-size: 52px; color: #fff;", 4.91),
        lab("s2", "c", "ERREUR", "left: 190px; top: 520px; font-size: 150px;", 5.73))),
    ("s3", "marches", 6.68, 10.85, "zoom", *acc(
        lab("s3", "a", "CAFÉINE", "left: 200px; top: 280px; font-size: 140px;", 7.56),
        tag("s3", "b", "PEUT AMÉLIORER", f"{C} top: 480px; font-size: 70px; color: #fff;", 8.22),
        lab("s3", "c", "PERFORMANCES", "left: 100px; top: 600px; font-size: 84px;", 9.17, white=True),
        tag("s3", "d", "SPORTIVES", f"{C} top: 780px; font-size: 80px; color: #fff;", 9.79))),
    ("s4", "mug", 10.85, 13.28, "flash", *acc(
        tag("s4", "a", "MAIS IL Y A UN", f"{C} top: 250px; font-size: 70px; color: #fff;", 10.85),
        lab("s4", "b", "PIÈGE", "left: 280px; top: 380px; font-size: 150px;", 11.41),
        tag("s4", "c", "QUE BEAUCOUP IGNORENT", f"{C} top: 600px; font-size: 52px; color: #fff;", 11.90))),
    ("s5", "grains2", 13.28, 16.50, "whip", *acc(
        tag("s5", "a", "EN CONSOMMER TROP", f"{C} top: 250px; font-size: 56px; color: #fff;", 13.34),
        lab("s5", "b", "PALPITATIONS", "left: 90px; top: 400px; font-size: 90px;", 14.79),
        lab("s5", "c", "ANXIÉTÉ", "left: 220px; top: 560px; font-size: 110px;", 15.65, white=True))),
    ("s6", "chambre", 16.50, 19.14, "zoom", *acc(
        tag("s6", "a", "PERTURBER", f"{C} top: 250px; font-size: 90px; color: #fff;", 17.44),
        lab("s6", "b", "TON SOMMEIL", "left: 110px; top: 380px; font-size: 96px;", 18.00))),
    ("s7", "reveil", 19.14, 23.00, "flash", *acc(
        tag("s7", "a", "ET C'EST LÀ", f"{C} top: 250px; font-size: 70px; color: #fff;", 19.14),
        lab("s7", "b", "INTÉRESSANT", "left: 100px; top: 380px; font-size: 96px;", 19.86),
        tag("s7", "c", "TU PRENDS UNE BOISSON", f"{C} top: 560px; font-size: 50px; color: #fff;", 20.89),
        lab("s7", "d", "BOOSTER", "left: 200px; top: 680px; font-size: 130px;", 21.82, white=True))),
    ("s8", "lit", 23.00, 26.00, "whip", *acc(
        tag("s8", "a", "MAIS TU RISQUES", f"{C} top: 250px; font-size: 70px; color: #fff;", 23.22),
        lab("s8", "b", "COMPROMETTRE", "left: 90px; top: 380px; font-size: 84px;", 23.78),
        lab("s8", "c", "RÉCUPÉRATION", "left: 80px; top: 540px; font-size: 84px;", 24.37, white=True),
        tag("s8", "d", "PENDANT LA NUIT", f"{C} top: 720px; font-size: 64px; color: #fff;", 25.06))),
    ("s9", "horloge", 26.00, 28.30, "zoom", *acc(
        tag("s9", "a", "AVANT DE CHERCHER", f"{C} top: 250px; font-size: 60px; color: #fff;", 26.53),
        lab("s9", "b", "UN COUP DE BOOST", "left: 100px; top: 380px; font-size: 62px;", 27.16),
        tag("s9", "c", "DEMANDE-TOI", f"{C} top: 560px; font-size: 90px; color: #fff;", 27.80))),
    ("s10", "legumes", 28.30, 30.97, "flash", *acc(
        tag("s10", "a", "SI TU DORS", f"{C} top: 250px; font-size: 80px; color: #fff;", 28.45),
        lab("s10", "b", "SUFFISAMMENT", "left: 90px; top: 380px; font-size: 86px;", 28.69),
        tag("s10", "c", "ET SI TU MANGES", f"{C} top: 560px; font-size: 66px; color: #fff;", 29.41),
        lab("s10", "d", "CORRECTEMENT", "left: 80px; top: 700px; font-size: 80px;", 29.90, white=True))),
    ("s11", "coureur", 30.97, 34.06, "whip", *acc(
        tag("s11", "a", "DIS-MOI EN COMMENTAIRE", f"{C} top: 250px; font-size: 50px; color: #fff;", 31.03),
        lab("s11", "b", "TU PRENDS QUOI", "left: 150px; top: 400px; font-size: 70px;", 32.43),
        tag("s11", "c", "AVANT TA SÉANCE ?", f"{C} top: 560px; font-size: 64px; color: #fff;", 32.98))),
    ("s12", "fin", 34.06, D, "flash", *acc(
        ('<div id="s12-end"><div class="tag" id="s12-ab">ABONNE-TOI</div><div class="tag" id="s12-nv">UNE NOUVELLE VIDÉO CHAQUE JOUR</div>'
         '<img id="s12-logo" src="assets/brand/icon-512.png" alt="CaliBodi" /><div class="big" id="s12-name">CaliBodi</div>'
         '<div class="lab" id="s12-url">calibodi.com</div><div class="tag" id="s12-st">Play Store · App Store</div></div>',
         "#s12-end { position: absolute; inset: 0; }"
         "#s12-ab { left: 0; width: 1080px; top: 190px; text-align: center; font-size: 84px; color: #fff; }"
         "#s12-nv { left: 0; width: 1080px; top: 300px; text-align: center; font-size: 46px; color: #fff; }"
         "#s12-logo { position: absolute; left: 400px; top: 410px; width: 280px; height: 280px; border-radius: 62px; box-shadow: 0 20px 50px rgba(0,0,0,.5); }"
         "#s12-name { left: 0; width: 1080px; top: 720px; text-align: center; font-size: 150px; color: #fff; text-shadow: 0 16px 50px rgba(0,0,0,.7); }"
         "#s12-url { left: 230px; top: 880px; font-size: 100px; }"
         "#s12-st { left: 0; width: 1080px; top: 1015px; text-align: center; font-size: 56px; color: #fff; }",
         'tl.fromTo("#s12-ab",{y:50,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(34.35));'
         'tl.fromTo("#s12-nv",{y:50,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(35.14));'
         'tl.fromTo("#s12-logo",{scale:0,rotation:-40},{scale:1,rotation:0,duration:.45,ease:"back.out(2.6)"},at(35.70));'
         'tl.fromTo("#s12-name",{scale:2.4,opacity:0},{scale:1,opacity:1,duration:.26,ease:"power4.out"},at(36.30));'
         'tl.fromTo("#s12-url",{scale:2.4,opacity:0,rotation:-6},{scale:1,opacity:1,rotation:-3,duration:.24,ease:"power4.out"},at(36.79));'
         'tl.fromTo("#s12-st",{y:40,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(37.50));'))),
]
PUNCH = [(0.99, 1.07), (2.91, 1.08), (5.73, 1.09), (9.17, 1.06), (11.41, 1.08), (14.79, 1.07), (18.00, 1.07), (19.86, 1.06),
         (21.82, 1.06), (24.37, 1.07), (28.69, 1.05), (32.43, 1.06), (36.30, 1.05)]
SHAKE = [11.41, 25.38]
POSES = [(0.20, "curieux"), (3.90, "choc"), (6.70, "explique"), (10.90, "sceptique"), (13.30, "non"), (16.60, "fatigue"),
         (19.20, "explique"), (23.10, "choc"), (26.10, "pointe"), (28.40, "nutrition"), (31.00, "pointe"),
         (34.90, "app"), (36.40, "pouce")]
KW = {"énergisantes", "caféine", "performances", "piège", "palpitations", "anxiété", "sommeil", "intéressant", "booster",
      "récupération", "boost", "séance", "erreur", "commentaire", "calibodi", "calibodicom"}
CHAPTERS = [0.0, 6.68, 13.28, 19.14, 26.00]
