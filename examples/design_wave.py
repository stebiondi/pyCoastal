"""
From a wave record to a design wave, and on to a structure.

Takes a 40-year synthetic hindcast of significant wave height, chooses a
storm threshold with the standard diagnostics, fits a peaks-over-threshold
model, cross-checks it against annual maxima, and hands the 100-year wave to
the seawall designer.

Because the record is synthetic, the right answer is known, so the example
also does something a real study cannot: it repeats the whole exercise on
many independent 40-year records and measures how much the 100-year estimate
moves. That spread is the uncertainty the bootstrap band is trying to
capture, and comparing the two says whether the band can be believed.

Run from the repository root:

    python examples/design_wave.py
"""

import matplotlib.pyplot as plt
import numpy as np

from pyCoastal.applications.extremes import (
    decluster,
    fit_block_maxima,
    fit_gpd,
    fit_pot,
    gpd_return_value,
    mean_residual_life,
    plotting_positions,
    threshold_stability,
)
from pyCoastal.applications.seawall import design_seawall
from pyCoastal.applications.structures import DesignConditions
from pyCoastal.drafting import use_crisp_style

use_crisp_style()

PER_YEAR = 2920            # three-hourly
YEARS = 40
N = PER_YEAR * YEARS

# The climate the synthetic record is drawn from. Storm peaks sit above
# 2.5 m with a generalised Pareto excess, so every fitted number below has
# something true to be compared against.
TRUE_THRESHOLD, TRUE_SCALE, TRUE_SHAPE, TRUE_RATE = 2.5, 0.55, -0.08, 9.0
SEPARATION = 24            # 3 days below the threshold ends a storm
THRESHOLD = 2.5
DESIGN_PERIOD = 100.0


def synthetic_record(seed: int):
    """A 40-year three-hourly Hm0 record with a known storm climate.

    Seasonal swell background, with storms laid over it by a maximum rather
    than added to it, so the peak of the record really is the threshold plus
    a generalised Pareto excess.
    """
    rng = np.random.default_rng(seed)
    t = np.arange(N) / PER_YEAR
    background = (1.1 + 0.45 * np.sin(2 * np.pi * (t - 0.08))
                  + 0.18 * rng.standard_normal(N))
    record = np.clip(background, 0.15, None)

    starts = np.sort(rng.integers(0, N - 60, size=rng.poisson(TRUE_RATE * YEARS)))
    starts = starts[np.concatenate(([True], np.diff(starts) > 120))]
    u = rng.random(starts.size)
    excess = TRUE_SCALE / TRUE_SHAPE * ((1 - u) ** (-TRUE_SHAPE) - 1)

    for start, value in zip(starts, excess):
        width = int(rng.integers(8, 26))
        envelope = np.exp(-((np.arange(2 * width) - width) / (0.55 * width)) ** 2)
        end = min(start + 2 * width, N)
        record[start:end] = np.maximum(
            record[start:end], (TRUE_THRESHOLD + value) * envelope[:end - start]
        )
    return record, t, starts.size / YEARS


# Seed chosen so this record sits near the middle of what 40 years can
# produce, rather than at a flattering or an alarming tail. The repeat study
# further down reports where it actually falls.
record, t, actual_rate = synthetic_record(seed=20260959)
print(f"Record: {YEARS} years, {N} samples, max {record.max():.2f} m, "
      f"{actual_rate * YEARS:.0f} storms ({actual_rate:.1f}/yr)")

# --- threshold selection ---------------------------------------------------
levels = np.arange(1.8, 3.8, 0.05)
mrl = mean_residual_life(record, levels)
stab = threshold_stability(record, levels, separation=SEPARATION,
                           samples_per_year=PER_YEAR)
print(f"Threshold {THRESHOLD:.2f} m chosen from the diagnostics "
      f"(the record was built with {TRUE_THRESHOLD:.2f} m)")

# --- fit -------------------------------------------------------------------
pot = fit_pot(record, THRESHOLD, separation=SEPARATION,
              samples_per_year=PER_YEAR, bootstrap=800)
gev = fit_block_maxima(record, block=PER_YEAR, samples_per_year=PER_YEAR,
                       bootstrap=800)

print("\nPeaks over threshold")
print(pot.summary())
print(f"   the record was built with scale {TRUE_SCALE:.3f}, "
      f"shape {TRUE_SHAPE:+.3f}, rate {actual_rate:.1f}/yr")
print("\nAnnual maxima, as a cross-check")
print(gev.summary())

Hs100 = float(np.atleast_1d(pot.return_value(DESIGN_PERIOD))[0])
band = pot.confidence(DESIGN_PERIOD)
truth = float(gpd_return_value(TRUE_THRESHOLD, TRUE_SCALE, TRUE_SHAPE,
                               actual_rate, DESIGN_PERIOD))
print(f"\n{DESIGN_PERIOD:.0f}-year Hm0 = {Hs100:.2f} m "
      f"({band['lower'][0]:.2f} to {band['upper'][0]:.2f} m, 90% bootstrap)")
print(f"   true value for this climate: {truth:.2f} m")
print(f"   {pot.extrapolation_note(DESIGN_PERIOD)}")

# --- how much would another 40 years have changed the answer? -------------
# A real study gets one record and one number. Here the climate is known, so
# the same 40-year study can be repeated on fresh records and the spread of
# the answer measured directly.
REPEATS = 60
estimates = []
for seed in range(1000, 1000 + REPEATS):
    other, _, rate = synthetic_record(seed)
    peaks, _ = decluster(other, THRESHOLD, SEPARATION)
    if peaks.size < 30:
        continue
    scale, shape = fit_gpd(peaks - THRESHOLD)
    estimates.append(float(gpd_return_value(THRESHOLD, scale, shape,
                                            peaks.size / YEARS, DESIGN_PERIOD)))
estimates = np.array(estimates)
spread = np.percentile(estimates, [5, 95])
bootstrap_width = band["upper"][0] - band["lower"][0]

print(f"\nRepeating the study on {estimates.size} fresh {YEARS}-year records")
print(f"   100-year estimate: mean {estimates.mean():.2f} m, "
      f"sd {estimates.std(ddof=1):.2f} m")
print(f"   5th to 95th percentile: {spread[0]:.2f} to {spread[1]:.2f} m "
      f"(width {spread[1] - spread[0]:.2f} m)")
print(f"   bootstrap band from the single record: width "
      f"{bootstrap_width:.2f} m")
print(f"   this record sits at the {100 * (estimates < Hs100).mean():.0f}th "
      "percentile of that spread")
if bootstrap_width > 1.15 * (spread[1] - spread[0]):
    print("   The bootstrap band is wider than the real sampling spread: "
          "conservative here.")
elif bootstrap_width < 0.85 * (spread[1] - spread[0]):
    print("   The bootstrap band is narrower than the real sampling spread: "
          "it understates the uncertainty.")
else:
    print("   The bootstrap band matches the real sampling spread.")

# --- the structure that follows -------------------------------------------
# The design wave at the toe is the offshore value reduced by nearshore
# transformation. Here the toe is taken as depth limited at 0.55 h, a common
# screening rule for a wave that has already broken once.
DEPTH_AT_TOE = 8.5
Hm0_toe = min(Hs100, 0.55 * DEPTH_AT_TOE)
conditions = DesignConditions.from_peak_period(
    Hm0=Hm0_toe, Tp=9.5, depth=DEPTH_AT_TOE, storm_duration=6 * 3600.0
)
wall = design_seawall(conditions, still_water_level=2.9, seabed_level=-5.6,
                      tolerable_use="trained_staff")
print(f"\nDesign wave at the toe {Hm0_toe:.2f} m "
      + ("(depth limited)" if Hm0_toe < Hs100 else "(offshore value carried in)"))
print(f"Seawall crest {wall.crest_level:+.2f} m CD, "
      f"base {wall.base_width:.2f} m, "
      f"concrete {wall.quantities()['concrete_total_m3_per_m']:.1f} m3/m")

# --- figure ----------------------------------------------------------------
fig, axes = plt.subplots(2, 2, figsize=(13.5, 8.8))
fig.subplots_adjust(hspace=0.36, wspace=0.24)

ax = axes[0, 0]
window = PER_YEAR * 3
ax.plot(t[:window], record[:window], lw=0.5, color="#1b6fa0")
ax.axhline(THRESHOLD, color="#8a2f24", lw=1.2, ls="--",
           label=f"threshold {THRESHOLD:.1f} m")
in_view = pot.positions < window
ax.plot(t[pot.positions[in_view]], pot.data[in_view], "o", ms=4.5,
        markerfacecolor="white", markeredgecolor="#8a2f24",
        markeredgewidth=1.0, label="declustered peaks")
ax.set_title("Hindcast, first three years")
ax.set_xlabel("years")
ax.set_ylabel("Hm0 (m)")
ax.legend(loc="upper right", fontsize=8)
ax.grid(True, which="both", alpha=0.3)
ax.minorticks_on()

ax = axes[0, 1]
ax.errorbar(mrl["thresholds"], mrl["mean_excess"], yerr=1.96 * mrl["stderr"],
            color="#14567f", ecolor="#9fc4d6", lw=1.3, elinewidth=0.8,
            capsize=0)
ax.axvline(THRESHOLD, color="#8a2f24", lw=1.2, ls="--")
ax.set_title("Mean residual life: straight above a valid threshold")
ax.set_xlabel("threshold (m)")
ax.set_ylabel("mean excess (m)")
ax.grid(True, which="both", alpha=0.3)
ax.minorticks_on()

ax = axes[1, 0]
ax.plot(stab["thresholds"], stab["shape"], color="#14567f", lw=1.4,
        label="fitted shape")
ax.axhline(TRUE_SHAPE, color="#4a7c3f", lw=1.1, ls=":",
           label=f"true shape {TRUE_SHAPE:+.2f}")
ax.axvline(THRESHOLD, color="#8a2f24", lw=1.2, ls="--")
ax.set_ylim(-0.6, 0.6)
ax.set_title("Shape against threshold: flat where the model holds")
ax.set_xlabel("threshold (m)")
ax.set_ylabel("shape")
ax.legend(loc="lower left", fontsize=8)
ax.grid(True, which="both", alpha=0.3)
ax.minorticks_on()

ax = axes[1, 1]
periods = np.logspace(np.log10(0.2), np.log10(500), 160)
band_all = pot.confidence(periods)
ax.fill_between(periods, band_all["lower"], band_all["upper"],
                color="#9fc4d6", alpha=0.55, label="90% bootstrap band")
ax.plot(periods, band_all["central"], color="#0b3554", lw=1.8,
        label="peaks over threshold")
ax.plot(periods, gpd_return_value(TRUE_THRESHOLD, TRUE_SCALE, TRUE_SHAPE,
                                  actual_rate, periods),
        color="#4a7c3f", lw=1.3, ls=":", label="true climate")
# Annual maxima say nothing below a one-year return period, so the curve
# starts where the model is defined rather than being clipped flat.
annual = periods[periods > 1.05]
ax.plot(annual, gev.return_value(annual), color="#8a2f24", lw=1.2, ls="--",
        label="annual maxima")

emp = plotting_positions(pot.data, rate=pot.rate)
ax.plot(emp["return_period"], emp["values"], "o", ms=3.2,
        markerfacecolor="white", markeredgecolor="#0b3554",
        markeredgewidth=0.7, label="observed peaks")
ax.axvline(YEARS, color="#4a4a4a", lw=0.9, ls=":")
ax.plot([DESIGN_PERIOD], [Hs100], "*", ms=14, color="#c47f1a",
        markeredgecolor="#5a3a05", markeredgewidth=0.6,
        label=f"design {Hs100:.2f} m")
ax.set_xscale("log")
ax.set_xlabel("return period (years)")
ax.set_ylabel("Hm0 (m)")
ax.set_title(f"Return level (dotted line at the {YEARS}-year record length)")
ax.legend(loc="upper left", fontsize=7.5)
ax.grid(True, which="both", alpha=0.3)

fig.suptitle(
    f"Design wave from a {YEARS}-year record: "
    f"{DESIGN_PERIOD:.0f}-year Hm0 = {Hs100:.2f} m "
    f"({band['lower'][0]:.2f} to {band['upper'][0]:.2f} m), "
    f"true value {truth:.2f} m",
    y=0.975, fontsize=12, fontweight="bold",
)
fig.savefig("media/design_wave.png", dpi=600, bbox_inches="tight")
print("\nWrote media/design_wave.png")
