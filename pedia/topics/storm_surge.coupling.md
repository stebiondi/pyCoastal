# Wave-surge-tide coupling

`storm_surge.coupling` | Nonlinear interaction among waves, surge, and tide.

Parent: [Storm surge and coastal flooding](storm_surge.md)

Subtopics: [Wave setup contribution to storm surge](storm_surge.coupling.wave_setup.md)

Papers: 10. Claims: 7. Equations: 3.

## Synthesis

**Well established.** Storm tide and waves interact dynamically. Tide and surge change depth and currents that control wave growth, refraction, breaking and bottom interaction; waves return radiation stress, setup and modified surface/bottom stress to circulation. Flooding additionally depends on the transition from wave runup/overtopping to mean overflow.

**Governing physics.** Key feedbacks are tide–surge phase interaction, depth-limited wave transformation, current refraction and Doppler shifting, radiation-stress gradients, wave setup, wind-stress modification, wave-enhanced bottom friction, surge overflow and intermittent overtopping across changing freeboard.

**Dimensionless parameters.** Important controls include surge-to-tide ratio, relative depth, wave steepness, Froude number, current-to-group-speed ratio, radiation-stress normalization, relative freeboard R_c/H_s, Iribarren number, wave direction reduction, tide–surge phase and wave-setup fraction.

**Major equations.** Coupled circulation uses depth-integrated mass and momentum with radiation-stress divergence and wave-modified stresses. Spectral waves obey an action balance on time-varying depth/current fields. Total water level combines mean sea level, tide, surge and setup, while overtopping discharge depends nonlinearly on relative freeboard and incident wave statistics.

**Typical methods.** Practice uses unstructured circulation grids coupled one- or two-way to spectral wave models, shared wind/pressure forcing, gauge calibration, stress and setup sensitivity runs, tide-phase ensembles, random-wave transformation, overtopping formulae and idealized transition experiments.

**Numerical models.** ADCIRC–SWAN is validated around Taiwan. The 2024 framework fully couples surge, wave, tide and overtopping/runup with random wave transformation, directional reduction and spatial averaging. The review covers established circulation–spectral-wave coupling classes.

**Experimental datasets.** The extracted evidence combines multi-region review cases, historical Taiwan typhoons with water-level, pressure, wind, height and period gauges, and idealized typhoon/tide/freeboard numerical experiments resolving overtopping and overflow transition.

**Validated ranges.** Taiwan validation spans historical typhoons and four harbor sites; wave setup contributed 6–35% of surge and coupled water levels exceeded tide–surge results by 0.22–0.24 m on average. Overtopping-transition conclusions remain bounded to idealized bathymetry, tested tides, incidence and freeboards.

**Recent advances.** Validated regional coupling now quantifies setup contributions, while fully coupled inundation frameworks evolve offshore waves and freeboard through the entire overtopping-to-overflow transition. This replaces static superposition with continuous process exchange.

**Disagreements.** Coupling magnitude is not universal: wave setup varies strongly by site and coastal slope, tides can alter or sometimes mitigate surge, and decoupled overtopping can overestimate flooding even though omitting waves underestimates setup. Model direction and transition treatment explain the apparent tension.

**Limitations.** Dominant uncertainties include wind and pressure forcing, bathymetry, wave breaking, radiation stress, wave-modified bottom friction, current refraction, wetting/drying, overtopping parameterization, structure geometry, phase sampling and limited simultaneous field observations of all coupled variables.

**Open questions.** Needs include process-resolving validation of stress pathways, irregular-wave overtopping/overflow transitions, tide-phase uncertainty, steep and shallow-shelf contrasts, structure-specific field measurements, coupled ensemble forecasting, model intercomparison and probabilistic treatment of forcing and closure error.

**Seminal papers.** The 2009 review codified the two-way coupling pathways and their flood significance. It remains foundational because it distinguishes well-established depth/setup feedbacks from less-settled stress, friction and refraction details.

## Equations

### Wave-radiation-stress forcing of mean flow

$$
\frac{\partial(h\mathbf{u})}{\partial t}+\nabla\cdot(h\mathbf{u}\mathbf{u})+gh\nabla\eta=\boldsymbol{\tau}_w/\rho-\boldsymbol{\tau}_b/\rho-\nabla\cdot\mathbf{S}/\rho
$$

Regime: Shelf and coastal flooding where wind waves coexist with tide and storm surge and bathymetry/wind forcing are adequately resolved.

Variables: `h` total water depth; `u` depth-averaged current; `eta` mean water elevation; `tau_w` surface wind/wave-modified stress; `tau_b` bottom stress; `S` wave radiation-stress tensor; `rho` water density

Source: (Wolf 2009, [doi:10.1007/s11069-008-9316-5](https://doi.org/10.1007/s11069-008-9316-5))

### Wave-radiation-stress forcing of mean flow

$$
\frac{\partial(h\mathbf{u})}{\partial t}+\nabla\cdot(h\mathbf{u}\mathbf{u})+gh\nabla\eta=\boldsymbol{\tau}_w/\rho-\boldsymbol{\tau}_b/\rho-\nabla\cdot\mathbf{S}/\rho
$$

Regime: Idealized coastal bathymetry, tested typhoon incidence/tides and defence freeboard cases, including a 3 m freeboard example.

Variables: `h` total water depth; `u` depth-averaged current; `eta` mean water elevation; `tau_w` surface wind/wave-modified stress; `tau_b` bottom stress; `S` wave radiation-stress tensor; `rho` water density

Source: (Jo 2024, [doi:10.1016/j.coastaleng.2023.104448](https://doi.org/10.1016/j.coastaleng.2023.104448))

### Wave-radiation-stress forcing of mean flow

$$
\frac{\partial(h\mathbf{u})}{\partial t}+\nabla\cdot(h\mathbf{u}\mathbf{u})+gh\nabla\eta=\boldsymbol{\tau}_w/\rho-\boldsymbol{\tau}_b/\rho-\nabla\cdot\mathbf{S}/\rho
$$

Regime: Historical Taiwan typhoon events and Taipei Tamsui, Taichung, Kaohsiung and Hualien harbor gauges.

Variables: `h` total water depth; `u` depth-averaged current; `eta` mean water elevation; `tau_w` surface wind/wave-modified stress; `tau_b` bottom stress; `S` wave radiation-stress tensor; `rho` water density

Source: (Liu 2020, [doi:10.1016/j.oceaneng.2020.107571](https://doi.org/10.1016/j.oceaneng.2020.107571))

## Claims

- **C327.** Coupled coastal-flood modelling must pass tide- and surge-modified depth and currents to the wave model and return wave radiation stress, surface stress and wave-enhanced bottom friction to circulation; wave setup then contributes to total water level, although several stress and refraction interaction details remain uncertain. *Regime: Shelf and coastal flooding where wind waves coexist with tide and storm surge and bathymetry/wind forcing are adequately resolved..* [literature_review_statement, review] (Wolf 2009, [doi:10.1007/s11069-008-9316-5](https://doi.org/10.1007/s11069-008-9316-5))
- **C328.** Around Taiwan during historical typhoons, the calibrated ADCIRC–SWAN tide–surge–wave model reproduced observed water levels, pressure, wind and waves; including waves raised mean modelled water levels by 0.22–0.24 m at four harbors, with wave setup contributing 6–35% of total storm surge. *Regime: Historical Taiwan typhoon events and Taipei Tamsui, Taichung, Kaohsiung and Hualien harbor gauges..* [direct_finding, numerical] (Liu 2020, [doi:10.1016/j.oceaneng.2020.107571](https://doi.org/10.1016/j.oceaneng.2020.107571))
- **C329.** In idealized coastal experiments, fully coupled surge–wave–tide–overtopping simulations showed that conventional decoupled overtopping/runup calculations overestimated inundation; prolonged overtopping still produced considerable flooding for typhoon landfall at low tide, demonstrating the need to resolve the transition between overtopping and overflow. *Regime: Idealized coastal bathymetry, tested typhoon incidence/tides and defence freeboard cases, including a 3 m freeboard example..* [direct_finding, numerical] (Jo 2024, [doi:10.1016/j.coastaleng.2023.104448](https://doi.org/10.1016/j.coastaleng.2023.104448))
- **C1284.** Storm Gloria produced eastern-Iberian surge up to 1 m with waves up to 8 m, whereas Balearic impacts were wave-dominated; 30 m Ebro Delta simulation resolved surge flooding and Mallorca calculations represented wave overtopping. *Regime: Coastal impacts of Storm Gloria (January 2020) over the north-western Mediterranean.* [direct_finding, mixed] (Angel Amores 2020, [doi:10.5194/nhess-20-1955-2020](https://doi.org/10.5194/nhess-20-1955-2020))
- **C1287.** A review of marine-storm flooding identifies coupled wind, tide, wave and mean-circulation mechanisms and uses Liverpool Bay and European applications to show why wave–surge interaction matters for coastal impacts. *Regime: Coupled wave and surge modelling and implications for coastal flooding.* [literature_review_statement, review] (Judith Wolf 2008, [doi:10.5194/adgeo-17-19-2008](https://doi.org/10.5194/adgeo-17-19-2008))
- **C1391.** Reconstruction of the 5 December 2013 southern North Sea event synthesizes exceptional water levels, waves and coastal impacts and shows their spatially varying combined effects. *Regime: Southern North Sea storm surge event of 5 December 2013: Water levels, waves and coastal impacts.* [literature_review_statement, review] (Tom Spencer 2015, [doi:10.1016/j.earscirev.2015.04.002](https://doi.org/10.1016/j.earscirev.2015.04.002))
- **C1717.** An unstructured finite-element model coupling river flow, tides, storm surge, wind waves, and hurricane forcing reproduces Hurricane Katrina hydrographs and high-water marks and supports interpretation and design for extreme Louisiana-Mississippi surge. *Regime: Hurricane Katrina across coastal Louisiana and Mississippi, including riverine flow, tides, waves, and storm surge..* [direct_finding, mixed] (Bunya 2008, [doi:10.2208/proce1989.55.316](https://doi.org/10.2208/proce1989.55.316))

## Papers

- Tom Spencer (2015). Southern North Sea storm surge event of 5 December 2013: Water levels, waves and coastal impacts. *Earth-Science Reviews*. [doi:10.1016/j.earscirev.2015.04.002](https://doi.org/10.1016/j.earscirev.2015.04.002)
- Wolf (2009). Coastal flooding: impacts of coupled wave–surge–tide models. *Natural Hazards*. [doi:10.1007/s11069-008-9316-5](https://doi.org/10.1007/s11069-008-9316-5)
- Angel Amores (2020). Coastal impacts of Storm Gloria (January 2020) over the north-western Mediterranean. *Natural Hazards and Earth System Sciences*. [doi:10.5194/nhess-20-1955-2020](https://doi.org/10.5194/nhess-20-1955-2020)
- Judith Wolf (2008). Coupled wave and surge modelling and implications for coastal flooding. *Advances in Geosciences*. [doi:10.5194/adgeo-17-19-2008](https://doi.org/10.5194/adgeo-17-19-2008)
- Liu (2020). Investigating typhoon-induced storm surge and waves in the coast of Taiwan using an integrally-coupled tide-surge-wave model. *Ocean Engineering*. [doi:10.1016/j.oceaneng.2020.107571](https://doi.org/10.1016/j.oceaneng.2020.107571)
- Jo (2024). Combined storm surge and wave overtopping inundation based on fully coupled storm surge-wave-tide model. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2023.104448](https://doi.org/10.1016/j.coastaleng.2023.104448)
- Bunya (2008). Hurricane Katrina Storm Surge Hindcast Using a Coupled Storm Surge, Wind Wave and Tidal Current Model on an Unstructured Grid. *PROCEEDINGS OF COASTAL ENGINEERING, JSCE*. [doi:10.2208/proce1989.55.316](https://doi.org/10.2208/proce1989.55.316)
- Félix Santiago-Collazo (2019). A comprehensive review of compound inundation models in low-gradient coastal watersheds. *Environmental Modelling & Software*. [doi:10.1016/j.envsoft.2019.06.002](https://doi.org/10.1016/j.envsoft.2019.06.002)
- J. C. Dietrich (2018). Sensitivity of Storm Surge Predictions to Atmospheric Forcing during Hurricane Isaac. *Journal of Waterway, Port, Coastal, and Ocean Engineering*. [doi:10.1061/(asce)ww.1943-5460.0000419](https://doi.org/10.1061/(asce)ww.1943-5460.0000419)
- Anna Nikishova (2017). Uncertainty quantification and sensitivity analysis applied to the wind wave model SWAN. *Environmental Modelling & Software*. [doi:10.1016/j.envsoft.2017.06.030](https://doi.org/10.1016/j.envsoft.2017.06.030)
