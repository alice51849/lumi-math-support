#!/usr/bin/env python3
# Generate hero artwork for the Lumi Math Planet support site — clay/soft-vinyl + golden starlight, math motifs.
import os, json, base64, urllib.request

def load_key():
    k = os.environ.get("OPENAI_API_KEY", "").strip()
    if k: return k
    for p in ("~/.lumi_openai_key", "~/.openai_key"):
        fp = os.path.expanduser(p)
        if os.path.exists(fp): return open(fp).read().strip()
    return ""

API_KEY = load_key()
ROOT = os.path.dirname(os.path.abspath(__file__))

JOBS = [
    {
        "out": "hero-bg.png", "size": "1536x1024", "background": "opaque",
        "prompt": (
            "A dreamy cosmic background illustration for a children's MATH learning brand, in soft lavender and cosmic "
            "violet gradients fading to a paler center, gentle aurora ribbons in pink and gold, scattered tiny twinkling "
            "stars and delicate golden sparkles. Floating very softly and subtly in the distance: a few faint glowing "
            "numbers (1, 2, 3) and small plus, minus and multiply signs, plus a couple of soft pastel geometric shapes "
            "(triangle, circle) and a small planet with a thin golden ring near the edges. Lots of calm open empty space "
            "in the middle for text. Soft bokeh, premium clay / soft-vinyl dreamy texture, ethereal cinematic lighting, "
            "no characters, no readable text blocks, elegant and high-end, wide landscape."
        ),
    },
    {
        "out": "friends.png", "size": "1536x1024", "background": "transparent",
        "prompt": (
            "Three tiny adorable cosmic MATH friends as a children's brand illustration, evenly spaced: (1) a cute glowing "
            "golden number-block cube showing a friendly '1' with a little smiling face, (2) a small pastel planet with a "
            "golden ring and a happy face, (3) a cute soft geometric crystal shaped like a smiling triangle/gem. Soft "
            "premium clay / soft-vinyl designer-toy texture, gentle golden rim light, macaron pastel colors with gold "
            "accents, glassy highlights, floating with tiny sparkles around them, fully transparent background, soft "
            "cinematic lighting, no text, premium and charming."
        ),
    },
]

def gen(job):
    body = {"model": "gpt-image-1", "prompt": job["prompt"], "size": job["size"],
            "quality": "high", "background": job["background"], "n": 1}
    req = urllib.request.Request("https://api.openai.com/v1/images/generations",
        data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=420) as r:
        resp = json.load(r)
    img = base64.b64decode(resp["data"][0]["b64_json"])
    open(os.path.join(ROOT, job["out"]), "wb").write(img)
    print("saved ->", job["out"], len(img), "bytes")

if not API_KEY:
    print("NO_KEY")
else:
    for j in JOBS:
        try: gen(j)
        except Exception as e: print("FAIL", j["out"], repr(e)[:200])
