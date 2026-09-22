# Linear wave theory

`analytical.linear` | Linearized wave solutions.

Parent: [Analytical methods](analytical.md)

Papers: 6. Claims: 4. Equations: 0.

## Synthesis

**Well established.** Linear wave theory remains the reference model for small-amplitude surface-gravity-wave dispersion, kinematics, energy flux, shoaling, refraction and diffraction. Its usefulness depends on stating depth, slope, amplitude, directionality and scattering assumptions.

**Governing physics.** Core physics are gravity-restored free-surface motion, depth-dependent dispersion, conservation of energy or wave action, bathymetric refraction and diffraction, and slope-dependent vertical structure.

**Dimensionless parameters.** Key regime controls include relative depth kh, H/h, wave steepness, Ursell number, bed slope, directional spread and topographic length relative to wavelength.

**Major equations.** Common formulations include the Airy dispersion relation, linear velocity-transfer functions, shoaling and group-velocity relations, mild-slope and coupled-mode equations, and spectral wave-action balance.

**Typical methods.** Methods compare analytical solutions with field velocity profiles, laboratory transformation data, stochastic moment equations, non-hydrostatic solvers and operational spectral hindcast-nowcast-forecast systems.

**Numerical models.** Models include sloping-bed linear transfer theory, forward-scattering stochastic coupled modes, a two-layer non-hydrostatic solver benchmarked against linear dispersion, and SWAN driven by WAM, WW3 or buoy observations.

**Experimental datasets.** Reviewed evidence includes storm observations over a 2-degree nearshore slope, three laboratory cases including a fringing reef and barred beach, laboratory topographic-scattering observations, and six regional operational-model applications.

**Validated ranges.** Explicit abstract-level bounds include H/h<0.3 and Ursell number<0.6 on a 2-degree slope, and improved two-layer dispersion and shoaling through kh=4 compared with a one-layer shallow-water range kh<1.

**Recent advances.** Recent developments improve dispersion through layered non-hydrostatic pressure structure, retain coherent interference in stochastic coupled modes, and integrate increasingly resolved coastal domains into operational spectral systems.

**Disagreements.** A model can match bulk wave height while scattering more in setup or second-order statistics, and horizontal-bottom kinematics can fail near a slope even when horizontal velocity remains little affected. Accuracy therefore depends on the diagnostic, not merely the model label.

**Limitations.** Linearization omits finite-amplitude harmonic coupling, breaking, strongly nonlinear runup and some current interactions. Forward-scattering, hydrostatic structure, spectral closure and abstract-only evidence impose additional source-specific limits.

**Open questions.** Priorities include quantified switching criteria between linear and nonlinear models, uncertainty propagation from bathymetry and forcing, efficient wide-angle scattering, and common benchmarks spanning kinematics, spectra, setup and extremes.

**Seminal papers.** The branch rests on classical Airy dispersion and kinematics, energy-flux shoaling, mild-slope transformation and action-balance modeling; the current review slice validates selected descendants rather than establishing a complete historical canon.

## Claims

- **C358.** For observed nearshore waves on a 2-degree bed slope with H/h below 0.3 and Ursell number below 0.6, sloping-bed linear theory reproduced near-bed vertical-velocity magnitude and phase substantially better than horizontal-bottom theory, while horizontal velocity was comparatively insensitive to slope. *Regime: Near-bed observations on a 2-degree slope for H/h below 0.3 and Ursell number below 0.6 during two storm intervals..* [direct_finding, mixed] (Qingping Zou 2003, [doi:10.1029/2002jc001432](https://doi.org/10.1029/2002jc001432))
- **C359.** Against linear-wave dispersion and shoaling benchmarks, the two-layer non-hydrostatic model extended useful behavior from the one-layer model's shallow-water range kh<1 to shallow and intermediate depths through kh=4, though setup and second-order statistics showed more scatter than bulk and spectral wave height. *Regime: Shallow to intermediate water through kh=4, with validation cases including a fringing reef and barred beach..* [direct_finding, mixed] (Menno P. de Ridder 2020, [doi:10.1016/j.coastaleng.2020.103808](https://doi.org/10.1016/j.coastaleng.2020.103808))
- **C360.** For the tested two-dimensional topographies, a stochastic coupled-mode model based on forward scattering reproduced coherent interference and the combined wide-angle refraction-diffraction effects in agreement with analytical solutions and laboratory observations within its linear-interaction focus. *Regime: Random directionally spread waves over fully two-dimensional coastal topography under a forward-scattering approximation; the reported paper focuses on linear topographic interaction..* [direct_finding, mixed] (T. T. Janssen 2008, [doi:10.1029/2007jc004410](https://doi.org/10.1029/2007jc004410))
- **C361.** Across six ocean and coastal applications, SWAN-based hindcast, nowcast, and forecast schemes provided an effective wave-prediction framework when forced by WAM, WW3, or buoy observations, but the abstract does not establish universal accuracy or isolate linear-theory error. *Regime: SWAN applications from high-resolution coastal domains to quasi-oceanic scales in Portugal, Madeira, Sardinia, and the Black Sea..* [literature_review_statement, review] (Eugen Rusu 2011, [doi:10.51400/2709-6998.2138](https://doi.org/10.51400/2709-6998.2138))

## Papers

- Menno P. de Ridder (2020). Efficient two-layer non-hydrostatic wave model with accurate dispersive behaviour. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2020.103808](https://doi.org/10.1016/j.coastaleng.2020.103808)
- Qingping Zou (2003). Vertical structure of surface gravity waves propagating over a sloping seabed: Theory and field measurements. *Journal of Geophysical Research Atmospheres*. [doi:10.1029/2002jc001432](https://doi.org/10.1029/2002jc001432)
- Eugen Rusu (2011). STRATEGIES IN USING NUMERICAL WAVE MODELS IN OCEAN/COASTAL APPLICATIONS. *Journal of Marine Science and Technology*. [doi:10.51400/2709-6998.2138](https://doi.org/10.51400/2709-6998.2138)
- T. T. Janssen (2008). Evolution of ocean wave statistics in shallow water: Refraction and diffraction over seafloor topography. *Journal of Geophysical Research: Oceans*. [doi:10.1029/2007jc004410](https://doi.org/10.1029/2007jc004410)
- Svendsen (1984). Wave heights and set-up in a surf zone. *Coastal Engineering*. [doi:10.1016/0378-3839(84)90028-0](https://doi.org/10.1016/0378-3839(84)90028-0)
- Gioele Ruffini (2019). Numerical modelling of landslide-tsunami propagation in a wide range of idealised water body geometries. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2019.103518](https://doi.org/10.1016/j.coastaleng.2019.103518)
