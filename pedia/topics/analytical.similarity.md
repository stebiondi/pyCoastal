# Similarity and scaling analysis

`analytical.similarity` | Dimensional and similarity methods.

Parent: [Analytical methods](analytical.md)

Papers: 9. Claims: 8. Equations: 0.

## Synthesis

**Well established.** Physical-model similarity requires matching dominant nondimensional controls; geometric resemblance alone does not guarantee dynamic similarity when gravity, viscosity, elasticity, air entrainment, granular drag, structural response, or power conversion compete.

**Governing physics.** Froude scaling preserves gravity-inertia balance, Reynolds scaling represents viscous effects, Cauchy-type controls represent elastic-fluid interaction, and power similarity governs energy-conversion stages; exact simultaneous similitude is often impossible.

**Dimensionless parameters.** Reviewed controls include slide Froude number, relative slide thickness and mass, grain Reynolds number, Cauchy and WFSI parameters, fence porosity and relative thickness, and stage-specific power ratios.

**Major equations.** Core tools are Buckingham-Pi dimensional analysis and model-prototype scale ratios for length, time, velocity, force, pressure, stiffness, power, Froude number, Reynolds number, Cauchy number, and process-specific relative geometry.

**Typical methods.** Methods combine multi-scale flume tests, systematic parameter variation, prototype-model numerical comparison, discrete-element or hydrodynamic simulation, calibration, uncertainty/error estimation, and mechanism-by-mechanism scaling orchestration.

**Numerical models.** Numerical support includes discrete-element slide simulations, prototype/model wave-flexible-plate simulations, SWASH fence upscaling, and process-decomposed WEC scaling frameworks.

**Experimental datasets.** Evidence includes 144 block-slide tests, factor-four granular-slide tests in a 6 m apparatus, plate-impact models up to 40 times smaller, 1:5 wooden-fence tests, and three WEC PTO case studies.

**Validated ranges.** Reported bounds include wave-height effects up to a factor two from block-slide parameters, granular velocity and runout effects of 35% and 26%, breaking-pressure errors to 132%, displacement errors to 98%, new WFSI deviations below 4.3%, and fence scale bias near 5%.

**Recent advances.** Recent work uses paired numerical and physical models to quantify rather than merely note scale effects, proposes partial-parameter WFSI scaling, orchestrates similarity across energy-conversion stages, and separates scale bias from design-variable effects.

**Disagreements.** Rigid landslide blocks do not necessarily generate larger waves than granular slides, and a scaling law adequate for nonbreaking loads can fail badly for breaking pressure or flexible response. Apparent disagreement reflects unmatched secondary physics and response choice.

**Limitations.** Abstract-level evidence, laboratory confinement, finite scale range, unscaled air or fluid properties, particle stiffness, material substitution, simplified PTO behavior, and incomplete prototype validation bound transfer.

**Open questions.** Needs include optimal multi-physics scale selection, principled distortion correction, uncertainty propagation to prototypes, shared multi-scale benchmarks, and field validation for breaking impacts, nature-based structures, slides, and energy devices.

**Seminal papers.** Classical Froude similitude and Buckingham-Pi analysis provide the foundation; the reviewed corpus demonstrates why Reynolds, elasticity, grain-air, porosity, and power constraints must be added for specific coastal processes.

## Claims

- **C373.** Across 144 Froude-model block-slide tests, slide Froude number, relative thickness, and relative mass changed wave amplitude and height by as much as a factor of two, and rigid blocks did not systematically generate larger waves than deformable granular slides. *Regime: Systematic variation of slide Froude number, relative thickness, and relative mass in physical landslide-tsunami models..* [direct_finding, experimental] (Valentin Heller 2013, [doi:10.1002/jgrc.20099](https://doi.org/10.1002/jgrc.20099))
- **C374.** For wave impacts on plates modeled at scales down to 1:40, precise Froude scaling removed detectable scale effects, whereas unscaled fluid properties produced breaking-pressure errors up to 132% and traditional Froude scaling underestimated displacement by up to 98%; a new WFSI approach kept validated peak deviations below 4.3%. *Regime: Rigid and flexible plates under breaking and non-breaking regular and solitary waves, with models up to 40 times smaller..* [direct_finding, mixed] (Tommaso Attili 2023, [doi:10.1016/j.jfluidstructs.2023.103987](https://doi.org/10.1016/j.jfluidstructs.2023.103987))
- **C375.** A review of wave-energy-converter power-take-off experiments found that credible small-scale reproduction requires explicit setup enhancement, calibration, and error estimation, with some recommendations transferable across technologies despite device-specific scaling choices. *Regime: Small-scale wave-energy-converter PTO experiments across technology-dependent configurations..* [literature_review_statement, review] (Gianmaria Giannini 2020, [doi:10.3390/jmse8090632](https://doi.org/10.3390/jmse8090632))
- **C376.** For oscillating-buoy wave-energy-converter model tests, the proposed orchestration applies Froude similarity to the water-contacting capture stage and power similarity to later conversion stages without requiring their geometric similitude. *Regime: Oscillating-buoy WEC model tests decomposed into capture and downstream conversion stages..* [direct_finding, analytical] (Dongsheng Qiao 2021, [doi:10.3389/fmars.2021.627453](https://doi.org/10.3389/fmars.2021.627453))
- **C377.** For porosity-0.81 wooden fences, a SWASH model validated against 1:5 tests with 4.7% transmitted-height RMSE predicted model-scale reflection and transmission about 5% above full-scale values, smaller than the effects of fence thickness and porosity. *Regime: Wooden fence porosity 0.81 with varied thickness, comparing 1:5 and full-scale simulations..* [direct_finding, mixed] (Hoang Tung Dao 2021, [doi:10.48438/jchs.2021.0004](https://doi.org/10.48438/jchs.2021.0004))
- **C378.** Across factor-four Froude-scaled dry granular-slide models, nondimensional surface velocity increased up to 35% and runout up to 26% from smallest to largest scale; correlation with grain Reynolds number and air-free DEM comparisons implicated particle-air drag. *Regime: Dry granular slides in a 6 m apparatus across a factor-four scale range..* [direct_finding, mixed] (Matthew Kesseler 2020, [doi:10.1029/2019jf005347](https://doi.org/10.1029/2019jf005347))
- **C383.** For Froude-scaled dry granular slides in 0.25-1.00 m channels at grain Reynolds numbers of order 10^2-10^3, experiments showed significant velocity and runout scale effects that the discrete-element model did not capture at the smaller scale. *Regime: Dry granular slides in channels 0.25-1.00 m wide with grain Reynolds numbers of order 10^2-10^3..* [direct_finding, mixed] (Matthew Kesseler 2018, [doi:10.1007/s10346-018-1023-z](https://doi.org/10.1007/s10346-018-1023-z))
- **C1590.** Similarity criteria relate turbulent vertical-displacement time scales to phytoplankton photoadaptation time scales, identifying regimes in which vertical mixing alters light exposure and production response. *Regime: Relationships between vertical mixing and photoadaptation of phytoplankton: similarity criteria.* [direct_finding, analytical] (MR Lewis 1984, [doi:10.3354/meps015141](https://doi.org/10.3354/meps015141))

## Papers

- MR Lewis (1984). Relationships between vertical mixing and photoadaptation of phytoplankton: similarity criteria. *Marine Ecology Progress Series*. [doi:10.3354/meps015141](https://doi.org/10.3354/meps015141)
- Valentin Heller (2013). Improved landslide‐tsunami prediction: Effects of block model parameters and slide model. *Journal of Geophysical Research Oceans*. [doi:10.1002/jgrc.20099](https://doi.org/10.1002/jgrc.20099)
- Gianmaria Giannini (2020). Wave Energy Converter Power Take-Off System Scaling and Physical Modelling. *Journal of Marine Science and Engineering*. [doi:10.3390/jmse8090632](https://doi.org/10.3390/jmse8090632)
- Matthew Kesseler (2018). A laboratory-numerical approach for modelling scale effects in dry granular slides. *Landslides*. [doi:10.1007/s10346-018-1023-z](https://doi.org/10.1007/s10346-018-1023-z)
- Tommaso Attili (2023). Scaling approaches and scale effects in wave–flexible structure interaction. *Journal of Fluids and Structures*. [doi:10.1016/j.jfluidstructs.2023.103987](https://doi.org/10.1016/j.jfluidstructs.2023.103987)
- Matthew Kesseler (2020). Grain Reynolds Number Scale Effects in Dry Granular Slides. *Journal of Geophysical Research Earth Surface*. [doi:10.1029/2019jf005347](https://doi.org/10.1029/2019jf005347)
- Hoang Tung Dao (2021). Numerical and small-scale physical modelling of wave transmission by wooden fences. *Journal of Coastal and Hydraulic Structures*. [doi:10.48438/jchs.2021.0004](https://doi.org/10.48438/jchs.2021.0004)
- Dongsheng Qiao (2021). Scaling Orchestration in Physical Model Test of Oscillating Buoy Wave Energy Converter. *Frontiers in Marine Science*. [doi:10.3389/fmars.2021.627453](https://doi.org/10.3389/fmars.2021.627453)
- Sandy Day (2015). Hydrodynamic modelling of marine renewable energy devices: A state of the art review. *Ocean Engineering*. [doi:10.1016/j.oceaneng.2015.05.036](https://doi.org/10.1016/j.oceaneng.2015.05.036)
