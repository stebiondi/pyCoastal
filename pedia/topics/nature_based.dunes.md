# Dune-based protection

`nature_based.dunes` | Natural and restored dunes.

Parent: [Nature-based coastal protection](nature_based.md)

Papers: 6. Claims: 3. Equations: 0.

## Synthesis

**Well established.** Coastal dunes provide a sacrificial sand reservoir and elevated barrier that can reduce overwash and flooding while supporting habitat; their protective function depends on geometry, sediment supply, vegetation, storm sequence and capacity to recover or be maintained.

**Governing physics.** Wind transports dry beach sand into dunes where vegetation traps it; waves and surge erode the seaward face, trigger scarping, slumping and overwash, and redistribute sediment offshore or landward. Barrier performance changes sharply when runup exceeds crest or volume is depleted.

**Dimensionless parameters.** Controls include crest freeboard relative to runup, dune volume normalized by storm erosion demand, beach width relative to runup, sediment fall velocity and grain size, vegetation density or frontal area, overwash ratio, recovery-to-storm timescale and vertical error relative to detected change.

**Major equations.** Design and assessment combine sediment-volume continuity, aeolian transport relations, wave runup and overtopping formulas, erosion or storm-impact models and probabilistic exceedance. Monitoring derives elevation and volume change from co-registered point clouds and propagates surface-classification error.

**Typical methods.** Workflows survey beach-dune topography before and after storms, classify bare ground beneath vegetation, validate with RTK checkpoints, calculate profiles and volumes, document planting/fencing/nourishment and access paths, couple wave-level scenarios to erosion and overtopping and monitor recovery and habitat outcomes.

**Numerical models.** Reviewed methods include a genetic-algorithm ground classifier for vegetated dune LiDAR and paired LiDAR–SfM change analysis. Direct storm-erosion, runup, overwash and nature-based protection modeling remains in the lawful-full-text queue.

**Experimental datasets.** Reviewed evidence includes Topsail Hill UAV LiDAR and photogrammetry checked against 526 RTK points and eight paired Baltic UAV surveys covering 895 profiles over two years. These datasets validate monitoring, not protective-load reduction.

**Validated ranges.** Topsail ground elevation achieved 7.64 cm MAE and 9.86 cm RMSE, while Baltic net beach-plus-dune volume change differed by 0.48% between methods. These site-specific monitoring results do not validate dune performance under design storms.

**Recent advances.** Recent advances use UAV LiDAR and SfM, satellite topography, automated vegetation-aware classification, storm-by-storm digital twins, coupled aeolian–marine morphodynamics, nature-based benefit accounting and adaptive monitoring tied to intervention thresholds.

**Disagreements.** Hard, fixed design elevations conflict with dunes as mobile landforms, while unmanaged mobility can threaten assets. LiDAR better penetrates vegetation but costs more; SfM can recover aggregate volume yet produce local artifacts that matter for crest and weak-point assessment.

**Limitations.** Current reviewed evidence lacks direct wave attenuation, erosion demand, overwash, breach probability, recovery and ecological performance. Vegetation occlusion, wet sand and water artifacts, co-registration error, sparse checkpoints and short monitoring periods constrain detected change.

**Open questions.** Priorities include linking measured geometry to probabilistic failure, full-scale storm validation, vegetation species and planting design, recovery under storm clusters, sediment-source sustainability, access weak points, habitat tradeoffs and adaptive nourishment triggers.

**Seminal papers.** Coastal dune erosion and runup-impact regimes established geometry-based storm response; aeolian transport and vegetation-trapping studies explained growth, while profile-volume monitoring and probabilistic fragility reframed dunes as dynamic defenses.

## Claims

- **C158.** At Topsail Hill, UAV LiDAR combined with a genetic algorithm estimated dune ground elevation with 7.64 cm MAE and 9.86 cm RMSE against 526 RTK checkpoints. *Regime: The vegetated Florida dune, tested UAV sensor, and trained regression setup..* [direct_finding, field] (Pinton 2022, [doi:10.3390/rs15010226](https://doi.org/10.3390/rs15010226))
- **C1472.** Field evidence links spatial organization of dominant dune grass and sand-flux feedbacks to foredune development and natural flood-barrier function. *Regime: Biomorphogenic Feedbacks and the Spatial Organization of a Dominant Grass Steer Dune Development.* [direct_finding, field] (Dries Bonte 2021, [doi:10.3389/fevo.2021.761336](https://doi.org/10.3389/fevo.2021.761336))
- **C1605.** Barrier-dune resistance to storm-tide flooding depends on dune-beach type, sediment reserve and erosional response rather than crest elevation alone. *Regime: PROTECTION OF SANDY COASTS IN DEPENDENCE OF THE DUNE - BEACH - TYPE.* [literature_review_statement, review] (Erchinger 1974, [doi:10.9753/icce.v14.68](https://doi.org/10.9753/icce.v14.68))

## Papers

- Dries Bonte (2021). Biomorphogenic Feedbacks and the Spatial Organization of a Dominant Grass Steer Dune Development. *Frontiers in Ecology and Evolution*. [doi:10.3389/fevo.2021.761336](https://doi.org/10.3389/fevo.2021.761336) [published version, CC BY](https://www.frontiersin.org/articles/10.3389/fevo.2021.761336/pdf)
- Erchinger (1974). PROTECTION OF SANDY COASTS IN DEPENDENCE OF THE DUNE - BEACH - TYPE. *Coastal Engineering Proceedings*. [doi:10.9753/icce.v14.68](https://doi.org/10.9753/icce.v14.68) [published version, CC BY](https://journals.tdl.org/icce/index.php/icce/article/download/2963/2628)
- Derek Jackson (2011). Investigation of three‐dimensional wind flow behaviour over coastal dune morphology under offshore winds using computational fluid dynamics (CFD) and ultrasonic anemometry. *Earth Surface Processes and Landforms*. [doi:10.1002/esp.2139](https://doi.org/10.1002/esp.2139) [submitted manuscript, CC BY-NC-ND](https://research.edgehill.ac.uk/ws/files/20180738/Jackson_etal_2011_ESPL_3DwindFlow.pdf)
- Dustin Whalen (2022). Mechanisms, volumetric assessment, and prognosis for rapid coastal erosion of Tuktoyaktuk Island, an important natural barrier for the harbour and community. *Canadian Journal of Earth Sciences*. [doi:10.1139/cjes-2021-0101](https://doi.org/10.1139/cjes-2021-0101) [published version, CC BY](https://doi.org/10.1139/cjes-2021-0101)
- Pinton (2022). Estimating Ground Elevation in Coastal Dunes from High-Resolution UAV-LIDAR Point Clouds and Photogrammetry. *Remote Sensing*. [doi:10.3390/rs15010226](https://doi.org/10.3390/rs15010226) [published version, CC BY](https://www.mdpi.com/2072-4292/15/1/226/pdf)
- Śledziowski (2026). UAV Lidar vs. Structure-from-Motion (SfM) Photogrammetry for Coastal Dune Monitoring: A Two-Year Multi-Temporal Case Study from the Southern Baltic Sea. *Photogrammetric Engineering &amp; Remote Sensing*. [doi:10.14358/pers.26-00015r2](https://doi.org/10.14358/pers.26-00015r2) [accepted manuscript, read only](https://www.researchgate.net/publication/403382894_UAV_Lidar_vs_Structure-from-Motion_SfM_Photogrammetry_for_Coastal_Dune_Monitoring_A_Two-Year_Multi-Temporal_Case_Study_from_the_Southern_Baltic_Sea)
