# Data-driven forecasting

`ml.forecasting` | Prediction of waves, levels, and morphology.

Parent: [Machine learning and data science](ml.md)

Papers: 3. Claims: 1. Equations: 0.

## Synthesis

**Well established.** Data-driven coastal forecasting maps recent observations and predicted forcing to future hazards or morphology; credible use requires temporal holdout validation, comparison with persistence and physics baselines, calibrated uncertainty and monitoring for regime shift.

**Governing physics.** Forecast skill is constrained by the physical memory and drivers represented in inputs: waves, water levels, storm duration, antecedent profile, tides and currents. Models may learn associations but do not by themselves establish sediment conservation or causal mechanisms.

**Dimensionless parameters.** Controls include forecast horizon relative to system memory, training length relative to climate variability, RMSE normalized by observed range or measurement error, skill relative to persistence, event imbalance, input lag, regularization strength, calibration error and out-of-distribution distance.

**Major equations.** Regression and neural forecasts approximate a conditional response y at lead time from lagged states and forcing; training minimizes losses such as mean-square error, while evaluation uses RMSE, bias, correlation and event or threshold scores. Probabilistic variants estimate quantiles or predictive distributions.

**Typical methods.** Workflows align quality-controlled forcing and response time series, prevent temporal leakage, split by events or years, engineer physically meaningful lags, tune only on training data, compare simple and physics-based baselines, test unseen extremes and sites, quantify uncertainty and archive reproducible preprocessing.

**Numerical models.** The reviewed branch centers on a multilinear event-erosion forecast with reported shoreline RMSE. Adjacent evidence includes a regularized nonlinear extreme-learning machine and physics-data hybrid concepts; model architecture alone is not evidence of operational value.

**Experimental datasets.** Reviewed primary evidence covers storm-event shoreline erosion at three monitored locations. Related graph evidence includes Iztuzu storm-duration and energy correlations and multi-sensor 2011 Tohoku waveform forecasting, but these do not directly validate the erosion model.

**Validated ranges.** The event-erosion RMSE of 3.7-6.4 m applies to three monitored locations and their tested events. Transfer to other beach states, storm climates, sensors, lead times or future climate requires independent validation.

**Recent advances.** Recent advances use transformers and graph networks, physics-informed and differentiable hybrids, probabilistic deep ensembles, conformal prediction, self-supervised coastal representation learning, online drift detection and operational model–data fusion.

**Disagreements.** Complex nonlinear learners can capture interactions but may not outperform transparent regression with limited events. Random splits inflate skill in autocorrelated data, while event-wise and future-period tests are stricter; lowest RMSE need not yield calibrated extremes or useful decisions.

**Limitations.** Small event samples, missing extremes, sensor changes, target uncertainty, leakage, nonstationarity, site dependence, unreported baselines, deterministic outputs and weak interpretability limit trust. Forecasts can fail when nourishment, morphology or forcing leaves the training distribution.

**Open questions.** Priorities include multi-site transfer, physics-constrained loss functions, calibrated event tails, adaptive updating, causal driver tests, missing-data robustness, forecast-value evaluation, standardized hindcasts and uncertainty triggers for human review or physics-model fallback.

**Seminal papers.** Autoregressive and transfer-function models established coastal time-series prediction; neural networks and support-vector methods expanded nonlinear mapping, followed by ensemble learning, recurrent networks and hybrid residual correction around numerical models.

## Claims

- **C121.** The multilinear event-erosion model reported shoreline-change RMSE between 3.7 and 6.4 m across the three monitored locations. *Regime: The paper's site-specific training/validation design for Narrabeen-Collaroy; split details require full text..* [direct_finding, mixed] (Ibaceta 2024, [doi:10.1016/j.coastaleng.2024.104596](https://doi.org/10.1016/j.coastaleng.2024.104596))

## Papers

- Evan B. Goldstein (2019). A review of machine learning applications to coastal sediment transport and morphodynamics. *Earth-Science Reviews*. [doi:10.1016/j.earscirev.2019.04.022](https://doi.org/10.1016/j.earscirev.2019.04.022) [preprint, read only](https://eartharxiv.org/repository/object/1247/download/2864/)
- M. A. Habib (2024). Efficient data-driven machine learning models for scour depth predictions at sloping sea defences. *Frontiers in Built Environment*. [doi:10.3389/fbuil.2024.1343398](https://doi.org/10.3389/fbuil.2024.1343398) [published version, CC BY](https://www.frontiersin.org/articles/10.3389/fbuil.2024.1343398/pdf)
- Ibaceta (2024). Data-driven modelling of coastal storm erosion for real-time forecasting at a wave-dominated embayed beach. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2024.104596](https://doi.org/10.1016/j.coastaleng.2024.104596) [published version, CC BY](https://api.elsevier.com/content/article/PII:S0378383924001443?httpAccept=text/xml)
