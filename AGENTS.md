> Repo topology: see /root/damn/AGENT-START-HERE.md (three repos: damn=channels+judgment, influence=platform+hands, sleepdraw=this workshop). Secrets never in repo; timers in system crontab; absolute paths bind all three.

# AGENTS.md — sleepdraw (read first, every session)

Tiny engine room for the sleep B&W slow-draw style. `lora1.yaml` + `lora2.yaml` are law.

## What this is

FLUX pencil art → 16:9 crop → skeleton-stroke draw (techdou+WB_SMOOTH) →
R2 test channel. Variants game: new art OR new knobs per round, never both.

## The two locks

- **lora1 (pen)**: minimal art, single-gesture draw, 30s. `lora1.yaml`.
- **lora2 (etched)**: dense intaglio art, slow shade, 2min. `lora2.yaml`.
  Only deltas vs lora1: COLOR_W 3, BRUSH 10. Pick per scene, don't blend.

## Where everything is

| What | Where |
|---|---|
| Locked style | `lora1.yaml` (pen) · `lora2.yaml` (etched) — read before any render |
| Reference art | `assets/moon-lora1-flux-pencil.jpg` |
| Pipeline | `sleepdraw/art.py`, `draw.py`, `ship.py` |
| CLI | `cli.py make --prompt … --name …` |
| Animator (vendored MIT) | `vendor/techdou/` — patches: WB_SKETCH_LIGHT, WB_SPLIT, WB_SMOOTH, pen lifts, luminance ink |

## Laws

- lora1/lora2 are the house looks. Drift needs a new preset file, never silent tweaks.
- Secrets never in repo (env or `/root/.r2-env` vault file).
- Every ship carries recipe JSON. Test prefix `powoutputs/test/`.
- No torch deps. CPU renders. Keep it small: no vertical, no subs, no voice here —
  those live in powvid; this repo draws.

## Run book

```bash
pip install -r requirements.txt
python3 cli.py make --prompt "<minimal B&W scene>" --name <thing>-v1
python3 cli.py make --image assets/moon-lora1-flux-pencil.jpg --name moon-check --no-ship
```

## Journey library (Artist Journey Engine)

Sketch→final pairs for multi-stage drawing journeys. See `docs/JOURNEY-LIBRARY.md`
for full source inventory and `docs/JOURNEY-AXIOMS.md` for the 14 validation rules.

| File | What |
|------|------|
| `storyboards/journey-pairs.json` | 2,290 labeled pairs (2,287 CIRThan + 3 owner storyboards). Each has: start/end zip_keys, subject, level1/2/3 captions, essay mapping |
| `storyboards/journey-database.json` | Flat database (essay → subject → captions) |
| `storyboards/cirthan/` | CIRThan captions + splits (from GitHub jinyuxu-whut/CIRThan) |
| `storyboards/*.md` | CIRThan paper, three 12-stage prototype storyboards |
| `docs/BAILIAN-STACK.md` | Alibaba/bailian CLI, endpoint, URL-not-local gotcha |
| `assets/six-step-deity-tutorial.png` | Six-stage construction reference (from stallshark) |

### Querying pairs

```python
import json
db = json.load(open('storyboards/journey-pairs.json'))
# By essay
devotion = [e for e in db if e['essay'] == '12-devotion']  # 531 pairs
# By subject
tara = [e for e in db if 'green tara' in e['subject'].lower()]
# Captions: level1 (sketch target), level2 (construction), level3 (final detail)
```

### Extracting images from zips (ranged read, ~5s, zero disk)

Images live in R2 zips (`uploads/sketch-*.zip` + `uploads/image-*.zip`).
Use ranged reads: fetch last 4MB for central directory → find member → fetch
byte range → decompress. See `JOURNEY-LIBRARY.md` for the code pattern.

### Image generation

`bl image edit` (Bailian, qwen-image-3.0) — MUST use URLs, not local paths
(local upload = 401). Upload to R2, generate presigned URL, pass to `bl`.
Or via quill worker: `POST /journey {image_url, prompt}`.

### Organic extension

Pre-processing: take CIRThan plate → one `bl image edit` with organic-border
prompt → use as journey endpoint (instead of rigid plate). Pair 68 has this
banked as `journey/68-final-organic.png`.

## THE JOURNEY PIPELINE — how it works (make no mistake)

**The 12-step storyboards ARE the checkpoints.** That's it. That's the design.

```
storyboards/01-stage-01.png ... 01-stage-12.png   ← 12 pixel-registered frames
         ↓ VALIDATE (axioms.py — 14 gates must pass)
         ↓ etch each transition (lora2/techdou): stage N canvas + new strokes from N+1
         ↓ chain with sequence.py (contemplative fades + black holds)
journey_complete.mp4
```

### Step by step

1. **PROTOTYPE**: Generate a 12-stage storyboard for a journey pair.
   - Stages are pixel-registered (620x900), same canvas position throughout.
   - Stage 1 = original sketch. Stage 12 = exact final painting.
   - Middle stages = progressive drawing actions (see manifest.json axes).
   - Owner uploads as `storyboards/NN-stage-*.png` + `manifest.json`.

2. **VALIDATE**: Run `axioms.py validate_stage()` on every consecutive pair.
   - All 14 axioms must pass before the journey is usable.
   - `encode_prompt()` feeds axioms into any stage regeneration.
   - Failing stages get regenerated, NOT skipped (axiom 14: no arbitrary quota).

3. **ETCH**: For each transition (stage N → N+1):
   - Start with stage N as the canvas (white-on-black after inversion).
   - Compute the pixel diff: new strokes = pixels in N+1 that aren't in N.
   - Animate drawing ONLY those new strokes onto the stage N canvas.
   - This is the artist adding to what's already there — axiom 2 compliant.
   - Rendered by lora2/techdou at finest settings (COLOR_W=3, BRUSH=10).

4. **CHAIN**: `sequence.py` links the 11 transitions with fades (2-4s) and
   black holds (2-3s). Each clip starts FROM black — the fade-in IS the
   emergence of the next stage's strokes.

5. **VALIDATE OUTPUT**: Final video must preserve both endpoints exactly
   (axiom 1) and show continuous identity (axiom 12).

### The 12 stages (from manifest.json — each journey follows this grammar)

| Stage | Name | What happens |
|-------|------|-------------|
| 01 | SOURCE | original sketch, untouched |
| 02 | READ/EXPLORE | construction circles, axes, guides |
| 03 | REPAIR | erase wrong proportions, keep useful guides |
| 04 | ANCHOR/STRUCTURE | figure geometry locked, contours established |
| 05 | DETAIL | features, ornament, clothing |
| 06 | INK | line work completes, first warm accents |
| 07-11 | COLOUR | grows from drawing, one region at a time |
| 12 | TARGET | exact final painting, unchanged |

The number 12 is REFERENCE, not a quota (axiom 14). A journey needing 15
stages gets 15. One needing 8 gets 8. The manifest records whatever was
actually generated.

### Key files

| File | Role |
|------|------|
| `storyboards/manifest.json` | Stage axes + frame labels per journey |
| `storyboards/NN-stage-*.png` | The pixel-registered checkpoints |
| `axioms.py` | 14 validation gates + encode_prompt() |
| `journey.py` | Full pipeline (currently prototype — uses API generation; **REPLACE with checkpoint-based etching once validated**) |
| `sleepdraw/sequence.py` | Chain transitions with contemplative fades |
| `docs/JOURNEY-AXIOMS.md` | The 14 axioms (full text) |
