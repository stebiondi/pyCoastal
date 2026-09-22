# Remote sensing

`remote_sensing` | Coastal observation using non-contact sensors.

Subtopics: [LiDAR and photogrammetry](remote_sensing.lidar.md), [Satellite remote sensing](remote_sensing.satellite.md), [Uncrewed aerial systems](remote_sensing.uas.md), [Coastal video monitoring](remote_sensing.video.md)

Papers: 22. Claims: 4. Equations: 0.

## Synthesis

**Well established.** Coastal remote sensing derives shoreline, elevation, bathymetry, waves and land-cover change from optical, radar, laser and photogrammetric measurements. Every product represents a defined physical or image proxy whose resolution, datum, acquisition conditions and uncertainty must be explicit.

**Governing physics.** Optical reflectance depends on illumination, atmosphere, water constituents and bottom signal; radar backscatter responds to roughness, moisture and geometry; LiDAR travel time and refraction yield elevation or depth; photogrammetry reconstructs geometry from parallax and control.

**Dimensionless parameters.** Key descriptors include pixel or point spacing relative to feature scale, signal-to-noise and contrast, overlap and baseline ratios, incidence angle, depth-to-attenuation scale, tide range-to-beach slope effect, classification accuracy and normalized positional error.

**Major equations.** Retrievals use sensor geometry, radiometric correction, refraction and travel-time relations, structure-from-motion bundle adjustment, spectral indices, classifiers and edge detection. Change rates regress proxy positions through time with positional and temporal uncertainty.

**Typical methods.** Workflows calibrate and georeference imagery, correct atmosphere and water level, segment land and water, build orthomosaics or point clouds, classify returns, validate against surveys, propagate error and analyze repeated acquisitions or fused sensors.

**Numerical models.** Processing uses threshold and index methods, supervised or unsupervised classification, machine learning, structure from motion, stereo reconstruction, LiDAR classification, bathymetric inversion, SAR speckle reduction and multitemporal change models.

**Experimental datasets.** Evidence spans forty years at Narrabeen–Collaroy, microtidal Landsat and Sentinel beaches, UAV beach and tombolo surveys, Langue de Barbarie and Bangladesh shoreline archives, Baltic bathymetric LiDAR and coastal topography–bathymetry demonstrations.

**Validated ranges.** The reviewed corpus spans centimeter-to-decimeter UAV products, meter-scale airborne or spaceborne elevation and 10–30 m multispectral archives, with instantaneous to four-decade coverage. Valid ranges remain sensor-, water-clarity- and proxy-specific.

**Recent advances.** Recent advances integrate UAV structure from motion, satellite-derived topography–bathymetry, cloud-scale processing, SAR–optical complementarity, machine learning and dense multitemporal archives to observe the coast as a connected continuum.

**Disagreements.** A shoreline is not unique: wet–dry, vegetation, waterline and datum-based proxies differ systematically. Automated methods improve repeatability but can mask tide, runup, turbidity and geolocation error; higher spatial resolution often trades against coverage and revisit.

**Limitations.** Clouds, haze, sun glint, turbidity, waves, refraction, limited LiDAR penetration, SAR speckle, vegetation, weak texture, ground-control error, sensor changes and sparse validation constrain accuracy and long-term consistency.

**Open questions.** Priorities include analysis-ready multi-sensor archives, robust uncertainty across proxies, turbid-water bathymetry, global validation, near-real-time hazards, automated quality control, physics-aware ML and equitable access to repeat coastal surveys.

**Seminal papers.** Aerial photogrammetry and shoreline mapping established repeat coastal surveys; Landsat enabled global multidecadal archives, while airborne LiDAR, SAR and video expanded elevation, all-weather and high-frequency observation.

## Claims

- **C147.** Coastal-current monitoring platforms are complementary: HF radar can map surface currents to roughly 200 km offshore, while satellites and drifters extend coverage but impose revisit, cloud, or tracking limitations. *Regime: Surface-current observation and the sensor technologies available through 2012..* [literature_review_statement, review] (Anon. 2012, [doi:10.2112/jcoastres-d-11-00197.1](https://doi.org/10.2112/jcoastres-d-11-00197.1))
- **C1306.** Shoreline mapping requires an explicit physical shoreline definition and sensor-appropriate proxy because extracted position varies with tide, wave conditions, morphology, image characteristics and interpretation method. *Regime: Shoreline Definition and Detection: A Review.* [literature_review_statement, review] (Elizabeth H. Boak 2005, [doi:10.2112/03-0071.1](https://doi.org/10.2112/03-0071.1))
- **C1321.** Coastal remote sensing combines satellite, airborne and in-situ non-contact observations to monitor shoreline, water, habitat and hazards across scales, with sensor fusion and validation central to operational use. *Regime: Remote Sensing Applications in Coastal Areas.* [literature_review_statement, review] (Lacava 2020, [doi:10.3390/s20092673](https://doi.org/10.3390/s20092673))
- **C1745.** Field hyperspectra can discriminate many salt-marsh vegetation types because pigment absorption and especially canopy-structure effects create distinct spectral signatures; continuum removal improves visible-band separability but reduces near- and shortwave-infrared separability. *Regime: Field reflectance spectra from 27 salt-marsh vegetation types on the Dutch Wadden Sea coast, measured from 400 to 2500 nm during the growing season..* [direct_finding, field] (K.S. Schmidt 2003, [doi:10.1016/s0034-4257(02)00196-7](https://doi.org/10.1016/s0034-4257(02)00196-7))

## Papers

- Elizabeth H. Boak (2005). Shoreline Definition and Detection: A Review. *Journal of Coastal Research*. [doi:10.2112/03-0071.1](https://doi.org/10.2112/03-0071.1)
- K.S. Schmidt (2003). Spectral discrimination of vegetation types in a coastal wetland. *Remote Sensing of Environment*. [doi:10.1016/s0034-4257(02)00196-7](https://doi.org/10.1016/s0034-4257(02)00196-7)
- Anon. (2012). Remote Sensing of Coastal and Ocean Currents: An Overview. *Journal of Coastal Research*. [doi:10.2112/jcoastres-d-11-00197.1](https://doi.org/10.2112/jcoastres-d-11-00197.1)
- Lacava (2020). Remote Sensing Applications in Coastal Areas. *Sensors*. [doi:10.3390/s20092673](https://doi.org/10.3390/s20092673)
- Francesco Mancini (2013). Using Unmanned Aerial Vehicles (UAV) for High-Resolution Reconstruction of Topography: The Structure from Motion Approach on Coastal Environments. *Remote Sensing*. [doi:10.3390/rs5126880](https://doi.org/10.3390/rs5126880)
- Hugues Lantuit (2011). The Arctic Coastal Dynamics Database: A New Classification Scheme and Statistics on Arctic Permafrost Coastlines. *Estuaries and Coasts*. [doi:10.1007/s12237-010-9362-6](https://doi.org/10.1007/s12237-010-9362-6)
- Seynabou Toure (2019). Shoreline Detection using Optical Remote Sensing: A Review. *ISPRS International Journal of Geo-Information*. [doi:10.3390/ijgi8020075](https://doi.org/10.3390/ijgi8020075)
- Josep E. Pardo‐Pascual (2018). Assessing the Accuracy of Automatically Extracted Shorelines on Microtidal Beaches from Landsat 7, Landsat 8 and Sentinel-2 Imagery. *Remote Sensing*. [doi:10.3390/rs10020326](https://doi.org/10.3390/rs10020326)
- Edward Salameh (2019). Monitoring Beach Topography and Nearshore Bathymetry Using Spaceborne Remote Sensing: A Review. *Remote Sensing*. [doi:10.3390/rs11192212](https://doi.org/10.3390/rs11192212)
- Emma McAllister (2022). Multispectral satellite imagery and machine learning for the extraction of shoreline indicators. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2022.104102](https://doi.org/10.1016/j.coastaleng.2022.104102)
- Ian L. Turner (2021). Satellite optical imagery in Coastal Engineering. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2021.103919](https://doi.org/10.1016/j.coastaleng.2021.103919)
- Splinter (2018). Remote Sensing Is Changing Our View of the Coast: Insights from 40 Years of Monitoring at Narrabeen-Collaroy, Australia. *Remote Sensing*. [doi:10.3390/rs10111744](https://doi.org/10.3390/rs10111744)
- Erwin W. J. Bergsma (2021). Coastal morphology from space: A showcase of monitoring the topography-bathymetry continuum. *Remote Sensing of Environment*. [doi:10.1016/j.rse.2021.112469](https://doi.org/10.1016/j.rse.2021.112469)
- Weiwei Sun (2023). Coastline extraction using remote sensing: a review. *GIScience & Remote Sensing*. [doi:10.1080/15481603.2023.2243671](https://doi.org/10.1080/15481603.2023.2243671)
- Antonio Zanutta (2020). UAV Photogrammetry and Ground Surveys as a Mapping Tool for Quickly Monitoring Shoreline and Beach Changes. *Journal of Marine Science and Engineering*. [doi:10.3390/jmse8010052](https://doi.org/10.3390/jmse8010052)
- Adélaïde Taveneau (2021). Observing and Predicting Coastal Erosion at the Langue de Barbarie Sand Spit around Saint Louis (Senegal, West Africa) through Satellite-Derived Digital Elevation Model and Shoreline. *Remote Sensing*. [doi:10.3390/rs13132454](https://doi.org/10.3390/rs13132454)
- Shamsuzzoha (2023). Shoreline Change Assessment in the Coastal Region of Bangladesh Delta Using Tasseled Cap Transformation from Satellite Remote Sensing Dataset. *Remote Sensing*. [doi:10.3390/rs15020295](https://doi.org/10.3390/rs15020295)
- Paweł Burdziakowski (2020). Using UAV Photogrammetry to Analyse Changes in the Coastal Zone Based on the Sopot Tombolo (Salient) Measurement Project. *Sensors*. [doi:10.3390/s20144000](https://doi.org/10.3390/s20144000)
- Donatella Dominici (2019). High Resolution Satellite Images for Instantaneous Shoreline Extraction Using New Enhancement Algorithms. *Geosciences*. [doi:10.3390/geosciences9030123](https://doi.org/10.3390/geosciences9030123)
- Paweł Tysiąc (2020). Bringing Bathymetry LiDAR to Coastal Zone Assessment: A Case Study in the Southern Baltic. *Remote Sensing*. [doi:10.3390/rs12223740](https://doi.org/10.3390/rs12223740)
- Specht (2025). Spatial Analysis of Bathymetric Data from UAV Photogrammetry and ALS LiDAR: Shallow-Water Depth Estimation and Shoreline Extraction. *Remote Sensing*. [doi:10.3390/rs17173115](https://doi.org/10.3390/rs17173115)
- Erasmus (2026). Shoreline extraction and coastal change detection from satellite SAR using thresholding-based methods. *ISPRS Annals of the Photogrammetry, Remote Sensing and Spatial Information Sciences*. [doi:10.5194/isprs-annals-xi-3-2026-871-2026](https://doi.org/10.5194/isprs-annals-xi-3-2026-871-2026)
