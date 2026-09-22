# Structural failure and damage

`structures.failure` | Damage progression and failure modes.

Parent: [Coastal structures](structures.md)

Papers: 4. Claims: 3. Equations: 0.

Used by pyCoastal design modules: Seawall design.

## Synthesis

**Well established.** Coastal-structure failure is not a single endpoint: evidence distinguishes hydraulic instability, progressive physical damage, loss of stability or function, and damage to buildings and infrastructure exposed to coastal flooding.

**Governing physics.** Damage depends on the interaction of wave and surge loading, water depth, erosion and morphology, flow concentration around built features, armour or material response, foundation conditions, and the accumulated state of the structure.

**Dimensionless parameters.** Relevant model families commonly organize response through normalized wave loading, relative geometry and water depth, material or armour stability, and normalized damage measures; coefficients and exact forms are intentionally deferred to full-text extraction.

**Major equations.** The accessible evidence supports families of damage and stability models rather than one universal equation. Their use requires preserving each model's damage definition, response variable, structural type, and hydraulic regime.

**Typical methods.** Failure evidence combines historical model review, laboratory or application review, post-event field inspection, UAV mapping, environmental observations, and numerical reconstruction of surge, waves, flooding, and coastal change.

**Numerical models.** Numerical reconstruction can connect regional storm forcing to local flood depth and damage, while damage-model reviews expose how alternate definitions and assumptions affect predicted rubble-mound response.

**Experimental datasets.** This initial branch contains post-Irma field and UAV observations from Saint-Martin and Saint-Barthélemy plus reviewed experimental knowledge for rubble-mound and geosynthetic coastal defenses.

**Validated ranges.** The indexed abstracts document an Irma regime with approximately 4 m surge and 10 m waves, but do not expose sufficient coefficients or ranges to claim general validation limits for the reviewed breakwater and geosynthetic models.

**Recent advances.** Recent work increasingly combines forensic field evidence, remote sensing, high-resolution numerical reconstruction, and explicit review of model assumptions to move from isolated component response toward contextual failure diagnosis.

**Disagreements.** Apparent disagreement among failure models may arise from different definitions of damage, failure modes, variables, and structural systems. Cross-model comparison is unsafe until these semantic and regime differences are aligned.

**Limitations.** This branch is abstract-bounded and has only three extractable sources. It cannot yet quantify full failure envelopes, repeated-loading effects, geotechnical mechanisms, cascading system failure, or repair and recovery.

**Open questions.** Priority gaps are common damage ontologies, progressive and interacting failure modes, prototype-scale validation, coupling with erosion and foundations, probabilistic reliability, and links from physical damage to service loss and recovery.

**Seminal papers.** The rubble-mound historical review is the branch's guide to the development of damage-model concepts; source-level identification and extraction of individual seminal formulations remains a full-text task.

## Claims

- **C418.** After Hurricane Irma in Saint-Martin and Saint-Barthélemy, urban structures and streets channelled flood flow and locally amplified erosion and water levels, while observed damage intensity increased with flood depth. *Regime: Saint-Martin and Saint-Barthélemy during Category 5 Hurricane Irma, with modelled surge near 4 m and waves near 10 m.* [direct_finding, mixed] (Tony Rey 2019, [doi:10.3390/jmse7070215](https://doi.org/10.3390/jmse7070215))
- **C419.** For rubble-mound breakwaters, hydraulic instability is the principal damage mode addressed by historical damage models, whose differing damage definitions and assumptions constrain direct comparison and transfer. *Regime: rubble-mound breakwaters exposed to wave action.* [literature_review_statement, review] (Álvaro Campos 2020, [doi:10.3390/jmse8050317](https://doi.org/10.3390/jmse8050317))
- **C420.** Geosynthetic coastal defenses can be advantageous on weak foundations, but several applications still lack well-founded design formulae and specifications for hydraulic performance, stability, and failure modes. *Regime: geosynthetic coastal structures, including applications on weak foundations.* [literature_review_statement, review] (Brian Oyegbile 2017, [doi:10.1016/j.ijsbe.2017.04.001](https://doi.org/10.1016/j.ijsbe.2017.04.001))

## Papers

- Tony Rey (2019). Coastal Processes and Influence on Damage to Urban Structures during Hurricane Irma (St-Martin & St-Barthélemy, French West Indies). *Journal of Marine Science and Engineering*. [doi:10.3390/jmse7070215](https://doi.org/10.3390/jmse7070215)
- Álvaro Campos (2020). Damage in Rubble Mound Breakwaters. Part I: Historical Review of Damage Models. *Journal of Marine Science and Engineering*. [doi:10.3390/jmse8050317](https://doi.org/10.3390/jmse8050317)
- Brian Oyegbile (2017). Applications of geosynthetic membranes in soil stabilization and coastal defence structures. *International Journal of Sustainable Built Environment*. [doi:10.1016/j.ijsbe.2017.04.001](https://doi.org/10.1016/j.ijsbe.2017.04.001)
- Mohsen Azadbakht (2016). Effect of trapped air on wave forces on coastal bridge superstructures. *Journal of Ocean Engineering and Marine Energy*. [doi:10.1007/s40722-016-0043-9](https://doi.org/10.1007/s40722-016-0043-9)
