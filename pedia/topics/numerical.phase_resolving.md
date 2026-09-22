# Phase-resolving wave models

`numerical.phase_resolving` | Boussinesq and nonhydrostatic models.

Parent: [Numerical modeling](numerical.md)

Papers: 15. Claims: 10. Equations: 0.

## Synthesis

**Well established.** Phase-resolving models simulate individual wave crests and troughs, retaining nonlinear interactions, dispersion, reflection and runup that phase-averaged spectral models parameterize; their added detail requires finer space-time resolution, consistent boundaries and process-specific validation.

**Governing physics.** Nonlinear free-surface motion, frequency dispersion, shoaling, refraction, diffraction, reflection, breaking, infragravity generation, wetting/drying, currents and structure or vegetation interactions govern resolved waves. Depth-averaged formulations still approximate vertical shear, turbulence and overturning.

**Dimensionless parameters.** Controls include relative depth kh, wave steepness, Ursell and Froude numbers, relative amplitude and submergence, directional spread, Courant number, cells per wavelength, layer count, breaking or dissipation parameters, wetting depth and morphological acceleration factor.

**Major equations.** Boussinesq-type equations extend shallow-water mass and momentum with dispersive terms; depth-averaged nonhydrostatic models solve pressure corrections, while fully nonlinear potential flow, RANS/VOF and multilayer formulations add successively more vertical physics. Bed evolution couples sediment-flux divergence to morphology.

**Typical methods.** Workflows verify linear dispersion, shoaling, conservation and still-water balance; validate solitary waves, runup, breaking, bars, vegetation and harbor spectra; test convergence and boundaries; separate surface elevation, velocity and morphology skill; and compare against phase-averaged or physical models.

**Numerical models.** The set spans higher-order Boussinesq, FORCE-based depth-averaged nonhydrostatic, XBNH/XBNH+, weakly coupled wave-resolving–wave-averaged morphology and hybrid numerical/physical modeling, with applications from tsunami runup to vegetation and harbors.

**Experimental datasets.** Reviewed evidence includes Synolakis plane-beach and conical-island runup, controlled frequency/directional-spread runup, vegetation attenuation, FORCE-scheme verification cases, a large-scale barred beach, weakly coupled bed evolution, deterministic physical–numerical combinations and multimodal harbor spectra.

**Validated ranges.** Support is benchmark- and site-specific. The Boussinesq runup model degraded from H/d=0.10 to 0.20 at the conical island, and barred-beach models reproduced seaward waves but overpredicted landward heights; no solver is validated across all breaking and morphology regimes.

**Recent advances.** Recent advances use multilayer nonhydrostatic and high-order unstructured solvers, adaptive meshes, immersed and porous boundaries, GPU acceleration, deterministic physical–numerical coupling, differentiable calibration and phase-resolving data assimilation.

**Disagreements.** Boussinesq models efficiently capture weak-to-moderate dispersion but need breaking closures; nonhydrostatic multilayer models broaden dispersion at higher cost; RANS resolves overturning but is expensive. Surface-elevation tuning can leave velocity and sediment errors unresolved.

**Limitations.** Boundary reflection, sponge design, numerical dispersion, grid and time resolution, breaking and turbulence closures, wet/dry thresholds, vertical averaging, bathymetric error and morphology coupling can dominate results. Phase accuracy degrades over long domains without careful dispersion control.

**Open questions.** Priorities include parameter-robust breaking, adaptive vertical resolution, conservative nested phase coupling, irregular directional seas, air and porous structures, wave-current-vorticity interactions, scalable GPU solvers, uncertainty propagation and multi-variable morphodynamic validation.

**Seminal papers.** Peregrine and later enhanced Boussinesq equations established dispersive coastal-wave simulation; fully nonlinear potential flow, nonhydrostatic pressure correction and VOF/RANS expanded regimes, while FUNWAVE, BOSZ, SWASH and XBeach-NH enabled practical applications.

## Claims

- **C6.** The higher-order Boussinesq model reproduced the principal runup and rundown evolution in the Synolakis plane-beach validation case. *Regime: Solitary-wave runup on a 1:19.85 plane beach with 0.2 m still-water depth; the source reports H/d inconsistently as 0.25 in the caption and 0.28 in prose..* [direct_finding, mixed] (Samaras 2015, [doi:10.5194/os-11-643-2015](https://doi.org/10.5194/os-11-643-2015))
- **C7.** For conical-island runup, agreement was closer at H/d=0.10 than at H/d=0.20, where the model underpredicted front-side maximum runup. *Regime: Briggs et al. conical island: 14-degree face, 0.32 m water depth, solitary waves with H/d 0.10 and 0.20..* [direct_finding, mixed] (Samaras 2015, [doi:10.5194/os-11-643-2015](https://doi.org/10.5194/os-11-643-2015))
- **C137.** For the tested large-scale barred beach, XBNH and XBNH+ reproduced seaward hydrodynamics but overpredicted wave heights landward of the bar because crest breaking and turbulence were simplified; dissipation tuning did not also fix velocity and morphology errors. *Regime: Single- and reduced-two-layer XBeach nonhydrostatic modes for the tested fixed/mobile barred profiles..* [direct_finding, mixed] (Elsayed 2022, [doi:10.1061/(asce)ww.1943-5460.0000685](https://doi.org/10.1061/(asce)ww.1943-5460.0000685))
- **C140.** The FORCE-based depth-averaged nonhydrostatic model was well balanced, accurately captured wet-dry fronts, and simulated wave breaking reasonably without a tunable breaking coefficient across its verification tests. *Regime: The paper's SNHE benchmarks over uneven beds; depth-averaging limitations remain for vertical turbulence..* [direct_finding, numerical] (Lu 2016, [doi:10.1016/j.coastaleng.2016.04.004](https://doi.org/10.1016/j.coastaleng.2016.04.004))
- **C1302.** A validated nonhydrostatic reef model shows fore-reef slope controls runup on reef-fronted coasts; for a 1:5 fore-reef and 500 m flat, beach slope near 1:30 separated runup reduction from enhancement, with tall roughness most effective. *Regime: Wave‐Driven Hydrodynamic Processes Over Fringing Reefs With Varying Slopes, Depths, and Roughness: Implications for Coastal Protection.* [direct_finding, mixed] (Mark L. Buckley 2022, [doi:10.1029/2022jc018857](https://doi.org/10.1029/2022jc018857))
- **C1341.** A fourth-order Boussinesq moving-bottom model using sixth-order spatial and temporal schemes agreed with three-dimensional experiments and retained nonlinear and dispersive accuracy for landslide waves generated into intermediate and deeper water. *Regime: A higher‐order Boussinesq‐type model with moving bottom boundary: applications to submarine landslide tsunami waves.* [direct_finding, numerical] (Ataie‐Ashtiani 2007, [doi:10.1002/fld.1354](https://doi.org/10.1002/fld.1354))
- **C1673.** Three-dimensional high-level Green-Naghdi models extend strong nonlinearity to stronger dispersion, and GN-3 is converged for the tested shoal-diffraction cases while agreeing with analytical, laboratory and fully nonlinear Boussinesq benchmarks. *Regime: Three-dimensional shallow-water wave evolution and diffraction over the modeled elliptic and submerged shoals within the benchmark ranges..* [direct_finding, numerical] (Binbin Zhao 2014, [doi:10.1007/s40722-014-0009-8](https://doi.org/10.1007/s40722-014-0009-8))
- **C1686.** Finite-volume fluxes, MUSCL/WENO reconstructions and wet–dry treatment can be extended to Boussinesq-type systems to simulate bidirectional dispersive waves, solitary-wave interactions, dispersive shocks, and breaking or non-breaking long-wave run-up. *Regime: One-dimensional nonlinear dispersive long-wave propagation and run-up within the tested Boussinesq and wet–dry benchmarks..* [direct_finding, numerical] (Denys Dutykh 2011, [doi:10.1016/j.jcp.2011.01.003](https://doi.org/10.1016/j.jcp.2011.01.003))
- **C1688.** A hybrid finite-volume/finite-difference Green–Naghdi solver with improved dispersion reproduces strongly nonlinear wave transformation over a submerged bar, including high-order harmonics generated by bathymetric interactions. *Regime: One-dimensional, strongly nonlinear and dispersive shallow-water waves over submerged bathymetry without dry areas and up to wave breaking..* [direct_finding, numerical] (Chazel 2010, [doi:10.1007/s10915-010-9395-9](https://doi.org/10.1007/s10915-010-9395-9))
- **C1765.** Correcting incompressible SPH gradient operators to reproduce linear velocity fields and preserve angular momentum materially improves free-surface tracking of solitary-wave breaking and post-breaking splash-up relative to standard ISPH. *Regime: Two-dimensional, single-phase solitary waves breaking and post-breaking on uniform plane slopes, including spilling, plunging, and surging regimes..* [direct_finding, numerical] (Abbas Khayyer 2007, [doi:10.1016/j.coastaleng.2007.10.001](https://doi.org/10.1016/j.coastaleng.2007.10.001))

## Papers

- Abbas Khayyer (2007). Corrected Incompressible SPH method for accurate water-surface tracking in breaking waves. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2007.10.001](https://doi.org/10.1016/j.coastaleng.2007.10.001)
- Denys Dutykh (2011). Finite volume schemes for dispersive wave propagation and runup. *Journal of Computational Physics*. [doi:10.1016/j.jcp.2011.01.003](https://doi.org/10.1016/j.jcp.2011.01.003)
- Chazel (2010). Numerical Simulation of Strongly Nonlinear and Dispersive Waves Using a Green–Naghdi Model. *Journal of Scientific Computing*. [doi:10.1007/s10915-010-9395-9](https://doi.org/10.1007/s10915-010-9395-9)
- Ataie‐Ashtiani (2007). A higher‐order Boussinesq‐type model with moving bottom boundary: applications to submarine landslide tsunami waves. *International Journal for Numerical Methods in Fluids*. [doi:10.1002/fld.1354](https://doi.org/10.1002/fld.1354)
- Binbin Zhao (2014). High-level Green–Naghdi wave models for nonlinear wave transformation in three dimensions. *Journal of Ocean Engineering and Marine Energy*. [doi:10.1007/s40722-014-0009-8](https://doi.org/10.1007/s40722-014-0009-8)
- Mark L. Buckley (2022). Wave‐Driven Hydrodynamic Processes Over Fringing Reefs With Varying Slopes, Depths, and Roughness: Implications for Coastal Protection. *Journal of Geophysical Research Oceans*. [doi:10.1029/2022jc018857](https://doi.org/10.1029/2022jc018857)
- Elsayed (2022). Nonhydrostatic Numerical Modeling of Fixed and Mobile Barred Beaches: Limitations of Depth-Averaged Wave Resolving Models around Sandbars. *Journal of Waterway, Port, Coastal, and Ocean Engineering*. [doi:10.1061/(asce)ww.1943-5460.0000685](https://doi.org/10.1061/(asce)ww.1943-5460.0000685)
- Lu (2016). Depth-averaged non-hydrostatic numerical modeling of nearshore wave propagations based on the FORCE scheme. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2016.04.004](https://doi.org/10.1016/j.coastaleng.2016.04.004)
- Junliang Gao (2023). Mechanism analysis on the mitigation of harbor resonance by periodic undulating topography. *Ocean Engineering*. [doi:10.1016/j.oceaneng.2023.114923](https://doi.org/10.1016/j.oceaneng.2023.114923)
- Guza (2012). Effect of wave frequency and directional spread on shoreline runup. *Geophysical Research Letters*. [doi:10.1029/2012gl051959](https://doi.org/10.1029/2012gl051959)
- Phan (2019). The effects of wave non-linearity on wave attenuation by vegetation. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2019.01.004](https://doi.org/10.1016/j.coastaleng.2019.01.004)
- Samaras (2015). Simulation of tsunami generation, propagation and coastal inundation in the Eastern Mediterranean. *Ocean Science*. [doi:10.5194/os-11-643-2015](https://doi.org/10.5194/os-11-643-2015)
- Zhang (2007). Deterministic combination of numerical and physical coastal wave models. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2006.08.009](https://doi.org/10.1016/j.coastaleng.2006.08.009)
- Romano-Moreno (2023). Multimodal harbor wave climate characterization based on wave agitation spectral types. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2022.104271](https://doi.org/10.1016/j.coastaleng.2022.104271)
- Gallerano (2016). Modeling Bed Evolution Using Weakly Coupled Phase-Resolving Wave Model and Wave-Averaged Sediment Transport Model. *Coastal Engineering Journal*. [doi:10.1142/s057856341650011x](https://doi.org/10.1142/s057856341650011x)
