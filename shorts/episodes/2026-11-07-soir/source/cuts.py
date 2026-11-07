# vertical cuts of the stock clips: name, pixabay id, source start, length, horizontal centre (0-1), slow-down factor
import subprocess, sys, os
from concurrent.futures import ThreadPoolExecutor
CUTS = [("horloge", 176024, 3.0, 4.4, .5, 1), ("fenetre", 11722, 2.0, 3.3, .5, 1), ("ville", 343478, 3.0, 4.8, .5, 1),
        ("chrono", 47835, 0.0, 4.8, .5, 1), ("vapeur", 267, 2.0, 4.0, .5, 1), ("rue", 180386, 2.0, 4.1, .5, 1),
        ("ragout", 227137, 5.0, 4.8, .5, 1), ("minuteur", 7515, 1.0, 3.6, .5, 1), ("adn", 197931, 2.0, 3.7, .5, 1),
        ("legumes", 11604, 6.0, 3.9, .5, 1), ("synth", 134915, 3.0, 2.9, .5, 1), ("ragout2", 227137, 40.0, 2.0, .5, 1),
        ("nuit", 12126, 2.0, 3.2, .5, 1), ("sablier", 357743, 0.0, 3.9, .5, 1), ("assiette", 11659, 2.0, 4.4, .5, 1),
        ("ruelle", 3134, 0.5, 3.4, .5, 1), ("fin", 11722, 12.0, 4.4, .5, 1)]
os.makedirs("assets/clips", exist_ok=True)
def cut(c):
    name, pid, ss, t, cx, slow = c
    vf = f"scale=-2:1920:flags=lanczos,crop=1080:1920:(iw-1080)*{cx}:0,fps=30,setpts={slow}*PTS,format=yuv420p"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(ss), "-i", f"assets/stock/pixabay-video-{pid}.mp4", "-t", str(t), "-an",
                    "-vf", vf, "-c:v", "libx264", "-crf", "19", "-preset", "medium", f"assets/clips/{name}.mp4"], check=True)
    return name
only = set(sys.argv[1:])
with ThreadPoolExecutor(4) as ex:
    for n in ex.map(cut, [c for c in CUTS if not only or c[0] in only]):
        print(n, end=" ", flush=True)
