# Machine learning and data science

`ml` | Data-driven coastal analysis and prediction.

Subtopics: [Feature detection and classification](ml.classification.md), [Data-driven forecasting](ml.forecasting.md), [Physics-informed machine learning](ml.physics.md), [Surrogate and reduced-order models](ml.surrogates.md)

Papers: 10. Claims: 7. Equations: 0.

## Synthesis

**Well established.** Coastal machine learning learns mappings from observations, simulations or hybrid evidence, but credible use requires a decision-defined target, traceable data, leakage-safe validation, strong baselines, physical and tail checks, calibrated uncertainty, transfer tests, interpretable diagnostics and operational monitoring.

**Governing physics.** Useful predictors encode waves, tides, surge, rainfall, winds, bathymetry, morphology, structures and antecedent state; conservation, causality, boundary conditions, temporal memory, spatial dependence and extremes constrain learned relationships even when not explicit in the architecture.

**Dimensionless parameters.** Relevant controls include training-to-feature ratio, event and site coverage, class imbalance, forecast lead-to-memory ratio, spatial resolution to process scale, extrapolation distance, signal-to-noise, missingness, calibration and sharpness, tail sample size, computational speedup, and physics-residual-to-data-loss weighting.

**Major equations.** Core formulations include empirical-risk loss with regularization, sequence and spatiotemporal mappings, ensemble aggregation, Gaussian or quantile predictive distributions, surrogate emulation, physics- or constraint-penalized loss, calibration scores, feature attribution and skill metrics against persistence, climatology and process models.

**Typical methods.** Methods curate and align observations or simulations, define features and targets, partition by event/site/time, train linear/tree/kernel/ensemble/deep models, tune without test leakage, compare baselines, diagnose features and errors, calibrate probabilities, test physics and extremes, quantify shift and deploy with monitoring.

**Numerical models.** Represented approaches include deep surge predictors, seq2seq LSTM flood surrogates, ensemble runup/erosion models, simulation-to-ML inundation emulators, scientific-knowledge-guided learning and model-agnostic feature explanations; process models provide training, constraints or benchmarks.

**Experimental datasets.** The reviewed evidence includes coastal surge time series, simulation-derived tidal–pluvial flood maps, wave-runup and dune-erosion observations, coastal-urban nuisance-flood sequences and environmental datasets used to illustrate model-agnostic explanation and scientific-knowledge integration.

**Validated ranges.** Evidence spans site-specific coastal water levels, compound street-scale flooding and beach runup/erosion, primarily hindcast or simulation-supported settings; transfer beyond sampled sites, event magnitudes, morphology, forcing statistics and sensor systems remains unproven without explicit tests.

**Recent advances.** Recent work uses sequence surrogates for real-time compound flooding, deep coastal surge models, ensembles for runup and erosion, scientific-knowledge integration, probabilistic prediction, model-agnostic explanation, simulation-informed learning and operationally oriented acceleration.

**Disagreements.** Higher aggregate accuracy can hide worse extreme or minority-regime performance; random splits overstate skill when events or locations leak; explanations can be unstable or noncausal; physics constraints may improve plausibility but introduce model-form bias; a fast surrogate may reproduce its simulator rather than reality.

**Limitations.** Coastal datasets are short, nonstationary, spatially clustered, missing during extremes and shaped by changing sensors and interventions; labels and simulator outputs contain error; rare tails are underrepresented; black-box dependence, distribution shift and false confidence impede safety-critical use.

**Open questions.** Priorities include cross-site and future-climate transfer, physics-conserving architectures, sparse-event and tail learning, causal and invariant representations, calibrated compound uncertainty, multimodal data fusion, trustworthy explanations, adaptive sensing, drift detection and auditable human–AI decisions.

**Seminal papers.** Early coastal data-driven work used regression, neural networks, classification and autoregressive models for waves, shorelines and morphology; ensembles, kernel methods and remote-sensing classifiers broadened nonlinear prediction before modern deep spatiotemporal and hybrid models.

## Claims

- **C1033.** A review argues that engineering and environmental machine learning should integrate scientific laws, constraints, simulations, and domain knowledge rather than rely on unconstrained pattern fitting. *Regime: Integrating Scientific Knowledge with Machine Learning for Engineering and Environmental Systems.* [literature_review_statement, review] (Jared Willard 2022, [doi:10.1145/3514228](https://doi.org/10.1145/3514228))
- **C1034.** Deep-learning experiments for coastal surge prediction show that data-driven models can learn sea-level response while remaining dependent on training coverage, predictors, lead time, and site regime. *Regime: Exploring deep learning capabilities for surge predictions in coastal areas.* [direct_finding, numerical] (Timothy Tiggeloven 2021, [doi:10.1038/s41598-021-96674-0](https://doi.org/10.1038/s41598-021-96674-0))
- **C1035.** A machine-learning surrogate predicts combined tidal and pluvial flood inundation at operational speed, transferring information from computational simulations into street-scale coastal-flood estimates. *Regime: Predicting combined tidal and pluvial flood inundation using a machine learning surrogate model.* [direct_finding, numerical] (Faria Tuz Zahura 2022, [doi:10.1016/j.ejrh.2022.101087](https://doi.org/10.1016/j.ejrh.2022.101087))
- **C1036.** An ensemble machine-learning analysis of wave runup and coastal dune erosion demonstrates that combining learners can characterize nonlinear response while exposing data and extrapolation limits. *Regime: Ensemble models from machine learning: an example of wave runup and coastal dune erosion.* [direct_finding, mixed] (Tomas Beuzen 2019, [doi:10.5194/nhess-19-2295-2019](https://doi.org/10.5194/nhess-19-2295-2019))
- **C1037.** An environmental-data example shows how model-agnostic explanations can diagnose feature influence in otherwise opaque predictors, while explanation is not a substitute for uncertainty or causal validation. *Regime: An illustration of model agnostic explainability methods applied to environmental data.* [direct_finding, analytical] (Christopher K. Wikle 2022, [doi:10.1002/env.2772](https://doi.org/10.1002/env.2772))
- **C1038.** A sequence-to-sequence LSTM surrogate provides multi-step street-scale nuisance-flood forecasts for a coastal-urban system under joint rain and tide forcing. *Regime: Forecasting Multi-Step-Ahead Street-Scale Nuisance Flooding using a seq2seq LSTM Surrogate Model for Real-Time Application in a Coastal-Urban City.* [direct_finding, numerical] (Binata Roy 2025, [doi:10.1016/j.jhydrol.2025.132697](https://doi.org/10.1016/j.jhydrol.2025.132697))
- **C1641.** A review of machine learning in coastal sediment transport and morphodynamics finds applications from grain-scale flux to bars, shorelines and overwash, with value in nonlinear regression, emulation, prediction and explicit uncertainty, but recommends transparent train-test separation, baselines, uncertainty and physically informed interpretation. *Regime: Published coastal sediment-transport and morphodynamic ML applications available to the review..* [literature_review_statement, review] (Evan B. Goldstein 2019, [doi:10.1016/j.earscirev.2019.04.022](https://doi.org/10.1016/j.earscirev.2019.04.022))

## Papers

- Jared Willard (2022). Integrating Scientific Knowledge with Machine Learning for Engineering and Environmental Systems. *ACM Computing Surveys*. [doi:10.1145/3514228](https://doi.org/10.1145/3514228)
- Evan B. Goldstein (2019). A review of machine learning applications to coastal sediment transport and morphodynamics. *Earth-Science Reviews*. [doi:10.1016/j.earscirev.2019.04.022](https://doi.org/10.1016/j.earscirev.2019.04.022)
- Timothy Tiggeloven (2021). Exploring deep learning capabilities for surge predictions in coastal areas. *Scientific Reports*. [doi:10.1038/s41598-021-96674-0](https://doi.org/10.1038/s41598-021-96674-0)
- Faria Tuz Zahura (2022). Predicting combined tidal and pluvial flood inundation using a machine learning surrogate model. *Journal of Hydrology Regional Studies*. [doi:10.1016/j.ejrh.2022.101087](https://doi.org/10.1016/j.ejrh.2022.101087)
- Tomas Beuzen (2019). Ensemble models from machine learning: an example of wave runup and coastal dune erosion. *Natural hazards and earth system sciences*. [doi:10.5194/nhess-19-2295-2019](https://doi.org/10.5194/nhess-19-2295-2019)
- Christopher K. Wikle (2022). An illustration of model agnostic explainability methods applied to environmental data. *Environmetrics*. [doi:10.1002/env.2772](https://doi.org/10.1002/env.2772)
- Binata Roy (2025). Forecasting Multi-Step-Ahead Street-Scale Nuisance Flooding using a seq2seq LSTM Surrogate Model for Real-Time Application in a Coastal-Urban City. *Journal of Hydrology*. [doi:10.1016/j.jhydrol.2025.132697](https://doi.org/10.1016/j.jhydrol.2025.132697)
- Emma McAllister (2022). Multispectral satellite imagery and machine learning for the extraction of shoreline indicators. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2022.104102](https://doi.org/10.1016/j.coastaleng.2022.104102)
- Liu (2024). ANN-Based Filtering of Drone LiDAR in Coastal Salt Marshes Using Spatial–Spectral Features. *Remote Sensing*. [doi:10.3390/rs16183373](https://doi.org/10.3390/rs16183373)
- Herkül (2024). Mapping Shallow Water Coastal Habitats Using Optical Remote Sensing and Machine Learning: Evaluating Drone, Airplane, and Satellite-Based Imagery. *Journal of Coastal Research*. [doi:10.2112/jcr-si113-102.1](https://doi.org/10.2112/jcr-si113-102.1)
