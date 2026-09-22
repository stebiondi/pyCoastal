# Sensitivity analysis

`uncertainty.sensitivity` | Attribution of response variability.

Parent: [Reliability and uncertainty](uncertainty.md)

Papers: 11. Claims: 11. Equations: 0.

## Synthesis

**Well established.** Sensitivity analysis ranks how uncertain inputs, interactions, configurations, and scenarios influence a defined model output. Rankings are conditional on input ranges, dependence, site, output metric, model structure, and time horizon.

**Governing physics.** Influential controls span boundary forcing, sea level, surge and waves, topography, solver and grid, friction, breaches, damage functions, vegetation geometry, sediment pathways, structural geometry, and coupled atmosphere-ocean initial conditions.

**Dimensionless parameters.** Sensitivity is summarized by normalized derivatives, variance fractions, total-effect indices, interaction contributions, confidence bounds, surrogate error, and sometimes decision-specific value of information rather than a universal physical dimensionless group.

**Major equations.** Common tools include local derivatives, one-at-a-time screening, variance decomposition with first-order and total Sobol indices, polynomial chaos, response surfaces, Gaussian processes, factor mapping, Monte Carlo sampling, and interaction indices.

**Typical methods.** Good workflows define input distributions and dependence, sample the model, build or validate emulators, test convergence, compute main and interaction effects, repeat for multiple outputs and horizons, and confirm recommendations against observations or held-out simulations.

**Numerical models.** Models include shoreline projections, flood-damage Monte Carlo approximations, marine-flood occurrence models, COAWST vegetation, LISFLOOD-FP, UWIN-CM with polynomial chaos, Gaussian-process overtopping surrogates, and a barrier evolution model.

**Experimental datasets.** Reviewed evidence includes four French beaches, three Netherlands breach sites, a Mediterranean city, 17 European coastal sites with 72 configurations each, COAWST vegetation cases, Hurricane Earl ensembles, 163 overtopping tests, and an end-century barrier model.

**Validated ranges.** Reported effects include 20-40% shoreline variance from erosion-model choice, greater-than-fourfold 95% flood-damage bounds around the median, 17-site regional configuration patterns, and overtopping validation against 163 tests.

**Recent advances.** Recent studies combine global sensitivity with Gaussian processes, polynomial chaos, regional clustering, factor mapping, and efficient quadratures to expose interactions while reducing expensive coastal-model evaluations.

**Disagreements.** No parameter is universally dominant: surge, sea-level variability, and SLR scenarios dominate at different horizons; solvers, boundaries, and resolution dominate different European regions; friction may be secondary globally yet important locally.

**Limitations.** Rankings can be distorted by arbitrary input ranges, independence assumptions, inadequate sample size, surrogate bias, output aggregation, omitted structural error, nonstationarity, and lack of observational validation.

**Open questions.** Needs include dependent-input sensitivity, structural and scenario uncertainty, multi-output decision sensitivity, nonstationary rankings, efficient high-dimensional sampling, and robust transfer across sites.

**Seminal papers.** The branch builds on derivative screening, Monte Carlo uncertainty analysis, Sobol variance decomposition, polynomial-chaos expansions, and emulator-based global sensitivity; the reviewed sources demonstrate coastal uses.

## Claims

- **C392.** For four contrasting sandy beaches in southwest France, the choice between two sea-level-rise erosion models accounted for 20-40% of projected shoreline-change variance by 2100 and beyond. *Regime: Four minimally managed sandy beaches in southwest France, projected to 2100 and beyond..* [direct_finding, numerical] (Gonéri Le Cozannet 2019, [doi:10.1038/s41598-018-37017-4](https://doi.org/10.1038/s41598-018-37017-4))
- **C393.** Across three western Netherlands breach sites, the 95% flood-damage range extended more than fourfold below and above the median; depth-damage curves were most influential, while damage-model and inflow-volume parameter groups contributed about equally. *Regime: Three breach locations on the western Netherlands coast with 12 uncertain surge, breach-growth, and damage inputs..* [direct_finding, numerical] (Hans de Moel 2012, [doi:10.5194/nhess-12-1045-2012](https://doi.org/10.5194/nhess-12-1045-2012))
- **C394.** For the studied northwestern Mediterranean site, dominant marine-flood uncertainty shifted over time from storm-surge propagation to sea-level variability and later global sea-level-rise scenarios, so sensitivity-based research priorities depended on the planning horizon. *Regime: Low-lying northwestern Mediterranean urban site over the twenty-first century..* [direct_finding, numerical] (Gonéri Le Cozannet 2015, [doi:10.1016/j.envsoft.2015.07.021](https://doi.org/10.1016/j.envsoft.2015.07.021))
- **C395.** Sobol analysis of the COAWST vegetation module found kinetic energy, turbulence, and water level most sensitive to stem density and height, with diameter secondary, while wave dissipation depended primarily on stem density. *Regime: COAWST submerged-aquatic-vegetation module varying stem density, height, and diameter..* [direct_finding, numerical] (Tarandeep S. Kalra 2017, [doi:10.5194/gmd-10-4511-2017](https://doi.org/10.5194/gmd-10-4511-2017))
- **C396.** Across 17 European coastal test cases and 72 configurations per case, both sensitivity methods found floodplain solver dominance on Atlantic coasts, boundary-condition dominance on Mediterranean coasts, strong grid-resolution effects in North and Baltic seas, and generally smaller friction influence. *Regime: Seventeen European coastal sites spanning Atlantic, Mediterranean, North Sea, and Baltic conditions..* [direct_finding, numerical] (Marine Le Gal 2024, [doi:10.1016/j.coastaleng.2024.104541](https://doi.org/10.1016/j.coastaleng.2024.104541))
- **C397.** In Hurricane Earl coupled ensembles, rapid intensification was most sensitive to initial azimuthal-mean maximum wind and asymmetry orientation, whereas stochastic kinetic-energy backscatter influenced storm tracks more than initial-condition perturbations alone. *Regime: Hurricane Earl (2010) perturbations in strength, size, asymmetry, and stochastic backscatter..* [direct_finding, numerical] (Guotu Li 2018, [doi:10.1175/mwr-d-17-0371.1](https://doi.org/10.1175/mwr-d-17-0371.1))
- **C398.** Using 163 laboratory and field-scale overtopping tests, Gaussian-process surrogates supported probabilistic input sensitivity and predicted mean overtopping discharge more accurately than the regression formulae used for comparison. *Regime: A homogeneous dataset of 163 laboratory and field-scale coastal-defense tests..* [direct_finding, numerical] (Paul F. Kent 2024, [doi:10.3390/su16209110](https://doi.org/10.3390/su16209110))
- **C399.** Global sensitivity analysis of an end-century barrier model found narrow and low-relief initial geometries most vulnerable to width and height drowning, with toe depth, sea-level-rise rate, backbarrier shear stress, and inlet-delivered sediment creating strong interacting controls. *Regime: Barrier-backbarrier evolution through end-century across geometry, SLR, sediment, and marsh parameters..* [direct_finding, numerical] (Steven Hoagland 2024, [doi:10.1016/j.geomorph.2024.109087](https://doi.org/10.1016/j.geomorph.2024.109087))
- **C1613.** Probabilistic sediment-budget modeling found a detectable Bruun-rule erosion signal by mid-century for RCP4.5, 6.0 and 8.5 on idealized gently sloping undefended beaches, while RCP2.6 did not clearly separate from other uncertain drivers. *Regime: Wave-exposed, gently sloping sandy coasts without defenses, evaluated with the paper's probabilistic sediment-budget and RCP assumptions..* [direct_finding, numerical] (Gonéri Le Cozannet 2016, [doi:10.3389/fmars.2016.00049](https://doi.org/10.3389/fmars.2016.00049))
- **C1659.** European-scale Bruun-rule projections show that sandy-beach location and spatially varying nearshore-slope datasets can contribute uncertainty comparable to sea-level scenarios, especially before mid-century, and materially shift estimated retreat hotspots and coastal land loss. *Regime: European sandy coastlines under RCP4.5 and RCP8.5 sea-level rise from a 2010 baseline to 2100, absent ambient shoreline change..* [direct_finding, numerical] (Panagiotis Athanasiou 2020, [doi:10.1038/s41598-020-68576-0](https://doi.org/10.1038/s41598-020-68576-0))
- **C1702.** For unstructured-grid SWAN near the Saint Petersburg flood barrier, uncertainty is proportionally greatest for Hs below 0.3 m but about 5-10% for operationally significant waves; wind direction dominates sensitivity, followed by wind speed, bathymetry, water level and breaker index. *Regime: SWAN hindcast/forecast points near the Saint Petersburg Flood Prevention Facility on the documented unstructured Baltic grid..* [direct_finding, numerical] (Anna Nikishova 2017, [doi:10.1016/j.envsoft.2017.06.030](https://doi.org/10.1016/j.envsoft.2017.06.030))

## Papers

- Gonéri Le Cozannet (2019). Quantifying uncertainties of sandy shoreline change projections as sea level rises. *Scientific Reports*. [doi:10.1038/s41598-018-37017-4](https://doi.org/10.1038/s41598-018-37017-4)
- Hans de Moel (2012). Uncertainty and sensitivity analysis of coastal flood damage estimates in the west of the Netherlands. *Natural hazards and earth system sciences*. [doi:10.5194/nhess-12-1045-2012](https://doi.org/10.5194/nhess-12-1045-2012)
- Panagiotis Athanasiou (2020). Uncertainties in projections of sandy beach erosion due to sea level rise: an analysis at the European scale. *Scientific Reports*. [doi:10.1038/s41598-020-68576-0](https://doi.org/10.1038/s41598-020-68576-0)
- Gonéri Le Cozannet (2015). Evaluating uncertainties of future marine flooding occurrence as sea-level rises. *Environmental Modelling & Software*. [doi:10.1016/j.envsoft.2015.07.021](https://doi.org/10.1016/j.envsoft.2015.07.021)
- Gonéri Le Cozannet (2016). Uncertainties in Sandy Shorelines Evolution under the Bruun Rule Assumption. *Frontiers in Marine Science*. [doi:10.3389/fmars.2016.00049](https://doi.org/10.3389/fmars.2016.00049)
- Tarandeep S. Kalra (2017). Sensitivity analysis of a coupled hydrodynamic-vegetation model using the effectively subsampled quadratures method (ESQM v5.2). *Geoscientific model development*. [doi:10.5194/gmd-10-4511-2017](https://doi.org/10.5194/gmd-10-4511-2017)
- Anna Nikishova (2017). Uncertainty quantification and sensitivity analysis applied to the wind wave model SWAN. *Environmental Modelling & Software*. [doi:10.1016/j.envsoft.2017.06.030](https://doi.org/10.1016/j.envsoft.2017.06.030)
- Marine Le Gal (2024). Influence of model configuration for coastal flooding across Europe. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2024.104541](https://doi.org/10.1016/j.coastaleng.2024.104541)
- Guotu Li (2018). Uncertainty Propagation in Coupled Atmosphere–Wave–Ocean Prediction System: A Study of Hurricane Earl (2010). *Monthly Weather Review*. [doi:10.1175/mwr-d-17-0371.1](https://doi.org/10.1175/mwr-d-17-0371.1)
- Paul F. Kent (2024). Resilient Coastal Protection Infrastructures: Probabilistic Sensitivity Analysis of Wave Overtopping Using Gaussian Process Surrogate Models. *Sustainability*. [doi:10.3390/su16209110](https://doi.org/10.3390/su16209110)
- Steven Hoagland (2024). Morphodynamic and modeling insights from global sensitivity analysis of a barrier island evolution model. *Geomorphology*. [doi:10.1016/j.geomorph.2024.109087](https://doi.org/10.1016/j.geomorph.2024.109087)
