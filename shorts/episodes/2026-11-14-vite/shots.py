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
# Shot list of « vite », read by build_v4.py. Global times in seconds (voice of 2026-11-12).
# Footage: the author's own clips (plate, empty plate, full / empty yoghurt), brand labels cropped out, original sound removed.
A = "#FF6B35"
def clk(sid, text, t, out=None):
    return big(sid, "t", text, f"{C} top: 330px; font-size: 330px; color: {A}; {SH}", t, out)
SHOTS = [
    ("s1", "plat1", 0.00, 2.98, None, *acc(
        tag("s1", "a", "IL EST", f"{C} top: 190px; font-size: 64px; color: #fff;", 0.19),
        clk("s1", "20:00", 0.37),
        lab("s1", "b", "MON PLAT", "left: 250px; top: 780px; font-size: 110px;", 2.34))),
    ("s2", "plat2", 2.98, 5.15, "whip", *acc(
        clk("s2", "20:05", 3.14),
        tag("s2", "a", "DÉJÀ", f"{C} top: 720px; font-size: 84px; color: #fff;", 4.27),
        lab("s2", "b", "FINI", "left: 380px; top: 830px; font-size: 130px;", 5.00))),
    ("s3", "yaourt1", 5.15, 7.90, "flash", *acc(
        clk("s3", "20:06", 5.23),
        tag("s3", "a", "JE COMMENCE", f"{C} top: 720px; font-size: 70px; color: #fff;", 6.51),
        lab("s3", "b", "MON YAOURT", "left: 150px; top: 830px; font-size: 100px;", 7.01))),
    ("s4", "yaourt2", 7.90, 10.18, "whip", *acc(
        clk("s4", "20:07", 8.04),
        lab("s4", "a", "VIDE", "left: 330px; top: 800px; font-size: 150px;", 9.32))),
    ("s5", "lent1", 10.18, 13.86, "zoom", *acc(
        tag("s5", "a", "J'AI TOUT MANGÉ EN", f"{C} top: 250px; font-size: 56px; color: #fff;", 10.28),
        big("s5", "n", "7", f"left: 400px; top: 340px; font-size: 400px; color: {A}; {SH}", 11.00),
        lab("s5", "m", "MINUTES", "left: 250px; top: 760px; font-size: 110px;", 11.27, white=True),
        lab("s5", "p", "LE PROBLÈME", "left: 140px; top: 960px; font-size: 90px;", 12.93))),
    ("s6", "lent2", 13.86, 17.83, "flash", *acc(
        tag("s6", "a", "TROP VITE", f"{C} top: 250px; font-size: 100px; color: #fff;", 14.19),
        lab("s6", "b", "CERVEAU", "left: 250px; top: 400px; font-size: 130px;", 15.33),
        lab("s6", "c", "RASSASIÉ ?", "left: 200px; top: 600px; font-size: 110px;", 16.94, white=True))),
    ("s7", "lent3", 17.83, 21.21, "whip", *acc(
        tag("s7", "a", "ET TOI", f"{C} top: 250px; font-size: 100px; color: #fff;", 17.98),
        lab("s7", "b", "COMBIEN DE TEMPS", "left: 100px; top: 400px; font-size: 72px;", 18.54),
        tag("s7", "c", "POUR MANGER ?", f"{C} top: 560px; font-size: 76px; color: #fff;", 19.15),
        lab("s7", "d", "COMMENTAIRE", "left: 120px; top: 720px; font-size: 90px;", 20.30, white=True))),
    ("s8", "fin", 21.21, D, "flash", *acc(
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
         'tl.fromTo("#s8-ab",{y:50,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(21.36));'
         'tl.fromTo("#s8-nv",{y:50,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(22.00));'
         'tl.fromTo("#s8-logo",{scale:0,rotation:-40},{scale:1,rotation:0,duration:.45,ease:"back.out(2.6)"},at(22.60));'
         'tl.fromTo("#s8-name",{scale:2.4,opacity:0},{scale:1,opacity:1,duration:.26,ease:"power4.out"},at(23.20));'
         'tl.fromTo("#s8-url",{scale:2.4,opacity:0,rotation:-6},{scale:1,opacity:1,rotation:-3,duration:.24,ease:"power4.out"},at(23.96));'
         'tl.fromTo("#s8-st",{y:40,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(24.70));'))),
]
PUNCH = [(0.37, 1.07), (3.14, 1.07), (5.23, 1.07), (8.04, 1.07), (11.00, 1.09), (15.33, 1.06), (18.54, 1.05), (23.20, 1.05)]
SHAKE = [11.00]
POSES = [(0.20, "curieux"), (3.00, "choc"), (5.20, "pointe"), (7.95, "sceptique"), (10.20, "choc"), (13.90, "non"),
         (17.90, "pointe"), (22.60, "app"), (24.00, "pouce")]
KW = {"vingt", "heures", "plat", "fini", "yaourt", "vide", "minutes", "problème", "vite", "cerveau", "rassasié", "combien", "temps",
      "commentaire", "calibodi", "calibodicom", "7"}
CHAPTERS = [0.0, 10.18, 17.83]
