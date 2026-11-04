# vertical cuts of the stock clips: name, pixabay id, source start, length, horizontal centre (0-1), slow-down factor
import subprocess, sys, os
from concurrent.futures import ThreadPoolExecutor
CUTS = [("bureau", 377388, 1.0, 4.0, .5, 1), ("horloge", 7549, 1.0, 2.1, .5, 1), ("spirale", 207866, 2.0, 5.3, .5, 1),
        ("clavier", 43559, 2.0, 4.2, .5, 1), ("dos", 270432, 1.0, 6.8, .5, 1), ("pieds", 3171, 1.0, 5.3, .5, 1),
        ("bureau2", 377388, 5.0, 4.2, .5, 1), ("chaises", 2709, 2.0, 4.5, .5, 1), ("gratte", 45985, 0.5, 5.5, .5, 1),
        ("velo", 1351, 2.0, 5.8, .5, 1), ("meca", 34855, 1.0, 2.3, .5, 1), ("salon", 254027, 1.0, 5.1, .5, 1),
        ("foule", 21782, 5.0, 4.8, .5, 1), ("escalier", 239276, 2.0, 3.0, .5, 1), ("velo2", 107859, 2.0, 4.0, .5, 1),
        ("plage", 4722, 2.0, 4.8, .5, 1), ("coucher", 339317, 0.0, 7.6, .5, 1.45), ("fin", 7713, 2.0, 7.8, .5, 1)]
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
