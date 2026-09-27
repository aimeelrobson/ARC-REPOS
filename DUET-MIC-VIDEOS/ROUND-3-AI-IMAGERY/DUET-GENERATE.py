#!/usr/bin/env python3
"""DUET Round 3: generate test images via Gemini (Nano Banana) image model.
The API key is injected by the environment proxy; none is sent here.
Usage: python3 DUET-GENERATE.py [SET-NUMBER ...] [--aspect 4:5] [--model MODEL]
"""
import base64, json, sys, argparse, urllib.request, pathlib, mimetypes

HERE = pathlib.Path(__file__).parent
PRODUCT = HERE / "PRODUCT-PHOTOS" / "KIT-BLUSH.png"
REFS = HERE / "AESTHETIC-REFERENCES"
OUT = HERE / "OUTPUTS"

PRODUCT_NOTE = (
    "IMAGE 1 is the exact product: the DUET Blush wireless clip-on mic kit. Reproduce it faithfully: "
    "thumb-sized rounded-rectangle soft-pink body, rounded-square white foam head on top, large square "
    "front button, tiny green LED dot above the button, small side clip wings; the matching small pink "
    "USB-C receiver with a silver USB-C plug; optional fluffy pink faux-fur windshields. Keep proportions, "
    "colours and shapes exactly as in IMAGE 1. No logos or text on the product. "
    "IMAGE 2 is a mood reference for set, palette and lighting only; do not copy its products, people or text."
)
STYLE = (
    "Style: Pastel Maximalism meets editorial surrealism, Barbiecore/coquette, retro-whimsy. Chic, witty, "
    "a little absurd, premium not kitsch. Palette: bubblegum pink, mint, lilac, butter yellow, tangerine, "
    "brass accents. Hard direct flash / direct sun, crisp graphic shadows, saturated colour, sharp focus, "
    "high-end commercial photography. No alcohol, no visible text, words, logos or fake branding anywhere. "
    "Keep the pink mic clearly visible as the hero."
)

SETS = {
    1: ("DUET-R3-SET-1-PEOPLE-TEST", "REF-07.jpg",
        "Two friends, characters not models, fully dressed and sitting side by side in a pink tiled bathtub "
        "overflowing with white bubbles. One wears a lilac blazer and pearls, the other a butter-yellow knit. "
        "Each has a blush-pink DUET mic clipped to their collar, clearly visible. Deadpan expressions, looking "
        "at a smartphone mounted on a small pink tripod that is filming them. Mint green tiled walls, a pink "
        "rotary wall phone with a coiled cord. Surreal, funny, 'two voices' energy."),
    2: ("DUET-R3-SET-2-PRODUCT-IN-SETTING-TEST", "REF-06.jpg",
        "Still life: a pair of blush-pink DUET mics and the pink USB-C receiver on pink gridded tiles. "
        "A mint transistor radio and a brass twin-bell alarm clock behind, scattered popcorn, and a pink "
        "coiled rotary-phone cord playfully curling around the two mics. Mics sharp and prominent in the "
        "foreground, uncluttered around them."),
    3: ("DUET-R3-SET-3-PRODUCT-ALONE-TEST", "REF-10.jpg",
        "Hero product shot: a single blush-pink DUET mic standing upright on top of a sculptural wavy "
        "tangerine plinth, on a pink and orange checkerboard floor, against a smooth pink-to-tangerine "
        "gradient backdrop. A fresh grapefruit slice beside the plinth. Hard sun casting a long crisp "
        "graphic shadow. Minimal, sculptural, iconic."),
}

def part(path):
    mime = mimetypes.guess_type(path)[0] or "image/png"
    return {"inline_data": {"mime_type": mime, "data": base64.b64encode(path.read_bytes()).decode()}}

def generate(n, aspect, model):
    name, ref, scene = SETS[n]
    body = {
        "contents": [{"parts": [part(PRODUCT), part(REFS / ref),
                                {"text": f"{PRODUCT_NOTE}\n\nScene: {scene}\n\n{STYLE}"}]}],
        "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": aspect}},
    }
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    req = urllib.request.Request(url, json.dumps(body).encode(), {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        data = json.load(r)
    for p in data["candidates"][0]["content"]["parts"]:
        blob = p.get("inlineData") or p.get("inline_data")
        if blob:
            ext = ".PNG" if "png" in blob.get("mimeType", blob.get("mime_type", "")) else ".JPG"
            out = OUT / f"{name}-{aspect.replace(':', 'X')}{ext}"
            out.write_bytes(base64.b64decode(blob["data"]))
            print("saved", out)
            return
    print("no image returned for set", n, json.dumps(data)[:800])

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("sets", nargs="*", type=int, default=[1, 2, 3])
    ap.add_argument("--aspect", default="4:5")
    ap.add_argument("--model", default="gemini-3-pro-image")
    a = ap.parse_args()
    OUT.mkdir(exist_ok=True)
    for n in a.sets:
        generate(n, a.aspect, a.model)
