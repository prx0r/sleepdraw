#!/usr/bin/env bash
# r2sync.sh — factory transport. pull <slug> | push <slug> | bank
# Creds: R2_ACCESS_KEY / R2_SECRET_KEY / R2_ENDPOINT (+ R2_BUCKET) in env.
# Never committed — export in shell, never in a file.
set -euo pipefail
BUCKET="${R2_BUCKET:-blog-video-assets}"
WORK="/root/sleepdraw/runs/studio/work"
PACKS="/root/sleepdraw/runs/studio/packs"
VOICE="/root/sleepdraw/runs/studio/voice"

need_creds() {
  : "${R2_ACCESS_KEY:?export R2_ACCESS_KEY first (see pack/R2-LAYOUT.md)}"
  : "${R2_SECRET_KEY:?export R2_SECRET_KEY first (see pack/R2-LAYOUT.md)}"
  : "${R2_ENDPOINT:?export R2_ENDPOINT first (see pack/R2-LAYOUT.md)}"
  export AWS_ACCESS_KEY_ID="$R2_ACCESS_KEY" AWS_SECRET_ACCESS_KEY="$R2_SECRET_KEY"
}
s3() { aws --endpoint-url "$R2_ENDPOINT" s3 "$@"; }

cmd="${1:-}"; slug="${2:-}"
free_gb() { df -BG / | awk 'NR==2{gsub("G","",$4); print $4}'; }
case "$cmd" in
  pull)
    need_creds; [[ -n "$slug" ]] || { echo "usage: r2sync.sh pull <slug>"; exit 1; }
    # disk guard: refuse rather than fill the box (render-episodes rule: 2G floor)
    if [ "$(free_gb)" -lt 3 ]; then
      echo "REFUSED: <3G free on / — push + wipe a workdir first"; exit 1
    fi
    mkdir -p "$WORK/$slug"
    s3 cp "s3://$BUCKET/fable/packs/$slug.zip" "$WORK/$slug/pack.zip"
    unzip -o "$WORK/$slug/pack.zip" -d "$WORK/$slug/pack"
    # audio: prefer R2 canonical, fall back to local voice bank
    while IFS= read -r a; do
      if s3 ls "s3://$BUCKET/fable/voice/$(basename "$a")" >/dev/null 2>&1; then
        s3 cp "s3://$BUCKET/fable/voice/$(basename "$a")" "$WORK/$slug/"
        s3 cp "s3://$BUCKET/fable/voice/$(basename "$a").json" "$WORK/$slug/" 2>/dev/null || true
      else
        cp "$VOICE/$(basename "$a")" "$WORK/$slug/" 2>/dev/null || echo "WARN: no $a anywhere"
        cp "$VOICE/$(basename "$a").json" "$WORK/$slug/" 2>/dev/null || true
      fi
    done < <(python3 -c "import json;d=json.load(open('$WORK/$slug/pack/meta.json'));[print(x['path']) for x in d['audio']]")
    echo "READY: $WORK/$slug"
    ;;
  push)
    need_creds; [[ -n "$slug" ]] || { echo "usage: r2sync.sh push <slug>"; exit 1; }
    s3 sync "$WORK/$slug/stills/" "s3://$BUCKET/fable/stills/$slug/" --exclude "*" --include "*.jpg"
    s3 cp "$WORK/$slug/$slug-full.mp4" "s3://$BUCKET/fable/finals/"
    s3 cp "$WORK/$slug/thumb.jpg" "s3://$BUCKET/fable/thumbs/$slug.jpg" 2>/dev/null || true
    s3 cp "$WORK/$slug/upload-manifest.json" "s3://$BUCKET/fable/manifests/$slug.json" 2>/dev/null || true
    echo "PUSHED: $slug — verifying, then wiping workdir"
    if s3 ls "s3://$BUCKET/fable/finals/$slug-full.mp4" >/dev/null 2>&1; then
      rm -rf "$WORK/$slug"
      echo "WIPED: $WORK/$slug (box stays lean — R2 is canonical)"
    else
      echo "VERIFY FAILED: workdir kept at $WORK/$slug"
    fi
    ;;
  bank)
    # one-time: migrate local voice bank to R2 canonical
    need_creds
    s3 sync "$VOICE/" "s3://$BUCKET/fable/voice/" --exclude "*" --include "*.mp3" --include "*.json"
    s3 sync "$PACKS/" "s3://$BUCKET/fable/packs/" --exclude "*" --include "*.zip"
    echo "BANKED"
    ;;
  check)
    need_creds
    s3 ls "s3://$BUCKET/fable/" 2>&1 | head
    ;;
  *) echo "usage: r2sync.sh pull|push|bank|check [slug]"; exit 1 ;;
esac
