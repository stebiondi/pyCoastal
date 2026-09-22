# Diffraction

`waves.transformation.diffraction` | Lateral redistribution around obstacles.

Parent: [Waves and wave transformation](waves.md) > [Wave transformation](waves.transformation.md)

Papers: 11. Claims: 5. Equations: 1.

Used by pyCoastal design modules: Harbour agitation.

## Synthesis

**Well established.** Diffraction laterally redistributes wave amplitude and direction when bathymetry or obstacles impose along-crest gradients. It interacts with refraction, shoaling and reflection; coherent phase-resolving methods capture interference, whereas spectral methods require phase-decoupled approximations for random seas.

**Governing physics.** The process follows spatial phase and amplitude gradients governed by dispersion, energy flux and boundary conditions. Important controls are wavelength relative to obstacle/gap scale, water depth, incidence angle, directional spreading, reflection, bathymetric gradients and coherence; focusing can amplify waves locally while shadow zones attenuate them.

**Dimensionless parameters.** Controls include relative depth kh, obstacle or gap width over wavelength, mound length over wavelength, directional spread, propagation angle, reflection coefficient, relative wave height H/h, Ursell number and grid points per wavelength. The improved parabolic model was tested to 70 degrees.

**Major equations.** Foundational formulations are the elliptic mild-slope equation and its parabolic forward-marching approximations. Spectral models augment the action balance with a diffraction turning/diffusion term, while nonhydrostatic models solve free-surface flow directly. Generalized Padé operators improve angular dispersion accuracy.

**Typical methods.** Methods include regular and irregular wave-basin tests, harbor transfer functions, mild-slope finite elements, one-way parabolic marching, phase-decoupled spectral action models, three-dimensional nonhydrostatic solvers and spatial attenuation diagnostics for laterally heterogeneous vegetation or structures.

**Numerical models.** The corpus contains a generalized-[1/1]-Padé parabolic model, a phase-decoupled diffraction extension in SWAN, and a three-dimensional nonhydrostatic solver validated on flat- and sloping-bed mound benchmarks. Each trades phase detail, backscatter capability and computational cost differently.

**Experimental datasets.** Key evidence includes two natural-harbor physical models with irregular wave grouping, Vincent-Briggs and Berkhoff elliptical-mound benchmarks, and controlled laterally heterogeneous vegetation layouts. These probe shadowing, focusing, reflection-diffraction and lateral nonuniformity.

**Validated ranges.** The parabolic model reports tests up to 70-degree propagation. The nonhydrostatic solver reports dimensionless wave-height RMSE of 0.070–0.165 for the flat-bed mound and 0.060–0.114 for the sloping-bed mound, with focusing to 2.2 times incident height in the latter benchmark.

**Recent advances.** Recent nonhydrostatic validation quantifies focusing errors across classic three-dimensional mound tests, while spatial vegetation experiments show that lateral layout controls attenuation uniformity—an engineering manifestation of diffraction and lateral redistribution absent from one-dimensional transmission metrics.

**Disagreements.** Differences largely reflect model scope rather than incompatible physics: phase-decoupled spectral diffraction is intended for random short-crested waves without coherent standing patterns, parabolic models assume predominantly forward propagation, and phase-resolving solvers retain interference but require finer grids and boundary treatment.

**Limitations.** One-way marching misses strong backscatter; spectral closures cannot reproduce coherent phase interference; physical models may have scale and reflection artifacts; Cartesian grids distort curved boundaries; breaking, vegetation wakes and complex natural-reef roughness add dissipation that can be confused with diffraction.

**Open questions.** Priorities are irregular directional-wave benchmarks with combined diffraction, breaking and reflection; robust diffraction closures on unstructured grids; uncertainty from bathymetry and boundary reflection; field validation around reefs and structures; adaptive resolution; and separation of lateral scattering from dissipation.

**Seminal papers.** The 1989 harbor experiments established why irregular-wave diffraction-reflection transfer functions can be more stable within the energetic band. The 2003 phase-decoupled formulation made diffraction compatible with operational spectral wave modeling.

## Equations

### Wave-energy transformation balance

$$
\nabla\cdot(E\mathbf{C}_g)=-D_b-D_f
$$

Regime: Forward-scattered waves and tested incidence/propagation angles up to 70 degrees; backward reflection is outside a one-way marching model.

Variables: `E` wave energy density; `C_g` group velocity; `D_b` breaking dissipation; `D_f` bottom-friction or other dissipation

Source: (Saied 2005, [doi:10.1016/j.coastaleng.2004.10.001](https://doi.org/10.1016/j.coastaleng.2004.10.001))

## Claims

- **C343.** A forward-marching parabolic model using a locally updated generalized [1/1] Padé approximation improved combined refraction-diffraction predictions over complex bathymetry at propagation angles up to 70 degrees relative to earlier rational-approximation parabolic models. *Regime: Forward-scattered waves and tested incidence/propagation angles up to 70 degrees; backward reflection is outside a one-way marching model..* [direct_finding, numerical] (Saied 2005, [doi:10.1016/j.coastaleng.2004.10.001](https://doi.org/10.1016/j.coastaleng.2004.10.001))
- **C1280.** Experiments over a submerged mound measured amplification beyond twice the incident wave and downstream crest reorganization, with cross-wave steepening up to 30% greater than along the principal propagation direction. *Regime: Gravity wave amplification and phase crest re-organization over a shoal.* [direct_finding, experimental] (Nicolas Jarry 2011, [doi:10.5194/nhess-11-789-2011](https://doi.org/10.5194/nhess-11-789-2011))
- **C1570.** The contribution of wave energy to the renewable energy supply is rising. *Regime: The study system, forcing, data and methods stated in the indexed abstract..* [direct_finding, mixed] (Peter Troch 2011, [doi:10.9753/icce.v32.waves.53](https://doi.org/10.9753/icce.v32.waves.53))
- **C1578.** Coastal zones, at the interface between land and sea, face increasing challenges from erosion, sea-level rise, and anthropogenic interventions, necessitating innovative tools for effective management and protection. *Regime: The study system, forcing, data and methods stated in the indexed abstract..* [direct_finding, numerical] (Pietro Scala 2025, [doi:10.3390/w17020269](https://doi.org/10.3390/w17020269))
- **C1581.** The placement and operation of marine energy deployments in the ocean have the potential to change flow patterns, decrease wave heights, and/or remove energy from the oceanographic system. *Regime: The study system, forcing, data and methods stated in the indexed abstract..* [direct_finding, mixed] (Jonathan Whiting 2023, [doi:10.36688/imej.6.45-54](https://doi.org/10.36688/imej.6.45-54))

## Papers

- Nicolas Jarry (2011). Gravity wave amplification and phase crest re-organization over a shoal. *Natural Hazards and Earth System Sciences*. [doi:10.5194/nhess-11-789-2011](https://doi.org/10.5194/nhess-11-789-2011)
- Saied (2005). Improved parabolic water wave transformation model. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2004.10.001](https://doi.org/10.1016/j.coastaleng.2004.10.001)
- Shirkavand (2025). A 3D non-hydrostatic model for simulating coastal wave transformations: shoaling, diffraction, and refraction. *Scientific Reports*. [doi:10.1038/s41598-025-23341-z](https://doi.org/10.1038/s41598-025-23341-z)
- L.H. Holthuijsen (2003). Phase-decoupled refraction–diffraction for spectral wave models. *Coastal Engineering*. [doi:10.1016/s0378-3839(03)00065-6](https://doi.org/10.1016/s0378-3839(03)00065-6)
- Binbin Zhao (2014). High-level Green–Naghdi wave models for nonlinear wave transformation in three dimensions. *Journal of Ocean Engineering and Marine Energy*. [doi:10.1007/s40722-014-0009-8](https://doi.org/10.1007/s40722-014-0009-8)
- Peter Troch (2011). WAKE EFFECTS BEHIND A FARM OF WAVE ENERGY CONVERTERS FOR IRREGULAR LONG-CRESTED AND SHORT-CRESTED WAVES. *Coastal Engineering Proceedings*. [doi:10.9753/icce.v32.waves.53](https://doi.org/10.9753/icce.v32.waves.53)
- Romano-Moreno (2023). Multimodal harbor wave climate characterization based on wave agitation spectral types. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2022.104271](https://doi.org/10.1016/j.coastaleng.2022.104271)
- Pietro Scala (2025). COAST-PROSIM: A Model for Predicting Shoreline Evolution and Assessing the Impacts of Coastal Defence Structures. *Water*. [doi:10.3390/w17020269](https://doi.org/10.3390/w17020269)
- Jonathan Whiting (2023). Effects of small marine energy deployments on oceanographic systems. *International Marine Energy Journal*. [doi:10.36688/imej.6.45-54](https://doi.org/10.36688/imej.6.45-54)
- Wang (2026). Vegetation layouts influence the spatial uniformity of wave attenuation: Laboratory insights. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2025.104937](https://doi.org/10.1016/j.coastaleng.2025.104937)
- Quellet (1989). Wave Grouping Effect in Irregular Wave Agitation in Harbors. *Journal of Waterway, Port, Coastal, and Ocean Engineering*. [doi:10.1061/(asce)0733-950x(1989)115:3(363)](https://doi.org/10.1061/(asce)0733-950x(1989)115:3(363))
