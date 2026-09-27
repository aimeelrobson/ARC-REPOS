"""DUET FILM grade: subtle grain + on-camera flash + retro tone. Deterministic (seeded) so every image matches."""
import sys, numpy as np
from PIL import Image, ImageFilter

def grade(src, dst, grain=19.0, seed=7, people=False, scale=2):
    im = Image.open(src).convert('RGB')
    if scale > 1:                                                        # grade at 2x so grain reads as fine film, not blocky pixels
        im = im.resize((im.width * scale, im.height * scale), Image.LANCZOS)
    im = im.filter(ImageFilter.GaussianBlur(0.45))                      # soften AI crispness
    a = np.asarray(im).astype(np.float32) / 255.0
    h, w, _ = a.shape
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    # 1. On-camera flash: centre lift + soft vignette falloff
    cx, cy = w * 0.5, h * (0.40 if people else 0.46)
    r = np.sqrt(((x - cx) / (w * 0.62)) ** 2 + ((y - cy) / (h * 0.62)) ** 2)
    if people:
        # direct on-camera flash: subject pops, light falls away fast, very slight vignette at the corners
        flash = 1.17 - 0.33 * np.clip(r, 0, 1.4) ** 1.25 - 0.08 * np.clip(r - 0.85, 0, 1) ** 1.2
    else:
        flash = 1.07 - 0.30 * np.clip(r, 0, 1.4) ** 1.7
    a = a * flash[..., None]
    # 2. Tone: slightly darker mids, deeper shadows, gentle S-curve, soft highlight roll-off
    a = np.clip(a, 0, 1)
    a = a ** 1.04
    a = a + (0.30 if people else 0.22) * (a - 0.5) * (1 - np.abs(2 * a - 1))   # S-curve (flash punch)
    a = 1 - (1 - a) ** 1.04
    # 3. Colour: calm hot reds/oranges, warm highlights, faint cool shadows
    lum = (a * [0.299, 0.587, 0.114]).sum(2, keepdims=True)
    warm = np.clip(a[..., 0:1] - (a[..., 1:2] + a[..., 2:3]) / 2, 0, 1)  # how red/orange a pixel is
    a = lum + (a - lum) * (1.12 - 0.38 * warm)                            # richer cool pastels, calm hot reds/oranges
    a = a * np.array([0.95, 0.985, 1.10])                                # cooler, pink-magenta film cast
    hi = np.clip((lum - 0.55) / 0.45, 0, 1); lo = np.clip((0.35 - lum) / 0.35, 0, 1)
    a = a + hi * np.array([0.020, 0.008, -0.012]) + lo * np.array([-0.010, 0.004, 0.016])
    # 4. Flash bloom + halation around bright highlights
    b = np.clip((lum - 0.78) / 0.22, 0, 1)[..., 0]
    bloom = np.asarray(Image.fromarray((b * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(max(w, h) / 90))).astype(np.float32) / 255
    a = a + bloom[..., None] * (np.array([0.09, 0.05, 0.035]) if people else np.array([0.06, 0.025, 0.02]))   # flash glow on skin/highlights
    # 4b. Printed-film finish: faded whites, lifted blacks
    a = 0.035 + np.clip(a, 0, 1.2) * 0.885
    # 5. Film grain: luminance, fine, strongest in midtones
    rng = np.random.default_rng(seed)
    n = rng.normal(0, 1, (h, w)).astype(np.float32)
    n = np.asarray(Image.fromarray(((n * 40) + 128).clip(0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.55))).astype(np.float32)
    n = (n - 128) / 40
    mid = 0.55 + 0.45 * (1 - np.abs(2 * lum[..., 0] - 1))
    a = a + (n * mid * grain / 255.0)[..., None]
    Image.fromarray((np.clip(a, 0, 1) * 255).round().astype(np.uint8)).save(dst, quality=92, subsampling=0)

if __name__ == '__main__':
    people = '--people' in sys.argv
    args = [v for v in sys.argv[1:] if not v.startswith('--')]
    grade(args[0], args[1], people=people, scale=1 if '--1x' in sys.argv else 2)
