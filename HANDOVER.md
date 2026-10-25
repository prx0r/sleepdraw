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

---

# HANDOVER — session 2026-10-25 (journey engine + engine comparison)

Read this + AGENTS.md + docs/JOURNEY-AXIOMS.md + docs/JOURNEY-LIBRARY.md.

## What shipped this session

### 1. Journey pipeline (the core deliverable)

**`progressive_journey.py`** — THE ANSWER. 12 pixel-registered checkpoints →
one continuous drawing video in **15 seconds** (pure numpy/OpenCV, no GPU,
no model). Component-by-component reveal: stage N is the base, stage N+1's
diff pixels appear largest-first over 40 frames. No fades, no black, no
canvas reset. Result: 520 frames, 34.7s, 1.2MB.

```bash
python3 progressive_journey.py --out journey.mp4
```

- **`continuous_journey.py`** (v1, superseded) — used techdou per transition,
  too slow (2h) and too much disk (libpng errors at 97% disk). Kept for reference.
- **`continuous_journey_v2.py`** — parallel techdou renders + streaming composite.
  Not tested to completion (disk died at transition 8). Faster but still heavy.

### 2. The 14 journey axioms

**`axioms.py`** — programmable validation gates. Each axiom is a function
(prev_img, next_img, ...) → (pass, detail). Post-hoc validators for: exact
endpoints (hash), stroke continuity (edge overlap), small transitions (density
ratio), conserved geometry (SSIM), material continuity (saturation), progressive
colour (saturation monotonic), locality (changed regions), hidden work (new ink
in empty space), final convergence (SSIM to target). Prompt-encoded: artist
causality, cumulative progress, purposeful exploration, continuous identity,
no arbitrary quota. `encode_prompt(stage, total)` builds the model prompt suffix.

**docs/JOURNEY-AXIOMS.md** — full text of all 14 + the 8-stage reference trajectory.

### 3. Journey-pair database (2,290 entries)

**`storyboards/journey-pairs.json`** — 2,287 CIRThan pairs + 3 owner storyboards.
Each entry: start/end zip_keys (ranged-read from R2 zips, ~5s each, zero disk),
subject, level1/2/3 captions, essay mapping (531 devotion, 315 rebirth, 263
energy, 177 roots, 110 yogini, 302 Trika-adjacent). Captions in
`storyboards/cirthan/` (from github.com/jinyuxu-whut/CIRThan). Paper saved.

### 4. Three owner storyboard prototypes (the reference examples)

`storyboards/01-stage-01..12.png` + `manifest.json` — three 12-stage journeys
(GEOMETRY TO GESTURE / FLOW OF MUSIC / HALO BECOMES A GARDEN). Pixel-registered,
620x900, with exact_source/exact_target constraints. **These ARE the checkpoints.**

### 5. Engine comparison (same sketch, 4 engines)

| Engine | Style | Key finding |
|--------|-------|-------------|
| whiteboard-video-engine | crisp pen + hand + contour-wipe colour | **best for journey** (colour grows from drawing) |
| whiteboard-animator | flat, fast monochrome | good for quick previews |
| techdou lora1 | beige paper, white-on-black glow | sleep-channel minimal |
| techdou lora2 | black canvas, slow shade fill | **sleep-channel etched (stays)** |

Installed at `/root/engines/` (venv: `/root/engines/.venv`), 7 repos cloned.
whiteboard-video-engine has `--source-image` for colour reveal from reference +
30 style presets + hand cursors. whiteboard-animator: `pip install whiteboard-animator`.

### 6. Bailian/Qwen image models (Singapore workspace)

Config: `/root/.bailian/config.json` (workspace endpoint, NOT dashscope-intl).
Worker `/journey` endpoint accepts `{image_url|image_urls[], prompt, model, seed, size}`.
Chat detects model names: `wan2.7-image`, `qwen-image-2.1-turbo`, etc.

Prices (CNY → USD ≈ ×0.14): turbo 0.10 · qwen3.0 0.18 · wan2.7 0.20 (fastest, 9s) ·
qwen3.0-pro 0.25 · wan2.7-pro 0.50 · qwen2.0-pro 0.50 (n=6 outputs).

**wan2.7-image multi-panel**: generated an 8-panel storyboard grid from sketch+final
in ONE call — the checkpoint generator.

### 7. Six-step deity tutorial

`assets/six-step-deity-tutorial.png` — owner's construction reference (6 stages:
original → ghost reposition → rebuild anatomy → structure → details → final ink).
Encoded as stage archetypes in AGENTS.md.

### 8. Axioms encoded in repo

AGENTS.md: pipeline section (validate → etch transitions → chain).
docs/JOURNEY-AXIOMS.md: pipeline summary + axiom table.
journey.py: docstring marks it PROTOTYPE (API generation → replace with checkpoint etching).
skills/JOURNEY.md (quill-app): journey director skill with axioms.

## Open threads

- **progressive_journey.py** is the production pipeline. Test on other pairs
  (fetch pair from zip → progressive_journey → watch).
- **Engine choice**: whiteboard-video-engine for colour-reveal stages; progressive
  for structure stages. Possible hybrid: progressive for line stages, whiteboard
  for colour stages.
- **wan2.7-image multi-panel** can generate fresh 12-stage checkpoints from
  sketch+final in one call — test with n=6 twice for 12.
- **FAL_KEY** still missing (ROADMAP item 6).
- **Disk**: 97% full. Old runs in `runs/` can be cleaned (portrait 165M,
  yuki-* ~50M each). Engine test debris in /root/engines (~490M).
- **quill-app canvas**: persistent chat, journey model selection, video embeds
  all live. AGENTS.md in manuscriptAI/ has full docs.

## Key commands

```bash
# Journey pipeline (the main thing)
python3 /root/sleepdraw/progressive_journey.py --out /tmp/journey.mp4

# Extract a pair from R2 zips (ranged read, ~5s)
python3 -c "import sys; sys.path.insert(0,'/root/sleepdraw'); ..."  # see journey-pairs.json keys

# Bailian image edit
bl image edit --image <r2_url> --prompt "..." --out-dir /tmp

# Engine comparison
/root/engines/.venv/bin/whiteboard render-image sketch.png --source-image final.png --color-fill contour-wipe -o out.mp4
```
