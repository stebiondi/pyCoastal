# Planform evolution

`morphodynamics.planform` | Two-dimensional coastal morphology.

Parent: [Coastal morphodynamics](morphodynamics.md)

Papers: 8. Claims: 4. Equations: 0.

Used by pyCoastal design modules: Beach nourishment.

## Synthesis

**Well established.** Coastal planforms evolve through gradients and exchanges in alongshore and cross-shore sediment transport, with shoreline orientation, inlets, headlands, structures and nourishment creating coupled cells whose apparent local stability may mask sediment transfer across boundaries.

**Governing physics.** Oblique breaking waves drive alongshore transport; shoreline curvature changes wave angle and transport gradients, while storms redistribute profile sediment, tidal prisms maintain inlet channels and deltas, and groins or nourishment perturb bypassing and spreading.

**Dimensionless parameters.** Controls include relative wave angle, diffusivity time normalized by shoreline length squared, nourishment volume relative to active-profile volume, groin length relative to surf-zone width, notch elevation relative to swash, tidal-prism-to-wave forcing ratios and delta extent normalized by inlet width.

**Major equations.** One-line continuity relates shoreline change to the alongshore gradient of sediment transport plus sources and sinks, scaled by active-profile height. More complete planform budgets integrate volume flux across open boundaries and inlet exchange; equilibrium-shape models relate shoreline orientation to spatial wave transformation.

**Typical methods.** Studies repeat shoreline and topobathymetric surveys, define sediment control volumes, measure boundary fluxes, track nourishment spreading and storms, analyze structure bypassing, relate inlet geometry to prism and exposure, calibrate one-line or reduced-complexity models and validate both position and volume.

**Numerical models.** The evidence supports sediment-budget and reduced planform interpretations; direct stability, quasi-three-dimensional bar, estuarine morphodynamic and equilibrium-planform model papers remain in the lawful-full-text queue.

**Experimental datasets.** Reviewed evidence includes four southern California nourishment sites over years to 16 years, the 1100 m Upham Beach project through hurricane influence, UAS-SfM monitoring of three notched groins at Deal and morphology data for 89 United States tidal inlets.

**Validated ranges.** Support spans nourished open coasts, one groin field and a national inlet sample. The reported transport pathways and prism relationships depend on wave exposure, structure geometry, survey boundary and event sequence and are not universal coefficients.

**Recent advances.** Recent advances combine UAS and satellite shoreline/topobathymetry, multi-contour and hybrid 2D/one-line models, unstructured wave coupling, differentiable calibration, ensemble sediment budgets and graph- or neural-accelerated planform solvers.

**Disagreements.** Shoreline-only models can reproduce orientation change while missing cross-shore or offshore volume loss; equilibrium shapes may be useful for sheltered crenulate bays but fail under time-varying wave climates, sediment sources, complex geology or active inlets.

**Limitations.** Open sediment boundaries, uncertain closure depth, sparse bathymetry, event aliasing, shoreline-proxy error, unmeasured bypassing, structure burial, geological controls and simultaneous profile change undermine simple planform attribution.

**Open questions.** Priorities include coupled planform-profile prediction, inlet–beach exchange, time-varying sediment cells, geological constraints, structure permeability, climate-conditioned wave direction, data assimilation, probabilistic nourishment spreading and stable numerics for nonlocal transport.

**Seminal papers.** Pelnard-Considère shoreline diffusion and one-line continuity established planform modeling; equilibrium-bay formulations treated wave sheltering, while sediment-cell budgets and shoreline contour models expanded sources, sinks, structures and multiple contours.

## Claims

- **C132.** Ebb-delta seaward and downdrift extents showed moderate-to-high prism correlations for mildly and highly wave-exposed inlet groups, but poor or no correlation for moderately exposed inlets. *Regime: The 89-inlet database; exposure grouping and a proposed prism scale near 1e8 m3 are empirical and not universal..* [direct_finding, field] (Anon. 2012, [doi:10.2112/jcoastres-d-11-00124.1](https://doi.org/10.2112/jcoastres-d-11-00124.1))
- **C1178.** Appropriate-complexity geomorphic models should bound systems at the behavior and decision scale, match process detail to the question, anticipate possible dynamics and critical state changes, and assess assumptions against observable behavior. *Regime: Appropriate complexity for the prediction of coastal and estuarine geomorphic behaviour at decadal to centennial scales.* [direct_finding, mixed] (Jon French 2016, [doi:10.1016/j.geomorph.2015.10.005](https://doi.org/10.1016/j.geomorph.2015.10.005))
- **C1182.** Monthly lidar over 2.5 years showed two foredunes only 700 m apart diverged: the steeper, sparsely vegetated site retreated and lost volume while the heavily vegetated site prograded and accreted. *Regime: Spatial Variability of Coastal Foredune Evolution, Part A: Timescales of Months to Years.* [direct_finding, mixed] (Katherine Brodie 2019, [doi:10.3390/jmse7050124](https://doi.org/10.3390/jmse7050124))
- **C1649.** LX-Shore combines gradients in longshore sediment transport with wave-energy-driven cross-shore response in a reduced-complexity one-line model, allowing complex sandy shoreline geometries, fixed headlands or defenses, and evolution from storm to decadal scales. *Regime: Wave-dominated sandy coasts represented as translating profiles, including non-erodible rocky areas, headlands and coastal structures..* [direct_finding, numerical] (Arthur Robinet 2018, [doi:10.1016/j.envsoft.2018.08.010](https://doi.org/10.1016/j.envsoft.2018.08.010))

## Papers

- Arthur Robinet (2018). A reduced-complexity shoreline change model combining longshore and cross-shore processes: The LX-Shore model. *Environmental Modelling & Software*. [doi:10.1016/j.envsoft.2018.08.010](https://doi.org/10.1016/j.envsoft.2018.08.010)
- Jon French (2016). Appropriate complexity for the prediction of coastal and estuarine geomorphic behaviour at decadal to centennial scales. *Geomorphology*. [doi:10.1016/j.geomorph.2015.10.005](https://doi.org/10.1016/j.geomorph.2015.10.005)
- Bonnie C. Ludka (2018). Nourishment evolution and impacts at four southern California beaches: A sand volume analysis. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2018.02.003](https://doi.org/10.1016/j.coastaleng.2018.02.003)
- Elko (2007). Immediate profile and planform evolution of a beach nourishment project with hurricane influences. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2006.08.001](https://doi.org/10.1016/j.coastaleng.2006.08.001)
- Katherine Brodie (2019). Spatial Variability of Coastal Foredune Evolution, Part A: Timescales of Months to Years. *Journal of Marine Science and Engineering*. [doi:10.3390/jmse7050124](https://doi.org/10.3390/jmse7050124)
- Zimmerman (2021). UAS-SfM approach to evaluate the performance of notched groins within a groin field and their impact on the morphological evolution of a beach nourishment. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2021.103997](https://doi.org/10.1016/j.coastaleng.2021.103997)
- Panagiotis Athanasiou (2020). Uncertainties in projections of sandy beach erosion due to sea level rise: an analysis at the European scale. *Scientific Reports*. [doi:10.1038/s41598-020-68576-0](https://doi.org/10.1038/s41598-020-68576-0)
- Anon. (2012). Tidal Inlet Morphology Classification and Empirical Determination of Seaward and Down-Drift Extents of Tidal Inlets. *Journal of Coastal Research*. [doi:10.2112/jcoastres-d-11-00124.1](https://doi.org/10.2112/jcoastres-d-11-00124.1)
