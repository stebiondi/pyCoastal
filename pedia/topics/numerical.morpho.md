# Morphodynamic models

`numerical.morpho` | Coupled flow-sediment-bed models.

Parent: [Numerical modeling](numerical.md)

Papers: 9. Claims: 5. Equations: 0.

## Synthesis

**Well established.** Process-based coastal morphodynamic models couple hydrodynamics, sediment transport and bed updating through feedback: flow moves sediment, divergence changes elevation, and the changed bed modifies subsequent waves and currents. Calibration fit alone does not establish predictive skill.

**Governing physics.** Bed evolution reflects gradients in bedload and suspended transport driven by waves, currents, runup and gravity, with feedback through water depth, breaking, circulation and inlet exchange; relevant scales range from intra-wave transport to seasonal and engineering evolution.

**Dimensionless parameters.** Controls include Shields mobility, relative grain size, fall-velocity and suspension parameters, wave asymmetry and skewness, surf similarity, sediment Courant number, morphological acceleration factor, active-layer thickness ratios and normalized bed or shoreline error.

**Major equations.** The core system combines hydrodynamic mass and momentum equations, sediment advection–diffusion or bulk transport formulae, and the Exner bed-continuity equation, often with separate cross-shore and longshore components, wetting/drying, avalanching and porosity corrections.

**Typical methods.** Workflows define sediment classes and closures, spin up hydrodynamics, couple transport and Exner updating, test conservation and morphological time step, calibrate a constrained subset, validate against independent profiles or volumes at multiple scales, and audit parameter plausibility and boundary flux.

**Numerical models.** The evidence spans a cross-shore storm-profile model, coupled cross-/longshore inlet morphodynamics, weak phase-resolving-wave to wave-averaged-sediment coupling, and reduced linear, exponential, one-line and combined nourishment-evolution models.

**Experimental datasets.** Reviewed evidence includes storm-profile erosion, Wilson Inlet waves–currents–bed observations, multiple laboratory benchmarks plus Pescara Harbor evolution, and post-nourishment volume series at Folly Beach and Hunting Island.

**Validated ranges.** Current evidence is case-bound to sandy storm profiles, one microtidal wave-dominated seasonal inlet, laboratory tests and one harbor coast, and two South Carolina nourishment sites; it does not establish universal closures or acceleration factors.

**Recent advances.** Recent work emphasizes weak multiscale coupling, phase-resolving forcing of longer-term transport, probabilistic ensembles, scale-aware skill metrics, data assimilation and efficient reduced emulators while retaining conservation and physically constrained parameters.

**Disagreements.** Detailed process models represent more feedback but accumulate closure and numerical uncertainty, whereas reduced models can be robust for aggregate volume or shoreline response yet omit inlets, cross-shore exchange and event sequencing. Similar fit can coexist with physically implausible parameters.

**Limitations.** Limitations include uncertain transport formulae, compensating calibration, sparse subaqueous observations, boundary sediment flux, scale-dependent skill, numerical diffusion, morphological acceleration, bed-layer and wet/dry choices, storm sequencing and weak transfer across grain sizes and coast types.

**Open questions.** Priorities include scale-selective validation, probabilistic structural uncertainty, mixed and cohesive sediment, event-to-decadal acceleration, coupled inlet–beach exchange, climate nonstationarity, observation updating and reliable extrapolation beyond calibration conditions.

**Seminal papers.** Exner bed continuity, energetics and equilibrium-profile concepts, one-line shoreline diffusion and early coupled wave–current–sediment models established the hierarchy from reduced shoreline response to process-based area morphodynamics.

## Claims

- **C119.** Leont'yev's storm-profile model decomposes total cross-shore transport into wave/current and runup components, using only runup transport in swash, only wave/current transport in shoaling water, and both in the surf zone. *Regime: The proposed 1996 short-term sandy beach-profile model; coefficients and tested forcing ranges are unavailable from the abstract..* [direct_finding, numerical] (Leont'yev 1996, [doi:10.1016/s0378-3839(96)00029-4](https://doi.org/10.1016/s0378-3839(96)00029-4))
- **C138.** A weakly coupled phase-resolving hydrodynamic and wave-averaged sediment model was validated against multiple experiments and reproduced long-term bed evolution opposite Pescara Harbor. *Regime: The model's articulated coastal grids, tested sediment closures, and Pescara Harbor case..* [direct_finding, mixed] (Gallerano 2016, [doi:10.1142/s057856341650011x](https://doi.org/10.1142/s057856341650011x))
- **C1384.** Tidal-basin morphodynamic modeling shows sea-level rise reorganizes channel-flat morphology and sediment demand through coupled hydrodynamic and bed-evolution feedbacks. *Regime: Numerical modeling of the impact of sea level rise on tidal basin morphodynamics.* [direct_finding, numerical] (Mick van der Wegen 2013, [doi:10.1002/jgrf.20034](https://doi.org/10.1002/jgrf.20034))
- **C1530.** In the LIP profile tests, the model reproduced two nearshore bars that migrated about 7 m seaward, with initial crest heights near 0.10 and 0.12 m. *Regime: LIP fine-sand regular-wave profile tests 1a and 1b..* [direct_finding, experimental] (Gallerano 2016, [doi:10.1142/s057856341650011x](https://doi.org/10.1142/s057856341650011x))
- **C1531.** For the 1997–2000 Pescara hindcast, simulated annual settlement was about 38,500 m³/year versus about 40,000 m³/year inferred from bathymetric surveys. *Regime: Pescara Harbor under the dominant 1.5 m wave class and modeled 1997 bathymetry..* [direct_finding, mixed] (Gallerano 2016, [doi:10.1142/s057856341650011x](https://doi.org/10.1142/s057856341650011x))

## Papers

- Mick van der Wegen (2013). Numerical modeling of the impact of sea level rise on tidal basin morphodynamics. *Journal of Geophysical Research Earth Surface*. [doi:10.1002/jgrf.20034](https://doi.org/10.1002/jgrf.20034) [published version, read only](https://onlinelibrary.wiley.com/doi/pdfdirect/10.1002/jgrf.20034)
- Gallerano (2016). Modeling Bed Evolution Using Weakly Coupled Phase-Resolving Wave Model and Wave-Averaged Sediment Transport Model. *Coastal Engineering Journal*. [doi:10.1142/s057856341650011x](https://doi.org/10.1142/s057856341650011x) [published version, CC BY](https://www.tandfonline.com/doi/pdf/10.1142/S057856341650011X?needAccess=true)
- Arthur Robinet (2018). A reduced-complexity shoreline change model combining longshore and cross-shore processes: The LX-Shore model. *Environmental Modelling & Software*. [doi:10.1016/j.envsoft.2018.08.010](https://doi.org/10.1016/j.envsoft.2018.08.010) [submitted manuscript, read only](https://brgm.hal.science/hal-02734892v1/file/Manuscript_PostPrint.pdf)
- Zhou (2016). Is “Morphodynamic Equilibrium” an oxymoron?. *Earth-Science Reviews*. [doi:10.1016/j.earscirev.2016.12.002](https://doi.org/10.1016/j.earscirev.2016.12.002) [accepted manuscript, read only](https://eprints.soton.ac.uk/406579/1/equilibriumESRrev2.pdf)
- D.M.P.K. Dissanayake (2012). The morphological response of large tidal inlet/basin systems to relative sea level rise. *Climatic Change*. [doi:10.1007/s10584-012-0402-z](https://doi.org/10.1007/s10584-012-0402-z) [published version, read only](https://repository.tudelft.nl/file/File_7c6d7fed-e3ea-4507-a743-ea365a73ccb2)
- Linlin Li (2012). Numerical modeling of the morphological change in Lhok Nga, west Banda Aceh, during the 2004 Indian Ocean tsunami: understanding tsunami deposits using a forward modeling method. *Natural Hazards*. [doi:10.1007/s11069-012-0325-z](https://doi.org/10.1007/s11069-012-0325-z) [published version, read only](https://link.springer.com/content/pdf/10.1007/s11069-012-0325-z.pdf)
- Ranasinghe (1999). The seasonal closure of tidal inlets: Wilson Inlet—a case study. *Coastal Engineering*. [doi:10.1016/s0378-3839(99)00007-1](https://doi.org/10.1016/s0378-3839(99)00007-1) [published version, read only](https://www.researchgate.net/publication/222507097_The_seasonal_closure_of_tidal_inlets_Wilson_Inlet-A_case_study)
- Leont'yev (1996). Numerical modelling of beach erosion during storm event. *Coastal Engineering*. [doi:10.1016/s0378-3839(96)00029-4](https://doi.org/10.1016/s0378-3839(96)00029-4)
- Weathers (2013). Evaluation of Beach Nourishment Evolution Models Using Data from Two South Carolina, USA Beaches: Folly Beach and Hunting Island. *Journal of Coastal Research*. [doi:10.2112/si_69_7](https://doi.org/10.2112/si_69_7)
