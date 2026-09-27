# SEQUENCES — unbroken-chain sleep films (spec v1, 2026-09-27)

Thesis: a sleep film should never cut, fade to black, or restart. One continuous
line from first stroke to final frame: DRAW → BLOOM → BREATHE → DRIFT → MORPH → …

## The grammar (verbs, composable)

| Verb | What the viewer sees | Engine |
|---|---|---|
| DRAW | pen draws the scene (lora1) or etches it (lora2) | sleepdraw now |
| BLOOM | tone floods in over the linework | colorize now |
| BREATHE | finished image subtly lives: cloud drift, water shimmer, lantern flicker, beard-still | fal.ai image-to-video, low motion |
| DRIFT | feather-slow zoom/pan across the living image (Ken Burns at 0.1x) | ffmpeg zoompan now |
| MORPH | next scene draws OVER the current one; shared anchors (moon, horizon) persist, the rest redraws | new (see below) |
| SETTLE | final hold on a complete image, bed only, no motion | hold now |

A film = a sentence in these verbs. Example 6-min piece:
`DRAW(moon) → BLOOM → BREATHE(6s) → MORPH(arch, moon persists) → BLOOM → BREATHE → DRIFT → MORPH(farm, moon persists) → BLOOM → BREATHE(12s) → SETTLE`.

## Technique A — BREATHE (fal image-to-video)

Take the final rendered frame (full tone, 1080x600) → fal.ai i2v model with a
stillness prompt ("moonlight ripples almost imperceptibly, clouds breathe,
4 seconds, minimal motion, no camera move, no morphing, no new objects").
Candidates: Kling 1.6, Luma Ray, MiniMax Hailuo — all take start-frame + prompt.
- Needs: FAL_KEY (missing — owner to paste). Cost: ~$0.02–0.10 per 4–8s clip.
- Plumb as: `sleepdraw/breathe.py — image → fal → clip`, Studio button next.
- Risk: models love motion; prompts must forbid it hard. Test matrix: 3 models ×
  2 prompts on the moon frame, pick the stillest.

## Technique B — MORPH (unbroken scene chain, no black)

The clean-ending problem: today a scene ends dead (hold on finished image) and
the next begins dead (black canvas). Fix: never clear the canvas.
1. Scene B art is generated CONDITIONED on scene A: same anchor objects, new
   subject. Prompt pattern: "same crescent moon top-center, same horizon line,
   now a stone arch rises left…" (FLUX text-only today; FLUX-redux/img2img when
   we want pixel continuity).
2. Canvas starts from A's final frame. B's skeleton walk draws only B-minus-A
   strokes; strokes A-and-B share stay put. Erasure (A-only strokes that must go)
   is a reverse draw: hand… no hand in our grammar — fade those strokes over 3s
   while new strokes arrive. Net effect: the drawing never stops, the scene turns.
3. Implementation: `sleepdraw/morph.py` — diff ink masks (A vs B, dilated),
   walk B-only pixels first, fade A-only pixels concurrently, shared pixels
   untouched. Anchors declared per sequence (moon, horizon) so the prompter and
   the differ agree on what persists.
- Risk: FLUX won't place anchors pixel-exact; differ needs anchor re-detection
  (template-match the moon disc, align, then diff). v1 can cheat: SAME moon asset
  composited into every B prompt image before draw (moon is drawn once, then
  exempted from redraw — literally unbroken).

## Technique C — mixed sequences (the actual films)

No single verb carries 10 minutes. Mix by energy:
- **"Night Journey" (6 min)**: moon/pen (lora1, fast-ish) → arch/etch (lora2) →
  farm/etch → mariner/etch → BREATHE on mariner 12s → SETTLE. Moon persists
  through all four (cheat v1). Arc: simple → dense → densest → face.
- **"Water" (4 min)**: three water scenes (lake, arch-water, farm-water), all
  lora1, BREATHE between each (shimmer), DRIFT across the last. Meditative,
  low density = cheap renders.
- **"Faces" (5 min)**: mariner → second portrait (generate next) → MORPH between
  (shared oval/eye-line anchors — hardest morph, best payoff).

## Audio spine (parallel, same chain logic)

Voice (edge-tts now, Qwen3/Kaggle later) + rain bed (ambience rain-tent now) +
piano (fal ACE-Step when FAL_KEY lands). Bed never drops between scenes; voice
pauses map to BREATHE/DRIFT verbs. Mix map lives in the sequence file, not code.

## Sequence file format (proposed, v1)

```yaml
name: night-journey-v1
anchors: [moon-disc]          # drawn once, exempt from redraw
bed: rain-tent
scenes:
  - art: moon-lora1           # banked asset or prompt
    style: lora1
    verbs: [DRAW, BLOOM, BREATHE(6s)]
  - art: prompt(arch + same moon)
    style: lora2
    verbs: [MORPH, BLOOM, BREATHE(6s), DRIFT]
```

## Order of attack

1. FAL_KEY → `breathe.py` + stillness matrix (cheapest wow per dollar).
2. Moon-cheat MORPH (composite shared moon, diff the rest) — unbroken chain v1.
3. Sequence runner: yaml in, one mp4 + chapter metas out, R2 ship.
4. Anchor re-detection + FLUX-redux continuity (real morph, later).
5. fal music bed under the whole chain (ACE-Step, same key).
