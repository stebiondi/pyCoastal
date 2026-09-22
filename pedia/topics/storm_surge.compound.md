# Compound flooding

`storm_surge.compound` | Joint marine, fluvial, pluvial, and groundwater flooding.

Parent: [Storm surge and coastal flooding](storm_surge.md)

Papers: 18. Claims: 17. Equations: 8.

Used by pyCoastal design modules: Storm surge and flooding.

## Synthesis

**Well established.** Compound coastal flooding occurs when coastal water level, waves, river discharge, direct rainfall, runoff, groundwater or infrastructure pathways interact in space or time. Combined inundation is generally not recoverable by simply adding independently calculated peak maps because phasing, storage, backwater and drainage capacity are nonlinear.

**Governing physics.** Coastal surge and tide impose downstream head; river discharge propagates seaward; rainfall creates runoff and local ponding; saturated storage delays drainage; waves overtop barriers; seawalls, gates, dams, storm drains and sewers redirect or block flux. Geometry and driver timing determine coastal, hydrologic and transition zones.

**Dimensionless parameters.** Controls include surge-to-tide ratio, discharge-to-tidal prism, rainfall duration and intensity ratios, phase lag normalized by tidal period, Froude number, storage and drainage-capacity ratios, seawall freeboard, overtopping rate, joint exceedance probability and fractional driver contribution.

**Major equations.** Models solve depth-integrated mass and momentum with rainfall, infiltration, river, drain and coastal source terms. Statistical studies use peaks over threshold, marginal extreme distributions and copulas. Driver attribution compares all-driver and leave-one-driver-out simulations, while interaction residuals quantify departure from additive response.

**Typical methods.** Methods include tightly or singly coupled hydrologic–hydrodynamic models, flexible meshes, reduced-physics solvers, sewer/drain networks, wave overtopping and breach modules, idealized phasing tests, historical hurricane hindcasts, high-water-mark validation, driver-isolation scenarios, POT and copula analysis.

**Numerical models.** SFINCS provides efficient reduced physics; Delft3D-FM resolves flexible-mesh estuary and river interaction; SuWAT integrates surge, tide, waves, overtopping and pluvial/sewer processes; other coupled city models explicitly include drainage, dams, gates, seawalls and rainfall runoff.

**Experimental datasets.** Evidence includes five Virginia hurricanes; Jacksonville/Irma and Hernani wave cases; Napa River and idealized channels; 15 southeastern China regions with 1960–2015 records; Xiangshan infrastructure; Typhoon Jebi at Kansai Airport; a 2017 embayment event; and Harvey, Ike, Rita and calibration data in Sabine–Neches.

**Validated ranges.** Validation is case bounded. Sabine–Neches mean water-level calibration reached R²=0.91 and 84% of Imelda high-water-mark depths were within ±0.2 m. Jebi attribution was 90.8% overtopping, 7.5% seawall failure and smaller sewer shares. Napa scenarios included surge small relative to a 2 m tide.

**Recent advances.** Recent work partitions dynamic driver zones, represents urban sewers and structural failure, and quantifies flood-volume contributions. Historical multistorm studies now show temporally separated compound peaks, shifting attention from coincident maxima to evolving event sequences.

**Disagreements.** A dominant driver varies by event and location: Jebi airport flooding was overtopping dominated, prolonged Harvey rainfall created extensive delayed fluvial–pluvial compounding, and larger tidal amplitude can suppress upstream surge propagation. These are regime differences, not a universal ranking of drivers.

**Limitations.** Uncertainty arises from rainfall fields, runoff and infiltration, river boundaries, bathymetry/topography, roughness, drainage connectivity and blockage, breach assumptions, wave overtopping, groundwater omission, grid resolution, daily statistical sampling, copula tails and sparse validation of extreme combinations.

**Open questions.** Priorities are groundwater and soil saturation, dynamic drainage failure, defence breach probability, wave–surge–rain–river coupling, multivariate climate nonstationarity, probabilistic phasing, real-time data assimilation, common intercomparison cases and consequence-aware attribution.

**Seminal papers.** Within this corpus, the 2018 Napa River study demonstrates non-additive tide–surge–river phasing, while the 2021 SFINCS study establishes an efficient all-driver solver with explicit evidence that advection is required for broken-wave and shock flow.

## Equations

### Depth-integrated compound-flood mass balance

$$
\frac{\partial h}{\partial t}+\nabla\cdot(h\mathbf{u})=R-I+q_r+q_d+q_c
$$

Regime: Verification cases, Hurricane Irma Jacksonville flooding, and broken-wave flooding at Hernani.

Variables: `h` water depth; `u` depth-averaged velocity; `R` rainfall; `I` infiltration; `q_r` river/runoff source; `q_d` drain or sewer exchange; `q_c` coastal boundary, overtopping or failure source

Source: (Leijnse 2021, [doi:10.1016/j.coastaleng.2020.103796](https://doi.org/10.1016/j.coastaleng.2020.103796))

### Depth-integrated compound-flood mass balance

$$
\frac{\partial h}{\partial t}+\nabla\cdot(h\mathbf{u})=R-I+q_r+q_d+q_c
$$

Regime: Xiangshan topography, drainage, coastal dam and tide-gate configurations in the tested storm scenarios.

Variables: `h` water depth; `u` depth-averaged velocity; `R` rainfall; `I` infiltration; `q_r` river/runoff source; `q_d` drain or sewer exchange; `q_c` coastal boundary, overtopping or failure source

Source: (Shi 2022, [doi:10.1016/j.coastaleng.2021.104064](https://doi.org/10.1016/j.coastaleng.2021.104064))

### Depth-integrated compound-flood mass balance

$$
\frac{\partial h}{\partial t}+\nabla\cdot(h\mathbf{u})=R-I+q_r+q_d+q_c
$$

Regime: Kansai Airport geometry and infrastructure during the reconstructed 2018 Typhoon Jebi event.

Variables: `h` water depth; `u` depth-averaged velocity; `R` rainfall; `I` infiltration; `q_r` river/runoff source; `q_d` drain or sewer exchange; `q_c` coastal boundary, overtopping or failure source

Source: (Jo 2025, [doi:10.1016/j.jhydrol.2025.133698](https://doi.org/10.1016/j.jhydrol.2025.133698))

### Depth-integrated compound-flood mass balance

$$
\frac{\partial h}{\partial t}+\nabla\cdot(h\mathbf{u})=R-I+q_r+q_d+q_c
$$

Regime: Sabine–Neches domain for Harvey, Ike and Rita, with tide-gauge and Imelda high-water-mark calibration evidence.

Variables: `h` water depth; `u` depth-averaged velocity; `R` rainfall; `I` infiltration; `q_r` river/runoff source; `q_d` drain or sewer exchange; `q_c` coastal boundary, overtopping or failure source

Source: (Maymandi 2022, [doi:10.1029/2022wr033144](https://doi.org/10.1029/2022wr033144))

### Depth-integrated compound-flood mass balance

$$
\frac{\partial h}{\partial t}+\nabla\cdot(h\mathbf{u})=R-I+q_r+q_d+q_c
$$

Regime: Five Virginia hurricanes spanning different rainfall and surge intensities.

Variables: `h` water depth; `u` depth-averaged velocity; `R` rainfall; `I` infiltration; `q_r` river/runoff source; `q_d` drain or sewer exchange; `q_c` coastal boundary, overtopping or failure source

Source: (Han 2024, [doi:10.1029/2023wr037014](https://doi.org/10.1029/2023wr037014))

### Depth-integrated compound-flood mass balance

$$
\frac{\partial h}{\partial t}+\nabla\cdot(h\mathbf{u})=R-I+q_r+q_d+q_c
$$

Regime: Fifteen regions between 106–120°E and 18–32°N with available 1960–2015 daily records.

Variables: `h` water depth; `u` depth-averaged velocity; `R` rainfall; `I` infiltration; `q_r` river/runoff source; `q_d` drain or sewer exchange; `q_c` coastal boundary, overtopping or failure source

Source: (Lu 2022, [doi:10.3390/atmos13020238](https://doi.org/10.3390/atmos13020238))

### Depth-integrated compound-flood mass balance

$$
\frac{\partial h}{\partial t}+\nabla\cdot(h\mathbf{u})=R-I+q_r+q_d+q_c
$$

Regime: The studied embayment-backed catchment, historical 12 January 2017 event and tested seawall/drain scenarios.

Variables: `h` water depth; `u` depth-averaged velocity; `R` rainfall; `I` infiltration; `q_r` river/runoff source; `q_d` drain or sewer exchange; `q_c` coastal boundary, overtopping or failure source

Source: (Boxiang Tang 2023, [doi:10.3390/jmse11071454](https://doi.org/10.3390/jmse11071454))

### Depth-integrated compound-flood mass balance

$$
\frac{\partial h}{\partial t}+\nabla\cdot(h\mathbf{u})=R-I+q_r+q_d+q_c
$$

Regime: Napa River geometry plus idealized small-river scenarios, including 0.2 m surge and 2 m tide cases.

Variables: `h` water depth; `u` depth-averaged velocity; `R` rainfall; `I` infiltration; `q_r` river/runoff source; `q_d` drain or sewer exchange; `q_c` coastal boundary, overtopping or failure source

Source: (Liv Herdman 2018, [doi:10.3390/jmse6040158](https://doi.org/10.3390/jmse6040158))

## Claims

- **C319.** SFINCS reproduced compound fluvial, pluvial, tidal and wind-driven flooding for Hurricane Irma at Jacksonville with limited computational expense, while an advective momentum term was necessary for shock-like dam-break and broken-wave flows and enabled wave-driven flooding at Hernani. *Regime: Verification cases, Hurricane Irma Jacksonville flooding, and broken-wave flooding at Hernani..* [direct_finding, mixed] (Leijnse 2021, [doi:10.1016/j.coastaleng.2020.103796](https://doi.org/10.1016/j.coastaleng.2020.103796))
- **C320.** For Xiangshan, coupled simulation of surge, heavy rainfall, urban drainage, a coastal dam and tide gates partitioned inundation into tidal, hydrologic and transition zones, showing that mitigation choice must follow the locally dominant driver and infrastructure interaction. *Regime: Xiangshan topography, drainage, coastal dam and tide-gate configurations in the tested storm scenarios..* [direct_finding, mixed] (Shi 2022, [doi:10.1016/j.coastaleng.2021.104064](https://doi.org/10.1016/j.coastaleng.2021.104064))
- **C321.** In Napa River field-scale and idealized Delft3D-FM simulations, coincident high tide, surge and river discharge maximized water levels; large tidal amplitude diminished upstream surge propagation, and the phase between peak discharge and high tide shifted the location and timing of maxima. *Regime: Napa River geometry plus idealized small-river scenarios, including 0.2 m surge and 2 m tide cases..* [direct_finding, mixed] (Liv Herdman 2018, [doi:10.3390/jmse6040158](https://doi.org/10.3390/jmse6040158))
- **C322.** For Harvey, Ike and Rita in the Sabine–Neches Estuary, a single-domain Delft3D-FM model identified four coastal–fluvial–pluvial interaction mechanisms; extended rainfall produced the largest extent and duration and a lagged second flood peak, while calibration achieved mean water-level R²=0.91 and 84% of Imelda high-water-mark depths within ±0.2 m. *Regime: Sabine–Neches domain for Harvey, Ike and Rita, with tide-gauge and Imelda high-water-mark calibration evidence..* [direct_finding, mixed] (Maymandi 2022, [doi:10.1029/2022wr033144](https://doi.org/10.1029/2022wr033144))
- **C323.** For 15 southeastern China coastal-estuarine regions using 1960–2015 daily discharge and sea-level records, peak-over-threshold and copula analyses showed that joint fluvial–storm-tide flooding can exceed the flooding implied by either driver in isolation and that dependence varies among sites. *Regime: Fifteen regions between 106–120°E and 18–32°N with available 1960–2015 daily records..* [direct_finding, mixed] (Lu 2022, [doi:10.3390/atmos13020238](https://doi.org/10.3390/atmos13020238))
- **C324.** Across five hurricanes simulated for low-gradient coastal Virginia, flooding separated into rainfall-dominant, surge-dominant and transitional zones; coastal-zone extent correlated strongly with surge magnitude, while transitional-zone extent correlated very strongly with the product of surge-inundated area and total rainfall. *Regime: Five Virginia hurricanes spanning different rainfall and surge intensities..* [direct_finding, mixed] (Han 2024, [doi:10.1029/2023wr037014](https://doi.org/10.1029/2023wr037014))
- **C325.** For an embayment-backed urban catchment and the 12 January 2017 compound event, coupled simulations resolved separate and combined high-marine-level and precipitation flooding and showed that seawall and storm-drain configuration controls whether coastal protection blocks or facilitates drainage. *Regime: The studied embayment-backed catchment, historical 12 January 2017 event and tested seawall/drain scenarios..* [direct_finding, mixed] (Boxiang Tang 2023, [doi:10.3390/jmse11071454](https://doi.org/10.3390/jmse11071454))
- **C326.** For Typhoon Jebi flooding at Kansai International Airport, the integrated SuWAT analysis attributed 90.8% of total flood volume to wave overtopping, 7.5% to seawall failure, and 1.7% and 0.26% to seawater and rainwater sewer reverse flows, respectively. *Regime: Kansai Airport geometry and infrastructure during the reconstructed 2018 Typhoon Jebi event..* [direct_finding, mixed] (Jo 2025, [doi:10.1016/j.jhydrol.2025.133698](https://doi.org/10.1016/j.jhydrol.2025.133698))
- **C1283.** Across 3,433 river mouths, surge exacerbated 1-in-10-year river flood levels at 64.0% of sites by a mean 11 cm; ignoring surge significantly underestimated depths for 9.3% of expected annually exposed population. *Regime: The effect of surge on riverine flood hazard and impact in deltas globally.* [direct_finding, numerical] (Dirk Eilander 2020, [doi:10.1088/1748-9326/ab8ca6](https://doi.org/10.1088/1748-9326/ab8ca6))
- **C1285.** A coupled NWM–D-Flow FM–ADCIRC/WW3 system reproduced Delaware storm peaks with skill 0.79–0.91 and negligible phase error; upstream levels depended strongly on streamflow, while winds and roughness controlled prediction quality. *Regime: A New 1D/2D Coupled Modeling Approach for a Riverine‐Estuarine System Under Storm Events: Application to Delaware River Basin.* [direct_finding, mixed] (R. Bakhtyar 2020, [doi:10.1029/2019jc015822](https://doi.org/10.1029/2019jc015822))
- **C1388.** European projections show anthropogenic climate change increases the joint probability of heavy precipitation and storm surge, making compound flooding more likely than stationary dependence implies. *Regime: Higher probability of compound flooding from precipitation and storm surge in Europe under anthropogenic climate change.* [direct_finding, numerical] (Emanuele Bevacqua 2019, [doi:10.1126/sciadv.aaw5531](https://doi.org/10.1126/sciadv.aaw5531))
- **C1389.** A global analysis combines river-discharge and storm-surge extremes to identify where dependence and event timing create elevated compound-flood potential. *Regime: Measuring compound flood potential from river discharge and storm surge extremes at the global scale.* [direct_finding, numerical] (Anaïs Couasnon 2020, [doi:10.5194/nhess-20-489-2020](https://doi.org/10.5194/nhess-20-489-2020))
- **C1390.** Low-gradient coastal modeling defines transitions among surge-, river-, and compound-dominated flood zones and shows downstream sea level can propagate far inland. *Regime: Defining Flood Zone Transitions in Low‐Gradient Coastal Regions.* [direct_finding, numerical] (Matthew V. Bilskie 2018, [doi:10.1002/2018gl077524](https://doi.org/10.1002/2018gl077524))
- **C1650.** A dynamically linked Atlantic-ocean and four-level nested harbor-to-street model reproduces the November 2009 Cork coastal-fluvial flood and resolves how tide, surge, river inflow and their interaction control urban flood-wave routes, depths, velocities and human-safety risk. *Regime: November 2009 compound coastal-fluvial flooding of Cork City and Cork Harbour, Ireland..* [direct_finding, numerical] (Olbert 2017, [doi:10.1016/j.coastaleng.2016.12.006](https://doi.org/10.1016/j.coastaleng.2016.12.006))
- **C1680.** Rapid FLORES screening for Beira shows compound surge and rainfall losses exceed isolated-hazard impacts because high coastal water levels block drainage; drainage expansion dominates near-term benefits, while coastal protection becomes increasingly important under high-end climate change. *Regime: Concept-stage compound storm-surge and pluvial flood planning for Beira, Mozambique, using the documented schematization and data..* [direct_finding, numerical] (Erik C. van Berchum 2020, [doi:10.5194/nhess-20-2633-2020](https://doi.org/10.5194/nhess-20-2633-2020))
- **C1744.** Compound inundation models for low-gradient coastal watersheds should progress from linked, one-way, and loose coupling toward tight or full coupling that resolves rainfall across the whole domain and two-way storm-surge interactions with surface runoff, out-of-bank flow, and streamflow. *Regime: Low-gradient coastal watersheds exposed to coincident or sequential intense rainfall, river runoff, tropical-cyclone surge, and coastal inundation..* [literature_review_statement, review] (Félix Santiago-Collazo 2019, [doi:10.1016/j.envsoft.2019.06.002](https://doi.org/10.1016/j.envsoft.2019.06.002))
- **C1757.** Compound flood design in tidal channels must represent both statistical dependence and nonlinear hydraulic interaction between upstream discharge and downstream ocean level: joint AND scenarios can produce higher interior water levels than marginal scenarios despite smaller boundary values, whereas an OR-return-period scenario provides a conservative single spatial hazard profile. *Regime: Tidal channels and estuaries with upstream river-discharge records, downstream ocean-level records, known channel geometry and resistance, and flood hazard expressed as a spatial water-surface profile for a specified return period..* [direct_finding, mixed] (Hamed Moftakhari 2019, [doi:10.1016/j.advwatres.2019.04.009](https://doi.org/10.1016/j.advwatres.2019.04.009))

## Papers

- Emanuele Bevacqua (2019). Higher probability of compound flooding from precipitation and storm surge in Europe under anthropogenic climate change. *Science Advances*. [doi:10.1126/sciadv.aaw5531](https://doi.org/10.1126/sciadv.aaw5531)
- Anaïs Couasnon (2020). Measuring compound flood potential from river discharge and storm surge extremes at the global scale. *Natural hazards and earth system sciences*. [doi:10.5194/nhess-20-489-2020](https://doi.org/10.5194/nhess-20-489-2020)
- Félix Santiago-Collazo (2019). A comprehensive review of compound inundation models in low-gradient coastal watersheds. *Environmental Modelling & Software*. [doi:10.1016/j.envsoft.2019.06.002](https://doi.org/10.1016/j.envsoft.2019.06.002)
- Hamed Moftakhari (2019). Linking statistical and hydrodynamic modeling for compound flood hazard assessment in tidal channels and estuaries. *Advances in Water Resources*. [doi:10.1016/j.advwatres.2019.04.009](https://doi.org/10.1016/j.advwatres.2019.04.009)
- Matthew V. Bilskie (2018). Defining Flood Zone Transitions in Low‐Gradient Coastal Regions. *Geophysical Research Letters*. [doi:10.1002/2018gl077524](https://doi.org/10.1002/2018gl077524)
- Leijnse (2021). Modeling compound flooding in coastal systems using a computationally efficient reduced-physics solver: Including fluvial, pluvial, tidal, wind- and wave-driven processes. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2020.103796](https://doi.org/10.1016/j.coastaleng.2020.103796)
- Dirk Eilander (2020). The effect of surge on riverine flood hazard and impact in deltas globally. *Environmental Research Letters*. [doi:10.1088/1748-9326/ab8ca6](https://doi.org/10.1088/1748-9326/ab8ca6)
- Olbert (2017). High-resolution multi-scale modelling of coastal flooding due to tides, storm surges and rivers inflows. A Cork City example. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2016.12.006](https://doi.org/10.1016/j.coastaleng.2016.12.006)
- R. Bakhtyar (2020). A New 1D/2D Coupled Modeling Approach for a Riverine‐Estuarine System Under Storm Events: Application to Delaware River Basin. *Journal of Geophysical Research: Oceans*. [doi:10.1029/2019jc015822](https://doi.org/10.1029/2019jc015822)
- Shi (2022). Numerical simulations of compound flooding caused by storm surge and heavy rain with the presence of urban drainage system, coastal dam and tide gates: A case study of Xiangshan, China. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2021.104064](https://doi.org/10.1016/j.coastaleng.2021.104064)
- Liv Herdman (2018). Storm Surge Propagation and Flooding in Small Tidal Rivers during Events of Mixed Coastal and Fluvial Influence. *Journal of Marine Science and Engineering*. [doi:10.3390/jmse6040158](https://doi.org/10.3390/jmse6040158)
- Maymandi (2022). Compound Coastal, Fluvial, and Pluvial Flooding During Historical Hurricane Events in the Sabine–Neches Estuary, Texas. *Water Resources Research*. [doi:10.1029/2022wr033144](https://doi.org/10.1029/2022wr033144)
- Erik C. van Berchum (2020). Rapid flood risk screening model for compound flood events in Beira, Mozambique. *Natural hazards and earth system sciences*. [doi:10.5194/nhess-20-2633-2020](https://doi.org/10.5194/nhess-20-2633-2020)
- Lu (2022). Compounding Effects of Fluvial Flooding and Storm Tides on Coastal Flooding Risk in the Coastal-Estuarine Region of Southeastern China. *Atmosphere*. [doi:10.3390/atmos13020238](https://doi.org/10.3390/atmos13020238)
- Han (2024). Compound Flooding Hazards Due To Storm Surge and Pluvial Flow in a Low‐Gradient Coastal Region. *Water Resources Research*. [doi:10.1029/2023wr037014](https://doi.org/10.1029/2023wr037014)
- Boxiang Tang (2023). Predicting Compound Coastal Flooding in Embayment-Backed Urban Catchments: Seawall and Storm Drain Implications. *Journal of Marine Science and Engineering*. [doi:10.3390/jmse11071454](https://doi.org/10.3390/jmse11071454)
- Jo (2025). Coastal and pluvial compound flooding of surge, wave, tide, rainfall-runoff, sewer flow, and seawall failure at coastal urban areas. *Journal of Hydrology*. [doi:10.1016/j.jhydrol.2025.133698](https://doi.org/10.1016/j.jhydrol.2025.133698)
- Bunya (2008). Hurricane Katrina Storm Surge Hindcast Using a Coupled Storm Surge, Wind Wave and Tidal Current Model on an Unstructured Grid. *PROCEEDINGS OF COASTAL ENGINEERING, JSCE*. [doi:10.2208/proce1989.55.316](https://doi.org/10.2208/proce1989.55.316)
