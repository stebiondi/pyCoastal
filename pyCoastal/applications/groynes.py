"""
Groynes and detached breakwaters: structures that reshape a sandy shoreline.

A nourishment adds sand. These two add a *constraint*, and the shoreline
rearranges itself around it. The design question is not "will it stand up"
(that is :mod:`pyCoastal.applications.structures`) but "what shape will the
beach take, and who pays for it downdrift".

Two families, two quite different states of knowledge:

**Groynes** are shore-normal barriers to alongshore transport. The
linearized one-line equation has an exact solution for a complete barrier
(Pelnard-Considere 1956), so the updrift fillet, the impounded volume, the
time to bypassing and the mirrored downdrift erosion are all analytical.
That solution is the backbone of this half of the module and it is
genuinely predictive, within its assumptions.

**Detached breakwaters** sit shore-parallel and work by sheltering, not
blocking. There is no comparable closed-form answer. What there is, is
sixty years of laboratory and field observation compressed into
classification rules on the ratio of breakwater length to distance
offshore, and those rules disagree with each other. This module reports
:func:`shoreline_response` from three published sets side by side rather
than averaging them into a single number that would look more certain than
it is.

What this module is not
-----------------------
The analytical solutions assume small wave angles, one representative wave
condition, a complete barrier, and a shoreline free to move without running
into anything. Real groyne fields bypass, leak, and sit on beaches with a
seawall behind them. ``pyCoastal.tools.shoreline`` has the numerical
one-line model for when those assumptions fail; this module is the design
layer that tells you roughly what to expect, and what to ask the model.

References
----------
Pelnard-Considere, R. (1956). Essai de theorie de l'evolution des formes de
rivage en plages de sable et de galets. Quatriemes Journees de
l'Hydraulique, Paris.

Larson, M., Hanson, H. and Kraus, N.C. (1987). Analytical solutions of the
one-line model of shoreline change. Technical Report CERC-87-15, USACE.

d'Angremond, K., van der Meer, J.W. and de Jong, R.J. (1996). Wave
transmission at low-crested structures. Proc. 25th Int. Conf. Coastal
Engineering, ASCE, 2418-2427.

Shore Protection Manual (1984). 4th ed. USACE Coastal Engineering Research
Center.

Dally, W.R. and Pope, J. (1986). Detached breakwaters for shore protection.
Technical Report CERC-86-1, USACE.

Suh, K. and Dalrymple, R.A. (1987). Offshore breakwaters in laboratory and
field. Journal of Waterway, Port, Coastal and Ocean Engineering, 113(2),
105-121.

Hsu, J.R.C. and Evans, C. (1989). Parabolic bay shapes and applications.
Proc. Institution of Civil Engineers, 87(4), 557-570.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np

from .nourishment import SECONDS_PER_YEAR, WaveClimate, longshore_diffusivity
from .sediment import sediment

__all__ = [
    "LittoralCell",
    "ierfc",
    "Groyne",
    "groyne_planform",
    "groyne_impoundment",
    "bypassing_time",
    "fillet_geometry",
    "bay_planform",
    "GroyneFieldDesign",
    "design_groyne_field",
    "wave_transmission",
    "DetachedBreakwater",
    "RESPONSE_CRITERIA",
    "shoreline_response",
    "parabolic_bay",
    "segment_layout",
    "DetachedSchemeDesign",
    "design_detached_scheme",
]


# ---------------------------------------------------------------------------
# The coast the structure sits on
# ---------------------------------------------------------------------------


@dataclass
class LittoralCell:
    """The stretch of sandy coast a structure is placed on.

    Everything alongshore scales with the height of the active profile,
    ``D + B``: sand moved alongshore has to fill that whole height before
    the shoreline moves at all. A deep closure depth makes every structure
    slower to fill and every erosion problem slower to appear, which is why
    it belongs here rather than being buried in a function signature.

    Attributes
    ----------
    D : float
        Depth of closure [m], the offshore limit of the active profile.
    B : float
        Berm height above mean water [m].
    bed : str
        Sediment key, for scour at the structure and for reporting. The
        porosity is taken from it unless ``porosity`` is given explicitly.
    porosity : float, optional
        Sediment porosity [-]. Defaults to the bed material's own value.
    """

    D: float = 6.0
    B: float = 2.0
    bed: str = "medium_sand"
    porosity: float | None = None

    def __post_init__(self) -> None:
        if self.D <= 0:
            raise ValueError(f"Depth of closure must be positive, got {self.D}")
        if self.B <= 0:
            raise ValueError(f"Berm height must be positive, got {self.B}")
        material = sediment(self.bed)
        if material.d50 <= 0:
            raise ValueError(
                f"{material.name} is cohesive; these are sandy-coast models. "
                "Pick a sand or gravel."
            )
        if self.porosity is None:
            self.porosity = material.porosity
        if not 0 <= self.porosity < 1:
            raise ValueError(f"Porosity must be in [0,1), got {self.porosity}")

    @property
    def active_height(self) -> float:
        """Vertical extent of the active profile, D + B [m]."""
        return self.D + self.B

    @property
    def material(self):
        """The bed sediment."""
        return sediment(self.bed)

    def diffusivity(self, climate: WaveClimate) -> float:
        """Alongshore diffusivity [m^2/s] for this cell and wave climate.

        The same group as in :mod:`pyCoastal.applications.nourishment`; a
        cell and a fill both present ``porosity`` and ``active_height``.
        """
        return longshore_diffusivity(climate, self)


# ---------------------------------------------------------------------------
# Groynes
# ---------------------------------------------------------------------------


def ierfc(u):
    """Integral of the complementary error function.

        ierfc(u) = exp(-u^2)/sqrt(pi) - u erfc(u)

    This is the shape of the fillet that builds against a groyne, and
    ``ierfc(0) = 1/sqrt(pi)`` is what sets the shoreline advance right at
    the structure. Accepts a scalar or an array.
    """
    u = np.asarray(u, dtype=float)
    out = np.exp(-u * u) / math.sqrt(math.pi) - u * _erfc(u)
    return out if out.ndim else float(out)


_erfc = np.vectorize(math.erfc)


@dataclass
class Groyne:
    """A single shore-normal barrier.

    Attributes
    ----------
    length : float
        Length seaward of the *original* shoreline [m]. This is the length
        that matters: a groyne's buried root does nothing for the fillet.
    permeability : float
        Fraction of the approaching transport that passes the structure
        [-]. 0.0 is the complete barrier the analytical solution assumes;
        a rock groyne is typically 0.1 to 0.3, a timber one higher still.
    """

    length: float = 50.0
    permeability: float = 0.0

    def __post_init__(self) -> None:
        if self.length <= 0:
            raise ValueError(f"Groyne length must be positive, got {self.length}")
        if not 0.0 <= self.permeability < 1.0:
            raise ValueError(
                f"Permeability must be in [0,1), got {self.permeability}"
            )


def groyne_planform(x, t: float, groyne: Groyne, cell: LittoralCell,
                    climate: WaveClimate):
    """Shoreline offset around a groyne after time ``t`` [m].

    The Pelnard-Considere solution for a complete littoral barrier at
    ``x = 0``, with transport running in the positive x direction:

        y(x,t) = 2 m sqrt(eps t) ierfc( |x| / (2 sqrt(eps t)) )

    accreting updrift (x < 0) and the mirror image eroding downdrift
    (x > 0), where ``m = tan(alpha_b)`` is the breaking wave angle to the
    original shoreline.

    The downdrift limb is the part people forget to draw. It is the same
    size as the fillet, it appears at the same rate, and it is the reason
    groynes generate litigation.

    Parameters
    ----------
    x : array_like
        Alongshore coordinate [m], zero at the groyne, positive downdrift.
    t : float
        Time since construction [s].

    Returns
    -------
    ndarray
        Shoreline offset [m]: positive seaward, negative eroded.

    Notes
    -----
    Valid only while the groyne still blocks everything, that is until
    :func:`bypassing_time`. After that the fillet stops growing and the
    solution overstates it without bound. A partly permeable groyne is
    handled by scaling the trapped fraction, which is a crude but standard
    first pass; it does not change the shape of the fillet, only its size.
    """
    x = np.asarray(x, dtype=float)
    if t < 0:
        raise ValueError(f"Time cannot be negative, got {t}")

    m = math.tan(climate.alpha0)
    if t == 0 or m == 0:
        return np.zeros_like(x)

    trapped = 1.0 - groyne.permeability
    eps = cell.diffusivity(climate)
    spread = math.sqrt(eps * t)

    y = 2.0 * m * trapped * spread * ierfc(np.abs(x) / (2.0 * spread))
    return np.where(x < 0.0, y, -y)


def groyne_impoundment(t: float, groyne: Groyne, cell: LittoralCell,
                       climate: WaveClimate) -> float:
    """Sand volume trapped updrift of a groyne after time ``t`` [m^3].

    Integrating the fillet over the active profile height gives, exactly,

        V(t) = (1 - r) tan(alpha_b) eps (D + B) t

    which is just the alongshore transport rate times the elapsed time, as
    it has to be while the barrier is complete. The check is worth having:
    it is the one place the diffusivity, the wave angle and the profile
    height must combine consistently, and an error in any of them shows up
    here as a volume that does not match the transport.
    """
    if t < 0:
        raise ValueError(f"Time cannot be negative, got {t}")
    m = math.tan(climate.alpha0)
    trapped = 1.0 - groyne.permeability
    return (trapped * m * cell.diffusivity(climate)
            * cell.active_height * t)


def bypassing_time(groyne: Groyne, cell: LittoralCell,
                   climate: WaveClimate) -> float:
    """Time for the fillet to reach the groyne tip and start bypassing [s].

    Setting ``y(0,t) = L`` in the analytical solution, with
    ``y(0,t) = 2 m sqrt(eps t / pi)``:

        t_bypass = pi L^2 / (4 m^2 eps)

    The design significance is blunt. Before this time the groyne is
    trapping everything and starving the coast downdrift. After it, the
    groyne has filled, transport resumes, and the downdrift erosion stops
    growing. A groyne field that never reaches this state never stops
    causing damage, which is the argument for filling one artificially at
    construction.

    Returns ``inf`` for shore-normal waves, which drive no transport and so
    never fill anything.
    """
    m = math.tan(climate.alpha0)
    trapped = 1.0 - groyne.permeability
    if m == 0 or trapped == 0:
        return math.inf
    eps = cell.diffusivity(climate)
    return math.pi * groyne.length**2 / (4.0 * (m * trapped) ** 2 * eps)


def fillet_geometry(groyne: Groyne, cell: LittoralCell,
                    climate: WaveClimate, t: float) -> dict:
    """The fillet at one moment: advance, reach, volume and how full it is.

    ``reach`` is where the fillet has decayed to a tenth of its height at
    the groyne, which is a workable definition of how far updrift the
    structure is felt. It is ``2.30 sqrt(eps t)``, from solving
    ``ierfc(u) = 0.1 ierfc(0)``.
    """
    if t < 0:
        raise ValueError(f"Time cannot be negative, got {t}")

    m = math.tan(climate.alpha0)
    trapped = 1.0 - groyne.permeability
    eps = cell.diffusivity(climate)
    spread = math.sqrt(eps * t)
    advance = 2.0 * m * trapped * spread / math.sqrt(math.pi)
    full = bypassing_time(groyne, cell, climate)

    # Sand held when the fillet first touches the tip. Substituting the
    # bypassing time into the impoundment gives a closed form that loses
    # the diffusivity entirely:
    #
    #     V_full = pi L^2 (D + B) / (4 m)
    #
    # so a gently oblique wave climate impounds *more* sand before it
    # bypasses, not less. The fillet is long and shallow and has to fill a
    # much greater length of coast before it stands as high as the groyne.
    capacity = (math.pi * groyne.length**2 * cell.active_height
                / (4.0 * m * trapped)) if m * trapped > 0 else math.inf

    bypassing = advance >= groyne.length
    note = ""
    if bypassing:
        note = (
            f"Past bypassing. The unconstrained solution gives a "
            f"{advance:.0f} m fillet against a {groyne.length:.0f} m groyne, "
            f"which cannot happen: from {full / SECONDS_PER_YEAR:.2f} years "
            "the groyne is full, sand passes the tip and the fillet stops "
            "growing. Read the advance as the groyne length and the volume "
            "as the capacity.")

    return {
        "advance": advance,
        "reach": _DECAY_TENTH * spread,
        "volume": groyne_impoundment(t, groyne, cell, climate),
        "capacity": capacity,
        "bypassing_time": full,
        "filled_fraction": min(advance / groyne.length, 1.0),
        "bypassing": bypassing,
        "valid": not bypassing,
        "note": note,
        "diffusivity": eps,
        "transport_rate": trapped * m * eps * cell.active_height,
    }


#: u at which ierfc(u) falls to a tenth of ierfc(0). Solved rather than
#: recalled: the value is not a round number and a wrong one would quietly
#: misreport how far updrift a groyne is felt.
_DECAY_TENTH = 0.9626934117142310


def bay_planform(xi, t: float, spacing: float, cell: LittoralCell,
                 climate: WaveClimate, terms: int = 401):
    """Shoreline in one closed groyne bay, measured from its updrift end.

    While both groynes block completely the bay is sealed: no sand enters
    and none leaves. The shoreline tilts at constant volume towards the
    equilibrium at which the waves arrive parallel to it everywhere,

        y_eq(x) = tan(alpha_b) (x - S/2)

    accreting against the downdrift groyne and eroding away from the
    updrift one. Substituting ``w = y - y_eq`` turns the zero-flux
    condition into a homogeneous Neumann problem, whose solution is

        w = sum_{n odd} (4 tan(a) S / (n pi)^2)
                        cos(n pi x / S) exp(-eps n^2 pi^2 t / S^2)

    The series conserves volume exactly, term by term, because every
    cosine integrates to zero over the cell. That is the property worth
    knowing: sand only moves *within* a sealed bay, so anything the model
    gains at one end it must lose at the other.

    Parameters
    ----------
    xi : array_like
        Distance from the updrift groyne [m], in ``[0, spacing]``.
    terms : int
        Fourier terms to sum. The series converges slowly near ``t = 0``,
        where it has to reproduce a straight line; 401 holds the initial
        condition to about 5 mm in a 150 m bay.
    """
    xi = np.asarray(xi, dtype=float)
    if t < 0:
        raise ValueError(f"Time cannot be negative, got {t}")
    if spacing <= 0:
        raise ValueError(f"Spacing must be positive, got {spacing}")

    m = math.tan(climate.alpha0)
    if t == 0 or m == 0:
        return np.zeros_like(xi)

    eps = cell.diffusivity(climate)
    w = np.zeros_like(xi)
    for n in range(1, terms, 2):
        decay = math.exp(-eps * (n * math.pi) ** 2 * t / spacing**2)
        if decay < 1e-12:
            break
        w += (4.0 * m * spacing / (n * math.pi) ** 2
              * np.cos(n * math.pi * xi / spacing) * decay)
    return m * (xi - 0.5 * spacing) + w


def design_groyne_field(cell: LittoralCell, climate: WaveClimate,
                        length: float, spacing: float, count: int = 5,
                        permeability: float = 0.0,
                        horizon: float = 5.0 * SECONDS_PER_YEAR,
                        prefill: bool = False) -> "GroyneFieldDesign":
    """Lay out a groyne field and say what it will do to the coast.

    Three things decide whether a field works, and all three are geometry
    rather than structural design:

    1. **Spacing to length.** Conventional guidance is 1.5 to 3 groyne
       lengths. Too close and the field is expensive for no extra benefit;
       too far and the bay between groynes erodes back to the backshore.
    2. **The fillet fits.** The shoreline between two groynes rotates
       towards the wave crests, so the downdrift corner of each bay retreats
       by about ``spacing * tan(alpha_b)``. If that exceeds the groyne
       length, the bay cuts back past the root and the structure is
       outflanked.
    3. **What happens downdrift.** The field traps sand until it fills.
       Everything it traps is sand the coast downdrift does not receive.

    Parameters
    ----------
    prefill : bool
        Whether the field is filled with imported sand at construction.
        This is the difference between a scheme that takes the sand from
        the neighbours and one that does not, and it is usually the whole
        argument at the planning inquiry.

    Returns
    -------
    GroyneFieldDesign
    """
    if count < 1:
        raise ValueError(f"A field needs at least one groyne, got {count}")
    if spacing <= 0:
        raise ValueError(f"Spacing must be positive, got {spacing}")
    if horizon < 0:
        raise ValueError(f"Horizon cannot be negative, got {horizon}")

    groyne = Groyne(length=length, permeability=permeability)
    m = math.tan(climate.alpha0)

    ratio = spacing / length
    fillet_drop = spacing * abs(m)
    state = fillet_geometry(groyne, cell, climate, horizon)

    # The field as a whole traps like one long barrier: the updrift groyne
    # fills first, then the next, so the volume to fill the whole field is
    # the sum of the bays.
    bay_volume = 0.5 * spacing * length * cell.active_height
    field_capacity = bay_volume * max(count - 1, 1)
    rate = state["transport_rate"]
    fill_time = field_capacity / rate if rate > 0 else math.inf

    deficit = 0.0 if prefill else min(
        groyne_impoundment(horizon, groyne, cell, climate), field_capacity)

    notes = []
    if ratio < 1.5:
        notes.append(
            f"Spacing is {ratio:.1f} groyne lengths, closer than the usual "
            "1.5 to 3. The extra groynes buy little; check whether fewer, "
            "longer ones do the same job.")
    elif ratio > 3.0:
        notes.append(
            f"Spacing is {ratio:.1f} groyne lengths, wider than the usual "
            "1.5 to 3. The bays between groynes will behave as open coast "
            "over most of their length.")
    else:
        notes.append(
            f"Spacing is {ratio:.1f} groyne lengths, inside the "
            "conventional 1.5 to 3.")

    if fillet_drop >= length:
        notes.append(
            f"The bay rotates back {fillet_drop:.0f} m across a {spacing:.0f} m "
            f"spacing, which reaches the {length:.0f} m groyne root. The "
            "field will be outflanked at the downdrift corner of each bay. "
            "Shorten the spacing or lengthen the groynes.")
    else:
        notes.append(
            f"The bay rotates back {fillet_drop:.0f} m, against a "
            f"{length:.0f} m groyne. The downdrift corner of each bay holds.")

    if prefill:
        notes.append(
            f"Prefilled with {field_capacity / 1e3:.0f} thousand m3, so the "
            "field starts full and takes nothing from downdrift.")
    else:
        notes.append(
            f"Not prefilled. The field will take about "
            f"{deficit / 1e3:.0f} thousand m3 out of the littoral drift over "
            f"{horizon / SECONDS_PER_YEAR:.3g} years, and that sand comes "
            "off the coast downdrift.")

    return GroyneFieldDesign(
        cell=cell, climate=climate, groyne=groyne, spacing=spacing,
        count=count, horizon=horizon, prefill=prefill,
        spacing_ratio=ratio, fillet_drop=fillet_drop,
        field_capacity=field_capacity, fill_time=fill_time,
        downdrift_deficit=deficit, state=state, notes=notes,
    )


@dataclass
class GroyneFieldDesign:
    """The outcome of :func:`design_groyne_field`."""

    cell: LittoralCell
    climate: WaveClimate
    groyne: Groyne
    spacing: float
    count: int
    horizon: float
    prefill: bool
    spacing_ratio: float
    fillet_drop: float
    field_capacity: float
    fill_time: float
    downdrift_deficit: float
    state: dict
    notes: list[str] = field(default_factory=list)

    @property
    def field_length(self) -> float:
        """Alongshore length of the whole field [m]."""
        return self.spacing * (self.count - 1)

    @property
    def outflanked(self) -> bool:
        """Whether the bay rotation reaches the groyne root."""
        return self.fillet_drop >= self.groyne.length

    @property
    def positions(self) -> np.ndarray:
        """Alongshore position of each groyne [m], centred on zero."""
        first = -0.5 * self.field_length
        return first + self.spacing * np.arange(self.count)

    @property
    def relaxation_time(self) -> float:
        """Time constant for a bay to reach its equilibrium tilt [s].

        The slowest Fourier mode of the closed cell decays as
        ``exp(-eps pi^2 t / S^2)``, so ``tau = S^2 / (eps pi^2)``. Bays are
        short, so this is usually days to weeks: groyne compartments fill
        far faster than the field as a whole takes to bypass.
        """
        eps = self.cell.diffusivity(self.climate)
        return self.spacing**2 / (eps * math.pi**2)

    def planform(self, x, t: float | None = None, terms: int = 401):
        """Shoreline offset along the field [m].

        Three regions, each with its own exact solution:

        - **Updrift of the first groyne**, the single-barrier fillet of
          :func:`groyne_planform`. The full drift arrives here and is
          stopped, so the lone-groyne solution applies unchanged.
        - **Each bay between two groynes** is a *closed cell*: the updrift
          groyne lets nothing in and the downdrift groyne lets nothing
          out. The shoreline tilts, at constant volume, towards a sawtooth
          of slope ``tan(alpha_b)`` pivoting about the bay centre. See
          :func:`bay_planform`.
        - **Downdrift of the last groyne**, the mirrored erosion.

        Superposing single-groyne solutions instead, which is the tempting
        shortcut, is wrong: a groyne is a zero-flux *boundary condition*,
        not a source term, and a sum of single-barrier solutions satisfies
        zero flux at none of them. It produces accretion and erosion that
        grow without bound along the field.
        """
        t = self.horizon if t is None else t
        if t < 0:
            raise ValueError(f"Time cannot be negative, got {t}")

        x = np.asarray(x, dtype=float)
        out = np.zeros_like(x)
        groynes = self.positions
        first, last = groynes[0], groynes[-1]

        updrift = x < first
        if updrift.any():
            out[updrift] = groyne_planform(x[updrift] - first, t, self.groyne,
                                           self.cell, self.climate)

        downdrift = x > last
        if downdrift.any():
            out[downdrift] = groyne_planform(x[downdrift] - last, t,
                                             self.groyne, self.cell,
                                             self.climate)

        for i in range(self.count - 1):
            a, b = groynes[i], groynes[i + 1]
            inside = (x > a) & (x < b)
            if inside.any():
                out[inside] = bay_planform(x[inside] - a, t, self.spacing,
                                           self.cell, self.climate,
                                           terms=terms)

        # The shoreline is double-valued at a groyne: sand stands against
        # the updrift face and is scoured from the downdrift one, so the
        # beach steps across the structure. Points landing exactly on a
        # groyne take the updrift, accreted side, which is the beach a
        # surveyor would record there. Without a rule the bays overlap at
        # their shared endpoints and the later one silently wins, flipping
        # the sign at every interior groyne.
        for i, position in enumerate(groynes):
            on = x == position
            if not on.any():
                continue
            if i == 0:
                out[on] = groyne_planform(np.zeros(int(on.sum())) - 1e-12, t,
                                          self.groyne, self.cell, self.climate)
            else:
                out[on] = bay_planform(np.full(int(on.sum()), self.spacing), t,
                                       self.spacing, self.cell, self.climate,
                                       terms=terms)
        return out


# ---------------------------------------------------------------------------
# Detached breakwaters
# ---------------------------------------------------------------------------


def wave_transmission(Hs: float, freeboard: float, crest_width: float,
                      Dn50: float, cot_alpha: float = 2.0,
                      steepness: float | None = None,
                      period: float | None = None) -> dict:
    """Wave transmission past a low-crested rubble mound.

    d'Angremond, van der Meer and de Jong (1996):

        Kt = -0.4 Rc/Hs + 0.64 (B/Hs)^-0.31 (1 - exp(-0.5 xi))

    bounded to 0.075 <= Kt <= 0.8. ``Rc`` is the crest freeboard, negative
    when the crest is submerged.

    This matters for a detached breakwater in a way it does not for a
    harbour arm. The classification rules in :func:`shoreline_response`
    were built on emergent structures that block nearly everything. A
    submerged sill passing half the wave energy will not build the salient
    those rules promise, and reading the ratio without reading the
    transmission is the standard way to be disappointed by a reef scheme.

    Parameters
    ----------
    freeboard : float
        Crest level minus water level [m]. Negative if submerged.
    steepness : float, optional
        Wave steepness for the surf similarity parameter. Given a
        ``period`` instead, it is computed from deep-water theory.
    """
    if Hs <= 0:
        raise ValueError(f"Wave height must be positive, got {Hs}")
    if crest_width <= 0:
        raise ValueError(f"Crest width must be positive, got {crest_width}")
    if Dn50 <= 0:
        raise ValueError(f"Dn50 must be positive, got {Dn50}")

    if steepness is None:
        if period is None:
            raise ValueError("Give either a wave steepness or a period")
        steepness = 2.0 * math.pi * Hs / (9.81 * period**2)
    if steepness <= 0:
        raise ValueError(f"Steepness must be positive, got {steepness}")

    xi = (1.0 / cot_alpha) / math.sqrt(steepness)
    raw = (-0.4 * freeboard / Hs
           + 0.64 * (crest_width / Hs) ** -0.31 * (1.0 - math.exp(-0.5 * xi)))
    Kt = min(0.8, max(0.075, raw))

    ratio = crest_width / Hs
    return {
        "Kt": Kt,
        "unbounded": raw,
        "clipped": raw != Kt,
        "surf_similarity": xi,
        "relative_freeboard": freeboard / Hs,
        "relative_crest_width": ratio,
        "energy_transmitted": Kt**2,
        "in_range": 0.5 <= ratio <= 4.0 and abs(freeboard / Hs) <= 2.5,
    }


@dataclass
class DetachedBreakwater:
    """One shore-parallel breakwater, or one segment of a chain.

    Attributes
    ----------
    length : float
        Alongshore length of the structure [m], ``Ls``.
    offshore : float
        Distance from the original shoreline to the structure [m], ``X``.
    gap : float
        Gap to the next segment [m]. Zero for a single breakwater.
    crest_level : float
        Crest level relative to the design water level [m]. Negative for a
        submerged sill.
    """

    length: float = 150.0
    offshore: float = 100.0
    gap: float = 0.0
    crest_level: float = 1.5

    def __post_init__(self) -> None:
        if self.length <= 0:
            raise ValueError(f"Breakwater length must be positive, got {self.length}")
        if self.offshore <= 0:
            raise ValueError(f"Distance offshore must be positive, got {self.offshore}")
        if self.gap < 0:
            raise ValueError(f"Gap cannot be negative, got {self.gap}")

    @property
    def ratio(self) -> float:
        """``Ls / X``, the ratio every classification rule is built on."""
        return self.length / self.offshore


#: Published classification rules, as ``Ls/X`` thresholds.
#:
#: They disagree, and the disagreement is the honest answer: these are
#: envelopes fitted to scattered laboratory and field data, not physical
#: laws. Reporting all three shows how much of the verdict is the data and
#: how much is whose paper you opened.
RESPONSE_CRITERIA = {
    "spm_1984": {
        "source": "Shore Protection Manual (1984)",
        "tombolo": 2.0,
        "periodic_tombolo": 1.0,
        "salient": 0.5,
    },
    "dally_pope_1986": {
        "source": "Dally and Pope (1986)",
        "tombolo": 1.5,
        "periodic_tombolo": 1.0,
        "salient": 0.5,
    },
    "suh_dalrymple_1987": {
        "source": "Suh and Dalrymple (1987)",
        "tombolo": 1.0,
        "periodic_tombolo": 0.8,
        "salient": 0.5,
    },
}


def shoreline_response(breakwater: DetachedBreakwater,
                       criterion: str | None = None) -> dict:
    """What shape the beach will take behind a detached breakwater.

    The response is governed by ``Ls / X``: a structure that is long
    compared with its distance offshore shelters enough of the beach for
    sand to build all the way out to it (a tombolo); one that is short
    relative to its distance only bulges the shoreline (a salient).

    With no ``criterion`` given, all of :data:`RESPONSE_CRITERIA` are
    evaluated and the result carries every verdict plus whether they agree.
    A unanimous verdict is worth acting on; a split one means the layout
    sits on a threshold and deserves a model.

    For segmented schemes Suh and Dalrymple's gap criterion also applies:
    a tombolo needs ``G X / Ls^2 < 0.5``, so a wide gap behind a short
    segment lets enough wave energy through to stop one forming.

    Returns
    -------
    dict
        ``ratio``, per-criterion ``verdicts``, the ``consensus`` verdict or
        None if they disagree, and a plain-language ``note``.
    """
    ratio = breakwater.ratio
    keys = [criterion] if criterion else list(RESPONSE_CRITERIA)
    for key in keys:
        if key not in RESPONSE_CRITERIA:
            raise ValueError(
                f"Unknown criterion {key!r}. Options: {sorted(RESPONSE_CRITERIA)}"
            )

    verdicts = {}
    for key in keys:
        rule = RESPONSE_CRITERIA[key]
        if ratio >= rule["tombolo"]:
            verdicts[key] = "tombolo"
        elif ratio >= rule["periodic_tombolo"]:
            verdicts[key] = "periodic tombolo"
        elif ratio >= rule["salient"]:
            verdicts[key] = "salient"
        else:
            verdicts[key] = "no sinuosity"

    distinct = set(verdicts.values())
    consensus = distinct.pop() if len(distinct) == 1 else None

    gap_index = None
    gap_tombolo = None
    if breakwater.gap > 0:
        gap_index = (breakwater.gap * breakwater.offshore
                     / breakwater.length**2)
        gap_tombolo = gap_index < 0.5

    if consensus:
        note = (f"Ls/X = {ratio:.2f}. All three criteria give a "
                f"{consensus}.")
    else:
        spread = ", ".join(
            f"{RESPONSE_CRITERIA[k]['source'].split('(')[0].strip()} says "
            f"{v}" for k, v in verdicts.items())
        note = (f"Ls/X = {ratio:.2f} sits on a threshold: {spread}. "
                "The layout is not decisively one thing or the other; model "
                "it before committing.")
    if gap_index is not None:
        note += (f" Gap index G X / Ls^2 = {gap_index:.2f}, "
                 + ("below 0.5, so the gaps are narrow enough for a tombolo "
                    "to form." if gap_tombolo else
                    "above 0.5, so the gaps pass enough energy to prevent a "
                    "tombolo whatever Ls/X says."))

    return {
        "ratio": ratio,
        "verdicts": verdicts,
        "consensus": consensus,
        "unanimous": consensus is not None,
        "gap_index": gap_index,
        "gap_allows_tombolo": gap_tombolo,
        "note": note,
    }


# Hsu and Evans (1989) fitted coefficients, with beta in degrees. They are
# least-squares fits, so C0 + C1 + C2 comes to 1 only to about half a
# percent; the test suite checks that, since a typo in any digit breaks it
# by far more.
_BAY_C0 = (0.0707, -0.0047, 0.000349, -0.00000875, 0.00000004765)
_BAY_C1 = (0.9536, 0.0078, -0.0004879, 0.0000182, -0.0000001281)
_BAY_C2 = (0.0214, -0.0078, 0.0003004, -0.00001183, 0.00000009343)


def _poly(coefficients, beta: float) -> float:
    return sum(c * beta**i for i, c in enumerate(coefficients))


def parabolic_bay(beta_degrees: float, R0: float, theta_degrees):
    """Static equilibrium bay shape, Hsu and Evans (1989).

    A beach held between two control points settles into a shape where the
    breaking wave crests arrive parallel to the shoreline everywhere, so
    there is no alongshore transport left to move anything. That shape fits

        R / R0 = C0 + C1 (beta/theta) + C2 (beta/theta)^2

    measured from the upcoast diffraction point, where ``beta`` is the
    angle between the incident wave crest and the control line, and
    ``theta`` is the angle to the radius ``R``.

    This is the planform a headland bay, a groyne bay, or the lee of a
    detached breakwater tends towards if it is left alone and sand is not
    in short supply. It is an *equilibrium*, and says nothing about how
    long it takes to get there.

    Parameters
    ----------
    beta_degrees : float
        Wave obliquity at the control point [deg]. Must be positive; the
        fit is quoted for roughly 20 to 80 degrees.
    R0 : float
        Length of the control line [m].
    theta_degrees : array_like
        Angles at which to evaluate the radius [deg], measured from the
        incident wave crest at the diffraction point. ``theta = beta`` is
        the downcoast control point, where ``R = R0``; larger angles are
        closer in under the diffraction point, so ``R`` *shrinks* as
        ``theta`` grows. Values below ``beta`` lie beyond the control
        point, where the beach is straight and the relation no longer
        applies, and come back as NaN.

    Returns
    -------
    ndarray
        Radius R at each angle [m].
    """
    if beta_degrees <= 0:
        raise ValueError(f"Beta must be positive, got {beta_degrees}")
    if R0 <= 0:
        raise ValueError(f"Control line must be positive, got {R0}")

    theta = np.asarray(theta_degrees, dtype=float)
    c0 = _poly(_BAY_C0, beta_degrees)
    c1 = _poly(_BAY_C1, beta_degrees)
    c2 = _poly(_BAY_C2, beta_degrees)

    with np.errstate(divide="ignore", invalid="ignore"):
        frac = beta_degrees / theta
        R = R0 * (c0 + c1 * frac + c2 * frac**2)
    return np.where(theta >= beta_degrees, R, np.nan)


def segment_layout(total_length: float, breakwater: DetachedBreakwater) -> dict:
    """How many segments fit along a frontage, and what they cover.

    A chain of detached breakwaters is described by its segment length and
    gap. The useful derived numbers are the number of segments, the
    fraction of the frontage that is sheltered, and the rock quantity,
    which is what the cost follows.
    """
    if total_length <= 0:
        raise ValueError(f"Frontage must be positive, got {total_length}")

    pitch = breakwater.length + breakwater.gap
    count = max(1, int(round((total_length + breakwater.gap) / pitch)))
    covered = count * breakwater.length
    span = count * pitch - breakwater.gap

    return {
        "count": count,
        "pitch": pitch,
        "covered_length": covered,
        "span": span,
        "sheltered_fraction": covered / span if span > 0 else 0.0,
        "gap_fraction": 1.0 - covered / span if span > 0 else 0.0,
    }


def design_detached_scheme(cell: LittoralCell, climate: WaveClimate,
                           breakwater: DetachedBreakwater,
                           frontage: float,
                           Hs: float | None = None,
                           period: float | None = None,
                           Dn50: float = 1.0,
                           crest_width: float = 4.0,
                           cot_alpha: float = 2.0,
                           criterion: str | None = None
                           ) -> "DetachedSchemeDesign":
    """Lay out a detached breakwater scheme and say what the beach will do.

    Pulls the three strands together: the geometric classification, the
    wave transmission that decides whether the classification is
    believable, and the segment arithmetic that decides what it costs.

    Parameters
    ----------
    Hs, period : float, optional
        Design wave at the structure, for the transmission. Defaults to the
        climate's breaking height and period.
    Dn50, crest_width, cot_alpha : float
        Armour size, crest width and slope of the mound. Size these with
        :func:`pyCoastal.applications.structures.design_rubble_mound`; they
        are inputs here because transmission depends on the section, not the
        other way round.

    Returns
    -------
    DetachedSchemeDesign
    """
    Hs = climate.Hb if Hs is None else Hs
    period = climate.T if period is None else period

    response = shoreline_response(breakwater, criterion)
    layout = segment_layout(frontage, breakwater)
    transmission = wave_transmission(
        Hs, breakwater.crest_level, crest_width, Dn50,
        cot_alpha=cot_alpha, period=period)

    notes = [response["note"]]

    Kt = transmission["Kt"]
    if Kt >= 0.5:
        notes.append(
            f"Transmission Kt = {Kt:.2f}: about half the wave height passes "
            "the structure. The classification above was built on emergent "
            "breakwaters that block nearly everything, so expect a markedly "
            "smaller response than it promises.")
    elif Kt >= 0.3:
        notes.append(
            f"Transmission Kt = {Kt:.2f}: the crest is low enough to pass "
            "useful energy, so treat the predicted response as an upper "
            "bound.")
    else:
        notes.append(
            f"Transmission Kt = {Kt:.2f}: the structure blocks most of the "
            "wave energy, which is the condition the classification rules "
            "were fitted to.")

    if not transmission["in_range"]:
        notes.append(
            "The transmission formula is outside its fitted range here "
            f"(B/Hs = {transmission['relative_crest_width']:.1f}, "
            f"Rc/Hs = {transmission['relative_freeboard']:.1f}); treat Kt as "
            "indicative only.")

    if breakwater.crest_level < 0:
        notes.append(
            "A submerged sill also traps water shoreward of it, and the "
            "return flow through the gaps can drive an offshore current "
            "strong enough to lose sand. That is not in any of these "
            "relations.")

    notes.append(
        f"{layout['count']} segments of {breakwater.length:.0f} m shelter "
        f"{100 * layout['sheltered_fraction']:.0f}% of a "
        f"{layout['span']:.0f} m frontage.")

    return DetachedSchemeDesign(
        cell=cell, climate=climate, breakwater=breakwater,
        frontage=frontage, response=response, layout=layout,
        transmission=transmission, Hs=Hs, period=period,
        Dn50=Dn50, crest_width=crest_width, cot_alpha=cot_alpha,
        notes=notes,
    )


@dataclass
class DetachedSchemeDesign:
    """The outcome of :func:`design_detached_scheme`."""

    cell: LittoralCell
    climate: WaveClimate
    breakwater: DetachedBreakwater
    frontage: float
    response: dict
    layout: dict
    transmission: dict
    Hs: float
    period: float
    Dn50: float
    crest_width: float
    cot_alpha: float
    notes: list[str] = field(default_factory=list)

    @property
    def verdict(self) -> str:
        """The consensus response, or ``"disputed"`` if the rules split."""
        return self.response["consensus"] or "disputed"

    @property
    def submerged(self) -> bool:
        return self.breakwater.crest_level < 0
