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
