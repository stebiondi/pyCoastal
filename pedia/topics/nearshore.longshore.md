# Longshore currents

`nearshore.longshore` | Alongshore wave-driven currents.

Parent: [Nearshore hydrodynamics](nearshore.md)

Papers: 11. Claims: 9. Equations: 0.

Used by pyCoastal design modules: Beach nourishment.

## Synthesis

**Well established.** Obliquely breaking waves drive alongshore momentum and currents whose cross-shore and vertical shear can become unstable. The resulting mean flow, shear waves, vortices, and low-frequency eddies advect and disperse sediment, tracers, organisms, heat, and contaminants.

**Governing physics.** Controls include wave angle, height, directional spread and breaking, radiation stress or vortex force, rollers, setup gradients, bathymetry, vertical shear, bottom and turbulent mixing, shear instability, vortex tilting, and upscale energy transfer.

**Dimensionless parameters.** Important controls include breaker angle, relative water depth, wave height and directional spread, current-to-wave velocity scale, cross-shore shear, friction and mixing coefficients, roller scale, eddy scale relative to surf-zone width, and normalized vertical elevation.

**Major equations.** Frameworks use wave-action and circulation momentum equations with radiation-stress or vortex-force coupling, roller and breaking closures, turbulence models, shear-wave energy and enstrophy balances, Fickian tracer diffusion, and vertical power laws.

**Typical methods.** Methods combine current meters and vertical profiles, continuous dye releases, two-dimensional sensor arrays, long-duration low-frequency observations, bathymetric assimilation, theoretical instability analysis, vortex-force circulation models, SWASH, and coupled SWAN-FVCOM.

**Numerical models.** Depth-uniform, quasi-three-dimensional, and fully three-dimensional models differ in shear-wave energy, confinement, vortex interactions, and vertical profiles. Bathymetric assimilation and spatially variable roller/turbulence parameters improve skill.

**Experimental datasets.** Evidence includes six 1-2 h Huntington Beach dye releases, 120 days of surf-zone currents, Duck two-dimensional arrays and Duck'94 validation, SUPERDUCK conditions, plane/barred-beach profiles, and barred-beach waves from 0.5-2.0 m at 0-15 degrees.

**Validated ranges.** Reported evidence includes cross-shore diffusivity of 0.5-2.5 m2/s, low-frequency motions at 0.1-4.0 mHz over 120 days, validated 0.5-2.0 m waves at 0-15 degrees, O(10 m) and O(100 m) eddies, and profile exponents from 1/10 to 1/3.

**Recent advances.** Recent advances combine months-long observations, phase-resolving three-dimensional models, directional-spread-dependent eddy scaling, bathymetric inversion, and explicit inverse-cascade diagnostics to improve transport prediction.

**Disagreements.** Low-frequency surf-zone currents are not always explained by instability of the mean alongshore current: a 120-day record showed weak correlation with current strength and shear and stronger consistency with breaking-wave-driven inverse energy transfer.

**Limitations.** Steady, depth-uniform, fixed-bathymetry assumptions omit rapid morphology, vertical dispersion, rollers, breaking turbulence, inverse cascades, directional spectra, wind and tides. Sparse field arrays and closure calibration limit transfer.

**Open questions.** Priorities include partitioning shear instability from breaking-generated cascades, resolving three-dimensional saturation and vertical exchange, assimilating storm-time bathymetry, and predicting material pathways under combined wave, wind, and tidal forcing.

**Seminal papers.** The shear-instability review traces the discovery and theory of shear waves and their finite-amplitude development; later quasi-3D and vortex-force studies extend that lineage to vertical structure and realistic bathymetry.

## Claims

- **C454.** Six Huntington Beach dye releases in wave-driven alongshore currents yielded cross-shore diffusivities of 0.5-2.5 m2/s, with plumes often mixed across the surf zone after a few hundred metres and rotational motions contributing to dispersion. *Regime: Huntington Beach surf zone; releases of 1-2 h over varied waves and currents.* [direct_finding, field] (David B. Clark 2010, [doi:10.1029/2009jc005683](https://doi.org/10.1029/2009jc005683))
- **C455.** At Duck, ensemble assimilation of wave height and alongshore current corrected bathymetry and circulation, showing that hourly storm-driven morphology changes can make daily bathymetric surveys inadequate for current prediction. *Regime: Duck natural beach with two-dimensional wave and current sensor array.* [direct_finding, mixed] (Gregory Wilson 2010, [doi:10.1029/2010jc006286](https://doi.org/10.1029/2010jc006286))
- **C456.** A three-dimensional Un-SWAN-FVCOM vortex-force model agreed with laboratory and Duck'94 measurements across oblique and barred-beach cases, while spatially variable roller and turbulence effects improved vertical current profiles. *Regime: planar beach, barred-beach laboratory case, Duck'94 field case, and breakwater case.* [direct_finding, numerical] (Peng Zheng 2017, [doi:10.1016/j.ocemod.2017.06.003](https://doi.org/10.1016/j.ocemod.2017.06.003))
- **C457.** Over 120 field days, 0.1-4.0 mHz surf-zone currents were weakly correlated with alongshore-current shear or strength but were consistent with an inverse energy cascade energized by short-crested breaking waves. *Regime: shallow surf zone across a broad wave range; 0.1-4.0 mHz motions.* [direct_finding, field] (Steve Elgar 2020, [doi:10.1175/jpo-d-19-0327.1](https://doi.org/10.1175/jpo-d-19-0327.1))
- **C458.** Relative to depth-uniform modelling, quasi-three-dimensional SHORECIRC produced weaker, more shoreward-confined shear waves but similar total momentum mixing through combined shear-wave and depth-varying-current transfers. *Regime: idealized SUPERDUCK topography and 16 October 1986 waves.* [direct_finding, numerical] (Qun Zhao 2003, [doi:10.1029/2002jc001306](https://doi.org/10.1029/2002jc001306))
- **C459.** SWASH reproduced alongshore-current and rip-cell trends for 0.5-2.0 m waves at 0-15 degrees, with directional spread intensifying roughly 10 m eddies and alongshore bathymetric variability enhancing roughly 100 m eddies. *Regime: alongshore-variable barred beach; H=0.5-2.0 m and direction=0-15 degrees.* [direct_finding, mixed] (Christine M. Baker 2021, [doi:10.1029/2020jc016899](https://doi.org/10.1029/2020jc016899))
- **C460.** Shear waves arise from instability of wave-driven alongshore currents, with occurrence and finite-amplitude behavior governed by current structure, mixing, and perturbation dynamics documented across theory, field, and laboratory work. *Regime: wave-driven alongshore currents in field, laboratory, and theory.* [literature_review_statement, review] (Nick Dodd 2000, [doi:10.1029/1999rg000067](https://doi.org/10.1029/1999rg000067))
- **C461.** Longshore-current profiles were generally represented by a 1/10 power law across laboratory and field data, but barred-beach trough structure required a substantially different 1/3 exponent. *Regime: plane beach, bar trough, bar crest, and published profile datasets.* [direct_finding, mixed] (Zhenwei Zhang 2019, [doi:10.1016/j.wse.2019.04.004](https://doi.org/10.1016/j.wse.2019.04.004))
- **C1218.** Tri-cuspate beach measurements resolved repeated rip-fed circulation cells for normal waves and a stable meandering longshore current above 0.5 m/s for oblique waves, with predominantly depth-uniform rip flow above the boundary layer. *Regime: Wave-induced nearshore currents at a tri-cuspate beach in the UKCRF.* [direct_finding, mixed] (Alistair G.L. Borthwick 2002, [doi:10.1680/wame.2002.154.4.251](https://doi.org/10.1680/wame.2002.154.4.251))

## Papers

- David B. Clark (2010). Cross‐shore surfzone tracer dispersion in an alongshore current. *Journal of Geophysical Research Atmospheres*. [doi:10.1029/2009jc005683](https://doi.org/10.1029/2009jc005683)
- Gregory Wilson (2010). Data assimilation and bathymetric inversion in a two‐dimensional horizontal surf zone model. *Journal of Geophysical Research: Oceans*. [doi:10.1029/2010jc006286](https://doi.org/10.1029/2010jc006286)
- Peng Zheng (2017). A 3D unstructured grid nearshore hydrodynamic model based on the vortex force formalism. *Ocean Modelling*. [doi:10.1016/j.ocemod.2017.06.003](https://doi.org/10.1016/j.ocemod.2017.06.003)
- Steve Elgar (2020). Field Evidence of Inverse Energy Cascades in the Surfzone. *Journal of Physical Oceanography*. [doi:10.1175/jpo-d-19-0327.1](https://doi.org/10.1175/jpo-d-19-0327.1)
- Qun Zhao (2003). Three‐dimensional effects in shear waves. *Journal of Geophysical Research Atmospheres*. [doi:10.1029/2002jc001306](https://doi.org/10.1029/2002jc001306)
- Christine M. Baker (2021). Modeled Three‐Dimensional Currents and Eddies on an Alongshore‐Variable Barred Beach. *Journal of Geophysical Research Oceans*. [doi:10.1029/2020jc016899](https://doi.org/10.1029/2020jc016899)
- Nick Dodd (2000). Shear instabilities of wave‐driven alongshore currents. *Reviews of Geophysics*. [doi:10.1029/1999rg000067](https://doi.org/10.1029/1999rg000067)
- Alistair G.L. Borthwick (2002). Wave-induced nearshore currents at a tri-cuspate beach in the UKCRF. *Proceedings of the Institution of Civil Engineers - Water and Maritime Engineering*. [doi:10.1680/wame.2002.154.4.251](https://doi.org/10.1680/wame.2002.154.4.251)
- Zhenwei Zhang (2019). Application of power law to vertical distribution of longshore currents. *Water Science and Engineering*. [doi:10.1016/j.wse.2019.04.004](https://doi.org/10.1016/j.wse.2019.04.004)
- Arthur Robinet (2018). A reduced-complexity shoreline change model combining longshore and cross-shore processes: The LX-Shore model. *Environmental Modelling & Software*. [doi:10.1016/j.envsoft.2018.08.010](https://doi.org/10.1016/j.envsoft.2018.08.010)
- Alexandra Spodar (2017). Evolution of a beach nourishment project using dredged sand from navigation channel, Dunkirk, northern France. *Journal of Coastal Conservation*. [doi:10.1007/s11852-017-0514-8](https://doi.org/10.1007/s11852-017-0514-8)
