# AGENTS.md — sleepdraw (read first, every session)

Tiny engine room for the sleep B&W slow-draw style. `lora1.yaml` is law.

## What this is

FLUX pencil art → 16:9 crop → skeleton-stroke draw (techdou+WB_SMOOTH) →
R2 test channel. Variants game: new art OR new knobs per round, never both.

## Where everything is

| What | Where |
|---|---|
| Locked style | `lora1.yaml` (read before any render) |
| Reference art | `assets/moon-lora1-flux-pencil.jpg` |
| Pipeline | `sleepdraw/art.py`, `draw.py`, `ship.py` |
| CLI | `cli.py make --prompt … --name …` |
| Animator (vendored MIT) | `vendor/techdou/` — patches: WB_SKETCH_LIGHT, WB_SPLIT, WB_SMOOTH, pen lifts, luminance ink |

## Laws

- lora1 is the house look. Drift needs a new preset file, never silent tweaks.
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
