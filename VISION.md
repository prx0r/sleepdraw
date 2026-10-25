# VISION — view, render, push (and why each leg is where it is)

Owner's ask: a dashboard to simply view created content, click render,
push to YouTube. Status of each leg, honestly:

## 1. VIEW — done, works for you today

`outputs.moltwork.com/review` — channel grids, all videos inline,
approve/reject. Edge Worker + R2, same path as the mp4s you already watch.
If this page ever fails you, it is NOT us — retest with a direct mp4 link;
same worker, same edge.

## 2. RENDER — works, but only I can click it. That's the gap.

Renders run on this box (CPU, 1–6 min). The Studio tab triggers them — but
the Studio lives behind the tunnel, and the tunnel 404s for you (proven:
your requests never arrive; log shows only mine). So today: you ask, I click.

The fix (queued, small): **R2 job queue.** Edge review page gets a
"render this" button → writes `powoutputs/jobs/<id>.json` → a 30-line poller
on this box picks it up, renders, uploads, marks done. Same edge path that
works for you, no tunnel involved. No Cloudflare product does this for us;
it's ~100 lines across worker.js + a poller. This is the actual missing piece.

## 3. PUSH TO YOUTUBE — blocked on Google, not us. One browser flow by you.

Uploads cannot use our API key (read-only public data). YouTube demands:
- **OAuth consent, once, in YOUR browser**: Google Cloud project → authorize
  `youtube.upload` → refresh token stored in our vault. Nobody can do this
  for you — Google requires the channel owner to click. ~10 minutes.
- **Quota**: one upload costs ~1,600 of 10,000 daily units → ~6 uploads/day
  until Google approves a quota increase (form + wait).
- **Paperwork per upload**: self-declare made-for-kids, category, license —
  defaults cover it, but it's a form, not a button.

After your one consent click, `powvid/shorts/upload.py` (already built,
Jev-gated, fail-closed) does the rest: unlisted → you flip public.

## Why the tunnel saga ate the day (so we never repeat it)

- Quick tunnels 404 at the edge during setup; named tunnel needed creds that
  are gone from this box; SIGHUP doesn't reload cloudflared (restart only).
- The killer: per-client edge splits are REAL — 200 for me, 404 for you,
  same URL, same minute, and the tunnel log proved your packets never
  arrived. No config fixes that. Lesson enshrined in
  influence/dash/HOSTING.md: check arrival first; if absent, pivot to edge.
- Cloudflare docs cover none of this per-client behavior; the docs path
  (tunnel troubleshooting) assumes requests arrive. Ours didn't.

## Order of attack

1. R2 job queue (render button on the working page). ← the unlock
2. Your OAuth click (10 min, then uploads work forever).
3. Quota increase form (only when 6/day binds).
