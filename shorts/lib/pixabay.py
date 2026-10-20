#!/usr/bin/env python3
"""Search and download free stock photos or videos from Pixabay into an episode, with a rights ledger.

usage: pixabay.py <episode_dir> <photo|video> "<query>" [count]
       pixabay.py <episode_dir> <photo|video> id:<pixabay id>

Reads the key from PIXABAY_API_KEY (never put it in the code). Files land in <episode>/assets/stock/ and every
download is recorded in <episode>/assets/stock/credits.json (source page, author, licence) so each medium in a
video can be traced back to its rights. Pixabay Content License: commercial use allowed, no attribution
required; still avoid recognisable people, brands and logos in a promotional context.
Photos come at 1280 px max through the standard API: fine for blurred or framed backgrounds, not full screen.
"""
import json
import os
import sys
import urllib.parse
import urllib.request

EP, kind, query = os.path.abspath(sys.argv[1]), sys.argv[2], sys.argv[3]
count = int(sys.argv[4]) if len(sys.argv) > 4 else 3
key = os.environ["PIXABAY_API_KEY"]
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) CaliBodiShorts/1.0"}  # Cloudflare rejects Python's default agent


def fetch(u):
    with urllib.request.urlopen(urllib.request.Request(u, headers=UA)) as r:
        return r.read()


out = os.path.join(EP, "assets", "stock")
os.makedirs(out, exist_ok=True)

params = {"key": key, "q": query, "lang": "fr", "safesearch": "true", "per_page": max(3, min(200, count * 4))}
if query.startswith("id:"):  # a specific medium chosen from a contact sheet
    params = {"key": key, "id": query[3:]}
if kind == "photo":
    params.update({"image_type": "photo", "orientation": "vertical"})
    url = "https://pixabay.com/api/?" + urllib.parse.urlencode(params)
else:
    url = "https://pixabay.com/api/videos/?" + urllib.parse.urlencode(params)
hits = json.loads(fetch(url))["hits"]
if kind == "video":  # prefer portrait clips for TikTok, then the longest ones
    hits.sort(key=lambda h: (h["videos"]["medium"]["height"] < h["videos"]["medium"]["width"], -h["duration"]))

ledger_path = os.path.join(out, "credits.json")
ledger = json.load(open(ledger_path)) if os.path.exists(ledger_path) else []
for h in hits[:count]:
    if kind == "photo":
        src, ext = h["largeImageURL"], ".jpg"
    else:
        # smallest rendition that still covers a 1080x1920 frame (4K is ~10x heavier for nothing)
        rends = [r for r in h["videos"].values() if r.get("url")]
        good = [r for r in rends if min(r["width"], r["height"]) >= 1080]
        v = min(good, key=lambda r: r["width"] * r["height"]) if good else max(rends, key=lambda r: r["width"] * r["height"])
        src, ext = v["url"], ".mp4"
    name = f"pixabay-{kind}-{h['id']}{ext}"
    path = os.path.join(out, name)
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        data = fetch(src)  # fetch first, so a failed download never leaves an empty file behind
        open(path, "wb").write(data)
    if not any(e["file"] == name for e in ledger):
        ledger.append({"file": name, "source": h["pageURL"], "author": h.get("user"), "tags": h.get("tags"),
                       "query": query, "licence": "Pixabay Content License (https://pixabay.com/service/license-summary/)"})
    print(f"{name}  ·  {h.get('tags')}  ·  {h['pageURL']}")
json.dump(ledger, open(ledger_path, "w"), ensure_ascii=False, indent=1)
print(f"{min(count, len(hits))} {kind}(s) saved in {out} · ledger: {ledger_path}")
