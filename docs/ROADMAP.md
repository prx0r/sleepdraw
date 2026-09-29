# ROADMAP — sleepdraw continued dev (from lora3 lock, 2026-09-28)

Order is owner-priority; each item states entry price and done-criteria.
One variable per round still applies to knob work. New modules get preset
files, never silent tweaks.

## 1. Checkpoint scheduler (next engine build)
Checkpoints as artist stages (construction → lines → ink → tone → color),
each with a breath between, storyboard timestamps conducting. Builds on
WB_ACTS (spatial) → staged by FIDELITY instead: derive stage stack from
the color master (division-sketch → threshold ladder, proven in
runs/yuki-exp/cp1-5 + yuki-ladder.jpg), reveal stage-by-stage with
`sequence.chain`-style breaths. Done when: 10-min staged Yuki film ships.
Needs no keys (numpy fallback); img2img stages upgrade inputs later.

## 2. Morph-chain module (`sleepdraw/morph.py`, spec in SEQUENCES.md B)
Next scene draws OVER current: shared anchors exempt, B-only strokes walk
with rhythm scheduler, A-only strokes reverse-fade. v1 cheat: composite the
same moon asset into every plate (pixel-stable anchors). Prototype pair:
hut→doorway. Done when: seamless handoff test ships.

## 3. Render-feel varieties (branch from lora3 lock)
- Overdraw (cheapest, highest humanity-per-effort): construction pass 40% +
  ink commit. Small change in smooth path.
- Boil-settle (Paperman boil param): micro-wobble during draw, frozen hold.
- Hatchfill: shade as contour hatching following forms (fill-phase rework).
- Inkwash: crisp lines over tonal bloom (needs wash-friendly plates).
Each: 30s shootout on doorway-v3, owner verdict, winner folds into lora4
candidate. Never stack unreviewed.

## 4. Pen-scratch sound (with easy repo)
Procedural pen bed synced to the reveal velocity profile (rhythm targets =
amplitude envelope; lifts = silence). Placement: narration-free slots only
(intro star-draw, chapter thresholds, draw opens). easy `foley.pen_scratch`
+ mix slot. Reference: PenSound (synthesis beats loops — ears catch loops).
Freesound CC0 pencil recordings as texture reference.

## 5. Longform (3-hour wedge)
Color-first pipeline (color master → derived B&W = perfect registration),
low-fps drift sections (new time knobs; 60fps×3h = 648K frames, never),
30-min prototype → measure R2 bytes + encode → scale. Done when: 30-min
staged color film ships with size receipt.

## 6. FAL_KEY tracks (blocked on owner paste)
Uni-1 masters ($0.042), img2img stage ladder ($0.024×4), Inworld TTS bulk
shootout, breathe stillness matrix (SEQUENCES.md A). Wire into art.py +
foley_eleven pattern on arrival. Nothing here blocks 1–5.

## 7. Micro-motion holds (after voice lock, never before)
p5 particle layers over finished plates (snow, lantern flicker, mist drift),
gold-only motion rule. Drowsiness test: midnight watch, owner is the sample.
Kill on any alerting feel.
