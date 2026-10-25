"""journey.py — generate checkpoint images, etch each with lora2, chain them.

Two-phase per stage:
  1. GENERATE: bl image edit / Bailian → stage images (each feeds the next)
  2. ETCH: techdou lora2 renders each stage as a draw animation
  3. CHAIN: sequence.py links them with contemplative fades

Usage:
    from journey import run_journey
    run_journey(sketch_path, final_path, n_stages=5, style="cubist geometric")
"""
from __future__ import annotations
import json
import os
import subprocess
import sys
import tempfile
import time

ENGINE = "/root/sleepdraw/vendor/techdou/scripts/generate_whiteboard.py"
SEQUENCE = "/root/sleepdraw/sleepdraw/sequence.py"
LORA2_ENV = {
    "WB_SKIP": "8", "WB_SKETCH_W": "4", "WB_COLOR_W": "3",
    "WB_HOLD_S": "3", "WB_BG": "#000000", "WB_SKETCH_LIGHT": "1",
    "WB_SPLIT": "5", "WB_SMOOTH": "1", "WB_BRUSH": "10",
}


def generate_stage(prev_img_url: str, prompt: str, out_path: str,
                   worker_url: str = "https://quill.agi.xn--q9jyb4c") -> str:
    """Phase 1: call /journey to generate the next stage image."""
    import urllib.request
    body = json.dumps({"image_url": prev_img_url, "prompt": prompt}).encode()
    req = urllib.request.Request(
        f"{worker_url}/journey", data=body,
        headers={"Content-Type": "application/json",
                 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                               "AppleWebKit/537.36 (KHTML, like Gecko) "
                               "Chrome/120.0.0.0 Safari/537.36",
                 "Origin": worker_url, "Referer": f"{worker_url}/"})
    with urllib.request.urlopen(req, timeout=180) as r:
        d = json.load(r)
    img_url = d.get("image_url")
    if not img_url:
        raise RuntimeError(f"journey failed: {d}")
    # Download
    with urllib.request.urlopen(img_url, timeout=60) as r:
        data = r.read()
    with open(out_path, "wb") as f:
        f.write(data)
    return img_url


def etch_stage(image_path: str, out_dir: str, duration_ms: int = 10000) -> str:
    """Phase 2: render a stage as lora2 etch animation via techdou."""
    # Invert to white-on-black (techdou input)
    import cv2
    import numpy as np
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"cannot read {image_path}")
    inv = cv2.bitwise_not(img)
    tmp = os.path.join(out_dir, "_input.png")
    cv2.imwrite(tmp, inv)

    os.makedirs(out_dir, exist_ok=True)
    env = {**os.environ, **LORA2_ENV}
    cmd = [sys.executable, ENGINE, tmp, "--output-dir", out_dir,
           "--duration", str(duration_ms), "--no-hand"]
    r = subprocess.run(cmd, env=env, capture_output=True, text=True,
                       timeout=300, cwd="/root/sleepdraw")
    if r.returncode != 0:
        raise RuntimeError(f"techdou failed: {r.stderr[-500:]}")
    # Find output mp4
    mp4s = [f for f in os.listdir(out_dir) if f.endswith("_h264.mp4")]
    if not mp4s:
        mp4s = [f for f in os.listdir(out_dir) if f.endswith(".mp4")]
    if not mp4s:
        raise RuntimeError(f"no mp4 output in {out_dir}")
    return os.path.join(out_dir, mp4s[-1])


def chain_stages(stage_mp4s: list[str], out_path: str, fades=None, hold=None) -> str:
    """Phase 3: chain with sequence.py contemplative transitions."""
    sys.path.insert(0, "/root/sleepdraw")
    from sleepdraw.sequence import chain
    kwargs = {}
    if fades:
        kwargs["fades"] = fades
    if hold is not None:
        kwargs["hold"] = hold
    return chain(stage_mp4s, out_path, **kwargs)


def run_journey(sketch_url: str, final_url: str, n_stages: int = 5,
                style_hint: str = "", out_dir: str | None = None,
                duration_ms: int = 10000, worker_url: str = "") -> dict:
    """Full pipeline: generate N stages, etch each, chain into one video.

    Returns: {stages: [...], etched: [...], final_video: path}
    """
    if out_dir is None:
        stamp = time.strftime("%Y%m%d_%H%M%S")
        out_dir = f"/root/sleepdraw/runs/journey_{stamp}"
    os.makedirs(out_dir, exist_ok=True)

    stages = [sketch_url]  # stage 0 = original sketch
    stage_files = [os.path.join(out_dir, "stage_00_source.png")]

    # Phase 1: generate intermediate stages
    print(f"Phase 1: generating {n_stages} stages...")
    prev = sketch_url
    for i in range(1, n_stages):
        # Determine prompt based on stage position
        if i == 1:
            prompt = (f"Redraw this rough sketch as a clean construction drawing: "
                      f"correct proportions, guide circles, crosshairs, confident "
                      f"linework. Black ink on white paper. {style_hint}").strip()
        elif i < n_stages - 1:
            prompt = (f"Continue developing this drawing: add detail, refine "
                      f"contours, build toward the finished painting. "
                      f"Keep existing geometry. {style_hint}").strip()
        else:
            prompt = (f"Complete this drawing to match the finished painting. "
                      f"All detail, ornament, colour. {style_hint}").strip()

        path = os.path.join(out_dir, f"stage_{i:02d}.png")
        print(f"  stage {i}/{n_stages-1}: {prompt[:60]}...")
        img_url = generate_stage(prev, prompt, path, worker_url)
        stages.append(img_url)
        stage_files.append(path)
        prev = img_url  # chain: next stage uses this as input

    # Final stage = exact reference (axiom 1)
    final_path = os.path.join(out_dir, f"stage_{n_stages-1:02d}_final.png")
    import urllib.request
    with urllib.request.urlopen(final_url, timeout=60) as r:
        open(final_path, "wb").write(r.read())
    stage_files[-1] = final_path

    # Phase 2: etch each stage
    print(f"Phase 2: etching {len(stage_files)} stages...")
    etched = []
    for i, sf in enumerate(stage_files):
        edir = os.path.join(out_dir, f"etch_{i:02d}")
        print(f"  etch {i}...")
        mp4 = etch_stage(sf, edir, duration_ms)
        etched.append(mp4)

    # Phase 3: chain
    print("Phase 3: chaining...")
    final_video = os.path.join(out_dir, "journey_complete.mp4")
    chain_stages(etched, final_video)

    result = {
        "stages": stage_files,
        "etched": etched,
        "final_video": final_video,
        "out_dir": out_dir,
    }
    # Save manifest
    json.dump(result, open(os.path.join(out_dir, "manifest.json"), "w"), indent=1)
    print(f"Done: {final_video}")
    return result


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="Sketch → journey pipeline")
    p.add_argument("--sketch", required=True, help="sketch image URL or path")
    p.add_argument("--final", required=True, help="final painting URL or path")
    p.add_argument("--stages", type=int, default=5)
    p.add_argument("--style", default="")
    p.add_argument("--duration", type=int, default=10000)
    p.add_argument("--out", default=None)
    p.add_argument("--worker", default="https://quill.agi.xn--q9jyb4c")
    a = p.parse_args()

    # If local paths, presign them for the API
    if not a.sketch.startswith("http"):
        import boto3
        env = {}
        for line in open("/root/.r2-env"):
            line = line.strip()
            if line and "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip().strip("'\"")
        s3 = boto3.client("s3",
            endpoint_url=env.get("R2_ENDPOINT"),
            aws_access_key_id=env.get("R2_ACCESS_KEY"),
            aws_secret_access_key=env.get("R2_SECRET_KEY"))
        # Upload local files to R2
        for key, path in [("journey/tmp-sketch.png", a.sketch),
                          ("journey/tmp-final.png", a.final)]:
            s3.put_object(Bucket="stallshark", Key=key,
                          Body=open(path, "rb").read(), ContentType="image/png")
        a.sketch = s3.generate_presigned_url("get_object",
            Params={"Bucket": "stallshark", "Key": "journey/tmp-sketch.png"},
            ExpiresIn=604800)
        a.final = s3.generate_presigned_url("get_object",
            Params={"Bucket": "stallshark", "Key": "journey/tmp-final.png"},
            ExpiresIn=604800)

    result = run_journey(a.sketch, a.final, n_stages=a.stages,
                         style_hint=a.style, out_dir=a.out,
                         duration_ms=a.duration, worker_url=a.worker)
    print(json.dumps(result, indent=1))
