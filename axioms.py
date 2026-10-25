"""axioms.py — the 14 journey axioms as programmable validation gates.

Each axiom is a function: (prev_img, next_img, endpoint_info) → (pass, detail).
Some axioms are prompt-encoded (fed to the model before generation).
Some are post-hoc validators (checked on generated images).
Some are architectural (enforced by pipeline structure, not image analysis).

Usage:
    from axioms import validate_stage
    result = validate_stage(prev_frame, next_frame, stage_num, total, endpoints)
    if not result['pass']:
        reject_or_regen(result['violations'])
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
import hashlib
import numpy as np


@dataclass
class StageResult:
    stage: int
    passed: bool
    violations: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    scores: dict = field(default_factory=dict)


def _load_gray(path_or_arr) -> np.ndarray:
    if isinstance(path_or_arr, np.ndarray):
        return path_or_arr
    import cv2
    img = cv2.imread(str(path_or_arr), cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"cannot read: {path_or_arr}")
    return img


def _to_color(path_or_arr) -> np.ndarray:
    if isinstance(path_or_arr, np.ndarray):
        return path_or_arr
    import cv2
    img = cv2.imread(str(path_or_arr), cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError(f"cannot read: {path_or_arr}")
    return img


def _resize_match(a: np.ndarray, b: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    h = min(a.shape[0], b.shape[0])
    w = min(a.shape[1], b.shape[1])
    import cv2
    return cv2.resize(a, (w, h)), cv2.resize(b, (w, h))


# ─── Axiom 1: Exact endpoints ────────────────────────────────────────────────
def axiom1_exact_endpoints(stage: int, total: int, endpoint_sketch_hash: str,
                           endpoint_final_hash: str, frame_hash: str) -> tuple[bool, str]:
    """Stage 1 must match sketch, last stage must match final. Exact."""
    if stage == 0:
        if frame_hash != endpoint_sketch_hash:
            return False, "stage 1 does not match original sketch (exact endpoint violated)"
        return True, "exact sketch endpoint"
    if stage == total - 1:
        if frame_hash != endpoint_final_hash:
            return False, f"final stage does not match final painting (exact endpoint violated)"
        return True, "exact final endpoint"
    return True, "interior stage (endpoints not applicable)"


# ─── Axiom 2: Stroke continuity ─────────────────────────────────────────────
def axiom2_stroke_continuity(prev_img, next_img) -> tuple[bool, str, float]:
    """No lines teleport. Check: edge maps should overlap significantly."""
    import cv2
    p = _load_gray(prev_img)
    n = _load_gray(next_img)
    p, n = _resize_match(p, n)
    edges_p = cv2.Canny(p, 50, 150)
    edges_n = cv2.Canny(n, 50, 150)
    # Dilate to allow small shifts
    kernel = np.ones((5, 5), np.uint8)
    edges_p_d = cv2.dilate(edges_p, kernel)
    edges_n_d = cv2.dilate(edges_n, kernel)
    # How much of next frame's edges are "explained" by prev frame
    total_edges = (edges_n > 0).sum()
    if total_edges == 0:
        return True, "no edges in next frame", 1.0
    explained = ((edges_n > 0) & (edges_p_d > 0)).sum() / total_edges
    # New strokes are OK (artist drawing), but mass disappearance is bad
    prev_edges = (edges_p > 0).sum()
    disappeared = ((edges_p > 0) & (edges_n_d == 0)).sum()
    vanish_ratio = disappeared / max(prev_edges, 1)
    if vanish_ratio > 0.4:
        return False, f"strokes vanished without redraw ({vanish_ratio:.0%})", explained
    if explained < 0.15:
        return False, f"strokes teleported (only {explained:.0%} continuity)", explained
    return True, f"continuity {explained:.0%}", explained


# ─── Axiom 3: Small transitions ─────────────────────────────────────────────
def axiom3_small_transition(prev_img, next_img) -> tuple[bool, str, float]:
    """Not dramatically more complete. Measure edge density change."""
    import cv2
    p = _load_gray(prev_img)
    n = _load_gray(next_img)
    p, n = _resize_match(p, n)
    density_p = (cv2.Canny(p, 50, 150) > 0).sum() / p.size
    density_n = (cv2.Canny(n, 50, 150) > 0).sum() / n.size
    if density_p < 1e-6:
        return True, "prev too sparse to measure", 0.0
    ratio = density_n / density_p
    if ratio > 5.0:
        return False, f"dramatic completeness jump ({ratio:.1f}x edges)", ratio
    return True, f"density ratio {ratio:.2f}x", ratio


# ─── Axiom 4: Conserved geometry ────────────────────────────────────────────
def axiom4_conserved_geometry(prev_img, next_img) -> tuple[bool, str, float]:
    """Major shapes don't teleport. Check: structural similarity of layout."""
    from skimage.metrics import structural_similarity as ssim
    p = _load_gray(prev_img)
    n = _load_gray(next_img)
    p, n = _resize_match(p, n)
    # Downsample to focus on structure not detail
    import cv2
    p_s = cv2.resize(p, (64, 64))
    n_s = cv2.resize(n, (64, 64))
    score = ssim(p_s, n_s)
    if score < 0.1:
        return False, f"geometry completely shifted (ssim={score:.3f})", score
    return True, f"geometry stable (ssim={score:.3f})", score


# ─── Axiom 6: Material continuity ───────────────────────────────────────────
def axiom6_material_continuity(prev_img, next_img) -> tuple[bool, str, float]:
    """No medium change (sketch stays sketch-like). Check colour saturation shift."""
    p = _to_color(prev_img)
    n = _to_color(next_img)
    p, n = _resize_match(p, n)
    import cv2
    hsv_p = cv2.cvtColor(p, cv2.COLOR_BGR2HSV)
    hsv_n = cv2.cvtColor(n, cv2.COLOR_BGR2HSV)
    sat_p = hsv_p[:, :, 1].mean()
    sat_n = hsv_n[:, :, 1].mean()
    # Sudden jump from monochrome to full colour (or vice versa)
    if sat_p < 30 and sat_n > 120:
        return False, f"suddenly colourized ({sat_p:.0f} → {sat_n:.0f} saturation)", abs(sat_n - sat_p)
    if sat_p > 120 and sat_n < 30:
        return False, f"suddenly desaturated ({sat_p:.0f} → {sat_n:.0f})", abs(sat_n - sat_p)
    return True, f"saturation {sat_p:.0f} → {sat_n:.0f}", abs(sat_n - sat_p)


# ─── Axiom 9: Progressive colour ───────────────────────────────────────────
def axiom9_progressive_colour(prev_img, next_img) -> tuple[bool, str, float]:
    """Colour grows monotonically (or stays), never regresses then floods."""
    p = _to_color(prev_img)
    n = _to_color(next_img)
    p, n = _resize_match(p, n)
    import cv2
    sat_p = cv2.cvtColor(p, cv2.COLOR_BGR2HSV)[:, :, 1].mean()
    sat_n = cv2.cvtColor(n, cv2.COLOR_BGR2HSV)[:, :, 1].mean()
    if sat_n > sat_p + 80:
        return False, f"colour flooded (+{sat_n - sat_p:.0f} saturation jump)", sat_n - sat_p
    return True, f"colour delta {sat_n - sat_p:+.0f}", sat_n - sat_p


# ─── Axiom 10: Locality ─────────────────────────────────────────────────────
def axiom10_locality(prev_img, next_img, max_regions: int = 3) -> tuple[bool, str, int]:
    """Changes concentrated in limited regions, not everywhere at once."""
    import cv2
    p = _load_gray(prev_img)
    n = _load_gray(next_img)
    p, n = _resize_match(p, n)
    diff = cv2.absdiff(p, n)
    _, changed = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
    # Count connected regions of change
    contours, _ = cv2.findContours(changed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Filter tiny noise
    big = [c for c in contours if cv2.contourArea(c) > 200]
    if len(big) > max_regions:
        return False, f"{len(big)} distant regions changed simultaneously", len(big)
    return True, f"{len(big)} regions changed", len(big)


# ─── Axiom 11: No hidden work ───────────────────────────────────────────────
def axiom11_no_hidden_work(prev_img, next_img) -> tuple[bool, str]:
    """New content must appear in regions that existed before (no teleporting
    complete elements into previously empty space without intermediate)."""
    import cv2
    p = _load_gray(prev_img)
    n = _load_gray(next_img)
    p, n = _resize_match(p, n)
    # Find regions with new ink that were empty before
    _, p_bin = cv2.threshold(p, 200, 255, cv2.THRESH_BINARY_INV)
    _, n_bin = cv2.threshold(n, 200, 255, cv2.THRESH_BINARY_INV)
    new_ink = ((n_bin > 0) & (p_bin == 0))
    old_empty_context = cv2.erode(p_bin, np.ones((15, 15), np.uint8))
    hidden = ((new_ink > 0) & (old_empty_context == 0)).sum()
    total_new = new_ink.sum()
    if total_new > 0 and hidden / total_new > 0.6:
        return False, f"{hidden/total_new:.0%} of new content in previously empty space"
    return True, "new content follows existing structure"


# ─── Axiom 13: Final convergence ────────────────────────────────────────────
def axiom13_final_convergence(prev_img, final_img) -> tuple[bool, str, float]:
    """Penultimate stage close enough to final for the transition to be drawable."""
    from skimage.metrics import structural_similarity as ssim
    p = _load_gray(prev_img)
    f = _load_gray(final_img)
    p, f = _resize_match(p, f)
    p_s = cv2.resize(p, (64, 64))
    f_s = cv2.resize(f, (64, 64))
    score = ssim(p_s, f_s)
    if score < 0.2:
        return False, f"penultimate too far from final (ssim={score:.3f}) — transition not drawable", score
    return True, f"convergence ssim={score:.3f}", score


# ─── PROMPT-ENCODED axioms (not programmable — fed to the model) ────────────
PROMPT_AXIOMS = {
    5: "Artist causality: jewellery only after neck exists, flowers only after positions set",
    7: "Cumulative progress: every stage makes the next one easier to develop toward the final",
    8: "Purposeful exploration: style experiments must serve construction (alignment, contour, rhythm), never just spectacle",
    12: "Continuous identity: same figure, pose, expression, instrument throughout — never lose the subject",
    14: "No arbitrary frame quota: give the journey as many stages as it needs",
}


def encode_prompt(stage_num: int, total: int, style_hint: str = "") -> str:
    """Build the prompt suffix that encodes all axioms for the model."""
    axioms = []
    # Checkpoint: warn about stage-specific traps
    if stage_num == 0:
        axioms.append("This is the SOURCE stage — reproduce the sketch exactly, add nothing.")
    elif stage_num == total - 1:
        axioms.append("This is the TARGET stage — match the final painting exactly.")
    elif stage_num <= 2:
        axioms.append("Exploration stage: construction guides only, no finished detail. "
                      "Style experiments allowed if they reveal geometry.")
    elif stage_num <= 4:
        axioms.append("Construction stage: proportional correction, contour establishment. "
                      "Keep exploration lines as construction.")
    elif stage_num <= 6:
        axioms.append("Detail stage: add ornament and features on established geometry. "
                      "Colour grows from the drawing, never floods.")
    else:
        axioms.append("Final stages: converge to the target. Small finishing actions only.")

    # Always-on axiom reminders
    axioms.append("Do not teleport elements — every change must be a visible drawing operation.")
    axioms.append("Do not change the medium or artistic style mid-journey.")
    axioms.append("Do not lose the figure, pose, or identity of the subject.")
    if style_hint:
        axioms.append(f"Style constraint: {style_hint}")
    return " ".join(axioms)


# ─── Combined validator ─────────────────────────────────────────────────────
def validate_stage(prev_img, next_img, stage: int, total: int,
                   sketch_hash: str = "", final_hash: str = "",
                   frame_hash: str = "") -> StageResult:
    """Run all programmable axioms on a stage transition."""
    result = StageResult(stage=stage, passed=True)

    if stage == 0 or stage == total - 1:
        r = axiom1_exact_endpoints(stage, total, sketch_hash, final_hash, frame_hash)
        if not r[0]:
            result.passed = False
            result.violations.append(r[1])

    r = axiom2_stroke_continuity(prev_img, next_img)
    if not r[0]:
        result.passed = False
        result.violations.append(r[1])
    result.scores['continuity'] = r[2]

    r = axiom3_small_transition(prev_img, next_img)
    if not r[0]:
        result.passed = False
        result.violations.append(r[1])
    result.scores['density_ratio'] = r[2]

    r = axiom4_conserved_geometry(prev_img, next_img)
    if not r[0]:
        result.warnings.append(r[1])
    result.scores['geometry_ssim'] = r[2]

    r = axiom6_material_continuity(prev_img, next_img)
    if not r[0]:
        result.passed = False
        result.violations.append(r[1])
    result.scores['saturation_delta'] = r[2]

    r = axiom9_progressive_colour(prev_img, next_img)
    if not r[0]:
        result.passed = False
        result.violations.append(r[1])

    r = axiom10_locality(prev_img, next_img)
    if not r[0]:
        result.warnings.append(r[1])
    result.scores['changed_regions'] = r[2]

    r = axiom11_no_hidden_work(prev_img, next_img)
    if not r[0]:
        result.warnings.append(r[1])

    if stage == total - 1 and sketch_hash:
        r = axiom13_final_convergence(prev_img, next_img)
        if not r[0]:
            result.passed = False
            result.violations.append(r[1])
        result.scores['final_ssim'] = r[2]

    return result


def file_hash(path: str) -> str:
    """Deterministic content hash for exact-endpoint comparison."""
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()[:16]
