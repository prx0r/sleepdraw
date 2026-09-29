# YUKI — art direction for the Yuki-Onna plates (lora3 experiment)

Grammar: lora3 (white sumi-e pencil on black, one gold accent #D4A94E,
stacked planes, faceless figures, vast black). Template:

```
{subject}, night, white sumi-e pencil etching on deep black,
no linear perspective, stacked planes, {motifs}, one gold accent: {object}.
No text, no letters, no numbers, no words. Wide landscape, generous black margins.
```

## Round 1 — three hero plates (art only, CF flux free) — DONE 2026-09-28

* hut-storm: KEEPER (moon crops out in 16:9, hut+reflection+gold window survive).
* doorway-v1: REJECT (two women, faces, white borders, glyph garbage).
* doorway-v2: KEEPER + HERO — `powoutputs/test/yuki-doorway-hero.mp4` (2min
  lora3 etch, on dash review queue). Single veiled shadow-face woman, gold
  breath-wisp, full-bleed black.
* mist-exit-v1: spare abstract; mist-exit-v2: KEEPER (16:9 crop removes the
  red seal; mist + gold shaft survive).
* Lesson: add "full-bleed, no border/signature, key elements vertical-center"
  to every prompt (16:9 center band keeps y 22–78% of square).

## Round 2 — rhythm (WB_RHYTHM, vendor patch) — DONE 2026-09-28

* Width round verdict: SKETCH_W 2/3/4 look near-identical — width was the
  wrong variable. Soft (W=3) kept as base.
* `WB_RHYTHM=1/2` added to vendor smooth path (lift pauses + curvature
  pacing, same frame count, deterministic): yuki-v-rhythm1/2 shipped.
  Owner: deep (L2) is cool.
* doorway-v3 (fine-line regen): KEEPER — two sleepers (story-accurate!),
  faceless veil, hatched beams, gold flecks, full-bleed. v4 REJECT
  (borders + signatures + visible face).
* HERO: `powoutputs/test/yuki-doorway-v3-slow.mp4` — v3 art, 2min, L2 deep
  rhythm, SKETCH_W=3. On dash review queue.

## Round 3 — pencil point + gold ritual (engine) — DONE 2026-09-28

* `WB_LINE` knob (pen point px, default = old floor): yuki-v-pencil (1px)
  shipped — pencil, not felt-tip.
* Gold drawn by the ENGINE (flux gold lottery bypassed): `WB_GOLD` waypoints
  reserved from ink + fill, revealed progressively in the hold-phase ritual,
  then stillness. Proven in yuki-v-ritual2 (wisp rises from the porch woman).
* Bug caught by pixel audit: a stray line doubled every hold frame in gold
  runs (yuki-v-staged, yuki-v-ritual v1 holds run 2x long — tests only).
  Non-gold runs never touched the branch — unaffected.
* Master art: master-v4 selected (clean edges, safe faces). Moons keep
  landing top-edge (crop removes) — composition must survive without them.

1. **hut-storm** (establishing): ferryman's hut on a wide river in a great
   snowstorm at night, snow-laden pines bending, roaring black water;
   motifs: snowfield, pine silhouettes, tiny hut; gold: snow-light glint on
   the river.
2. **doorway** (money shot): snow-light glowing doorway of a dark hut, a
   veiled woman in white kimono bending over two sleeping woodcutters,
   faceless, breath like faint smoke; motifs: doorway frame, sleepers as
   dark mounds; gold: the breath-smoke wisp.
3. **mist-exit** (final): white mist spiraling up through a smoke-hole in a
   dark beamed roof, vanishing into black; motifs: roof beams, rising
   spiral; gold: faint moonbeam shaft through the smoke-hole.

## Round 2 — draw the winner(s)

lora2 knobs frozen (`make --set WB_COLOR_W=3 --set WB_BRUSH=10`), 30s test
first, 2min hero for the keeper. Ship keepers to `powoutputs/test/`
→ dash review queue.

## Later (not this round)

Plates 3–4 of the 5-beat sheet (road meeting, hearth sewing) once the style
locks. Micro-motion trials (snow particles, gold-only drift) after voice.
