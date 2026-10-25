# Bailian / Alibaba stack for sleepdraw (2026-10-25)

## What's installed

- **CLI:** `bl` v2.5.1 (updated from 2.1.0 via `bl update`)
- **Config:** `/root/.bailian/config.json`
- **Skills:** installed via `bl skill init` (bailian-gen, bailian-cli, etc.)

## Auth

```json
// /root/.bailian/config.json
{
  "api_key": "sk-ws-H.DHXDMHD...",  // workspace-scoped Singapore key
  "base_url": "https://ws-h6o7g3oq9mc7u24u.ap-southeast-1.maas.aliyuncs.com"
}
```

- **Region:** Singapore (`ap-southeast-1`)
- **Workspace endpoint** (recommended): `ws-h6o7g3oq9mc7u24u.ap-southeast-1.maas.aliyuncs.com`
- **Generic endpoint** (does NOT work with this key): `dashscope-intl.aliyuncs.com`
- Key is workspace-scoped — must use workspace endpoint or get 401
- If key expires: `bl auth login --api-key <new-key>` (get from bailian.console.aliyun.com)

## Image edit (the core tool for six-stage pipeline)

```bash
bl image edit \
  --image <URL> \                    # MUST be a URL, not local path (see below)
  --prompt "<edit instruction>" \
  --model qwen-image-3.0 \           # default, works
  --size 3:4 \                       # or 16:9, 1024*1024, etc.
  --out-dir <dir> \                  # downloads result here
  --out-prefix <name> \
  --seed <n>                         # reproducible
```

### CRITICAL: URL not local path

Local file upload (`--image ./file.png`) hits a DIFFERENT auth endpoint 
and returns 401 "InvalidApiKey" even with a valid key. Workaround:

1. Upload file to R2 (stallshark bucket or any)
2. Generate presigned URL (7-day expiry)
3. Pass URL to `bl image edit --image <url>`

```python
# upload + presign
s3.put_object(Bucket='stallshark', Key='file.png', Body=open('file.png','rb').read(), ContentType='image/png')
url = s3.generate_presigned_url('get_object', Params={'Bucket':'stallshark','Key':'file.png'}, ExpiresIn=604800)
```

### Models available

| Model | What | Cost |
|-------|------|------|
| `qwen-image-3.0` | image edit (default) | free tier (workspace) |
| `qwen-image-2.0` | image generate | free tier (verified working 2026-10-12) |
| `wanx*-imageedit` | stylization, description_edit | free tier |

## Other bl commands (working or tested)

```bash
bl image generate --prompt "..." --model qwen-image-2.0  # t2i, verified
bl text chat --model qwen-flash-character                # chat, verified
bl speech synthesize --model qwen-audio-3.0-tts-flash    # TTS, verified
bl speech recognize --model qwen3-asr-flash              # ASR, needs upload policy (may 401)
bl auth status                                            # check auth state
bl update                                                 # update CLI
```

## Six-stage pipeline (the plan)

```
input plate (any image)
  → [1] rough construction sketch   bl image edit, prompt="loose gesture..."
  → [2] ghost correction            bl image edit, stage1 + corrected proportions
  → [3] rebuild anatomy             bl image edit, stage2 + clean construction
  → [4] structure                   bl image edit, stage3 + clothing/forms
  → [5] details                     bl image edit, stage4 + jewelry/features
  → [6] final ink                   bl image edit, stage5 + complete B&W
  → lora2 draw pipeline animates EACH static plate (techdou skeleton-stroke)
  → sequence.py chains the 6 draws with breaths
```

Two-phase per stage: GENERATE (bl image edit) then ANIMATE (lora2/cli.py make --image).
lora2 is the rendering mechanism — its WB_* knobs make any plate draw itself
hand-drawn. The image model only produces the static input; the draw pipeline
provides the hand-drawn feel.
Cost: ~free on workspace tier (image edit is included).

## Key gotchas

- Local file upload = 401 (use R2 presigned URL workaround)
- Workspace key ≠ generic endpoint (must match)
- `qwen-image-3.0` regenerates rather than pixel-crops — good for style
  transforms, bad for exact crops (use PIL for those)
- Output images land in `--out-dir` as PNG
- `--prompt-extend true` (default) lets the model expand your prompt —
  sometimes helpful, sometimes adds unwanted detail. Set `--prompt-extend false`
  for precise control.
