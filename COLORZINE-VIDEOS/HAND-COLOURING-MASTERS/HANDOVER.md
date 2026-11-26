# COLORZINE hand-colouring footage handover

Created: 24 November 2026 (NZ)

## Deliverables

All five masters are silent H.264 MP4s, 1080 × 1920, 30 fps and exactly 10 seconds. Each visibly carries the label `AI-GENERATED VISUAL`; none should be described as customer UGC.

| Posting/file code | Real page used | Master |
| --- | --- | --- |
| D03 priority slot | Could've Been an Email | `MASTERS/COLORZINE-D03-COULDVE-BEEN-AN-EMAIL-HAND-COLOURING.mp4` |
| D05 priority slot | Touch Grass | `MASTERS/COLORZINE-D05-TOUCH-GRASS-HAND-COLOURING.mp4` |
| D06 | Botanical Serial Killer | `MASTERS/COLORZINE-D06-BOTANICAL-SERIAL-KILLER-HAND-COLOURING.mp4` |
| D15 | Out of Office | `MASTERS/COLORZINE-D15-OUT-OF-OFFICE-HAND-COLOURING.mp4` |
| D10 | Liquid Therapy | `MASTERS/COLORZINE-D10-LIQUID-THERAPY-HAND-COLOURING.mp4` |

The D03/D05 codes follow the priority posting slots in Aimée's 24 November brief. Historically, the first two page concepts were called D02 and D04 in the earlier content plan; the page names in the new filenames remove that ambiguity.

## Verification

- 1080 × 1920 portrait.
- Exactly 10.000 seconds each.
- Video stream only: no audio stream.
- Real approved lifestyle photograph and real printed page are pixel-locked.
- The photographed hand remains visibly gripping the marker and moves during the colour build.
- Colour builds progressively beneath the marker over the shot.
- Start, midpoint and end-frame checks are saved in `QA-FRAMES/`.

## Claude hand-off

Drag the five files from `MASTERS/` into Claude for beat-timing, audio-strip confirmation and final assembly. Add exactly one approved track per video natively in TikTok; do not bake music into these masters and do not mix tracks.

## Reproducible source

The working Remotion project, source photographs and the new compositions are in `REMOTION-SOURCE/`. The five 10-second compositions are:

- `D03EmailHandColouring`
- `D05TouchGrassHandColouring`
- `D06BotanicalHandColouring`
- `D15OutOfOfficeHandColouring`
- `D10LiquidTherapyHandColouring`

Render with the project-local Remotion CLI and H.264, CRF 18, yuv420p. Node dependencies are intentionally excluded from the handover and can be restored with `npm install`.
