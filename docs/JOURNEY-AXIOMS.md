# JOURNEY AXIOMS — Artist Journey Engine (locked 2026-10-25)

> The non-negotiable rules for generating multi-stage drawing journeys
> from a rough human sketch to a finished thangka. These are validation
> gates, not prompt suggestions. A stage that violates any axiom is rejected.

## Core principle

Every frame must be a physically achievable continuation of the previous
frame, using the drawing operations available to Sleepdraw (draw, erase,
redraw, colour).

The mistake to avoid: treating each frame as an independent image-generation
problem. We're simulating an artist discovering a finished painting through
a continuous sequence of drawing decisions. The rough sketch is valuable
precisely because it gives the artist something unexpected to work with.

## The 14 axioms

| # | Axiom | What breaks it |
|---|-------|----------------|
| 1 | **Exact endpoints** | Reinterpreting, regenerating, or approximating the original sketch or final painting |
| 2 | **Stroke continuity** | Lines disappearing, shifting, or morphing without a visible erasure or redrawing operation |
| 3 | **Small, achievable transitions** | One frame becoming dramatically more complete without enough drawing actions between frames |
| 4 | **Conserved geometry** | A head, hand, instrument, or halo teleporting into its final position |
| 5 | **Artist causality** | Adding jewellery before establishing the neck, flowers before establishing their positions |
| 6 | **Material continuity** | Suddenly transforming a monochrome drawing into a completely different medium or surface |
| 7 | **Cumulative progress** | A stylistic experiment that makes the drawing harder to develop toward the final reference |
| 8 | **Purposeful exploration** | Cubism, geometry, or another style appearing just for visual spectacle rather than helping construct the eventual painting |
| 9 | **Progressive colour** | Large regions suddenly becoming fully saturated, textured, and finished |
| 10 | **Locality** | Several unrelated regions of the canvas changing simultaneously without corresponding artist actions |
| 11 | **No hidden work** | The renderer displaying a completed element that nobody visibly drew |
| 12 | **Continuous identity** | Losing the same figure, pose, expression, instrument, or overall composition along the journey |
| 13 | **Final convergence** | The second-to-last stage differing so substantially that the final transition cannot plausibly be drawn |
| 14 | **No arbitrary frame quota** | Forcing a transformation into eight frames if it requires considerably more drawing actions |

## Continuity vs similarity (the key distinction)

Two images might look very similar while being impossible to connect using
our drawing engine. Conversely, a frame might look surprisingly different
after a long sequence of perfectly visible, individual drawing operations.

**Validate the actions required between frames, not merely the visual
similarity of the frames.**

A stage is valid only if we can construct a replayable sequence:

```
Canvas A → draw / erase / redraw / colour → Canvas B
```

Without that sequence, the proposed stage is invalid.

## Three rules for style changes

Style changes are allowed along the journey, but only if:

1. A new style **reuses recognizable geometry already on the page**.
2. The transformation **into and out of** that style must be drawable.
3. The experiment must **produce something useful for a later stage**:
   alignment, contour, ornament, rhythm, colour planning, or composition.

Example: the oversized head from the original sketch inspires circles and
intersecting geometric lines → cubist construction study → helps discover
correct head orientation → artist selects useful contours, removes redundant
guides → develops into flowing thangka linework. The cubist influence was
real, but it existed as an exploratory drawing technique, not as an
inexplicable completed cubist painting.

## Eight-stage trajectory (reference, not fixed)

1. **Original human sketch** — exact supplied image, awkward proportions intact
2. **Geometric exploration** — construction circles, axes, triangles, perspective guides
3. **Proportion correction** — erase/replace incorrect contours, retain useful guides as construction
4. **Elaborating the figure** — facial features, cloth, hair, jewellery, floral architecture
5. **Completing the ink** — decorative linework, floral frame, throne, halo, textile ornament
6. **Localised colour** — gold crown, green instrument, red ribbons, selected flowers. Paper still visible.
7. **Nearly finished** — all major colour regions, background, ornaments present
8. **Exact final reference** — the supplied original painting, without reinterpretation

The number of frames is flexible. If a transformation needs extra drawing
time, give it extra drawing time rather than forcing a visual jump.

## Architecture: Artist Journey Engine

```
Exact source sketch + exact final reference
  ↓
Journey planner — discover coherent intermediate artistic decisions
  ↓
Action timeline — Draw · Erase · Correct · Detail · Colour
  ↓
LoRA 3 / Techdou renderer — animate real stroke-by-stroke transformations
  ↓
Continuity validator — reject impossible jumps, missing actions, endpoint drift
```

**Recipe file:** `lora4.yaml` (orchestration config, not a trained LoRA).
**Base renderer:** LoRA 3 (fixed nib, rhythmic strokes, pen lifts).
**Key shift:** generate ONE evolving canvas with hundreds/thousands of
recorded drawing actions, then sample frames from that continuous history.
Do NOT generate eight independently finished pictures.

## What needs new code

| Capability | LoRA 3 has it? | What's needed |
|---|---|---|
| Fine stroke animation | Yes | — |
| Natural pen lifts | Yes | — |
| White-paper black-ink | Needs override | Small change to env defaults |
| Draw new details incrementally | With supplied art | Stage orchestration |
| Erase incorrect proportions | No | New capability |
| Transform construction → correct contours | No | New capability |
| Paint selected regions in order | Limited | New capability |
| Maintain continuity across stages | No | Journey planner + validator |

## The pipeline (crystal clear)

**The 12-step storyboards ARE the checkpoints.** No API generation of stages
after validation — the validated storyboard frames are the source of truth.

```
prototype storyboard (12 pixel-registered frames)
  → VALIDATE (axioms.py, all 14 must pass)
  → ETCH each transition: stage N as canvas + diff-strokes from N+1 drawn on top
    (lora2/techdou, finest settings: COLOR_W=3, BRUSH=10, SKIP=8, SMOOTH=1)
  → CHAIN: sequence.py, fades 2-4s, black holds 2-3s
  → journey_complete.mp4 (both endpoints exact, continuous identity)
```

Validation happens ONCE per storyboard. After that, the frames are fixed
checkpoints — etching animates BETWEEN them, never regenerating them.
