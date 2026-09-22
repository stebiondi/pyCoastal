# Refraction

`waves.transformation.refraction` | Depth- and current-induced turning.

Parent: [Waves and wave transformation](waves.md) > [Wave transformation](waves.transformation.md)

Papers: 9. Claims: 8. Equations: 0.

## Synthesis

**Well established.** Wave refraction changes propagation direction and energy density as phase speed varies with depth or current; converging rays focus energy and diverging rays defocus it, while diffraction, reflection, breaking and spectral spreading regularize ideal ray singularities.

**Governing physics.** Conservation of frequency along stationary paths and of wave action in currents combines with the dispersion relation to rotate wave crests toward slower regions. Bathymetric mounds, channels, headlands and current gradients produce caustics, shadow zones and frequency-dependent focusing.

**Dimensionless parameters.** Controls include kh, relative depth and bathymetric slope, incident angle, directional spread, current-to-group-speed ratio, refraction and shoaling coefficients, mound height and width relative to wavelength, focusing gain and grid or spectral resolution relative to caustic width.

**Major equations.** Linear dispersion links frequency, wavenumber and depth; Snell-type relations conserve along-crest wavenumber for parallel contours. Spectral action balance transports action through geographic and directional space, while mild-slope, Boussinesq and nonhydrostatic equations include diffraction and nonlinear transformation.

**Typical methods.** Studies map directional spectra and bathymetry, ray-trace or solve spectral/phase-resolving equations, validate mound and island benchmarks, compare cross-shore wave-height sections, test frequency-direction boundary sensitivity and report focusing, sheltered-site and bias errors separately.

**Numerical models.** The set includes a three-dimensional nonhydrostatic model for shoaling, diffraction and refraction and two regional spectral formulations with and without diffraction. Direct current-refraction and multidirectional model records remain in the lawful-full-text queue.

**Experimental datasets.** Reviewed evidence includes Vincent–Briggs flat-bed and Berkhoff 1:50 sloping-bed mound benchmarks and a roughly 300 km by 300 km Southern California Bight comparison of refraction and refraction–diffraction spectral models.

**Validated ranges.** The Berkhoff focusing section reached 2.2 times incident wave height; the flat-bed focusing section had MAE 0.158 and MBE -0.114. Regional models improved with broader incident spectra but neither was accurate at highly sheltered sites.

**Recent advances.** Recent advances combine unstructured high-resolution spectral models, current-coupled action balance, nonhydrostatic and dispersive solvers, satellite-derived bathymetry, data assimilation, adaptive phase-resolving nests and differentiable calibration.

**Disagreements.** Geometric rays are efficient away from caustics but fail where diffraction or multi-path interference matters. Spectral phase-averaged models handle broad seas but smooth coherent focusing, while phase-resolving models capture interference at higher cost and remain sensitive to boundaries and breaking.

**Limitations.** Bathymetric resolution, boundary directional spectra, current uncertainty, caustics, diffraction closure, unresolved islands and structures, nonlinear breaking, bottom friction and sparse directional observations can dominate. Agreement at exposed sites does not prove skill in sheltered zones.

**Open questions.** Priorities include current–depth refraction in strong shears, probabilistic caustics, rapidly changing bathymetry, spectral-to-phase coupling, breaking-limited focusing, remote directional validation, adaptive grids and uncertainty propagation into loads and sediment transport.

**Seminal papers.** Snell-law and ray theory established depth refraction; action conservation extended it to currents and spectra, while mild-slope equations introduced diffraction and reflection and later Boussinesq/nonhydrostatic solvers resolved nonlinear phase effects.

## Claims

- **C28.** In the flat-bed mound case, the largest reported MAE was 0.158 at the energy-focusing section and the MBE there was -0.114, indicating local underprediction of dimensionless wave height. *Regime: Vincent-Briggs flat-bed elliptical-mound benchmark and the paper's section definitions..* [direct_finding, mixed] (Shirkavand 2025, [doi:10.1038/s41598-025-23341-z](https://doi.org/10.1038/s41598-025-23341-z))
- **C29.** In the Berkhoff 1:50 sloping-bed mound case, wave height at the focusing section reached 2.2 times the incident height. *Regime: Regular H=4.64 cm, T=1 s wave over the specified rotated elliptical mound on a 1:50 bed..* [direct_finding, mixed] (Shirkavand 2025, [doi:10.1038/s41598-025-23341-z](https://doi.org/10.1038/s41598-025-23341-z))
- **C1276.** Ten months of Hanalei Bay observations and modeling show that episodic long-period swells are preferentially refracted into the reef embayment and drive currents up to an order of magnitude stronger than modal trade-wind conditions. *Regime: Hydrodynamics of a bathymetrically complex fringing coral reef embayment: Wave climate, in situ observations, and wave prediction.* [direct_finding, mixed] (R. K. Hoeke 2011, [doi:10.1029/2010jc006170](https://doi.org/10.1029/2010jc006170))
- **C1541.** Assuming linear wave theory for waves riding on a weak current of 0(ε) compared to the wave phase speed, an approximate dispersion relation is developed to 0(ε2) for arbitrary current U(z) in water of finite depth. *Regime: The study system, forcing, data and methods stated in the indexed abstract..* [literature_review_statement, mixed] (James T. Kirby 1989, [doi:10.1029/jc094ic01p01013](https://doi.org/10.1029/jc094ic01p01013))
- **C1548.** Abstract We apply a coupled circulation‐wave model to simulate extreme sea levels induced by tropical cyclones at the basin scale. *Regime: The study system, forcing, data and methods stated in the indexed abstract..* [literature_review_statement, mixed] (Reza Marsooli 2018, [doi:10.1029/2017jc013434](https://doi.org/10.1029/2017jc013434))
- **C1713.** Characteristic-based regular- and irregular-wave models reproduce current-depth refraction benchmarks, while irregular-wave height is not amplified by following or opposing currents and opposing-current cases show slight overestimation from directional energy leakage. *Regime: Regular and directional irregular waves refracted by one-dimensional following or opposing currents and depth gradients..* [direct_finding, numerical] (YAMAGUCHI 1985, [doi:10.2208/jscej.1985.357_187](https://doi.org/10.2208/jscej.1985.357_187))
- **C1716.** A multidirectional random-wave action-balance model using a QUICK scheme resolves transformation, breaking, and blocking in current fields and reproduces wave-height behavior in caustics and a river-mouth application. *Regime: Directional random waves traveling through spatially varying following or opposing coastal currents, including river-mouth flow..* [direct_finding, numerical] (OKI 2008, [doi:10.2208/proce1989.55.1](https://doi.org/10.2208/proce1989.55.1))
- **C1718.** At the Gunsan-Janghang Harbor entrance, comparison of spectral wind-wave and energy-balance models characterizes wave transformation through a changing reclaimed coastline, islands, shoals, breakwaters, and a long navigation channel. *Regime: Gunsan-Janghang Harbor entrance under reclamation-modified bathymetry, river-mouth shoals, coastal islands, breakwaters, and wind waves..* [direct_finding, mixed] (Lee 2005, [doi:10.5394/kinpr.2005.29.7.627](https://doi.org/10.5394/kinpr.2005.29.7.627))

## Papers

- R. K. Hoeke (2011). Hydrodynamics of a bathymetrically complex fringing coral reef embayment: Wave climate, in situ observations, and wave prediction. *Journal of Geophysical Research*. [doi:10.1029/2010jc006170](https://doi.org/10.1029/2010jc006170)
- YAMAGUCHI (1985). NUMERICAL MODELS FOR WAVE TRANSFORMATION DUE TO CURRENT-DEPTH REFRACTION. *Doboku Gakkai Ronbunshu*. [doi:10.2208/jscej.1985.357_187](https://doi.org/10.2208/jscej.1985.357_187)
- Shirkavand (2025). A 3D non-hydrostatic model for simulating coastal wave transformations: shoaling, diffraction, and refraction. *Scientific Reports*. [doi:10.1038/s41598-025-23341-z](https://doi.org/10.1038/s41598-025-23341-z)
- OKI (2008). Development of Multidirectional Random Wave Transformation Model in Wave-Current Coexisting Field. *PROCEEDINGS OF COASTAL ENGINEERING, JSCE*. [doi:10.2208/proce1989.55.1](https://doi.org/10.2208/proce1989.55.1)
- Lee (2005). Analysis of Numerical Model Wave Predictions for Coastal Waters at Gunsan-Janghang Harbor Entrance. *Journal of Navigation and Port Research*. [doi:10.5394/kinpr.2005.29.7.627](https://doi.org/10.5394/kinpr.2005.29.7.627)
- James T. Kirby (1989). Surface waves on vertically sheared flows: Approximate dispersion relations. *Journal of Geophysical Research Atmospheres*. [doi:10.1029/jc094ic01p01013](https://doi.org/10.1029/jc094ic01p01013)
- Reza Marsooli (2018). Numerical Modeling of Historical Storm Tides and Waves and Their Interactions Along the U.S. East and Gulf Coasts. *Journal of Geophysical Research Oceans*. [doi:10.1029/2017jc013434](https://doi.org/10.1029/2017jc013434)
- W. C. O’Reilly (1993). A comparison of two spectral wave models in the Southern California Bight. *Coastal Engineering*. [doi:10.1016/0378-3839(93)90032-4](https://doi.org/10.1016/0378-3839(93)90032-4)
- Jung (2007). A Practical Application of Multiple Wave Models to the Small Fishery Harbor Entrance. *Journal of Navigation and Port Research*. [doi:10.5394/kinpr.2007.31.7.579](https://doi.org/10.5394/kinpr.2007.31.7.579)
