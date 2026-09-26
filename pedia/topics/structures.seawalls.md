# Seawalls and revetments

`structures.seawalls` | Shore-parallel armoring.

Parent: [Coastal structures](structures.md)

Papers: 16. Claims: 11. Equations: 0.

Used by pyCoastal design modules: Seawall design.

## Synthesis

**Well established.** Seawalls hold a shoreline or protect a hinterland by reflecting, redirecting, and sometimes overtopping incident waves and surges. Performance includes crest exceedance, structural loading, toe stability, beach response, drainage, and landward consequences.

**Governing physics.** Key processes are breaking and impulsive impact, aeration and turbulence, reflection and standing-wave motion, runup and overtopping, return flow, setup and surge, sediment resuspension and longshore transport, toe scour, and foundation interaction.

**Dimensionless parameters.** Important controls include relative wall and recurve height, freeboard, water depth, wave height and steepness, breaker location, wall setback, reflection coefficient, relative toe geometry, sediment mobility, and normalized force and moment.

**Major equations.** Evidence uses force and overturning-moment reduction relations, RANS-VOF free-surface and turbulence equations, sediment-transport and morphology conservation, breaking and overtopping relations, and reflection and load metrics; no universal seawall equation spans all failure modes.

**Typical methods.** Methods combine wave-flume force and velocimetry tests, large-scale morphology experiments, OpenFOAM and coupled RANS-VOF morphodynamics, acoustic and optical field monitoring, post-event evidence, and historical or state-of-the-art review.

**Numerical models.** OpenFOAM resolves overtopped landward force and moment, while coupled RANS-VOF, bedload, sand-slide, and partial-cell morphology models track the evolving water-soil interface and toe scour.

**Experimental datasets.** The branch includes solid and perforated tsunami-wall tests, 1:5 seawall-versus-woody-debris morphology tests, breaking-solitary-wave velocimetry, 31 days of winter-gale scour observations, and validated vertical-structure morphology cases.

**Validated ranges.** Reported findings include tsunami-force reductions up to 41% for a high nearby wall and about 27% for a half-height wall, gale SSC of 12,222 mg/L and net sediment flux of 769 t/m2/day, and a 1:5 reflection/morphology comparison.

**Recent advances.** Recent work couples image velocimetry, long-duration seabed sensing, free-surface CFD, evolving morphology, physical comparisons with nature-based structures, and climate-adaptation review to examine the full wall-beach-hinterland system.

**Disagreements.** Higher or more elaborate walls do not always yield proportional benefit: a recurve delayed impact but added little load reduction under overtopped flow, and a low wall could increase landward force. Nature-based alternatives range from lower-reflection single logs to stacked forms behaving like walls.

**Limitations.** Evidence is fragmented across tsunami, solitary-wave, storm, morphology, and regional-adaptation regimes. Scale effects, aeration, three-dimensionality, evolving toes, drainage, foundations, ecological response, and compound sea-level and storm change restrict transfer.

**Open questions.** Needs include coupled wall-toe-foundation failure, prototype impulsive pressures and velocities, overtopped hinterland pathways, repeated storm recovery, adaptive crest design, ecological and recreational tradeoffs, and uncertainty-aware lifecycle performance.

**Seminal papers.** A century-scale UK review traces movement from largely vertical wall-and-groyne practice toward curved, stepped, model-informed, environmentally constrained, and nourishment-supported designs; detailed formulation lineage remains a full-text task.

## Claims

- **C435.** A Malaysian review identified increased seawall platform levels and earth bunds as erosion-control measures adaptable to sea-level rise, while several fixed offshore structures become less effective as sea level increases. *Regime: Malaysian shoreline and hold-the-line/adaptation strategies.* [literature_review_statement, review] (Ahmad Hadi Mohamed Rashidi 2021, [doi:10.3390/w13131741](https://doi.org/10.3390/w13131741))
- **C436.** In physical tests, a higher seawall close to a building reduced tsunami force by up to 41%, versus about 27% for a half-height wall, while a perforated wall performed approximately like a solid wall and drained retained water. *Regime: building behind walls of varied type, height, and setback under tsunami-like waves.* [direct_finding, experimental] (Sadia Rahman 2014, [doi:10.1155/2014/729357](https://doi.org/10.1155/2014/729357))
- **C437.** Structural tsunami countermeasures such as seawalls aim to reduce inundation depth and distance, but their effectiveness and damage modes depend on regional conditions and event-specific performance. *Regime: hard tsunami countermeasures including seawalls and offshore breakwaters.* [literature_review_statement, review] (Jan Oetjen 2022, [doi:10.1007/s11069-022-05367-y](https://doi.org/10.1007/s11069-022-05367-y))
- **C438.** Over a century of UK practice, seawall design became more rigorous through physical and numerical modelling, while environmental and recreational constraints reduced the formerly dominant role of hard wall-and-groyne solutions. *Regime: United Kingdom seawalls and groynes since the 1911 Royal Commission.* [literature_review_statement, review] (A. T. Williams 2016, [doi:10.2112/jcoastres-d-15-00213.1](https://doi.org/10.2112/jcoastres-d-15-00213.1))
- **C439.** A coupled RANS-VOF, bedload, and partial-cell morphology model reproduced storm-driven beach change and toe scour in front of a vertical coastal structure across multiple wave, depth, and slope conditions. *Regime: vertical coastal structure across validated waves, depths, and bottom slopes.* [direct_finding, numerical] (Zhong Peng 2017, [doi:10.1016/j.coastaleng.2017.09.006](https://doi.org/10.1016/j.coastaleng.2017.09.006))
- **C440.** During a 31-day seawall field deployment, winter gales raised suspended sediment concentration to 12,222 mg/L and horizontal net sediment flux to 769 t/m2/day, whereas tidal forcing in calm weather caused little suspension. *Regime: severely scoured seabed in front of a seawall during winter.* [direct_finding, field] (Hongan Sun 2022, [doi:10.3389/fmars.2022.1080578](https://doi.org/10.3389/fmars.2022.1080578))
- **C441.** Under simulated overtopped tsunami-like flow, a large recurve delayed impact but reduced inland-structure force little relative to a vertical wall; low walls could amplify load, while greater wall height reduced force linearly and overturning moment exponentially. *Regime: inland structure behind vertical or large-recurve walls of varied height.* [direct_finding, numerical] (S. Harish 2022, [doi:10.3390/w14131986](https://doi.org/10.3390/w14131986))
- **C442.** In 1:5 physical modelling, a single anchored log reduced wave reflection relative to a vertical seawall, while a stacked-log wall behaved nearly identically to the seawall and beach response depended on structure configuration. *Regime: vertical seawall versus single-log and stacked large-woody-debris structures.* [direct_finding, experimental] (Falkenrich 2021, [doi:10.3390/w13152020](https://doi.org/10.3390/w13152020))
- **C443.** Bubble image velocimetry resolved phase-dependent maximum velocity and turbulence for breaking solitary waves impacting and overtopping a vertical seawall, distinguishing high- and low-aeration regimes. *Regime: shoaling solitary waves striking and overtopping a vertical seawall under two aeration regimes.* [direct_finding, experimental] (Wu 2022, [doi:10.3390/w14040583](https://doi.org/10.3390/w14040583))
- **C444.** A state-of-the-art review found limited, dispersed evidence on storm-driven morphological change in front of coastal defenses and its coupling to overtopping, rundown, stability, and failure. *Regime: coastal defense structures and natural barriers during storms.* [literature_review_statement, review] (Frederico Romão 2024, [doi:10.3390/jmse13010040](https://doi.org/10.3390/jmse13010040))
- **C1610.** In 20 seawall cross-section optimization trials, DYCORS coupled to an ANN overtopping model improved both discharge and cost even in the worst trial (17.67% and 12.1% reductions) and outperformed the genetic-algorithm benchmark. *Regime: The paper's composite-slope, berm and wave-wall decision space and ANN overtopping model under the tested wave and water-level combinations..* [direct_finding, numerical] (Yuanyuan Tao 2024, [doi:10.3390/w16162222](https://doi.org/10.3390/w16162222))

## Papers

- Ahmad Hadi Mohamed Rashidi (2021). Coastal Structures as Beach Erosion Control and Sea Level Rise Adaptation in Malaysia: A Review. *Water*. [doi:10.3390/w13131741](https://doi.org/10.3390/w13131741) [published version, CC BY](https://mdpi-res.com/d_attachment/water/water-13-01741/article_deploy/water-13-01741-v2.pdf)
- Sadia Rahman (2014). Experimental Study on Tsunami Risk Reduction on Coastal Building Fronted by Sea Wall. *The Scientific World JOURNAL*. [doi:10.1155/2014/729357](https://doi.org/10.1155/2014/729357) [published version, CC BY](https://downloads.hindawi.com/journals/tswj/2014/729357.pdf)
- Jan Oetjen (2022). A comprehensive review on structural tsunami countermeasures. *Natural Hazards*. [doi:10.1007/s11069-022-05367-y](https://doi.org/10.1007/s11069-022-05367-y) [published version, CC BY](https://link.springer.com/content/pdf/10.1007/s11069-022-05367-y.pdf)
- A. T. Williams (2016). Canons of Coastal Engineering in the United Kingdom: Seawalls/Groynes, a Century of Change?. *Journal of Coastal Research*. [doi:10.2112/jcoastres-d-15-00213.1](https://doi.org/10.2112/jcoastres-d-15-00213.1) [published version, read only](https://bioone.org/journals/Journal-of-Coastal-Research/volume-32/issue-5/JCOASTRES-D-15-00213.1/Canons-of-Coastal-Engineering-in-the-United-Kingdom--Seawalls/10.2112/JCOASTRES-D-15-00213.1.pdf)
- Zhong Peng (2017). A partial cell technique for modeling the morphological change and scour. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2017.09.006](https://doi.org/10.1016/j.coastaleng.2017.09.006) [published version, CC BY](https://www.sciencedirect.com/science/article/am/pii/S037838391630182X?via%3Dihub)
- Hongan Sun (2022). Field observations of seabed scour dynamics in front of a seawall during winter gales. *Frontiers in Marine Science*. [doi:10.3389/fmars.2022.1080578](https://doi.org/10.3389/fmars.2022.1080578) [published version, CC BY](https://www.frontiersin.org/articles/10.3389/fmars.2022.1080578/pdf)
- S. Harish (2022). Tsunami-like Flow-Induced Forces on the Landward Structure behind a Vertical Seawall with and without Recurve Using OpenFOAM. *Water*. [doi:10.3390/w14131986](https://doi.org/10.3390/w14131986) [published version, CC BY](https://www.mdpi.com/2073-4441/14/13/1986/pdf?version=1655951930)
- Falkenrich (2021). Nature-Based Coastal Protection by Large Woody Debris as Compared to Seawalls: A Physical Model Study of Beach Morphology and Wave Reflection. *Water*. [doi:10.3390/w13152020](https://doi.org/10.3390/w13152020) [published version, CC BY](https://www.mdpi.com/2073-4441/13/15/2020/pdf?version=1627373468)
- Wu (2022). Breaking Solitary Wave Impact on a Vertical Seawall. *Water*. [doi:10.3390/w14040583](https://doi.org/10.3390/w14040583) [published version, CC BY](https://www.mdpi.com/2073-4441/14/4/583/pdf?version=1645666237)
- Frederico Romão (2024). A State-of-the-Art Review on Storm Events, Overtopping and Morphological Changes in Front of Coastal Structures. *Journal of Marine Science and Engineering*. [doi:10.3390/jmse13010040](https://doi.org/10.3390/jmse13010040) [published version, CC BY](https://mdpi-res.com/d_attachment/jmse/jmse-13-00040/article_deploy/jmse-13-00040.pdf)
- Yuanyuan Tao (2024). Multi-Objective Optimization of the Seawall Cross-Section by DYCORS Algorithm. *Water*. [doi:10.3390/w16162222](https://doi.org/10.3390/w16162222) [published version, CC BY](https://mdpi-res.com/d_attachment/water/water-16-02222/article_deploy/water-16-02222.pdf)
- Talia Schoonees (2019). Hard Structures for Coastal Protection, Towards Greener Designs. *Estuaries and Coasts*. [doi:10.1007/s12237-019-00551-z](https://doi.org/10.1007/s12237-019-00551-z) [published version, read only](https://link.springer.com/content/pdf/10.1007/s12237-019-00551-z.pdf)
- M. Salauddin (2021). Eco-Engineering of Seawalls—An Opportunity for Enhanced Climate Resilience From Increased Topographic Complexity. *Frontiers in Marine Science*. [doi:10.3389/fmars.2021.674630](https://doi.org/10.3389/fmars.2021.674630) [published version, CC BY](https://www.frontiersin.org/articles/10.3389/fmars.2021.674630/pdf)
- M. A. Habib (2024). Efficient data-driven machine learning models for scour depth predictions at sloping sea defences. *Frontiers in Built Environment*. [doi:10.3389/fbuil.2024.1343398](https://doi.org/10.3389/fbuil.2024.1343398) [published version, CC BY](https://www.frontiersin.org/articles/10.3389/fbuil.2024.1343398/pdf)
- Chris Blenkinsopp (2022). Remote Sensing of Wave Overtopping on Dynamic Coastal Structures. *Remote Sensing*. [doi:10.3390/rs14030513](https://doi.org/10.3390/rs14030513) [published version, CC BY](https://mdpi-res.com/d_attachment/remotesensing/remotesensing-14-00513/article_deploy/remotesensing-14-00513.pdf)
- Damjan Bujak (2025). Overtopping over Vertical Walls with Storm Walls on Steep Foreshores. *Journal of Marine Science and Engineering*. [doi:10.3390/jmse13071285](https://doi.org/10.3390/jmse13071285) [published version, CC BY](https://mdpi-res.com/d_attachment/jmse/jmse-13-01285/article_deploy/jmse-13-01285.pdf)
