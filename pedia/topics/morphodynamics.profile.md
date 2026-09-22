# Cross-shore profile evolution

`morphodynamics.profile` | Profile response and equilibrium concepts.

Parent: [Coastal morphodynamics](morphodynamics.md)

Papers: 11. Claims: 6. Equations: 0.

## Synthesis

**Well established.** Cross-shore beach profiles adjust sediment between dune, berm, surf zone and shoreface as wave energy, water level and sediment supply vary; profile and planform evolution interact, so shoreline position alone is not a complete sediment-budget measure.

**Governing physics.** Wave breaking, undertow, skewed and asymmetric orbital motion, swash infiltration, gravity, avalanching and alongshore divergence govern transport. Storms tend to erode upper profiles and build bars or offshore deposits, while milder forcing can restore berms conditional on sediment availability.

**Dimensionless parameters.** Controls include wave steepness, relative depth, surf-similarity and Dean-type fall-velocity parameters, Shields and mobility numbers, sediment fall velocity relative to orbital velocity, relative freeboard, normalized profile volume and nourishment grain-size ratio.

**Major equations.** Models couple wave-action or momentum balances to cross-shore sediment-transport gradients and bed continuity, dz/dt plus dqx/dx equals zero; equilibrium-profile forms commonly relate depth to offshore distance, while dynamic-equilibrium models relax shoreline or profile state toward forcing-dependent targets.

**Typical methods.** Studies repeat surveys or video-derived shorelines and profiles, close sediment budgets, separate storm and recovery intervals, calibrate equilibrium or process models, test hindcasts independently, quantify profile and planform change together and examine sensitivity to closure depth, transport formula and boundary exchange.

**Numerical models.** The set includes a one-parameter dynamic-equilibrium shoreline model based on a bi-parabolic profile, coupled profile-planform interpretation of nourishment evolution and scenario-based mixed-beach defense adjustment; detailed process-based cross-shore solvers remain a review gap.

**Experimental datasets.** Reviewed evidence includes two years of daily Nova Icaria video observations, the 1100 m Upham Beach nourishment and hurricane response, 87 surveys along 50 transects of Nice gravel beach, and four southeast England mixed sand-gravel defenses under sea-level-rise scenarios.

**Validated ranges.** Support is site-specific: one Mediterranean sandy beach, one nourished Florida segment, one steep French gravel beach and four English mixed beaches. Performance does not establish universality across sediment sizes, reefs, tidal ranges or storm climates.

**Recent advances.** Recent advances combine dense video, lidar and satellite profiles with Bayesian calibration, differentiable and surrogate morphodynamic models, phase-resolving swash physics, mixed-grain formulations, probabilistic storm sequences and profile-aware adaptive nourishment.

**Disagreements.** Equilibrium-profile models offer parsimonious shoreline skill but compress transport mechanisms and offshore loss, whereas process models resolve more physics at greater calibration and computational cost. A stable shoreline can coexist with large internal profile redistribution or sediment leakage.

**Limitations.** Uncertain closure boundaries, survey error, sparse storm sampling, alongshore gradients, grain-size sorting, groundwater, structures, unresolved swash, offshore loss and equifinal calibration limit inference. Scenario profiles also depend on assumed sediment supply and sea-level trajectory.

**Open questions.** Priorities include unified profile-planform models, storm-sequence memory, recovery timescales, mixed and gravel sediment sorting, reef-fronted profiles, overwash and dune coupling, climate-conditioned equilibrium, data assimilation and uncertainty-aware nourishment design.

**Seminal papers.** Bruun-type recession concepts and power-law equilibrium profiles established reduced descriptions; energetics and transport-gradient models introduced dynamic evolution, followed by barred-profile, shoreline-relaxation and process-based wave–current–sediment solvers.

## Claims

- **C192.** At Nova Icaria beach, a dynamic-equilibrium shoreline model using a theoretical bi-parabolic profile and one calibrated rate parameter showed no loss of skill relative to compared models with four free parameters over two years of daily video monitoring. *Regime: Wave-driven cross-shore response at the monitored Mediterranean beach; longshore gradients and complex fills are omitted..* [direct_finding, mixed] (Jara 2015, [doi:10.1016/j.coastaleng.2015.02.006](https://doi.org/10.1016/j.coastaleng.2015.02.006))
- **C1184.** Laboratory and natural overwash morphometrics follow scale-invariant relationships across several orders of magnitude and align with classic drainage and alluvial-fan scaling laws. *Regime: Scaling laws for coastal overwash morphology.* [direct_finding, mixed] (Eli D. Lazarus 2016, [doi:10.1002/2016gl071213](https://doi.org/10.1002/2016gl071213))
- **C1189.** A sediment-conservation model coupling waves, wave-driven currents and transport used bed-slope updating, oscillation removal and multilevel time discretization to improve stability over complex coastal topography. *Regime: NUMERICAL SOLUTIONS OF COASTAL MORPHODYNAMIC EVOLUTION FOR COMPLEX TOPOGRAPHY.* [direct_finding, mixed] (Yun-Chih Chiang 2010, [doi:10.51400/2709-6998.1878](https://doi.org/10.51400/2709-6998.1878))
- **C1626.** A behavior-oriented panel model reasonably hindcast century and millennial Central Holland shoreface evolution and supports faster upper- than lower-shoreface response, but its wave-driven transport coefficients absorb omitted processes and provide only order-of-magnitude transfer beyond the calibration coast. *Regime: Central Holland shoreface hindcasts over engineering and geological time scales..* [direct_finding, mixed] (M.J.F. Stive 1995, [doi:10.1016/0025-3227(95)00080-i](https://doi.org/10.1016/0025-3227(95)00080-i))
- **C1636.** Lower shorefaces can supply beaches, dunes, estuaries and tidal basins, especially where sediment-rich shelves experience swell-driven onshore transport, but nonlinear bedload and suspended-load interactions, sparse seabed mapping and scale separation make sediment-connectivity magnitude and direction highly uncertain. *Regime: Diverse clastic and carbonate lower shorefaces linking inner shelves to upper shorefaces and beaches..* [literature_review_statement, review] (Edward J. Anthony 2020, [doi:10.1016/j.earscirev.2020.103334](https://doi.org/10.1016/j.earscirev.2020.103334))
- **C1652.** A mesoscale shoreface synthesis defines a temporally variable upper-lower shoreface framework, with depth of closure separating the zones and significant sediment-transport stress defining the seaward limit, and proposes sediment supply and accommodation as organizing controls on diverse two- and three-dimensional morphologies. *Regime: Wave-influenced mobile shorefaces between the fair-weather surf-zone edge or beachface and the seaward limit of significant sediment transport..* [literature_review_statement, review] (Klervi Hamon-Kerivel 2020, [doi:10.1016/j.earscirev.2020.103330](https://doi.org/10.1016/j.earscirev.2020.103330))

## Papers

- M.J.F. Stive (1995). Modelling shoreface profile evolution. *Marine Geology*. [doi:10.1016/0025-3227(95)00080-i](https://doi.org/10.1016/0025-3227(95)00080-i)
- Edward J. Anthony (2020). The lower shoreface: Morphodynamics and sediment connectivity with the upper shoreface and beach. *Earth-Science Reviews*. [doi:10.1016/j.earscirev.2020.103334](https://doi.org/10.1016/j.earscirev.2020.103334)
- Elko (2007). Immediate profile and planform evolution of a beach nourishment project with hurricane influences. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2006.08.001](https://doi.org/10.1016/j.coastaleng.2006.08.001)
- Klervi Hamon-Kerivel (2020). Shoreface mesoscale morphodynamics: A review. *Earth-Science Reviews*. [doi:10.1016/j.earscirev.2020.103330](https://doi.org/10.1016/j.earscirev.2020.103330)
- Eli D. Lazarus (2016). Scaling laws for coastal overwash morphology. *Geophysical Research Letters*. [doi:10.1002/2016gl071213](https://doi.org/10.1002/2016gl071213)
- Jara (2015). Shoreline evolution model from a dynamic equilibrium beach profile. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2015.02.006](https://doi.org/10.1016/j.coastaleng.2015.02.006)
- Yun-Chih Chiang (2010). NUMERICAL SOLUTIONS OF COASTAL MORPHODYNAMIC EVOLUTION FOR COMPLEX TOPOGRAPHY. *Journal of Marine Science and Technology*. [doi:10.51400/2709-6998.1878](https://doi.org/10.51400/2709-6998.1878)
- Tim Scott (2011). Morphodynamic characteristics and classification of beaches in England and Wales. *Marine Geology*. [doi:10.1016/j.margeo.2011.04.004](https://doi.org/10.1016/j.margeo.2011.04.004)
- Gerd Masselink (2014). Role of wave forcing, storms and NAO in outer bar dynamics on a high-energy, macro-tidal beach. *Geomorphology*. [doi:10.1016/j.geomorph.2014.07.025](https://doi.org/10.1016/j.geomorph.2014.07.025)
- Anthony (2011). Chronic offshore loss of nourishment on Nice beach, French Riviera: A case of over-nourishment of a steep beach?. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2010.11.001](https://doi.org/10.1016/j.coastaleng.2010.11.001)
- Dornbusch (2017). Design requirement for mixed sand and gravel beach defences under scenarios of sea level rise. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2017.03.006](https://doi.org/10.1016/j.coastaleng.2017.03.006)
