# Sediment and morphology observations

`field.sediment` | Sampling and seabed surveys.

Parent: [Field measurements](field.md)

Papers: 6. Claims: 3. Equations: 1.

## Synthesis

**Well established.** Field sediment transport is intermittent, vertically structured and often strongly two-way; concentration or delivery alone does not determine net accumulation because advection, resuspension, settling and export must be measured within a sediment budget.

**Governing physics.** Waves mobilize grains, asymmetric orbital motion, undertow and currents advect them, turbulence suspends sediment and settling plus bed exchange controls concentration. At inlets and reefs, persistent directional forcing and local trapping or flushing integrate these processes over larger scales.

**Dimensionless parameters.** Controls include Shields and mobility numbers, Rouse number, sediment fall velocity relative to orbital velocity, wave-current ratio, suspension height relative to boundary-layer thickness, sampling duration relative to waves and events, gross-to-net flux ratio and closure error relative to measured transport.

**Major equations.** Suspended flux is the time and depth integral of concentration times velocity, bed change follows sediment continuity, and settling–diffusion balances describe mean concentration profiles. Trap or tray mass rates measure gross directional exchange, while surveys close net volume budgets.

**Typical methods.** Campaigns pair concentration samplers, optical or acoustic sensors, pumps or pressure-difference collectors, velocity profilers, bed-level surveys, sediment traps/trays and tracers; synchronize sampling, calibrate grain and turbidity response, resolve vertical profiles and waves, estimate uncertainty and close gross and net budgets.

**Numerical models.** The reviewed set is observation-centered. Interpretation uses suspension-profile, flux and sediment-continuity concepts; direct process-model calibration is not established for this node, and instrument-comparison and fluorescent-tracer papers await full-text review.

**Experimental datasets.** Reviewed evidence includes 65 seven-level concentration profiles in about 1.5 m depth, paired two-way flux trays at four sites on two turbid Great Barrier Reef systems and seasonal entrance-bar observations at Wilson Inlet.

**Validated ranges.** The pressure-difference sampler resolved roughly three-minute profiles from 1 cm above bed upward; reef trays measured gross flux of 34 to over 640 g/m2/d while net sedimentation stayed below 122 g/m2/d. Results are method- and site-specific.

**Recent advances.** Recent advances combine acoustic/optical arrays, fluorescent and RFID tracers, sediment-imaging velocimetry, autonomous platforms, UAV and sonar morphology, Bayesian sensor fusion and real-time sediment-budget assimilation.

**Disagreements.** Optical sensors offer high frequency but depend on grain size and bubbles; pumped samples are direct but intrusive and sparse; traps can disturb flow and mix deposition with resuspension. Gross flux, suspended concentration and morphological change answer different questions.

**Limitations.** Spatial aliasing, sensor calibration drift, biofouling, bubbles, uncertain sampling efficiency, unmeasured bedload, short deployments, storm gaps, tracer recovery, changing bathymetry and open control-volume boundaries can prevent sediment-budget closure.

**Open questions.** Priorities include co-located bedload and suspension, event-resolving vertical flux, tracer recovery and mixing depth, autonomous calibration, cohesive–sand mixtures, reef and vegetation interactions, cross-shore/alongshore integration and open standardized field benchmarks.

**Seminal papers.** Pump and bottle sampling established concentration profiles; optical and acoustic backscatter enabled high-frequency suspension records, tracers revealed pathways, and synchronized velocity–concentration measurements advanced direct flux estimation.

## Equations

### pressure-difference suction sediment sampler

$$
y(t,\mathbf{x})=\mathcal{M}[\mathbf{o}(t),\mathbf{b},\mathbf{p}]
$$

Regime: Sixty-five profiles; seven simultaneous elevations starting about 1 cm above bed; approximately 3 min samples in about 1.5 m water depth.

Variables: `y` predicted or derived coastal response; `o` event observations; `b` bathymetry or beach state; `p` model or instrument parameters; normalized observation-model mapping

Source: (Nielsen 1984, [doi:10.1016/0378-3839(84)90022-x](https://doi.org/10.1016/0378-3839(84)90022-x))

## Claims

- **C183.** At four sites on two turbid Great Barrier Reef systems, paired trays measured two-way sediment flux from 34 to more than 640 g/m2/d while mean net sedimentation remained below 122 g/m2/d, demonstrating that high delivery need not imply high accumulation. *Regime: Shallow turbid inshore reefs; tray and site-specific limitations apply..* [direct_finding, field] (Anon. 2012, [doi:10.2112/jcoastres-d-11-00171.1](https://doi.org/10.2112/jcoastres-d-11-00171.1))
- **C259.** A pump-free pressure-difference sampler collected seven suspended-sand samples simultaneously from about 1 cm above the bed upward during approximately 3 min intervals in roughly 1.5 m depth, yielding 65 field concentration profiles with hydraulic and sediment metadata. *Regime: Sixty-five profiles; seven simultaneous elevations starting about 1 cm above bed; approximately 3 min samples in about 1.5 m water depth..* [direct_finding, field] (Nielsen 1984, [doi:10.1016/0378-3839(84)90022-x](https://doi.org/10.1016/0378-3839(84)90022-x))
- **C1523.** A quantitative Venice Lagoon assessment maps cumulative human disturbance of shallow coastal seabeds and associated geomorphic footprints. *Regime: Assessing the human footprint on the sea-floor of coastal systems: the case of the Venice Lagoon, Italy.* [direct_finding, field] (Fantina Madricardo 2019, [doi:10.1038/s41598-019-43027-7](https://doi.org/10.1038/s41598-019-43027-7))

## Papers

- Nielsen (1984). Field measurements of time-averaged suspended sediment concentrations under waves. *Coastal Engineering*. [doi:10.1016/0378-3839(84)90022-x](https://doi.org/10.1016/0378-3839(84)90022-x)
- Fantina Madricardo (2019). Assessing the human footprint on the sea-floor of coastal systems: the case of the Venice Lagoon, Italy. *Scientific Reports*. [doi:10.1038/s41598-019-43027-7](https://doi.org/10.1038/s41598-019-43027-7)
- Anon. (2012). A Field-Based Technique for Measuring Sediment Flux on Coral Reefs: Application to Turbid Reefs on the Great Barrier Reef. *Journal of Coastal Research*. [doi:10.2112/jcoastres-d-11-00171.1](https://doi.org/10.2112/jcoastres-d-11-00171.1)
- Ranasinghe (1999). The seasonal closure of tidal inlets: Wilson Inlet—a case study. *Coastal Engineering*. [doi:10.1016/s0378-3839(99)00007-1](https://doi.org/10.1016/s0378-3839(99)00007-1)
- Alan Cuthbertson (2017). Model studies for flocculation of sand-clay mixtures. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2017.11.006](https://doi.org/10.1016/j.coastaleng.2017.11.006)
- Alexandra Spodar (2017). Evolution of a beach nourishment project using dredged sand from navigation channel, Dunkirk, northern France. *Journal of Coastal Conservation*. [doi:10.1007/s11852-017-0514-8](https://doi.org/10.1007/s11852-017-0514-8)
