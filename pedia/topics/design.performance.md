# Performance-based design

`design.performance` | Response and consequence-based objectives.

Parent: [Coastal engineering design](design.md)

Papers: 3. Claims: 2. Equations: 1.

Used by pyCoastal design modules: Breakwater design.

## Synthesis

**Well established.** Performance-based coastal design begins with explicit functional objectives and limit states, maps uncertain hazards to response and consequences, and verifies that structural, hydraulic, morphological and operational performance remains acceptable over stated conditions and time horizons.

**Governing physics.** Performance emerges from interaction of waves, water levels, currents, sediment and ecological or structural geometry; changing submergence, depth, exposure, material state and morphology alter loads, attenuation, erosion, overtopping and failure pathways.

**Dimensionless parameters.** Useful controls include demand-to-capacity and reliability indices, annual exceedance probability, relative crest elevation or submergence, response normalized by allowable limit, adaptation increment relative to sea-level rise, lifecycle utilization and expected loss or downtime ratios.

**Major equations.** Core formulations combine hazard exceedance with conditional response and limit-state probability, reliability or fragility functions, lifecycle accumulation and consequence integration; system-specific equations relate crest or reef elevation, water depth, wave transformation, sediment volume and load resistance.

**Typical methods.** Workflows define stakeholders and objectives, identify hazards and failure modes, select measurable performance metrics and thresholds, propagate joint forcing through response models, validate component behavior, quantify epistemic and aleatory uncertainty, compare alternatives and monitor triggers for adaptation.

**Numerical models.** Current evidence combines scenario-based beach-defense crest and volume design with observed reef wave-attenuation performance; broader response-based, reliability and consequence models are represented only by title-screened records and are not treated as extracted evidence.

**Experimental datasets.** The reviewed evidence includes four southeast England mixed sand–gravel defenses evaluated under 1–5 m sea-level-rise scenarios and a Virginia restored-oyster field experiment comparing two substrates, reef elevation, water level and marsh-edge response.

**Validated ranges.** Direct support is limited to four mixed sand–gravel sites and one restored-oyster setting with two substrates. It does not establish transferable performance targets, fragilities, design lives or reliability levels for caissons, levees, pumps or other systems.

**Recent advances.** Recent advances use environmental contours, stochastic response simulation, time-dependent climate scenarios, lifecycle reliability, adaptive pathways, digital monitoring, coupled consequence assessment and performance objectives for hybrid and nature-based coastal systems.

**Disagreements.** Prescriptive event-based design is simpler and transparent, whereas response-based probabilistic design better represents nonlinear response and joint uncertainty but requires more data and computation. Nature-based performance also changes biologically and morphologically, challenging fixed resistance assumptions.

**Limitations.** The evidence slice is small; objectives and acceptable consequences are context dependent; hazard dependence and nonstationarity are difficult to estimate; model and deterioration uncertainty can dominate tails; ecological functions and cascading systems lack common metrics; and monitoring may not match design variables.

**Open questions.** Priorities include multi-hazard joint probability, response-based versus event-based calibration, time-dependent deterioration and climate adaptation, system fragility and cascading failure, nature-based lifecycle reliability, equity-weighted consequences, observation updating and transferable verification datasets.

**Seminal papers.** Reliability-based and limit-state structural design established probabilistic performance checks; coastal work extended them to overtopping, sliding, erosion, flood consequences and lifecycle adaptation, while performance-based earthquake engineering supplied hazard–response–damage–loss integration concepts.

## Equations

### Scenario crest-rise amplification

$$
\Delta z_c/\Delta SLR\le 1.26
$$

Regime: Four fixed-position southeast England mixed sand-gravel beach defenses under the tested 1-5 m scenarios.

Variables: `Delta z_c` required increase in beach crest elevation; `Delta SLR` imposed sea-level rise

Source: (Dornbusch 2017, [doi:10.1016/j.coastaleng.2017.03.006](https://doi.org/10.1016/j.coastaleng.2017.03.006))

## Claims

- **C187.** Across four southeast England mixed sand-gravel defenses under 1-5 m sea-level-rise scenarios, required crest elevation increased by as much as 1.26 times the sea-level rise, with the largest beach-volume adjustments on shallow foreshores and obliquely exposed beaches. *Regime: Fixed-position mixed sand-gravel beaches represented by the Shingle Beach Run-up Tool and Barrier Inertia Model; future wave and sediment changes remain uncertain..* [direct_finding, numerical] (Dornbusch 2017, [doi:10.1016/j.coastaleng.2017.03.006](https://doi.org/10.1016/j.coastaleng.2017.03.006))
- **C1426.** A practitioner-oriented catalogue organizes tested eco-engineering designs for breakwaters, revetments, seawalls, piers, and tidal walls to enhance biodiversity and ecosystem services. *Regime: Design catalogue for eco-engineering of coastal artificial structures: a multifunctional approach for stakeholders and end-users.* [literature_review_statement, review] (Kathryn A. O’Shaughnessy 2019, [doi:10.1007/s11252-019-00924-z](https://doi.org/10.1007/s11252-019-00924-z))

## Papers

- Kathryn A. O’Shaughnessy (2019). Design catalogue for eco-engineering of coastal artificial structures: a multifunctional approach for stakeholders and end-users. *Urban Ecosystems*. [doi:10.1007/s11252-019-00924-z](https://doi.org/10.1007/s11252-019-00924-z) [published version, CC BY](https://link.springer.com/content/pdf/10.1007/s11252-019-00924-z.pdf)
- Dornbusch (2017). Design requirement for mixed sand and gravel beach defences under scenarios of sea level rise. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2017.03.006](https://doi.org/10.1016/j.coastaleng.2017.03.006)
- Bieri (2026). Designing restored oyster reefs to enhance coastal protection benefits. *Estuarine, Coastal and Shelf Science*. [doi:10.1016/j.ecss.2026.110156](https://doi.org/10.1016/j.ecss.2026.110156) [submitted manuscript, read only](https://papers.ssrn.com/sol3/Delivery.cfm/efdb6ddd-282e-43ff-bebf-31f0a0de97e2-MECA.pdf?abstractid=6110269&mirid=1)
