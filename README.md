# sleepdraw — the B&W slow-draw engine room

One style ([lora1](lora1.yaml)), one pipeline: FLUX pencil art → 16:9 crop →
skeleton-stroke draw → R2 test channel. Lightweight (this repo ≈ 2MB) and
extensible: new art OR new knobs per round, never both.

```bash
pip install -r requirements.txt   # boto3 pillow numpy opencv-python-headless pyyaml
python3 cli.py make --prompt "small glowing lantern on dark water, extremely minimal, vast black" --name lantern-v1
python3 cli.py make --image assets/moon-lora1-flux-pencil.jpg --name moon-check --no-ship
python3 cli.py make --prompt "..." --name pine-v2 --set WB_SKIP=6
python3 cli.py lora1              # print the locked recipe
```

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
