# HANDOVER-NEXT — read this FIRST (session 2026-10-25 close)

> For the next agent. Where everything is, why it exists, what's open.
> Companion files: `HANDOVER.md` (session log), `AGENTS.md` (rules),
> `docs/JOURNEY-AXIOMS.md` (validation), `docs/JOURNEY-LIBRARY.md` (sources).

## TL;DR — the one thing that works

```bash
python3 /root/sleepdraw/progressive_journey.py --out /tmp/journey.mp4
```
12 pixel-registered checkpoint frames → one continuous drawing video in ~15s.
Pure numpy/OpenCV. No GPU, no model, no fades. This is the journey pipeline.

It reveals stage N+1's diff pixels component-by-component onto stage N's canvas.
14 axioms in `axioms.py` validate any candidate storyboard before use.

## Where everything is

### sleepdraw (this repo)

| Path | What | Why it exists |
|------|------|---------------|
| `progressive_journey.py` | **PRODUCTION** journey renderer | 15s, no deps. The answer to "etch from A to B continuously" |
| `axioms.py` | 14 programmable validation gates | Post-hoc checks (SSIM, edge overlap, saturation) + `encode_prompt()` for model prompts |
| `journey.py` | PROTOTYPE — API stage generation | Kept for reference; replace generation phase with checkpoint etching once validated |
| `continuous_journey.py` v1 | techdou-per-transition (BROKEN: 2h, disk death) | Historical — do not use |
| `continuous_journey_v2.py` | parallel techdou + streaming composite | Untested to completion (disk died at trans 8) |
| `storyboards/journey-pairs.json` | 2,290 labeled pairs (2,287 CIRThan + 3 owner) | start/end zip_keys, 3-level captions, essay mapping. Query: filter by `essay` or `subject` |
| `storyboards/cirthan/` | CIRThan captions + splits (GitHub clone) | 3-level text descriptions = journey prompt chain (L1 sketch, L2 construction, L3 final) |
| `storyboards/01..03-stage-*.png` + `manifest.json` | Owner's 3 twelve-stage prototypes | **THE checkpoints.** Pixel-registered 620x900. Stage1=sketch, Stage12=exact final |
| `docs/JOURNEY-AXIOMS.md` | 14 axioms + 8-stage reference + pipeline summary | Validation gates, not suggestions |
| `docs/JOURNEY-LIBRARY.md` | All source inventory (CIRThan, HAR, iconometry, Kaggle, Trika images) | Where to find pairs, guides, datasets |
| `docs/BAILIAN-STACK.md` | Alibaba/Bailian CLI + endpoint quirks | **Gotcha: workspace endpoint, URL-not-local-path (local upload = 401)** |
| `lora1.yaml` `lora2.yaml` `lora2-corbin.yaml` `lora3.yaml` | Locked style presets | Do not drift — new look = new file |
| `AGENTS.md` | Rules + pipeline section + file map | Read first every session |
| `HANDOVER.md` | Session log (2026-09-27 + 2026-10-25) | History |
| `journey.py` → `runs/` | Generated outputs | Last 5 runs kept; older cleaned |

### quill-app (`/root/manuscriptAI`, repo `prx0r/quill-app`)

| Path | What |
|------|------|
| `src/components/canvas/CanvasChat.tsx` | Journey director chat — persistent, sees canvas, calls `/journey`, model detection |
| `src/components/canvas/WriteCanvas.tsx` | Canvas: blocks, resize, images (`![label](url)`), video embeds, delete, split |
| `deploy/worker.ts` | Cloudflare Worker: `/journey` (Bailian proxy, BAILIAN_KEY secret), `/v1/chat`, canvas static assets |
| `AGENTS.md` | Session notes: video embeds, model selection, multi-ref, journey skill |
| `skills/JOURNEY.md` + `public/skills/JOURNEY.md` | Journey director system prompt (14 axioms encoded) |

**Live:** https://quill.agi.みんな — canvas at `?canvas=new`. Deploy: `WEB=1 npm run build` + `wrangler deploy` from `deploy/` (see AGENTS.md).

### External

| Path | What |
|------|------|
| `/root/engines/` | 7 cloned drawing-animation engines + `.venv` (whiteboard-video-engine, whiteboard-animator, Sketch2Motion, PaintTransformer, plottter, daub, codex-skill). Trimmed of examples. |
| `/root/.bailian/config.json` | Bailian Singapore workspace key — **workspace endpoint only, NOT dashscope-intl** |
| `/root/.cf-api-token` | Cloudflare deploy token (600) |
| R2 `uploads/` | CIRThan zips: `sketch-*.zip` (2GB) + `image-*.zip` (2×2GB) — ranged-read, never full download |
| R2 `stallshark/` | `journey/` exports, storyboards upload, engine comparison MP4s |
| R2 `sacred-art/` | wikiart/symbolism images + `raw/artdl/ArtDL.zip` (Christian saints, 3.6GB) |

## Engine comparison (verified this session)

| Engine | Job | Notes |
|--------|-----|-------|
| **progressive_journey.py** | **journey rendering (production)** | 15s, component reveal, no deps |
| whiteboard-video-engine | stroke-by-stroke + colour reveal from source image | `/root/engines`, `--source-image` flag, 30 styles |
| whiteboard-animator | quick single-image previews | pip install, CPU-only |
| techdou (lora1/lora2/lora3) | sleep-channel etch aesthetic (white-on-black) | **stays for sleep channels, NOT for journeys** |
| LayerInbetween (GitHub) | line-drawing inbetweening (SIGGRAPH 2026) | Not cloned — needs torch+weights; alternative if progressive isn't enough |

## Bailian image models (Singapore, verified prices CNY)

`qwen-image-2.1-turbo` 0.10 (10 refs) · `qwen-image-3.0` 0.18 (default) ·
`wan2.7-image` 0.20 (9s, multi-panel storyboard) · `qwen-image-3.0-pro` 0.25 ·
`wan2.7-image-pro` 0.50 (9 refs) · `qwen-image-2.0-pro` 0.50 (n=6 outputs)

Worker `/journey` takes `{image_url|image_urls[], prompt, model, seed, size, n}`.
Chat detects model names. wan2.7-image generated an 8-panel journey grid from
sketch+final in ONE call — the checkpoint generator.

## Open threads (priority order)

1. **Test progressive_journey on a 2nd pair** (fetch from zip → render → watch).
   Confirms generalization beyond storyboard 01.
2. **The real drawing aesthetic** — owner wants "beautiful slow thin etch" drawing
   continuously. progressive_journey fades pixels (fast but not hand-drawn).
   Next candidates: LayerInbetween (line-art inbetweening) or whiteboard-video-engine
   per-transition with `--source-image`. Experiment, don't overbuild.
3. **twelve-generation checkpoint factory** — wan2.7-image multi-panel or
   qwen-image-2.0-pro n=6 (two calls for 12) → validate with axioms.py → render.
4. **Disk** — 96%, 3.6G free. Old runs cleaned this session. Biggest eaters outside
   this repo (projects 6.3G, gcomedy 3.1G). Stream to R2, never download big zips.
5. **FAL_KEY missing** — unlocks ROADMAP item 6 (Uni-1 masters, img2img ladder).
6. **quill-app canvas** — journey chat + video + model selection live; verify
   end-to-end in browser (not just Playwright).
7. **Backups intact** — quill-app stash `backup-dirty-before-live-2026-10-24` +
   `/tmp` file backups exist; tantraessays pushed clean.
8. **`journey.py`** — either delete or rewrite with checkpoint etching (docs say replace).

## House rules (unchanged, load-bearing)

- lora1/lora2/lora2-corbin/lora3 locked — new look = new file.
- Secrets never in repo: `/root/.r2-env`, `/root/.cf-api-token`, `.bailian/config.json`.
- CIRThan images: ranged-read zips (~5s), never full download (5.4GB).
- quill deploy: `WEB=1 npm run build` + `wrangler deploy` from `deploy/` ONLY.
- NEVER restart box bridge (port 18787) until canvas endpoints reconstructed in-repo.
- No text in essays unless from a verified source or high-signal analysis of one.
