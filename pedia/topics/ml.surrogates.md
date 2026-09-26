# Surrogate and reduced-order models

`ml.surrogates` | Fast emulation of process models.

Parent: [Machine learning and data science](ml.md)

Papers: 5. Claims: 2. Equations: 1.

## Synthesis

**Well established.** Coastal surrogates replace repeated high-fidelity process-model runs with a learned input-output map. They can reduce forecast or ensemble cost dramatically, but inherit the training simulator's physics, biases, boundary conditions, and sampled parameter domain.

**Governing physics.** Physical fidelity enters through training labels and predictor design: tropical-cyclone track history controls surge, while winds, currents, ice and release conditions control spill transport. A surrogate learns these dependencies but does not independently conserve mass or momentum unless constrained.

**Dimensionless parameters.** There is no universal coastal-surrogate dimensionless group. Relevant physical nondimensionalization should retain storm size, speed and intensity ratios, depth and Froude controls, ice concentration, forecast horizon, spatial resolution, and response normalization; ML controls include sample count and error metrics.

**Major equations.** Common formulations minimize prediction loss between surrogate output and process-model fields or responses. Reviewed examples combine convolutional temporal encoding, PCA and clustering for spatial surge, and XGBoost or KNN regression for affected area and particle positions.

**Typical methods.** A defensible workflow defines an application domain, generates a designed physics-model ensemble, partitions training/validation/test cases without leakage, compresses outputs if needed, trains candidate emulators, evaluates held-out and historical cases, and tests extrapolation and uncertainty.

**Numerical models.** Process generators are high-fidelity storm-surge simulations and coupled GNOME-GLOFS spill transport. Surrogates include C1PKNet (1-D CNN plus PCA/k-means), XGBoost affected-area regression, and KNN particle-location prediction.

**Experimental datasets.** The reviewed evidence includes 1,031 Chesapeake Bay surge simulations plus observations from Hurricanes Isabel, Irene and Sandy, and 6,800 Straits of Mackinac GNOME-GLOFS spill simulations using 2023-2025 hydrodynamic-ice forcing.

**Validated ranges.** C1PKNet was evaluated for Chesapeake Bay landfalling and bypassing storms and three historical hurricanes. The spill surrogates cover a hypothetical Mackinac release, 3-24 h horizons and 2023-2025 ice/forcing, with R2=0.85-0.93 for area and 0.70-0.98 for particle location.

**Recent advances.** The 2026 ice-aware spill study extends coastal emulation from scalar peak hazard to affected-area and particle-distribution outputs, demonstrating rapid response prediction while quantifying strong seasonal control by ice cover.

**Disagreements.** High in-domain accuracy does not establish physical validity or extrapolation. A surrogate may outperform a chosen baseline while reproducing simulator bias; random data splits can overstate skill when storms, times, or spatial fields are correlated.

**Limitations.** Current extracted evidence covers only two application domains and relies primarily on synthetic labels. Rare extremes, changing bathymetry or climate, unseen release/track geometry, uncertain boundaries, distribution shift, wet-dry discontinuities, and spatial mass conservation require explicit testing.

**Open questions.** Priorities include physics- and conservation-aware architectures, calibrated predictive uncertainty, active learning, multifidelity training, interpretable failure detection, transfer among coastlines, real-time data assimilation, and benchmarks that separate interpolation from genuine extrapolation.

**Seminal papers.** Within this corpus, the 2021 Chesapeake Bay C1PKNet study establishes a track-time-series surge surrogate validated against both 1,031 simulations and historical hurricanes; it is the core coastal exemplar for regional response emulation.

## Equations

### Supervised coastal process-model surrogate

$$
\widehat{\mathbf{y}}=f_{\theta}(\mathbf{x});\quad \theta^*=\arg\min_{\theta}\mathcal{L}(f_{\theta}(\mathbf{x}),\mathbf{y}_{process})
$$

Regime: Straits of Mackinac training and test ensemble.

Variables: `x` initial spill and environmental predictor vector; `y_hat` surrogate affected area or particle-location output; `theta` trained XGBoost or KNN parameters; `y_process` GNOME-GLOFS ensemble output; `L` training loss; normalized learning formulation

Source: (Song 2026, [doi:10.1016/j.oceaneng.2026.125783](https://doi.org/10.1016/j.oceaneng.2026.125783))

## Claims

- **C289.** For 6,800 GNOME-GLOFS simulations of hypothetical Straits of Mackinac spills during 2023-2025, an XGBoost area surrogate achieved R2=0.85-0.93 and a k-nearest-neighbor particle-location surrogate achieved R2=0.70-0.98; dense February ice limited 24 h spread to 15 km2 versus an April maximum of 46 km2. *Regime: Hypothetical Straits of Mackinac spill; 6,800 GNOME-GLOFS simulations with 2023-2025 forcing and 3-24 h horizons..* [direct_finding, mixed] (Song 2026, [doi:10.1016/j.oceaneng.2026.125783](https://doi.org/10.1016/j.oceaneng.2026.125783))
- **C1655.** Wave-GAN, trained on CFD images, predicts three-dimensional nonlinear regular-wave loads and run-up on a fixed vertical cylinder for held-out wave conditions with CFD-comparable accuracy and seconds-scale inference, but remains bounded by its training domain. *Regime: Three-dimensional nonlinear regular waves interacting with the modeled fixed vertical cylinder over the trained and tested wave-condition range..* [direct_finding, numerical] (Blanca Peña 2021, [doi:10.1016/j.coastaleng.2021.103902](https://doi.org/10.1016/j.coastaleng.2021.103902))

## Papers

- Blanca Peña (2021). Wave-GAN: A deep learning approach for the prediction of nonlinear regular wave loads and run-up on a fixed cylinder. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2021.103902](https://doi.org/10.1016/j.coastaleng.2021.103902) [submitted manuscript, read only](https://discovery.ucl.ac.uk/10125729/1/Wave-GAN_CE_accepted%20manuscript.pdf)
- Song (2026). Efficient machine learning surrogate models for predicting oil spill transport with ice cover effects. *Ocean Engineering*. [doi:10.1016/j.oceaneng.2026.125783](https://doi.org/10.1016/j.oceaneng.2026.125783)
- Lee (2021). Rapid prediction of peak storm surge from tropical cyclone track time series using machine learning. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2021.104024](https://doi.org/10.1016/j.coastaleng.2021.104024) [published version, read only](https://api.elsevier.com/content/article/PII:S0378383921001691?httpAccept=text/xml)
- Pinton (2022). Estimating Ground Elevation in Coastal Dunes from High-Resolution UAV-LIDAR Point Clouds and Photogrammetry. *Remote Sensing*. [doi:10.3390/rs15010226](https://doi.org/10.3390/rs15010226) [published version, CC BY](https://www.mdpi.com/2072-4292/15/1/226/pdf)
- Bishop-Taylor (2026). Optimising coastal tide predictions: an ensemble satellite altimetry and optical remote sensing approach. *International Journal of Remote Sensing*. [doi:10.1080/01431161.2026.2666912](https://doi.org/10.1080/01431161.2026.2666912) [published version, CC BY](https://www.tandfonline.com/doi/pdf/10.1080/01431161.2026.2666912)
