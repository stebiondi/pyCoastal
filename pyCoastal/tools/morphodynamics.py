# morphodynamics.py

import math
import numpy as np

def circle_through_points(p1, p2, p3, n=200):
    """
    Build a circular arc passing through three non-collinear points (x, y).
    Returns x, y arrays following the branch that goes through p2.
    """
    (x1, y1), (x2, y2), (x3, y3) = p1, p2, p3
    temp = x2**2 + y2**2
    bc = (x1**2 + y1**2 - temp) / 2.0
    cd = (temp - x3**2 - y3**2) / 2.0
    det = (x1 - x2) * (y2 - y3) - (x2 - x3) * (y1 - y2)
    if abs(det) < 1e-12:
        raise ValueError("Points are collinear; cannot fit circle")
    cx = (bc * (y2 - y3) - cd * (y1 - y2)) / det
    cy = ((x1 - x2) * cd - (x2 - x3) * bc) / det
    r = math.hypot(cx - x1, cy - y1)

    ang1 = math.atan2(y1 - cy, x1 - cx)
    ang2 = math.atan2(y2 - cy, x2 - cx)
    ang3 = math.atan2(y3 - cy, x3 - cx)

    def angle_in_between(a, b, c):
        return math.sin(b - a) * math.sin(c - a) > 0

    if angle_in_between(ang1, ang3, ang2):
        angles = np.linspace(ang1, ang3, n)
    else:
        if ang3 > ang1:
            ang3 -= 2 * math.pi
        else:
            ang3 += 2 * math.pi
        angles = np.linspace(ang1, ang3, n)

    x = cx + r * np.cos(angles)
    y = cy + r * np.sin(angles)
    return x, y


def two_point_arc(p_start, p_end, sag, n=200):
    """
    Arc through two points with a prescribed sag (positive = bulge up, negative = bulge down).
    """
    (x1, y1), (x2, y2) = p_start, p_end
    mx, my = 0.5 * (x1 + x2), 0.5 * (y1 + y2)
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy)
    if L == 0:
        return np.array([x1, x2]), np.array([y1, y2])
    nx, ny = -dy / L, dx / L  # left-hand normal
    h = sag
    R = (L**2) / (8.0 * abs(h)) + abs(h) / 2.0
    sign = 1.0 if h >= 0 else -1.0
    cx = mx + sign * nx * (R - abs(h))
    cy = my + sign * ny * (R - abs(h))
    ang1 = math.atan2(y1 - cy, x1 - cx)
    ang2 = math.atan2(y2 - cy, x2 - cx)
    if ang2 < ang1:
        ang2 += 2 * math.pi
    angles = np.linspace(ang1, ang2, n)
    x = cx + R * np.cos(angles)
    y = cy + R * np.sin(angles)
    return x, y


def build_tombolo_arcs(Lshore: float, Gb: float, Lb1: float, Lb2: float, yb: float,
                       x_b1: float | None = None, x_b2: float | None = None,
                       n_pts: int = 200, sag_side_factor: float = 0.3) -> tuple[np.ndarray, np.ndarray, dict]:
    """
    Build a schematic shoreline (Hsu/Evans-like) using three arcs: left, central, right.
    Ye = 1.204*Yi - 0.07*Gb is the retreat depth below the breakwater crest line.
    """
    if x_b1 is None or x_b2 is None:
        x_b1 = Lshore / 2.0 - Gb 
        x_b2 = Lshore / 2.0 + Gb 

    Yi = yb
    Ye = 1.204 * Yi - 0.07 * Gb

    S0 = (x_b1 - (Gb + Lb1) / 2.0, Yi - Ye)
    S1 = (x_b2 + (Gb + Lb2) / 2.0, Yi - Ye)

    tf1 = 0.2 * Lb1
    tf2 = 0.2 * Lb2
    T1 = (x_b1 - tf1, Yi)
    T2 = (x_b1 + tf1, Yi)
    T3 = (x_b2 - tf2, Yi)
    T4 = (x_b2 + tf2, Yi)

    Sx = 0.5 * (T2[0] + T3[0])
    S = (Sx, Yi - Ye)

    sag_side = sag_side_factor * Ye
    xA, yA = two_point_arc(S0, T1, sag_side, n=n_pts)
    xB, yB = circle_through_points(T2, S, T3, n=n_pts)
    xC, yC = two_point_arc(T4, S1, sag_side, n=n_pts)

    x_eq = np.concatenate([xA, xB, xC])
    y_eq = np.concatenate([yA, yB, yC])

    geom = {
        "Lshore": Lshore,
        "Gb": Gb,
        "Lb1": Lb1,
        "Lb2": Lb2,
        "x_b1": x_b1,
        "x_b2": x_b2,
        "Yi": Yi,
        "Ye": Ye,
        "T1": T1,
        "T2": T2,
        "T3": T3,
        "T4": T4,
        "S0": S0,
        "S": S,
        "S1": S1,
    }
    return x_eq, y_eq, geom


def accretion_metrics(x_eq: np.ndarray, y_eq: np.ndarray, geom: dict) -> tuple[float, float]:
    """
    Compute retreat (Yi-Ye) and accretion percentage including rectangles under T1–T2 and T3–T4.
    """
    retreat_val = geom["Yi"] - geom["Ye"]
    area_red = np.trapz(np.maximum(0.0, -y_eq), x_eq)
    bw1_area = max(0.0, (geom["T2"][0] - geom["T1"][0]) * max(0.0, geom["Yi"]))
    bw2_area = max(0.0, (geom["T4"][0] - geom["T3"][0]) * max(0.0, geom["Yi"]))
    area_red += bw1_area + bw2_area
    area_ref = (geom["S1"][0] - geom["S0"][0]) * abs(geom["Ye"]) if abs(geom["Ye"]) > 1e-9 else 1.0
    acc_pct = 100.0 * area_red / area_ref
    return retreat_val, acc_pct

def bruuns_rule(S: float, beta: float, L: float = None, h: float = None, B: float = None) -> float:
    """
    Estimate shoreline retreat (R) using Bruun's rule.
    If L, h, and B are provided: R = S*L / (h + B)
    Else: R = S / tan(beta)
    """
    if L is not None and h is not None and B is not None:
        return S * L / (h + B)
    return S / math.tan(beta)


def exner_change(qs_dx: float, porosity: float = 0.64) -> float:
    """
    Compute bed elevation change rate (∂η/∂t) from sediment divergence based on the Exner equation.
    ∂η/∂t = -1/(1–n) * qs_dx
    """
    return -qs_dx / (1 - porosity)


def linear_slope(grid, north_level: float, south_level: float) -> np.ndarray:
    """
    Create a plane beach profile that is south_level at y=0 and north_level at y=L_y.
    """
    _, dy = grid.spacing
    Ly = grid.shape[1] * dy
    y = grid.Xc[1]
    return south_level + (north_level - south_level) * (y / Ly)
