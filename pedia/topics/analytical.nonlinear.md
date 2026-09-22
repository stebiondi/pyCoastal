# Nonlinear and asymptotic theory

`analytical.nonlinear` | Perturbation and nonlinear solutions.

Parent: [Analytical methods](analytical.md)

Papers: 4. Claims: 2. Equations: 0.

## Synthesis

**Well established.** Nonlinear coastal theory is useful when finite amplitude, shallow depth, moving shorelines, wave asymmetry, harmonic coupling, dispersion, or morphology feedback invalidate linear superposition. Its value depends on explicit ordering assumptions and validation inside the retained regime.

**Governing physics.** Key mechanisms are finite-amplitude kinematics and dynamic boundary conditions, weak dispersion, quadratic and higher-order harmonic coupling, free-bound interference, nonlinear shoaling and runup, moving wet-dry boundaries, wave-current diffusion, settling lag, and feedback toward or away from morphological equilibrium.

**Dimensionless parameters.** Approximation choice is organized by wave steepness, relative depth kh, Ursell number, relative amplitude H/h, dispersion and nonlinearity orders, surf similarity, Froude number, Shields parameter, suspension number, settling-to-advection time ratio, and morphology relaxation time.

**Major equations.** Principal frameworks include nonlinear shallow-water equations, Boussinesq and extended mild-slope equations, Stokes and perturbation expansions, eigenfunction wavemaker solutions, asymptotic convection-diffusion reductions, exact Lagrangian seiche solutions, stochastic half-cycle transport, and dynamic-equilibrium profile laws.

**Typical methods.** Methods derive ordered reduced equations, exact or semi-analytical solutions, matched or regular perturbation expansions, spectral/eigenfunction decompositions, stochastic averaging, equilibrium stability analysis, and comparisons with laboratory, field, or higher-dimensional numerical solutions.

**Numerical models.** Reviewed implementations include semi-analytical eigenfunction-FFT wavemakers, higher-order Boussinesq solvers, nonlinear shallow-water inundation models, SWAN phase-decoupled diffraction, quasi-3-D transport, exact seiche benchmarks, stochastic bedload models, and dynamic-equilibrium shoreline models.

**Experimental datasets.** Theory has been checked against transient-wave flumes, Tainan nonlinear shoaling tests, Synolakis plane-beach and Briggs conical-island runup, Monai valley inundation, current-wave suspended-transport measurements, and multi-year shoreline or inlet observations.

**Validated ranges.** Examples include Tainan H=0.05-0.40 m and T=2-5 s, plane-beach H/d=0.021-0.626 with breaking above 0.045 on a 1:19.85 slope, conical-island H/d=0.10 and 0.20, narrow-band second-order random waves, and source-specific low-to-steep wavemaker tests.

**Recent advances.** Recent work combines free-bound harmonic separation, nonlinear spectral diagnostics, stochastic transport, benchmark-driven model hierarchies, and dynamic-equilibrium reduced models to retain essential physics while remaining efficient enough for design or forecasting.

**Disagreements.** A reduced model may solve its parent equations accurately yet omit decisive physics. Linear or weakly nonlinear wavemaker theory fails at higher steepness; nonlinear shallow-water theory cannot reproduce dispersive or post-breaking behavior; local linear wavelengths can misinterpret free-bound spatial beating.

**Limitations.** Asymptotic truncation, idealized geometry, inviscid or hydrostatic assumptions, weak dispersion, prescribed profile shape, unidirectionality, nonbreaking conditions, friction closure, and scale separation constrain transfer. Mathematical existence alone does not establish coastal relevance.

**Open questions.** Needs include uniform theories across shoaling, breaking and runup; multidirectional and current-coupled nonlinear interactions; error bounds for truncation and closure; efficient stochastic extremes; sediment and morphology coupling; and principled switching among reduced and process-resolving models.

**Seminal papers.** Within the reviewed corpus, exact shallow-water shoreline benchmarks, Boussinesq runup validation, mild-slope-derived diffraction, quasi-3-D transport asymptotics, and nonlinear wavemaker theory form reusable analytical foundations across coastal applications.

## Claims

- **C1501.** Sine-Gordon and generalized Kudryashov methods yield soliton solutions of the Boussinesq equation used for weakly nonlinear long waves in harbors and shallow seas. *Regime: Soliton solutions to the Boussinesq equation through sine-Gordon method and Kudryashov method.* [direct_finding, analytical] (M. Ali Akbar 2021, [doi:10.1016/j.rinp.2021.104228](https://doi.org/10.1016/j.rinp.2021.104228))
- **C1503.** Nonlinear WKB and perturbation analyses show a convex non-reflecting beach generates higher harmonics during wave propagation. *Regime: Nonlinear wave effects at the non-reflecting beach.* [direct_finding, analytical] (Ira Didenkulova 2012, [doi:10.5194/npg-19-1-2012](https://doi.org/10.5194/npg-19-1-2012))

## Papers

- M. Ali Akbar (2021). Soliton solutions to the Boussinesq equation through sine-Gordon method and Kudryashov method. *Results in Physics*. [doi:10.1016/j.rinp.2021.104228](https://doi.org/10.1016/j.rinp.2021.104228)
- Ira Didenkulova (2012). Nonlinear wave effects at the non-reflecting beach. *Nonlinear processes in geophysics*. [doi:10.5194/npg-19-1-2012](https://doi.org/10.5194/npg-19-1-2012)
- Jara (2015). Shoreline evolution model from a dynamic equilibrium beach profile. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2015.02.006](https://doi.org/10.1016/j.coastaleng.2015.02.006)
- Uma (2016). A wavelet approach for computing nonlinear wave–wave interactions in discrete spectral wave models. *Journal of Ocean Engineering and Marine Energy*. [doi:10.1007/s40722-015-0041-3](https://doi.org/10.1007/s40722-015-0041-3)
