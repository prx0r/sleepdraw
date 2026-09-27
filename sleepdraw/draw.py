"""Draw stage: 16:9 crop + techdou smooth-stroke render + preview frames."""
import glob
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TECHDOU = os.path.join(HERE, "vendor", "techdou")
KNOB_KEYS = ("WB_SKIP", "WB_SKETCH_W", "WB_COLOR_W", "WB_HOLD_S", "WB_BG",
             "WB_SKETCH_LIGHT", "WB_SPLIT", "WB_BRUSH", "WB_SMOOTH")


def crop_169(src, dest):
    from PIL import Image
    im = Image.open(src)
    w, h = im.size
    th = int(w * 9 / 16)
    top = (h - th) // 2
    im.crop((0, top, w, top + th)).save(dest, quality=88)
    return dest


def render(image, outdir, knobs, duration_ms=30000, no_hand=True):
    """knobs: dict of WB_* strings. Returns (mp4_path, frame_paths, log_tail)."""
    os.makedirs(outdir, exist_ok=True)
    env = dict(os.environ)
    for k in KNOB_KEYS:
        if k in knobs:
            env[k] = str(knobs[k])
    env["SHORTS_ORIENT"] = "landscape"
    cmd = [sys.executable, os.path.join(TECHDOU, "scripts", "batch_generate.py"),
           "--images", image, "--durations", str(duration_ms),
           "--output-dir", outdir]
    if no_hand:
        cmd.append("--no-hand")
    r = subprocess.run(cmd, cwd=HERE, env=env, capture_output=True,
                       text=True, timeout=1200)
    mp4s = sorted(glob.glob(os.path.join(outdir, "*.mp4")))
    if not mp4s:
        raise RuntimeError("no mp4:\n" + (r.stdout + r.stderr)[-1500:])
    mp4 = mp4s[0]
    dur_s = duration_ms / 1000
    frames = []
    for i, frac in enumerate((0.15, 0.4, 0.65, 0.9)):
        f = os.path.join(outdir, f"frame{i}.jpg")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss",
                        str(round(dur_s * frac, 1)), "-i", mp4,
                        "-frames:v", "1", f], check=True)
        frames.append(f)
    return mp4, frames, (r.stdout + r.stderr)[-2000:]
