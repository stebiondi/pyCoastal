# Tracer and drifter studies

`field.tracers` | Lagrangian and scalar transport observations.

Parent: [Field measurements](field.md)

Papers: 13. Claims: 12. Equations: 0.

## Synthesis

**Well established.** Tracers and drifters reveal coastal advection, dispersion, retention, and exchange, but scalar parcels, surface drifters, subsurface drogues, organisms, and numerical particles can follow different pathways.

**Governing physics.** Observed transport reflects mean currents, tides, wind and Ekman flow, waves and surf-zone currents, fronts, vertical shear, turbulence, bathymetry, shoreline interaction, and particle buoyancy or behavior.

**Dimensionless parameters.** Relevant controls include excursion relative to domain scale, release duration relative to tide, inertial and windage response, horizontal/vertical diffusivity, sampling interval relative to decorrelation time, and observation duration relative to residence time.

**Major equations.** Core tools include advection-diffusion, single- and pair-particle statistics, residence/flushing/age/transit definitions, trajectory integration, coherent structures, mass balance, and model-observation skill metrics.

**Typical methods.** Methods include soluble fluorescent or SF6 releases, GPS/RTK surface and subsurface drifters, introduced biological cohorts, conductivity plume probes, UAV concentration imaging, Eulerian co-observations, particle models, and Lagrangian coherent structures.

**Numerical models.** Trajectory and tracer models range from local lagoon and shoreline-release simulations to coupled wave-current shelf models and climatological coherent structures; model particles require observational checks against scalar and drifter behavior.

**Experimental datasets.** Accessible observations include an eight-day lagoon cohort/SF6/drifter comparison, centimetre-accuracy 10 Hz shallow-water drifters, three UAV dye campaigns, and three nine-probe estuary plume releases.

**Validated ranges.** Reported capabilities include 10 Hz centimetre positioning, motion resolved to 1 Hz, UAV concentration grids of 2×2 m, three releases of nine probes, and basin-scale attraction attribution of 44% to the Black Sea Rim Current.

**Recent advances.** Recent advances include centimetre RTK positioning, low-cost open electronics, UAV tracer concentration maps, multiscale wave-current tracer models, and climatological coherent pathways for persistent transport diagnosis.

**Disagreements.** SF6/tracer models and drifter/particle models predicted different larval fate in the same lagoon experiment, showing that apparent validation depends on tracer type, vertical sampling, biological spread, and the transport quantity compared.

**Limitations.** Surface windage, drogue slip, positioning error, dye photochemistry, finite release duration, sparse recovery, vertical motion, shoreline loss, imperfect concentration calibration, model resolution, and ambiguous timescale definitions bias inference.

**Open questions.** Needs include vertical and three-dimensional dispersion, intermittent fronts and rip exchange, storm sampling, shoreline/beaching processes, multi-tracer intercomparison, source attribution, adaptive releases, and uncertainty propagation into residence and connectivity metrics.

**Seminal papers.** The branch connects classical dye and inert-gas dispersion, Lagrangian drifters, diagnostic timescales, biological cohort tracking, particle trajectories, and coherent-structure analysis.

## Claims

- **C589.** Coastal residence, flushing, age, and transit times must be explicitly defined because they answer different transport questions and depend on the chosen Lagrangian or Eulerian framework. *Regime: Lagrangian, Eulerian, field, model, and algebraic timescales are not interchangeable and require explicit definitions and process scope..* [literature_review_statement, review] (Lisa V. Lucas 2020, [doi:10.3390/w12102717](https://doi.org/10.3390/w12102717))
- **C590.** An eight-day lagoon experiment found SF6/tracer-model and drifter/particle predictions disagreed and observed larval spreading along the advective path that the models omitted. *Regime: SF6/tracer-model fate disagreed with drifter/particle predictions and observed larvae spread along the advective path, exposing missing dispersion mechanisms..* [direct_finding, mixed] (William S. Arnold 2005, [doi:10.4319/lo.2005.50.2.0587](https://doi.org/10.4319/lo.2005.50.2.0587))
- **C591.** Gulf transport synthesis identifies coupled river, wind, wave, tide, front, inlet, shelf, and open-ocean processes as controls on tracer fate, with storm fluxes and multiscale coupling unresolved. *Regime: Winds, waves, tides, river inputs, fronts, shelf-deep-ocean exchange, and multiscale advection jointly control constituent fate; storm fluxes and scale coupling remain uncertain..* [literature_review_statement, review] (Dubravko Justić 2021, [doi:10.1007/s12237-021-01005-1](https://doi.org/10.1007/s12237-021-01005-1))
- **C592.** A 10 Hz centimetre-accuracy RTK-GNSS shallow-water drifter resolved motion to 1 Hz and yielded dispersion coefficients comparable to dye-tracer studies. *Regime: The low-windage drifter resolved motion to 1 Hz, captured tidal elevation, and produced shallow-estuary dispersion estimates comparable to dye studies..* [direct_finding, field] (Kabir Suara 2014, [doi:10.1175/jtech-d-14-00127.1](https://doi.org/10.1175/jtech-d-14-00127.1))
- **C593.** A shoreline-dye simulation attributed alongshore transport to wave breaking and pressure gradients and offshore exchange to wind-driven Ekman flow and submesoscale frontogenesis rather than tides. *Regime: Wave breaking and pressure gradients drove alongshore transport; wind-driven Ekman and submesoscale frontogenesis contributed cross-shelf exchange, while tides did not explain it..* [direct_finding, numerical] (Xiaodong Wu 2020, [doi:10.1175/jpo-d-19-0225.1](https://doi.org/10.1175/jpo-d-19-0225.1))
- **C594.** UAV visible imagery calibrated against a fluorometer mapped fluorescent-tracer concentration on a 2×2 m grid across three measurement campaigns. *Regime: Visible-camera imagery produced georeferenced fluorescein and Rhodamine WT concentration maps on a 2×2 m grid..* [direct_finding, field] (Paweł Burdziakowski 2021, [doi:10.3390/s21113905](https://doi.org/10.3390/s21113905))
- **C595.** Three nine-probe estuary releases showed open-source GPS/conductivity drifters can track plume attenuation and parameterize mean velocity and salinity-proxy concentration. *Regime: Open-source GPS probes tracked plume position, temperature, and conductivity until attenuation and supported an analytical mean-flow/salinity fit..* [direct_finding, field] (Vladimir Divić 2020, [doi:10.3390/w12010209](https://doi.org/10.3390/w12010209))
- **C596.** Black Sea coherent structures identified persistent aggregation, barriers, and cross-shelf pathways, with the Rim Current accounting for 44% of climatological attraction strength. *Regime: Persistent squeezelines, jets, barriers, and shelf pathways organized aggregation and cross-shelf export; the Rim Current contributed 44% of climatological attraction strength..* [direct_finding, numerical] (Mainara Biazati Gouveia 2025, [doi:10.1038/s41598-025-00432-5](https://doi.org/10.1038/s41598-025-00432-5))
- **C1362.** HF-radar Lagrangian diagnostics at 3.5–25 km scales link attracting fronts and negative divergence to phytoplankton clustering, while positive-divergence filaments indicate upward nutrient injection and high chlorophyll. *Regime: Effect of small scale transport processes on phytoplankton distribution in coastal seas.* [direct_finding, mixed] (Ismael Hernández‐Carrasco 2018, [doi:10.1038/s41598-018-26857-9](https://doi.org/10.1038/s41598-018-26857-9))
- **C1363.** A 250 m triangular oxygen-control volume on a Hawaiian reef produced Eulerian net-production estimates agreeing with dye-based Lagrangian estimates at r²=0.81; drifters moved 30–100% faster than dye and depth-mean currents. *Regime: Continuous measurements of net production over a shallow reef community using a modified Eulerian approach.* [direct_finding, field] (James L. Falter 2008, [doi:10.1029/2007jc004663](https://doi.org/10.1029/2007jc004663))
- **C1364.** Validation with 4,130 drifter–radar pairs gave X-band radar near-surface current RMSE of 4 cm/s and direction error of 12°, resolving roughly 500 m currents to 3 km range. *Regime: Near-Surface Current Mapping by Shipboard Marine X-Band Radar: A Validation.* [direct_finding, field] (Björn Lund 2018, [doi:10.1175/jtech-d-17-0154.1](https://doi.org/10.1175/jtech-d-17-0154.1))
- **C1691.** Marine population connectivity cannot be inferred from circulation alone: resolving larval pathways requires coordinated Lagrangian physical observations and biological evidence because fronts, stratification, vertical behavior, tides, mortality, and spawning timing jointly shape dispersal. *Regime: Coastal, shelf, bay and estuarine transport of weakly swimming marine early life stages, with source-specific hydrodynamic and biological controls..* [literature_review_statement, review] (Glen Gawarkiewicz 2007, [doi:10.5670/oceanog.2007.28](https://doi.org/10.5670/oceanog.2007.28))

## Papers

- Glen Gawarkiewicz (2007). Observing Larval Transport Processes Affecting Population Connectivity: Progress and Challenges. *Oceanography*. [doi:10.5670/oceanog.2007.28](https://doi.org/10.5670/oceanog.2007.28)
- Ismael Hernández‐Carrasco (2018). Effect of small scale transport processes on phytoplankton distribution in coastal seas. *Scientific Reports*. [doi:10.1038/s41598-018-26857-9](https://doi.org/10.1038/s41598-018-26857-9)
- James L. Falter (2008). Continuous measurements of net production over a shallow reef community using a modified Eulerian approach. *Journal of Geophysical Research Atmospheres*. [doi:10.1029/2007jc004663](https://doi.org/10.1029/2007jc004663)
- Lisa V. Lucas (2020). Timescale Methods for Simplifying, Understanding and Modeling Biophysical and Water Quality Processes in Coastal Aquatic Ecosystems: A Review. *Water*. [doi:10.3390/w12102717](https://doi.org/10.3390/w12102717)
- Björn Lund (2018). Near-Surface Current Mapping by Shipboard Marine X-Band Radar: A Validation. *Journal of Atmospheric and Oceanic Technology*. [doi:10.1175/jtech-d-17-0154.1](https://doi.org/10.1175/jtech-d-17-0154.1)
- William S. Arnold (2005). Dispersal of an introduced larval cohort in a coastal lagoon. *Limnology and Oceanography*. [doi:10.4319/lo.2005.50.2.0587](https://doi.org/10.4319/lo.2005.50.2.0587)
- Dubravko Justić (2021). Transport Processes in the Gulf of Mexico Along the River-Estuary-Shelf-Ocean Continuum: a Review of Research from the Gulf of Mexico Research Initiative. *Estuaries and Coasts*. [doi:10.1007/s12237-021-01005-1](https://doi.org/10.1007/s12237-021-01005-1)
- Kabir Suara (2014). High-Resolution GNSS-Tracked Drifter for Studying Surface Dispersion in Shallow Water. *Journal of Atmospheric and Oceanic Technology*. [doi:10.1175/jtech-d-14-00127.1](https://doi.org/10.1175/jtech-d-14-00127.1)
- Xiaodong Wu (2020). Mechanisms of Mid- to Outer-Shelf Transport of Shoreline-Released Tracers. *Journal of Physical Oceanography*. [doi:10.1175/jpo-d-19-0225.1](https://doi.org/10.1175/jpo-d-19-0225.1)
- Paweł Burdziakowski (2021). Tracking Fluorescent Dye Dispersion from an Unmanned Aerial Vehicle. *Sensors*. [doi:10.3390/s21113905](https://doi.org/10.3390/s21113905)
- Vladimir Divić (2020). Application of Open Source Electronics for Measurements of Surface Water Properties in an Estuary: A Case Study of River Jadro, Croatia. *Water*. [doi:10.3390/w12010209](https://doi.org/10.3390/w12010209)
- Mainara Biazati Gouveia (2025). Persistent Lagrangian transport patterns in the Black Sea identified from climatological Lagrangian Coherent Structures. *Scientific Reports*. [doi:10.1038/s41598-025-00432-5](https://doi.org/10.1038/s41598-025-00432-5)
- Kabir Suara (2017). Relative dispersion of clustered drifters in a small micro-tidal estuary. *Estuarine Coastal and Shelf Science*. [doi:10.1016/j.ecss.2017.05.001](https://doi.org/10.1016/j.ecss.2017.05.001)
