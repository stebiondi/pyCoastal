# Part III. Design applications {.part .unnumbered}

# Design conditions from a record {#sec:extremes}

*Module:* `pyCoastal.applications.extremes`. *Example:*
`examples/design_wave.py`. *Browser:* Return values.

The module derives a design condition from a measured or hindcast record and
returns a return value with a confidence band. The design conditions used by
the structural modules of this part originate here.

## Methods

**Peaks over threshold (POT).** Independent storm peaks above a threshold are
retained, a generalized Pareto distribution (GPD) is fitted to the excesses,
and the fit is combined with the arrival rate of the peaks. The result
depends on the threshold, which is selected with the diagnostics described
below.

**Block maxima.** The largest value in each year is retained and a
generalized extreme value (GEV) distribution is fitted. The method uses less
of the record and provides an independent check on a POT result.

Both are fitted by **L-moments** (Hosking and Wallis 1997). L-moment
estimators are close to unbiased at the sample sizes of a coastal record,
are stable on the flat likelihood surfaces of short records, and require no
optimizer. Shape parameters follow the extreme-value convention: a positive
shape gives a heavy tail with no upper bound, a negative shape a finite
upper limit. Hosking's $k = -\text{shape}$ is converted internally and is
not exposed in the interface.

## Formulation

**Declustering.** `decluster(values, threshold, separation)` scans the record
and retains the largest value in each run above the threshold. Two runs
separated by fewer than `separation` samples below the threshold are treated
as one storm. For a 3-hourly record, 24 samples corresponds to a three-day
separation, the standard value for storm waves.

**GPD fit.** With survivor function
$1 - F(x) = (1 + \xi x/\sigma)^{-1/\xi}$ (exponential as $\xi \to 0$), the
L-moment estimators from the mean $\lambda_1$ and L-CV
$\tau = \lambda_2/\lambda_1$ of the excesses are given by @eq:gpd-lmom,

$$ \xi = 2 - \frac{1}{\tau},\qquad \sigma = \lambda_1(1 - \xi). $$ {#eq:gpd-lmom}

A shape at or above one implies an undefined fitted mean. The fit is
returned with a warning and is not clipped.

**POT return value.** With $\lambda$ peaks per year, the $T$-year value is @eq:pot-return,

$$ x_T = u + \frac{\sigma}{\xi}\left[(\lambda T)^{\xi} - 1\right], $$ {#eq:pot-return}

with the logarithmic form in the exponential limit. Return periods shorter
than $1/\lambda$ are outside the model.

**GEV fit.** With $F(x) = \exp\{-[1 + \xi(x - \mu)/\sigma]^{-1/\xi}\}$, the
parameters follow Hosking's L-moment estimators. The polynomial
approximation for $k$ from the L-skewness has an accuracy better than
$10^{-4}$ for $-0.5 < k < 0.5$.

**Plotting positions.** Empirical return periods use the Gringorten position
$(i - a)/(n + 1 - 2a)$ with $a = 0.44$, which is close to unbiased for the
Gumbel and GEV families.

**Threshold diagnostics.** Above a threshold at which the GPD applies, the
mean excess is linear in the threshold (`mean_residual_life`), and the
fitted shape and the *modified* scale $\sigma^* = \sigma - \xi u$ are
constant (`threshold_stability`). The raw scale is not threshold-invariant
and is not used for threshold selection.

**Confidence band.** `ExtremeFit.confidence` applies a percentile bootstrap
over the fitted peaks. It quantifies sampling error in the parameters. It
excludes measurement error, threshold selection, and non-stationarity of the
wave climate.

## Interface

```python
from pyCoastal.applications.extremes import (
    fit_pot, fit_block_maxima, mean_residual_life, threshold_stability,
)

mrl = mean_residual_life(record, thresholds)          # threshold diagnostics
stab = threshold_stability(record, thresholds, separation=24)
fit = fit_pot(record, threshold=2.5, separation=24, samples_per_year=2920)

fit.return_value(100)                  # 100-year Hm0
fit.confidence(100, level=0.90)        # confidence band
fit.extrapolation_note(100)            # extrapolation beyond the record
print(fit.summary())

check = fit_block_maxima(record, block=2920)   # annual maxima cross-check
```

`fit_pot` and `fit_block_maxima` return an `ExtremeFit` with `kind`
(`"pot"` or `"gev"`), `parameters`, the peaks or maxima in `data`, their
`positions`, the `rate` and record length `years`, the bootstrap `samples`,
and a `warnings` list. A warning is issued for fewer than one or two peaks
per year and for fewer than about thirty peaks in total.

## Worked example

`examples/design_wave.py` generates a 40-year synthetic 3-hourly record of
$H_{m0}$ with known parameters, selects the threshold from the diagnostics,
fits POT and annual maxima, and passes the 100-year wave to the seawall
module. The record is synthetic, so the target value is known. The example
repeats the analysis on 60 independent 40-year records, measures the
sampling spread of the 100-year estimate, and compares the bootstrap band
with that spread.

<!-- output: design_wave -->

![Extreme value analysis of a 40-year record: threshold diagnostics, return level plot with bootstrap band, and the sampling spread of the 100-year estimate.](media/design_wave.png){#fig:design-wave}

The bootstrap band from the single record has a width of 1.45 m against a
sampling spread across records of 1.32 m, and contains the target value of
5.25 m. The 100-year return period is 2.5 times the record length;
`extrapolation_note` reports this ratio, and the band is a lower bound on
the total uncertainty.

## Limitations

- Stationarity is assumed: no trend or climate change in the record.
- The confidence band quantifies sampling error only.
- Short records and thresholds retaining few peaks are fitted and flagged.
