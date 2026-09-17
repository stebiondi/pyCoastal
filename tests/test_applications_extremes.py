"""Extreme value analysis: L-moments, fits, return values and diagnostics."""

import math

import numpy as np
import pytest

from pyCoastal.applications.extremes import (
    ExtremeFit,
    block_maxima,
    decluster,
    fit_block_maxima,
    fit_gev,
    fit_gpd,
    fit_pot,
    gev_return_value,
    gpd_return_value,
    l_moments,
    mean_residual_life,
    peaks_over_threshold,
    plotting_positions,
    threshold_stability,
)

EULER = 0.5772156649015329


def gpd_sample(scale, shape, size, rng):
    """Exact inverse-transform draw from a generalised Pareto."""
    u = rng.random(size)
    if shape == 0:
        return -scale * np.log(1 - u)
    return scale / shape * ((1 - u) ** (-shape) - 1)


def gev_sample(loc, scale, shape, size, rng):
    y = -np.log(rng.random(size))
    if shape == 0:
        return loc - scale * np.log(y)
    return loc + scale / shape * (y ** (-shape) - 1)


# ---------------------------------------------------------------------------
# L-moments
# ---------------------------------------------------------------------------


def test_first_l_moment_is_the_mean():
    x = np.array([3.0, 1.0, 4.0, 1.0, 5.0])
    assert l_moments(x, 1)[0] == pytest.approx(x.mean())


def test_l_moments_do_not_depend_on_order():
    rng = np.random.default_rng(3)
    x = rng.random(50)
    assert np.allclose(l_moments(x, 4), l_moments(rng.permutation(x), 4))


def test_second_l_moment_is_half_the_mean_absolute_difference():
    """l2 = E|X1 - X2| / 2, the defining property."""
    x = np.array([1.0, 2.0, 6.0, 9.0])
    pairs = [abs(a - b) for i, a in enumerate(x) for b in x[i + 1:]]
    assert l_moments(x, 2)[1] == pytest.approx(np.mean(pairs) / 2.0)


def test_l_moments_of_a_constant_sample_have_no_spread():
    lam = l_moments(np.full(10, 4.2), 3)
    assert lam[0] == pytest.approx(4.2)
    assert lam[1] == pytest.approx(0.0, abs=1e-12)
    assert lam[2] == pytest.approx(0.0, abs=1e-12)


def test_l_moments_only_return_what_was_asked_for():
    x = np.arange(1.0, 11.0)
    for count in (1, 2, 3, 4):
        assert l_moments(x, count).size == count
    # The lower moments must not change with how many were requested.
    assert l_moments(x, 1)[0] == pytest.approx(l_moments(x, 4)[0])
    assert l_moments(x, 2)[1] == pytest.approx(l_moments(x, 4)[1])


def test_l_moments_refuse_an_impossible_request():
    with pytest.raises(ValueError):
        l_moments([1.0, 2.0], 4)
    with pytest.raises(ValueError):
        l_moments([1.0, 2.0, 3.0], 5)


# ---------------------------------------------------------------------------
# Declustering
# ---------------------------------------------------------------------------


def test_decluster_keeps_one_peak_per_storm():
    x = np.array([0, 1, 5, 3, 6, 1, 0, 0, 0, 0, 0, 4, 2, 0])
    peaks, positions = decluster(x, threshold=2.0, separation=1)
    assert list(peaks) == [6.0, 4.0]
    assert list(positions) == [4, 11]


def test_decluster_separation_merges_nearby_exceedances():
    # Two exceedances two samples apart: one storm at separation 3.
    x = np.array([0, 5, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0])
    assert decluster(x, 2.0, separation=3)[0].size == 1
    assert decluster(x, 2.0, separation=1)[0].size == 2


def test_decluster_returns_nothing_when_nothing_exceeds():
    peaks, positions = decluster(np.zeros(20), threshold=1.0)
    assert peaks.size == 0 and positions.size == 0


def test_decluster_handles_a_storm_running_to_the_end():
    x = np.array([0.0, 0.0, 3.0, 9.0])
    peaks, positions = decluster(x, 1.0, separation=2)
    assert peaks == pytest.approx([9.0])
    assert positions[0] == 3


def test_decluster_rejects_a_zero_separation():
    with pytest.raises(ValueError):
        decluster([1.0, 2.0], 0.5, separation=0)


def test_peak_rate_counts_per_year():
    x = np.zeros(2920 * 4)
    x[[100, 1000, 2000, 3000]] = 9.0
    pot = peaks_over_threshold(x, 1.0, separation=1, samples_per_year=2920)
    assert pot["years"] == pytest.approx(4.0)
    assert pot["rate"] == pytest.approx(1.0)


def test_block_maxima_drops_an_incomplete_block():
    x = np.arange(25.0)
    maxima = block_maxima(x, block=10)
    assert list(maxima) == [9.0, 19.0]


def test_block_maxima_rejects_a_record_shorter_than_a_block():
    with pytest.raises(ValueError):
        block_maxima(np.arange(5.0), block=10)


# ---------------------------------------------------------------------------
# Fits, against known parameters
# ---------------------------------------------------------------------------


def test_gpd_recovers_an_exponential_tail():
    rng = np.random.default_rng(11)
    scale, shape = fit_gpd(gpd_sample(1.5, 0.0, 40000, rng))
    assert scale == pytest.approx(1.5, rel=0.03)
    assert shape == pytest.approx(0.0, abs=0.03)


def test_gpd_recovers_a_heavy_tail():
    rng = np.random.default_rng(12)
    scale, shape = fit_gpd(gpd_sample(2.0, 0.2, 60000, rng))
    assert scale == pytest.approx(2.0, rel=0.04)
    assert shape == pytest.approx(0.2, abs=0.03)


def test_gpd_recovers_a_bounded_tail():
    rng = np.random.default_rng(13)
    scale, shape = fit_gpd(gpd_sample(0.55, -0.12, 60000, rng))
    assert scale == pytest.approx(0.55, rel=0.04)
    assert shape == pytest.approx(-0.12, abs=0.03)


def test_gpd_is_unbiased_at_a_realistic_sample_size():
    """A 40-year wave record gives a few hundred peaks, not thousands."""
    rng = np.random.default_rng(14)
    shapes = [fit_gpd(gpd_sample(0.55, -0.08, 250, rng))[1] for _ in range(300)]
    assert np.mean(shapes) == pytest.approx(-0.08, abs=0.02)


def test_gpd_rejects_negative_excesses():
    with pytest.raises(ValueError):
        fit_gpd([-0.5, 1.0, 2.0])


def test_gpd_rejects_a_sample_with_no_spread():
    with pytest.raises(ValueError):
        fit_gpd(np.full(20, 2.0))


def test_gev_recovers_a_gumbel():
    rng = np.random.default_rng(15)
    loc, scale, shape = fit_gev(gev_sample(5.0, 2.0, 0.0, 40000, rng))
    assert loc == pytest.approx(5.0, abs=0.05)
    assert scale == pytest.approx(2.0, rel=0.03)
    assert shape == pytest.approx(0.0, abs=0.02)


def test_gev_recovers_a_bounded_shape():
    rng = np.random.default_rng(16)
    loc, scale, shape = fit_gev(gev_sample(5.0, 2.0, -0.15, 40000, rng))
    assert loc == pytest.approx(5.0, abs=0.08)
    assert scale == pytest.approx(2.0, rel=0.04)
    assert shape == pytest.approx(-0.15, abs=0.02)


def test_gev_needs_three_maxima():
    with pytest.raises(ValueError):
        fit_gev([1.0, 2.0])


# ---------------------------------------------------------------------------
# Return values
# ---------------------------------------------------------------------------


def test_gpd_return_value_matches_the_exponential_form():
    got = gpd_return_value(3.0, 1.5, 0.0, rate=5.0, return_period=100.0)
    assert float(got) == pytest.approx(3.0 + 1.5 * math.log(500.0))


def test_gpd_return_value_is_continuous_across_the_zero_shape_branch():
    kwargs = dict(threshold=2.0, scale=0.5, rate=4.0, return_period=50.0)
    near_zero = float(gpd_return_value(shape=1e-7, **kwargs))
    exactly_zero = float(gpd_return_value(shape=0.0, **kwargs))
    assert near_zero == pytest.approx(exactly_zero, rel=1e-5)


def test_gpd_return_value_rises_with_return_period():
    values = gpd_return_value(2.0, 0.6, -0.05, 6.0, [1.0, 10.0, 100.0, 1000.0])
    assert np.all(np.diff(values) > 0)


def test_gpd_bounded_tail_has_a_ceiling():
    """A negative shape has a finite upper limit, u + scale / |shape|."""
    ceiling = 2.0 + 0.6 / 0.15
    far = float(gpd_return_value(2.0, 0.6, -0.15, 6.0, 1e12))
    assert far < ceiling
    assert far == pytest.approx(ceiling, rel=0.01)


def test_gpd_return_value_validates_its_inputs():
    with pytest.raises(ValueError):
        gpd_return_value(2.0, -1.0, 0.0, 5.0, 100.0)
    with pytest.raises(ValueError):
        gpd_return_value(2.0, 1.0, 0.0, 0.0, 100.0)
    with pytest.raises(ValueError):
        gpd_return_value(2.0, 1.0, 0.0, 5.0, -10.0)


def test_gev_return_value_matches_the_gumbel_form():
    T = 100.0
    y = -math.log(-math.log(1.0 - 1.0 / T))
    assert float(gev_return_value(5.0, 2.0, 0.0, T)) == pytest.approx(5.0 + 2.0 * y)


def test_gev_return_value_rejects_a_sub_block_period():
    with pytest.raises(ValueError):
        gev_return_value(5.0, 2.0, 0.0, 0.5)


def test_gev_return_value_is_continuous_across_zero_shape():
    near = float(gev_return_value(5.0, 2.0, 1e-9, 100.0))
    exact = float(gev_return_value(5.0, 2.0, 0.0, 100.0))
    assert near == pytest.approx(exact, rel=1e-6)


# ---------------------------------------------------------------------------
# Whole fits
# ---------------------------------------------------------------------------


@pytest.fixture
def storm_record():
    """Forty years of three-hourly data with a known storm tail."""
    rng = np.random.default_rng(20260916)
    per_year, years = 2920, 40
    n = per_year * years
    record = 0.5 + 0.2 * rng.random(n)
    starts = np.arange(60, n - 60, 400)
    excess = gpd_sample(0.55, -0.08, starts.size, rng)
    for start, value in zip(starts, excess):
        record[start] = 2.5 + value
    return record, per_year, years


def test_pot_fit_recovers_the_planted_climate(storm_record):
    record, per_year, years = storm_record
    fit = fit_pot(record, 2.5, separation=24, samples_per_year=per_year,
                  bootstrap=0)
    assert fit.parameters["scale"] == pytest.approx(0.55, abs=0.12)
    assert fit.parameters["shape"] == pytest.approx(-0.08, abs=0.12)
    assert fit.years == pytest.approx(years)


def test_pot_confidence_band_brackets_the_estimate(storm_record):
    record, per_year, _ = storm_record
    fit = fit_pot(record, 2.5, separation=24, samples_per_year=per_year,
                  bootstrap=300, seed=2)
    band = fit.confidence(100.0, level=0.90)
    assert band["lower"][0] < band["central"][0] < band["upper"][0]


def test_wider_confidence_levels_give_wider_bands(storm_record):
    record, per_year, _ = storm_record
    fit = fit_pot(record, 2.5, separation=24, samples_per_year=per_year,
                  bootstrap=300, seed=3)
    narrow = fit.confidence(100.0, level=0.50)
    wide = fit.confidence(100.0, level=0.99)
    assert (wide["upper"][0] - wide["lower"][0]
            > narrow["upper"][0] - narrow["lower"][0])


def test_confidence_without_a_bootstrap_says_so(storm_record):
    record, per_year, _ = storm_record
    fit = fit_pot(record, 2.5, separation=24, samples_per_year=per_year,
                  bootstrap=0)
    with pytest.raises(RuntimeError):
        fit.confidence(100.0)


def test_confidence_level_is_validated(storm_record):
    record, per_year, _ = storm_record
    fit = fit_pot(record, 2.5, separation=24, samples_per_year=per_year,
                  bootstrap=50)
    with pytest.raises(ValueError):
        fit.confidence(100.0, level=1.5)


def test_pot_warns_about_a_thin_sample():
    n = 2920 * 40
    record = np.zeros(n)
    spikes = np.arange(100, n, 6000)
    record[spikes] = np.linspace(3.0, 4.0, spikes.size)
    fit = fit_pot(record, 3.5, separation=24, bootstrap=0)
    assert fit.data.size < 30
    assert any("peaks above the threshold" in w for w in fit.warnings)
    assert any("Peak rate" in w for w in fit.warnings)


def test_pot_refuses_a_threshold_nothing_reaches():
    with pytest.raises(ValueError):
        fit_pot(np.zeros(3000), threshold=5.0, bootstrap=0)


def test_pot_and_block_maxima_broadly_agree(storm_record):
    record, per_year, _ = storm_record
    pot = fit_pot(record, 2.5, separation=24, samples_per_year=per_year,
                  bootstrap=0)
    gev = fit_block_maxima(record, block=per_year, samples_per_year=per_year,
                           bootstrap=0)
    a = float(np.atleast_1d(pot.return_value(100.0))[0])
    b = float(np.atleast_1d(gev.return_value(100.0))[0])
    assert abs(a - b) < 0.25 * max(a, b)


def test_block_maxima_fit_has_unit_rate(storm_record):
    record, per_year, _ = storm_record
    gev = fit_block_maxima(record, block=per_year, samples_per_year=per_year,
                           bootstrap=0)
    assert gev.rate == 1.0
    assert gev.data.size == 40


def test_extrapolation_note_flags_reaching_past_the_record(storm_record):
    record, per_year, _ = storm_record
    fit = fit_pot(record, 2.5, separation=24, samples_per_year=per_year,
                  bootstrap=0)
    assert "Within" in fit.extrapolation_note(10.0)
    assert "times the" in fit.extrapolation_note(1000.0)


def test_summary_reports_the_return_values(storm_record):
    record, per_year, _ = storm_record
    fit = fit_pot(record, 2.5, separation=24, samples_per_year=per_year,
                  bootstrap=100)
    text = fit.summary(return_periods=(10, 100))
    assert "Threshold" in text
    assert "10 yr" in text and "100 yr" in text


# ---------------------------------------------------------------------------
# Diagnostics
# ---------------------------------------------------------------------------


def test_mean_residual_life_is_linear_for_an_exponential_tail():
    """For shape zero the mean excess is constant in the threshold."""
    rng = np.random.default_rng(21)
    x = gpd_sample(1.0, 0.0, 200000, rng)
    mrl = mean_residual_life(x, [0.5, 1.0, 1.5, 2.0])
    assert np.allclose(mrl["mean_excess"], 1.0, atol=0.05)


def test_mean_residual_life_rises_for_a_heavy_tail():
    rng = np.random.default_rng(22)
    x = gpd_sample(1.0, 0.25, 200000, rng)
    mrl = mean_residual_life(x, [0.5, 1.5, 3.0])
    assert np.all(np.diff(mrl["mean_excess"]) > 0)


def test_mean_residual_life_reports_nan_where_nothing_exceeds():
    mrl = mean_residual_life([1.0, 2.0, 3.0], [10.0])
    assert np.isnan(mrl["mean_excess"][0])
    assert mrl["count"][0] == 0


def test_threshold_stability_reports_the_modified_scale_it_promises():
    """modified_scale must be scale - shape * threshold, exactly."""
    rng = np.random.default_rng(23)
    n = 2920 * 60
    record = np.zeros(n)
    idx = np.arange(50, n - 50, 300)
    record[idx] = 2.0 + gpd_sample(0.6, 0.0, idx.size, rng)

    levels = [2.2, 2.4, 2.6, 2.8]
    stab = threshold_stability(record, levels, separation=24)
    for i, level in enumerate(levels):
        peaks, _ = decluster(record, level, 24)
        scale, shape = fit_gpd(peaks - level)
        assert stab["shape"][i] == pytest.approx(shape)
        assert stab["modified_scale"][i] == pytest.approx(scale - shape * level)
        assert stab["count"][i] == peaks.size


def test_threshold_stability_raw_scale_climbs_for_a_heavy_tail():
    """For a positive shape, sigma_u grows linearly with the threshold."""
    rng = np.random.default_rng(24)
    n = 2920 * 80
    record = np.zeros(n)
    idx = np.arange(50, n - 50, 120)
    record[idx] = 2.0 + gpd_sample(0.6, 0.25, idx.size, rng)

    levels = np.array([2.5, 3.5, 4.5, 5.5])
    scales = []
    for level in levels:
        peaks, _ = decluster(record, float(level), 24)
        scales.append(fit_gpd(peaks - level)[0])
    assert np.all(np.diff(scales) > 0)
    # The slope of sigma_u against u is the shape itself.
    slope = np.polyfit(levels, scales, 1)[0]
    assert slope == pytest.approx(0.25, abs=0.08)


def test_threshold_stability_skips_thresholds_with_too_few_peaks():
    record = np.zeros(2920 * 10)
    record[[100, 2000, 5000]] = 6.0
    stab = threshold_stability(record, [1.0, 9.0], separation=24)
    assert stab["count"][0] == 3
    assert np.isnan(stab["shape"][1])


def test_plotting_positions_are_ordered_and_span_the_sample():
    values = np.array([3.0, 1.0, 2.0, 5.0])
    pp = plotting_positions(values, rate=2.0)
    assert list(pp["values"]) == [1.0, 2.0, 3.0, 5.0]
    assert np.all(np.diff(pp["return_period"]) > 0)
    assert np.all(pp["exceedance"] > 0) and np.all(pp["exceedance"] < 1)


def test_plotting_positions_scale_with_the_peak_rate():
    values = np.arange(1.0, 11.0)
    slow = plotting_positions(values, rate=1.0)
    fast = plotting_positions(values, rate=5.0)
    assert np.allclose(slow["return_period"], 5.0 * fast["return_period"])


def test_plotting_positions_reject_an_empty_sample():
    with pytest.raises(ValueError):
        plotting_positions([])
