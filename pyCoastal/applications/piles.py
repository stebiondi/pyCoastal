"""
Wave loads on slender piles: Morison forces, shear, moment and scour.

The load on a pile is not one number. It is a distribution up the pile that
changes through the wave cycle, and the two things a designer needs from it
(the base shear and the overturning moment at the mudline) peak at different
phases. This module computes the distribution, integrates it, and sweeps the
phase, rather than evaluating a formula at the crest and hoping.

The Morison equation splits the load on a slender member into a drag term,
in phase with the velocity, and an inertia term, in phase with the
acceleration::

    f(z) = 0.5 rho Cd D u|u|  +  rho Cm (pi D^2 / 4) du/dt

Slender means the member is small enough not to change the wave that is
loading it, conventionally D / L below about 0.2. Above that the wave
diffracts around the member and the Morison equation no longer applies; the
functions here say so rather than returning a number.

Sources
-------
Morison, J. R., O'Brien, M. P., Johnson, J. W. and Schaaf, S. A. (1950),
    "The force exerted by surface waves on piles".

Sarpkaya, T. (2010), Wave Forces on Offshore Structures. Drag and inertia
    coefficients, and their dependence on Keulegan-Carpenter number.

DNV-RP-C205 (2010), Environmental Conditions and Environmental Loads.
    Coefficient guidance for smooth and rough cylinders.

Fenton, J. D. (1988), "The numerical solution of steady water wave
    problems", Computers and Geosciences 14(3). The stream function wave
    used for the design wave, which stays valid up to breaking where linear
    theory does not.

Wheeler, J. D. (1970), "Method for calculating forces produced by irregular
    waves". The stretching used to carry linear kinematics up to the
    instantaneous free surface, when linear theory is asked for.

Sumer, B. M., Fredsoe, J. and Christiansen, N. (1992), "Scour around
    vertical pile in waves"; Sumer, B. M. and Fredsoe, J. (2001), "Scour
    around pile in combined waves and current". The scour relations used
    here.

Conventions
-----------
Elevation z is measured from the still water level and increases upward, so
the mudline is at z = -depth and a wave crest reaches z = +eta. Forces are
newtons, forces per unit length newtons per metre, and moments newton metres
about the mudline unless stated.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np

from ..tools.wave import dispersion

G = 9.81
RHO = 1025.0
NU = 1.19e-6          # kinematic viscosity of seawater at 15 C

__all__ = [
    "wave_kinematics",
    "StreamFunctionWave",
    "stream_function_wave",
    "bed_keulegan_carpenter",
    "keulegan_carpenter",
    "reynolds_number",
    "drag_inertia_coefficients",
    "morison_load_profile",
    "integrate_load",
    "PileLoad",
    "morison_pile_load",
    "phase_sweep",
    "scour_depth_pile",
    "design_monopile",
]


# ---------------------------------------------------------------------------
# Kinematics
# ---------------------------------------------------------------------------


def wave_kinematics(H: float, T: float, depth: float, z, phase: float = 0.0,
                    stretching: str = "wheeler") -> dict:
    """Horizontal velocity and acceleration under a linear wave.

    Parameters
    ----------
    H : float
        Wave height [m].
    T : float
        Period [s].
    depth : float
        Still water depth [m].
    z : array_like
        Elevations from the still water level, negative downward [m].
    phase : float
        Wave phase in radians. Zero is the crest at the pile.
    stretching : str
        "wheeler" maps the still-water profile onto the instantaneous water
        column, "none" evaluates linear theory as written, and "extrapolate"
        continues the still-water profile above the still water level.

        Linear theory says nothing about the water between the still water
        level and the crest, which is exactly where the load is largest.
        Extrapolating the cosh profile there overstates the velocity badly;
        Wheeler stretching is the usual fix and is the default.

    Returns
    -------
    dict
        ``u`` and ``dudt`` at each elevation, the surface elevation ``eta``,
        the wavelength, and a mask of which elevations are in the water.
    """
    if H <= 0 or T <= 0 or depth <= 0:
        raise ValueError("Height, period and depth must be positive")
    if stretching not in ("wheeler", "none", "extrapolate"):
        raise ValueError(f"Unknown stretching {stretching!r}")

    z = np.atleast_1d(np.asarray(z, dtype=float))
    L = dispersion(T, depth)
    k = 2 * math.pi / L
    omega = 2 * math.pi / T
    a = 0.5 * H
    eta = a * math.cos(phase)

    wet = z <= eta
    if stretching == "wheeler":
        z_eval = (z - eta) * depth / (depth + eta)
    elif stretching == "none":
        z_eval = np.minimum(z, 0.0)
    else:
        z_eval = z

    kz = k * (z_eval + depth)
    shape = np.cosh(kz) / math.sinh(k * depth)
    u = a * omega * shape * math.cos(phase)
    dudt = a * omega**2 * shape * math.sin(phase)

    u = np.where(wet, u, 0.0)
    dudt = np.where(wet, dudt, 0.0)
    return {"u": u, "dudt": dudt, "eta": eta, "wavelength": L, "k": k,
            "omega": omega, "wet": wet, "z_eval": z_eval}


def _sinh_ratio(j: np.ndarray, y: float, D: float) -> np.ndarray:
    """sinh(j y) / cosh(j D), written so large j D cannot overflow."""
    return ((np.exp(j * (y - D)) - np.exp(-j * (y + D)))
            / (1.0 + np.exp(-2.0 * j * D)))


def _cosh_ratio(j: np.ndarray, y: float, D: float) -> np.ndarray:
    """cosh(j y) / cosh(j D), overflow-safe."""
    return ((np.exp(j * (y - D)) + np.exp(-j * (y + D)))
            / (1.0 + np.exp(-2.0 * j * D)))


class StreamFunctionWave:
    """A steady nonlinear wave by Fenton's Fourier method.

    Solves the full nonlinear free-surface problem for a wave of given
    height, period and depth with no Eulerian mean current, in the
    dimensionless unknowns of Fenton (1988): kd, kH, T sqrt(gk), c sqrt(k/g),
    the two mean currents, the mean fluid speed, the flux q, the Bernoulli
    constant, the surface kη at N + 1 points over half a wavelength and the
    N Fourier coefficients B_j. Newton's method, with the height raised in
    steps from a linear start.

    Attributes
    ----------
    converged : bool
        False when Newton did not settle, which in practice means the wave
        is at or beyond breaking.
    """

    def __init__(self, H: float, T: float, depth: float, N: int = 20,
                 steps: int = 6, tolerance: float = 1e-10):
        if H <= 0 or T <= 0 or depth <= 0:
            raise ValueError("Height, period and depth must be positive")
        self.H, self.T, self.depth, self.N = H, T, depth, N
        self.converged = False
        self.z = None
        H_d = H / depth
        H_gT2 = H / (G * T**2)

        k = 2 * math.pi / dispersion(T, depth)
        kd = k * depth
        prev = prev2 = None
        z = None
        for step in range(1, steps + 1):
            frac = step / steps
            if prev is None:
                z = self._linear(kd, frac * H_d * kd, N)
            elif prev2 is None:
                z = prev.copy()
            else:
                z = 2.0 * prev - prev2
            # A wave past breaking sends Newton to overflow; that is the
            # answer (no solution), not an error to report.
            with np.errstate(all="ignore"):
                z = self._newton(z, frac * H_d, frac * H_gT2, tolerance)
            if z is None:
                return
            prev2, prev = prev, z
        self.z = z
        self.converged = True
        self.k = z[0] / depth
        self.celerity = z[3] * math.sqrt(G / self.k)
        self.wavelength = 2 * math.pi / self.k
        # Surface Fourier cosine coefficients, for eta at any phase.
        eta = z[9:10 + N]
        m = np.arange(N + 1)
        w = np.ones(N + 1)
        w[0] = w[-1] = 0.5
        self._E = np.array([2.0 / N * np.sum(w * eta * np.cos(j * m * math.pi / N))
                            for j in range(N + 1)])
        self.crest = eta[0] / self.k - depth
        self.trough = eta[-1] / self.k - depth

    @staticmethod
    def _linear(kd: float, kH: float, N: int) -> np.ndarray:
        z = np.zeros(2 * N + 10)
        c = math.sqrt(math.tanh(kd))
        z[0] = kd
        z[1] = kH
        z[3] = c
        z[2] = 2 * math.pi / c
        z[4] = 0.0
        z[5] = c
        z[6] = c
        z[7] = c * kd
        z[8] = 0.5 * c**2 + kd
        m = np.arange(N + 1)
        z[9:10 + N] = kd + 0.5 * kH * np.cos(m * math.pi / N)
        z[10 + N] = 0.5 * kH * c / math.tanh(kd)
        return z

    def _residual(self, z: np.ndarray, H_d: float, H_gT2: float) -> np.ndarray:
        N = self.N
        f = np.empty(2 * N + 10)
        f[0] = z[1] - z[0] * H_d
        f[1] = z[1] - H_gT2 * z[2] ** 2
        f[2] = z[2] * z[3] - 2 * math.pi
        f[3] = z[4] + z[6] - z[3]
        f[4] = z[5] + z[7] / z[0] - z[3]
        f[5] = z[4]                              # no Eulerian current
        eta = z[9:10 + N]
        f[6] = eta[0] + eta[-1] + 2.0 * np.sum(eta[1:-1]) - 2.0 * N * z[0]
        f[7] = eta[0] - eta[-1] - z[1]
        B = z[10 + N:]
        j = np.arange(1, N + 1, dtype=float)
        for m in range(N + 1):
            theta = m * math.pi / N
            cj = np.cos(j * theta)
            sj = np.sin(j * theta)
            sr = _sinh_ratio(j, eta[m], z[0])
            cr = _cosh_ratio(j, eta[m], z[0])
            psi = np.sum(B * sr * cj)
            u = -z[6] + np.sum(j * B * cr * cj)
            v = np.sum(j * B * sr * sj)
            f[8 + m] = psi - z[6] * eta[m] + z[7]
            f[9 + N + m] = 0.5 * (u * u + v * v) + eta[m] - z[8]
        return f

    def _newton(self, z: np.ndarray, H_d: float, H_gT2: float,
                tolerance: float) -> np.ndarray | None:
        n = z.size
        for _ in range(40):
            f = self._residual(z, H_d, H_gT2)
            J = np.empty((n, n))
            for i in range(n):
                h = 1e-7 * max(abs(z[i]), 1e-3)
                zp = z.copy()
                zp[i] += h
                J[:, i] = (self._residual(zp, H_d, H_gT2) - f) / h
            try:
                dz = np.linalg.solve(J, -f)
            except np.linalg.LinAlgError:
                return None
            z = z + dz
            if not np.all(np.isfinite(z)):
                return None
            if np.max(np.abs(dz)) < tolerance:
                return z
        return z if np.max(np.abs(self._residual(z, H_d, H_gT2))) < 1e-6 else None

    def surface(self, phase: float) -> float:
        """Surface elevation above still water at a phase [m]."""
        j = np.arange(self.N + 1)
        w = np.ones(self.N + 1)
        w[0] = w[-1] = 0.5
        keta = float(np.sum(w * self._E * np.cos(j * phase)))
        return keta / self.k - self.depth

    def kinematics(self, z, phase: float) -> dict:
        """Horizontal velocity and local acceleration, as wave_kinematics."""
        z = np.atleast_1d(np.asarray(z, dtype=float))
        N = self.N
        B = self.z[10 + N:]
        D = self.z[0]
        j = np.arange(1, N + 1, dtype=float)
        eta = self.surface(phase)
        wet = z <= eta
        u = np.zeros_like(z)
        dudt = np.zeros_like(z)
        scale_u = math.sqrt(G / self.k)
        scale_a = self.z[3] * G
        cj = np.cos(j * phase)
        sj = np.sin(j * phase)
        for i, zi in enumerate(z):
            if not wet[i]:
                continue
            ky = self.k * (min(zi, eta) + self.depth)
            cr = _cosh_ratio(j, ky, D)
            u[i] = scale_u * (self.z[4] + np.sum(j * B * cr * cj))
            dudt[i] = scale_a * np.sum(j * j * B * cr * sj)
        return {"u": u, "dudt": dudt, "eta": eta,
                "wavelength": self.wavelength, "k": self.k,
                "omega": 2 * math.pi / self.T, "wet": wet, "z_eval": z}


_STREAM_CACHE: dict = {}


def stream_function_wave(H: float, T: float, depth: float,
                         N: int = 20) -> StreamFunctionWave:
    """A solved stream function wave, cached since a phase sweep reuses it."""
    key = (round(H, 9), round(T, 9), round(depth, 9), N)
    wave = _STREAM_CACHE.get(key)
    if wave is None:
        wave = StreamFunctionWave(H, T, depth, N=N)
        if len(_STREAM_CACHE) > 64:
            _STREAM_CACHE.clear()
        _STREAM_CACHE[key] = wave
    return wave


def keulegan_carpenter(H: float, T: float, depth: float, diameter: float,
                       z: float = 0.0) -> float:
    """KC = u_max T / D, at elevation ``z``.

    Sets which Morison term dominates. Below about 3 the load is almost all
    inertia and the drag coefficient hardly matters; above about 20 drag
    governs and the inertia coefficient hardly matters. A monopile in a
    design storm usually sits awkwardly between the two.
    """
    if diameter <= 0:
        raise ValueError(f"Diameter must be positive, got {diameter}")
    kin = wave_kinematics(H, T, depth, [z], phase=0.0, stretching="none")
    return float(abs(kin["u"][0]) * T / diameter)


def bed_keulegan_carpenter(Hs: float, T: float, depth: float,
                           diameter: float) -> dict:
    """KC at the seabed from the significant wave, as scour relations use.

    U_m = pi Hs / (T sinh(k h)), linear theory at the bed, and
    KC = U_m T / D (Sumer and Fredsoe 2001). Not the KC at the surface
    under the design wave, which sets the Morison coefficients and is
    several times larger.
    """
    if diameter <= 0 or Hs <= 0 or T <= 0 or depth <= 0:
        raise ValueError("Diameter, height, period and depth must be positive")
    L = dispersion(T, depth)
    Um = math.pi * Hs / (T * math.sinh(2 * math.pi * depth / L))
    return {"Um": Um, "KC": Um * T / diameter}


def reynolds_number(H: float, T: float, depth: float, diameter: float,
                    z: float = 0.0, viscosity: float = NU) -> float:
    """Re = u_max D / nu, at elevation ``z``."""
    kin = wave_kinematics(H, T, depth, [z], phase=0.0, stretching="none")
    return float(abs(kin["u"][0]) * diameter / viscosity)


def drag_inertia_coefficients(KC: float, rough: bool = True) -> dict:
    """Indicative Cd and Cm, with the regime named.

    Post-critical Reynolds number values from DNV-RP-C205: a rough cylinder,
    which is what any pile becomes once marine growth establishes, takes
    Cd = 1.05, and a clean one Cd = 0.65. The inertia coefficient falls from
    the potential-flow value of 2.0 as KC rises and the wake starts to
    interfere with the next half cycle.

    Returns
    -------
    dict
        ``Cd``, ``Cm`` and the dominant ``regime``. These are starting
        values for a concept design. A real design takes them from the
        governing code for the actual roughness, KC and Re, and a real
        fatigue assessment does not use a single pair at all.
    """
    if KC <= 0:
        raise ValueError(f"KC must be positive, got {KC}")

    Cd = 1.05 if rough else 0.65
    if KC < 3.0:
        regime, Cm = "inertia dominated", 2.0
    elif KC < 15.0:
        regime, Cm = "mixed", 2.0 - 0.04 * (KC - 3.0)
    else:
        regime, Cm = "drag dominated", max(1.5, 2.0 - 0.04 * (KC - 3.0))
    return {"Cd": Cd, "Cm": Cm, "regime": regime, "KC": KC, "rough": rough}


# ---------------------------------------------------------------------------
# Morison load
# ---------------------------------------------------------------------------


def morison_load_profile(diameter: float, u, dudt, Cd: float = 1.05,
                         Cm: float = 2.0, rho: float = RHO) -> dict:
    """Inline force per unit length, split into its two terms [N/m]."""
    if diameter <= 0:
        raise ValueError(f"Diameter must be positive, got {diameter}")
    if Cd < 0 or Cm < 0:
        raise ValueError("Coefficients must be non-negative")

    u = np.asarray(u, dtype=float)
    dudt = np.asarray(dudt, dtype=float)
    drag = 0.5 * rho * Cd * diameter * u * np.abs(u)
    inertia = rho * Cm * 0.25 * math.pi * diameter**2 * dudt
    return {"drag": drag, "inertia": inertia, "total": drag + inertia}


def integrate_load(z, load, mudline: float) -> dict:
    """Total force and mudline moment from a load profile.

    Trapezoidal in z, which is what the profile is sampled on. The moment
    arm is measured from the mudline, so the result is the overturning
    moment the foundation has to carry.
    """
    z = np.asarray(z, dtype=float)
    load = np.asarray(load, dtype=float)
    if z.shape != load.shape:
        raise ValueError("Elevation and load arrays must match")
    if z.size < 2:
        raise ValueError("Need at least two points to integrate")

    force = float(np.trapezoid(load, z))
    moment = float(np.trapezoid(load * (z - mudline), z))
    arm = moment / force if force != 0 else 0.0
    return {"force": force, "moment": moment, "arm": arm}


@dataclass
class PileLoad:
    """Wave load on a pile at one phase, or at the worst phase."""

    diameter: float
    H: float
    T: float
    depth: float
    phase: float
    z: np.ndarray
    drag: np.ndarray
    inertia: np.ndarray
    total: np.ndarray
    force: float
    moment: float
    arm: float
    eta: float
    Cd: float
    Cm: float
    KC: float
    regime: str
    diffraction_ratio: float
    warnings: list[str] = field(default_factory=list)
    theory: str = "linear"

    @property
    def inertia_fraction(self) -> float:
        """Share of the total force carried by the inertia term."""
        inertia = abs(float(np.trapezoid(self.inertia, self.z)))
        drag = abs(float(np.trapezoid(self.drag, self.z)))
        total = inertia + drag
        return inertia / total if total > 0 else float("nan")

    def summary(self) -> str:
        lines = [
            f"Pile                {self.diameter:.2f} m diameter in "
            f"{self.depth:.1f} m of water",
            f"Wave                H = {self.H:.2f} m, T = {self.T:.1f} s, "
            f"{self.theory} theory",
            f"KC, regime          {self.KC:.1f}, {self.regime}",
            f"Cd, Cm              {self.Cd:.2f}, {self.Cm:.2f}",
            f"D / L               {self.diffraction_ratio:.3f}",
            "",
            f"Worst phase         {math.degrees(self.phase):.0f} degrees "
            f"(crest at 0), surface at {self.eta:+.2f} m",
            f"Base shear          {self.force / 1e3:,.0f} kN",
            f"Mudline moment      {self.moment / 1e6:,.1f} MNm",
            f"Effective arm       {self.arm:.2f} m above the mudline",
            f"Inertia share       {100 * self.inertia_fraction:.0f}% of the load",
        ]
        if self.warnings:
            lines += ["", "Warnings"] + [f"  - {w}" for w in self.warnings]
        return "\n".join(lines)


def morison_pile_load(diameter: float, H: float, T: float, depth: float,
                      phase: float = 0.0, Cd: float | None = None,
                      Cm: float | None = None, points: int = 400,
                      stretching: str = "wheeler", rough: bool = True,
                      air_gap: float = 0.0, theory: str = "stream") -> PileLoad:
    """Morison load on a vertical pile at one wave phase.

    Parameters
    ----------
    points : int
        Samples up the pile. The load is concentrated near the surface, so
        a coarse grid loses the peak; 400 is ample for a monopile.
    air_gap : float
        Elevation above the still water level to sample to. The profile is
        zero above the instantaneous surface, so this only matters for
        plotting the dry part of the pile.
    Cd, Cm : float, optional
        Taken from :func:`drag_inertia_coefficients` when not given.
    theory : str
        "stream" (default) for Fenton's stream function wave, which is what
        a design wave in intermediate or shallow water needs; "linear" for
        Airy theory with the ``stretching`` given. A stream function wave
        that does not converge is at breaking, and the load falls back to
        linear theory with a warning.
    """
    if points < 2:
        raise ValueError(f"Need at least two points, got {points}")

    KC = keulegan_carpenter(H, T, depth, diameter)
    coefficients = drag_inertia_coefficients(KC, rough=rough)
    Cd = coefficients["Cd"] if Cd is None else Cd
    Cm = coefficients["Cm"] if Cm is None else Cm

    if theory not in ("stream", "linear"):
        raise ValueError(f"Unknown wave theory {theory!r}")
    warnings: list[str] = []
    wave = None
    if theory == "stream" and H < 0.78 * depth:
        wave = stream_function_wave(H, T, depth)
        if not wave.converged:
            warnings.append(
                "The stream function wave did not converge, which puts this "
                "wave at breaking. Linear theory with Wheeler stretching is "
                "used instead and understates the crest kinematics."
            )
            wave = None
    top = (wave.crest if wave is not None else 0.5 * H) + air_gap
    z = np.linspace(-depth, top, points)
    if wave is not None:
        kin = wave.kinematics(z, phase)
    else:
        kin = wave_kinematics(H, T, depth, z, phase=phase, stretching=stretching)
    load = morison_load_profile(diameter, kin["u"], kin["dudt"], Cd, Cm)
    totals = integrate_load(z, load["total"], mudline=-depth)

    ratio = diameter / kin["wavelength"]
    if ratio > 0.2:
        warnings.append(
            f"D / L = {ratio:.2f} is above 0.2, so the pile diffracts the "
            "wave and the Morison equation does not apply. Use a diffraction "
            "method such as MacCamy and Fuchs."
        )
    if H > 0.78 * depth:
        warnings.append(
            f"H = {H:.2f} m exceeds 0.78 of the {depth:.1f} m depth, so the "
            "wave has broken. Breaking wave slam is a separate and much "
            "larger load, and is not computed here."
        )
    if wave is None and stretching == "extrapolate":
        warnings.append(
            "Kinematics were extrapolated above the still water level, which "
            "overstates the crest velocity. Wheeler stretching is the usual "
            "choice."
        )

    return PileLoad(
        diameter=diameter, H=H, T=T, depth=depth, phase=phase, z=z,
        drag=load["drag"], inertia=load["inertia"], total=load["total"],
        force=totals["force"], moment=totals["moment"], arm=totals["arm"],
        eta=kin["eta"], Cd=Cd, Cm=Cm, KC=KC, regime=coefficients["regime"],
        diffraction_ratio=ratio, warnings=warnings,
        theory="stream function" if wave is not None else "linear",
    )


def phase_sweep(diameter: float, H: float, T: float, depth: float,
                phases: int = 181, **kwargs) -> dict:
    """Force and moment through the wave cycle, and where each peaks.

    The base shear and the overturning moment do not peak at the same
    phase, because the drag term peaks under the crest while the inertia
    term peaks a quarter cycle earlier, and the two have different lever
    arms. Designing on the crest phase alone can miss the worst moment.
    """
    if phases < 3:
        raise ValueError(f"Need at least three phases, got {phases}")

    angles = np.linspace(0.0, 2 * math.pi, phases)
    force = np.empty(phases)
    moment = np.empty(phases)
    for i, angle in enumerate(angles):
        result = morison_pile_load(diameter, H, T, depth, phase=float(angle),
                                   **kwargs)
        force[i] = result.force
        moment[i] = result.moment

    i_force = int(np.argmax(np.abs(force)))
    i_moment = int(np.argmax(np.abs(moment)))
    return {
        "phase": angles,
        "force": force,
        "moment": moment,
        "max_force": float(abs(force[i_force])),
        "max_moment": float(abs(moment[i_moment])),
        "phase_of_max_force": float(angles[i_force]),
        "phase_of_max_moment": float(angles[i_moment]),
        "same_phase": i_force == i_moment,
    }


# ---------------------------------------------------------------------------
# Scour
# ---------------------------------------------------------------------------


def scour_depth_pile(diameter: float, KC: float, current_only: bool = False,
                     live_bed: bool = True, bed=None, Hs: float | None = None,
                     T: float | None = None, depth: float | None = None,
                     current_ratio: float = 0.0) -> dict:
    """Equilibrium scour depth at a vertical pile [m].

    Sumer and Fredsoe (2001), for combined waves and current::

        S / D = 1.3 [1 - exp(-A (KC - B))]      for KC > B
        A = 0.03 + 0.75 Ucw^2.6,  B = 6 exp(-4.7 Ucw)

    with Ucw = Uc / (Uc + Um) the current share of the near-bed velocity.
    Ucw = 0 recovers the waves-only relation of Sumer, Fredsoe and
    Christiansen (1992), with no scour below KC = 6, where the horseshoe
    vortex does not form. Under a steady current S / D = 1.3 with a
    standard deviation of 0.7, which is the ``current_only`` branch and the
    limit the others tend to.

    Parameters
    ----------
    KC : float
        Keulegan-Carpenter number at the bed from the significant wave,
        :func:`bed_keulegan_carpenter`.
    current_ratio : float
        Ucw, between 0 (waves only) and 1 (current only).

    Notes
    -----
    This is the equilibrium depth under a sustained condition, not the depth
    after one storm, and it is a live-bed result. In clear water the
    equilibrium is similar but takes far longer to develop. Scour protection
    is designed on the equilibrium depth; the pile itself is often checked
    for both, since a scoured pile is a longer cantilever and a softer one.
    """
    if diameter <= 0:
        raise ValueError(f"Diameter must be positive, got {diameter}")
    if KC <= 0:
        raise ValueError(f"KC must be positive, got {KC}")
    if not 0.0 <= current_ratio <= 1.0:
        raise ValueError(f"Ucw must be in [0, 1], got {current_ratio}")

    A = 0.03 + 0.75 * current_ratio**2.6
    B = 6.0 * math.exp(-4.7 * current_ratio)
    if current_only or current_ratio >= 1.0:
        ratio = 1.3
    elif KC <= B:
        ratio = 0.0
    else:
        ratio = 1.3 * (1.0 - math.exp(-A * (KC - B)))

    result = {
        "depth": ratio * diameter,
        "ratio": ratio,
        "KC": KC,
        "current_ratio": current_ratio,
        "no_scour": (not current_only) and ratio == 0.0,
        "standard_deviation": 0.7 * diameter if current_only else None,
        "live_bed": live_bed,
    }

    # Sumer and Fredsoe's experiments are live-bed results. A bed that never
    # reaches its threshold in the approach waves still scours locally,
    # where the pile amplifies the flow, but not to the live-bed depth.
    if bed is not None and None not in (Hs, T, depth):
        from .sediment import bed_mobility

        mobility = bed_mobility(bed, Hs, T, depth)
        result["mobility"] = mobility
        result["note"] = mobility["note"]
        if mobility.get("regime") == "cohesive":
            result["depth"] = 0.0
            result["applies"] = False
        elif not mobility["mobile"] and current_ratio == 0.0:
            result["depth"] *= 0.5
            result["applies"] = False
        else:
            result["applies"] = True
    return result


def design_monopile(diameter: float, H: float, T: float, depth: float,
                    rough: bool = True, stretching: str = "wheeler",
                    phases: int = 181, bed=None, theory: str = "stream",
                    Hs: float | None = None, current: float = 0.0) -> dict:
    """Worst-phase load, scour, and the numbers a foundation designer wants.

    Sweeps the phase for the worst moment rather than assuming the crest,
    returns the load at that phase, and adds the scour depth and the
    resulting increase in cantilever length.

    Parameters
    ----------
    H, T : float
        The design (maximum) wave, which loads the pile.
    Hs : float, optional
        The significant wave height of the sea state, which drives scour.
        Defaults to H / 1.86, the Rayleigh ratio for about 1000 waves.
    current : float
        Depth-averaged current speed at the pile [m/s]. Tidal currents are
        present at almost every monopile site and dominate its scour.
    """
    if current < 0:
        raise ValueError(f"Current must be non-negative, got {current}")
    Hs = H / 1.86 if Hs is None else Hs
    sweep = phase_sweep(diameter, H, T, depth, phases=phases, rough=rough,
                        stretching=stretching, theory=theory)
    worst = morison_pile_load(diameter, H, T, depth,
                             phase=sweep["phase_of_max_moment"], rough=rough,
                             stretching=stretching, theory=theory)
    crest = morison_pile_load(diameter, H, T, depth, phase=0.0, rough=rough,
                              stretching=stretching, theory=theory)
    bed_kc = bed_keulegan_carpenter(Hs, T, depth, diameter)
    Ucw = current / (current + bed_kc["Um"]) if current + bed_kc["Um"] > 0 else 0.0
    scour = scour_depth_pile(diameter, bed_kc["KC"], bed=bed, Hs=Hs, T=T,
                             depth=depth, current_ratio=Ucw)
    scour["Um"] = bed_kc["Um"]
    scour["Hs"] = Hs

    missed = (abs(worst.moment) - abs(crest.moment)) / abs(worst.moment)
    if missed > 0.02:
        worst.warnings.append(
            f"The worst moment is {100 * missed:.0f}% larger than the moment "
            "at the crest phase. Designing on the crest alone would have "
            "understated it."
        )
    if current == 0.0:
        worst.warnings.append(
            "No current was given, so the scour is for waves alone. A tidal "
            "current of even 0.5 m/s usually dominates monopile scour and "
            "takes it towards 1.3 D; give the site current before relying "
            "on this number."
        )
    return {
        "load": worst,
        "crest_load": crest,
        "sweep": sweep,
        "scour": scour,
        "crest_underestimate": missed,
        "cantilever_increase": scour["depth"],
    }
