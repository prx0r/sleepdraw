# R2 FACTORY LAYOUT — fable pipeline without disk pressure

Bucket: `blog-video-assets` (same bucket the powoutputs-dash worker reads).
Box holds ONLY the active video. Everything else lives on R2.

```
fable/
  voice/          # canonical voice bank (masters + .json sidecars, ~5GB, upload once)
  packs/          # 22 slim pack zips (KBs — also fine in git, mirrored here)
  stills/<slug>/ # rendered tableau stills, 16:9 jpgs (~1-2MB each)
  finals/         # finished uploadables <slug>-full.mp4 (~30MB ea at practice grade)
  thumbs/         # thumbnail finals (1280x720)
  cue/            # cue.yaml + segments.txt per uploadable (edit in place)
```

## Factory loop (per video, box never holds more than one)
1. `r2sync.sh pull <slug>` — fetch pack zip + its audio master(s) to runs/studio/work/
2. Render stills (vision model, from pack prompts) → `work/<slug>/stills/`
3. Fill `segments.txt` durations → `./build.sh` → `<slug>-full.mp4`
4. `r2sync.sh push <slug>` — upload stills + final + thumb; verify sha; `rm -rf work/<slug>`
5. Next slug. Disk steady at ~200MB transient regardless of scale.

## Storage math (whole channel)
Voice 5GB + stills ~0.5GB + finals ~1.2GB + packs KBs ≈ **under 7GB** —
inside R2's 10GB free tier. Box needs ~2GB scratch (one audio + one render).

## Disk policy (the box never grows)
- R2 is canonical; the box is scratch. `push` verifies the final on R2,
  then wipes the workdir automatically. `pull` refuses under 3G free.
- Voice bank stays local (owner call) AND on R2 — if `/` drops under 10G,
  thin local `voice/` to R2-only (`fable.pull` fetches per pack anyway).
- Logs: dash logs truncate (BrokenPipe noise), journal vacuum when >500M.
- Git: media never enters git (mp4/mp3/wav/png/scenes gitignored everywhere).
  Big `.git` dirs (pogpet 577M of STL/GLB history) need owner-approved
  `filter-repo` — gc alone won't shrink them.
- Practice renders (e.g. `yuki-practice-full.mp4`, stand-in still + pre-lock
  voice) are proof artifacts, not inventory — delete before they confuse anyone.

## Credential setup (OWNER ACTION, one time)
Direct S3 keys on this box are dead (rotated — Unauthorized on every call),
rclone remotes are stale, wrangler is logged out. To switch the factory on:
1. Cloudflare dashboard → R2 → `blog-video-assets` → Manage API tokens →
   Create token with **Object Read & Write**, scope to this bucket.
2. Paste the three values (access key, secret, endpoint stays
   `https://<account>.r2.cloudflarestorage.com`) — I configure + verify,
   migrate the voice bank, and the factory runs.
Alternative (no keys): I add an authed POST upload route to
powvid/dash/worker.js; you `wrangler deploy` it from your laptop.
Keys are better for 100MB+ files — rclone multipart, resumable.
