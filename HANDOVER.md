# HANDOVER — sleepdraw session 2026-09-27 (for next agent)

Read this + AGENTS.md + lora1.yaml + lora2.yaml + styles/corbin.md. You are current.

## What this is

sleepdraw = tiny B&W slow-draw engine room. FLUX pencil art → 16:9 crop →
skeleton-stroke draw → R2 test channel → fade-chained sequences. Variants game:
new art OR new knobs per round, never both. Owner reviews on dash + R2 links.

## Locks (do not drift)

- **lora1 (pen)**: minimal art, 30s, SKIP 8 / SPLIT 5 / SMOOTH 1 / LIGHT 1 /
  black canvas / no hand. Ref: assets/moon-lora1-flux-pencil.jpg.
- **lora2 (etched)**: dense intaglio, 2min, same + COLOR_W 3 / BRUSH 10.
  Ref: assets/farm-lora2-flux-pencil.jpg.
- **lora2-corbin**: imaginal preset (miniature space, pencil medium, gold
  accent #D4A94E). Ref: assets/corbin-garden-lora2-flux-pencil.jpg.
- **Outro law**: 15s fade to black + 5s black wait baked per clip (fixed,
  therapeutic — owner's call, not varied).
- No LoRA training, ever (owner: prompts > weights, more freedom).

## Engine patches (vendor/techdou/scripts/generate_whiteboard.py)

1. WB_SKETCH_LIGHT: sketch bright pixels (white-on-black invisible otherwise —
   sketch only painted <10).
2. WB_SPLIT env (default 10; we use 5 — 10px pops read as blocks).
3. WB_SMOOTH: skeleton path (Zhang-Suen thin → CC grain filter → endpoint
   walk → AA polyline via reveal mask → pen lifts on gaps). Falls back to cells.
4. Ink from luminance directly (adaptive threshold inverts on dark art: 98% white).
5. Default cell path untouched (XMR etc. unaffected).

## Decisions this session (all owner-approved)

- sleepdraw = separate repo (prompt styles per channel, each film = variants).
- Studio lives in /root/influence dash (Content → Sleep Studio tab), powered
  ONLY by sleepdraw. Chat agent has `studio` verbs + plain-English bridge.
- Test channel: R2 powoutputs/test/. Finals: powoutputs/films/<film>/.
- Film machine: new → bible → flow → bench → board → shot → status → sequence.
- One 3h Corbin film (sleep genre rewards length), produced in halves (01–03, 04–07).
- 5-min chapters hour one, then black + bed. Images hold up to 10 min each.
- Real manuscript images = holds/inspiration only (draw of dense miniatures
  fragments); FLUX-minimal draws.
- Voices: edge-tts now (aria/guy/ana/christopher, -5%/-2Hz); Qwen3/Kaggle later.
- fal: flux-2/edit $0.024/img, breathe LTX-2 fast $0.016/s, Wan 3 $0.10/s 720p
  (API-only, no weights — verified). FAL_KEY STILL MISSING — ask owner.
- 30fps before scaling (halves 40–60MB files).

## State right now

- Corbin-01 shots 1–4 DONE: garden (banked), map-compass, veil-stars,
  green-guide — all lora2-corbin, 2min + 15s fade + 5s black, shipped to
  powoutputs/films/corbin-01-map/. Next: shots 5–7 (mihrab, heliotrope/gold, throne).
- Flow: films/corbin-01-map/flow.md (12 shots). Bench: shots-bench.md (25).
- Board: cli.py board/shot/status/new. Sequence: sleepdraw/sequence.py.
- Studio: influence dash Sleep Studio (art/knobs/render/publish/voice) +
  MCP studio.* + chat `studio` verbs. Dash live via serve.sh --tunnel.
- R2 test ≈ 173MB+; dash worker redeployed (query-token auth); DASH_TOKEN rotated
  (copy: powvid/dash/.token-powoutputs, 600).
- Vault: /root/.r2-env (CF+R2, 600). Kaggle: /root/.kaggle/access_token (600).
- Repos + remotes: sleepdraw (NEW, unpushed), powvid/powvid (+vendor patch),
  sleepintel (+jev fixes, REVIEW/AUDIT), tubeintel (+ledger fix), influence
  (+studio/chat — UNCOMMITTED, commit before push).

## Docs map

- styles/corbin.md (bible) · films/corbin-01-map/flow.md + shots-bench.md
- docs/: fal-flux2-edit.md, STACK.md, FUTURE.md (wan3 verdict, self-host, audio)
- COSTS.md (~$0.70 full-fal film) · SEQUENCES.md (verbs, morph plan)
- assets/library.json (tagged casting pool) · assets/registry.json (R2 clips)

## Next (in order)

1. Corbin-01 shots 5–7 (mihrab lora1, heliotrope/gold lora1, throne lora2).
2. Muxer: chapter TTS + clip + bed marry (ffmpeg plumbing).
3. FAL_KEY → breathe.py + stillness matrix; then morph cheats.
4. Corbin intro/logo asset (gold girih star, 8s).
5. Push cadence: commit per feature, push when owner says.

## Session 2026-09-28 — lora3 fineliner + Yuki master-arc (all night, $0)

Owner verdicts drove everything: width variants identical (wrong variable) →
rhythm L2 deep wins → wave-smoothing fixes jitter → 1px pencil point →
staged acts + engine gold ritual → master-arc wedge → checkpoint ladder →
color target. lora3 LOCKED (see lora3.yaml).

Engine patches (vendor/techdou/scripts/generate_whiteboard.py):
- WB_RHYTHM 1/2: curvature pacing + lift pauses, wave-smoothed costs, same frames.
- WB_LINE: pen point px override (1 = pencil). WB_AA 2 = supersample sub-pixel.
  WB_INK <255 = faint-line feel. "0"/"" both parse as off (fixed 9/28).
- WB_ACTS N + WB_ACT_PAUSE_S: y-band staged reveal, breaths between acts.
- WB_GOLD waypoints: reserved from ink+fill, progressive ritual in hold phase
  (fill can never erase it). Flux must NOT paint gold.
- Bug caught by pixel audit: stray line doubled hold frames in gold runs
  (fixed). KNOB_KEYS extended in sleepdraw/draw.py. cli.py make: --preset flag
  (recipe honesty).
- art.py: new "photo" style (color masters via CF flux, free).

Art direction (styles/yuki.md): fineliner brief locked; 16:9 crop keeps y 22-78%;
moons land top-edge (compose without them); signatures/glyphs (regen hardened);
flux will not paint gold (engine owns it).

Shipped (R2 powoutputs/test/, dash review queue): yuki-doorway-hero (2min),
yuki-full-v1 (5-plate chain), wave/pencil/thinAA/faint/ritual variants,
yuki-ladder.jpg (5-stage checkpoint contact sheet), master-v4 + color-v1.
Yuki-Onna text measured: 7,968 chars, 11-12 min, $0.08 Eleven v4 (/tmp files).

Open threads: FAL_KEY missing (Uni-1 masters, img2img stages, Inworld shootout).
Morph/overdraw/boil/hatchfill/inkwash/pen-scratch/checkpoint-scheduler/longform
→ docs/ROADMAP.md. Yuki film assembly → films/yuki/.
