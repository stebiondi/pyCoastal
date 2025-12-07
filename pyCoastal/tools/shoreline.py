# shoreline.py
#
# One-line shoreline change utilities with simple diffraction shadowing
# for detached breakwaters (any number of tips).

import math
import numpy as np

try:
    from numpy.typing import ArrayLike
except ImportError:  # pragma: no cover - typing convenience only
    ArrayLike = np.ndarray  # type: ignore


class OneLineParams:
    """
    Parameters for the one-line shoreline change model:
      D      active profile depth [m]
      p      porosity [-]
      Kcerc  alongshore transport coefficient [SI units so that Q is m^3/s]
      Hfree  offshore or structure-free breaking height field H_b,free(x) [m] or scalar
      alpha0 incident breaking angle relative to local shoreline, before feedback [rad] or array over x
      Kt     transmission factor field in [0,1] or scalar
      beta0  incident wave direction azimuth [rad], measured from +x axis pointing alongshore
      morfac morphological acceleration factor for faster adjustment
    """

    def __init__(
        self,
        D: float = 8.0,
        p: float = 0.4,
        Kcerc: float = 0.4,
        Hfree: float | ArrayLike = 1.0,
        alpha0: float | ArrayLike = np.deg2rad(10.0),
        Kt: float | ArrayLike = 1.0,
        beta0: float = np.deg2rad(-30.0),
        morfac: float = 1.0,
    ):
        self.D = float(D)
        self.p = float(p)
        self.Kcerc = float(Kcerc)
        self.Hfree = Hfree
        self.alpha0 = alpha0
        self.Kt = Kt
        self.beta0 = float(beta0)
        self.morfac = float(morfac)


def make_grid(Lx: float = 1000.0, dx: float = 5.0) -> tuple[np.ndarray, np.ndarray]:
    """
    Alongshore grid x and initial shoreline position y(x,0).
    y is the cross-shore offset at MSL. y0=0 means straight shoreline.
    """
    x = np.arange(0.0, Lx + dx, dx)
    y = np.zeros_like(x)
    return x, y


def breakwaters_geometry(
    x: np.ndarray,
    tips: list[float] | tuple[float, ...],
    y_tip: float = 150.0,
    crest_freeboard: float = 2.0,
) -> dict:
    """
    Geometry for N detached rubble-mound breakwaters.
      tips    iterable of alongshore tip positions [m]
      y_tip   offshore distance of the tips from initial shoreline [m]
    Returns dictionary with arrays over x.
    """
    return {
        "tips": tuple(float(v) for v in tips),
        "y_tip": float(y_tip),
        "crest_freeboard": float(crest_freeboard),
        "x": x.copy(),
    }


def _gaussian_smooth(arr: np.ndarray, sigma: float = 1.0) -> np.ndarray:
    """Lightweight 1D Gaussian smoothing without scipy dependency."""
    # kernel width ~ 3 sigma on either side
    half = max(1, int(3 * sigma))
    xk = np.arange(-half, half + 1, 1.0)
    kernel = np.exp(-(xk**2) / (2 * sigma**2))
    kernel /= kernel.sum()
    padded = np.pad(arr, half, mode="edge")
    conv = np.convolve(padded, kernel, mode="same")
    return conv[half:-half]


def kd_diffraction_field(x: np.ndarray, geom: dict, beta0: float) -> np.ndarray:
    """
    Simple linear-diffraction shadow factor Kd(x) in [0,1].
    Approximates each breakwater tip as a semi-infinite barrier.
    Kd = 0.5*(1 + cos(theta)) clamped, where theta is the diffraction angle between
    incident direction and the ray from the tip to the shoreline point (x,0).
    Combined shadow from both tips taken as min over the two tips.
    """

    def kd_from_tip(x_tip: float) -> np.ndarray:
        dxv = x - x_tip
        dy = 0.0 - geom["y_tip"]  # from tip to shoreline at y=0
        ray_ang = np.arctan2(dy, dxv)  # angle of ray from tip to cell, measured from +x
        theta = np.mod(ray_ang - beta0 + math.pi, 2 * math.pi) - math.pi
        kd_raw = 0.5 * (1.0 + np.cos(np.clip(np.abs(theta), 0.0, math.pi)))
        return np.clip(kd_raw, 0.0, 1.0)

    tips = geom.get("tips", None)
    if tips is None:
        # backward compatibility with older two-breakwater geometry
        tips = (geom["x1"], geom["x2"])
    kd_list = [kd_from_tip(xi) for xi in tips]
    kd = kd_list[0]
    for kd_i in kd_list[1:]:
        kd = np.minimum(kd, kd_i)

    return _gaussian_smooth(kd, sigma=1.0)


def field_or_scalar_to_array(val: float | ArrayLike, x: np.ndarray) -> np.ndarray:
    """Broadcast scalar to 1D array if needed, otherwise validate shape."""
    if np.isscalar(val):
        return np.full_like(x, float(val), dtype=float)
    arr = np.array(val, dtype=float)
    if arr.shape != x.shape:
        raise ValueError("Field length must match x")
    return arr


def compute_flux_Qls(
    x: np.ndarray,
    y: np.ndarray,
    pars: OneLineParams,
    kd: np.ndarray,
    Hfree: np.ndarray,
    Kt: np.ndarray,
    alpha0: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Q_ls = Kcerc * H_b^(5/2) * sin(2*alpha_b)
    alpha_b = alpha0 - y_x  (small angle approximation, radians)
    H_b = kd * Kt * Hfree
    """
    dx = x[1] - x[0]
    yx = np.gradient(y, dx)
    Hb = kd * Kt * Hfree
    alpha_b = alpha0 - yx
    Qls = pars.Kcerc * np.power(np.maximum(Hb, 0.0), 2.5) * np.sin(2.0 * alpha_b)
    return Qls, Hb, alpha_b


def rhs_y_t(
    x: np.ndarray,
    y: np.ndarray,
    pars: OneLineParams,
    kd: np.ndarray,
    Hfree: np.ndarray,
    Kt: np.ndarray,
    alpha0: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    y_t = - 1/((1-p) D) * dQls/dx
    """
    Qls, Hb, alpha_b = compute_flux_Qls(x, y, pars, kd, Hfree, Kt, alpha0)
    dx = x[1] - x[0]
    dQdx = np.gradient(Qls, dx)
    fac = -1.0 / ((1.0 - pars.p) * pars.D)
    return fac * dQdx, Qls, Hb, alpha_b


def suggest_dt(x: np.ndarray, pars: OneLineParams, Hb: np.ndarray) -> float:
    """
    Stability guidance for explicit scheme from linearized diffusion term:
      G = 2 Kcerc H_b^(5/2) / ((1-p) D)
      dt <= 0.45 * dx^2 / max(G)
    """
    dx = x[1] - x[0]
    G = 2.0 * pars.Kcerc * np.power(np.maximum(Hb, 0.0), 2.5) / (
        (1.0 - pars.p) * pars.D
    )
    Gmax = max(1e-12, float(np.max(G)))
    return 0.45 * dx * dx / Gmax


def apply_bcs(y: np.ndarray, bc: str = "fixed_ends", yL: float = 0.0, yR: float = 0.0) -> np.ndarray:
    """
    Boundary conditions on y.
      fixed_ends: y(0)=yL, y(L)=yR
      zero_slope: y_x=0 at ends
    """
    y_new = y.copy()
    if bc == "fixed_ends":
        y_new[0] = yL
        y_new[-1] = yR
    elif bc == "zero_slope":
        y_new[0] = y_new[1]
        y_new[-1] = y_new[-2]
    else:
        raise ValueError("Unknown BC")
    return y_new


def run_one_line_model() -> tuple[np.ndarray, np.ndarray, np.ndarray, dict, OneLineParams, dict]:
    """
    Convenience runner with default 2-breakwater setup (backward-compatible).
    Returns x, y_final, kd, hist, pars, geom.
    """
    x, y = make_grid(Lx=1000.0, dx=5.0)

    pars = OneLineParams(
        D=8.0,
        p=0.4,
        Kcerc=0.35,
        Hfree=1.0,
        alpha0=np.deg2rad(12.0),
        Kt=0.9,
        beta0=np.deg2rad(-25.0),
        morfac=1.0,
    )

    geom = breakwaters_geometry(
        x, tips=(400.0, 600.0), y_tip=150.0, crest_freeboard=2.0
    )

    kd = kd_diffraction_field(x, geom, pars.beta0)
    Hfree = field_or_scalar_to_array(pars.Hfree, x)
    Kt = field_or_scalar_to_array(pars.Kt, x)
    alpha0 = field_or_scalar_to_array(pars.alpha0, x)

    y[:] = 0.0

    _, Hb0, _ = compute_flux_Qls(x, y, pars, kd, Hfree, Kt, alpha0)
    dt_stab = suggest_dt(x, pars, Hb0)
    dt = 0.8 * dt_stab / pars.morfac

    t = 0.0
    t_end_days = 120.0
    seconds_per_day = 86400.0
    t_end = t_end_days * seconds_per_day / pars.morfac

    save_every = 500
    hist: dict[str, list] = {"t": [], "y": []}
    it = 0

    while t < t_end:
        yt, Qls, Hb, alpha_b = rhs_y_t(x, y, pars, kd, Hfree, Kt, alpha0)

        # Forward Euler
        y_new = y + dt * yt

        # Boundary conditions at domain ends
        y_new = apply_bcs(y_new, bc="fixed_ends", yL=0.0, yR=0.0)

        # Optional pinning at breakwater heads once a tombolo touches the tips
        for tip in geom["tips"]:
            idx_tip = int(np.argmin(np.abs(x - tip)))
            y_new[idx_tip] = min(y_new[idx_tip], geom["y_tip"])

        y = y_new
        t += dt
        it += 1

        if it % save_every == 0 or t >= t_end:
            hist["t"].append(t * pars.morfac)
            hist["y"].append(y.copy())

        # Optional adaptive dt with updated Hb
        if it % 50 == 0:
            dt = min(dt, 0.8 * suggest_dt(x, pars, Hb) / pars.morfac)

    return x, y, kd, hist, pars, geom
