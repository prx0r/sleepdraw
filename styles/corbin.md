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

## Book anchor (Alone with the Alone — real TOC)

- Intro: spiritual topography · Ibn Arabi life-curve (Averroes funeral,
  pilgrim to Orient, disciple of Khidr, maturity) · esoterism
- Part One/SYMPATHY: I divine passion (heliotrope, pathetic god, unio
  sympathetica) · II sophiology (sophianic poem, dialectic of love, feminine)
- Part Two/PRAYER: III creation as theophany · IV heart (field, subtile
  organ, science) · V prayer (method, homologations, responses) ·
  VI form of god (hadith of vision, mystic Kaaba) · Epilogue
- Our 7 essays map 1:1 onto this spine. Films follow the book's order.

## Reference works (real, citable, look at these)

- Mi'raj paintings (Buraq ascent, layered heavens, vessel-angels, flaming
  aureoles; Safavid veiled faces — our no-faces rule is period-correct).
- Tazhib illumination: shamsa sunbursts, girih strapwork, islimi vines,
  gold-on-lapis borders and chapter marks.
- Rumi Masnavi opening pages (Dartmouth): gold arabesque fields.
- Timurid Herat / Bihzad school: Majnun on Layla's tomb (extra-textual
  mystical figures inside narrative scenes — our emblem-in-landscape move).
- Sheikh Lotfollah dome + Nasir al-Mulk hall: architecture as luminous body.
- Mamluk glass lamps with the Light Verse: hanging light motif source.

## Sleeper figure (stolen from the miniatures)

Persian painters put small "spectator figures" at the horizon to model the
viewer's gaze. Ours: ONE tiny resting/sleeping figure at the horizon of
landscapes — the viewer's surrogate, already asleep. Recurs across films.

## Library tags (assets/library.json)

Tag every banked asset: motif (moon/garden/lamp/dome/mihrab/girih/figure/
stair/mirror), anchor?, film-used-in[]. Chapters reference tags, not files —
art direction becomes casting.
