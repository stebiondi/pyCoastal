# Reefs and living shorelines

`nature_based.reefs` | Oyster, coral, and constructed reef protection.

Parent: [Nature-based coastal protection](nature_based.md)

Subtopics: [Living shoreline breakwalls](nature_based.reefs.breakwalls.md)

Papers: 10. Claims: 7. Equations: 1.

## Synthesis

**Well established.** Reefs and reef-like living shorelines can reduce wave energy, currents, and shoreline erosion, but protection is conditional on crest elevation relative to water level, porosity and roughness, reef width and morphology, incident forcing, sediment setting, biological persistence, and maintenance.

**Governing physics.** Breaking on reef rims creates setup and cross-reef pressure gradients; porous and rough reef material dissipates energy; emergence, submergence, wave breaking, bottom friction, lagoon wind-wave generation, and bidirectional sediment resuspension determine the realized response.

**Dimensionless parameters.** Important nondimensional controls are relative crest or reef height, relative submergence, porosity, transmission coefficient, friction and resistance coefficients, relative wave height and depth, and ratios separating wave, infragravity, and locally generated lagoon energy.

**Major equations.** Core formulations include radiation-stress/setup balances, open-channel reef-top and reef-rim control, energy-flux transmission Kt=sqrt(Ft/Fi), Darcy-Forchheimer porous resistance, shallow-water breaking and friction balances, and paired-tray sediment mass balance.

**Typical methods.** Evidence combines reef-platform flumes, pressure and velocity arrays across porous structures, paired treatment-control shoreline experiments, oyster demographic and topographic surveys, sediment mass balances, spectral and surfbeat models, and multi-year lifecycle monitoring.

**Numerical models.** The screened evidence uses analytical reef-control and porous-transmission models plus phase-averaged SWAN and surfbeat-resolving XBeach; model choice must preserve locally generated wind waves when they dominate reef-lagoon storm energy.

**Experimental datasets.** Key datasets include nearly 1000 boat wakes at two Florida breakwalls, a four-year three-site hybrid intervention, six Louisiana reefs revisited after ten years, four paired-tray sites on two Great Barrier Reef systems, a steep-faced reef-platform experiment, and comparative restored-oyster substrates in Virginia.

**Validated ranges.** Observed regimes include 0.7-porosity branch barriers with mean energy transmission 53%, 0.9-porosity barriers with 83%, relative breakwall height about 0.5-1 for clear tidal modulation, four-year shoreline trends from about 1 m/y advance to nearly 2 m/y retreat, and ten-year oyster density below 60 individuals/m2 with erosion near 1 m/y.

**Recent advances.** Recent work shifts from proving short-term attenuation toward optimizing substrate and elevation, testing decade-scale ecological persistence, resolving cyclone-specific model physics, and embedding future conditions, maintenance, and adaptive action into design.

**Disagreements.** Short-term hybrid success and decade-scale native-reef failure are not universal contradictions: structure, exposure, recruitment, salinity, maintenance, and monitoring horizon differ. Likewise, wave-height amplification over a submerged reef need not imply increased energy flux, so performance metrics must match the erosion mechanism.

**Limitations.** Most studies cover few sites, narrow structural designs, boat wakes or ordinary wind waves rather than extremes, and limited design lives. Geometry, biology, water quality, sea-level rise, material degradation, and maintenance covary, preventing simple transfer of one attenuation coefficient.

**Open questions.** Priorities are storm-scale multi-site validation, coupled ecology-hydraulics-morphology prediction, lifecycle performance under recruitment failure and sea-level rise, metric choice for height versus energy flux, maintainable porous materials, and adaptive thresholds for intervention.

**Seminal papers.** Within this screened slice, the 2005 steep-faced reef study establishes coupled setup-flow control, while the 2020 paired breakwall studies connect porous-transmission physics to measured shoreline and habitat response.

## Equations

### Wave-energy transformation balance

$$
\nabla\cdot(E\mathbf{C}_g)=-D_b-D_f
$$

Regime: Regular waves over the tested steep-face, sloping reef-top physical models; extrapolation to irregular, directional and strongly three-dimensional reefs is limited.

Variables: `E` wave energy density; `C_g` group velocity; `D_b` breaking dissipation; `D_f` bottom-friction or other dissipation

Source: (Gourlay 1994, [doi:10.1016/0378-3839(94)90013-2](https://doi.org/10.1016/0378-3839(94)90013-2))

## Claims

- **C180.** For a laboratory steep-faced horizontal reef, wave-generated flow was organized into reef-top-control and reef-rim-control regimes, and coupled open-channel setup-flow relationships reproduced most measured values with reasonable accuracy. *Regime: Two-dimensional horizontal reef tops with steep faces under wave-driven quasi-steady flow..* [direct_finding, mixed] (Gourlay 2005, [doi:10.1016/j.coastaleng.2004.11.007](https://doi.org/10.1016/j.coastaleng.2004.11.007))
- **C182.** Ten years after construction of six Louisiana oyster reefs, oyster density was below 60 individuals/m2 versus above 1000/m2 during 2009-2011, and both reef and reference shorelines continued eroding at about 1 m/y. *Regime: Sister Lake native-shell fringing reefs exposed to highly variable salinity; results do not imply all oyster defenses fail..* [direct_finding, field] (La Peyre 2022, [doi:10.1016/j.ecoleng.2022.106603](https://doi.org/10.1016/j.ecoleng.2022.106603))
- **C185.** A restored-oyster field study found that coastal-protection performance depends jointly on reef elevation, substrate type, and adjacent marsh-edge morphology, with wave dissipation effective primarily when water depth is near or below reef crest height. *Regime: The tested Virginia intertidal reef designs and wind-wave conditions; storm-scale and long-term transfer remain unresolved..* [direct_finding, field] (Bieri 2026, [doi:10.1016/j.ecss.2026.110156](https://doi.org/10.1016/j.ecss.2026.110156))
- **C338.** Regular-wave experiments over an idealized steep-faced fringing reef showed that wave transformation is controlled by shoaling and breaking at the reef edge followed by reforming waves over the reef flat, providing a bounded laboratory basis for predicting reef-flat wave heights and setup. *Regime: Regular waves over the tested steep-face, sloping reef-top physical models; extrapolation to irregular, directional and strongly three-dimensional reefs is limited..* [direct_finding, experimental] (Gourlay 1994, [doi:10.1016/0378-3839(94)90013-2](https://doi.org/10.1016/0378-3839(94)90013-2))
- **C350.** Across the coral-reef studies synthesized by the meta-analysis, reefs reduced wave energy by an average of 97%, with reef crests accounting for 86% dissipation; these global averages should not be treated as site-specific design coefficients. *Regime: Global coral-reef evidence synthesized in the indexed abstract; site-specific hydrodynamic regimes are not recoverable from the abstract..* [literature_review_statement, review] (Filippo Ferrario 2014, [doi:10.1038/ncomms4794](https://doi.org/10.1038/ncomms4794))
- **C1205.** Flume measurements showed restored coral-canopy attenuation rose with coral cover; force–velocity energy loss agreed with observed wave-height decay, and well-designed canopies dissipated more than 50% of incoming energy under typical reef-flat conditions. *Regime: Wave Attenuation by Restored Coral Reef Canopies: Implications for Coastal Protection.* [direct_finding, mixed] (Geldard 2025, [doi:10.1029/2025jc022854](https://doi.org/10.1029/2025jc022854))
- **C1370.** An oyster-reef restoration review recommends matching site, substrate, species and genotype to future environmental suitability and explicit ecosystem-service and socioeconomic goals. *Regime: Contemporary Oyster Reef Restoration: Responding to a Changing World.* [literature_review_statement, review] (Alice H. Howie 2021, [doi:10.3389/fevo.2021.689915](https://doi.org/10.3389/fevo.2021.689915))

## Papers

- Filippo Ferrario (2014). The effectiveness of coral reefs for coastal hazard risk reduction and adaptation. *Nature Communications*. [doi:10.1038/ncomms4794](https://doi.org/10.1038/ncomms4794)
- Gourlay (1994). Wave transformation on a coral reef. *Coastal Engineering*. [doi:10.1016/0378-3839(94)90013-2](https://doi.org/10.1016/0378-3839(94)90013-2)
- Gourlay (2005). Wave-generated flow on coral reefs—an analysis for two-dimensional horizontal reef-tops with steep faces. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2004.11.007](https://doi.org/10.1016/j.coastaleng.2004.11.007)
- Alice H. Howie (2021). Contemporary Oyster Reef Restoration: Responding to a Changing World. *Frontiers in Ecology and Evolution*. [doi:10.3389/fevo.2021.689915](https://doi.org/10.3389/fevo.2021.689915)
- La Peyre (2022). Long-term assessments are critical to determining persistence and shoreline protection from oyster reef nature-based coastal defenses. *Ecological Engineering*. [doi:10.1016/j.ecoleng.2022.106603](https://doi.org/10.1016/j.ecoleng.2022.106603)
- Geldard (2025). Wave Attenuation by Restored Coral Reef Canopies: Implications for Coastal Protection. *Journal of Geophysical Research: Oceans*. [doi:10.1029/2025jc022854](https://doi.org/10.1029/2025jc022854)
- Bieri (2026). Designing restored oyster reefs to enhance coastal protection benefits. *Estuarine, Coastal and Shelf Science*. [doi:10.1016/j.ecss.2026.110156](https://doi.org/10.1016/j.ecss.2026.110156)
- Anon. (2012). A Field-Based Technique for Measuring Sediment Flux on Coral Reefs: Application to Turbid Reefs on the Great Barrier Reef. *Journal of Coastal Research*. [doi:10.2112/jcoastres-d-11-00171.1](https://doi.org/10.2112/jcoastres-d-11-00171.1)
- Drost (2019). Predicting the hydrodynamic response of a coastal reef-lagoon system to a tropical cyclone using phase-averaged and surfbeat-resolving wave models. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2019.103525](https://doi.org/10.1016/j.coastaleng.2019.103525)
- DiPetto (2025). Future-oriented coastal protection: The utility of living shorelines under changing climatic conditions. *Nature-Based Solutions*. [doi:10.1016/j.nbsj.2025.100285](https://doi.org/10.1016/j.nbsj.2025.100285)
