"""
Extreme value analysis: the design wave and the design water level.

Every structure in this package is sized against a design condition, and
that condition has to come from somewhere. This module is where it comes
from: a measured or hindcast record in, a return value with an honest
confidence band out.

Two routes, both standard.

Peaks over threshold
    Keep the independent storm peaks above a threshold, fit a generalised
    Pareto distribution to the excesses, and combine it with the rate at
    which peaks arrive. Uses the record efficiently, but the answer depends
    on the threshold, so choose it with the diagnostics here rather than by
    eye.
Block maxima
    Keep the largest value in each year and fit a generalised extreme value
    distribution. Wastes data but is hard to get wrong, and is the right
    check on a peaks-over-threshold answer.

Both are fitted by L-moments, which are close to unbiased for the sample
sizes a coastal record actually offers, are not troubled by the flat
likelihood surfaces that defeat maximum likelihood on short records, and
need no optimiser.

Sources
-------
Hosking, J. R. M. and Wallis, J. R. (1997), Regional Frequency Analysis:
    An Approach Based on L-Moments. Cambridge University Press.
Coles, S. (2001), An Introduction to Statistical Modeling of Extreme
    Values. Springer. Threshold selection, return level interpretation.
Goda, Y. (2010), Random Seas and Design of Maritime Structures, ch. 11.
    Extreme wave statistics in coastal engineering practice.

Conventions
-----------
Shape parameters use the extreme value convention, so a positive shape is a
heavy tail with no upper bound and a negative shape has a finite upper
limit. Hosking writes k = -shape; the two are converted where his estimators
are used, and never mixed in the public interface.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np

__all__ = [
    "l_moments",
    "decluster",
    "peaks_over_threshold",
    "block_maxima",
    "fit_gpd",
    "fit_gev",
    "gpd_return_value",
    "gev_return_value",
    "ExtremeFit",
    "fit_pot",
    "fit_block_maxima",
    "mean_residual_life",
    "threshold_stability",
    "plotting_positions",
]


# ---------------------------------------------------------------------------
# L-moments
# ---------------------------------------------------------------------------


def l_moments(sample, count: int = 4) -> np.ndarray:
    """Sample L-moments, unbiased, from probability weighted moments.

    Parameters
    ----------
    sample : array_like
        One-dimensional sample. Order does not matter; it is sorted here.
    count : int
        How many L-moments to return, from 1 to 4. The first is the mean,
        the second a measure of spread, the third and fourth the L-skewness
        and L-kurtosis numerators.

    Returns
    -------
    ndarray
        ``count`` L-moments.

    Notes
    -----
    These are the unbiased estimators, so they need at least ``count``
    points. With fewer, the higher moments are not estimable at all and the
    function says so rather than returning a plausible-looking number.
    """
    if not 1 <= count <= 4:
        raise ValueError(f"Can return 1 to 4 L-moments, asked for {count}")
    x = np.sort(np.asarray(sample, dtype=float).ravel())
    n = x.size
    if n < count:
        raise ValueError(
            f"Need at least {count} points for {count} L-moments, got {n}"
        )

    j = np.arange(1, n + 1, dtype=float)
    b = np.zeros(4)
    b[0] = x.mean()
    b[1] = np.sum((j - 1) / (n - 1) * x) / n
    if count > 2:
        b[2] = np.sum((j - 1) * (j - 2) / ((n - 1) * (n - 2)) * x) / n
    if count > 3:
        b[3] = np.sum(
            (j - 1) * (j - 2) * (j - 3) / ((n - 1) * (n - 2) * (n - 3)) * x
        ) / n

    # Only the moments that were asked for: b[2] and b[3] are untouched
    # when count is small, and combining them would be arithmetic on
    # whatever np.empty happened to hand back.
    lam = np.empty(count)
    lam[0] = b[0]
    if count > 1:
        lam[1] = 2 * b[1] - b[0]
    if count > 2:
        lam[2] = 6 * b[2] - 6 * b[1] + b[0]
    if count > 3:
        lam[3] = 20 * b[3] - 30 * b[2] + 12 * b[1] - b[0]
    return lam


# ---------------------------------------------------------------------------
# Extracting extremes from a record
# ---------------------------------------------------------------------------


def decluster(values, threshold: float, separation: int = 1):
    """Independent peaks above a threshold.

    Walks the record, and within each run of values above the threshold
    keeps only the largest. Two runs separated by fewer than ``separation``
    samples below the threshold are treated as one storm, which is what
    stops a single event contributing several "independent" peaks.

    Parameters
    ----------
    values : array_like
        The record, evenly sampled.
    threshold : float
        Level above which a storm is counted.
    separation : int
        Number of consecutive samples below the threshold needed to end a
        storm. For a 3-hourly record, 24 samples is a 3-day separation,
        which is the usual choice for storm waves.

    Returns
    -------
    (ndarray, ndarray)
        Peak values and their indices in the record.
    """
    x = np.asarray(values, dtype=float).ravel()
    if separation < 1:
        raise ValueError(f"Separation must be at least 1 sample, got {separation}")
    above = x > threshold
    if not above.any():
        return np.array([]), np.array([], dtype=int)

    peaks, positions = [], []
    i = 0
    n = x.size
    while i < n:
        if not above[i]:
            i += 1
            continue
        # Extend the storm while any exceedance lies within the separation.
        start = i
        end = i
        j = i
        while j < n:
            if above[j]:
                end = j
                j += 1
            elif j - end <= separation:
                j += 1
            else:
                break
        window = x[start:end + 1]
        local = int(np.argmax(window))
        peaks.append(float(window[local]))
        positions.append(start + local)
        i = end + 1
    return np.array(peaks), np.array(positions, dtype=int)


def peaks_over_threshold(values, threshold: float, separation: int = 1,
                         samples_per_year: float = 2920.0) -> dict:
    """Declustered peaks and the rate at which they arrive.

    ``samples_per_year`` converts the record length into years, so the
    default is a 3-hourly record. The rate is what turns a distribution of
    excesses into a return period.
    """
    peaks, positions = decluster(values, threshold, separation)
    n = np.asarray(values).size
    years = n / samples_per_year
    if years <= 0:
        raise ValueError("Record length works out as zero years")
    return {
        "peaks": peaks,
        "positions": positions,
        "excesses": peaks - threshold,
        "threshold": threshold,
        "rate": peaks.size / years,
        "years": years,
        "count": peaks.size,
    }


def block_maxima(values, block: int) -> np.ndarray:
    """Largest value in each complete block of ``block`` samples.

    A partial block at the end is dropped: an annual maximum taken from
    four months of record is not an annual maximum.
    """
    x = np.asarray(values, dtype=float).ravel()
    if block < 1:
        raise ValueError(f"Block must be at least one sample, got {block}")
    n_blocks = x.size // block
    if n_blocks < 1:
        raise ValueError(
            f"Record of {x.size} samples is shorter than one {block}-sample block"
        )
    return x[: n_blocks * block].reshape(n_blocks, block).max(axis=1)


# ---------------------------------------------------------------------------
# Distributions
# ---------------------------------------------------------------------------


def fit_gpd(excesses) -> tuple[float, float]:
    """Fit a generalised Pareto distribution to threshold excesses.

    Returns
    -------
    (scale, shape)
        With the survivor function
        ``1 - F(x) = (1 + shape x / scale) ** (-1 / shape)``, and the
        exponential limit as shape goes to zero.

    Notes
    -----
    L-moment estimators, from the mean and L-CV of the excesses::

        shape = 2 - 1 / tau
        scale = mean * (1 - shape)

    where tau = l2 / l1. A shape at or above 1 means the fitted mean does
    not exist, which on a wave record means the threshold is far too low or
    the sample far too small; the fit is returned anyway, flagged by the
    caller, rather than silently clipped.
    """
    x = np.asarray(excesses, dtype=float).ravel()
    if x.size < 2:
        raise ValueError(f"Need at least two excesses to fit, got {x.size}")
    if np.any(x < 0):
        raise ValueError("Excesses must be non-negative; subtract the threshold")

    l1, l2 = l_moments(x, 2)
    if l1 <= 0 or l2 <= 0:
        raise ValueError("Excesses have no spread; cannot fit a distribution")
    tau = l2 / l1
    shape = 2.0 - 1.0 / tau
    scale = l1 * (1.0 - shape)
    if scale <= 0:
        raise ValueError(
            f"Fitted scale {scale:.3g} is not positive; the sample is not "
            "Pareto-like. Try a higher threshold."
        )
    return float(scale), float(shape)


def fit_gev(maxima) -> tuple[float, float, float]:
    """Fit a generalised extreme value distribution to block maxima.

    Returns
    -------
    (location, scale, shape)
        With ``F(x) = exp(-(1 + shape (x - loc) / scale) ** (-1 / shape))``.

    Notes
    -----
    Hosking's L-moment estimators. His shape k is the negative of the
    extreme value shape, and his polynomial approximation for k from the
    L-skewness is accurate to better than 1e-4 for -0.5 < k < 0.5, which
    covers every coastal record in practice.
    """
    x = np.asarray(maxima, dtype=float).ravel()
    if x.size < 3:
        raise ValueError(f"Need at least three maxima to fit, got {x.size}")

    l1, l2, l3 = l_moments(x, 3)
    if l2 <= 0:
        raise ValueError("Maxima have no spread; cannot fit a distribution")

    tau3 = l3 / l2
    c = 2.0 / (3.0 + tau3) - math.log(2.0) / math.log(3.0)
    k = 7.8590 * c + 2.9554 * c * c

    if abs(k) < 1e-6:
        # Gumbel limit.
        scale = l2 / math.log(2.0)
        loc = l1 - scale * 0.5772156649015329
        return float(loc), float(scale), 0.0

    gamma_k = math.gamma(1.0 + k)
    scale = l2 * k / ((1.0 - 2.0 ** -k) * gamma_k)
    loc = l1 - scale * (1.0 - gamma_k) / k
    return float(loc), float(scale), float(-k)


def gpd_return_value(threshold: float, scale: float, shape: float,
                     rate: float, return_period) -> np.ndarray:
    """Return value from a peaks-over-threshold fit.

    ``rate`` is the mean number of peaks per year and ``return_period`` is
    in years, so ``rate * return_period`` is the expected number of peaks in
    that period::

        x_T = u + scale / shape * ((rate T) ** shape - 1)

    with the logarithmic form in the exponential limit. A return period
    shorter than one over the rate asks for a level exceeded more often
    than peaks occur, which is outside the model.
    """
    if scale <= 0:
        raise ValueError(f"Scale must be positive, got {scale}")
    if rate <= 0:
        raise ValueError(f"Peak rate must be positive, got {rate}")
    T = np.asarray(return_period, dtype=float)
    if np.any(T <= 0):
        raise ValueError("Return periods must be positive")

    m = rate * T
    if abs(shape) < 1e-8:
        return threshold + scale * np.log(m)
    return threshold + scale / shape * (m ** shape - 1.0)


def gev_return_value(location: float, scale: float, shape: float,
                     return_period) -> np.ndarray:
    """Return value from a block maxima fit, for blocks of one year.

        x_T = loc + scale / shape * (1 - (-ln(1 - 1/T)) ** shape)

    with the Gumbel form in the limit. If the blocks are not years, the
    return period is in blocks.
    """
    if scale <= 0:
        raise ValueError(f"Scale must be positive, got {scale}")
    T = np.asarray(return_period, dtype=float)
    if np.any(T <= 1.0):
        raise ValueError("Block maxima return periods must exceed one block")

    y = -np.log(-np.log(1.0 - 1.0 / T))
    if abs(shape) < 1e-8:
        return location + scale * y
    return location + scale / shape * (np.exp(shape * y) - 1.0)


# ---------------------------------------------------------------------------
# A fitted model
# ---------------------------------------------------------------------------


@dataclass
class ExtremeFit:
    """A fitted extreme value model with a confidence band.

    Attributes
    ----------
    kind : str
        "pot" or "gev".
    parameters : dict
        The fitted parameters.
    data : ndarray
        The peaks or maxima the fit used.
    positions : ndarray or None
        Index of each peak in the original record, for a peaks-over-
        threshold fit. None for block maxima.
    rate : float
        Peaks per year. One, by definition, for annual maxima.
    years : float
        Length of the record, for judging how far the fit can be pushed.
    samples : ndarray
        Bootstrap parameter sets, one row each, used for the band.
    warnings : list of str
        Anything about the fit the engineer should see before using it.
    """

    kind: str
    parameters: dict
    data: np.ndarray
    rate: float
    years: float
    samples: np.ndarray | None = None
    positions: np.ndarray | None = None
    warnings: list[str] = field(default_factory=list)

    def return_value(self, return_period):
        """Return value at one or many return periods [same units as the data]."""
        p = self.parameters
        if self.kind == "pot":
            return gpd_return_value(p["threshold"], p["scale"], p["shape"],
                                    self.rate, return_period)
        return gev_return_value(p["location"], p["scale"], p["shape"],
                                return_period)

    def confidence(self, return_period, level: float = 0.90) -> dict:
        """Bootstrap confidence band on the return value.

        Percentile bootstrap over the fitted peaks. It captures sampling
        error in the parameters and nothing else: not the measurement error
        in the record, not the choice of threshold, and not whether the
        climate that produced the record is the climate the structure will
        see. Those are usually the larger uncertainties.
        """
        if self.samples is None or len(self.samples) == 0:
            raise RuntimeError("This fit carries no bootstrap samples")
        if not 0.0 < level < 1.0:
            raise ValueError(f"Confidence level must be in (0,1), got {level}")

        T = np.atleast_1d(np.asarray(return_period, dtype=float))
        draws = np.empty((len(self.samples), T.size))
        for i, row in enumerate(self.samples):
            if self.kind == "pot":
                threshold, scale, shape, rate = row
                draws[i] = gpd_return_value(threshold, scale, shape, rate, T)
            else:
                loc, scale, shape = row
                draws[i] = gev_return_value(loc, scale, shape, T)

        alpha = 0.5 * (1.0 - level)
        return {
            "central": np.atleast_1d(self.return_value(T)),
            "lower": np.percentile(draws, 100 * alpha, axis=0),
            "upper": np.percentile(draws, 100 * (1.0 - alpha), axis=0),
            "level": level,
        }

    def extrapolation_note(self, return_period: float) -> str:
        """How far beyond the record a return period reaches."""
        ratio = return_period / self.years if self.years > 0 else float("inf")
        if ratio <= 1.0:
            return f"Within the {self.years:.0f} year record."
        return (
            f"{ratio:.1f} times the {self.years:.0f} year record. Treat the "
            "confidence band as a lower bound on the real uncertainty."
        )

    def summary(self, return_periods=(10, 50, 100)) -> str:
        """A short report of the fit and its return values."""
        p = self.parameters
        lines = [
            f"Model              {'peaks over threshold' if self.kind == 'pot' else 'annual maxima'}",
            f"Record             {self.years:.1f} years, {self.data.size} "
            f"{'peaks' if self.kind == 'pot' else 'maxima'}",
        ]
        if self.kind == "pot":
            lines += [
                f"Threshold          {p['threshold']:.2f}",
                f"Rate               {self.rate:.2f} peaks per year",
                f"Scale, shape       {p['scale']:.3f}, {p['shape']:+.3f}",
            ]
        else:
            lines += [
                f"Location           {p['location']:.3f}",
                f"Scale, shape       {p['scale']:.3f}, {p['shape']:+.3f}",
            ]
        lines.append("")
        lines.append("Return period   value    90% band")
        for T in return_periods:
            value = float(np.atleast_1d(self.return_value(T))[0])
            if self.samples is not None:
                band = self.confidence(T)
                lines.append(
                    f"  {T:>5g} yr     {value:6.2f}   "
                    f"{band['lower'][0]:.2f} to {band['upper'][0]:.2f}"
                )
            else:
                lines.append(f"  {T:>5g} yr     {value:6.2f}")
        if self.warnings:
            lines += ["", "Warnings"] + [f"  - {w}" for w in self.warnings]
        return "\n".join(lines)


def _bootstrap_pot(excesses, threshold, rate, years, draws, rng):
    """Resample peaks, refit, and also resample how many peaks occur."""
    out = []
    n = excesses.size
    for _ in range(draws):
        resample = rng.choice(excesses, size=n, replace=True)
        try:
            scale, shape = fit_gpd(resample)
        except ValueError:
            continue
        # The number of peaks is itself a Poisson observation, so the rate
        # carries its own sampling error. Ignoring it understates the band.
        count = rng.poisson(rate * years)
        out.append((threshold, scale, shape, max(count, 1) / years))
    return np.array(out)


def _bootstrap_gev(maxima, draws, rng):
    out = []
    n = maxima.size
    for _ in range(draws):
        resample = rng.choice(maxima, size=n, replace=True)
        try:
            out.append(fit_gev(resample))
        except ValueError:
            continue
    return np.array(out)


def fit_pot(values, threshold: float, separation: int = 1,
            samples_per_year: float = 2920.0, bootstrap: int = 500,
            seed: int = 0) -> ExtremeFit:
    """Peaks-over-threshold fit to a record, with a bootstrap band.

    Parameters
    ----------
    values : array_like
        The record, evenly sampled.
    threshold : float
        Storm threshold, in the units of the record.
    separation : int
        Samples below the threshold that end a storm.
    samples_per_year : float
        Default is a 3-hourly record: 2920 samples a year.
    bootstrap : int
        Bootstrap resamples. Zero skips the band.

    Notes
    -----
    A useful rule is to want at least one or two peaks a year and no fewer
    than about thirty in total; the fit warns when either is missed.
    """
    pot = peaks_over_threshold(values, threshold, separation, samples_per_year)
    excesses = pot["excesses"]
    if excesses.size < 2:
        raise ValueError(
            f"Only {excesses.size} peak(s) above {threshold}; lower the threshold"
        )

    scale, shape = fit_gpd(excesses)
    warnings = []
    if excesses.size < 30:
        warnings.append(
            f"Only {excesses.size} peaks above the threshold. Below about 30 the "
            "shape parameter is poorly determined and the band is optimistic."
        )
    if pot["rate"] < 1.0:
        warnings.append(
            f"Peak rate {pot['rate']:.2f} per year is under one. The threshold "
            "is high enough that whole years contribute nothing."
        )
    if shape >= 0.5:
        warnings.append(
            f"Fitted shape {shape:+.2f} is a very heavy tail. Check the "
            "threshold and look for outliers before using the return values."
        )

    rng = np.random.default_rng(seed)
    samples = (_bootstrap_pot(excesses, threshold, pot["rate"], pot["years"],
                              bootstrap, rng) if bootstrap else None)

    return ExtremeFit(
        kind="pot",
        parameters={"threshold": threshold, "scale": scale, "shape": shape},
        data=pot["peaks"],
        rate=pot["rate"],
        years=pot["years"],
        samples=samples,
        positions=pot["positions"],
        warnings=warnings,
    )


def fit_block_maxima(values, block: int, samples_per_year: float = 2920.0,
                     bootstrap: int = 500, seed: int = 0) -> ExtremeFit:
    """Block maxima fit, with a bootstrap band.

    ``block`` is in samples. For annual maxima from a 3-hourly record that
    is 2920.
    """
    maxima = block_maxima(values, block)
    loc, scale, shape = fit_gev(maxima)
    years = np.asarray(values).size / samples_per_year

    warnings = []
    if maxima.size < 20:
        warnings.append(
            f"Only {maxima.size} block maxima. A GEV fitted to fewer than "
            "about 20 blocks carries very wide real uncertainty."
        )
    if shape >= 0.5:
        warnings.append(
            f"Fitted shape {shape:+.2f} implies an extremely heavy tail; "
            "check for outliers."
        )

    rng = np.random.default_rng(seed)
    samples = _bootstrap_gev(maxima, bootstrap, rng) if bootstrap else None

    return ExtremeFit(
        kind="gev",
        parameters={"location": loc, "scale": scale, "shape": shape},
        data=maxima,
        rate=1.0,
        years=years,
        samples=samples,
        warnings=warnings,
    )


# ---------------------------------------------------------------------------
# Threshold diagnostics
# ---------------------------------------------------------------------------


def mean_residual_life(values, thresholds) -> dict:
    """Mean excess above each threshold, with a standard error.

    Above a threshold where the generalised Pareto model holds, the mean
    excess is linear in the threshold. The lowest threshold from which the
    plot is straight is the one to use: lower wastes the model's validity,
    higher throws away data.
    """
    x = np.asarray(values, dtype=float).ravel()
    u = np.asarray(thresholds, dtype=float).ravel()
    mean = np.full(u.size, np.nan)
    stderr = np.full(u.size, np.nan)
    count = np.zeros(u.size, dtype=int)

    for i, level in enumerate(u):
        excess = x[x > level] - level
        count[i] = excess.size
        if excess.size > 1:
            mean[i] = excess.mean()
            stderr[i] = excess.std(ddof=1) / math.sqrt(excess.size)
    return {"thresholds": u, "mean_excess": mean, "stderr": stderr,
            "count": count}


def threshold_stability(values, thresholds, separation: int = 1,
                        samples_per_year: float = 2920.0) -> dict:
    """Fitted shape and modified scale against threshold.

    Both should be flat above a threshold where the model holds. The scale
    is reported in its modified form, ``scale - shape * threshold``, which
    is the quantity that is threshold-invariant; the raw scale is not, and
    reading it as if it were is a common way to pick a threshold badly.
    """
    u = np.asarray(thresholds, dtype=float).ravel()
    shape = np.full(u.size, np.nan)
    modified = np.full(u.size, np.nan)
    count = np.zeros(u.size, dtype=int)

    for i, level in enumerate(u):
        pot = peaks_over_threshold(values, level, separation, samples_per_year)
        count[i] = pot["count"]
        if pot["count"] < 5:
            continue
        try:
            scale, xi = fit_gpd(pot["excesses"])
        except ValueError:
            continue
        shape[i] = xi
        modified[i] = scale - xi * level
    return {"thresholds": u, "shape": shape, "modified_scale": modified,
            "count": count}


def plotting_positions(sample, rate: float = 1.0, a: float = 0.44) -> dict:
    """Empirical return periods for a sample, for the return level plot.

    Uses the Gringorten plotting position, ``(i - a) / (n + 1 - 2a)`` with
    a = 0.44, which is close to unbiased for the Gumbel and GEV families
    that extreme wave records follow. ``rate`` converts an exceedance
    probability per peak into years.
    """
    x = np.sort(np.asarray(sample, dtype=float).ravel())
    n = x.size
    if n < 1:
        raise ValueError("Empty sample")
    if rate <= 0:
        raise ValueError(f"Rate must be positive, got {rate}")
    i = np.arange(1, n + 1, dtype=float)
    non_exceedance = (i - a) / (n + 1.0 - 2.0 * a)
    exceedance = 1.0 - non_exceedance
    return {"values": x, "return_period": 1.0 / (rate * exceedance),
            "exceedance": exceedance}
