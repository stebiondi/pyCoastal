# Contraction and channel scour

`scour.contraction` | Scour caused by flow constriction.

Parent: [Scour and erosion](scour.md)

Papers: 7. Claims: 7. Equations: 0.

## Synthesis

**Well established.** Contraction scour results when lateral or vertical restriction accelerates flow and increases sediment transport capacity through an opening. Clear-water, live-bed, pressure-flow, and unsteady-flood regimes produce different depths and timescales.

**Governing physics.** Controls include opening ratio, discharge and Froude number, flow depth, pressure confinement, hydrograph duration and peak, sediment size and critical mobility, surface layering, abutment or pier blockage, and upstream channel/floodplain adjustment.

**Dimensionless parameters.** Important groups include contracted-to-uncontracted width, blockage or opening ratio, relative scour depth, Froude number, velocity-to-critical velocity, sediment-to-flow-depth ratio, surface-to-subsurface grain-size ratio, and contraction length or abutment length relative to depth.

**Major equations.** Methods use continuity and energy balances, critical-velocity and sediment-mobility relations, additive contraction and local-scour components, equilibrium and time-dependent empirical formulas, hydrograph stepping, HEC-RAS hydraulics, and ANFIS predictors.

**Typical methods.** Evidence combines long rectangular flumes, steady and stepped hydrographs, clear-water and live-bed tests, pressure-flow decks, layered beds, parametric equation comparison, remote sensing, field inspection, and one-dimensional/two-dimensional hydraulic modelling.

**Numerical models.** Empirical, theoretical, data-driven, and hydraulic models serve different purposes. ANFIS can optimize fit, energy-continuity theory preserves mechanism, and HEC-RAS with geomorphic history supports site screening; none alone establishes universal transfer.

**Experimental datasets.** The branch includes 0.90 mm pressure-scour tests, six hydrographs in a 20 m flume at width ratio 0.80, long-contraction pier and gravel-layer tests, constant-discharge opening-ratio tests, and 1,276 Landsat scenes at five detailed bridge sites.

**Validated ranges.** Reported transitions include a scour-gradient change near opening ratio 0.8, live-bed relative scour approaching 3.36, an NCHRP/Froehlich crossover near L/ya 35-45, contraction width ratio 0.80, and severe risk persisting across 50-500 year floods at one site.

**Recent advances.** Recent work emphasizes time-dependent profiles, model-form divergence, long-term remote-sensing context, data-driven architecture comparison, and the possibility that floodplain widening progressively increases effective bridge contraction.

**Disagreements.** Legacy Froehlich and HIRE power laws increase continuously with contraction, whereas the physically based NCHRP response is bounded in live bed and may exceed Froehlich in a deep-encroachment transition. Conventional conservatism is therefore regime-dependent.

**Limitations.** Evidence is mostly alluvial, laboratory, clear-water, and bridge-specific. Marine waves and tides, cohesive beds, compound surge-river floods, debris, complex three-dimensional openings, scale effects, and sparse event bathymetry limit coastal transfer.

**Open questions.** Needs include unified local-plus-contraction scour under unsteady live bed, wave-tide-river interaction, vertical and lateral contraction together, layered/cohesive beds, changing floodplains, uncertainty-aware model selection, and coastal-crossing field validation.

**Seminal papers.** The branch builds on continuity-energy contraction theory, critical mobility, clear-water/live-bed distinction, and empirical bridge scour equations, extended by unsteady hydrographs, layered beds, pressure flow, model comparison, and geomorphic history.

## Claims

- **C502.** Clear-water bridge-deck experiments with 0.90 mm sand quantified pressure-flow scour and downstream deposition under both steady flow and single-peaked stepped flood hydrographs. *Regime: rectangular submerged bridge deck over 0.90 mm uniform sand in clear water.* [direct_finding, experimental] (Şerife Yurdagül Kumcu 2016, [doi:10.1139/cjce-2015-0385](https://doi.org/10.1139/cjce-2015-0385))
- **C503.** At constant discharge and depth, clear-water pier tests found a change in nondimensional scour-depth gradient near an opening ratio of 0.8, with a steeper slope above that threshold. *Regime: circular piers at constant discharge and depth with varied diameter.* [direct_finding, experimental] (Anandrao R. Deshmukh 2014, [doi:10.15623/ijret.2014.0301024](https://doi.org/10.15623/ijret.2014.0301024))
- **C504.** Six clear-water stepped-hydrograph experiments at contraction ratio 0.80 supported practical formulas for the time evolution of maximum scour depth, scour-hole length, and downstream centreline bed profile. *Regime: 20 m by 1 m rectangular channel, 1 m contraction length, width ratio 0.80, coarse sand, clear water.* [direct_finding, experimental] (Giuseppe Oliveto 2020, [doi:10.18280/ijsdp.150208](https://doi.org/10.18280/ijsdp.150208))
- **C505.** For the tested contraction-scour dataset, a zero-order Takagi-Sugeno ANFIS with four bell-shaped membership functions per input and Levenberg-Marquardt training gave the best statistical performance. *Regime: alluvial-channel equilibrium contraction scour dataset.* [direct_finding, numerical] (Minh Duc Bui 2017, [doi:10.9790/1684-1403051832](https://doi.org/10.9790/1684-1403051832))
- **C506.** Long-contraction tests showed deeper scour with coarser sediment and smaller opening ratio; thin gravel layers produced more scour than uniform beds, and equilibrium depth was represented by combined contraction and critical pier-scour components. *Regime: pier and thin gravel layer within long channel contraction.* [direct_finding, experimental] (Raikar 2006, [doi:10.1139/l05-097](https://doi.org/10.1139/l05-097))
- **C507.** Across varied contraction, legacy Froehlich and HIRE models increased continuously, whereas NCHRP 24-20 approached relative scour about 3.36 in live bed and could exceed Froehlich near L/ya 35-45. *Regime: bridge abutment models across contraction, Froude number, grain size, and mobility regimes.* [direct_finding, numerical] (Thi Thao Pham 2026, [doi:10.7409/rabdim.026.011](https://doi.org/10.7409/rabdim.026.011))
- **C508.** Analysis of 1,276 Landsat images and bridge hydraulics linked long-term floodplain widening to stronger opening contraction; Sego remained severely scour-prone for 50-, 100-, and 500-year floods. *Regime: 15 southern Ethiopia bridges, five detailed sites, 50-500 year floods.* [direct_finding, mixed] (Aklilu Alemayehu Kassaye 2024, [doi:10.59122/20519g6](https://doi.org/10.59122/20519g6))

## Papers

- Şerife Yurdagül Kumcu (2016). Steady and unsteady pressure scour under bridges at clear-water conditions. *Canadian Journal of Civil Engineering*. [doi:10.1139/cjce-2015-0385](https://doi.org/10.1139/cjce-2015-0385)
- Anandrao R. Deshmukh (2014). A CLEAR WATER SCOUR AROUND A CIRCULAR BRIDGE PIER UNDER STEADY FLOW FOR DIFFERENT OPENING RATIOS. *International Journal of Research in Engineering and Technology*. [doi:10.15623/ijret.2014.0301024](https://doi.org/10.15623/ijret.2014.0301024)
- Giuseppe Oliveto (2020). The Impact of River Contractions on the Bed Morphology under Unsteady Flows. *International Journal of Sustainable Development and Planning*. [doi:10.18280/ijsdp.150208](https://doi.org/10.18280/ijsdp.150208)
- Minh Duc Bui (2017). Performance Analysis Of Different Model Architectures Utilized In An Adaptive Neuro Fuzzy Inference System For Contraction Scour Prediction. *IOSR Journal of Mechanical and Civil Engineering*. [doi:10.9790/1684-1403051832](https://doi.org/10.9790/1684-1403051832)
- Raikar (2006). Pier scour and thin layered bed scour within a long contraction. *Canadian Journal of Civil Engineering*. [doi:10.1139/l05-097](https://doi.org/10.1139/l05-097)
- Thi Thao Pham (2026). Evaluating bridge abutment scour models under varying contraction. *Roads and Bridges - Drogi i Mosty*. [doi:10.7409/rabdim.026.011](https://doi.org/10.7409/rabdim.026.011)
- Aklilu Alemayehu Kassaye (2024). Morphodynamic alterations around the bridge opening and the process of scouring under the influence of hydraulic flow parameters on selected bridges in the south Ethiopia regional state, Sodo to Konso highway. *Ethiopian Journal of Water Science and Technology*. [doi:10.59122/20519g6](https://doi.org/10.59122/20519g6)
