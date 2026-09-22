# Part IV. Design applications {.part .unnumbered}

# Design conditions from a record {#sec:extremes}

*Module:* `pyCoastal.applications.extremes`. *Example:*
`examples/design_wave.py`. *Browser:* Return values.

Every structure in this package is sized against a design condition, and
that condition has to come from somewhere. This module is where it comes
from: a measured or hindcast record in, a return value with an honest
confidence band out.

## Two routes

**Peaks over threshold (POT).** Keep the independent storm peaks above a
threshold, fit a generalized Pareto distribution (GPD) to the excesses, and
combine it with the rate at which peaks arrive. It uses the record
efficiently, but the answer depends on the threshold, so the threshold is
chosen with the diagnostics below rather than by eye.

**Block maxima.** Keep the largest value in each year and fit a generalized
extreme value (GEV) distribution. It wastes data but is hard to get wrong,
and it is the right check on a POT answer.

Both are fitted by **L-moments** (Hosking and Wallis 1997), which are close
to unbiased for the sample sizes a coastal record offers, are not troubled by
the flat likelihood surfaces that defeat maximum likelihood on short
records, and need no optimizer. Shape parameters use the extreme-value
convention: a positive shape is a heavy tail with no upper bound, a negative
shape a finite upper limit. Hosking writes $k = -\text{shape}$; the
conversion is done internally and never exposed.

## Theory

**Declustering.** `decluster(values, threshold, separation)` walks the
record and keeps only the largest value in each run above the threshold.
Two runs separated by fewer than `separation` samples below the threshold
are one storm. For a 3-hourly record, 24 samples is a three-day separation,
the usual choice for storm waves.

**GPD fit.** With survivor function
$1 - F(x) = (1 + \xi x/\sigma)^{-1/\xi}$ (exponential as $\xi \to 0$), the
L-moment estimators from the mean $\lambda_1$ and L-CV
$\tau = \lambda_2/\lambda_1$ of the excesses are

$$ \xi = 2 - \frac{1}{\tau},\qquad \sigma = \lambda_1(1 - \xi). $$ {#eq:gpd-lmom}

A shape at or above one means the fitted mean does not exist; the fit is
returned and flagged rather than clipped.

**POT return value.** With $\lambda$ peaks per year, the $T$-year value is

$$ x_T = u + \frac{\sigma}{\xi}\left[(\lambda T)^{\xi} - 1\right], $$ {#eq:pot-return}

with the logarithmic form in the exponential limit. A return period shorter
than $1/\lambda$ is outside the model.

**GEV fit.** With $F(x) = \exp\{-[1 + \xi(x - \mu)/\sigma]^{-1/\xi}\}$, the
parameters come from Hosking's L-moment estimators, whose polynomial
approximation for $k$ from the L-skewness is accurate to better than
$10^{-4}$ for $-0.5 < k < 0.5$.

**Plotting positions.** The empirical return periods use the Gringorten
position $(i - a)/(n + 1 - 2a)$ with $a = 0.44$, close to unbiased for the
Gumbel and GEV families.

**Threshold diagnostics.** Above a threshold where the GPD holds, the mean
excess is linear in the threshold (`mean_residual_life`), and both the
fitted shape and the *modified* scale $\sigma^* = \sigma - \xi u$ are flat
(`threshold_stability`). The raw scale is not threshold-invariant, and
reading it as if it were is a common way to pick a threshold badly.

**Confidence.** `ExtremeFit.confidence` is a percentile bootstrap over the
fitted peaks. It captures sampling error in the parameters and nothing
else: not measurement error, not the choice of threshold, and not whether
the climate that produced the record is the one the structure will see.
Those are usually the larger uncertainties.

## Using the module

```python
from pyCoastal.applications.extremes import (
    fit_pot, fit_block_maxima, mean_residual_life, threshold_stability,
)

mrl = mean_residual_life(record, thresholds)          # pick the threshold properly
stab = threshold_stability(record, thresholds, separation=24)
fit = fit_pot(record, threshold=2.5, separation=24, samples_per_year=2920)

fit.return_value(100)                  # 100-year Hm0
fit.confidence(100, level=0.90)        # and how much it could have been
fit.extrapolation_note(100)            # how far past the record that reaches
print(fit.summary())

check = fit_block_maxima(record, block=2920)   # annual maxima cross-check
```

`fit_pot` and `fit_block_maxima` return an `ExtremeFit` with `kind`
(`"pot"` or `"gev"`), `parameters`, the peaks or maxima in `data`, their
`positions`, the `rate` and record length `years`, the bootstrap `samples`,
and a `warnings` list. The fit warns when there are fewer than one or two
peaks per year or fewer than about thirty in total.

## Worked example

`examples/design_wave.py` builds a 40-year synthetic 3-hourly hindcast of
$H_{m0}$ with known parameters, chooses the threshold with the diagnostics,
fits POT and annual maxima, and hands the 100-year wave to the seawall
designer. Because the record is synthetic, the right answer is known, so
the example also does what a real study cannot: it repeats the whole
analysis on 60 fresh 40-year records and measures the true sampling spread
of the 100-year estimate, then checks the bootstrap band against it.

<!-- output: design_wave -->

![Extreme value analysis of a 40-year record: threshold diagnostics, return level plot with bootstrap band, and the sampling spread of the 100-year estimate.](media/design_wave.png){#fig:design-wave}

The bootstrap band from the single record (width 1.45 m) matches the real
sampling spread across records (1.32 m), and the true 100-year value of
5.25 m sits inside it. The 100-year wave is 2.5 times the record length, so
the band should be treated as a lower bound on the real uncertainty, which
is exactly what `extrapolation_note` says.

## Limits

- Stationarity is assumed: no trend or climate change in the record.
- The band is sampling error only.
- Very short records, or thresholds that leave too few peaks, are flagged
  but still fitted.
