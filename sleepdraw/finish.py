"""finish.py: the AI finish step — human sketch + construction etch in,
finished B&W linework out. FLUX.1 Kontext [dev] on fal (multi-reference edit).

Usage (via cli.py finish) or direct:
    finish(sketch_path, construction_path, out_path, key=..., style="thangka")
"""
import json
import os
import time
import urllib.request

ENDPOINT = "https://fal.run/fal-ai/flux-kontext/dev"

HOUSE_FINISH = {
    # style: instruction template. {extra} = caller addition. The two refs
    # arrive side-by-side in ONE image: LEFT = the hand, RIGHT = geometry.
    "thangka": ("Two reference sketches side by side. LEFT image: imitate this "
                "HAND — loose confident strokes, uniform weight, plain white. "
                "RIGHT image: keep this GEOMETRY completely — every contour, "
                "ornament and figure, nothing dropped. Output a single clean "
                "finished black-and-white ink sketch: the right image redrawn "
                "in the left image's hand. No shading blocks, no text, "
                "no signature. {extra}"),
    "alchemy": ("Two reference sketches side by side. LEFT image: imitate this "
                "HAND. RIGHT image: keep this GEOMETRY completely. Output a "
                "single clean finished engraving-plate line sketch: the right "
                "image redrawn in the left image's hand. Hatched shading "
                "allowed. No text. {extra}"),
}


def _key(explicit=None):
    if explicit:
        return explicit
    if os.environ.get("FAL_API_KEY") or os.environ.get("FAL_KEY"):
        return os.environ.get("FAL_API_KEY") or os.environ.get("FAL_KEY")
    for envf in ("/root/freaktown/.env", "/root/.fal-env"):
        try:
            with open(envf) as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("FAL_API_KEY=") or line.startswith("FAL_KEY="):
                        return line.split("=", 1)[1].strip().strip("\"'")
        except OSError:
            continue
    raise RuntimeError("no fal key (FAL_API_KEY env or /root/freaktown/.env)")


def _upload_datauri(path):
    import base64
    with open(path, "rb") as f:
        raw = base64.b64encode(f.read()).decode()
    ext = os.path.splitext(path)[1].lower()
    mime = {".png": "image/png", ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg", ".webp": "image/webp"}.get(ext, "image/png")
    return f"data:{mime};base64,{raw}"


def _side_by_side(left_path, right_path, dest_path, height=1024):
    from PIL import Image
    a = Image.open(left_path).convert("RGB")
    b = Image.open(right_path).convert("RGB")
    def fit(im):
        w, h = im.size
        s = height / h
        return im.resize((round(w * s), height), Image.LANCZOS)
    a, b = fit(a), fit(b)
    canvas = Image.new("RGB", (a.width + b.width, height), "white")
    canvas.paste(a, (0, 0))
    canvas.paste(b, (a.width, 0))
    canvas.save(dest_path)
    return dest_path


def finish(sketch_path, construction_path, out_path, prompt_extra="",
           style="thangka", key=None, guidance=3.0, steps=28, seed=None):
    """sketch = the hand to imitate; construction = the geometry to keep."""
    if style not in HOUSE_FINISH:
        raise ValueError(f"style? {sorted(HOUSE_FINISH)}")
    instruction = HOUSE_FINISH[style].format(extra=prompt_extra).strip()
    import tempfile
    comp = os.path.join(tempfile.gettempdir(),
                        f"finish_ref_{os.getpid()}.png")
    _side_by_side(sketch_path, construction_path, comp)
    body = json.dumps({
        "prompt": instruction,
        "image_url": _upload_datauri(comp),
        "guidance_scale": guidance,
        "num_inference_steps": steps,
        **({"seed": seed} if seed is not None else {}),
    }).encode()
    for attempt in range(3):
        try:
            req = urllib.request.Request(
                ENDPOINT, data=body,
                headers={"Authorization": f"Key {_key(key)}",
                         "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=300) as r:
                d = json.load(r)
            url = d["images"][0]["url"]
            with urllib.request.urlopen(url, timeout=300) as r2:
                img = r2.read()
            with open(out_path, "wb") as f:
                f.write(img)
            return out_path
        except Exception:
            if attempt == 2:
                raise
            time.sleep(4)
    raise RuntimeError("unreachable")
