"""progressive_journey.py — 12 checkpoint frames → one continuous drawing video.

Pure numpy/OpenCV. No techdou, no GPU, no model. Runs in seconds.

How it works:
  - Stages are pixel-registered (same canvas)
  - For each transition N→N+1:
    * Base = stage N (already drawn)
    * Diff = pixels in N+1 not in N (the new strokes)
    * Reveal diff progressively over T frames (component-by-component for drawing feel)
  - Result: one continuous video, no fades, no black, no canvas reset

Usage:
    python3 progressive_journey.py --out journey.mp4
"""
import argparse
import glob
import os
import shutil
import subprocess
import sys
import tempfile

import cv2
import numpy as np


def diff_mask(prev, next, thresh=25):
    p = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY) if len(prev.shape) == 3 else prev
    n = cv2.cvtColor(next, cv2.COLOR_BGR2GRAY) if len(next.shape) == 3 else next
    diff = cv2.absdiff(p, n)
    _, m = cv2.threshold(diff, thresh, 255, cv2.THRESH_BINARY)
    return cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))


def component_order(mask, seed=42):
    """Order connected components for drawing feel: large first, then small.
    Returns list of (component_label_mask, area)."""
    n, labels, stats, _ = cv2.connectedComponentsWithStats(mask, 8)
    comps = []
    for i in range(1, n):
        area = stats[i, cv2.CC_STAT_AREA]
        if area < 15:  # skip noise
            continue
        comps.append((labels == i, area))
    comps.sort(key=lambda c: -c[1])  # big shapes first
    return comps


def reveal_frame(base, target, comp_masks, progress, partial_mask):
    """Build one frame: base + progressively revealed new pixels.

    progress: 0..1 across the transition
    partial_mask: bool array tracking which diff pixels are revealed so far
    """
    frame = base.copy()
    # Determine how many components to reveal at this progress
    n_comp = len(comp_masks)
    n_show = int(progress * n_comp)
    new_partial = partial_mask.copy()
    for i in range(n_show):
        new_partial |= comp_masks[i][0]
    # Reveal: where partial is true AND target has ink, show target
    tgt_gray = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY) if len(target.shape) == 3 else target
    _, tgt_ink = cv2.threshold(tgt_gray, 200, 255, cv2.THRESH_BINARY_INV)
    reveal = new_partial & (tgt_ink > 0)
    frame[reveal] = target[reveal] if len(target.shape) == 3 else target[reveal]
    return frame, new_partial


def build(stages_dir, prefix, out_path, frames_per_transition=40, fps=15):
    stage_files = sorted(glob.glob(os.path.join(stages_dir, f'{prefix}-*.png')))
    n = len(stage_files)
    if n < 2:
        raise RuntimeError(f'need >=2 stages, got {n}')
    print(f'{n} stages → {n-1} transitions × {frames_per_transition} frames')

    stages = []
    for sf in stage_files:
        img = cv2.imread(sf, cv2.IMREAD_COLOR)
        if img is None:
            raise RuntimeError(f'cannot read {sf}')
        stages.append(img)

    work = tempfile.mkdtemp(prefix='pj_')
    out_dir = os.path.join(work, 'frames')
    os.makedirs(out_dir, exist_ok=True)
    idx = 0

    # Stage 1: show fully (hold for a moment)
    stages[0] = stages[0].astype(np.uint8)
    for _ in range(frames_per_transition):
        cv2.imwrite(os.path.join(out_dir, f'f_{idx:05d}.png'), stages[0])
        idx += 1
    print(f'  stage 1: {frames_per_transition} frames (held)', flush=True)

    # Transitions
    for i in range(1, n):
        base = stages[i - 1]
        target = stages[i]
        mask = diff_mask(base, target)
        comps = component_order(mask)
        partial = np.zeros(mask.shape, dtype=bool)
        T = frames_per_transition

        for t in range(T):
            progress = (t + 1) / T
            frame, partial = reveal_frame(base, target, comps, progress, partial)
            cv2.imwrite(os.path.join(out_dir, f'f_{idx:05d}.png'), frame)
            idx += 1

        print(f'  trans {i}: {len(comps)} components, {T} frames → {idx:05d}', flush=True)

    # Hold final frame
    for _ in range(frames_per_transition):
        cv2.imwrite(os.path.join(out_dir, f'f_{idx:05d}.png'), stages[-1])
        idx += 1

    # Concat with ffmpeg
    frame_list = os.path.join(work, 'frames.txt')
    with open(frame_list, 'w') as f:
        for k in range(idx):
            f.write(f"file '{os.path.join(out_dir, f'f_{k:05d}.png')}'\nduration {1.0/fps:.4f}\n")
        f.write(f"file '{os.path.join(out_dir, f'f_{idx-1:05d}.png')}'\n")

    r = subprocess.run(
        ['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', frame_list,
         '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-r', str(fps), out_path],
        capture_output=True, text=True, timeout=300)

    if os.path.exists(out_path):
        sz = os.path.getsize(out_path)
        dur = idx / fps
        print(f'DONE: {out_path} ({sz//1024}KB, {idx} frames, {dur:.1f}s)')
        shutil.rmtree(work, ignore_errors=True)
        return out_path
    else:
        raise RuntimeError(f'ffmpeg failed: {r.stderr[-500:]}')


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--stages-dir', default='/root/sleepdraw/storyboards')
    p.add_argument('--prefix', default='01-stage')
    p.add_argument('--out', required=True)
    p.add_argument('--frames', type=int, default=40, help='frames per transition')
    p.add_argument('--fps', type=int, default=15)
    a = p.parse_args()
    build(a.stages_dir, a.prefix, a.out, a.frames, a.fps)
