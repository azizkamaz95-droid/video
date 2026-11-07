# vertical cuts of the stock clips: name, pixabay id, source start, length, horizontal centre (0-1), slow-down factor
import subprocess, sys, os
from concurrent.futures import ThreadPoolExecutor
CUTS = [("verse", 71900, 14.0, 4.4, .5, 1), ("bouteille", 34684, 8.0, 2.8, .5, 1), ("vagues", 192107, 2.0, 3.4, .5, 1),
        ("plage", 334716, 3.0, 5.8, .5, 1), ("rocher", 213132, 2.0, 2.4, .5, 1), ("grotte", 221868, 2.0, 4.6, .5, 1),
        ("coucher", 217850, 2.0, 2.3, .5, 1), ("concombre", 14129, 1.0, 3.2, .5, 1), ("globe", 29481, 1.0, 5.4, .5, 1),
        ("cascade", 228847, 1.0, 3.4, .5, 1), ("neon", 73798, 3.0, 3.4, .5, 1), ("gouttes", 33313, 4.0, 3.0, .5, 1),
        ("desert", 168788, 2.0, 4.0, .85, 1), ("lac", 23009, 12.0, 4.3, .5, 1), ("cote", 302182, 2.0, 2.9, .5, 1),
        ("ressac", 386307, 1.0, 2.9, .5, 1), ("fin", 3328, 17.0, 7.4, .5, 1)]
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
