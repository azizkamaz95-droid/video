#!/usr/bin/env python3
"""Assemble index.html + the fx overlay sub-composition from timeline.json."""
import json
import os

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
tl = json.load(open(os.path.join(PROJECT, "timeline.json")))
TOTAL = tl["total"]

WIPES = [
    # (boundary, color, number, label)
    (16.5, "#FF6B35", "01", "sport."),
    (25.0, "#00FF87", "02", "nutrition."),
    (35.0, "#BF5AF2", "03", "récup."),
    (41.5, "#00D4FF", "04", "hydratation."),
]
FLASHES = [11.0, 46.5, 54.5]


def font_faces(indent):
    pad = " " * indent
    rows = [f'{pad}@font-face{{font-family:"Inter";font-weight:{w};font-style:normal;font-display:block;src:url("assets/fonts/Inter-{w}.woff2") format("woff2");}}' for w in (400, 500, 600, 700, 800, 900)]
    rows += [f'{pad}@font-face{{font-family:"IBM Plex Mono";font-weight:{w};font-style:normal;font-display:block;src:url("assets/fonts/IBMPlexMono-{w}.woff2") format("woff2");}}' for w in (500, 600)]
    return "\n".join(rows)


# ---------- fx overlay sub-composition (wipes, flashes, vignette, grain) ----------
wipe_dom, wipe_js = [], []
for i, (b, color, num, label) in enumerate(WIPES):
    s = round(b - 0.42, 3)
    wipe_dom.append(
        f'      <div id="fx-wipe-{i}" class="fx-wipe" data-layout-allow-overflow>\n'
        f'        <div id="fx-wipe-{i}-trail" class="fx-trail"></div>\n'
        f'        <div id="fx-wipe-{i}-panel" class="fx-panel" style="background:{color}">\n'
        f'          <span class="fx-num">{num} / 04</span><span id="fx-wipe-{i}-label" class="fx-label">{label}</span>\n'
        f'        </div>\n'
        f'      </div>'
    )
    wipe_js.append(
        f'      tl.fromTo("#fx-wipe-{i}-trail", {{ xPercent: -101 }}, {{ xPercent: 0, duration: 0.34, ease: "power3.in" }}, {s});\n'
        f'      tl.fromTo("#fx-wipe-{i}-panel", {{ xPercent: -101 }}, {{ xPercent: 0, duration: 0.36, ease: "power3.in" }}, {round(s + 0.04, 3)});\n'
        f'      tl.set("#fx-wipe-{i}-trail", {{ xPercent: 101 }}, {round(s + 0.42, 3)});\n'
        f'      tl.to("#fx-wipe-{i}-panel", {{ xPercent: 101, duration: 0.44, ease: "power3.out" }}, {round(b + 0.06, 3)});\n'
        f'      tl.fromTo("#fx-wipe-{i}-label", {{ x: -160 }}, {{ x: 140, duration: 0.95, ease: "none" }}, {s});'
    )

flash_dom, flash_js = [], []
for i, t in enumerate(FLASHES):
    flash_dom.append(f'      <div id="fx-flash-{i}" class="fx-flash"></div>')
    flash_js.append(f'      tl.fromTo("#fx-flash-{i}", {{ opacity: 0.8 }}, {{ opacity: 0, duration: 0.45, ease: "power2.out", immediateRender: false }}, {t});')

overlay = f"""<template id="fx-overlay-template">
  <style>
{font_faces(4)}
    #root {{ position: absolute; inset: 0; overflow: hidden; pointer-events: none; }}
    .fx-wipe {{ position: absolute; inset: 0; overflow: hidden; }}
    .fx-trail {{ position: absolute; inset: 0; background: #0A0A0F; }}
    .fx-panel {{ position: absolute; inset: 0; display: flex; flex-direction: column; justify-content: center; padding-left: 106px; }}
    .fx-num {{ display: block; font-family: "IBM Plex Mono", monospace; font-weight: 600; font-size: 22px; letter-spacing: 0.14em; color: rgba(10,10,15,0.7); margin-bottom: 18px; }}
    .fx-label {{ display: block; font-family: "Inter", sans-serif; font-weight: 900; font-size: 260px; line-height: 0.88; letter-spacing: -0.05em; color: #0A0A0F; white-space: nowrap; }}
    .fx-flash {{ position: absolute; inset: 0; background: #ffffff; opacity: 0; }}
    #fx-vignette {{ position: absolute; inset: 0; background: radial-gradient(120% 95% at 50% 46%, rgba(0,0,0,0) 58%, rgba(0,0,0,0.55) 100%); }}
    #fx-grain {{ position: absolute; inset: -40px; background-image: url("assets/fx/grain.png"); background-size: 512px 512px; opacity: 0.075; mix-blend-mode: screen; }}
  </style>
  <div id="root" data-composition-id="fx-overlay" data-width="1920" data-height="1080" data-duration="{TOTAL}">
{chr(10).join(wipe_dom)}
{chr(10).join(flash_dom)}
      <div id="fx-vignette"></div>
      <div id="fx-grain"></div>
  </div>
  <script>
    (function () {{
      const tl = gsap.timeline({{ paused: true }});
{chr(10).join(wipe_js)}
{chr(10).join(flash_js)}
      tl.fromTo("#fx-grain", {{ backgroundPosition: "0px 0px" }}, {{ backgroundPosition: "{int(TOTAL * 12 * 173)}px {int(TOTAL * 12 * 97)}px", duration: {TOTAL}, ease: "steps({int(TOTAL * 12)})" }}, 0);
      window.__timelines["fx-overlay"] = tl;
    }})();
  </script>
</template>
"""
open(os.path.join(PROJECT, "compositions", "fx-overlay.html"), "w").write(overlay)

# ---------- index.html ----------
slots = [
    f'      <div id="el-{s["id"]}" data-composition-id="{s["id"]}" data-composition-src="compositions/frames/{s["id"]}.html"'
    f' data-start="{s["start"]}" data-duration="{s["duration"]}" data-track-index="1" data-width="1920" data-height="1080"></div>'
    for s in tl["scenes"]
]
voices = [
    f'      <audio id="vo-{s["frame"]:02d}" src="{s["vo_file"]}" data-audio-group="voiceover" data-start="{s["vo_start"]}"'
    f' data-duration="{s["vo_duration"]}" data-track-index="10" data-volume="1"></audio>'
    for s in tl["scenes"]
]
bed = os.path.exists(os.path.join(PROJECT, "assets", "audio", "bed.wav"))
bed_tag = (
    f'      <audio id="el-bgm" src="assets/audio/bed.wav" data-start="0" data-duration="{TOTAL}" data-track-index="11" data-volume="1"></audio>'
    if bed else "      <!-- music bed: run scripts/audio_bed.py -->"
)

html = f"""<!doctype html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <title>CaliBodi — promo</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
{font_faces(6)}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1920px; height: 1080px; overflow: hidden; background: #0A0A0F; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: #0A0A0F; font-family: "Inter", sans-serif; }}
      [data-composition-id="main"] > div[data-composition-src] {{ position: absolute; inset: 0; }}
      #base {{ position: absolute; inset: 0; background: #0A0A0F; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1920" data-height="1080">
      <div id="base" class="clip" data-start="0" data-duration="{TOTAL}" data-track-index="0"></div>
{chr(10).join(slots)}
      <div id="el-fx-overlay" data-composition-id="fx-overlay" data-composition-src="compositions/fx-overlay.html" data-start="0" data-duration="{TOTAL}" data-track-index="5" data-width="1920" data-height="1080"></div>
{chr(10).join(voices)}
{bed_tag}
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""
open(os.path.join(PROJECT, "index.html"), "w").write(html)
print("index.html + compositions/fx-overlay.html written", "(with bed)" if bed else "(no bed yet)")
