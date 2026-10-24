"""Real images -> white-on-black etched line art (draw-ready).

Museum scans, manuscript folios, architecture photos in; pencil-etch out.
Knobs: detail (edge threshold), softness (bilateral passes), levels.
Output feeds draw.py unchanged — same renderer, real sources.
"""
import cv2
import numpy as np


def etch(src_path, dest_path, detail=0.55, softness=2, invert_bg=True,
         max_side=1080):
    """detail 0..1: fraction of edges kept (lower = sparser, more drawable).
    Returns dest path."""
    img = cv2.imread(src_path)
    if img is None:
        raise ValueError(f"cannot read {src_path}")
    h, w = img.shape[:2]
    s = max_side / max(h, w)
    if s < 1:
        img = cv2.resize(img, (int(w * s), int(h * s)))
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    for _ in range(max(0, int(softness))):
        g = cv2.bilateralFilter(g, 7, 60, 60)
    # edges both directions, merged — catches pencil and paint alike
    e1 = cv2.Canny(g, 30, 110)
    lap = cv2.Laplacian(g, cv2.CV_8U, ksize=3)
    _, lap = cv2.threshold(lap, 18, 255, cv2.THRESH_BINARY)
    edges = cv2.bitwise_or(e1, lap)
    # thin to near-skeleton so the walk has clean paths
    kernel = np.ones((2, 2), np.uint8)
    edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
    if detail < 1.0:
        keep = np.random.default_rng(7).random(edges.shape) < detail
        edges = np.where(keep, edges, 0).astype(np.uint8)
    if invert_bg:
        pass  # Canny edges are already white-on-black: our canvas
    else:
        edges = cv2.bitwise_not(edges)  # black ink on paper white
        return cv2.imwrite(dest_path, cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR))
    cv2.imwrite(dest_path, cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR))
    return dest_path


if __name__ == "__main__":
    import sys
    etch(sys.argv[1], sys.argv[2], *(float(x) for x in sys.argv[3:]))
