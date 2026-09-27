# COSTS — sleepdraw pipeline (2026-09-27; $ = documented, ~ = estimate)

## Per-unit (what one variant costs)

| Step | Engine | Cost | Notes |
|---|---|---|---|
| Art (1 scene) | CF Workers AI FLUX | $0 (free allocation) | ~30s, no seed → curate-and-keep |
| Variant (inpaint) | CF SD-inpainting (beta) | $0 ($0.00/step while beta) | off-style; placeholder until fal |
| Variant (edit) | fal flux-2/edit | **$0.024**/img (1MP→1MP @ $0.012/MP) | needs FAL_KEY; style-true, seeded |
| Draw 30s | local CPU (techdou) | $0, ~1–3 min | 60fps; 30fps halves file size |
| Draw 2min | local CPU | $0, ~4–6 min | 40–60MB @60fps — biggest cost is R2 bytes |
| Breathe 4–8s | fal i2v (Kling/LTX) | **~$0.05–0.10**/clip | needs FAL_KEY; stillest-model matrix first |
| Voice | edge-tts | $0 | Qwen3/Kaggle later for character |
| Bed | fal ACE-Step | **~$0.02–0.05**/track | needs FAL_KEY; rain-tent free now |
| Ship + host | R2 + Workers dash | ~$0 | storage $0.015/GB-mo, egress $0 |

## Current burn

- Test channel (2026-09-27): 25 objects, **173MB ≈ $0.003/mo**. Irrelevant.
- A 10-min film (5× 2min etches): ~$0 compute, ~300MB hosted (~$0.005/mo),
  ~10 FLUX gens ($0), + optional fal: 5 edits ($0.12) + 5 breathes (~$0.50) +
  1 bed (~$0.05) ≈ **$0.70/film**. The product is Nigerians-cheap at any volume.
- Kaggle 30h/wk T4 + Colab 15h/wk cover all GPU voice/engine experiments ($0).

## Cost levers (biggest first)

1. **30fps not 60fps** for etched work (halves the 40–60MB files; motion is slow,
   nobody sees 60fps at sleep pace). One-line change, do before scaling.
2. fal breathe only on hero frames (moon/faces), not every scene.
3. Batch fal edits (multi-image single calls where the model allows).
4. Prune test channel monthly (v1–v3 superseded the moment v4 ships).
