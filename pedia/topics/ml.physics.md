# Physics-informed machine learning

`ml.physics` | Learning constrained by governing physics.

Parent: [Machine learning and data science](ml.md)

Papers: 11. Claims: 11. Equations: 0.

## Synthesis

**Well established.** Physics-informed learning embeds governing equations, differentiable solvers, reduced physics, or process-model output into model architecture, loss, training data, or parameter inversion rather than relying on correlations alone.

**Governing physics.** Accessible coastal examples constrain learning with shallow-water mass and momentum, nonlinear Schrödinger wave evolution, sediment transport, SST space-time PDEs, and low/high-fidelity XBeach dynamics.

**Dimensionless parameters.** Relevant controls are equation-residual weights, data-to-physics loss balance, spatial and temporal sampling, fidelity ratio, flow and wave regime, roughness, spectral bandwidth, and extrapolation distance; reported abstracts do not establish universal ranges.

**Major equations.** Common mechanisms are PDE-residual penalties, automatic differentiation through governing solvers, universal differential equations, reduced bases, and learned mappings from lower- to higher-fidelity process solutions.

**Typical methods.** Methods include PINNs, finite-difference PINNs, physics-guided CNNs/GANs, attention and recurrent networks, differentiable solvers, reduced-basis surrogates, parameter identification, and physics-constrained data assimilation.

**Numerical models.** Physics backbones include shallow-water solvers, XBeach Surfbeat and nonhydrostatic modes, NLSE wave dynamics, sediment equations, finite-difference residuals, and differentiable universal SWE implementations.

**Experimental datasets.** The branch uses numerical wave tanks, circular-basin tests, XBeach runup pairs, CFD/finite-element mangrove simulations, daily SST, a real river reach, and Hurricane Irene river-ocean flooding; independent coastal field validation is sparse.

**Validated ranges.** Reported results include sub-centimetre basin fluctuations, about 6.5-fold FD-PINN acceleration, mangrove RMSE near 10^-2 for elevation/velocity and 10^-3 for sediment, fivefold shorter training than FE, and second-scale inference; these are case-specific.

**Recent advances.** Recent coastal work combines finite-difference residuals, causal weighting, attention/recurrent models, differentiable SWE backbones, learned physical parameters, process-model fidelity transfer, and explicit comparison against data-only models.

**Disagreements.** Physics constraints do not automatically dominate data-driven models: in compound flooding FD-PINN improved vanilla PINN, yet CNN-LSTM gave the best overall data-driven balance, and fixed NLSE coefficients sometimes degraded wave reconstruction when assumptions failed.

**Limitations.** Evidence is dominated by simulation-trained and case-specific studies. Sparse field tests, inconsistent baselines, loss-weight sensitivity, optimization difficulty, discontinuities, imperfect equations, uncertainty calibration, and computational accounting limit general claims.

**Open questions.** Priorities are conservation under extrapolation, noisy and sparse observations, multi-fidelity bias, discontinuities and wetting/drying, uncertainty, interpretable learned closures, transfer across storms and sites, and reproducible operational benchmarks.

**Seminal papers.** This branch connects PINN residual minimization, reduced-order and universal differential equations, differentiable programming, data assimilation, and multi-fidelity surrogate learning to coastal applications.

## Claims

- **C532.** Physics-informed machine learning integrates prior physical knowledge with data-driven models to address data scarcity, generalization, and physical plausibility. *Regime: cross-domain PIML literature.* [literature_review_statement, review] (Meng 2025, [doi:10.1007/s44379-025-00016-0](https://doi.org/10.1007/s44379-025-00016-0))
- **C533.** Storm-surge ML literature identifies hybrid physics-data models as a route toward more trustworthy forecasting while retaining explicit limitations and evaluation needs. *Regime: storm-surge prediction and coastal oceanography.* [literature_review_statement, review] (Yue Qin 2023, [doi:10.3390/jmse11091729](https://doi.org/10.3390/jmse11091729))
- **C534.** Physics-based reduced-basis learning produced precise and interpretable surrogates in three PDE-governed geoscience examples, offering transferable methodological evidence rather than direct coastal validation. *Regime: PDE-governed geothermal, geodynamic, and hydrologic systems.* [literature_review_statement, review] (Denise Degen 2023, [doi:10.5194/gmd-16-7375-2023](https://doi.org/10.5194/gmd-16-7375-2023))
- **C535.** A space-time PDE-guided neural network outperformed finite-difference and several learning baselines for daily sea-surface-temperature prediction. *Regime: daily sea-surface-temperature prediction.* [direct_finding, numerical] (Taikang Yuan 2023, [doi:10.3390/rs15143498](https://doi.org/10.3390/rs15143498))
- **C536.** An attention/LSTM-enhanced shallow-water PINN improved discontinuity capture and reduced nonphysical oscillations relative to a classical PINN in 1-D and 2-D simulations. *Regime: one- and two-dimensional shallow-water equations.* [direct_finding, numerical] (Yanling Li 2024, [doi:10.3390/sym16101376](https://doi.org/10.3390/sym16101376))
- **C537.** A conditional GAN used lower-cost XBeach Surfbeat output as physical information to reconstruct higher-fidelity nonhydrostatic time-dependent wave runup. *Regime: time-dependent coastal wave runup.* [direct_finding, numerical] (Saeed Saviz Naeini 2024, [doi:10.1016/j.oceaneng.2024.116986](https://doi.org/10.1016/j.oceaneng.2024.116986))
- **C538.** A polar-coordinate shallow-water PINN reproduced nonstationary wind-driven basin motions and sub-centimetre water-level fluctuations from limited sparse data. *Regime: nonstationary wind-driven motion in a circular basin with sub-centimetre fluctuations.* [direct_finding, numerical] (Zaiyang Zhou 2025, [doi:10.1029/2024wr037490](https://doi.org/10.1029/2024wr037490))
- **C539.** A mangrove hybrid PINN constrained by shallow-water and sediment equations achieved reported RMSE near 10^-2 for elevation/velocity and 10^-3 for sediment, with fivefold shorter training than the FE benchmark and second-scale inference. *Regime: Sundarbans mangrove hydro-morphodynamics.* [direct_finding, numerical] (Majdi Fanous 2025, [doi:10.1016/j.ecoinf.2025.103302](https://doi.org/10.1016/j.ecoinf.2025.103302))
- **C540.** An NLSE-constrained PINN reconstructed wave fields between sparse gauges, while trainable frequency and wavenumber improved reconstructions when fixed narrow-band coefficients were inadequate. *Regime: sparse deep-water gravity-wave elevation time series in a numerical tank.* [direct_finding, numerical] (Svenja Ehlers 2024, [doi:10.3390/fluids9100231](https://doi.org/10.3390/fluids9100231))
- **C541.** A differentiable shallow-water solver coupled to a neural network supported gradient-based roughness inversion and physics discovery without surrogate pretraining. *Regime: forward, inverse, and real-river flow-resistance modelling.* [direct_finding, mixed] (Liu 2025, [doi:10.1029/2025wr040265](https://doi.org/10.1029/2025wr040265))
- **C542.** For Hurricane Irene river-ocean compound flooding, a finite-difference PINN accelerated vanilla PINN by about 6.5 times while improving accuracy, whereas CNN-LSTM offered the best overall data-driven balance. *Regime: Hurricane Irene compound flooding on a realistic river-ocean interface domain.* [direct_finding, numerical] (Dongyu Feng 2025, [doi:10.1029/2025jh000758](https://doi.org/10.1029/2025jh000758))

## Papers

- Meng (2025). When physics meets machine learning: a survey of physics-informed machine learning. *Machine Learning for Computational Science and Engineering*. [doi:10.1007/s44379-025-00016-0](https://doi.org/10.1007/s44379-025-00016-0) [published version, CC BY](https://link.springer.com/content/pdf/10.1007/s44379-025-00016-0.pdf)
- Yue Qin (2023). A Review of Application of Machine Learning in Storm Surge Problems. *Journal of Marine Science and Engineering*. [doi:10.3390/jmse11091729](https://doi.org/10.3390/jmse11091729) [published version, CC BY](https://www.mdpi.com/2077-1312/11/9/1729/pdf?version=1693565343)
- Denise Degen (2023). Perspectives of physics-based machine learning strategies for geoscientific applications governed by partial differential equations. *Geoscientific model development*. [doi:10.5194/gmd-16-7375-2023](https://doi.org/10.5194/gmd-16-7375-2023) [published version, CC BY](https://gmd.copernicus.org/articles/16/7375/2023/gmd-16-7375-2023.pdf)
- Taikang Yuan (2023). A Space-Time Partial Differential Equation Based Physics-Guided Neural Network for Sea Surface Temperature Prediction. *Remote Sensing*. [doi:10.3390/rs15143498](https://doi.org/10.3390/rs15143498) [published version, CC BY](https://www.mdpi.com/2072-4292/15/14/3498/pdf?version=1689124301)
- Yanling Li (2024). An Improved PINN Algorithm for Shallow Water Equations Driven by Deep Learning. *Symmetry*. [doi:10.3390/sym16101376](https://doi.org/10.3390/sym16101376) [published version, CC BY](https://www.mdpi.com/2073-8994/16/10/1376/pdf?version=1729058275)
- Saeed Saviz Naeini (2024). A physics-informed machine learning model for time-dependent wave runup prediction. *Ocean Engineering*. [doi:10.1016/j.oceaneng.2024.116986](https://doi.org/10.1016/j.oceaneng.2024.116986) [published version, CC BY-NC-ND](https://espace2.etsmtl.ca/id/eprint/28402/1/Snaiki-R-2024-28402.pdf)
- Zaiyang Zhou (2025). Modeling Non‐Stationary Wind‐Induced Fluid Motions With Physics‐Informed Neural Networks for the Shallow Water Equations in a Polar Coordinate System. *Water Resources Research*. [doi:10.1029/2024wr037490](https://doi.org/10.1029/2024wr037490) [published version, CC BY](https://onlinelibrary.wiley.com/doi/pdfdirect/10.1029/2024WR037490)
- Majdi Fanous (2025). Leveraging physics-informed neural networks for efficient modelling of coastal ecosystems dynamics: A case study of Sundarbans mangrove forest. *Ecological Informatics*. [doi:10.1016/j.ecoinf.2025.103302](https://doi.org/10.1016/j.ecoinf.2025.103302) [published version, CC BY-NC](https://api.elsevier.com/content/article/PII:S1574954125003115?httpAccept=text/xml)
- Svenja Ehlers (2024). Data Assimilation and Parameter Identification for Water Waves Using the Nonlinear Schrödinger Equation and Physics-Informed Neural Networks. *Fluids*. [doi:10.3390/fluids9100231](https://doi.org/10.3390/fluids9100231) [published version, CC BY](https://www.mdpi.com/2311-5521/9/10/231/pdf)
- Liu (2025). Scientific Machine Learning of Flow Resistance Using Universal Shallow Water Equations With Differentiable Programming. *Water Resources Research*. [doi:10.1029/2025wr040265](https://doi.org/10.1029/2025wr040265) [published version, CC BY-NC](https://onlinelibrary.wiley.com/doi/pdfdirect/10.1029/2025WR040265)
- Dongyu Feng (2025). A Comparative Study of Physics‐Informed and Data‐Driven Neural Networks for Compound Flood Simulation at River‐Ocean Interfaces: A Case Study of Hurricane Irene. *Journal of Geophysical Research Machine Learning and Computation*. [doi:10.1029/2025jh000758](https://doi.org/10.1029/2025jh000758) [published version, CC BY-NC](https://onlinelibrary.wiley.com/doi/pdfdirect/10.1029/2025JH000758)
