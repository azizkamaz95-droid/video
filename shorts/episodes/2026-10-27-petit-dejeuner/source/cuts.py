# vertical cuts of the stock clips: name, pixabay id, source start, length, horizontal centre (0-1)
import subprocess, sys, os
from concurrent.futures import ThreadPoolExecutor
CUTS = [("crepes", 278389, 1.0, 4.2, .5), ("reveil", 16346, 4.0, 2.6, .5), ("eclair", 283428, 10.8, 3.9, .5),
        ("docs", 212508, 3.0, 5.0, .45), ("oeuf", 290890, 2.0, 3.8, .45), ("balance", 220024, 2.0, 3.8, .5),
        ("archives", 349087, 2.0, 3.3, .55), ("pate", 200017, 1.0, 4.7, .5), ("expresso", 46989, 4.0, 2.5, .5),
        ("orage", 283426, 1.0, 3.3, .5), ("ville", 58151, 3.0, 4.2, .5), ("moniteur", 145344, 1.0, 3.6, .5),
        ("ecg", 8449, 0.5, 3.3, None), ("montre", 122810, 2.0, 2.5, .5), ("clope", 139464, 0.5, 3.4, .6),
        ("burger", 78962, 3.0, 2.1, .4), ("tasse", 38059, 3.0, 2.4, .55), ("livre", 41121, 1.0, 5.5, .5),
        ("gym", 20422, 1.0, 3.5, .5), ("pompes", 39475, 2.0, 3.3, .5), ("cafe", 3158, 5.0, 4.1, .55),
        ("canal", 230248, 5.0, 7.4, .5), ("skyline", 80724, 2.0, 7.6, .5)]
# no brand marks on screen: zoom past the monitor's logo, blur the watch and clock-radio names
EXTRA = {"moniteur": "scale=-2:2800:flags=lanczos,crop=1080:1920:(iw-1080)*.45:0,fps=30,format=yuv420p",
         "montre": None, "reveil": None}
POST = {"montre": "delogo=x=440:y=640:w=420:h=130,delogo=x=420:y=1000:w=420:h=160", "reveil": "delogo=x=870:y=580:w=205:h=90"}
os.makedirs("assets/clips", exist_ok=True)
def cut(c):
    name, pid, ss, t, cx = c
    vf = f"scale=-2:1920:flags=lanczos,crop=1080:1920:(iw-1080)*{cx}:0,fps=30,format=yuv420p"
    if cx is None:  # letterbox a wide shot on black (a line that must cross the whole frame)
        vf = "scale=1700:-2:flags=lanczos,crop=1080:ih,pad=1080:1920:0:(1920-ih)/2:black,fps=30,format=yuv420p"
    if EXTRA.get(name):
        vf = EXTRA[name]
    if name in POST:
        vf += "," + POST[name]
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(ss), "-i", f"assets/stock/pixabay-video-{pid}.mp4", "-t", str(t), "-an",
                    "-vf", vf, "-c:v", "libx264", "-crf", "19", "-preset", "medium", f"assets/clips/{name}.mp4"], check=True)
    return name
only = set(sys.argv[1:])
with ThreadPoolExecutor(4) as ex:
    for n in ex.map(cut, [c for c in CUTS if not only or c[0] in only]):
        print(n, end=" ", flush=True)
