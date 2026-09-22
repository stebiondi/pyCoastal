# Probabilistic hazard analysis

`risk.probabilistic` | Frequency and joint-probability analysis.

Parent: [Coastal hazards and risk](risk.md)

Papers: 21. Claims: 17. Equations: 7.

Used by pyCoastal design modules: Design conditions.

## Synthesis

**Well established.** Probabilistic coastal hazard analysis estimates exceedance rates or probabilities for physically meaningful responses, not merely storm frequency. It must represent forcing distributions, dependence among drivers, modelled coastal response, sampling uncertainty and the time basis of return quantities.

**Governing physics.** Cyclone pressure, size, speed and heading drive wind, surge, waves and rainfall; tide and sea-level trend shift total water levels; shoreline history controls erosion likelihood; earthquake magnitude and heterogeneous slip govern tsunami generation, propagation and inundation. Local bathymetry and topography strongly transform every source.

**Dimensionless parameters.** Annual exceedance probability, return period, conditional tail probability, extremal shape parameter, normalized pressure deficit, radius and translation-speed ratios, dependence and tail-dependence coefficients, earthquake magnitude and scenario weights organize analyses, but definitions remain method specific.

**Major equations.** Core expressions are exceedance probability H(z)=P(Z>z), annual exceedance rate, return level as an inverse hazard curve, joint-probability integrals over forcing parameters, peaks-over-threshold generalized Pareto tails, GEV or metastatistical extreme models, copula joint distributions, and nonstationary cumulative hazard.

**Typical methods.** Methods include historical-change probability zoning, peaks over threshold, annual maxima, metastatistics, Bayesian or frequentist uncertainty, synthetic storm generation, JPM with copulas, stochastic earthquake rupture ensembles, reduced-order scenario selection, hydrodynamic simulation and surrogate response surfaces.

**Numerical models.** CHS/PCHA couples storm climatology to high-resolution coastal models and surrogates. NEOWAVE resolves Chilean tsunami inundation after SROM scenario reduction. Statistical models include GPD, GEV, MEVD, meta-Gaussian and linear–circular vine copulas.

**Experimental datasets.** Evidence uses historical New Jersey aerial photographs, U.S. tide-gauge surge records, Boston and New York water levels and sea-level projections, U.S. cyclone climatologies, and a Chile–Peru stochastic rupture database simulated for 11 coastal cities.

**Validated ranges.** Extracted bounds include a 90 km New Jersey reach, Chilean Mw 8.0–9.6 ruptures across four segments and 11 cities, Boston and New York nonstationary cases, U.S. tide gauges, and the regional cyclone sample and grids used by CHS and the copula comparison.

**Recent advances.** Recent studies create multi-source stochastic tsunami maps, distinguish nonstationary return-period meanings, test metastatistical surge models nationwide, and compare circular–linear cyclone copulas. The common advance is explicit treatment of dependence, scenario reduction and epistemic uncertainty.

**Disagreements.** No single extreme-value or dependence model is uniformly best. MEVD and GEV can yield similar central estimates yet different stability and design levels; richer vine dependence can improve tail representation while simpler meta-Gaussian dependence may perform similarly in a tested region. Stationary return periods are ambiguous under changing sea level.

**Limitations.** Rare extremes provide little direct tail validation. Results depend on record length, thresholds, stationarity assumptions, marginal distributions, copula structure, synthetic-event sampling, bathymetry, numerical-model error, surrogate error, sea-level scenarios and definitions of return period.

**Open questions.** Priorities are compound rainfall–surge–wave–river probability, spatially coherent extremes, climate-conditioned cyclone and sea-level distributions, model-form ensembles, tail validation, dependence under sparse samples, adaptive scenario selection, and transparent propagation into consequences and decisions.

**Seminal papers.** The 1978 New Jersey study established observation-based probabilistic erosion and surge zoning, while the 1990 sea-level-extremes paper formalized shifting annual extreme distributions under rising mean level. These precede modern process-model ensembles and nonstationary frequency methods.

## Equations

### Maximum over non-identically distributed annual sea levels

$$
P(M_{1:n}\le z)=\prod_{t=1}^{n}F_t(z)
$$

Regime: Independent annual maxima drawn from time-varying distributions, with the paper emphasizing location shifts from mean sea-level rise.

Variables: `M_{1:n}` maximum sea level over the design interval; `F_t` annual-maximum distribution in year t; `z` candidate design elevation; `n` number of years

Source: (Bardsley 1990, [doi:10.1016/0378-3839(90)90028-u](https://doi.org/10.1016/0378-3839(90)90028-u))

### Hazard exceedance probability

$$
H(z)=P[Z>z]
$$

Regime: Historical storm population and coastal study region used for the JPM comparison.

Variables: `H` hazard exceedance probability; `Z` hazard response; `z` specified response level

Source: (Liu 2024, [doi:10.1007/s00477-023-02652-5](https://doi.org/10.1007/s00477-023-02652-5))

### Hazard exceedance probability

$$
H(z)=P[Z>z]
$$

Regime: Boston and New York City observations and the sea-level projections used in the two cases.

Variables: `H` hazard exceedance probability; `Z` hazard response; `z` specified response level

Source: (Jia 2024, [doi:10.1007/s11069-024-06447-x](https://doi.org/10.1007/s11069-024-06447-x))

### Hazard exceedance probability

$$
H(z)=P[Z>z]
$$

Regime: The historical record and developed 90 km New Jersey coastline analysed in the paper.

Variables: `H` hazard exceedance probability; `Z` hazard response; `z` specified response level

Source: (Dolan 1978, [doi:10.1016/0378-3839(78)90004-2](https://doi.org/10.1016/0378-3839(78)90004-2))

### Hazard exceedance probability

$$
H(z)=P[Z>z]
$$

Regime: Four Chile–Peru subduction segments, Mw 8.0–9.6 scenarios and 11 selected Chilean cities.

Variables: `H` hazard exceedance probability; `Z` hazard response; `z` specified response level

Source: (Aranguiz 2024, [doi:10.1080/21664250.2024.2326269](https://doi.org/10.1080/21664250.2024.2326269))

### Hazard exceedance probability

$$
H(z)=P[Z>z]
$$

Regime: U.S. tide-gauge records and calibration lengths evaluated in the paper.

Variables: `H` hazard exceedance probability; `Z` hazard response; `z` specified response level

Source: (Boumis 2024, [doi:10.1080/21664250.2024.2338323](https://doi.org/10.1080/21664250.2024.2338323))

### Hazard exceedance probability

$$
H(z)=P[Z>z]
$$

Regime: U.S. coastlines represented by the CHS regional climatologies, synthetic storms and numerical model grids.

Variables: `H` hazard exceedance probability; `Z` hazard response; `z` specified response level

Source: (Nadal-Caraballo 2020, [doi:10.2112/si95-235.1](https://doi.org/10.2112/si95-235.1))

## Claims

- **C186.** Under sea-level rise, coastal design maxima should be estimated from a sequence of annual extreme-value distributions with shifting location rather than one stationary distribution; future-magnitude quantiles are then more meaningful than stationary return-period levels. *Regime: Annual-maxima distributions whose principal future change is a mean or location shift; changing surge variance and dependence are not represented..* [direct_finding, analytical] (Bardsley 1990, [doi:10.1016/0378-3839(90)90028-u](https://doi.org/10.1016/0378-3839(90)90028-u))
- **C298.** The Coastal Hazards System probabilistic framework combines regional storm climatology, synthetic storms, joint probability modelling of atmospheric forcing, high-resolution hydrodynamic simulations, surrogate prediction, and explicit aleatory and epistemic uncertainty for U.S. hurricane- and extratropical-storm coastlines. *Regime: U.S. coastlines represented by the CHS regional climatologies, synthetic storms and numerical model grids..* [direct_finding, mixed] (Nadal-Caraballo 2020, [doi:10.2112/si95-235.1](https://doi.org/10.2112/si95-235.1))
- **C299.** Along a highly developed 90 km reach of the New Jersey coast, historical aerial photography was used to derive and test probabilities for shoreline-erosion and storm-surge-penetration hazard zones along and across the coast. *Regime: The historical record and developed 90 km New Jersey coastline analysed in the paper..* [direct_finding, mixed] (Dolan 1978, [doi:10.1016/0378-3839(78)90004-2](https://doi.org/10.1016/0378-3839(78)90004-2))
- **C300.** For 11 Chilean coastal cities, stochastic rupture scenarios of magnitude 8.0–9.6 across four Chile–Peru subduction segments were reduced with SROM and simulated with NEOWAVE; the resulting probabilistic inundation maps showed strong site dependence, so a uniform national planning criterion was not supported. *Regime: Four Chile–Peru subduction segments, Mw 8.0–9.6 scenarios and 11 selected Chilean cities..* [direct_finding, mixed] (Aranguiz 2024, [doi:10.1080/21664250.2024.2326269](https://doi.org/10.1080/21664250.2024.2326269))
- **C301.** Across U.S. tide-gauge sites, the metastatistical extreme-value distribution produced surge-extreme estimates comparable to GEV fits but generally lower error variability; model choice still caused site- and calibration-length-dependent differences in design surge height. *Regime: U.S. tide-gauge records and calibration lengths evaluated in the paper..* [direct_finding, mixed] (Boumis 2024, [doi:10.1080/21664250.2024.2338323](https://doi.org/10.1080/21664250.2024.2338323))
- **C302.** For Boston and New York City, detrending observed water levels, fitting a generalized Pareto distribution to threshold exceedances, and reintroducing projected sea-level trends generated nonstationary flood-hazard curves in which expected waiting time and expected-number-of-exceedances definitions of return period are explicitly distinguished. *Regime: Boston and New York City observations and the sea-level projections used in the two cases..* [direct_finding, mixed] (Jia 2024, [doi:10.1007/s11069-024-06447-x](https://doi.org/10.1007/s11069-024-06447-x))
- **C303.** In the study-region Joint Probability Method analysis, a linear–circular Frank vine copula increased hazard-curve stability and tail dependence between large central-pressure deficit and large radius of maximum wind, while a meta-Gaussian copula gave generally consistent performance with simpler implementation. *Regime: Historical storm population and coastal study region used for the JPM comparison..* [direct_finding, mixed] (Liu 2024, [doi:10.1007/s00477-023-02652-5](https://doi.org/10.1007/s00477-023-02652-5))
- **C405.** For Richmond, British Columbia, the direct joint probability method represented dependent contributors to extreme flood and runup-inclusive sea levels and showed that design sea level can differ substantially from extreme flood level alone. *Regime: Dependent tide, surge, wave runup, climate, and tectonic sea-level factors for Richmond, British Columbia..* [direct_finding, analytical] (Joan C. Liu 2009, [doi:10.1061/(asce)0733-950x(2010)136:1(66)](https://doi.org/10.1061/(asce)0733-950x(2010)136:1(66)))
- **C1220.** A global-risk review finds hydrometeorological studies more often include future projections and risk reduction, while earthquake and tsunami studies more often use stochastic fully probabilistic methods that could transfer across hazards. *Regime: Review article: Natural hazard risk assessments at the global scale.* [direct_finding, mixed] (Philip J. Ward 2020, [doi:10.5194/nhess-20-1069-2020](https://doi.org/10.5194/nhess-20-1069-2020))
- **C1223.** A five-step multi-hazard framework classifies impact overlap as spatiotemporal, temporal-only, spatial with residual damage, or independent and demonstrates earthquake-weakened levee failure followed by intense rain in the Po Valley. *Regime: A multi-hazard framework for spatial-temporal impact analysis.* [direct_finding, mixed] (Silvia De Angeli 2022, [doi:10.1016/j.ijdrr.2022.102829](https://doi.org/10.1016/j.ijdrr.2022.102829))
- **C1225.** For a 50 km Po reach, probabilistic mapping combines uncertain peak–volume hydrographs, downstream rating curves, and random overtopping, piping, and micro-instability dike failures to produce hazard confidence information. *Regime: Probabilistic flood hazard mapping: effects of uncertain boundary conditions.* [direct_finding, mixed] (Alessio Domeneghetti 2013, [doi:10.5194/hess-17-3127-2013](https://doi.org/10.5194/hess-17-3127-2013))
- **C1226.** Future-risk assessment must jointly project changing hazards, exposure and physical vulnerability rather than extrapolate static historical impacts under climate, urbanization, wealth and connectivity change. *Regime: Modelling and quantifying tomorrow's risks from natural hazards.* [direct_finding, mixed] (Gemma Cremen 2021, [doi:10.1016/j.scitotenv.2021.152552](https://doi.org/10.1016/j.scitotenv.2021.152552))
- **C1229.** For Rikuzentakata, 726 stochastic slip models derived from 11 inversions propagate source uncertainty through tsunami inundation, empirical fragility, damage, loss and risk visualization. *Regime: Uncertainty modeling and visualization for tsunami hazard and risk mapping: a case study for the 2011 Tohoku earthquake.* [direct_finding, mixed] (Katsuichiro Goda 2015, [doi:10.1007/s00477-015-1146-x](https://doi.org/10.1007/s00477-015-1146-x))
- **C1395.** NEAMTHM18 constructs a regional probabilistic tsunami hazard model from source ensembles and propagation calculations to support consistent hazard estimates across the Northeast Atlantic, Mediterranean and connected seas. *Regime: The Making of the NEAM Tsunami Hazard Model 2018 (NEAMTHM18).* [direct_finding, mixed] (Roberto Basili 2021, [doi:10.3389/feart.2020.616594](https://doi.org/10.3389/feart.2020.616594))
- **C1692.** A Bayesian network for Taitung links wave energy, shoreline change and socioeconomic/environmental factors with about 74% predictive accuracy; under 2 C warming, the maximum probability of high hazard in the Bainen River estuary sector rises to 60%. *Regime: Taitung, Taiwan coastal sectors under the documented long-term data and 2 C global-warming scenario..* [direct_finding, mixed] (Ye 2026, [doi:10.1007/s11069-026-08335-y](https://doi.org/10.1007/s11069-026-08335-y))
- **C1712.** RoadRAT combines extreme-value statistics for still-water level, total water level including runup, and storm erosion with shoreline evolution to screen present and future coastal-road impacts; its 89 km Swedish demonstration finds erosion dominates expanding future exposure. *Regime: Regional coastal roads exposed to inundation, wave runup, storm erosion, sea-level rise, and continued historical shoreline trends..* [direct_finding, mixed] (Hallin 2025, [doi:10.1016/j.coastaleng.2025.104741](https://doi.org/10.1016/j.coastaleng.2025.104741))
- **C1741.** Value-of-information maps combine probabilistic flood hazard and decision consequences to identify locations where additional evidence is worth acquiring before floodplain land-use decisions, complementing rather than replacing comprehensive risk maps. *Regime: Floodplain spatial planning where probabilistic inundation information, uncertain hydraulic-model skill, candidate land uses, and action consequences can be represented spatially..* [direct_finding, mixed] (Leonardo Alfonso 2016, [doi:10.1002/2015wr017378](https://doi.org/10.1002/2015wr017378))

## Papers

- Philip J. Ward (2020). Review article: Natural hazard risk assessments at the global scale. *Natural hazards and earth system sciences*. [doi:10.5194/nhess-20-1069-2020](https://doi.org/10.5194/nhess-20-1069-2020)
- Silvia De Angeli (2022). A multi-hazard framework for spatial-temporal impact analysis. *International Journal of Disaster Risk Reduction*. [doi:10.1016/j.ijdrr.2022.102829](https://doi.org/10.1016/j.ijdrr.2022.102829)
- Roberto Basili (2021). The Making of the NEAM Tsunami Hazard Model 2018 (NEAMTHM18). *Frontiers in Earth Science*. [doi:10.3389/feart.2020.616594](https://doi.org/10.3389/feart.2020.616594)
- Alessio Domeneghetti (2013). Probabilistic flood hazard mapping: effects of uncertain boundary conditions. *Hydrology and earth system sciences*. [doi:10.5194/hess-17-3127-2013](https://doi.org/10.5194/hess-17-3127-2013)
- Gemma Cremen (2021). Modelling and quantifying tomorrow's risks from natural hazards. *The Science of The Total Environment*. [doi:10.1016/j.scitotenv.2021.152552](https://doi.org/10.1016/j.scitotenv.2021.152552)
- Leonardo Alfonso (2016). Probabilistic Flood Maps to support decision‐making: Mapping the Value of Information. *Water Resources Research*. [doi:10.1002/2015wr017378](https://doi.org/10.1002/2015wr017378)
- Katsuichiro Goda (2015). Uncertainty modeling and visualization for tsunami hazard and risk mapping: a case study for the 2011 Tohoku earthquake. *Stochastic Environmental Research and Risk Assessment*. [doi:10.1007/s00477-015-1146-x](https://doi.org/10.1007/s00477-015-1146-x)
- Nadal-Caraballo (2020). Coastal Hazards System: A Probabilistic Coastal Hazard Analysis Framework. *Journal of Coastal Research*. [doi:10.2112/si95-235.1](https://doi.org/10.2112/si95-235.1)
- Joan C. Liu (2009). Direct Joint Probability Method for Estimating Extreme Sea Levels. *Journal of Waterway Port Coastal and Ocean Engineering*. [doi:10.1061/(asce)0733-950x(2010)136:1(66)](https://doi.org/10.1061/(asce)0733-950x(2010)136:1(66))
- Dolan (1978). Analysis of coastal erosion and storm surge hazards. *Coastal Engineering*. [doi:10.1016/0378-3839(78)90004-2](https://doi.org/10.1016/0378-3839(78)90004-2)
- Aranguiz (2024). A new generation of tsunami inundation maps of Chilean cities: tsunami source database and probabilistic hazard analysis. *Coastal Engineering Journal*. [doi:10.1080/21664250.2024.2326269](https://doi.org/10.1080/21664250.2024.2326269)
- Boumis (2024). A metastatistical frequency analysis of extreme storm surge hazard along the US coastline. *Coastal Engineering Journal*. [doi:10.1080/21664250.2024.2338323](https://doi.org/10.1080/21664250.2024.2338323)
- Jia (2024). Nonstationary coastal flood hazard analysis. *Natural Hazards*. [doi:10.1007/s11069-024-06447-x](https://doi.org/10.1007/s11069-024-06447-x)
- Hallin (2025). RoadRAT – A new framework to assess the probability of inundation, wave runup, and erosion impacting coastal roads. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2025.104741](https://doi.org/10.1016/j.coastaleng.2025.104741)
- Bardsley (1990). Estimating future sea level extremes under conditions of sea level rise. *Coastal Engineering*. [doi:10.1016/0378-3839(90)90028-u](https://doi.org/10.1016/0378-3839(90)90028-u)
- Liu (2024). Comparative analysis of joint distribution models for tropical cyclone atmospheric parameters in probabilistic coastal hazard analysis. *Stochastic Environmental Research and Risk Assessment*. [doi:10.1007/s00477-023-02652-5](https://doi.org/10.1007/s00477-023-02652-5)
- Ye (2026). Coastal risk assessment and hazard forecast analysis via a Bayesian network. *Natural Hazards*. [doi:10.1007/s11069-026-08335-y](https://doi.org/10.1007/s11069-026-08335-y)
- Hamed Moftakhari (2019). Linking statistical and hydrodynamic modeling for compound flood hazard assessment in tidal channels and estuaries. *Advances in Water Resources*. [doi:10.1016/j.advwatres.2019.04.009](https://doi.org/10.1016/j.advwatres.2019.04.009)
- James Savage (2016). Quantifying the importance of spatial resolution and other factors through global sensitivity analysis of a flood inundation model. *Water Resources Research*. [doi:10.1002/2015wr018198](https://doi.org/10.1002/2015wr018198)
- James Savage (2015). When does spatial resolution become spurious in probabilistic flood inundation predictions?. *Hydrological Processes*. [doi:10.1002/hyp.10749](https://doi.org/10.1002/hyp.10749)
- Percival (2019). A methodology for urban micro-scale coastal flood vulnerability and risk assessment and mapping. *Natural Hazards*. [doi:10.1007/s11069-019-03648-7](https://doi.org/10.1007/s11069-019-03648-7)
