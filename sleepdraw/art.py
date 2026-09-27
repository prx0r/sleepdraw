"""FLUX art for sleepdraw: white-on-black minimal scenes via Cloudflare Workers AI."""
import base64
import json
import os
import time
import urllib.request

MODEL_IDS = {
    "flux": "@cf/black-forest-labs/flux-1-schnell",
    "sdxl": "@cf/stabilityai/stable-diffusion-xl-base-1.0",
    "lightning": "@cf/bytedance/stable-diffusion-xl-lightning",
    "dreamshaper": "@cf/lykon/dreamshaper-8-lcm",
    # House pick for islamic line work (mihrab/girih/lamp grammar, free tier).
    # flux-2-dev + klein need multipart input — unsupported, do not add.
    "lucid": "@cf/leonardo/lucid-origin",
}

STYLES = {
    "pencil": ("Delicate white pencil sketch on pure black background. "
               "Fine monochrome linework, moonlit etching style. "
               "No text, no letters, no numbers, no words."),
    "paper": ("Hand-drawn black marker whiteboard sketch on warm white paper "
              "background. Minimalist doodle style. No text, no letters, no numbers, "
              "no words."),
    "chalk": ("Hand-drawn glowing marker sketch on dark charcoal blackboard "
              "background. Chalk style, minimalist doodle. No text, no letters, "
              "no numbers, no words."),
}

HOUSE_RULES = ("wide landscape composition; extremely minimal: one subject + "
               "vast empty ground; no text ever (garble risk); dense art "
               "cannot be drawn in 30s — sparse wins.")


def generate(prompt, token, account, model="flux", style="pencil"):
    import urllib.error
    if model not in MODEL_IDS:
        raise ValueError(f"model? {sorted(MODEL_IDS)}")
    if style not in STYLES:
        raise ValueError(f"style? {sorted(STYLES)}")
    body = json.dumps({"prompt": f"{STYLES[style]} Subject: {prompt}"}).encode()
    url = (f"https://api.cloudflare.com/client/v4/accounts/{account}"
           f"/ai/run/{MODEL_IDS[model]}")
    for attempt in range(4):
        try:
            req = urllib.request.Request(
                url, data=body,
                headers={"Authorization": f"Bearer {token}",
                         "Content-Type": "application/json"})
            resp = urllib.request.urlopen(req, timeout=180)
            raw = resp.read()
            if resp.headers.get("Content-Type", "").startswith("image/"):
                return raw
            return base64.b64decode(json.loads(raw.decode())["result"]["image"])
        except urllib.error.HTTPError:
            if attempt == 3:
                raise
            time.sleep(15)
