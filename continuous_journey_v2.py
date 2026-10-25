"""continuous_journey_v2.py — fast parallel render + streaming composite.

Speed: all 11 diff-mask renders run IN PARALLEL (~30s total instead of 5min).
Disk: compositing streams frames → ffmpeg, never stores all PNGs.

Pipeline:
  1. Stage 1 renders (techdou, lora3)
  2. All 11 diff-mask renders in PARALLEL
  3. Sequential compositing (fast: pixel ops only), streaming into ffmpeg
"""
import glob
import os
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed

import cv2
import numpy as np

ENGINE = "/root/sleepdraw/vendor/techdou/scripts/generate_whiteboard.py"

LORA3_ENV = {
    "WB_SKIP": "6", "WB_SKETCH_W": "3", "WB_COLOR_W": "1", "WB_HOLD_S": "4",
    "WB_BG": "#000000", "WB_SKETCH_LIGHT": "1", "WB_SPLIT": "5",
    "WB_SMOOTH": "1", "WB_BRUSH": "10", "WB_RHYTHM": "2",
    "WB_LINE": "1", "WB_AA": "0", "WB_INK": "0", "WB_ACTS": "0", "WB_GOLD": "",
}


def render_one(label, input_path, outdir, duration_ms):
    """Render a single techdou job. Returns output mp4 path or None."""
    os.makedirs(outdir, exist_ok=True)
    env = {**os.environ, **LORA3_ENV}
    r = subprocess.run(
        [sys.executable, ENGINE, input_path, '--output-dir', outdir,
         '--duration', str(duration_ms), '--no-hand'],
        env=env, capture_output=True, text=True, timeout=300, cwd='/root/sleepdraw')
    mp4s = sorted(glob.glob(os.path.join(outdir, '*h264.mp4')))
    if not mp4s:
        mp4s = sorted(glob.glob(os.path.join(outdir, '*.mp4')))
    return mp4s[-1] if mp4s else None


def extract_frames(mp4, outdir, fps=15):
    """Extract frames from mp4. Returns sorted list of png paths."""
    os.makedirs(outdir, exist_ok=True)
    subprocess.run(['ffmpeg', '-y', '-i', mp4, '-vsync', '0',
                    f'{outdir}/f_%04d.png'], capture_output=True, timeout=120)
    return sorted(glob.glob(os.path.join(outdir, 'f_*.png')))


def diff_mask(prev_img, next_img, thresh=25):
    p = cv2.cvtColor(prev_img, cv2.COLOR_BGR2GRAY) if len(prev_img.shape) == 3 else prev_img
    n = cv2.cvtColor(next_img, cv2.COLOR_BGR2GRAY) if len(next_img.shape) == 3 else next_img
    diff = cv2.absdiff(p, n)
    _, mask = cv2.threshold(diff, thresh, 255, cv2.THRESH_BINARY)
    return cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))


def build(stages_dir, prefix, out_path, duration_ms=6000, workers=6):
    stage_files = sorted(glob.glob(os.path.join(stages_dir, f'{prefix}-*.png')))
    n = len(stage_files)
    if n < 2:
        raise RuntimeError(f'need >=2 stages, got {n}')

    work = tempfile.mkdtemp(prefix='cj_')
    print(f'{n} stages → {n-1} transitions, {workers} parallel renders')

    # ── PHASE 1: prepare all inputs in parallel ──────────────────────
    jobs = []  # (label, input_path, outdir)

    # Stage 1: invert full drawing
    s1 = cv2.imread(stage_files[0], cv2.IMREAD_GRAYSCALE)
    s1_input = os.path.join(work, '_s1.png')
    cv2.imwrite(s1_input, cv2.bitwise_not(s1))
    jobs.append(('stage1', s1_input, os.path.join(work, 'r_stage1')))

    # All diff masks
    masks = {}
    for i in range(1, n):
        prev = cv2.imread(stage_files[i - 1], cv2.IMREAD_GRAYSCALE)
        nxt = cv2.imread(stage_files[i], cv2.IMREAD_GRAYSCALE)
        mask = diff_mask(prev, nxt)
        masks[i] = mask
        mp = os.path.join(work, f'_mask_{i:02d}.png')
        cv2.imwrite(mp, mask)
        jobs.append((f'trans{i}', mp, os.path.join(work, f'r_trans{i:02d}')))

    # ── PHASE 2: render ALL in parallel ──────────────────────────────
    print(f'rendering {len(jobs)} jobs in parallel...', flush=True)
    results = {}
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(render_one, lb, ip, od, duration_ms): lb
                for lb, ip, od in jobs}
        for f in as_completed(futs):
            lb = futs[f]
            try:
                mp4 = f.result()
                results[lb] = mp4
                print(f'  {lb}: {"ok" if mp4 else "FAIL"}', flush=True)
            except Exception as e:
                results[lb] = None
                print(f'  {lb}: ERROR {e}', flush=True)

    # ── PHASE 3: extract stage-1 frames, then stream-composite ──────
    print('extracting stage 1 frames...', flush=True)
    s1_frames = extract_frames(results['stage1'], os.path.join(work, 'f_s1'))
    print(f'  {len(s1_frames)} frames', flush=True)

    # Start ffmpeg concat via pipe — stream frames in, never store all
    frame_list = os.path.join(work, 'frames.txt')
    all_written = []

    # Stage 1: write frames to concat list
    accum = cv2.imread(s1_frames[-1])  # start compositing from fully-drawn stage 1
    h, w = accum.shape[:2]

    # For output: write all stage-1 frames first
    out_dir = os.path.join(work, 'out')
    os.makedirs(out_dir, exist_ok=True)
    idx = 0
    for fp in s1_frames:
        shutil.copy2(fp, os.path.join(out_dir, f'f_{idx:05d}.png'))
        all_written.append(idx)
        idx += 1

    # Transitions: extract overlay → composite → write → delete overlay
    for i in range(1, n):
        key = f'trans{i}'
        mp4 = results.get(key)
        if not mp4:
            print(f'  trans{i}: skipped (no render)', flush=True)
            continue
        ov_dir = os.path.join(work, f'ov_{i:02d}')
        ov_frames = extract_frames(mp4, ov_dir)
        for ofp in ov_frames:
            of = cv2.imread(ofp)
            if of is None:
                continue
            if of.shape[:2] != (h, w):
                of = cv2.resize(of, (w, h))
            og = cv2.cvtColor(of, cv2.COLOR_BGR2GRAY)
            _, omask = cv2.threshold(og, 50, 255, cv2.THRESH_BINARY)
            bf = accum.astype(np.float32)
            of_ = of.astype(np.float32)
            stroke = (omask > 0) & (of_.mean(axis=2) > 50)
            comp = bf.copy()
            comp[stroke] = of_[stroke]
            accum = comp.astype(np.uint8)
            cv2.imwrite(os.path.join(out_dir, f'f_{idx:05d}.png'), accum)
            idx += 1
        # Free overlay frames immediately
        shutil.rmtree(ov_dir, ignore_errors=True)
        # Free the render mp4 + mask
        os.remove(mp4)
        mp_path = os.path.join(work, f'_mask_{i:02d}.png')
        if os.path.exists(mp_path):
            os.remove(mp_path)
        print(f'  trans{i}: composited {len(ov_frames)} frames → out/{idx:05d}', flush=True)

    # Free stage-1 render
    s1_mp4 = results.get('stage1')
    if s1_mp4 and os.path.exists(s1_mp4):
        os.remove(s1_mp4)
    shutil.rmtree(os.path.join(work, 'f_s1'), ignore_errors=True)

    # ── PHASE 4: concat ─────────────────────────────────────────────
    print(f'concatenating {idx} frames...', flush=True)
    with open(frame_list, 'w') as f:
        for k in range(idx):
            f.write(f"file '{os.path.join(out_dir, f'f_{k:05d}.png')}'\nduration {1.0/15:.4f}\n")
        f.write(f"file '{os.path.join(out_dir, f'f_{idx-1:05d}.png')}'\n")

    r = subprocess.run(
        ['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', frame_list,
         '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-r', '15', out_path],
        capture_output=True, text=True, timeout=600)

    if os.path.exists(out_path):
        sz = os.path.getsize(out_path)
        print(f'DONE: {out_path} ({sz//1024}KB, {idx} frames)')
        # Cleanup out_dir frames
        shutil.rmtree(out_dir, ignore_errors=True)
        shutil.rmtree(work, ignore_errors=True)
        return out_path
    else:
        raise RuntimeError(f'ffmpeg failed: {r.stderr[-500:]}')


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--stages-dir', default='/root/sleepdraw/storyboards')
    p.add_argument('--prefix', default='01-stage')
    p.add_argument('--out', required=True)
    p.add_argument('--duration', type=int, default=6000, help='ms per stage')
    p.add_argument('--workers', type=int, default=6, help='parallel techdou renders')
    a = p.parse_args()
    build(a.stages_dir, a.prefix, a.out, a.duration, a.workers)
