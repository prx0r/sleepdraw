"""Cloudflare Workers AI image provider (FLUX schnell, no other keys needed).

config requires: CF_API_TOKEN (or CLOUDFLARE_API_TOKEN), CF_ACCOUNT_ID
config optional: CF_IMAGE_MODEL (default @cf/black-forest-labs/flux-1-schnell)
"""

import base64
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError

from providers.base import GeneratedImage, validate_config

DEFAULT_MODEL = "@cf/black-forest-labs/flux-1-schnell"
DEFAULT_ACCOUNT = "954612afb5a97bb15dddcdc70176813d"


def generate(prompt, aspect_ratio, output_dir, config, context=""):
    token = (config.get("CF_API_TOKEN") or config.get("CLOUDFLARE_API_TOKEN") or "").strip()
    account = (config.get("CF_ACCOUNT_ID") or DEFAULT_ACCOUNT).strip()
    if not token:
        validate_config(["CF_API_TOKEN"], config, "Cloudflare")
    model = (config.get("CF_IMAGE_MODEL") or DEFAULT_MODEL).strip()
    url = f"https://api.cloudflare.com/client/v4/accounts/{account}/ai/run/{model}"
    body = {"prompt": prompt}
    req = Request(url, data=json.dumps(body).encode("utf-8"), method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", f"Bearer {token}")
    try:
        with urlopen(req, timeout=180) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except HTTPError as e:
        raise RuntimeError(
            f"{context}Cloudflare AI error HTTP {e.code}: {e.read().decode('utf-8', errors='replace')[:300]}"
        ) from e
    try:
        image_bytes = base64.b64decode(data["result"]["image"])
    except (KeyError, ValueError) as e:
        raise RuntimeError(f"{context}Cloudflare AI returned no image: {json.dumps(data)[:200]}") from e
    return GeneratedImage(image_bytes=image_bytes, ext="jpg", metadata={"model": model})
