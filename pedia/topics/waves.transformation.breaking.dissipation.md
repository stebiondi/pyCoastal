# Energy dissipation

`waves.transformation.breaking.dissipation` | Breaking-related energy loss.

Parent: [Waves and wave transformation](waves.md) > [Wave transformation](waves.transformation.md) > [Breaking](waves.transformation.breaking.md)

Papers: 8. Claims: 2. Equations: 2.

## Synthesis

**Well established.** Depth-limited wave breaking removes organized wave energy through turbulence, roller motion, air entrainment, vorticity and heat while transferring momentum that contributes to setup and currents; dissipation rate depends on breaker type, wave statistics, depth and slope.

**Governing physics.** Shoaling increases wave height and steepness until instability; spilling, plunging or surging breakers generate different roller, jet and bubble dynamics. The cross-shore energy balance reflects competition among group-velocity flux convergence, breaking, bottom friction and nonlinear transfers.

**Dimensionless parameters.** Controls include breaker index H/h, wave steepness, surf-similarity or Iribarren number, relative depth kh, roller area, fraction breaking, dissipation normalized by rho g H squared times frequency, slope, Ursell number and air-volume fraction.

**Major equations.** Phase-averaged models balance wave-energy flux with a breaking sink, often based on bore analogies and a fraction of breaking waves; representative-wave methods apply a regular-wave dissipation relation to an irregular RMS height after calibration. Momentum balances use radiation-stress gradients for setup.

**Typical methods.** Studies measure cross-shore wave heights, spectra, setup and velocities in small- and large-scale flumes and field transects, estimate energy-flux gradients, classify breakers, calibrate coefficients on one set and validate on others, and compare errors and shoreline behavior among dissipation closures.

**Numerical models.** The set includes an improved bore-based breaking-dissipation closure and a representative-wave energy-flux model that embeds a regular-wave dissipation formulation with recalibrated coefficients.

**Experimental datasets.** Reviewed evidence spans three experimental datasets used to compare four parametric transformation models and separate small-scale, large-scale and field irregular-wave datasets evaluated with a representative-wave approach.

**Validated ranges.** The improved closure had the smallest wave-height error among four models over three datasets and avoided unphysical nearshore shoaling dominance; the representative-wave approach transferred across small-scale, large-scale and field data only with an appropriate closure and recalibration.

**Recent advances.** Recent advances use stereo/video and radar dissipation fields, bubble and turbulence measurements, data assimilation for bathymetry, LES and VOF breaker energetics, differentiable closure calibration and hybrid phase-resolving/phase-averaged surf-zone models.

**Disagreements.** Bulk bore closures are efficient but compress breaker-type, spectral and intermittency effects; spectral and phase-resolving models offer more detail but require additional closures or resolution. Coefficients calibrated in one scale or beach may not transfer unchanged.

**Limitations.** Current reviewed evidence lacks full parameter tables and direct turbulence, air, roller or heat measurements. Depth, slope, spectrum, scale, reflection, bottom friction and measurement differentiation can confound inferred dissipation, especially near shore.

**Open questions.** Priorities include breaker-type-aware closures, directional and group-scale dissipation, entrained-air and roller coupling, field turbulence budgets, remote dissipation retrieval, breaking–infragravity transfer, nonstationary bathymetry and uncertainty-aware cross-model calibration.

**Seminal papers.** Hydraulic-bore analogies established bulk surf-zone dissipation; Battjes–Janssen-type probabilistic closures represented irregular breaking, roller models improved setup and currents, and later spectral and phase-resolving approaches distributed dissipation in frequency and space.

## Equations

### Wave-energy transformation balance

$$
\nabla\cdot(E\mathbf{C}_g)=-D_b-D_f
$$

Regime: The three reported datasets, a standard initial-breaking ratio gamma and nonsaturated to dissipative surf-zone conditions.

Variables: `E` wave energy density; `C_g` group velocity; `D_b` breaking dissipation; `D_f` bottom-friction or other dissipation

Source: (Alsina 2007, [doi:10.1016/j.coastaleng.2007.05.005](https://doi.org/10.1016/j.coastaleng.2007.05.005))

### Wave-energy transformation balance

$$
\nabla\cdot(E\mathbf{C}_g)=-D_b-D_f
$$

Regime: The compiled experimental conditions and recalibrated dissipation coefficients; results concern cross-shore rms wave height.

Variables: `E` wave energy density; `C_g` group velocity; `D_b` breaking dissipation; `D_f` bottom-friction or other dissipation

Source: (Rattanapitikon 2003, [doi:10.1142/s0578563403000865](https://doi.org/10.1142/s0578563403000865))

## Claims

- **C339.** Adding a previously neglected term to bore-based breaking dissipation prevented shoaling amplification from exceeding dissipation near the shoreline and produced the smallest wave-height error of four compared models across all three experimental datasets. *Regime: The three reported datasets, a standard initial-breaking ratio gamma and nonsaturated to dissipative surf-zone conditions..* [direct_finding, mixed] (Alsina 2007, [doi:10.1016/j.coastaleng.2007.05.005](https://doi.org/10.1016/j.coastaleng.2007.05.005))
- **C342.** Across small-scale, large-scale and field datasets, a representative-wave energy-flux approach reproduced irregular root-mean-square wave-height transformation accurately when paired with an appropriate regular-wave breaking-dissipation model and recalibrated coefficients. *Regime: The compiled experimental conditions and recalibrated dissipation coefficients; results concern cross-shore rms wave height..* [direct_finding, mixed] (Rattanapitikon 2003, [doi:10.1142/s0578563403000865](https://doi.org/10.1142/s0578563403000865))

## Papers

- Alsina (2007). Improved representation of breaking wave energy dissipation in parametric wave transformation models. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2007.05.005](https://doi.org/10.1016/j.coastaleng.2007.05.005)
- Rattanapitikon (2003). Irregular Wave Height Transformation Using Representative Wave Approach. *Coastal Engineering Journal*. [doi:10.1142/s0578563403000865](https://doi.org/10.1142/s0578563403000865)
- Vincent Vuik (2016). Nature-based flood protection: The efficiency of vegetated foreshores for reducing wave loads on coastal dikes. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2016.06.001](https://doi.org/10.1016/j.coastaleng.2016.06.001)
- Devolder (2018). Performance of a buoyancy-modified k-ω and k-ω SST turbulence model for simulating wave breaking under regular waves using OpenFOAM®. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2018.04.011](https://doi.org/10.1016/j.coastaleng.2018.04.011)
- Scott Brown (2016). Evaluation of turbulence closure models under spilling and plunging breakers in the surf zone. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2016.04.002](https://doi.org/10.1016/j.coastaleng.2016.04.002)
- Davide Wüthrich (2021). Strong free-surface turbulence in breaking bores: a physical study on the free-surface dynamics and air–water interfacial features. *Journal of Fluid Mechanics*. [doi:10.1017/jfm.2021.614](https://doi.org/10.1017/jfm.2021.614)
- Rafaël Almar (2018). A new remote predictor of wave reflection based on runup asymmetry. *Estuarine Coastal and Shelf Science*. [doi:10.1016/j.ecss.2018.10.018](https://doi.org/10.1016/j.ecss.2018.10.018)
- Han-Jing Dai (2016). Entrained air in bore-driven swash on an impermeable rough slope. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2016.10.002](https://doi.org/10.1016/j.coastaleng.2016.10.002)
