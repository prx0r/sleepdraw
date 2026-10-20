#!/usr/bin/env bash
# overnight.sh — unattended factory loop (the characters2 LOOP.md tick, for video).
# Queue -> per slug: pull -> stills check -> build -> gate -> comply -> push -> receipt.
# Stops at human gates (upload approval, cast locks). Writes morning review.
# Usage: overnight.sh [--live] [slug...]   (default: dry-run from packs/queue.txt)
# Cron: 0 2 * * * /root/sleepdraw/pack/overnight.sh --live >> /root/sleepdraw/pack/overnight.log 2>&1
set -uo pipefail
PACKDIR=/root/sleepdraw/runs/studio/packs
WORK=/root/sleepdraw/runs/studio/work
R2=/root/sleepdraw/pack/r2sync.sh
LIVE=0; SLUGS=()
for a in "$@"; do
  [ "$a" = "--live" ] && LIVE=1 || SLUGS+=("$a")
done
if [ ${#SLUGS[@]} -eq 0 ] && [ -f "$PACKDIR/queue.txt" ]; then
  mapfile -t SLUGS < <(grep -v "^#" "$PACKDIR/queue.txt" | grep -v "^$" || true)
fi
[ ${#SLUGS[@]} -eq 0 ] && { echo "queue empty (packs/queue.txt or args)"; exit 0; }
DATE=$(date +%F)
REVIEW="$PACKDIR/morning-review-$DATE.md"
[ $LIVE = 1 ] && { echo "# Morning review $DATE" > "$REVIEW"; echo >> "$REVIEW"; echo "## Content (gates ran, $0)" >> "$REVIEW"; }
run() { [ $LIVE = 1 ] && eval "$@" || echo "DRY: $*"; }
# 0. content stage — channels write/gate text first (P0 sources, P1 drafts)
for ch in folk-and-fable etymology; do
  echo "=== content: $ch ==="
  if [ $LIVE = 1 ]; then
    OUT=$(python3 /root/damn/fish/content.py "$ch" 2>&1 | tail -6)
    echo "$OUT"
    echo "- $ch: $OUT" >> "$REVIEW"
  else
    echo "DRY: python3 fish/content.py $ch"
  fi
done
[ $LIVE = 1 ] && { echo >> "$REVIEW"; echo "## Factory (build/gate/push, R2 staging)" >> "$REVIEW"; }
for slug in "${SLUGS[@]}"; do
  echo "=== $slug ==="
  # 1. pull (fails closed on no creds / <3G disk — r2sync enforces)
  run "$R2 pull $slug" || { echo "SKIP $slug: pull failed"; [ $LIVE = 1 ] && echo "- $slug: SKIP pull failed" >> "$REVIEW"; continue; }
  W="$WORK/$slug"
  # 2. stills present?
  if ! ls "$W/stills/"*.jpg >/dev/null 2>&1; then
    echo "SKIP $slug: no stills (render vision prompts first)"
    [ $LIVE = 1 ] && echo "- $slug: NEEDS STILLS (human: render pack prompts)" >> "$REVIEW"
    continue
  fi
  # 3. segments baked?
  if grep -q "TBD" "$W/segments.txt" 2>/dev/null; then
    echo "SKIP $slug: segments unbaked"
    [ $LIVE = 1 ] && echo "- $slug: NEEDS SEGMENTS (bake durations)" >> "$REVIEW"
    continue
  fi
  # 4. thumb from first still (deterministic, no AI)
  FIRST=$(ls "$W/stills/"*.jpg | head -1)
  run "ffmpeg -y -v error -i $FIRST -vf scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720 -q:v 3 $W/thumb.jpg"
  # 5. build
  run "bash $W/build.sh" || { echo "FAIL $slug: build"; [ $LIVE = 1 ] && echo "- $slug: BUILD FAILED (investigate)" >> "$REVIEW"; continue; }
  FINAL="$W/$slug-full.mp4"
  # 6. manifest (draft) + gate + comply
  [ $LIVE = 1 ] && python3 -c "
import json
m = json.load(open('$W/pack/meta.json'))
tales = [t for t in [l.split('|')[0] for l in open('$W/segments.txt') if l.strip() and not l.startswith('#')] if t]
json.dump({'title': m.get('title', '$slug') + ' — Read Whole, Slowly for Sleep',
 'description': m.get('title', '$slug') + ', read whole and slowly for sleep. Public-domain text.',
 'tags': ['sleep stories', 'bedtime stories for adults', 'read aloud'],
 'categoryId': '27', 'madeForKids': False, 'privacyStatus': 'unlisted',
 'chapters': [{'start': '?:??', 'title': t} for t in tales],
 'sources': {}}, open('$W/upload-manifest.json', 'w'), indent=1)"
  [ $LIVE = 1 ] && python3 /root/damn/fish/gate_pack.py --final "$FINAL" --thumb "$W/thumb.jpg" \
    --manifest "$W/upload-manifest.json" --segments "$W/segments.txt" --audio-dir "$W" \
    --profiles /root/damn/projects/folk-and-fable/profiles.json --channel folk-and-fable \
    > "$W/gate.json" 2>&1
  if [ $LIVE = 1 ] && ! python3 -c "import json,sys; sys.exit(0 if json.load(open('$W/gate.json'))['ok'] else 1)" 2>/dev/null; then
    echo "FAIL $slug: gates"
    echo "- $slug: GATES FAILED (see workdir gate.json; human: fix or exception)" >> "$REVIEW"
    continue
  fi
  # 7. push (R2 staging only — YouTube upload stays human-gated, always)
  run "$R2 push $slug" || { echo "FAIL $slug: push"; [ $LIVE = 1 ] && echo "- $slug: PUSH FAILED" >> "$REVIEW"; continue; }
  [ $LIVE = 1 ] && echo "- $slug: BUILT+GATED+PUSHED ($FINAL on R2 fable/finals/; upload-manifest ready for human)" >> "$REVIEW"
  echo "OK $slug"
done
[ $LIVE = 1 ] && echo "(human next: cast locks, thumb picks, upload approvals — see table)" >> "$REVIEW"
echo "done. review: $REVIEW"
