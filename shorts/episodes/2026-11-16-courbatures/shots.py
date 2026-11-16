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
                f'<g class="ih" id="{sid}-h{i}" opacity="0">{shape("#B6FF3B")}</g></g>' for i in range(n))
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
# Shot list of « repos » (voix du 2026-11-15). Plans de musculation vus de dos ou sans visage, chrono vert sur fond noir.
A = "#B6FF3B"
SHOTS = [
    ("s1", "dos", 0.00, 4.00, None, *acc(
        tag("s1", "a", "TES SÉRIES", f"{C} top: 190px; font-size: 84px; color: #fff;", 0.66),
        big("s1", "n", "30", f"{C} top: 300px; font-size: 400px; color: {A}; {SH}", 1.70),
        lab("s1", "b", "SECONDES DE REPOS", "left: 90px; top: 760px; font-size: 80px;", 2.18))),
    ("s2", "halteres", 4.00, 7.70, "whip", *acc(
        lab("s2", "a", "RALENTIR", "left: 250px; top: 300px; font-size: 130px;", 5.38),
        tag("s2", "b", "TA PROGRESSION", f"{C} top: 500px; font-size: 84px; color: #fff;", 6.02),
        lab("s2", "c", "TROP VITE ?", "left: 220px; top: 650px; font-size: 120px;", 6.99, white=True))),
    ("s3", "banc", 7.70, 14.25, "zoom", *acc(
        tag("s3", "a", "CE QU'ON CROIT", f"{C} top: 220px; font-size: 80px; color: #fff;", 8.54, 9.55),
        lab("s3", "b", "TRANSPIRER", "left: 170px; top: 300px; font-size: 130px;", 9.63, out=11.9),
        lab("s3", "c", "PAS FORCÉMENT", "left: 110px; top: 560px; font-size: 100px;", 12.03, white=True),
        tag("s3", "d", "MIEUX TRAVAILLER", f"{C} top: 740px; font-size: 76px; color: #fff;", 12.83))),
    ("s4", "serie", 14.25, 19.80, "flash", *acc(
        tag("s4", "a", "RÉCUPÈRES TROP PEU", f"{C} top: 220px; font-size: 70px; color: #fff;", 14.87),
        lab("s4", "b", "MOINS DE RÉPÉTITIONS", "left: 40px; top: 400px; font-size: 70px;", 16.60),
        tag("s4", "c", "SÉRIES MOINS BONNES", f"{C} top: 640px; font-size: 68px; color: #fff;", 18.07))),
    ("s5", "chrono1", 19.80, 29.00, "whip", *acc(
        src("s5", "Singer et coll., Frontiers in Sports and Active Living, 2024", 20.4),
        tag("s5", "a", "MÉTA-ANALYSE · 2024", f"{C} top: 190px; font-size: 76px; color: #fff;", 20.20, 23.40),
        tag("s5", "r", "REPOS SUPÉRIEUR À", f"{C} top: 220px; font-size: 70px; color: #fff;", 23.49),
        big("s5", "n", "60", f"{C} top: 330px; font-size: 440px; color: {A}; {SH}", 24.05),
        lab("s5", "m", "SECONDES", "left: 270px; top: 790px; font-size: 100px;", 24.45, white=True),
        lab("s5", "p", "LÉGÈREMENT + DE MUSCLE", "left: 50px; top: 955px; font-size: 58px;", 25.36))),
    ("s6", "chrono2", 29.00, 34.55, "flash", *acc(
        tag("s6", "a", "NE REGARDE PAS", f"{C} top: 220px; font-size: 80px; color: #fff;", 30.19),
        lab("s6", "b", "QUE LE CHRONO", "left: 150px; top: 380px; font-size: 100px;", 30.96),
        tag("s6", "c", "RÉCUPÈRE ASSEZ", f"{C} top: 620px; font-size: 80px; color: #fff;", 32.31),
        lab("s6", "d", "BONNE SÉRIE", "left: 190px; top: 780px; font-size: 110px;", 33.69, white=True))),
    ("s7", "curl", 34.55, 39.50, "whip", *acc(
        tag("s7", "a", "ET TOI", f"{C} top: 220px; font-size: 100px; color: #fff;", 34.90),
        lab("s7", "b", "COMBIEN DE REPOS ?", "left: 90px; top: 380px; font-size: 82px;", 35.77),
        tag("s7", "c", "30 S · 1 MIN · PLUS", f"{C} top: 620px; font-size: 78px; color: #fff;", 37.69))),
    ("s8", "fin", 39.50, D, "flash", *acc(
        ('<div id="s8-end"><div class="tag" id="s8-ab">ABONNE-TOI</div><div class="tag" id="s8-nv">UN CONSEIL CHAQUE JOUR</div>'
         '<img id="s8-logo" src="assets/brand/icon-512.png" alt="CaliBodi" /><div class="big" id="s8-name">CaliBodi</div>'
         '<div class="lab" id="s8-url">calibodi.com</div><div class="tag" id="s8-st">Play Store · App Store</div></div>',
         "#s8-end { position: absolute; inset: 0; }"
         "#s8-ab { left: 0; width: 1080px; top: 190px; text-align: center; font-size: 84px; color: #fff; }"
         "#s8-nv { left: 0; width: 1080px; top: 300px; text-align: center; font-size: 52px; color: #fff; }"
         "#s8-logo { position: absolute; left: 400px; top: 410px; width: 280px; height: 280px; border-radius: 62px; box-shadow: 0 20px 50px rgba(0,0,0,.5); }"
         "#s8-name { left: 0; width: 1080px; top: 720px; text-align: center; font-size: 150px; color: #fff; text-shadow: 0 16px 50px rgba(0,0,0,.7); }"
         "#s8-url { left: 230px; top: 880px; font-size: 100px; }"
         "#s8-st { left: 0; width: 1080px; top: 1015px; text-align: center; font-size: 56px; color: #fff; }",
         'tl.fromTo("#s8-ab",{y:50,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(39.84));'
         'tl.fromTo("#s8-nv",{y:50,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(40.50));'
         'tl.fromTo("#s8-logo",{scale:0,rotation:-40},{scale:1,rotation:0,duration:.45,ease:"back.out(2.6)"},at(41.87));'
         'tl.fromTo("#s8-name",{scale:2.4,opacity:0},{scale:1,opacity:1,duration:.26,ease:"power4.out"},at(42.64));'
         'tl.fromTo("#s8-url",{scale:2.4,opacity:0,rotation:-6},{scale:1,opacity:1,rotation:-3,duration:.24,ease:"power4.out"},at(43.30));'
         'tl.fromTo("#s8-st",{y:40,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(44.00));'))),
]
PUNCH = [(1.70, 1.09), (5.38, 1.07), (9.63, 1.07), (16.60, 1.09), (24.05, 1.09), (30.96, 1.06), (35.77, 1.06), (42.64, 1.05)]
SHAKE = [16.60]
POSES = [(0.20, "curieux"), (4.30, "choc"), (8.00, "sceptique"), (14.60, "non"), (20.10, "explique"), (29.30, "pouce"),
         (34.90, "pointe"), (41.87, "app"), (43.30, "pouce")]
KW = {"séries", "repos", "30", "60", "secondes", "trop", "vite", "transpirer", "progression", "répétitions", "méta-analyse",
      "muscle", "chrono", "série", "minute", "calibodi", "calibodicom"}
CHAPTERS = [0.0, 14.51, 29.23]
