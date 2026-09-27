# CORBIN — channel style reference (v1, 2026-09-27)

Everything on this channel filters through here: art, music, intro, pacing.
Prompt-styles, not weights — freedom over determinism.

## World

The imaginal as a place you visit at night: black water that reflects what
isn't there, floating lanterns, astral skies, fluid reflections. Gravity is
optional; stillness is mandatory.

## Visual grammar

- **Space**: no linear perspective. Stacked planes — garden/pool below,
  hanging forms mid, stars above. Persian-miniature depth without the color.
- **Architecture (historically relevant, always real references)**:
  - Sheikh Lotfollah dome (Isfahan) — arabesque sunburst interior
  - Nasir al-Mulk prayer hall — light through colored glass (render as beams)
  - Mihrab geometry — prayer-niche arch frames the subject
  - Girih tile patterns — borders, slow-reveal backgrounds
  - Mamluk glass lamps — hanging lights with Light-Verse glow
  - Mi'raj layered skies — concentric heavens, ringed halos
- **Motifs**: cypress, nightingale-rose, walled garden pool, crescent + full
  moon (anchor, drawn once), veiled figures (no faces), stairs that lead up
  out of frame, mirrors reflecting stars.
- **Medium**: white pencil etching on black. ONE gold accent max (#D4A94E):
  sun-disc rim, dome finial, lamp flame. Emerald horizon thread optional.
- **Forbidden**: faces unveiled, perspective streets, daylight, color fields,
  text of any kind, cluttered compositions (vast black always wins).

## Prompt template

```
{subject}, {architectural anchor}, night, white pencil etching on deep black,
no linear perspective, stacked planes, {motif list}, one gold accent: {object}.
No text, no letters, no numbers, no words. Wide landscape, generous black margins.
```

## Music

Sparse oud plucks + rain bed (-22dB). Ney only at chapter thresholds. No rhythm
section, no swells, nothing that wakes. Same bed every film (channel sound).

## Intro + logo (every film, identical)

8 seconds: gold girih eight-point star draws itself on black (lora2-corbin
grammar, no hand) → "CORBIN" etches beneath in thin capitals → 2s hold →
fade. Then film. Reusable asset, rendered once: `assets/corbin-intro.mp4` (TODO).

## Pacing

- One image per ~5 min for hour one, then black + bed.
- Images may hold up to 10 min each: draw (1–2 min) → hold/breathe under
  continuing narration → slow fade (3–4s) → 2.5s black breath → next.
- Draw emerges from black; no fade-ins ever.

## Library tags (assets/library.json)

Tag every banked asset: motif (moon/garden/lamp/dome/mihrab/girih/figure/
stair/mirror), anchor?, film-used-in[]. Chapters reference tags, not files —
art direction becomes casting.
