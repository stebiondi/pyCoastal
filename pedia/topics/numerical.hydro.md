# Hydrodynamic circulation models

`numerical.hydro` | Depth-averaged and three-dimensional circulation.

Parent: [Numerical modeling](numerical.md)

Papers: 7. Claims: 6. Equations: 2.

## Synthesis

**Well established.** Coastal hydrodynamic models solve conservation of water mass and momentum under approximations matched to scale: depth-integrated shallow-water equations for long waves and vertically mixed flows, multilayer or three-dimensional hydrostatic models for stratification and shear, and nonhydrostatic or phase-resolving models where vertical acceleration matters.

**Governing physics.** Pressure gradients, gravity, Coriolis acceleration, advection, bed and surface stress, turbulence, density gradients, tides, wind, waves and boundary fluxes control circulation; wetting and drying, breaking, bores and hydraulic transitions introduce strong nonlinearities and numerical constraints.

**Dimensionless parameters.** Controls include Froude, Rossby, Reynolds and Richardson numbers, relative depth, aspect ratio, stratification and baroclinic Rossby radius, bottom-drag coefficient, Courant number, grid Peclet number, wetting threshold and normalized mass and energy errors.

**Major equations.** Core equations are free-surface continuity and horizontal momentum, optionally coupled to hydrostatic vertical structure, tracer transport, turbulence closure and wave radiation stresses. Conservative finite-volume or finite-difference forms must balance storage and boundary fluxes and preserve physically meaningful momentum across wet/dry fronts.

**Typical methods.** Workflows select dimensionality from the physics, construct datum-consistent bathymetry and boundaries, verify analytic waves and basins, test conservation and grid/time convergence, validate laboratory and field water levels and velocities, audit phase and extrema separately and document stabilization, friction and wet/dry sensitivity.

**Numerical models.** The reviewed implementation is UBO-TSUFD, a nonlinear shallow-water finite-difference model with inundation capability, evaluated within a broader tsunami verification and validation framework that supplies analytic, laboratory, conservation and operational tests.

**Experimental datasets.** Reviewed evidence includes analytical shoreline-motion and oscillating-basin cases, mass-conservation tests, the Monai laboratory tsunami benchmark and formal operational verification criteria. Direct circulation, tide and wetland datasets remain in the lawful-full-text queue.

**Validated ranges.** Support covers selected long-wave analytical and laboratory regimes and Monai behavior through 30 s. It does not validate post-breaking flow, stratified three-dimensional circulation, wave-resolving dynamics or arbitrary wetting/drying configurations.

**Recent advances.** Recent advances use unstructured high-order and discontinuous Galerkin methods, GPU acceleration, adaptive meshes, locally three-dimensional or nonhydrostatic patches, conservative subgrid structures, ensemble data assimilation and reproducible benchmark suites.

**Disagreements.** Depth-integrated models offer efficiency and horizontal resolution but omit vertical shear and baroclinicity; three-dimensional models add physics at greater data, closure and computational cost. Numerical robustness obtained through excess drag or diffusion can conflict with physical fidelity.

**Limitations.** Bathymetric and boundary uncertainty, wet/dry thresholds, turbulence and friction closure, numerical diffusion and dispersion, stability-driven tuning, unresolved breaking, grid anisotropy and incomplete conservation audits can produce plausible levels with incorrect velocities, fluxes or inundation.

**Open questions.** Priorities include conservative multiscale nesting, robust positivity without artificial drag, adaptive dimensionality, coupled baroclinic–wave–sediment physics, uncertainty-aware boundary assimilation, differentiable calibration and validation metrics that expose compensating errors.

**Seminal papers.** Saint-Venant shallow-water equations established depth-integrated long-wave modeling; primitive-equation coastal ocean models introduced sigma coordinates and turbulence closures, while finite-volume Riemann methods advanced conservative shocks, bores and wetting/drying.

## Equations

### Depth-integrated continuity equation

$$
\frac{\partial \eta}{\partial t}+\frac{\partial M}{\partial x}+\frac{\partial N}{\partial y}=0
$$

Regime: Nonlinear shallow-water formulation in Cartesian coordinates.

Variables: `eta` surface elevation; `M` x discharge flux u(h+eta); `N` y discharge flux v(h+eta)

Source: (Tinti 2013, [doi:10.5194/nhess-13-1795-2013](https://doi.org/10.5194/nhess-13-1795-2013))

### Manning bottom-friction component

$$
f_x=\frac{g n^2}{D^{7/3}}M\sqrt{M^2+N^2}
$$

Regime: Depth-averaged bottom friction; only the laboratory benchmark tests this implementation.

Variables: `n` Manning roughness; `D` total water column; `M,N` discharge fluxes

Source: (Tinti 2013, [doi:10.5194/nhess-13-1795-2013](https://doi.org/10.5194/nhess-13-1795-2013))

## Claims

- **C12.** UBO-TSUFD reproduced the selected analytical shoreline-motion, oscillating-basin, mass-conservation, and laboratory tsunami benchmarks with generally satisfactory agreement. *Regime: The four paper-specific benchmarks on single structured grids; this does not validate nested grids, landslide generation, dispersive physics, or wave breaking..* [direct_finding, mixed] (Tinti 2013, [doi:10.5194/nhess-13-1795-2013](https://doi.org/10.5194/nhess-13-1795-2013))
- **C13.** The nonlinear shallow-water model reproduced the Monai laboratory arrival and inundation behavior through 30 s but was not compared later because breaking waves are outside its physics. *Regime: Matsuyama-Tanaka Monai Valley benchmark, 5.446 x 3.406 m region, maximum depth 0.135 m; pre-breaking interval through 30 s..* [direct_finding, mixed] (Tinti 2013, [doi:10.5194/nhess-13-1795-2013](https://doi.org/10.5194/nhess-13-1795-2013))
- **C20.** A tsunami-model mass audit should integrate disturbed free-surface elevation and account for open-boundary fluxes; integrating total depth can mask numerical errors offshore. *Regime: Depth-integrated water-wave computations with closed, open, or absorbing boundaries..* [direct_finding, analytical] (Synolakis 2008, [doi:10.1007/s00024-004-0427-y](https://doi.org/10.1007/s00024-004-0427-y))
- **C24.** Ad hoc friction factors introduced mainly to stabilize marginally stable inundation computations create reliability that cannot be known a priori outside tested cases. *Regime: Numerical inundation models using empirically adjusted friction primarily for stability..* [literature_review_statement, review] (Synolakis 2008, [doi:10.1007/s00024-004-0427-y](https://doi.org/10.1007/s00024-004-0427-y))
- **C1374.** Modeling 0.5–1.0 m sea-level rise over 1–2 m reef flats increases waves, setup, shear, resuspension and offshore sediment flux while reducing sediment residence time and light availability. *Regime: Numerical modeling of the impact of sea-level rise on fringing coral reef hydrodynamics and sediment transport.* [direct_finding, numerical] (Curt D. Storlazzi 2011, [doi:10.1007/s00338-011-0723-9](https://doi.org/10.1007/s00338-011-0723-9))
- **C1608.** A finite-element formulation solves layer-averaged circulation for two vertically homogeneous coastal layers, retaining interfacial exchange and density-driven structure absent from a single-layer model. *Regime: FINITE ELEMENT MODEL OF TWO LAYER COASTAL CIRCULATION.* [direct_finding, numerical] (Wang 1974, [doi:10.9753/icce.v14.141](https://doi.org/10.9753/icce.v14.141))

## Papers

- Curt D. Storlazzi (2011). Numerical modeling of the impact of sea-level rise on fringing coral reef hydrodynamics and sediment transport. *Coral Reefs*. [doi:10.1007/s00338-011-0723-9](https://doi.org/10.1007/s00338-011-0723-9) [published version, CC BY-NC](https://link.springer.com/content/pdf/10.1007/s00338-011-0723-9.pdf)
- Wang (1974). FINITE ELEMENT MODEL OF TWO LAYER COASTAL CIRCULATION. *Coastal Engineering Proceedings*. [doi:10.9753/icce.v14.141](https://doi.org/10.9753/icce.v14.141) [published version, CC BY](https://journals.tdl.org/icce/index.php/icce/article/download/3036/2701)
- Synolakis (2008). Validation and Verification of Tsunami Numerical Models. *Pure and Applied Geophysics*. [doi:10.1007/s00024-004-0427-y](https://doi.org/10.1007/s00024-004-0427-y) [published version, read only](https://nctr.pmel.noaa.gov/Pdf/PAGEOPH_Synolakis_etal_2008.pdf)
- Tinti (2013). The UBO-TSUFD tsunami inundation model: validation and application to a tsunami case study focused on the city of Catania, Italy. *Natural Hazards and Earth System Sciences*. [doi:10.5194/nhess-13-1795-2013](https://doi.org/10.5194/nhess-13-1795-2013) [published version, CC BY](https://nhess.copernicus.org/articles/13/1795/2013/nhess-13-1795-2013.pdf)
- Jean Liénard (2016). Efficient three-dimensional reconstruction of aquatic vegetation geometry: Estimating morphological parameters influencing hydrodynamic drag. *Estuarine Coastal and Shelf Science*. [doi:10.1016/j.ecss.2016.05.011](https://doi.org/10.1016/j.ecss.2016.05.011) [published version, read only](https://wpcdn.web.wsu.edu/wp-vancouverlabs/uploads/sites/1204/2017/01/PublishedVegPhotos.pdf)
- Marcellin Samou Seujip (2024). Impact of mangrove on tidal propagation in a tropical coastal lagoon. *Environmental Earth Sciences*. [doi:10.1007/s12665-023-11349-5](https://doi.org/10.1007/s12665-023-11349-5) [submitted manuscript, read only](https://univ-rochelle.hal.science/hal-04882993v1/document)
- Yuanchi Xiao (2019). The development and evolution of the Burdekin River estuary freshwater plume during Cyclone Debbie (2017). *Estuarine Coastal and Shelf Science*. [doi:10.1016/j.ecss.2019.04.037](https://doi.org/10.1016/j.ecss.2019.04.037) [submitted manuscript, read only](https://unsworks.unsw.edu.au/bitstreams/60df5c18-d0a4-4702-aa30-a9f58a4633c1/download)
