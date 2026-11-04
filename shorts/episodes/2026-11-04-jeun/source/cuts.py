# vertical cuts of the stock clips: name, pixabay id, source start, length, horizontal centre (0-1), slow-down factor
import subprocess, sys, os
from concurrent.futures import ThreadPoolExecutor
CUTS = [("reveil", 16346, 12.0, 3.9, .5, 1), ("ciel", 8206, 2.0, 4.2, .5, 1), ("plage2", 199000, 12.0, 4.6, .25, 1),
        ("plat", 200129, 1.0, 5.2, .5, 1), ("lac", 23009, 2.0, 3.0, .5, 1), ("livres", 21941, 2.0, 5.6, .5, 1),
        ("micro", 86259, 2.0, 2.4, .5, 1), ("neon", 73798, 3.0, 4.6, .5, 1), ("cafe", 236256, 0.0, 4.6, .5, 1),
        ("plage", 199000, 5.0, 3.0, .25, 1), ("aube", 355486, 3.0, 5.6, .5, 1), ("fraises", 148288, 2.0, 3.2, .5, 1),
        ("alarme", 131994, 1.0, 4.2, .5, 1), ("plat2", 11659, 2.0, 3.2, .5, 1), ("lac2", 23009, 8.0, 2.8, .5, 1),
        ("fin", 225661, 3.0, 7.8, .5, 1)]
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
