"""
Port layout simulator.

Propagates a phase-resolved wave field into a harbour and reports how much
wave energy reaches the berths. Breakwaters are rasterized onto the grid as
reflecting walls, waves enter from a soft source line, and the open
boundaries are damped by sponge layers so outgoing and reflected energy
leaves the domain instead of ringing around it.

The solver integrates the second-order wave equation

    d2 eta / dt2 = div( c^2 grad eta )

in flux form, with zero flux on every face touching a breakwater cell. The
celerity c is taken from the linear dispersion relation at the local depth
and the chosen wave period, using ``pyCoastal.tools.wave.dispersion``, so the
wavelength is correct in intermediate water rather than the shallow-water
approximation sqrt(g h). The model is therefore accurate for the single
frequency it is run at; it is not a broad-banded spectral model, and it does
not represent breaking, wave-current interaction, or nonlinear transfers.

Harbour performance is reported as the disturbance coefficient

    Kd = H_local / H_reference

with H_reference measured at a probe in open water outside the harbour. That
normalisation makes the result independent of how the source is calibrated.

Coordinates follow the package convention: x and y span the horizontal
plane with x on axis 0, z is elevation.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np

from ..tools.wave import dispersion

G = 9.81


# ---------------------------------------------------------------------------
# Geometry
# ---------------------------------------------------------------------------


@dataclass
class Breakwater:
    """A breakwater as a polyline of a given thickness.

    Attributes
    ----------
    points : sequence of (x, y)
        Vertices of the centreline [m]. Two points give a straight arm;
        more give a bent or dog-leg structure.
    width : float
        Structure thickness [m]. Cells within ``width / 2`` of the
        centreline become land.
    name : str
        Label used in reports and plots.
    absorption : float
        Energy absorption of the seaward face, 0 for a fully reflecting
        vertical wall and 1 for a perfect absorber. A rubble-mound armour
        slope is roughly 0.5 to 0.8. Implemented as a damping collar in the
        water next to the structure, so this is a model knob and not the
        reflection coefficient itself. Measured Kr for a normally incident
        wave, from ``measure_reflection``:

            absorption  0.00  0.25  0.50  0.75  1.00
            Kr          0.95  0.48  0.22  0.19  0.25

        The mapping is not monotonic: past about 0.75 the collar is damped so
        strongly that it becomes an impedance step and starts reflecting
        again. Use roughly 0.3 to 0.4 for a rubble mound (Kr near 0.4), and
        leave it at 0 for a vertical caisson.
    """

    points: list[tuple[float, float]]
    width: float = 20.0
    name: str = "breakwater"
    absorption: float = 0.0

    def __post_init__(self) -> None:
        if len(self.points) < 2:
            raise ValueError(
                f"A breakwater needs at least two points, got {len(self.points)}"
            )
        if self.width <= 0:
            raise ValueError(f"Breakwater width must be positive, got {self.width}")
        if not 0.0 <= self.absorption <= 1.0:
            raise ValueError(
                f"Absorption must be in [0,1], got {self.absorption}"
            )

    def distance_field(self, X: np.ndarray, Y: np.ndarray) -> np.ndarray:
        """Distance from every grid point to this structure's centreline [m]."""
        d = np.full(X.shape, np.inf)
        for p0, p1 in zip(self.points, self.points[1:]):
            d = np.minimum(d, _distance_to_segment(X, Y, p0, p1))
        return d


def _distance_to_segment(
    X: np.ndarray, Y: np.ndarray, p0: tuple[float, float], p1: tuple[float, float]
) -> np.ndarray:
    """Perpendicular distance from every grid point to a line segment."""
    x0, y0 = p0
    x1, y1 = p1
    dx, dy = x1 - x0, y1 - y0
    length_sq = dx * dx + dy * dy

    if length_sq == 0.0:
        return np.hypot(X - x0, Y - y0)

    t = ((X - x0) * dx + (Y - y0) * dy) / length_sq
    t = np.clip(t, 0.0, 1.0)
    return np.hypot(X - (x0 + t * dx), Y - (y0 + t * dy))


@dataclass
class PortLayout:
    """Harbour geometry and bathymetry.

    Attributes
    ----------
    Lx, Ly : float
        Domain extent [m].
    dx : float
        Grid spacing [m], used in both directions.
    depth : float
        Still-water depth [m]. Constant depth only; refraction over a
        varying bed is out of scope for this solver.
    breakwaters : list of Breakwater
        Structures rasterized as reflecting walls.
    """

    Lx: float = 1200.0
    Ly: float = 900.0
    dx: float = 4.0
    depth: float = 10.0
    breakwaters: list[Breakwater] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.Lx <= 0 or self.Ly <= 0:
            raise ValueError(f"Domain must be positive, got {self.Lx} x {self.Ly}")
        if self.dx <= 0:
            raise ValueError(f"Grid spacing must be positive, got {self.dx}")
        if self.depth <= 0:
            raise ValueError(f"Depth must be positive, got {self.depth}")

    @property
    def shape(self) -> tuple[int, int]:
        nx = int(round(self.Lx / self.dx)) + 1
        ny = int(round(self.Ly / self.dx)) + 1
        return nx, ny

    def coordinates(self) -> tuple[np.ndarray, np.ndarray]:
        """1D coordinate arrays (x, y) [m]."""
        nx, ny = self.shape
        return np.arange(nx) * self.dx, np.arange(ny) * self.dx

    def meshgrid(self) -> tuple[np.ndarray, np.ndarray]:
        """2D coordinate arrays with x on axis 0."""
        x, y = self.coordinates()
        return np.meshgrid(x, y, indexing="ij")

    def land_mask(self) -> np.ndarray:
        """Boolean array, True where a breakwater occupies the cell."""
        X, Y = self.meshgrid()
        mask = np.zeros(self.shape, dtype=bool)

        for bw in self.breakwaters:
            half = 0.5 * bw.width
            for p0, p1 in zip(bw.points, bw.points[1:]):
                mask |= _distance_to_segment(X, Y, p0, p1) <= half

        return mask


def harbour_layout(
    Lx: float = 1200.0,
    Ly: float = 900.0,
    dx: float = 4.0,
    depth: float = 10.0,
    gap: float = 120.0,
    arm_length: float = 330.0,
    width: float = 24.0,
    back_wall: bool = True,
    absorption: float = 0.0,
) -> PortLayout:
    """A conventional two-arm harbour with a gap entrance.

    Two shore-normal breakwaters project from the downwave (east) side of the
    domain, leaving an opening of width ``gap`` centred on the domain. With
    ``back_wall`` the basin is closed by a quay along the landward edge, so
    energy entering the harbour has to leave through the gap again. Handy as
    a starting point and as the geometry used in the tests. ``absorption``
    is applied to every structure; see ``Breakwater.absorption``.

    When using a back wall, drop "east" from ``simulate_port(sponge_sides=...)``
    so the quay reflects instead of being absorbed.
    """
    x_entrance = 0.70 * Lx
    y_mid = 0.5 * Ly
    half_gap = 0.5 * gap
    structures = []

    south = Breakwater(
        points=[(x_entrance, y_mid - half_gap - arm_length), (x_entrance, y_mid - half_gap)],
        width=width,
        absorption=absorption,
        name="south arm",
    )
    north = Breakwater(
        points=[(x_entrance, y_mid + half_gap), (x_entrance, y_mid + half_gap + arm_length)],
        width=width,
        absorption=absorption,
        name="north arm",
    )
    structures.extend([south, north])

    if back_wall:
        # A shore-parallel quay closing the basin, one cell in from the edge.
        quay_x = Lx - 2.0 * dx
        structures.append(
            Breakwater(
                points=[(quay_x, 0.0), (quay_x, Ly)],
                width=2.0 * dx,
                absorption=absorption,
                name="quay",
            )
        )

    return PortLayout(Lx=Lx, Ly=Ly, dx=dx, depth=depth, breakwaters=structures)


# ---------------------------------------------------------------------------
# Forcing
# ---------------------------------------------------------------------------


@dataclass
class IncidentWave:
    """Monochromatic incident wave.

    Attributes
    ----------
    height : float
        Incident wave height H [m].
    period : float
        Wave period [s].
    direction : float
        Propagation direction [rad], measured from the +x axis. Zero sends
        the wave straight up-domain toward the harbour entrance.
    """

    height: float = 1.5
    period: float = 8.0
    direction: float = 0.0

    def __post_init__(self) -> None:
        if self.height <= 0:
            raise ValueError(f"Wave height must be positive, got {self.height}")
        if self.period <= 0:
            raise ValueError(f"Wave period must be positive, got {self.period}")

    @property
    def amplitude(self) -> float:
        return 0.5 * self.height

    @property
    def omega(self) -> float:
        return 2.0 * math.pi / self.period

    def wavelength(self, depth: float) -> float:
        """Wavelength at the given depth [m], from the dispersion relation."""
        return dispersion(self.period, depth)

    def celerity(self, depth: float) -> float:
        """Phase celerity at the given depth [m/s]."""
        return self.wavelength(depth) / self.period


# ---------------------------------------------------------------------------
# Result
# ---------------------------------------------------------------------------


@dataclass
class PortResult:
    """Output of a port simulation.

    Attributes
    ----------
    x, y : np.ndarray
        Coordinate axes [m].
    times : np.ndarray
        Times of the stored snapshots [s].
    snapshots : np.ndarray
        Surface elevation, shape (n_times, nx, ny) [m].
    land : np.ndarray
        Breakwater mask, shape (nx, ny).
    wave_height : np.ndarray
        Wave height over the analysis window, shape (nx, ny) [m].
    reference_height : float
        Wave height at the reference probe in open water [m].
    layout, wave
        The inputs the run came from.
    """

    x: np.ndarray
    y: np.ndarray
    times: np.ndarray
    snapshots: np.ndarray
    land: np.ndarray
    wave_height: np.ndarray
    reference_height: float
    layout: PortLayout
    wave: IncidentWave

    @property
    def disturbance_coefficient(self) -> np.ndarray:
        """Kd = H_local / H_reference, masked to water cells."""
        kd = self.wave_height / self.reference_height
        return np.where(self.land, np.nan, kd)

    def probe(self, point: tuple[float, float]) -> float:
        """Disturbance coefficient at a point [m, m]."""
        i = int(np.argmin(np.abs(self.x - point[0])))
        j = int(np.argmin(np.abs(self.y - point[1])))
        if self.land[i, j]:
            raise ValueError(f"Point {point} lies inside a breakwater")
        return float(self.wave_height[i, j] / self.reference_height)

    def berth_report(self, berths: dict[str, tuple[float, float]]) -> dict[str, dict]:
        """Wave height and Kd at each named berth."""
        report = {}
        for name, point in berths.items():
            kd = self.probe(point)
            report[name] = {
                "position": point,
                "Kd": kd,
                "Hs": kd * self.wave.height,
            }
        return report

    def operable_fraction(
        self, berths: dict[str, tuple[float, float]], limit: float
    ) -> dict[str, bool]:
        """Whether each berth stays below an operational wave-height limit [m]."""
        return {
            name: info["Hs"] <= limit
            for name, info in self.berth_report(berths).items()
        }


# ---------------------------------------------------------------------------
# Solver
# ---------------------------------------------------------------------------


VALID_SIDES = ("west", "east", "south", "north")


def _sponge_profile(
    shape: tuple[int, int],
    dx: float,
    thickness: float,
    strength: float,
    sides: tuple[str, ...] = VALID_SIDES,
) -> np.ndarray:
    """Damping coefficient array, zero inside and rising into the margins.

    Only the named ``sides`` absorb. A side left out reflects, which is what
    you want where the domain edge represents a quay or a coastline rather
    than open sea.
    """
    unknown = set(sides) - set(VALID_SIDES)
    if unknown:
        raise ValueError(f"Unknown sponge sides {sorted(unknown)}")

    nx, ny = shape
    i = np.arange(nx) * dx
    j = np.arange(ny) * dx
    Lx, Ly = (nx - 1) * dx, (ny - 1) * dx

    def ramp(distance):
        return np.clip((thickness - distance) / thickness, 0.0, 1.0) ** 2

    damp = np.zeros((nx, ny))
    if "west" in sides:
        damp = np.maximum(damp, ramp(i)[:, None])
    if "east" in sides:
        damp = np.maximum(damp, ramp(Lx - i)[:, None])
    if "south" in sides:
        damp = np.maximum(damp, ramp(j)[None, :])
    if "north" in sides:
        damp = np.maximum(damp, ramp(Ly - j)[None, :])

    return strength * damp


def _step_field(
    land: np.ndarray,
    layout: PortLayout,
    wave: IncidentWave,
    *,
    duration: float,
    dt: float,
    c2: np.ndarray,
    damping: np.ndarray,
    source_profile: np.ndarray,
    source_phase: np.ndarray,
    source_scale: float,
    ramp_periods: float,
    analysis_window: float,
    snapshot_times: np.ndarray | None,
) -> tuple[np.ndarray, list[np.ndarray]]:
    """Integrate the wave equation and return (wave_height, snapshots).

    Shared by the calibration pilot and the real run so both see exactly the
    same discretisation.
    """
    nx, ny = layout.shape
    dx = layout.dx
    n_steps = int(round(duration / dt))
    analysis_start = duration - analysis_window

    wet = ~land
    face_x = wet[:-1, :] & wet[1:, :]
    face_y = wet[:, :-1] & wet[:, 1:]

    eta_prev = np.zeros((nx, ny))
    eta = np.zeros((nx, ny))
    fx = np.zeros((nx + 1, ny))
    fy = np.zeros((nx, ny + 1))

    sum_sq = np.zeros((nx, ny))
    n_analysis = 0

    snapshots: list[np.ndarray] = []
    next_snapshot = 0
    n_snapshots = 0 if snapshot_times is None else len(snapshot_times)

    for step in range(n_steps + 1):
        t = step * dt

        # Flux form, with no flux through any face touching a structure.
        fx[1:-1, :] = np.where(face_x, (eta[1:, :] - eta[:-1, :]) / dx, 0.0)
        fy[:, 1:-1] = np.where(face_y, (eta[:, 1:] - eta[:, :-1]) / dx, 0.0)
        lap = (fx[1:, :] - fx[:-1, :]) / dx + (fy[:, 1:] - fy[:, :-1]) / dx

        ramp = min(1.0, t / (ramp_periods * wave.period))
        drive = (
            source_scale
            * ramp
            * np.sin(wave.omega * t - source_phase)
            * source_profile
        )

        eta_next = (
            2.0 * eta
            - eta_prev
            + dt * dt * (c2 * lap + drive)
            - 2.0 * dt * damping * (eta - eta_prev)
        )
        eta_next[land] = 0.0

        eta_prev, eta = eta, eta_next

        if t >= analysis_start:
            sum_sq += eta * eta
            n_analysis += 1

        while next_snapshot < n_snapshots and t >= snapshot_times[next_snapshot]:
            snapshots.append(eta.copy())
            next_snapshot += 1

    while len(snapshots) < n_snapshots:
        snapshots.append(eta.copy())

    # Monochromatic wave: H = 2a and std = a/sqrt(2), so H = 2 sqrt(2) rms.
    rms = np.sqrt(sum_sq / max(n_analysis, 1))
    return 2.0 * math.sqrt(2.0) * rms, snapshots


def simulate_port(
    layout: PortLayout,
    wave: IncidentWave,
    duration: float | None = None,
    cfl: float = 0.35,
    sponge_thickness: float | None = None,
    sponge_strength: float = 2.0,
    sponge_sides: tuple[str, ...] = VALID_SIDES,
    source_x: float | None = None,
    ramp_periods: float = 3.0,
    analysis_periods: float = 6.0,
    n_snapshots: int = 120,
    store_from: float | None = None,
    reference_point: tuple[float, float] | None = None,
) -> PortResult:
    """Propagate a phase-resolved wave field into the harbour.

    Parameters
    ----------
    layout, wave
        Harbour geometry and incident wave.
    duration : float, optional
        Simulated time [s]. Defaults to enough for the wave to cross the
        domain twice plus the ramp and analysis windows.
    cfl : float
        Courant number for the explicit leapfrog step.
    sponge_thickness : float, optional
        Width of the absorbing margin [m]. Defaults to 1.5 wavelengths.
    sponge_strength : float
        Peak damping rate in the sponge [1/s].
    sponge_sides : tuple of str
        Which domain edges absorb. Drop a side to make it reflect, for
        instance the landward edge behind a harbour basin.
    source_x : float, optional
        x position of the wave-maker line [m]. Defaults to just inside the
        west sponge.
    ramp_periods : float
        Number of periods over which the source amplitude ramps up, to avoid
        a start-up shock.
    analysis_periods : float
        Length of the window at the end of the run used to measure wave
        height, in wave periods.
    n_snapshots : int
        Number of stored surface snapshots, spread over the stored window.
    store_from : float, optional
        Time from which to start storing snapshots [s]. Defaults to the
        beginning of the analysis window, so the movie shows the developed
        field. Pass 0.0 to record the whole run including start-up.
    reference_point : (float, float), optional
        Probe used to define the incident height. Defaults to a point in
        open water upwave of the harbour entrance.

    Returns
    -------
    PortResult
    """
    nx, ny = layout.shape
    dx = layout.dx
    land = layout.land_mask()

    c = wave.celerity(layout.depth)
    wavelength = wave.wavelength(layout.depth)

    dt = cfl * dx / (c * math.sqrt(2.0))

    if sponge_thickness is None:
        sponge_thickness = 1.5 * wavelength
    if source_x is None:
        source_x = sponge_thickness + 0.5 * wavelength
    if duration is None:
        crossing = layout.Lx / c
        duration = 2.0 * crossing + (ramp_periods + analysis_periods) * wave.period

    analysis_window = analysis_periods * wave.period
    if store_from is None:
        store_from = max(0.0, duration - analysis_window)

    # Celerity squared, zeroed inside structures so no energy enters them.
    c2 = np.full((nx, ny), c * c)
    damping = _sponge_profile(
        (nx, ny), dx, sponge_thickness, sponge_strength, sponge_sides
    )

    # Partially absorbing structures get a damping collar in the water just
    # outside their footprint, so they reflect less than a bare wall.
    collar = 0.25 * wavelength
    for bw in layout.breakwaters:
        if bw.absorption <= 0.0:
            continue
        clearance = bw.distance_field(*layout.meshgrid()) - 0.5 * bw.width
        profile = np.clip((collar - clearance) / collar, 0.0, 1.0) ** 2
        damping = np.maximum(damping, bw.absorption * sponge_strength * profile)

    # Soft source: a narrow Gaussian strip in x, phased along y so the wave
    # leaves at the requested angle. Being additive, it lets reflected waves
    # pass back through into the west sponge instead of trapping them.
    x, y = layout.coordinates()
    X, Y = layout.meshgrid()
    source_profile = np.exp(-(((X - source_x) / (0.25 * wavelength)) ** 2))
    ky = wave.omega / c * math.sin(wave.direction)
    source_phase = ky * Y

    if reference_point is None:
        reference_point = (source_x + 1.5 * wavelength, 0.5 * layout.Ly)

    common = dict(
        layout=layout,
        wave=wave,
        dt=dt,
        c2=c2,
        damping=damping,
        source_profile=source_profile,
        source_phase=source_phase,
        ramp_periods=ramp_periods,
        analysis_window=analysis_window,
    )

    i_ref = int(np.argmin(np.abs(x - reference_point[0])))
    j_ref = int(np.argmin(np.abs(y - reference_point[1])))

    # The source strength that produces a given wave height cannot be written
    # down cleanly for a finite-width soft source, so calibrate it: run the
    # same discretisation on an empty domain and measure what one unit of
    # forcing delivers at the probe. The model is linear, so a single scaling
    # then puts the incident height exactly on target. Doing this without the
    # structures also keeps reflected energy out of the reference height.
    pilot_duration = (
        (reference_point[0] - source_x) / c
        + (ramp_periods + analysis_periods) * wave.period
    )
    pilot_height, _ = _step_field(
        np.zeros((nx, ny), dtype=bool),
        duration=pilot_duration,
        source_scale=1.0,
        snapshot_times=None,
        **common,
    )
    unit_response = float(pilot_height[i_ref, j_ref])
    if unit_response <= 0:
        raise RuntimeError(
            "Calibration probe recorded no wave energy; check reference_point."
        )
    source_scale = wave.height / unit_response

    snapshot_times = np.linspace(store_from, duration, n_snapshots)
    wave_height, snapshots = _step_field(
        land,
        duration=duration,
        source_scale=source_scale,
        snapshot_times=snapshot_times,
        **common,
    )

    reference_height = wave.height

    return PortResult(
        x=x,
        y=y,
        times=snapshot_times,
        snapshots=np.array(snapshots),
        land=land,
        wave_height=wave_height,
        reference_height=reference_height,
        layout=layout,
        wave=wave,
    )


def measure_reflection(
    absorption: float,
    period: float = 8.0,
    depth: float = 10.0,
    dx: float = 5.0,
    sponge_strength: float = 2.0,
) -> float:
    """Reflection coefficient achieved by a given ``absorption`` setting.

    Fires a normally incident wave at a full-width wall and infers Kr from
    the standing-wave ratio in front of it,

        Kr = (Hmax - Hmin) / (Hmax + Hmin)

    which is the usual laboratory estimate. Useful for picking an
    ``absorption`` value that matches a measured or specified Kr.
    """
    Lx, Ly = 1400.0, 200.0
    wall_x = 1100.0
    wall = Breakwater(
        points=[(wall_x, -50.0), (wall_x, Ly + 50.0)],
        width=40.0,
        absorption=absorption,
        name="test wall",
    )
    layout = PortLayout(Lx=Lx, Ly=Ly, dx=dx, depth=depth, breakwaters=[wall])
    wave = IncidentWave(height=1.0, period=period)

    crossing = Lx / wave.celerity(depth)
    result = simulate_port(
        layout,
        wave,
        duration=6.0 * crossing,
        n_snapshots=2,
        analysis_periods=16.0,
        sponge_sides=("west",),
        sponge_strength=sponge_strength,
    )

    # Sample the standing-wave envelope over one wavelength in front of the
    # wall, clear of both the sponge and the absorbing collar.
    wavelength = wave.wavelength(depth)
    j = result.wave_height.shape[1] // 2
    x0, x1 = wall_x - 2.0 * wavelength, wall_x - 0.75 * wavelength
    band = (result.x >= x0) & (result.x <= x1)
    envelope = result.wave_height[band, j]

    hmax, hmin = float(envelope.max()), float(envelope.min())
    if hmax + hmin <= 0:
        return 0.0
    return (hmax - hmin) / (hmax + hmin)
