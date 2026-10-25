# sleepdraw — the B&W slow-draw engine room

One style ([lora1](lora1.yaml)), one pipeline: FLUX pencil art → 16:9 crop →
skeleton-stroke draw → R2 test channel. Lightweight (this repo ≈ 2MB) and
extensible: new art OR new knobs per round, never both.



## Journey pipeline (12-step checkpoints)

**The 12-step storyboards ARE the checkpoints.** See `AGENTS.md` for the full flow.

1. Prototype: 12 pixel-registered frames → `storyboards/NN-stage-*.png`
2. Validate: `axioms.py` — all 14 gates must pass
3. Etch: stage N canvas + new strokes from N+1 (lora2/techdou finest settings)
4. Chain: `sequence.py` → `journey_complete.mp4`

Validated frames are FIXED — etching animates between them, never regenerating.
`journey.py` is a prototype; replace its generation phase with checkpoint-based
etching once a storyboard passes validation.

```bash
pip install -r requirements.txt   # boto3 pillow numpy opencv-python-headless pyyaml
python3 cli.py make --prompt "small glowing lantern on dark water, extremely minimal, vast black" --name lantern-v1
python3 cli.py make --image assets/moon-lora1-flux-pencil.jpg --name moon-check --no-ship
python3 cli.py make --prompt "..." --name pine-v2 --set WB_SKIP=6
python3 cli.py lora1              # print the locked recipe
```

## Repeatable pipeline (any video)

```bash
python3 cli.py new --name <film> --script essay.txt   # scaffold films/<film>/
# 1. bible: styles/<channel>.md (write once per channel)
# 2. flow: films/<film>/flow.md (12 shots, hour one, landscape first)
# 3. bench: films/<film>/shots-bench.md (hyper-specific concepts)
python3 cli.py board --script films/<film>/source.txt --name <film>  # chapters
python3 cli.py shot --board runs/<film>-*/chapters.json --n 3 --prompt "..." --film <film>
python3 cli.py status --name <film>                   # board progress
# chain: sleepdraw/sequence.py over finished clips -> R2 -> dash
```

## Storage map

| Layer | Where | Notes |
|---|---|---|
| Channel bible | `styles/<channel>.md` | motifs, palette, music, intro spec |
| Film dir | `films/<film>/` (flow, bench, source) | committed |
| Board | `runs/<film>-*/chapters.json` (scratch) | render paths recorded back |
| Banked art | `assets/` + `assets/library.json` (tagged) | reuse across films |
| Drafts | R2 `powoutputs/test/` | review surface |
| Finals | R2 `powoutputs/films/<film>/` (`--film`) | `--film` on make/shot |
| Long-form | R2 `powoutputs/` root via sequence meta | chained films |

## Layout

| What | Where |
|---|---|
| Locked style | `lora1.yaml` (lr1: white pencil on black, no hand, 30s, 16:9) |
| Reference art | `assets/moon-lora1-flux-pencil.jpg` |
| Pipeline | `sleepdraw/art.py` (FLUX) · `draw.py` (crop+techdou) · `ship.py` (R2+meta) |
| CLI | `cli.py make` (one variable per round, recipe.json per run) |
| Animator | `vendor/techdou/` (MIT, patches: SKETCH_LIGHT, SPLIT/SMOOTH env, pen lifts) |
| Scratch | `runs/` (gitignored) |

## Rules

- Secrets never in repo: CF/R2 creds from env or `/root/.r2-env`.
- Every ship carries its recipe (same-name `.json`): art prompt + full env.
- Test channel: `powoutputs/test/<name>.mp4` on the dash.
- New variant = new art (keep knobs) or new knobs (keep art). v-suffix keys.

## Requirements

boto3, pillow, numpy, opencv-python-headless, pyyaml. System ffmpeg.
No torch. CPU render: ~1–3 min per 30s clip.
