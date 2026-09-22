# `pyCoastal.applications.extremes`

Source: [`pyCoastal/applications/extremes.py`](../../pyCoastal/applications/extremes.py)

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

## `l_moments`

```python
def l_moments(sample, count: int=4) -> np.ndarray
```

```text
Sample L-moments, unbiased, from probability weighted moments.

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
```

## `decluster`

```python
def decluster(values, threshold: float, separation: int=1)
```

```text
Independent peaks above a threshold.

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
```

## `peaks_over_threshold`

```python
def peaks_over_threshold(values, threshold: float, separation: int=1, samples_per_year: float=2920.0) -> dict
```

```text
Declustered peaks and the rate at which they arrive.

``samples_per_year`` converts the record length into years, so the
default is a 3-hourly record. The rate is what turns a distribution of
excesses into a return period.
```

## `block_maxima`

```python
def block_maxima(values, block: int) -> np.ndarray
```

```text
Largest value in each complete block of ``block`` samples.

A partial block at the end is dropped: an annual maximum taken from
four months of record is not an annual maximum.
```

## `fit_gpd`

```python
def fit_gpd(excesses) -> tuple[float, float]
```

```text
Fit a generalised Pareto distribution to threshold excesses.

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
```

## `fit_gev`

```python
def fit_gev(maxima) -> tuple[float, float, float]
```

```text
Fit a generalised extreme value distribution to block maxima.

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
```

## `gpd_return_value`

```python
def gpd_return_value(threshold: float, scale: float, shape: float, rate: float, return_period) -> np.ndarray
```

```text
Return value from a peaks-over-threshold fit.

``rate`` is the mean number of peaks per year and ``return_period`` is
in years, so ``rate * return_period`` is the expected number of peaks in
that period::

    x_T = u + scale / shape * ((rate T) ** shape - 1)

with the logarithmic form in the exponential limit. A return period
shorter than one over the rate asks for a level exceeded more often
than peaks occur, which is outside the model.
```

## `gev_return_value`

```python
def gev_return_value(location: float, scale: float, shape: float, return_period) -> np.ndarray
```

```text
Return value from a block maxima fit, for blocks of one year.

    x_T = loc + scale / shape * (1 - (-ln(1 - 1/T)) ** shape)

with the Gumbel form in the limit. If the blocks are not years, the
return period is in blocks.
```

## `ExtremeFit`

```python
class ExtremeFit
    kind: str
    parameters: dict
    data: np.ndarray
    rate: float
    years: float
    samples: np.ndarray | None = None
    positions: np.ndarray | None = None
    warnings: list[str] = field(default_factory=list)
```

```text
A fitted extreme value model with a confidence band.

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
```

### `ExtremeFit.return_value` (method)

```python
ExtremeFit.return_value(self, return_period)
```

```text
Return value at one or many return periods [same units as the data].
```

### `ExtremeFit.confidence` (method)

```python
ExtremeFit.confidence(self, return_period, level: float=0.9) -> dict
```

```text
Bootstrap confidence band on the return value.

Percentile bootstrap over the fitted peaks. It captures sampling
error in the parameters and nothing else: not the measurement error
in the record, not the choice of threshold, and not whether the
climate that produced the record is the climate the structure will
see. Those are usually the larger uncertainties.
```

### `ExtremeFit.extrapolation_note` (method)

```python
ExtremeFit.extrapolation_note(self, return_period: float) -> str
```

```text
How far beyond the record a return period reaches.
```

### `ExtremeFit.summary` (method)

```python
ExtremeFit.summary(self, return_periods=(10, 50, 100)) -> str
```

```text
A short report of the fit and its return values.
```

## `fit_pot`

```python
def fit_pot(values, threshold: float, separation: int=1, samples_per_year: float=2920.0, bootstrap: int=500, seed: int=0) -> ExtremeFit
```

```text
Peaks-over-threshold fit to a record, with a bootstrap band.

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
```

## `fit_block_maxima`

```python
def fit_block_maxima(values, block: int, samples_per_year: float=2920.0, bootstrap: int=500, seed: int=0) -> ExtremeFit
```

```text
Block maxima fit, with a bootstrap band.

``block`` is in samples. For annual maxima from a 3-hourly record that
is 2920.
```

## `mean_residual_life`

```python
def mean_residual_life(values, thresholds) -> dict
```

```text
Mean excess above each threshold, with a standard error.

Above a threshold where the generalised Pareto model holds, the mean
excess is linear in the threshold. The lowest threshold from which the
plot is straight is the one to use: lower wastes the model's validity,
higher throws away data.
```

## `threshold_stability`

```python
def threshold_stability(values, thresholds, separation: int=1, samples_per_year: float=2920.0) -> dict
```

```text
Fitted shape and modified scale against threshold.

Both should be flat above a threshold where the model holds. The scale
is reported in its modified form, ``scale - shape * threshold``, which
is the quantity that is threshold-invariant; the raw scale is not, and
reading it as if it were is a common way to pick a threshold badly.
```

## `plotting_positions`

```python
def plotting_positions(sample, rate: float=1.0, a: float=0.44) -> dict
```

```text
Empirical return periods for a sample, for the return level plot.

Uses the Gringorten plotting position, ``(i - a) / (n + 1 - 2a)`` with
a = 0.44, which is close to unbiased for the Gumbel and GEV families
that extreme wave records follow. ``rate`` converts an exceedance
probability per peak into years.
```

