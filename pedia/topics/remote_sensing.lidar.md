# LiDAR and photogrammetry

`remote_sensing.lidar` | Elevation and morphology mapping.

Parent: [Remote sensing](remote_sensing.md)

Papers: 11. Claims: 6. Equations: 0.

## Synthesis

**Well established.** Coastal LiDAR provides high-resolution elevation and structure for marsh, dune, defense, and flood applications; quantitative use still requires independent vertical validation and explicit treatment of vegetation, water, and hydraulic connectivity.

**Governing physics.** Return elevation depends on laser interaction with canopy and ground, whereas coastal engineering interpretation depends on whether mapped terrain represents the hydraulic surface, drainage pathways, and morphologic change rather than vegetation or water artifacts.

**Dimensionless parameters.** Classification accuracy, relative volume difference, and compliance fraction are useful dimensionless performance measures, but their meaning is conditional on class balance, change magnitude, reference uncertainty, and the engineering threshold being tested.

**Major equations.** The reviewed slice relies on point-to-reference residuals, MAE and RMSE, classification accuracy, DEM differencing, cross-section integration for sediment volume, and threshold-plus-connectivity inundation logic; it does not establish a universal coastal LiDAR transfer equation.

**Typical methods.** Typical workflows acquire airborne or UAV point clouds, classify ground and vegetation returns, build a DEM or DTM, coregister repeat surveys or auxiliary imagery, validate with RTK or field elevations, and propagate the terrain into habitat, morphology, defense, or inundation analyses.

**Numerical models.** Models range from cover-conditioned decision trees and genetic-algorithm ground estimators to automated levee-axis extraction, connected-cell inundation screening, DEM differencing, and data-driven attribution of morphologic change.

**Experimental datasets.** The reviewed datasets include a nine-class Spartina marsh, paired UAV marsh sensors, 526 RTK dune checkpoints, federal and local Louisiana levees, Staten Island terrain, and eight paired Baltic campaigns producing 16 DEMs and 895 profiles.

**Validated ranges.** Reported validation spans marsh DEM RMSE improvement from 0.15 to 0.10 m, UAV-LiDAR marsh ground RMSE of 5.9 cm, vegetated-dune RMSE of 9.86 cm, and a 0.48% LiDAR-SfM difference in bulk Baltic volume change; these values are site- and workflow-specific.

**Recent advances.** Recent work couples compact UAV LiDAR with field-calibrated learning, direct paired comparison with SfM, and repeat morphodynamic monitoring, shifting LiDAR from episodic mapping toward change detection and method selection by terrain regime.

**Disagreements.** LiDAR clearly outperformed photogrammetry for local ground and vegetation retrieval in dense marsh and dune settings, while paired Baltic surveys differed by only 0.48% in net volume change. This is a scale-and-metric distinction, not a contradiction: bulk change can agree while local errors persist near water and vegetation.

**Limitations.** Limitations include vegetation interception, sparse ground returns, water-surface artifacts, scan geometry, DEM vertical uncertainty, site-trained classifiers, cross-survey coregistration, and failure of elevation-only inundation to represent culverts, barriers, friction, and timing.

**Open questions.** Priorities are transferable vegetation corrections, standardized uncertainty budgets, repeated validation across tidal states and storm magnitudes, automated representation of culverts and defenses, and decision thresholds that compare expected change with the survey error floor.

**Seminal papers.** Within this screened branch, the 2013 salt-marsh study establishes cover-conditioned correction of vegetation-biased LiDAR elevation, and the 2014 levee study demonstrates engineering screening of long, irregular coastal defenses from airborne terrain.

## Claims

- **C156.** Hyperspectral cover-class corrections reduced salt-marsh LiDAR DEM RMSE from 0.15 to 0.10 m while a multisensor decision tree achieved 90% habitat-classification accuracy. *Regime: The studied southeastern US Spartina marsh and its nine cover classes..* [direct_finding, field] (Hladik 2013, [doi:10.1016/j.rse.2013.08.003](https://doi.org/10.1016/j.rse.2013.08.003))
- **C157.** At Little Sapelo marsh, UAV LiDAR ground-elevation RMSE was 5.9 cm versus 17.2 cm for photogrammetry, and vegetation-height RMSE was 17.5 versus 38.1 cm. *Regime: Dense Spartina marsh, 0.40 m output maps, and the tested UAV acquisition/classification workflow..* [direct_finding, field] (Pinton 2021, [doi:10.3390/rs13224506](https://doi.org/10.3390/rs13224506))
- **C161.** Across eight paired Baltic UAV surveys and 895 profiles, LiDAR and SfM net beach-plus-dune volume change differed by only 0.48%, although SfM produced more local artifacts over water and vegetated dunes. *Regime: The 2022-2023 Mrzezyno survey geometry and bulk-change metric; local small changes may not be equivalent..* [direct_finding, field] (Śledziowski 2026, [doi:10.14358/pers.26-00015r2](https://doi.org/10.14358/pers.26-00015r2))
- **C1320.** Bathymetric LiDAR supplies integrated elevation measurements across shallow water and land for coastal-zone assessment, subject to water clarity, depth penetration, classification and ground validation. *Regime: Bringing Bathymetry LiDAR to Coastal Zone Assessment: A Case Study in the Southern Baltic.* [direct_finding, mixed] (Paweł Tysiąc 2020, [doi:10.3390/rs12223740](https://doi.org/10.3390/rs12223740))
- **C1611.** Elevated 2D scanning LiDAR resolved wave-by-wave overtopping on an evolving porous cobble revetment; two reconstruction methods agreed within a factor of two for most events and showed rapid landward discharge decay from infiltration. *Regime: Laboratory dynamic cobble revetments with time-varying crest geometry under the tested waves and material configurations..* [direct_finding, experimental] (Chris Blenkinsopp 2022, [doi:10.3390/rs14030513](https://doi.org/10.3390/rs14030513))
- **C1768.** Structure-from-motion photogrammetry can efficiently recover elevation-dependent mangrove pneumatophore geometry needed by hydrodynamic drag models, matching manual stem count and number-times-mean-diameter while capturing barnacle-encrusted complexity that calipers miss. *Regime: Dense Sonneratia caseolaris pneumatophore canopies, including barnacle-encrusted roots, exposed at low tide on Cù Lao Dung Island in Vietnam's Mekong Delta..* [direct_finding, field] (Jean Liénard 2016, [doi:10.1016/j.ecss.2016.05.011](https://doi.org/10.1016/j.ecss.2016.05.011))

## Papers

- Hladik (2013). Salt marsh elevation and habitat mapping using hyperspectral and LIDAR data. *Remote Sensing of Environment*. [doi:10.1016/j.rse.2013.08.003](https://doi.org/10.1016/j.rse.2013.08.003)
- Pinton (2021). Estimating Ground Elevation and Vegetation Characteristics in Coastal Salt Marshes Using UAV-Based LiDAR and Digital Aerial Photogrammetry. *Remote Sensing*. [doi:10.3390/rs13224506](https://doi.org/10.3390/rs13224506) [published version, CC BY](https://www.mdpi.com/2072-4292/13/22/4506/pdf)
- Paweł Tysiąc (2020). Bringing Bathymetry LiDAR to Coastal Zone Assessment: A Case Study in the Southern Baltic. *Remote Sensing*. [doi:10.3390/rs12223740](https://doi.org/10.3390/rs12223740) [published version, CC BY](https://mdpi-res.com/d_attachment/remotesensing/remotesensing-12-03740/article_deploy/remotesensing-12-03740.pdf)
- Jean Liénard (2016). Efficient three-dimensional reconstruction of aquatic vegetation geometry: Estimating morphological parameters influencing hydrodynamic drag. *Estuarine Coastal and Shelf Science*. [doi:10.1016/j.ecss.2016.05.011](https://doi.org/10.1016/j.ecss.2016.05.011) [published version, read only](https://wpcdn.web.wsu.edu/wp-vancouverlabs/uploads/sites/1204/2017/01/PublishedVegPhotos.pdf)
- Pinton (2022). Estimating Ground Elevation in Coastal Dunes from High-Resolution UAV-LIDAR Point Clouds and Photogrammetry. *Remote Sensing*. [doi:10.3390/rs15010226](https://doi.org/10.3390/rs15010226) [published version, CC BY](https://www.mdpi.com/2072-4292/15/1/226/pdf)
- Palaseanu-Lovejoy (2014). Levee crest elevation profiles derived from airborne lidar-based high resolution digital elevation models in south Louisiana. *ISPRS Journal of Photogrammetry and Remote Sensing*. [doi:10.1016/j.isprsjprs.2014.02.010](https://doi.org/10.1016/j.isprsjprs.2014.02.010)
- Chris Blenkinsopp (2022). Remote Sensing of Wave Overtopping on Dynamic Coastal Structures. *Remote Sensing*. [doi:10.3390/rs14030513](https://doi.org/10.3390/rs14030513) [published version, CC BY](https://mdpi-res.com/d_attachment/remotesensing/remotesensing-14-00513/article_deploy/remotesensing-14-00513.pdf)
- Śledziowski (2026). UAV Lidar vs. Structure-from-Motion (SfM) Photogrammetry for Coastal Dune Monitoring: A Two-Year Multi-Temporal Case Study from the Southern Baltic Sea. *Photogrammetric Engineering &amp; Remote Sensing*. [doi:10.14358/pers.26-00015r2](https://doi.org/10.14358/pers.26-00015r2) [accepted manuscript, read only](https://www.researchgate.net/publication/403382894_UAV_Lidar_vs_Structure-from-Motion_SfM_Photogrammetry_for_Coastal_Dune_Monitoring_A_Two-Year_Multi-Temporal_Case_Study_from_the_Southern_Baltic_Sea)
- A. Pacheco (2014). Retrieval of nearshore bathymetry from Landsat 8 images: A tool for coastal monitoring in shallow waters. *Remote Sensing of Environment*. [doi:10.1016/j.rse.2014.12.004](https://doi.org/10.1016/j.rse.2014.12.004) [published version, read only](https://www.sciencedirect.com/science/article/pii/S0034425714004878)
- Poppenga (2015). Evaluation of Airborne Lidar Elevation Surfaces for Propagation of Coastal Inundation: The Importance of Hydrologic Connectivity. *Remote Sensing*. [doi:10.3390/rs70911695](https://doi.org/10.3390/rs70911695) [published version, CC BY](https://www.mdpi.com/2072-4292/7/9/11695/pdf)
- Mitchell D. Harley (2026). Three-dimensional amplification of storm-driven beach erosion: Implications for setback lines at Narrabeen-Collaroy Beach, Australia. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2026.104976](https://doi.org/10.1016/j.coastaleng.2026.104976) [published version, CC BY](https://api.elsevier.com/content/article/PII:S037838392600030X?httpAccept=text/xml)
