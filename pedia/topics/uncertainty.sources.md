# Aleatory and epistemic uncertainty

`uncertainty.sources` | Variability and knowledge uncertainty.

Parent: [Reliability and uncertainty](uncertainty.md)

Papers: 13. Claims: 10. Equations: 0.

Used by pyCoastal design modules: Design conditions.

## Synthesis

**Well established.** Aleatory uncertainty represents variability treated as irreducible at the analysis scale, whereas epistemic uncertainty arises from limited knowledge, data, models, scenarios, or assumptions and may be reducible. Semantic and ontological ambiguity can add further uncertainty.

**Governing physics.** Coastal risk uncertainty propagates through hazard sources and forcing, hydrodynamics, topography and defenses, exposure, vulnerability, damage, socioeconomic pathways, adaptation behavior, dependence, and decision models.

**Dimensionless parameters.** Unlike hydrodynamic similarity, uncertainty-source analysis is organized by variance contribution, bias factor, probability weight, confidence/credibility, return period, scenario horizon, dependence strength, and value of information.

**Major equations.** Common frameworks use conditional probability, total-probability integration, hazard curves, logic or condition trees, Bayesian updating, ensembles, sensitivity decomposition, interval or imprecise probability, and value-of-information metrics.

**Typical methods.** Methods include source taxonomies, logic trees, expert elicitation, multi-model ensembles, global sensitivity analysis, Bayesian calibration, database integration, hindcast validation, scenario analysis, robust decisions, and explicit assumption audits.

**Numerical models.** Relevant systems include probabilistic tsunami hazard models, compound hydrometeorological-hydrodynamic chains, catastrophe hazard-exposure-vulnerability models, coastal flood risk models, and depth-damage calculations.

**Experimental datasets.** Reviewed cases span global tsunami hazard, global-to-regional coastal flood risk, compound floods, Florida hurricane losses, multi-hazard reviews, and component-wise flood-damage uncertainty.

**Validated ranges.** Reported magnitudes include coastal-risk overestimation to factor 1300 when adaptation is omitted, adaptation uncertainty to factor 27, absolute flood-damage uncertainty of factor 5-6, and roughly factor-two contributions from asset values and depth-damage curves in one case.

**Recent advances.** Recent work quantifies adaptation as a dominant coastal-risk uncertainty, integrates multi-source tsunami hazard, traces cascades through compound-flood forecasts, and reduces vulnerability-model uncertainty through linked administrative and insurance data.

**Disagreements.** Treating epistemic uncertainty as if it were aleatory can simplify computation but understate plausible variability and conceal conditional assumptions. Conversely, not every uncertainty can be reduced economically, so value-of-information and decision relevance matter.

**Limitations.** Taxonomy boundaries depend on analysis scale; probabilities for rare events and deep uncertainty may be weakly identified. Dependence, nonstationarity, model discrepancy, adaptation feedback, data quality, and unmodeled processes often remain incomplete.

**Open questions.** Needs include coherent treatment of deep uncertainty and dependence, dynamic adaptation, open defense and vulnerability data, compound-event propagation, transparent expert weighting, and decision validation under surprise.

**Seminal papers.** The branch builds on the classical aleatory-epistemic distinction, conditional risk analysis, Bayesian and logic-tree hazard methods, and formal sensitivity and decision analysis; this slice emphasizes their coastal consequences.

## Claims

- **C384.** A hydrological uncertainty synthesis distinguishes aleatory, epistemic, semantic, and ontological uncertainty and proposes condition trees to expose assumptions and provide decision makers with an auditable evidence trail. *Regime: Hydrological analysis and prediction under multiple uncertainty forms and nonstationarity..* [literature_review_statement, review] (Keith Beven 2015, [doi:10.1080/02626667.2015.1031761](https://doi.org/10.1080/02626667.2015.1031761))
- **C385.** Probabilistic tsunami hazard analysis requires an integrated treatment of multiple source mechanisms, their relative intensities and occurrence rates, propagation and impact models, and associated aleatory and epistemic uncertainties to produce coherent hazard curves or maps. *Regime: Earthquake, landslide, volcanic, meteorological, and asteroid tsunami sources across global to local PTHA..* [literature_review_statement, review] (Anita Grezio 2017, [doi:10.1002/2017rg000579](https://doi.org/10.1002/2017rg000579))
- **C386.** A tsunami hazard-and-risk review found maturity uneven across the workflow: earthquake-source probabilistic hazard analysis was relatively advanced, while risk analysis and other sources retained major data, theoretical, and methodological gaps. *Regime: Probabilistic tsunami hazard and risk methods across source types and assessment stages..* [literature_review_statement, review] (Jörn Behrens 2021, [doi:10.3389/feart.2021.628772](https://doi.org/10.3389/feart.2021.628772))
- **C387.** Across global-to-regional coastal flood-risk assessments, omitting adaptation could overestimate 2100 risk by up to a factor 1300, while uncertainty in how societies adapt reached a factor 27 and dominated other globally quantified sources. *Regime: Global to world-regional current and future coastal flood-risk assessments..* [literature_review_statement, review] (Jochen Hinkel 2021, [doi:10.1029/2020ef001882](https://doi.org/10.1029/2020ef001882))
- **C388.** A cross-hazard review warns that representing epistemic uncertainty with simple aleatory distributions can understate hazard and risk variability, and recommends recording and evaluating the assumptions on which every uncertainty estimate is conditional. *Regime: Flood, landslide, dam, drought, earthquake, tsunami, volcanic, and wind hazards..* [literature_review_statement, review] (Keith Beven 2018, [doi:10.5194/nhess-18-2741-2018](https://doi.org/10.5194/nhess-18-2741-2018))
- **C389.** Compound-flood prediction requires uncertainty to be characterized across hydrometeorological and hydrodynamic layers and propagated through their interactions; remote sensing and data science offer routes to reduce predictive uncertainty rather than treating drivers independently. *Regime: Hydrometeorological and hydrodynamic layers of compound-flood modeling and forecasting..* [literature_review_statement, review] (Peyman Abbaszadeh 2022, [doi:10.1016/j.isci.2022.105201](https://doi.org/10.1016/j.isci.2022.105201))
- **C390.** In the Florida Public Hurricane Loss Model, epistemic uncertainty from incomplete and inconsistent exposure and claims data was reduced by integrating and county-level cross-referencing tax-appraiser, NFIP, and wind-insurance databases for development, calibration, and validation. *Regime: Florida residential hurricane vulnerability and insured-loss modeling using tax, NFIP, and wind-insurance data..* [direct_finding, mixed] (Jean‐Paul Pinelli 2020, [doi:10.1007/s13753-020-00316-4](https://doi.org/10.1007/s13753-020-00316-4))
- **C391.** In the flood-damage case study, approximately 25 cm inundation-depth uncertainty accompanied total absolute damage uncertainty of factor 5-6, while asset values and depth-damage curves each contributed about factor two; proportional damage changes were more robust. *Regime: Flood damage case study varying land use, values, depth-damage curves, and water depth..* [direct_finding, numerical] (Hans de Moel 2010, [doi:10.1007/s11069-010-9675-6](https://doi.org/10.1007/s11069-010-9675-6))
- **C1625.** A review of climate-driven sandy-coast erosion models finds that most studies sample only forcing ranges and emissions ensembles, while few are fully probabilistic; credible projections require bias-corrected driver time series and propagation of scenario, climate-model, erosion-model and parameter uncertainty. *Regime: Temperate sandy-beach shoreline projections under climate-driven mean sea level, waves, surge and tides..* [literature_review_statement, review] (A. Toimil 2020, [doi:10.1016/j.earscirev.2020.103110](https://doi.org/10.1016/j.earscirev.2020.103110))
- **C1672.** Extreme significant-wave-height return values vary substantially with initial-distribution, block-maxima, peaks-over-threshold and conditional-exceedance choices; methodological spread increases with return period and can exceed the projected climate-change signal. *Regime: The analyzed North Atlantic significant-wave-height time series for one location, historical climate and two future forcing scenarios..* [direct_finding, numerical] (Erik Vanem 2015, [doi:10.1007/s40722-015-0025-3](https://doi.org/10.1007/s40722-015-0025-3))

## Papers

- Hans de Moel (2010). Effect of uncertainty in land use, damage models and inundation depth on flood damage estimates. *Natural Hazards*. [doi:10.1007/s11069-010-9675-6](https://doi.org/10.1007/s11069-010-9675-6)
- Keith Beven (2015). Facets of uncertainty: epistemic uncertainty, non-stationarity, likelihood, hypothesis testing, and communication. *Hydrological Sciences Journal*. [doi:10.1080/02626667.2015.1031761](https://doi.org/10.1080/02626667.2015.1031761)
- Anita Grezio (2017). Probabilistic Tsunami Hazard Analysis: Multiple Sources and Global Applications. *Reviews of Geophysics*. [doi:10.1002/2017rg000579](https://doi.org/10.1002/2017rg000579)
- A. Toimil (2020). Climate change-driven coastal erosion modelling in temperate sandy beaches: Methods and uncertainty treatment. *Earth-Science Reviews*. [doi:10.1016/j.earscirev.2020.103110](https://doi.org/10.1016/j.earscirev.2020.103110)
- Jörn Behrens (2021). Probabilistic Tsunami Hazard and Risk Analysis: A Review of Research Gaps. *Frontiers in Earth Science*. [doi:10.3389/feart.2021.628772](https://doi.org/10.3389/feart.2021.628772)
- Jochen Hinkel (2021). Uncertainty and Bias in Global to Regional Scale Assessments of Current and Future Coastal Flood Risk. *Earth s Future*. [doi:10.1029/2020ef001882](https://doi.org/10.1029/2020ef001882)
- Keith Beven (2018). Epistemic uncertainties and natural hazard risk assessment – Part 1: A review of different natural hazard areas. *Natural hazards and earth system sciences*. [doi:10.5194/nhess-18-2741-2018](https://doi.org/10.5194/nhess-18-2741-2018)
- Erik Vanem (2015). Uncertainties in extreme value modelling of wave data in a climate change perspective. *Journal of Ocean Engineering and Marine Energy*. [doi:10.1007/s40722-015-0025-3](https://doi.org/10.1007/s40722-015-0025-3)
- Peyman Abbaszadeh (2022). Perspective on uncertainty quantification and reduction in compound flood modeling and forecasting. *iScience*. [doi:10.1016/j.isci.2022.105201](https://doi.org/10.1016/j.isci.2022.105201)
- Jean‐Paul Pinelli (2020). Uncertainty Reduction Through Data Management in the Development, Validation, Calibration, and Operation of a Hurricane Vulnerability Model. *International Journal of Disaster Risk Science*. [doi:10.1007/s13753-020-00316-4](https://doi.org/10.1007/s13753-020-00316-4)
- Zhou (2016). Is “Morphodynamic Equilibrium” an oxymoron?. *Earth-Science Reviews*. [doi:10.1016/j.earscirev.2016.12.002](https://doi.org/10.1016/j.earscirev.2016.12.002)
- Carlo Ruzzo (2021). Scaling strategies for multi-purpose floating structures physical modeling: state of art and new perspectives. *Applied Ocean Research*. [doi:10.1016/j.apor.2020.102487](https://doi.org/10.1016/j.apor.2020.102487)
- Xiaoyuan Luo (2025). Framework for uncertainty quantification of wave–structure interaction in a flume. *Computational Particle Mechanics*. [doi:10.1007/s40571-025-00967-4](https://doi.org/10.1007/s40571-025-00967-4)
