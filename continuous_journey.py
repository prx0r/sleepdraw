"""continuous_journey.py — one continuous drawing from sketch to final.

Unlike sequence.py (which chains clips with fades), this builds a SINGLE
video where each stage's new strokes draw onto the SAME persistent canvas.

Pipeline:
  1. Stage 1 renders fully (techdou, lora3 thin etch knobs)
  2. For each transition N→N+1:
     a. Compute new-stroke mask (pixels in N+1 not in N)
     b. Render mask via techdou (draws just the new strokes)
     c. Composite onto accumulated canvas frames
  3. Concatenate ALL frames into one video — no fades, no black holds

Usage:
    python3 continuous_journey.py --stages-dir storyboards --prefix 01-stage --out journey.mp4
"""
import argparse
import glob
import os
import subprocess
import sys
import tempfile

import cv2
import numpy as np

ENGINE = "/root/sleepdraw/vendor/techdou/scripts/generate_whiteboard.py"

# lora3 thin etch — the beautiful slow thin stroke
LORA3_ENV = {
    "WB_SKIP": "6",         # slower: fewer cells per frame
    "WB_SKETCH_W": "3",
    "WB_COLOR_W": "1",      # no fill phase — pure line drawing
    "WB_HOLD_S": "4",       # longer hold at completion
    "WB_BG": "#000000",
    "WB_SKETCH_LIGHT": "1",
    "WB_SPLIT": "5",
    "WB_SMOOTH": "1",
    "WB_BRUSH": "10",
    "WB_RHYTHM": "2",       # deep: curve slowdown + lift pauses
    "WB_LINE": "1",         # 1px fixed nib fineliner
    "WB_AA": "0",
    "WB_INK": "0",
    "WB_ACTS": "0",
    "WB_GOLD": "",
}


def compute_diff_mask(prev_img, next_img, thresh=30):
    """Pixels in next_img that are new/different from prev_img."""
    p = cv2.cvtColor(prev_img, cv2.COLOR_BGR2GRAY) if len(prev_img.shape) == 3 else prev_img
    n = cv2.cvtColor(next_img, cv2.COLOR_BGR2GRAY) if len(next_img.shape) == 3 else next_img
    diff = cv2.absdiff(p, n)
    _, mask = cv2.threshold(diff, thresh, 255, cv2.THRESH_BINARY)
    # Clean up noise
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    return mask


def render_transition(stage_prev, stage_next, mask, outdir, duration_ms=15000):
    """Render the new-stroke mask as a techdou draw animation."""
    os.makedirs(outdir, exist_ok=True)
    # Invert mask for techdou (white strokes on black)
    # Mask has white=changed, black=unchanged → already correct for techdou
    mask_bgr = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    tmp = os.path.join(outdir, '_mask.png')
    cv2.imwrite(tmp, mask_bgr)

    env = {**os.environ, **LORA3_ENV}
    cmd = [sys.executable, ENGINE, tmp, '--output-dir', outdir,
           '--duration', str(duration_ms), '--no-hand']
    r = subprocess.run(cmd, env=env, capture_output=True, text=True,
                       timeout=600, cwd='/root/sleepdraw')
    mp4s = sorted(glob.glob(os.path.join(outdir, '*.mp4')))
    if not mp4s:
        raise RuntimeError(f"techdou failed: {r.stderr[-300:]}")
    return mp4s[-1]


def composite_frames(base_frames_dir, overlay_mp4, out_frames_dir, fade_in_ms=0):
    """Overlay a techdou draw animation onto the accumulated base frames.

    Reads frames from overlay_mp4 and composites them onto base_frames.
    The overlay's white strokes are added (lighter) onto the base.
    """
    os.makedirs(out_frames_dir, exist_ok=True)
    # Extract overlay frames
    ov_dir = out_frames_dir + '_ov'
    os.makedirs(ov_dir, exist_ok=True)
    subprocess.run(['ffmpeg', '-y', '-i', overlay_mp4,
                    '-vsync', '0', f'{ov_dir}/f_%04d.png'],
                   capture_output=True, timeout=120)
    ov_frames = sorted(glob.glob(os.path.join(ov_dir, 'f_*.png')))
    base_frames = sorted(glob.glob(os.path.join(base_frames_dir, 'f_*.png')))
    if not base_frames:
        raise RuntimeError(f"no base frames in {base_frames_dir}")

    # Get base dimensions
    b0 = cv2.imread(base_frames[0])
    h, w = b0.shape[:2]

    # For each overlay frame, composite onto the LAST base frame
    # (the base grows as strokes are added)
    last_base = b0.copy()
    out_count = 0
    for of_path in ov_frames:
        of = cv2.imread(of_path)
        if of is None:
            continue
        # Resize overlay to match if needed
        if of.shape[:2] != (h, w):
            of = cv2.resize(of, (w, h))
        # Add white strokes (lighter = stroke appears)
        # Convert both to float, take max (white strokes overlay)
        b_f = last_base.astype(np.float32)
        o_f = of.astype(np.float32)
        # Only take bright pixels from overlay (strokes)
        _, o_mask = cv2.threshold(cv2.cvtColor(of, cv2.COLOR_BGR2GRAY), 60, 255, cv2.THRESH_BINARY)
        # Where overlay has strokes, overlay wins
        stroke_region = (o_mask > 0) & (o_f.mean(axis=2) > 40)
        composite = b_f.copy()
        composite[stroke_region] = o_f[stroke_region]
        last_base = composite.astype(np.uint8)
        cv2.imwrite(os.path.join(out_frames_dir, f'f_{out_count:04d}.png'), last_base)
        out_count += 1

    # Also output the accumulated base as final frames
    return out_count


def build_continuous(stages_dir, prefix, out_path, transition_ms=15000):
    """Build one continuous video from N stages."""
    stage_files = sorted(glob.glob(os.path.join(stages_dir, f'{prefix}-*.png')))
    if len(stage_files) < 2:
        raise RuntimeError(f"need ≥2 stages, found {len(stage_files)}")

    print(f"Building continuous journey from {len(stage_files)} stages...")

    work = tempfile.mkdtemp(prefix='cj_')
    all_frames = []  # accumulated frame dirs in order

    # Stage 1: render fully
    print("  stage 1: full render...", flush=True)
    s1_dir = os.path.join(work, 'stage_01')
    s1_frames = os.path.join(work, 'frames_01')
    os.makedirs(s1_frames, exist_ok=True)
    # Invert for techdou
    s1 = cv2.imread(stage_files[0], cv2.IMREAD_GRAYSCALE)
    s1_inv = cv2.bitwise_not(s1)
    s1_path = os.path.join(work, '_s1.png')
    cv2.imwrite(s1_path, s1_inv)
    env = {**os.environ, **LORA3_ENV}
    subprocess.run([sys.executable, ENGINE, s1_path, '--output-dir', s1_dir,
                    '--duration', str(transition_ms), '--no-hand'],
                   env=env, capture_output=True, text=True, timeout=600, cwd='/root/sleepdraw')
    # Extract frames from s1 render
    s1_mp4 = sorted(glob.glob(os.path.join(s1_dir, '*.mp4')))[-1]
    subprocess.run(['ffmpeg', '-y', '-i', s1_mp4, '-vsync', '0',
                    f'{s1_frames}/f_%04d.png'], capture_output=True, timeout=120)
    all_frames.append(s1_frames)
    print(f"  stage 1: {len(glob.glob(os.path.join(s1_frames, '*.png')))} frames", flush=True)

    # Transitions: draw new strokes ON TOP of the accumulated canvas.
    # The base grows with each transition — never resets to black.
    # Start with the LAST frame of stage 1 (fully drawn).
    s1_pngs = sorted(glob.glob(os.path.join(s1_frames, 'f_*.png')))
    accum_base = cv2.imread(s1_pngs[-1])
    h, w = accum_base.shape[:2]

    for i in range(1, len(stage_files)):
        print(f"  transition {i}→{i+1}...", flush=True)
        prev = cv2.imread(stage_files[i-1], cv2.IMREAD_GRAYSCALE)
        nxt = cv2.imread(stage_files[i], cv2.IMREAD_GRAYSCALE)
        if prev is None or nxt is None:
            continue
        mask = compute_diff_mask(prev, nxt, thresh=25)
        t_dir = os.path.join(work, f'transition_{i:02d}')
        t_mp4 = render_transition(prev, nxt, mask, t_dir, transition_ms)

        # Extract overlay frames and composite each onto accum_base
        ov_frames = os.path.join(work, f'ov_{i:02d}')
        os.makedirs(ov_frames, exist_ok=True)
        subprocess.run(['ffmpeg', '-y', '-i', t_mp4, '-vsync', '0',
                        f'{ov_frames}/f_%04d.png'], capture_output=True, timeout=120)
        ov_pngs = sorted(glob.glob(os.path.join(ov_frames, 'f_*.png')))

        comp_frames = os.path.join(work, f'comp_{i:02d}')
        os.makedirs(comp_frames, exist_ok=True)
        for j, of_path in enumerate(ov_pngs):
            of = cv2.imread(of_path)
            if of is None:
                continue
            if of.shape[:2] != (h, w):
                of = cv2.resize(of, (w, h))
            # White strokes from overlay replace base pixels where strokes exist
            o_gray = cv2.cvtColor(of, cv2.COLOR_BGR2GRAY)
            _, o_mask = cv2.threshold(o_gray, 50, 255, cv2.THRESH_BINARY)
            b_f = accum_base.astype(np.float32)
            o_f = of.astype(np.float32)
            stroke = (o_mask > 0) & (o_f.mean(axis=2) > 50)
            comp = b_f.copy()
            comp[stroke] = o_f[stroke]
            accum_base = comp.astype(np.uint8)
            cv2.imwrite(os.path.join(comp_frames, f'f_{j:04d}.png'), accum_base)

        all_frames.append(comp_frames)
        # Free disk: delete overlay frames + techdou mp4 immediately after compositing
        import shutil
        shutil.rmtree(ov_frames, ignore_errors=True)
        for _mp4 in glob.glob(os.path.join(t_dir, '*.mp4')):
            os.remove(_mp4)
        n = len(ov_pngs)
        print(f"  transition {i}: {n} composited frames (mask: {(mask>0).sum()}px)", flush=True)

    # Concatenate ALL frames in order
    print("Concatenating...", flush=True)
    # Create concat file
    frame_list = os.path.join(work, 'frames.txt')
    all_pngs = []
    for fdir in all_frames:
        all_pngs.extend(sorted(glob.glob(os.path.join(fdir, 'f_*.png'))))
    with open(frame_list, 'w') as f:
        for p in all_pngs:
            f.write(f"file '{p}'\nduration 0.066\n")  # ~15fps
        # Repeat last frame for hold
        f.write(f"file '{all_pngs[-1]}'\n")

    subprocess.run(['ffmpeg', '-y', '-f', 'concat', '-safe', '0',
                    '-i', frame_list, '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
                    '-r', '15', out_path], capture_output=True, timeout=600)

    if os.path.exists(out_path):
        sz = os.path.getsize(out_path)
        print(f"Done: {out_path} ({sz//1024}KB)")
        return out_path
    else:
        raise RuntimeError("ffmpeg concat failed")


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--stages-dir', default='/root/sleepdraw/storyboards')
    p.add_argument('--prefix', default='01-stage')
    p.add_argument('--out', required=True)
    p.add_argument('--duration', type=int, default=15000, help='ms per stage/transition')
    a = p.parse_args()
    build_continuous(a.stages_dir, a.prefix, a.out, a.duration)
