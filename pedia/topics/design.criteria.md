# Design conditions and criteria

`design.criteria` | Selection of design loads and levels.

Parent: [Coastal engineering design](design.md)

Papers: 5. Claims: 3. Equations: 0.

Used by pyCoastal design modules: Seawall design.

## Synthesis

**Well established.** Coastal design criteria translate probabilistic hazards, performance objectives, consequence classes and physical response into verifiable elevations, loads, geometry and maintenance requirements; compliance with a nominal return period alone does not establish lifecycle reliability.

**Governing physics.** Waves, water levels, currents, erosion and material or ecosystem response combine nonlinearly, while sea-level rise shifts baseline hazards and deterioration changes capacity. Spatial nonuniformity and weak points can govern failure even when average performance is acceptable.

**Dimensionless parameters.** Controls include reliability index, return-period-to-design-life ratio, freeboard relative to wave/runup scale, demand-to-capacity ratio, partial safety factors, crest deficit, attenuation or damage threshold and layout-uniformity parameters such as Sr.

**Major equations.** Criteria use extreme-value quantiles, load and resistance factors, reliability or exceedance probability, freeboard and crest checks and response functions for overtopping, stability or attenuation. Under nonstationarity, annual distributions shift through time and lifecycle failure integrates yearly exceedance.

**Typical methods.** Workflows define limit states and consequences, estimate joint and nonstationary hazards, propagate uncertainty, select target reliability, evaluate alternatives and failure modes, audit constructed geometry with surveys, test response across representative conditions and specify inspection, maintenance and adaptation triggers.

**Numerical models.** The set includes a multi-distributional nonstationary extreme-value model, geospatial crest-compliance analysis and a layout-response criterion for vegetation attenuation. Direct intermediate-depth design-wave selection remains pending full-text review.

**Experimental datasets.** Reviewed evidence includes changing annual sea-level extreme distributions, airborne-LiDAR profiles of federal levees in south Louisiana and four flexible-vegetation layouts tested for spatial wave-attenuation uniformity.

**Validated ranges.** The levee audit found about 5% of evaluated points met the stated 100-year minimum; the vegetation Sr threshold was derived from four tested layouts; the sea-level method addresses shifting annual distributions. None supplies universal criteria across asset classes.

**Recent advances.** Recent advances combine nonstationary extremes, Bayesian joint hazards, lidar and digital twins for as-built compliance, real-time condition monitoring, probabilistic fragility and adaptive criteria that trigger staged upgrades as observations and projections change.

**Disagreements.** Stationary return periods are familiar but can misstate future magnitude under changing baselines. Prescriptive geometry is auditable but may not capture system response, while performance-based criteria are flexible yet depend on models, uncertainty and validation.

**Limitations.** Hazard nonstationarity, dependence, model and survey error, undocumented weak points, construction tolerance, deterioration, maintenance, climate scenario spread and unmodeled failure modes can undermine nominal compliance. Evidence is heterogeneous and sparse for cross-system transfer.

**Open questions.** Priorities include joint nonstationary hazards, lifecycle and adaptive reliability targets, system-versus-component criteria, nature-based durability, cascading failure, equity and consequence classes, digital compliance monitoring and transparent treatment of deep uncertainty.

**Seminal papers.** Return-period design and factor-of-safety methods established prescriptive criteria; reliability-based design introduced probabilistic load–resistance balance, followed by performance-based, lifecycle and adaptive approaches under nonstationary climate.

## Claims

- **C159.** Airborne-LiDAR crest profiles showed only about 5% of evaluated federal levee crest points in the Atchafalaya study met the USACE minimum height for the 100-year flood. *Regime: The two evaluated federal levees and the contemporaneous USACE height requirement; this is not a structural-failure probability..* [direct_finding, field] (Palaseanu-Lovejoy 2014, [doi:10.1016/j.isprsjprs.2014.02.010](https://doi.org/10.1016/j.isprsjprs.2014.02.010))
- **C1487.** A coupled seepage and deformation analysis relates tidal groundwater fluctuations to the performance of coastal deep foundation pits. *Regime: Seepage Flow Model and Deformation Properties of Coastal Deep Foundation Pit under Tidal Influence.* [direct_finding, numerical] (Shuchen Li 2018, [doi:10.1155/2018/9714901](https://doi.org/10.1155/2018/9714901))
- **C1603.** A South African recreational-coast case derives transferable planning parameters for balancing wave climate, sediment behavior, structural function, safety and public use in coastal-structure design. *Regime: DESIGN OF COASTAL STRUCTURES FOR RECREATIONAL PURPOSES.* [literature_review_statement, review] (O'Connell 1982, [doi:10.9753/icce.v18.152](https://doi.org/10.9753/icce.v18.152))

## Papers

- Shuchen Li (2018). Seepage Flow Model and Deformation Properties of Coastal Deep Foundation Pit under Tidal Influence. *Mathematical Problems in Engineering*. [doi:10.1155/2018/9714901](https://doi.org/10.1155/2018/9714901)
- O'Connell (1982). DESIGN OF COASTAL STRUCTURES FOR RECREATIONAL PURPOSES. *Coastal Engineering Proceedings*. [doi:10.9753/icce.v18.152](https://doi.org/10.9753/icce.v18.152)
- Palaseanu-Lovejoy (2014). Levee crest elevation profiles derived from airborne lidar-based high resolution digital elevation models in south Louisiana. *ISPRS Journal of Photogrammetry and Remote Sensing*. [doi:10.1016/j.isprsjprs.2014.02.010](https://doi.org/10.1016/j.isprsjprs.2014.02.010)
- Wang (2026). Vegetation layouts influence the spatial uniformity of wave attenuation: Laboratory insights. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2025.104937](https://doi.org/10.1016/j.coastaleng.2025.104937)
- Bardsley (1990). Estimating future sea level extremes under conditions of sea level rise. *Coastal Engineering*. [doi:10.1016/0378-3839(90)90028-u](https://doi.org/10.1016/0378-3839(90)90028-u)
