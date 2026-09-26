# Breaking criteria

`waves.transformation.breaking.criteria` | Onset and type criteria.

Parent: [Waves and wave transformation](waves.md) > [Wave transformation](waves.transformation.md) > [Breaking](waves.transformation.breaking.md)

Papers: 7. Claims: 6. Equations: 0.

## Synthesis

**Well established.** Breaking onset is a local crest instability distinct from the later overturning and dissipation stages. Bulk depth and steepness indices are useful engineering proxies, while local crest-speed, particle-velocity and energy-flux measures provide more process-based prediction.

**Governing physics.** Nonlinear focusing and shoaling concentrate energy near a crest while crest propagation slows. Instability develops as fluid velocity and energy transport approach or overtake crest propagation; depth, bathymetry, bandwidth, wind and current alter this balance.

**Dimensionless parameters.** Important controls are H/h, H/L, ka, Ursell and Iribarren numbers, beach slope, spectral bandwidth, directional spread, crest particle-speed/crest-speed ratio, energy-flux ratio, relative wind speed and relative crest submergence.

**Major equations.** Criterion families include breaker index H_b/h_b, steepness H/L or ka, surf-similarity dependence, kinematic ratios u_c/C, local energy-flux ratios such as B_x, and rate-of-change parameters based on energy maxima and local wavenumber.

**Typical methods.** Studies use focused and random wave groups, flumes and field-scale facilities, surface reconstruction and particle velocimetry, fully nonlinear potential-flow or Navier–Stokes simulations, wave-by-wave field algorithms, breaker-index regression and threshold skill tests.

**Numerical models.** Models include fully nonlinear potential flow, high-resolution Navier–Stokes/SPH or Boussinesq implementations with onset flags, spectral models using modified breaker indices, wave-by-wave engineering algorithms and data-driven threshold classifiers.

**Experimental datasets.** The retained evidence includes deep-water group experiments, fully nonlinear near-breaking benchmarks, arbitrary-depth onset validation, field-scale wind-modified overturns, structure-adjacent breaker-index data and coastal steepness records.

**Validated ranges.** Evidence spans deep, intermediate and shallow water; solitary, quasi-regular, focused and random waves; constant and varying bathymetry; depth-limited overturning; and cases with cross-shore wind or coastal structures.

**Recent advances.** Recent work validates a unified energy-flux/crest-speed onset framework across arbitrary depth, quantifies wind effects on overturn geometry, revises structure-adjacent breaker indices and explores data-driven steepness thresholds.

**Disagreements.** No single bulk index is universally valid. Deep-water energy-growth thresholds, local kinematic/energy-flux criteria and shallow-water H/h or slope formulas emphasize different precursors and can trigger at different crest stages.

**Limitations.** Several seminal formulations remain title-only in the lawful corpus; surface velocity is difficult to measure near overturn; numerical smoothing affects crest speed; field directionality and currents are underrepresented; onset labels differ among studies.

**Open questions.** Needs include three-dimensional directional onset, wind and current corrections, irregular group history, bathymetric curvature, probabilistic thresholds, scale effects and consistent mapping from local onset to model dissipation.

**Seminal papers.** Engineering practice developed wave-by-wave breaker indices and slope/steepness formulas; later deep-water energy-growth and Boussinesq onset flags shifted attention toward local crest dynamics.

## Claims

- **C953.** For four mechanically focused 1-2 Hz wave groups, a Song-Banner energy-growth parameter computed with a local-geometry wavenumber remained below the proposed (1.4 +/- 0.1) x 10^-3 threshold for the nonbreaking group and exceeded it for all three plunging-breaker groups; the lead time and total energy loss increased with the parameter's prebreaking maximum. *Regime: Mechanically focused, unidirectional deep-water-like gravity-wave groups in finite tank depth, with local wavenumber based on adjacent zero-crossing geometry and onset defined just before crest overturning..* [direct_finding, mixed] (Tian 2008, [doi:10.1063/1.2939396](https://doi.org/10.1063/1.2939396))
- **C954.** Fully nonlinear simulations reproduce measured steep unidirectional group evolution and crest kinematics up to near-breaking conditions, providing a pre-onset benchmark. *Regime: Steep unidirectional wave groups – fully nonlinear simulations vs. experiments.* [direct_finding, mixed] (Lev Shemer 2015, [doi:10.5194/npg-22-737-2015](https://doi.org/10.5194/npg-22-737-2015))
- **C955.** Field-scale experiments show cross-shore wind direction and magnitude alter the overturning shape of depth-limited breakers for a given wave-height-to-depth nonlinearity. *Regime: Cross-shore wind-induced changes to field-scale overturning wave shape.* [direct_finding, experimental] (Falk Feddersen 2023, [doi:10.1017/jfm.2023.40](https://doi.org/10.1017/jfm.2023.40))
- **C956.** The Barthelemy energy-flux/crest-speed framework provides a robust breaking-onset criterion for surface gravity waves from deep through shallow water over varying bathymetry. *Regime: A Unified Breaking Onset Criterion for Surface Gravity Water Waves in Arbitrary Depth.* [direct_finding, mixed] (Morteza Derakhti 2020, [doi:10.1029/2019jc015886](https://doi.org/10.1029/2019jc015886))
- **C957.** A revised Weggel nomogram extends the breaker depth index for waves breaking at coastal structures beyond the range of the modified chart. *Regime: Breaker depth index of a wave breaking at a coastal structure – the modified Weggel’s nomogram revisited.* [direct_finding, analytical] (Magda 2025, [doi:10.1680/jmaen.25.00011](https://doi.org/10.1680/jmaen.25.00011))
- **C958.** Data-driven analysis relates coastal breaking-risk thresholds to wave steepness and identifies trends across observed wave conditions. *Regime: Thresholds and trends in wave steepness: A data-driven study of coastal wave breaking risk.* [direct_finding, numerical] (Durap 2025, [doi:10.33714/masteb.1649969](https://doi.org/10.33714/masteb.1649969))

## Papers

- Tian (2008). Evaluation of a deep-water wave breaking criterion. *Physics of Fluids*. [doi:10.1063/1.2939396](https://doi.org/10.1063/1.2939396) [published version, read only](https://web.njit.edu/~wychoi/pub/pof_08.pdf)
- Lev Shemer (2015). Steep unidirectional wave groups – fully nonlinear simulations vs. experiments. *Nonlinear processes in geophysics*. [doi:10.5194/npg-22-737-2015](https://doi.org/10.5194/npg-22-737-2015) [published version, CC BY](https://npg.copernicus.org/articles/22/737/2015/npg-22-737-2015.pdf)
- Falk Feddersen (2023). Cross-shore wind-induced changes to field-scale overturning wave shape. *Journal of Fluid Mechanics*. [doi:10.1017/jfm.2023.40](https://doi.org/10.1017/jfm.2023.40) [published version, CC BY](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/4236FD21F9A9EA5AFCF6ED8966B93596/S002211202300040Xa.pdf/div-class-title-cross-shore-wind-induced-changes-to-field-scale-overturning-wave-shape-div.pdf)
- Morteza Derakhti (2020). A Unified Breaking Onset Criterion for Surface Gravity Water Waves in Arbitrary Depth. *Journal of Geophysical Research Oceans*. [doi:10.1029/2019jc015886](https://doi.org/10.1029/2019jc015886) [submitted manuscript, read only](https://arxiv.org/pdf/1911.06896)
- Magda (2025). Breaker depth index of a wave breaking at a coastal structure – the modified Weggel’s nomogram revisited. *Maritime Engineering*. [doi:10.1680/jmaen.25.00011](https://doi.org/10.1680/jmaen.25.00011)
- Durap (2025). Thresholds and trends in wave steepness: A data-driven study of coastal wave breaking risk. *Marine Science and Technology Bulletin*. [doi:10.33714/masteb.1649969](https://doi.org/10.33714/masteb.1649969) [published version, CC BY](https://dergipark.org.tr/en/pub/masteb/article/1649969)
- Abbas Khayyer (2007). Corrected Incompressible SPH method for accurate water-surface tracking in breaking waves. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2007.10.001](https://doi.org/10.1016/j.coastaleng.2007.10.001) [accepted manuscript, read only](https://repository.kulib.kyoto-u.ac.jp/server/api/core/bitstreams/7c9a16a8-733c-4040-af0c-00a4cee4dddf/content)
