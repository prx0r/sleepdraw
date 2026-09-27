# STACK — art + motion options (researched 2026-09-27; $ documented, ~ estimated)

## Pencil art (best → cheapest)

1. **House LoRA (the move).** Train fal `flux-lora-fast-training` on our 10–20
   best frames (moon/farm/mariner/lantern — already one style!). Then every
   variant generates IN our style deterministically. Training ~$2–5 one-time;
   inference at standard fal rates. This makes "lora1/lora2" literal.
2. **Monochrome-Pencil (prithivMLmods, FLUX Kontext i2i).** Photo→pencil that
   preserves composition — ideal variant machine: keep the farm, restyle the
   light. Trigger: "[photo], replicate as pencil illustration, B&W".
3. **WizardWhitebeard etchings (SDXL).** `etching,` trigger + `dark background`
   contrast guide — closest off-the-shelf to our look. 2k downloads, proven.
4. **CF FLUX schnell ($0, now).** Free exploration; prompt-only style, no seed.
   Keep for sketching, promote winners into the LoRA training set.
5. DaVinci ink / Super-Pencil-Flux / Graphic-Etching — backups, bolder/graphic.

## Motion/breathe — fal-verified $/s (2026-09-27)

| Model (fal) | 720p | 1080p | 30s loop cost | Notes |
|---|---|---|---|---|
| Wan 3.0 std i2v | $0.10 | $0.20 | **$3.00** | 30s ONE pass, audio incl, end_image_url = perfect loops |
| Wan 3.0 Prime | $0.14 | $0.28 | $4.20 | faster turnaround, same params |
| LTX-2.5 Fast | $0.09 | $0.13 | $2.70 | audio incl; open weights |
| LTX-2.5 Pro | $0.12 | $0.17 | $3.60 | max fidelity |
| LTX-2.3 Fast | $0.03 | $0.06 | $0.90 | cheapest quality breathes |
| Kling 2.5 Turbo Pro | $0.07 | — | $2.10 | best quality/price, tail-frame input |
| Hailuo std | $0.045 | — | ~$1.35 | budget solid |
| Kling 3.0 std | $0.084 | $0.112 | $2.50+ | premium, multi-shot |

Audio included free on Wan 3 + LTX (others charge +40–100%).

## Self-host math (volume only)

- **LTX is the self-host pick**: open weights, 16GB min (4090 24GB @ ~$0.5–0.8/hr
  RunPod/Vast) → ~$0.004–0.007/finished-sec at volume. 30s loop ≈ $0.15–0.20
  vs $2.70–3.00 on fal. ComfyUI templates day-one, RunPod blog blessed.
- Wan 2.2 14B needs H100 (~$2–2.9/hr) → ~$0.03/s. Wan 2.5+ and 3.x are API-only.
- Break-even: self-host wins past ~100 clips/mo + you eat ops (images, queues,
  dead pods at 3am). fal wins for explore-and-iterate. Start fal, move the
  winners' workload if the bill ever matters (it won't until 1000s of clips).

## 30s loop recipe (the dream, $3)

Wan 3.0 std i2v, `start_image_url` = finished farm frame, `end_image_url` =
SAME frame → model must return to start = seamless loop by construction.
Stillness prompt, no camera move. One generation, 720p, audio off: $3.00.
Fallback: 5× 6s Hailuo (~$0.80) + crossfade seams (visible if you look).

## Recommended stack (sleepdraw v2)

- Explore: CF FLUX ($0) → curate winners.
- Lock style: house LoRA trained on winners (one-time $).
- Variants: fal flux-2/edit $0.024/img, hex palette locked.
- Breathe: LTX-2 fast ($0.10/loop); heroes on Kling 2.5 Turbo ($0.25).
- Draw/chain/ship/voice/bed: local ($0) as today.
- 10-min film, full fal: ~$1–2. Free tier: $0 minus quality on motion.
