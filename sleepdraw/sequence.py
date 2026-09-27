"""Sequence chaining: sleep-coded transitions between finished clips.

Grammar (from film research, tuned for sleep):
- fade to black 2-4s (contemplative; 5s+ makes darkness itself a presence)
- black hold 2-3s (the breath between chapters — never skip it)
- next clip starts FROM black (our draws open on black canvas anyway,
  so emergence is the fade-in; no fade-in filter needed)
- vary the durations clip to clip; identical timing reads mechanical
- bed audio (when present) dips, never cuts — muxed later, not here

Usage:
  chain(["a.mp4", "b.mp4"], "out.mp4")                       # defaults
  chain([...], "out.mp4", fades=[3, 4, 2.5], hold=2.5)       # explicit
"""
import os
import subprocess
import tempfile

# Contemplative band per research; variation keeps it from reading mechanical.
FADES = [3.0, 4.0, 2.5, 3.5]
HOLD = 2.5


def _probe(path):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height,avg_frame_rate,duration",
         "-of", "default=noprint_wrappers=1", path],
        capture_output=True, text=True, check=True).stdout
    d = dict(l.split("=") for l in r.strip().splitlines() if "=" in l)
    num, den = d["avg_frame_rate"].split("/")
    return int(d["width"]), int(d["height"]), float(num) / float(den), float(d["duration"])


def chain(clips, out, fades=None, hold=HOLD):
    """Fade each clip to black, hold black, continue. Returns out path."""
    if len(clips) < 2:
        raise ValueError("need 2+ clips to chain")
    fades = list(fades or FADES)
    w, h, fps, _ = _probe(clips[0])
    tmp = tempfile.mkdtemp(prefix="seq_")
    parts = []
    for i, c in enumerate(clips):
        cw, ch, cfps, dur = _probe(c)
        if (cw, ch) != (w, h):
            raise ValueError(f"{c} is {cw}x{ch}, chain is {w}x{h} — normalize first")
        f = fades[i % len(fades)]
        seg = os.path.join(tmp, f"seg{i}.mp4")
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-i", c,
             "-vf", f"fade=out:st={dur - f:.2f}:d={f:.2f},format=yuv420p",
             "-r", str(int(fps)), "-c:v", "libx264", "-preset", "veryfast",
             "-crf", "20", seg], check=True)
        parts.append(seg)
        if i < len(clips) - 1:
            blk = os.path.join(tmp, f"black{i}.mp4")
            subprocess.run(
                ["ffmpeg", "-y", "-v", "error", "-f", "lavfi",
                 "-i", f"color=black:s={w}x{h}:r={int(fps)}:d={hold}",
                 "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                 blk], check=True)
            parts.append(blk)
    lst = os.path.join(tmp, "list.txt")
    with open(lst, "w") as fh:
        for p in parts:
            fh.write(f"file '{p}'\n")
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
         "-i", lst, "-movflags", "+faststart", "-c", "copy", out], check=True)
    meta = {"clips": clips, "fades": [fades[i % len(fades)] for i in range(len(clips))],
            "hold": hold, "grammar": "fade-through-black + breath"}
    with open(out + ".meta.json", "w") as fh:
        fh.write(__import__("json").dumps(meta, indent=1))
    return out
