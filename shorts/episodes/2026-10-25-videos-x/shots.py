# Shot list of the full video, read by build_v4.py (exec'd after its defaults). Global times in seconds.
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


SHOTS = SHOTS[:3] + [
    ("s4", "mains", 8.55, 12.10, "flash", *acc(lab("s4", "f", "FAIT N°1", "left: 70px; top: 230px; font-size: 120px;", 8.75, out=9.8))),
    # « L'OMS reconnaît le trouble du comportement sexuel compulsif. »
    ("s5", "archives", 12.10, 15.55, "whip", *acc(
        lab("s5", "o", "OMS", "left: 70px; top: 230px; font-size: 150px;", 12.19),
        tag("s5", "t", "trouble du comportement<br>sexuel compulsif", "left: 70px; top: 420px; font-size: 64px; color: #fff; white-space: normal; line-height: 1.05;", 13.19),
        src("s5", "OMS, classification CIM-11 (en vigueur depuis 2022)", 12.4))),
    # « Dans une enquête américaine, environ un homme sur dix… »
    ("s6", "ville", 15.55, 19.45, "zoom", *acc(
        (row("s6", man, 10, 0, 96, 330), "", 'tl.fromTo("#s6 .ic",{opacity:0,y:40},{opacity:1,y:0,duration:.2,ease:"back.out(2)",stagger:.04},at(16.06));'),
        ("", "", 'tl.fromTo("#s6-h0",{opacity:0,scale:.3,transformOrigin:"50% 50%"},{opacity:1,scale:1.15,duration:.25,ease:"back.out(3)"},at(17.67));'),
        big("s6", "n", "1 SUR 10", "left: 0; width: 1080px; top: 480px; text-align: center; font-size: 190px; color: #FFC93C; text-shadow: 0 20px 60px rgba(0,0,0,.6);", 17.83),
        src("s6", "Dickenson et al., JAMA Network Open, 2018", 16.0))),
    # « …disait avoir du mal à contrôler ses envies sexuelles. Au point d'en souffrir. »
    ("s7", "mannequin", 19.45, 23.25, "whip", *acc(
        lab("s7", "a", "DU MAL À SE CONTRÔLER", "left: 60px; top: 260px; font-size: 66px;", 19.57),
        lab("s7", "b", "AU POINT D'EN SOUFFRIR", "left: 60px; top: 380px; font-size: 66px;", 21.67, white=True))),
    # « Fait numéro deux. Ça peut toucher ton couple. »
    ("s8", "alliances", 23.25, 25.85, "flash", *acc(
        lab("s8", "f", "FAIT N°2", "left: 70px; top: 230px; font-size: 120px;", 23.34, out=24.3),
        big("s8", "c", "TON COUPLE", "left: 0; width: 1080px; top: 330px; text-align: center; font-size: 150px; color: #fff; text-shadow: 0 16px 50px rgba(0,0,0,.7);", 24.94))),
    # « Des chercheurs ont rassemblé les études sur la masturbation en solo. »
    ("s9", "livre", 25.85, 29.15, "zoom", *acc(
        big("s9", "n", "22", "left: 0; width: 1080px; top: 230px; text-align: center; font-size: 380px; color: #FFC93C; text-shadow: 0 20px 60px rgba(0,0,0,.6);", 26.55),
        tag("s9", "t", "ÉTUDES RASSEMBLÉES", "left: 0; width: 1080px; top: 600px; text-align: center; font-size: 72px; letter-spacing: .06em; color: #fff;", 26.95),
        src("s9", "revue systématique, Healthcare, 2024 (22 études)", 26.0))),
    # « Chez les hommes, environ 7 études sur 10 trouvent le même lien : plus de masturbation, moins de satisfaction au lit. »
    ("s10", "chambre2", 29.15, 35.85, "whip", *acc(
        (row("s10", doc, 10, 0, 96, 300), "", 'tl.fromTo("#s10 .ic",{opacity:0,y:40},{opacity:1,y:0,duration:.2,ease:"back.out(2)",stagger:.04},at(29.94));'),
        ("", "", hi_js("s10", 7, 30.32, .07)),
        big("s10", "n", "7 SUR 10", "left: 0; width: 1080px; top: 440px; text-align: center; font-size: 170px; color: #FFC93C; text-shadow: 0 20px 60px rgba(0,0,0,.6);", 31.05, out=32.45),
        lab("s10", "p", "+ MASTURBATION", "left: 90px; top: 470px; font-size: 92px;", 32.57),
        lab("s10", "m", "− SATISFACTION", "left: 90px; top: 620px; font-size: 92px;", 34.02, white=True),
        src("s10", "revue systématique, Healthcare, 2024 · un lien, pas une preuve", 29.3))),
    # « Fait numéro trois. Celui que je t'ai promis. » (lightning on « trois »)
    ("s11", "orage", 35.85, 38.65, "flash", *acc(
        tag("s11", "k", "FAIT N°", "left: 0; width: 1080px; top: 250px; text-align: center; font-size: 110px; color: #fff;", 35.95),
        big("s11", "n", "3", "left: 0; width: 1080px; top: 330px; text-align: center; font-size: 640px; color: #FFC93C; text-shadow: 0 30px 90px rgba(0,0,0,.7);", 36.43))),
    # « Une étude a interrogé environ 2 000 hommes jeunes. »
    ("s12", "ville2", 38.65, 41.35, "zoom", *acc(
        big("s12", "n", "2 000", "left: 0; width: 1080px; top: 300px; text-align: center; font-size: 260px; color: #FFC93C; text-shadow: 0 20px 60px rgba(0,0,0,.6);", 40.15),
        tag("s12", "t", "HOMMES JEUNES", "left: 0; width: 1080px; top: 580px; text-align: center; font-size: 80px; letter-spacing: .06em; color: #fff;", 40.46),
        src("s12", "Jacobs et al., JMIR Public Health and Surveillance, 2021", 38.8))),
    # « Le plus lié aux problèmes d'érection, ce n'était pas la masturbation. »
    ("s13", "clavier", 41.35, 45.95, "whip", *acc(
        tag("s13", "q", "TROUBLES DE<br>L'ÉRECTION ?", "left: 70px; top: 260px; font-size: 110px; color: #fff; white-space: normal; line-height: .95;", 42.13),
        lab("s13", "m", "PAS LA MASTURBATION", "left: 60px; top: 560px; font-size: 70px;", 44.38, white=True))),
    # « C'était une consommation de vidéos X incontrôlée. »
    ("s14", "scroll2", 45.95, 49.25, "flash", *acc(
        big("s14", "x", "X", "left: 0; width: 1080px; top: 200px; text-align: center; font-size: 640px; color: #FFC93C; opacity: .92; text-shadow: 0 30px 80px rgba(0,0,0,.65);", 48.03),
        lab("s14", "i", "INCONTRÔLÉE", "left: 140px; top: 780px; font-size: 120px;", 48.17))),
    # « Attention : ce sont des liens. Pas des preuves. »
    ("s15", "chambre3", 49.25, 52.45, "zoom", *acc(
        ('<svg class="tri" id="s15-tri" viewBox="0 0 190 170"><path d="M95 10 L 182 160 L 8 160 Z" fill="#FFC93C" stroke="#141414" stroke-width="10" stroke-linejoin="round" /><path d="M95 60 V112" stroke="#141414" stroke-width="16" stroke-linecap="round" /><circle cx="95" cy="138" r="9" fill="#141414" /></svg>',
         "#s15-tri { position: absolute; left: 445px; top: 220px; width: 190px; height: 170px; }",
         'tl.fromTo("#s15-tri",{scale:0,rotation:-30},{scale:1,rotation:0,duration:.35,ease:"back.out(2.6)"},at(49.45));'),
        big("s15", "l", "LIEN ≠ PREUVE", "left: 0; width: 1080px; top: 440px; text-align: center; font-size: 130px; color: #fff; text-shadow: 0 16px 50px rgba(0,0,0,.7);", 50.88))),
    # « Mais si tu sens que tu perds le contrôle, parles-en à un médecin. »
    ("s16", "xray", 52.45, 56.20, "whip", *acc(
        lab("s16", "a", "PARLES-EN", "left: 70px; top: 260px; font-size: 130px;", 54.66),
        lab("s16", "b", "À UN MÉDECIN", "left: 70px; top: 420px; font-size: 110px;", 55.24, white=True))),
    # « Selon toi, les vidéos X, c'est un vrai problème chez les jeunes ? Réponds oui ou non. »
    ("s17", "mains2", 56.20, 60.65, "zoom", *acc(
        tag("s17", "q", "UN VRAI PROBLÈME<br>CHEZ LES JEUNES ?", "left: 0; width: 1080px; top: 250px; text-align: center; font-size: 84px; color: #fff; white-space: normal; line-height: 1;", 57.88),
        lab("s17", "y", "OUI", "left: 190px; top: 520px; font-size: 150px;", 59.89),
        lab("s17", "n", "NON", "left: 600px; top: 520px; font-size: 150px;", 60.08, white=True))),
    # « Partage cette vidéo à quelqu'un qui doit l'entendre. Et abonne-toi : une nouvelle vidéo chaque jour à 18h. »
    ("s18", "ville3", 60.65, 66.45, "whip", *acc(
        ('<div class="ic2" id="s18-ic"><svg viewBox="0 0 140 140"><path d="M14 120 C 20 70, 50 44, 104 44 M84 18 L 122 44 L 84 72" fill="none" stroke="#141414" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" /></svg></div>',
         "#s18-ic { position: absolute; left: 70px; top: 250px; width: 170px; height: 170px; border-radius: 50%; background: #fff; box-shadow: 0 14px 30px rgba(0,0,0,.4); }"
         "#s18-ic svg { position: absolute; left: 25px; top: 25px; width: 120px; height: 120px; overflow: visible; }",
         'tl.fromTo("#s18-ic",{scale:0,rotation:-40},{scale:1,rotation:0,duration:.35,ease:"back.out(2.4)"},at(60.85));'
         'tl.fromTo("#s18-ic",{opacity:1},{opacity:0,duration:.2,ease:"none",immediateRender:false},at(63.3));'),
        lab("s18", "p", "PARTAGE", "left: 270px; top: 270px; font-size: 120px;", 60.85, out=63.3),
        lab("s18", "a", "ABONNE-TOI", "left: 70px; top: 260px; font-size: 140px;", 63.52),
        big("s18", "h", "18H", "left: 0; width: 1080px; top: 470px; text-align: center; font-size: 300px; color: #FFC93C; text-shadow: 0 20px 60px rgba(0,0,0,.6);", 65.62),
        tag("s18", "j", "1 VIDÉO CHAQUE JOUR", "left: 0; width: 1080px; top: 780px; text-align: center; font-size: 70px; letter-spacing: .04em; color: #fff;", 64.41))),
    # « Pour suivre tes entraînements, ton sommeil et ton alimentation, découvre CaliBodi sur calibodi.com. »
    ("s19", "ville4", 66.45, D, "zoom", *acc(
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
         'tl.fromTo("#s19-p1",{y:1300,rotation:-30},{y:0,rotation:0,duration:.45,ease:"back.out(1.4)"},at(67.31));'
         'tl.fromTo("#s19-p2",{y:1300},{y:0,duration:.45,ease:"back.out(1.4)"},at(68.50));'
         'tl.fromTo("#s19-p3",{y:1300,rotation:30},{y:0,rotation:0,duration:.45,ease:"back.out(1.4)"},at(69.16));'
         'tl.fromTo(["#s19-p1","#s19-p2","#s19-p3"],{opacity:1,y:0},{opacity:0,y:-900,duration:.3,ease:"power3.in",immediateRender:false},at(70.0));'
         'tl.fromTo("#s19-end",{opacity:0},{opacity:1,duration:.1,ease:"none"},at(70.18));'
         'tl.fromTo("#s19-logo",{scale:0,rotation:-40},{scale:1,rotation:0,duration:.45,ease:"back.out(2.6)"},at(70.2));'
         'tl.fromTo("#s19-name",{scale:2.4,opacity:0},{scale:1,opacity:1,duration:.26,ease:"power4.out"},at(70.63));'
         'tl.fromTo("#s19-url",{scale:2.4,opacity:0,rotation:-6},{scale:1,opacity:1,rotation:-3,duration:.24,ease:"power4.out"},at(71.44));'
         'tl.fromTo("#s19-st",{y:40,opacity:0},{y:0,opacity:1,duration:.3,ease:"back.out(2)"},at(71.9));'),)),
]

PUNCH = PUNCH + [(12.19, 1.06), (17.83, 1.07), (21.67, 1.05), (23.34, 1.07), (24.94, 1.05), (26.55, 1.06), (31.05, 1.06),
                 (32.57, 1.05), (34.02, 1.05), (36.43, 1.10), (40.15, 1.06), (44.38, 1.06), (48.17, 1.08), (50.88, 1.06),
                 (54.66, 1.06), (59.89, 1.05), (60.85, 1.05), (63.52, 1.06), (65.62, 1.07), (70.63, 1.05), (71.44, 1.06)]
SHAKE = SHAKE + [36.43, 48.17]
POSES = POSES + [(12.19, "sceptique"), (15.73, "explique"), (17.67, "choc"), (19.57, "fatigue"), (23.34, "deux"), (24.38, "curieux"),
                 (25.91, "explique"), (30.32, "pointe"), (34.02, "non"), (35.95, "trois"), (37.23, "pointe"), (38.77, "explique"),
                 (44.38, "choc"), (46.12, "enerve"), (49.45, "sceptique"), (52.57, "explique"), (54.66, "pointe"), (56.35, "curieux"),
                 (59.52, "pointe"), (60.85, "pouce"), (63.52, "biceps"), (66.65, "app"), (70.18, "pouce")]
KW |= {"l'oms", "compulsif", "dix", "souffrir", "deux", "couple", "études", "sept", "masturbation", "satisfaction", "trois",
       "promis", "2", "000", "d'érection", "pas", "x", "incontrôlée", "liens", "preuves", "médecin", "oui", "non", "partage",
       "abonne-toi", "18h", "calibodi", "calibodicom"}
CHAPTERS = [0.0, 8.75, 23.34, 35.95]
