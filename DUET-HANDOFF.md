# DUET — HANDOFF (for a fresh Claude session)

## Who & what
- Client/brand: DUET (duet.nz, NZ) — wireless clip-on mic kits for two. Built by Aimée Robson (Aimée Robson Creative).
- Tagline: "Room for two voices." Colourways: Blush (pink), Cloud (white), Noir (black).
- Look: pastel, playful, editorial — now pushing BOLDER ("a real interruption in the market").
- Working style: concise, visual, kind + direct; bullets; "what if" ideas; ALL-CAPS file/folder names (lowercase extensions; Shopify web files stay lowercase).

## Repo
- GitHub: aimeelrobson/ARC-REPOS, branch `claude/eager-mayer-0s0nbk` (only branch; no PR).
- `DUET-MIC-VIDEOS/ROUND-3-AI-IMAGERY/` — AI image set, film grade, product refs
  - `PRODUCT-PHOTOS/` — REF-MIC-* (Blush/Cloud/Noir), KIT-*.png, kit-*.png cutouts (alpha), DUET-LOGO-BLACK.webp
  - `SET-4X5/`, `SET-9X16/`, `SET-WIDE/` — clean originals
  - `FILM-4X5/`, `FILM-9X16/`, `FILM-WIDE/` — graded (live on site)
  - `DUET-FILM-GRADE.py` — "5:44pm" look (grain 19, cooler pink cast), grades at 2x so grain reads as film. `python3 DUET-FILM-GRADE.py SRC DST [--people]`
  - `DUET-GENERATE-SET.py` — Gemini generation (strict mic-accuracy prompt + refs)
  - `HERO-LEMON-CHAIRS/` — NEW Cloud hero (see below)
- `DUET-MIC-VIDEOS/ROUND-4-THE-DUET-SHOW/` — Ep.01 retro-TV video (superseded by bolder direction)
- `DUET-MIC-VIDEOS/ROUND-5-BOLD/` — DUET-BOLD-01-TWO-VOICES-ONE-TAKE.mp4 (current direction) + SOURCE/
- `DUET-SHOPIFY-THEME/` — custom Dawn sections (duet-pastel-*.liquid), templates/index.json, PREVIEW-LEMON-CHAIRS/index.json

## Tools & how things are made
- Images: Gemini API `gemini-3-pro-image` via REST (key injected by environment credential; never paste keys). Attach product refs as inline_data. Use imageSize "4K"/"2K".
  - Lessons: tell it "same size as the object it replaces" for scale; patch-edit small crops then blend back to protect faces; it tends to recolour whole images — colour-match patches back.
- Videos: HTML page with `seek(t)` → Playwright screenshots (Chromium at /opt/pw-browsers) → ffmpeg (imageio_ffmpeg binary). 1080x1920, 30fps. Fonts: Instrument Serif + Figtree. Source HTML + DUET-RENDER.js saved in each video folder.
- Shopify: Admin GraphQL via Shopify MCP.
  - Upload images: push to GitHub, then `fileCreate` with raw.githubusercontent URL pinned to commit SHA; `duplicateResolutionMode: REPLACE` swaps an image everywhere it's used (same filename).
  - Theme files: `themeFilesUpsert` (URL body) — ONLY works on unpublished themes. Live theme writes + publishing are blocked → Aimée publishes herself.

## Shopify state
- Store: 6i83ta-ut.myshopify.com (duet.nz), NZD.
- LIVE theme: "DUET PASTEL v3 (MOVE & RESIZE)" id 165800181858 — hero = Blush bathtub, movable hero blocks, per-section size/colour/heading controls.
- PREVIEW theme: "DUET PREVIEW: LEMON CHAIRS HERO" id 165807030370 — identical to live except hero images → lemon chairs. APPROVED by Aimée; she needs to click Publish.
  - Preview link: https://6i83ta-ut.myshopify.com/?preview_theme_id=165807030370
- Products: SOLO $69, DUET Kit $109 (variants Pink 50523102445666 / White 50523102347362 / Black 50523102380130), DUET Kit + Case $129. Collection: duet-kits.
- Web files: duet-pastel-*.jpg (20 set images + bathtub wide), duet-pastel-people-05-lemon-chairs(-wide).jpg.

## Lemon chairs hero (Cloud) — current state
- Two women back to back on yellow chairs, lilac room. Brunette holds a Cloud mic (thumb over body, button + LED to camera). Blonde laughing, arm draped, mic dangling from her fingers against dark denim.
- Masters: DUET-HERO-LEMON-CHAIRS-CLOUD-MASTER.png (4K frame), ...-WIDE-MASTER.png (room extended for headline). Web: 2400x1340 desktop, 1000x1250 mobile (heads-to-seat crop).
- Headline sits left-middle on clear lilac (desktop); mobile shows text in panel below image.

## Video direction (agreed)
- BOLD, not cute: hard cuts every 0.5s (120 BPM grid), full-bleed Figtree 900 uppercase type edge to edge, colour blocks (lemon #F3E03B, hot pink #FF5FA2, lilac #D9CCF5, ink #141214, cream), real-people close-ups, signature opener = extreme close-up of a mic + "click".
- Silent exports → add trending audio in-app.
- DUET-BOLD-01 done (13s, 9:16). Awaiting Aimée's feedback.

## Next up (pick from)
1. Aimée publishes the lemon chairs preview theme.
2. Feedback on DUET-BOLD-01 → iterate.
3. Series idea: one bold edit per colourway (needs a real-people Noir/Blush hero like lemon chairs — generate or supply).
4. Aimée's own edited images (mentioned early) — send as JPG/PNG to swap in.

## Rules to keep
- Never publish or write to the live theme; work on a duplicate + share preview link.
- Keep original/clean files; commit + push after each deliverable.
- Product accuracy: no invented logos/text on mics; true scale (~finger length).
