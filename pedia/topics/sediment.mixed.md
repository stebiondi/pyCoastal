# Mixed sediment

`sediment.mixed` | Sand-mud and graded mixtures.

Parent: [Sediment transport](sediment.md)

Papers: 8. Claims: 7. Equations: 0.

## Synthesis

**Well established.** Mixed sediment cannot generally be represented as independent pure fractions: increasing fines can switch erosion mode, while sand-mud interactions alter transport and morphology.

**Governing physics.** Composition affects cohesion, dry bulk density, granular or silt-skeleton structure, roughness, erosion thresholds, and the exchange between active layer and substrate.

**Dimensionless parameters.** Key controls include applied-to-critical shear ratio, mud/silt fraction, clay fraction, grain-size distribution, dry bulk density, consolidation state, and active-layer/substrate composition contrast.

**Major equations.** Available formulations include composition-interpolated erosion laws, momentum-balance critical-stress relations, modified Shields-style thresholds, and multi-fraction active-layer conservation equations.

**Typical methods.** The evidence combines erosion experiments, analytical momentum and eigenstructure analysis, realistic hydro-sedimentary hindcasting, and schematized long-term morphodynamic scenarios.

**Numerical models.** Models range from shelf suspended-sediment simulations to tidal-basin morphodynamics and multi-fraction active-layer systems; both physical interaction terms and mathematical well-posedness affect credibility.

**Experimental datasets.** The directly accessible experimental evidence resolves a sand-silt transition near 35% silt; other mixture datasets are represented indirectly through model-data comparisons and compiled threshold data.

**Validated ranges.** Reported source-specific transitions include about 10-20% mud (3-6% clay) for switching from pure-sand erosion and about 35% silt for a sand- to silt-dominated threshold change.

**Recent advances.** Recent work unifies sand-to-mud thresholds, identifies a sand-silt tipping point, quantifies sand-mud morphological interaction, and diagnoses broader ill-posed domains in mixed-fraction models.

**Disagreements.** The critical fine fraction is not universal: clay-bearing sand-mud and nonclay sand-silt mixtures show different transition contents and mechanisms, reflecting mineralogy, grain size, density, and consolidation.

**Limitations.** This branch has only five abstract-accessible sources. Several direct graded, sand-clay, sand-silt, and mixed sand-gravel studies remain title-only, limiting synthesis of transport rates, segregation, waves, and field transferability.

**Open questions.** Priorities are transferable transition laws, joint erosion-deposition behavior, hiding/exposure and armoring, flocculation-segregation coupling, wave-current transport, and stable multi-fraction numerics.

**Seminal papers.** The accessible evidence extends Shields-type incipient motion, cohesive erosion concepts, and Hirano active-layer morphodynamics into composition-dependent mixed-bed formulations.

## Claims

- **C527.** Bay of Biscay modelling supported an abrupt erosion-law transition and a first critical mud fraction of about 10-20% (3-6% clay), below which pure-sand erosion should be prescribed. *Regime: fine sand, mud, and mixtures on the Bay of Biscay shelf.* [direct_finding, mixed] (Baptiste Mengual 2017, [doi:10.3390/w9080564](https://doi.org/10.3390/w9080564))
- **C528.** A momentum-balance formulation reproduced erosion thresholds from sand-mud mixtures to pure mud using mud content and the dry bulk density of the mud component. *Regime: sand-mud mixtures through the pure-sand and pure-mud endpoints and consolidation.* [direct_finding, analytical] (Dake Chen 2021, [doi:10.3389/fmars.2021.713039](https://doi.org/10.3389/fmars.2021.713039))
- **C529.** Sand-silt experiments identified a tipping point near 35% silt: below it Shields behavior applied, while above it a stable silt skeleton raised the threshold; a modified formula reduced average bias to about 10%. *Regime: sand-silt beds spanning sand-dominated and silt-dominated composition.* [direct_finding, experimental] (Peng Yao 2022, [doi:10.1029/2021wr031788](https://doi.org/10.1029/2021wr031788))
- **C530.** Mixed-fraction active-layer models can be ill posed under both aggradation and degradation, producing grid-dependent short-wave oscillations and possible numerical failure. *Regime: graded river-bed aggradation and degradation represented by Hirano active-layer and vertically continuous models.* [direct_finding, analytical] (Víctor Chavarrías 2018, [doi:10.1016/j.advwatres.2018.02.011](https://doi.org/10.1016/j.advwatres.2018.02.011))
- **C531.** Tidal-basin morphology and bimodal intertidal-flat composition depended strongly on sand-mud interaction, with erosion interaction exerting a larger effect than roughness interaction. *Regime: tide-dominated basins with varying mud erodibility and sand-mud erosion and roughness interaction.* [direct_finding, numerical] (A. Alonso 2023, [doi:10.1029/2023jf007391](https://doi.org/10.1029/2023jf007391))
- **C1527.** Field measurements on an island shelf test sediment-motion thresholds for carbonate-rich natural grains under wave influence. *Regime: Wave‐influenced deposition of carbonate‐rich sediment on the insular shelf of Santa Maria Island, Azores.* [direct_finding, field] (Zhongwei Zhao 2021, [doi:10.1111/sed.12963](https://doi.org/10.1111/sed.12963))
- **C1656.** Under low-to-medium shear, adding fine sand to kaolin suspensions reduces aggregation rate and equilibrium floc size through sand-floc collision breakup; at high shear, shear fragmentation dominates and the sand fraction has little additional effect. *Regime: Kaolin and fine sand-kaolin suspensions under the controlled low, medium and high grid-generated shear conditions..* [direct_finding, mixed] (Alan Cuthbertson 2017, [doi:10.1016/j.coastaleng.2017.11.006](https://doi.org/10.1016/j.coastaleng.2017.11.006))

## Papers

- Baptiste Mengual (2017). Modelling Fine Sediment Dynamics: Towards a Common Erosion Law for Fine Sand, Mud and Mixtures. *Water*. [doi:10.3390/w9080564](https://doi.org/10.3390/w9080564)
- Dake Chen (2021). Critical Shear Stress for Erosion of Sand-Mud Mixtures and Pure Mud. *Frontiers in Marine Science*. [doi:10.3389/fmars.2021.713039](https://doi.org/10.3389/fmars.2021.713039)
- Peng Yao (2022). Erosion Behavior of Sand‐Silt Mixtures: Revisiting the Erosion Threshold. *Water Resources Research*. [doi:10.1029/2021wr031788](https://doi.org/10.1029/2021wr031788)
- Alan Cuthbertson (2017). Model studies for flocculation of sand-clay mixtures. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2017.11.006](https://doi.org/10.1016/j.coastaleng.2017.11.006)
- Víctor Chavarrías (2018). Ill-posedness in modeling mixed sediment river morphodynamics. *Advances in Water Resources*. [doi:10.1016/j.advwatres.2018.02.011](https://doi.org/10.1016/j.advwatres.2018.02.011)
- A. Alonso (2023). Morphodynamic Modeling of Tidal Basins: The Role of Sand‐Mud Interaction. *Journal of Geophysical Research Earth Surface*. [doi:10.1029/2023jf007391](https://doi.org/10.1029/2023jf007391)
- Zhongwei Zhao (2021). Wave‐influenced deposition of carbonate‐rich sediment on the insular shelf of Santa Maria Island, Azores. *Sedimentology*. [doi:10.1111/sed.12963](https://doi.org/10.1111/sed.12963)
- Postacchini (2015). Scour depth under pipelines placed on weakly cohesive soils. *Applied Ocean Research*. [doi:10.1016/j.apor.2015.04.010](https://doi.org/10.1016/j.apor.2015.04.010)
