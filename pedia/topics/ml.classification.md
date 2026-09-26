# Feature detection and classification

`ml.classification` | Automated extraction from observations.

Parent: [Machine learning and data science](ml.md)

Papers: 20. Claims: 14. Equations: 1.

## Synthesis

**Well established.** Coastal feature classification is credible only when the target class and annotation protocol are explicit, evaluation is separated from training, and metrics address class imbalance and boundary quality; high within-dataset accuracy alone does not prove cross-site operational skill.

**Governing physics.** Models infer physical or ecological classes indirectly from spectral reflectance, color, texture, shape, elevation, echo behavior and temporal persistence; tides, turbidity, wetness, waves, illumination, season, sensor geometry and disturbance alter those observable signatures.

**Dimensionless parameters.** Useful normalized controls include IoU and Dice/F1, precision and recall, balanced accuracy, kappa, class prevalence, boundary tolerance relative to pixel size, train/test spatial separation, resolution-to-feature ratio, confidence and calibration error.

**Major equations.** Core formulations include supervised loss such as cross-entropy, class-weighted or overlap loss; SVM margins; clustering distances; object rules; and confusion-matrix metrics including accuracy, balanced accuracy, precision, recall, F1 and intersection-over-union.

**Typical methods.** Workflows define classes and use cases, acquire and co-register imagery or point clouds, label representative samples, engineer or learn features, split data spatially and temporally, train and tune models, compare baselines, audit errors and uncertainty, and validate on independent sites or surveys.

**Numerical models.** Methods include SVM, Otsu and Iso Cluster baselines, GEOBIA rules, U-Net with attention, ResNet and other pretrained CNNs, bagged handcrafted features, semantic segmentation, repeated point-cloud clustering and multi-resolution sensor fusion.

**Experimental datasets.** The reviewed evidence spans Landsat seagrass time series, Sentinel and UAV shoreline data, Florida UAS intertidal habitats, Togolese NDWI shorelines, South China Sea beachrock imagery, underwater benthic images from six Australia–Japan sites, and Polish topo-bathymetric LiDAR groynes.

**Validated ranges.** Reported tests range from one site and sensor to six study areas and a 31-year satellite record; performance values are conditional on the stated labels, resolution, preprocessing and split, and do not establish transfer to different coast types or acquisition conditions.

**Recent advances.** Recent advances combine attention U-Nets, pretrained multi-architecture comparison, satellite–UAV–GNSS fusion, long time-series deep classification, underwater habitat automation and topo-bathymetric LiDAR clustering for structures across the air–water interface.

**Disagreements.** Deep learned features can outperform fixed thresholds and handcrafted rules when labels are adequate, while object rules and classical classifiers can be more interpretable and data efficient. Pixel accuracy may conflict with boundary or minority-class performance, and apparent temporal change may reflect domain shift.

**Limitations.** Common weaknesses are small or correlated training sets, expensive and inconsistent labels, rare classes, unclear train/test leakage, cloud and water-column effects, sensor and seasonal domain shift, weak uncertainty calibration, coarse pixels, ambiguous boundaries and limited independent-site validation.

**Open questions.** Priorities include transferable labels, cross-sensor and cross-site adaptation, few-shot rare-class learning, physics-aware features, temporal consistency, boundary uncertainty, open benchmarks, reproducible annotation, calibrated confidence and operational human review.

**Seminal papers.** Remote-sensing classification developed from thresholding, clustering and maximum-likelihood methods through SVM and object-based image analysis; convolutional networks, U-Net semantic segmentation and transfer learning later enabled end-to-end coastal feature extraction.

## Equations

### Explained variance of spectral-type clustering

$$
EV=1-\frac{SSE}{SSE_T}
$$

Regime: PCA-reduced K-means clustering of hourly frequency-direction spectra at each of seven Africa-basin control points.

Variables: `EV` proportion of historical spectral variance explained by cluster centroids; `SSE` within-cluster sum of squared deviations from representative centroids; `SSE_T` total sum of squared errors of the historical dataset

Source: (Romano-Moreno 2023, [doi:10.1016/j.coastaleng.2022.104271](https://doi.org/10.1016/j.coastaleng.2022.104271))

## Claims

- **C5.** The selected 260-tree ensemble classified Minor, Moderate and Major dune-damage observations with reported accuracies of 92%, 84% and 98%, respectively. *Regime: The compiled, imbalanced New Jersey dataset and the paper's 80/20 random split; performance is not external validation in another region..* [direct_finding, field] (Lemke 2021, [doi:10.3390/jmse9121428](https://doi.org/10.3390/jmse9121428))
- **C103.** A 5 by 5 spectral-type lattice retained more than 70% explained variance while avoiding the one-hour-in-40-years clusters produced by larger lattices. *Regime: K-means/PCA clustering of 40 years of hourly reconstructed spectra at seven Africa-basin control points; 25 types are a study-specific compromise, not a universal optimum..* [direct_finding, numerical] (Romano-Moreno 2023, [doi:10.1016/j.coastaleng.2022.104271](https://doi.org/10.1016/j.coastaleng.2022.104271))
- **C145.** A random forest combining improved coastal altimetry with ten-year simulations correctly identified 93% of Gulf of Lion slope-current intrusions when evaluated against independent ADCP observations. *Regime: The Gulf of Lion, its retracked altimetry product, training simulations, and event definition..* [direct_finding, mixed] (Casella 2020, [doi:10.3390/rs12223686](https://doi.org/10.3390/rs12223686))
- **C155.** U-Net and DeepLabv3+ shoreline segmentation on coastal Timex imagery achieved global accuracy 0.98, mean IoU 0.95-0.97, and boundary F1 up to 0.99 within the evaluated dataset. *Regime: The labeled fixed-camera Timex dataset; independent cross-site generalization remains unverified..* [direct_finding, numerical] (Santos 2025, [doi:10.3390/rs17233865](https://doi.org/10.3390/rs17233865))
- **C1095.** A deep-learning analysis of 31 annual Landsat observations estimated stable St. Joseph Bay seagrass extent at 23±3 km² while resolving six short post-cyclone declines and recovery. *Regime: Temporal Stability of Seagrass Extent, Leaf Area, and Carbon Storage in St. Joseph Bay, Florida: a Semi-automated Remote Sensing Analysis.* [direct_finding, field] (Marie Cindy Lebrasse 2022, [doi:10.1007/s12237-022-01050-4](https://doi.org/10.1007/s12237-022-01050-4))
- **C1096.** A focused review identifies Landsat and Sentinel as core open shoreline records, U-Net/CNN segmentation as emerging automation, and UAV/GNSS data as local validation while highlighting cloud, fusion, and cross-coast generalization limits. *Regime: A Review of Open Remote Sensing Data with GIS, AI, and UAV Support for Shoreline Detection and Coastal Erosion Monitoring.* [literature_review_statement, review] (Demetris Christofi 2025, [doi:10.3390/app15094771](https://doi.org/10.3390/app15094771))
- **C1097.** UAS orthomosaics and surface models classified mudflat, salt-marsh, and oyster-reef habitat with a repeatable GEOBIA ruleset and 79% overall accuracy despite weak class separability. *Regime: Quantifying Intertidal Habitat Relative Coverage in a Florida Estuary Using UAS Imagery and GEOBIA.* [direct_finding, field] (Michael C. Espriella 2020, [doi:10.3390/rs12040677](https://doi.org/10.3390/rs12040677))
- **C1098.** Comparison of Otsu, unsupervised Iso Cluster, and supervised SVM on NDWI imagery found SVM more effective for shoreline extraction across linear and nonlinear Togolese coasts. *Regime: Coastline Change Modelling Induced by Climate Change Using Geospatial Techniques in Togo (West Africa).* [direct_finding, field] (Yawo Konko 2020, [doi:10.4236/ars.2020.92005](https://doi.org/10.4236/ars.2020.92005))
- **C1099.** A structured survey organizes deep-learning architectures, image sources, data limitations, and context-dependent tradeoffs for automated seagrass detection and classification. *Regime: A Survey of Deep Learning Approaches for the Monitoring and Classification of Seagrass.* [literature_review_statement, review] (Uzma Nawaz 2025, [doi:10.1007/s12601-025-00213-1](https://doi.org/10.1007/s12601-025-00213-1))
- **C1100.** Attention-enhanced U-Net segmentation of UAV beachrock imagery reached 97.47% accuracy and 88.65% IoU, improving IoU by 2.09 percentage points over baseline U-Net. *Regime: The Identification of Exposed Beachrocks on South China Sea Islands Based on UAV Images.* [direct_finding, field] (Chuang Liu 2025, [doi:10.3390/rs17091647](https://doi.org/10.3390/rs17091647))
- **C1101.** A six-area Australia–Japan evaluation combines pretrained CNNs, bagged features, color and texture for benthic classification and finds ResNet-50 strongest for both classification and semantic segmentation. *Regime: An Automated Framework for Benthic Habitat Classification and Segmentation Based on Deep Learning Algorithms.* [direct_finding, field] (H. A. Mohamed 2026, [doi:10.28991/cej-2026-012-02-022](https://doi.org/10.28991/cej-2026-012-02-022))
- **C1102.** Repeated clustering with topo-bathymetric LiDAR echo ratio automatically extracted Polish coastal groynes with 96% balanced accuracy against manual annotations. *Regime: Automated classification of coastal defense structures using airborne bathymetric LiDAR.* [direct_finding, field] (Jan Rhomberg-Kauert 2026, [doi:10.5194/isprs-annals-xi-2-2026-595-2026](https://doi.org/10.5194/isprs-annals-xi-2-2026-595-2026))
- **C1462.** Image-feature extraction and machine learning automate taxonomic classification of phytoplankton recorded by a submersible imaging flow cytometer. *Regime: Automated taxonomic classification of phytoplankton sampled with imaging‐in‐flow cytometry.* [direct_finding, mixed] (Heidi M. Sosik 2007, [doi:10.4319/lom.2007.5.204](https://doi.org/10.4319/lom.2007.5.204))
- **C1464.** Random forest, Cubist, and support-vector regression estimate chlorophyll-a and suspended particulate matter from GOCI imagery for Korean coastal-water monitoring. *Regime: Machine learning approaches to coastal water quality monitoring using GOCI satellite data.* [direct_finding, numerical] (Yong Hoon Kim 2014, [doi:10.1080/15481603.2014.900983](https://doi.org/10.1080/15481603.2014.900983))

## Papers

- Heidi M. Sosik (2007). Automated taxonomic classification of phytoplankton sampled with imaging‐in‐flow cytometry. *Limnology and Oceanography Methods*. [doi:10.4319/lom.2007.5.204](https://doi.org/10.4319/lom.2007.5.204) [published version, read only](https://onlinelibrary.wiley.com/doi/pdfdirect/10.4319/lom.2007.5.204)
- Yong Hoon Kim (2014). Machine learning approaches to coastal water quality monitoring using GOCI satellite data. *GIScience & Remote Sensing*. [doi:10.1080/15481603.2014.900983](https://doi.org/10.1080/15481603.2014.900983) [published version, read only](https://www.tandfonline.com/doi/pdf/10.1080/15481603.2014.900983?needAccess=true&role=button)
- Marie Cindy Lebrasse (2022). Temporal Stability of Seagrass Extent, Leaf Area, and Carbon Storage in St. Joseph Bay, Florida: a Semi-automated Remote Sensing Analysis. *Estuaries and Coasts*. [doi:10.1007/s12237-022-01050-4](https://doi.org/10.1007/s12237-022-01050-4) [published version, CC BY](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10054859/fullTextXML)
- Demetris Christofi (2025). A Review of Open Remote Sensing Data with GIS, AI, and UAV Support for Shoreline Detection and Coastal Erosion Monitoring. *Applied Sciences*. [doi:10.3390/app15094771](https://doi.org/10.3390/app15094771) [published version, CC BY](https://mdpi-res.com/d_attachment/applsci/applsci-15-04771/article_deploy/applsci-15-04771.pdf)
- Michael C. Espriella (2020). Quantifying Intertidal Habitat Relative Coverage in a Florida Estuary Using UAS Imagery and GEOBIA. *Remote Sensing*. [doi:10.3390/rs12040677](https://doi.org/10.3390/rs12040677) [published version, CC BY](https://www.mdpi.com/2072-4292/12/4/677/pdf?version=1582109444)
- Yawo Konko (2020). Coastline Change Modelling Induced by Climate Change Using Geospatial Techniques in Togo (West Africa). *Advances in Remote Sensing*. [doi:10.4236/ars.2020.92005](https://doi.org/10.4236/ars.2020.92005) [published version, CC BY](http://www.scirp.org/journal/PaperDownload.aspx?paperID=100744)
- Uzma Nawaz (2025). A Survey of Deep Learning Approaches for the Monitoring and Classification of Seagrass. *Ocean Science Journal*. [doi:10.1007/s12601-025-00213-1](https://doi.org/10.1007/s12601-025-00213-1) [published version, CC BY](https://link.springer.com/content/pdf/10.1007/s12601-025-00213-1.pdf)
- Chuang Liu (2025). The Identification of Exposed Beachrocks on South China Sea Islands Based on UAV Images. *Remote Sensing*. [doi:10.3390/rs17091647](https://doi.org/10.3390/rs17091647) [published version, CC BY](https://www.mdpi.com/2072-4292/17/9/1647/pdf?version=1746606314)
- H. A. Mohamed (2026). An Automated Framework for Benthic Habitat Classification and Segmentation Based on Deep Learning Algorithms. *Civil Engineering Journal*. [doi:10.28991/cej-2026-012-02-022](https://doi.org/10.28991/cej-2026-012-02-022) [published version, CC BY](https://civilejournal.org/index.php/cej/article/download/6258/2059)
- Jan Rhomberg-Kauert (2026). Automated classification of coastal defense structures using airborne bathymetric LiDAR. *ISPRS annals of the photogrammetry, remote sensing and spatial information sciences*. [doi:10.5194/isprs-annals-xi-2-2026-595-2026](https://doi.org/10.5194/isprs-annals-xi-2-2026-595-2026) [published version, CC BY](https://isprs-annals.copernicus.org/articles/XI-2-2026/595/2026/isprs-annals-XI-2-2026-595-2026.pdf)
- Lee (2021). Rapid prediction of peak storm surge from tropical cyclone track time series using machine learning. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2021.104024](https://doi.org/10.1016/j.coastaleng.2021.104024) [published version, read only](https://api.elsevier.com/content/article/PII:S0378383921001691?httpAccept=text/xml)
- Dewi (2016). Fuzzy Classification for Shoreline Change Monitoring in a Part of the Northern Coastal Area of Java, Indonesia. *Remote Sensing*. [doi:10.3390/rs8030190](https://doi.org/10.3390/rs8030190) [published version, CC BY](https://www.mdpi.com/2072-4292/8/3/190/pdf)
- Lemke (2021). Role of Storm Erosion Potential and Beach Morphology in Controlling Dune Erosion. *Journal of Marine Science and Engineering*. [doi:10.3390/jmse9121428](https://doi.org/10.3390/jmse9121428) [published version, CC BY](https://mdpi-res.com/bookfiles/book/6169/BeachDune_System_Morphodynamics.pdf)
- Romano-Moreno (2023). Multimodal harbor wave climate characterization based on wave agitation spectral types. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2022.104271](https://doi.org/10.1016/j.coastaleng.2022.104271) [published version, CC BY-NC-ND](https://api.elsevier.com/content/article/PII:S0378383922001843?httpAccept=text/xml)
- Simarro (2021). UCalib: Cameras Autocalibration on Coastal Video Monitoring Systems. *Remote Sensing*. [doi:10.3390/rs13142795](https://doi.org/10.3390/rs13142795) [published version, CC BY](https://www.mdpi.com/2072-4292/13/14/2795/pdf)
- Casella (2020). Coastal Current Intrusions from Satellite Altimetry. *Remote Sensing*. [doi:10.3390/rs12223686](https://doi.org/10.3390/rs12223686) [published version, CC BY](https://www.mdpi.com/2072-4292/12/22/3686/pdf)
- Santos (2025). Deep Learning-Based Semantic Segmentation for Automatic Shoreline Extraction in Coastal Video Monitoring Systems. *Remote Sensing*. [doi:10.3390/rs17233865](https://doi.org/10.3390/rs17233865) [published version, CC BY](https://www.mdpi.com/2072-4292/17/23/3865/pdf)
- Zongming WANG (2025). Advances and perspectives in coastal wetland remote sensing research. *National Remote Sensing Bulletin*. [doi:10.11834/jrs.20254407](https://doi.org/10.11834/jrs.20254407) [published version, read only](https://www.ygxb.ac.cn/rc-pub/front/front-article/download/100405752/lowqualitypdf/%E6%BB%A8%E6%B5%B7%E6%B9%BF%E5%9C%B0%E9%81%A5%E6%84%9F%E7%A0%94%E7%A9%B6%E8%BF%9B%E5%B1%95%E4%B8%8E%E5%B1%95%E6%9C%9B.pdf)
- Alipour (2026). Characterization of tropical cyclone surge evolution. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2026.105086](https://doi.org/10.1016/j.coastaleng.2026.105086)
- Marcus Silva-Santana (2026). Automated detection of river mouth opening and closure using cloud-based processing of Sentinel-2 imagery. *Estuarine Coastal and Shelf Science*. [doi:10.1016/j.ecss.2026.110052](https://doi.org/10.1016/j.ecss.2026.110052) [published version, read only](https://digibug.ugr.es/bitstream/10481/114341/1/Silva-Santana_etal_2026_EstuarCoastShelfSci.pdf)
