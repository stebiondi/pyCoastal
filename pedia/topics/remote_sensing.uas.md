# Uncrewed aerial systems

`remote_sensing.uas` | Drone-based coastal observations.

Parent: [Remote sensing](remote_sensing.md)

Papers: 18. Claims: 15. Equations: 2.

## Synthesis

**Well established.** Coastal UAS provide operator-timed centimetre-scale observations between ground surveys and crewed or satellite platforms, but accuracy depends on sensor physics, control and georeferencing, surface texture, vegetation, water, tide, weather, processing, validation, and the spatial scale of the reported metric.

**Governing physics.** Passive SfM requires stable visible texture and is degraded by moving or reflective water and canopy occlusion; LiDAR samples range and may penetrate canopy but still needs ground classification; multispectral and hyperspectral products depend on illumination, spectral contrast, water-column attenuation, turbidity, depth, and mixed pixels.

**Dimensionless parameters.** Important nondimensional quantities include spectral indices, normalized reflectance and band ratios, spectral angle, classification agreement such as kappa, relative vertical error, overlap and geometry quality measures, and habitat or vegetation fractions; dimensional pixel size alone is not an accuracy guarantee.

**Major equations.** Representative formulations include SfM bundle adjustment and surface differencing, NDVI and its calibrated biomass regression AGB=2428.2 NDVI+120.1, spectral-angle similarity, Random-Forest or ANN classification, allometric biomass regressions, and error metrics such as RMSE and Cohen kappa.

**Typical methods.** Workflows combine flight and tide planning, RTK/PPK or ground control, camera or LiDAR calibration, overlapping imagery and SfM, point-cloud filtering, orthomosaic or DEM creation, repeat differencing, spectral indices or supervised classification, and independent checkpoints, field plots, profiles, or underwater video.

**Numerical models.** Models range from photogrammetric reconstruction and DEM differencing to NDVI regression, vegetation allometry, spectral-angle mapping, Random Forest habitat classification, and ANN LiDAR filtering. Each model requires calibration and validation matched to the target variable and environment.

**Experimental datasets.** The branch includes seasonal biomass and multispectral imagery at Carpinteria, paired LiDAR-photogrammetry marsh observations at Little Sapelo, eight paired dune surveys and 895 profiles in the Baltic, nine morphology surveys of a New Jersey groin field, multiline LiDAR in dense marsh, and paired aerial-surface hyperspectral habitat maps.

**Validated ranges.** Reported tests span 1-10 cm imagery in the foundational review; 5.9 versus 17.2 cm marsh-ground RMSE for LiDAR and photogrammetry; 0.48% difference in integrated Baltic volume change across eight surveys and 895 profiles; 1-10 cm hyperspectral pixels over 230-20,200 m2; and 0.04 m UAV through 10-20 m satellite imagery with mean kappa 0.71-0.77.

**Recent advances.** Recent advances move beyond RGB surface reconstruction toward spatial-spectral ANN ground filtering, multi-temporal sensor intercomparison, UAV-derived vegetation allometry, multiscale hyperspectral habitat mapping, and target-specific comparisons spanning drone, airplane, surface vehicle, and satellite observations.

**Disagreements.** LiDAR's superior local marsh elevation accuracy and SfM's close agreement in integrated dune-volume change are not contradictory: point elevation, profile artifacts, and spatially integrated volume are different metrics over different surfaces. Likewise, UAV's finer pixels did not universally outperform airplane or satellite habitat mapping because target separability and water effects controlled skill.

**Limitations.** Small footprints, battery and weather limits, flight regulation, tide and sun-glint timing, ground-control distribution, moving water, dense or flexible vegetation, turbidity, processing choices, scarce reference data, and site-specific calibration limit repeatability and transfer. Newer 2026 evidence also remains lightly replicated.

**Open questions.** Priorities are standardized uncertainty budgets, synchronized multi-sensor benchmarks, cross-site classifier and allometry transfer, water-column correction, canopy and ground separation, automated quality flags, defensible change-detection thresholds, and scalable fusion with satellite and in-situ observations.

**Seminal papers.** Within this screened branch, the 2015 overview framed the platform and sensor opportunity, while the 2021 Little Sapelo comparison established quantitative LiDAR-versus-photogrammetry accuracy for vegetated coastal terrain.

## Equations

### NDVI aboveground-biomass regression

$$
AGB=2428.2\,NDVI+120.1
$$

Regime: Carpinteria Salt Marsh vegetation and study sensor/calibration seasons.

Variables: `AGB` salt-marsh aboveground biomass in g m-2; `NDVI` normalized difference vegetation index

Source: (Doughty 2019, [doi:10.3390/rs11050540](https://doi.org/10.3390/rs11050540))

### Spectral angle

$$
\theta=\cos^{-1}\left(\frac{\mathbf{t}\cdot\mathbf{r}}{\lVert\mathbf{t}\rVert\lVert\mathbf{r}\rVert}\right)
$$

Regime: Hyperspectral classification with selected SAM thresholds.

Variables: `theta` spectral angle; `t` target spectrum; `r` reference spectrum

Source: (Nevstad 2026, [doi:10.3390/rs18142361](https://doi.org/10.3390/rs18142361))

## Claims

- **C196.** Coastal UAVs offer operator-controlled revisit timing and sub-10-cm imagery with diverse sensors, but payload, endurance, weather, regulation, and ground control constrain performance. *Regime: beaches; wetlands; nearshore waters.* [literature_review_statement, review] (Klemas 2015, [doi:10.2112/jcoastres-d-15-00005.1](https://doi.org/10.2112/jcoastres-d-15-00005.1))
- **C197.** At Carpinteria Salt Marsh, seasonal NDVI biomass calibration outperformed pooled calibration, with spring r2=0.67 and RMSE=344 g m-2 versus pooled r2=0.36 and RMSE=496 g m-2. *Regime: California salt marsh.* [direct_finding, field] (Doughty 2019, [doi:10.3390/rs11050540](https://doi.org/10.3390/rs11050540))
- **C198.** Spatial-spectral ANN filtering of drone LiDAR improved salt-marsh ground-point discrimination needed for terrain reconstruction under dense vegetation. *Regime: vegetated coastal salt marsh.* [direct_finding, field] (Liu 2024, [doi:10.3390/rs16183373](https://doi.org/10.3390/rs16183373))
- **C199.** UAV-derived vegetation structure can support nondestructive aboveground-biomass allometry for temperate mangroves, subject to canopy penetration and calibration-population limits. *Regime: temperate mangrove forest.* [direct_finding, field] (Reef 2024, [doi:10.2112/jcoastres-d-23-00062.1](https://doi.org/10.2112/jcoastres-d-23-00062.1))
- **C200.** UAV hyperspectral imaging mapped 20,200 m2 at 10 cm resolution while a surface vehicle mapped 230 m2 at 1 cm, demonstrating a coverage-resolution tradeoff. *Regime: shallow seagrass and macroalgae habitat.* [direct_finding, mixed] (Nevstad 2026, [doi:10.3390/rs18142361](https://doi.org/10.3390/rs18142361))
- **C201.** In a Baltic lagoon, mean Random-Forest kappa was 0.71-0.77 across UAV, airplane, and satellite imagery, but target-specific skill ranged from 0.99 for UAV vegetation presence to 0.29-0.57 for free water column. *Regime: Baltic coastal lagoon.* [direct_finding, field] (Herkül 2024, [doi:10.2112/jcr-si113-102.1](https://doi.org/10.2112/jcr-si113-102.1))
- **C1307.** UAV structure-from-motion photogrammetry can reconstruct high-resolution coastal topography from overlapping imagery, providing flexible terrain products where survey design, control and surface texture support reliable matching. *Regime: Using Unmanned Aerial Vehicles (UAV) for High-Resolution Reconstruction of Topography: The Structure from Motion Approach on Coastal Environments.* [direct_finding, mixed] (Francesco Mancini 2013, [doi:10.3390/rs5126880](https://doi.org/10.3390/rs5126880))
- **C1315.** UAV photogrammetry combined with ground surveys enables rapid, repeatable mapping of shoreline and beach change at local scale when control, image overlap and survey comparison are managed. *Regime: UAV Photogrammetry and Ground Surveys as a Mapping Tool for Quickly Monitoring Shoreline and Beach Changes.* [direct_finding, mixed] (Antonio Zanutta 2020, [doi:10.3390/jmse8010052](https://doi.org/10.3390/jmse8010052))
- **C1318.** Repeated UAV photogrammetry over the Sopot tombolo produces high-resolution coastal-zone change measurements suitable for resolving rapid local morphological evolution. *Regime: Using UAV Photogrammetry to Analyse Changes in the Coastal Zone Based on the Sopot Tombolo (Salient) Measurement Project.* [direct_finding, mixed] (Paweł Burdziakowski 2020, [doi:10.3390/s20144000](https://doi.org/10.3390/s20144000))
- **C1322.** Comparing UAV photogrammetry and airborne laser scanning supports shallow-water depth estimation and shoreline extraction while quantifying method-specific spatial coverage and accuracy. *Regime: Spatial Analysis of Bathymetric Data from UAV Photogrammetry and ALS LiDAR: Shallow-Water Depth Estimation and Shoreline Extraction.* [direct_finding, mixed] (Specht 2025, [doi:10.3390/rs17173115](https://doi.org/10.3390/rs17173115))
- **C1509.** Repeated UAV photogrammetry maps joints, megaclasts, and deformation associated with slow-moving coastal landslides in Malta. *Regime: Advantages of Using UAV Digital Photogrammetry in the Study of Slow-Moving Coastal Landslides.* [direct_finding, field] (Stefano Devoto 2020, [doi:10.3390/rs12213566](https://doi.org/10.3390/rs12213566))
- **C1510.** Drone trials relate flight altitude and image resolution to detection and classification of litter on beaches, dunes, banks, and coastal waters. *Regime: Drones for litter monitoring on coasts and rivers: suitable flight altitude and image resolution.* [direct_finding, field] (Umberto Andriolo 2023, [doi:10.1016/j.marpolbul.2023.115521](https://doi.org/10.1016/j.marpolbul.2023.115521))
- **C1512.** A Spanish Mediterranean case study demonstrates repeatable UAV monitoring for coastal morphology and management at Almenara–Sagunto. *Regime: Coastal Monitoring Using Unmanned Aerial Vehicles (UAVs) for the Management of the Spanish Mediterranean Coast: The Case of Almenara-Sagunto.* [direct_finding, field] (Vicent Esteban Chapapría 2022, [doi:10.3390/ijerph19095457](https://doi.org/10.3390/ijerph19095457))
- **C1513.** A portable-UAV planning framework specifies survey design for high-resolution, repeatable observation of coastal hydro-environments. *Regime: A Framework for Survey Planning Using Portable Unmanned Aerial Vehicles (pUAVs) in Coastal Hydro-Environment.* [direct_finding, mixed] (Ha Linh Trinh 2022, [doi:10.3390/rs14092283](https://doi.org/10.3390/rs14092283))
- **C1600.** A coastal UAS survey protocol identifies flight planning, ground control, illumination, wind, platform, sensor and processing controls needed for repeatable high-resolution coastal products. *Regime: A Protocol for Aerial Survey in Coastal Areas Using UAS.* [literature_review_statement, review] (Doukari 2019, [doi:10.3390/rs11161913](https://doi.org/10.3390/rs11161913))

## Papers

- Francesco Mancini (2013). Using Unmanned Aerial Vehicles (UAV) for High-Resolution Reconstruction of Topography: The Structure from Motion Approach on Coastal Environments. *Remote Sensing*. [doi:10.3390/rs5126880](https://doi.org/10.3390/rs5126880) [published version, CC BY](https://mdpi-res.com/d_attachment/remotesensing/remotesensing-05-06880/article_deploy/remotesensing-05-06880.pdf)
- Klemas (2015). Coastal and Environmental Remote Sensing from Unmanned Aerial Vehicles: An Overview. *Journal of Coastal Research*. [doi:10.2112/jcoastres-d-15-00005.1](https://doi.org/10.2112/jcoastres-d-15-00005.1) [published version, read only](https://bioone.org/journals/journal-of-coastal-research/volume-31/issue-5/JCOASTRES-D-15-00005.1/Coastal-and-Environmental-Remote-Sensing-from-Unmanned-Aerial-Vehicles/10.2112/JCOASTRES-D-15-00005.1.pdf)
- Doughty (2019). Mapping Coastal Wetland Biomass from High Resolution Unmanned Aerial Vehicle (UAV) Imagery. *Remote Sensing*. [doi:10.3390/rs11050540](https://doi.org/10.3390/rs11050540) [published version, CC BY](https://mdpi-res.com/d_attachment/remotesensing/remotesensing-11-00540/article_deploy/remotesensing-11-00540.pdf)
- Stefano Devoto (2020). Advantages of Using UAV Digital Photogrammetry in the Study of Slow-Moving Coastal Landslides. *Remote Sensing*. [doi:10.3390/rs12213566](https://doi.org/10.3390/rs12213566) [published version, CC BY](https://www.mdpi.com/2072-4292/12/21/3566/pdf?version=1604233704)
- Antonio Zanutta (2020). UAV Photogrammetry and Ground Surveys as a Mapping Tool for Quickly Monitoring Shoreline and Beach Changes. *Journal of Marine Science and Engineering*. [doi:10.3390/jmse8010052](https://doi.org/10.3390/jmse8010052) [published version, CC BY](https://mdpi-res.com/d_attachment/jmse/jmse-08-00052/article_deploy/jmse-08-00052.pdf)
- Umberto Andriolo (2023). Drones for litter monitoring on coasts and rivers: suitable flight altitude and image resolution. *Marine Pollution Bulletin*. [doi:10.1016/j.marpolbul.2023.115521](https://doi.org/10.1016/j.marpolbul.2023.115521) [published version, CC BY-NC-ND](https://ktisis.cut.ac.cy/bitstream/20.500.14279/30665/1/Papakonstantinou%2C%20Apostolos%201.pdf)
- Doukari (2019). A Protocol for Aerial Survey in Coastal Areas Using UAS. *Remote Sensing*. [doi:10.3390/rs11161913](https://doi.org/10.3390/rs11161913) [published version, CC BY](https://www.mdpi.com/2072-4292/11/16/1913/pdf)
- Paweł Burdziakowski (2020). Using UAV Photogrammetry to Analyse Changes in the Coastal Zone Based on the Sopot Tombolo (Salient) Measurement Project. *Sensors*. [doi:10.3390/s20144000](https://doi.org/10.3390/s20144000) [published version, CC BY](https://mdpi-res.com/d_attachment/sensors/sensors-20-04000/article_deploy/sensors-20-04000.pdf)
- Vicent Esteban Chapapría (2022). Coastal Monitoring Using Unmanned Aerial Vehicles (UAVs) for the Management of the Spanish Mediterranean Coast: The Case of Almenara-Sagunto. *International Journal of Environmental Research and Public Health*. [doi:10.3390/ijerph19095457](https://doi.org/10.3390/ijerph19095457) [published version, CC BY](https://www.mdpi.com/1660-4601/19/9/5457/pdf?version=1651713153)
- Ha Linh Trinh (2022). A Framework for Survey Planning Using Portable Unmanned Aerial Vehicles (pUAVs) in Coastal Hydro-Environment. *Remote Sensing*. [doi:10.3390/rs14092283](https://doi.org/10.3390/rs14092283) [published version, CC BY](https://www.mdpi.com/2072-4292/14/9/2283/pdf?version=1652237384)
- Liu (2024). ANN-Based Filtering of Drone LiDAR in Coastal Salt Marshes Using Spatial–Spectral Features. *Remote Sensing*. [doi:10.3390/rs16183373](https://doi.org/10.3390/rs16183373) [published version, CC BY](https://www.mdpi.com/2072-4292/16/18/3373/pdf)
- Specht (2025). Spatial Analysis of Bathymetric Data from UAV Photogrammetry and ALS LiDAR: Shallow-Water Depth Estimation and Shoreline Extraction. *Remote Sensing*. [doi:10.3390/rs17173115](https://doi.org/10.3390/rs17173115) [published version, CC BY](https://mdpi-res.com/d_attachment/remotesensing/remotesensing-17-03115/article_deploy/remotesensing-17-03115.pdf)
- Reef (2024). Allometric Equations for Aboveground Biomass Estimation of Temperate Mangroves Using Uncrewed Aerial Vehicles. *Journal of Coastal Research*. [doi:10.2112/jcoastres-d-23-00062.1](https://doi.org/10.2112/jcoastres-d-23-00062.1)
- Nevstad (2026). Hyperspectral Imaging of Seagrass and Macroalgae Using Uncrewed Aerial and Surface Vehicles for Coastal Habitat Mapping. *Remote Sensing*. [doi:10.3390/rs18142361](https://doi.org/10.3390/rs18142361) [published version, CC BY](https://mdpi-res.com/d_attachment/remotesensing/remotesensing-18-02361/article_deploy/remotesensing-18-02361.pdf)
- Herkül (2024). Mapping Shallow Water Coastal Habitats Using Optical Remote Sensing and Machine Learning: Evaluating Drone, Airplane, and Satellite-Based Imagery. *Journal of Coastal Research*. [doi:10.2112/jcr-si113-102.1](https://doi.org/10.2112/jcr-si113-102.1)
- Pinton (2021). Estimating Ground Elevation and Vegetation Characteristics in Coastal Salt Marshes Using UAV-Based LiDAR and Digital Aerial Photogrammetry. *Remote Sensing*. [doi:10.3390/rs13224506](https://doi.org/10.3390/rs13224506) [published version, CC BY](https://www.mdpi.com/2072-4292/13/22/4506/pdf)
- Zimmerman (2021). UAS-SfM approach to evaluate the performance of notched groins within a groin field and their impact on the morphological evolution of a beach nourishment. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2021.103997](https://doi.org/10.1016/j.coastaleng.2021.103997)
- Śledziowski (2026). UAV Lidar vs. Structure-from-Motion (SfM) Photogrammetry for Coastal Dune Monitoring: A Two-Year Multi-Temporal Case Study from the Southern Baltic Sea. *Photogrammetric Engineering &amp; Remote Sensing*. [doi:10.14358/pers.26-00015r2](https://doi.org/10.14358/pers.26-00015r2) [accepted manuscript, read only](https://www.researchgate.net/publication/403382894_UAV_Lidar_vs_Structure-from-Motion_SfM_Photogrammetry_for_Coastal_Dune_Monitoring_A_Two-Year_Multi-Temporal_Case_Study_from_the_Southern_Baltic_Sea)
