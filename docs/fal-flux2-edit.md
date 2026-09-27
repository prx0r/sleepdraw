# fal flux-2/edit — reference (fetched 2026-09-27)

Image-to-image editing, natural language + hex color control, up to 4 input
images (@image1.. or "image N" indexing). Seed-repeatable.

- Endpoint: `fal-ai/flux-2/edit` (queue: submit → status → result; webhooks avail)
- Auth: `FAL_KEY` env (server-side proxy only — never browser-exposed)
- Inputs: `prompt*`, `image_urls[]*` (public URL or base64 data URI, or
  `fal.storage.upload`), `image_size` (512–2048, enum incl. landscape_16_9),
  `num_images`, `guidance_scale` 2.5, `num_inference_steps` 28,
  `acceleration` none|regular|high, `enable_prompt_expansion`,
  `output_format` jpeg|png|webp, `seed`, `enable_safety_checker` (default true)
- Output: `images[{url,…}]`, timings, seed
- **Price: $0.012/MP in + out** (1MP→1MP ≈ **$0.024/image**)
- JSON structured prompts for multi-subject control; HEX codes with
  "color"/"hex" keyword for exact palette (our muted umber/slate lock)
- Siblings: flux/dev/image-to-image, flux-1/schnell/redux (turbo cheap),
  flux-pro ultra redux, nano-banana-pro/edit, Kling 3.0 / Veo 3.1 / LTX 2.3 i2v

Our uses (in order): farm variants (sheep/dawn done free on CF; fal for
style-true edits) → portrait muted-color pass → BREATHE clips (i2v models) →
ACE-Step piano bed. Full attack order: SEQUENCES.md §Order of attack.
