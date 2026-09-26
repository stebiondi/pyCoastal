# Wave transformation

`waves.transformation` | Changes to waves during propagation.

Parent: [Waves and wave transformation](waves.md)

Subtopics: [Breaking](waves.transformation.breaking.md), [Diffraction](waves.transformation.diffraction.md), [Reflection](waves.transformation.reflection.md), [Refraction](waves.transformation.refraction.md), [Shoaling](waves.transformation.shoaling.md)

Papers: 4. Claims: 4. Equations: 3.

## Synthesis

**Well established.** Coastal wave transformation combines shoaling, refraction, diffraction, reflection, nonlinear interaction, breaking and friction as waves encounter changing depth, currents, boundaries and structures; validation must separate these processes and their coupled spatial effects.

**Governing physics.** The reviewed non-hydrostatic approach retains vertical acceleration and dynamic pressure to represent short-wave propagation and three-dimensional vertical structure while solving the free surface with only a few vertical layers.

**Dimensionless parameters.** Controls include kh, relative depth, wave steepness, Ursell and Froude numbers, bathymetric slope and curvature, incidence angle, directional spread, grid cells per wavelength, vertical layer count, Courant number and wave-height or velocity errors normalized by incident conditions.

**Major equations.** Models derive from free-surface mass and momentum conservation with hydrostatic or nonhydrostatic pressure; linear dispersion governs small waves, while nonlinear shallow-water, Boussinesq, multilayer and Navier–Stokes formulations retain increasing dispersion and vertical physics. Wave action governs phase-averaged spectra.

**Typical methods.** The reviewed model uses staggered finite volumes, boundary-fitted vertical layers, time splitting, Godunov-type horizontal advection, and a pressure-correction Poisson solve; validation combines analytical and laboratory comparisons.

**Numerical models.** The reviewed model is a three-dimensional nonhydrostatic finite-volume solver with boundary-fitted vertical layers and pressure correction, verified on standing-wave, elliptical-mound and parabolic-basin tests. It does not implement explicit breaking.

**Experimental datasets.** Two established regular-wave elliptical-mound datasets provide section-wise validation of combined shoaling, refraction, and diffraction on flat and 1:50 sloping backgrounds.

**Validated ranges.** For the flat-bed mound case at H=2.54 cm, T=1.3 s, and kh=1.27, reported dimensionless wave-height RMSE was 0.070-0.165; these values apply only to the specified geometry, two-layer grid, boundaries, and measurement sections. For the 1:50 sloping-bed mound case at H=4.64 cm and T=1 s, reported section-wise dimensionless wave-height RMSE was 0.060-0.114, and the focused wave height at one section reached 2.2 times the incident height.

**Recent advances.** Recent advances use multilayer nonhydrostatic and high-order unstructured schemes, adaptive phase-resolving nests, GPU acceleration, data assimilation, learned closures and benchmark suites that compare free surface, velocity, conservation and spatial focusing jointly.

**Disagreements.** Hydrostatic models are efficient for long waves but miss short-wave dispersion; Boussinesq and nonhydrostatic models extend dispersion at moderate cost; RANS/VOF resolves breaking and air at much higher cost. Good aggregate height skill can conceal local focusing or velocity errors.

**Limitations.** The current evidence does not validate breaking waves: all four reported tests are non-breaking and the model has no explicit breaking treatment. Accuracy is spatially nonuniform and can degrade where focusing, refraction, and diffraction interact or where a Cartesian mesh represents circular geometry; low global or section-averaged error does not imply uniform local accuracy.

**Open questions.** Reviewed evidence is still missing for irregular spectra, breaking and post-breaking transformation, currents, real bathymetry, coastal structures, field observations, and long-duration three-dimensional applications.

**Seminal papers.** Linear shoaling and Snell refraction established reduced transformation theory; mild-slope equations unified refraction and diffraction, Boussinesq equations added nonlinear dispersion, and nonhydrostatic and Navier–Stokes solvers broadened vertical and breaking physics.

## Equations

### Boundary-fitted vertical layer thickness

$$
d_p=f_p D=f_p(\eta+h),\quad 0<f_p<1,\quad \sum_p f_p=1
$$

Regime: Moving free surface on the paper's vertically boundary-fitted grid.

Variables: `d_p` thickness of layer p; `f_p` fixed fraction of total depth assigned to layer p; `D` total water depth; `eta` free-surface elevation; `h` still-water depth

Source: (Shirkavand 2025, [doi:10.1038/s41598-025-23341-z](https://doi.org/10.1038/s41598-025-23341-z))

### Flat-bed elliptical-mound bathymetry

$$
h=0.9144-0.762\sqrt{1-(x/3.81)^2-(y/4.95)^2}
$$

Regime: Vincent-Briggs submerged-mound validation inside (x/3.05)^2+(y/3.96)^2=1.

Variables: `h` still-water depth inside the elliptical boundary; `x` longitudinal coordinate; `y` transverse coordinate

Source: (Shirkavand 2025, [doi:10.1038/s41598-025-23341-z](https://doi.org/10.1038/s41598-025-23341-z))

### Parabolic-basin bed

$$
z_b=-h_0(1-r^2/R^2),\quad r=\sqrt{x^2+y^2}
$$

Regime: Thacker long-wave resonance and wet/dry analytical benchmark.

Variables: `z_b` bed elevation; `h_0` central depth scale; `R` basin radius parameter; `r` radial coordinate

Source: (Shirkavand 2025, [doi:10.1038/s41598-025-23341-z](https://doi.org/10.1038/s41598-025-23341-z))

## Claims

- **C26.** In the 10 m cubic standing-wave test, the model's free-surface residual relative to the analytical solution remained within plus or minus 0.005 m using five vertical layers. *Regime: Closed deep-water standing-wave benchmark; 0.5 m horizontal cells, five uniform layers, and 0.05 s time step..* [direct_finding, numerical] (Shirkavand 2025, [doi:10.1038/s41598-025-23341-z](https://doi.org/10.1038/s41598-025-23341-z))
- **C27.** For the Vincent-Briggs flat-bed elliptical-mound experiment, the present model's dimensionless wave-height RMSE ranged from 0.070 to 0.165 and was lower than both compared models at every section where all three reported values. *Regime: Regular H=2.54 cm, T=1.3 s, kh=1.27 wave; 0.457 m outer depth; two layers; specified mound and basin boundaries..* [direct_finding, mixed] (Shirkavand 2025, [doi:10.1038/s41598-025-23341-z](https://doi.org/10.1038/s41598-025-23341-z))
- **C30.** For the sloping-bed mound benchmark, the present model's dimensionless wave-height RMSE across eight sections ranged from 0.060 to 0.114. *Regime: Berkhoff regular-wave benchmark with H=4.64 cm, T=1 s, 1:50 slope, two vertical layers, and specified grids and boundaries..* [direct_finding, mixed] (Shirkavand 2025, [doi:10.1038/s41598-025-23341-z](https://doi.org/10.1038/s41598-025-23341-z))
- **C31.** In the Thacker parabolic-basin test with two vertical layers, reported free-surface RMSE was below 0.04 and radial-velocity RMSE below 0.07 at all four evaluated phases. *Regime: Frictionless parabolic basin with h0=1 m, r0=2000 m, R=2500 m, 20 m grid, 2 s step, and 1e-5 m wet/dry threshold..* [direct_finding, analytical] (Shirkavand 2025, [doi:10.1038/s41598-025-23341-z](https://doi.org/10.1038/s41598-025-23341-z))

## Papers

- Shirkavand (2025). A 3D non-hydrostatic model for simulating coastal wave transformations: shoaling, diffraction, and refraction. *Scientific Reports*. [doi:10.1038/s41598-025-23341-z](https://doi.org/10.1038/s41598-025-23341-z) [published version, CC BY](https://d-nb.info/1386515426/34)
- Luigi Cavaleri (2007). Wave modelling – The state of the art. *Progress In Oceanography*. [doi:10.1016/j.pocean.2007.05.005](https://doi.org/10.1016/j.pocean.2007.05.005) [accepted manuscript, read only](http://nora.nerc.ac.uk/id/eprint/2732/1/WISE_the_state_of_the_art.pdf)
- Rong Zhang (2023). Experimental investigation of wave attenuation by mangrove forests with submerged canopies. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2023.104403](https://doi.org/10.1016/j.coastaleng.2023.104403) [accepted manuscript, read only](https://repository.tudelft.nl/file/File_074d9118-701b-4b51-a286-87dfdffe8a57)
- Lu (2016). Depth-averaged non-hydrostatic numerical modeling of nearshore wave propagations based on the FORCE scheme. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2016.04.004](https://doi.org/10.1016/j.coastaleng.2016.04.004)
