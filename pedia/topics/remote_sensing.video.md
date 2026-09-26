# Coastal video monitoring

`remote_sensing.video` | Image-derived waves, currents, and shoreline.

Parent: [Remote sensing](remote_sensing.md)

Papers: 10. Claims: 6. Equations: 1.

## Synthesis

**Well established.** Fixed coastal cameras provide frequent, low-cost observations of shoreline and breaker-zone behavior, but quantitative products require stable geometry, accurate calibration, visible scene features, and algorithms validated for the site and image conditions.

**Governing physics.** Timex imagery converts persistent optical signatures into measurable spatial patterns: breaking foam marks the breaker zone and time-averaged land-water contrast marks the shoreline; perspective projection maps those pixels into coastal coordinates.

**Dimensionless parameters.** Normalized RMSE, IoU, F1, and automatic-success fraction quantify retrieval performance but are dataset-specific. Viewing-angle geometry and relative feature density are central conditioning factors rather than universal similarity parameters.

**Major equations.** Core operations include projective camera geometry, image registration transforms, cross-correlation displacement, foam-length empirical breaker-height relations, and segmentation metrics such as intersection over union and boundary F1.

**Typical methods.** Typical workflows create snapshot and Timex images, detect static edges or features, stabilize and calibrate each frame, rectify pixels to ground coordinates, then apply empirical foam geometry, thresholding, or semantic segmentation and validate against independent waves or shorelines.

**Numerical models.** Models include Hsb,v/Hsb,v24 empirical breaker estimators, edge-keypoint geometric stabilization, UCalib feature-transfer calibration, and U-Net/DeepLabv3+ semantic segmentation with several CNN backbones.

**Experimental datasets.** Reviewed evidence includes about 900 breaker-height records across five sites, five years of three-camera Anglet imagery, a three-camera UCalib conditioning study, and a labeled fixed-camera Timex segmentation dataset.

**Validated ranges.** The bathymetry-free breaker method spans 0.1-3.8 m with 18% mean normalized RMSE; Anglet stabilization automated at least 90% of frames; UCalib ranged from above 90% to about 40% success by feature availability; segmentation mIoU was 0.95-0.97 in-domain.

**Recent advances.** Recent advances shift from hand-designed thresholds toward autocalibration and deep segmentation, while adjacent satellite studies supply longer spatial context for waterline and shoreline interpretation.

**Disagreements.** High pixel-level segmentation scores do not guarantee accurate real-world shoreline coordinates: calibration drift can create tens to hundreds of metres of positional error. These evaluate different pipeline stages and must be validated jointly.

**Limitations.** Performance degrades with missing static features, poor visibility or illumination, foam ambiguity, occlusion, long camera range, thermal motion, unrepresented sites, and error propagation from calibration through rectification and extraction.

**Open questions.** Needs include standardized multi-site benchmarks, calibrated uncertainty from pixels to ground coordinates, robust feature-free calibration, domain adaptation across lighting and morphology, and fusion with satellite, UAV, buoy, and model observations.

**Seminal papers.** Within this screened slice, the Anglet stabilization study establishes the scale of long-term geometry error, while the Timex breaker-height paper demonstrates a directly engineering-relevant hydrodynamic retrieval.

## Equations

### Wave-energy transformation balance

$$
\nabla\cdot(E\mathbf{C}_g)=-D_b-D_f
$$

Regime: The tested irregular waves and laboratory bathymetry with incident energy and bathymetry known.

Variables: `E` wave energy density; `C_g` group velocity; `D_b` breaking dissipation; `D_f` bottom-friction or other dissipation

Source: (Flores 2016, [doi:10.1016/j.coastaleng.2016.04.008](https://doi.org/10.1016/j.coastaleng.2016.04.008))

## Claims

- **C149.** A bathymetry-free Timex foam-signature method estimated breaking wave heights of 0.1-3.8 m across five sites with mean normalized RMSE of 18% over about 900 records. *Regime: Visible breaker-foam signatures at the five tested sites; performance outside the tested morphology and lighting regimes is unverified..* [direct_finding, field] (Umberto Andriolo 2020, [doi:10.3390/rs12020204](https://doi.org/10.3390/rs12020204))
- **C150.** At Anglet, camera motion produced georectification errors up to 400 m at 2.5 km range and an apparent shoreline bias of roughly 10-20 m during winter 2013/2014; stabilization corrected at least 90% of frames automatically. *Regime: The Anglet installation and views containing stable recognizable land features..* [direct_finding, field] (Isaac Rodriguez-Padilla 2019, [doi:10.3390/rs12010070](https://doi.org/10.3390/rs12010070))
- **C151.** UCalib automatically calibrated more than 90% of images for feature-rich coastal cameras but only about 40% for the worst, nearly featureless camera, demonstrating that fixed-feature availability controls operational success. *Regime: Argus-like or CoastSnap imagery with reference calibrations and detectable fixed features..* [direct_finding, field] (Simarro 2021, [doi:10.3390/rs13142795](https://doi.org/10.3390/rs13142795))
- **C341.** In an irregular-wave laboratory surf zone, optical measurements of individual roller size yielded roller energy, dissipation and radiation stress that reproduced measured wave-height transformation and mean-water-level setup with minimal calibration, including transition-zone lag. *Regime: The tested irregular waves and laboratory bathymetry with incident energy and bathymetry known..* [direct_finding, experimental] (Flores 2016, [doi:10.1016/j.coastaleng.2016.04.008](https://doi.org/10.1016/j.coastaleng.2016.04.008))
- **C1278.** Pixel-intensity variability in coastal video robustly identifies the cross- and alongshore extent of shoaling, surf and swash domains, supporting automated breaking-height, depth-inversion and sediment-transport applications. *Regime: Nearshore Wave Transformation Domains from Video Imagery.* [direct_finding, mixed] (Umberto Andriolo 2019, [doi:10.3390/jmse7060186](https://doi.org/10.3390/jmse7060186))
- **C1431.** Inverse modeling of marine-radar image sequences retrieves surface-elevation maps and wave spectra, with buoy comparisons supporting the linear-wave imaging formulation. *Regime: Inversion of Marine Radar Images for Surface Wave Analysis.* [direct_finding, mixed] (JoséC. Nieto Borge 2004, [doi:10.1175/1520-0426(2004)021<1291:iomrif>2.0.co;2](https://doi.org/10.1175/1520-0426(2004)021<1291:iomrif>2.0.co;2))

## Papers

- JoséC. Nieto Borge (2004). Inversion of Marine Radar Images for Surface Wave Analysis. *Journal of Atmospheric and Oceanic Technology*. [doi:10.1175/1520-0426(2004)021<1291:iomrif>2.0.co;2](https://doi.org/10.1175/1520-0426(2004)021<1291:iomrif>2.0.co;2) [published version, read only](https://journals.ametsoc.org/downloadpdf/journals/atot/21/8/1520-0426_2004_021_1291_iomrif_2_0_co_2.pdf)
- Umberto Andriolo (2020). Breaking Wave Height Estimation from Timex Images: Two Methods for Coastal Video Monitoring Systems. *Remote Sensing*. [doi:10.3390/rs12020204](https://doi.org/10.3390/rs12020204) [published version, CC BY](https://www.mdpi.com/2072-4292/12/2/204/pdf)
- Umberto Andriolo (2019). Nearshore Wave Transformation Domains from Video Imagery. *Journal of Marine Science and Engineering*. [doi:10.3390/jmse7060186](https://doi.org/10.3390/jmse7060186) [published version, CC BY](https://mdpi-res.com/d_attachment/jmse/jmse-07-00186/article_deploy/jmse-07-00186.pdf)
- Isaac Rodriguez-Padilla (2019). A Simple and Efficient Image Stabilization Method for Coastal Monitoring Video Systems. *Remote Sensing*. [doi:10.3390/rs12010070](https://doi.org/10.3390/rs12010070) [published version, CC BY](https://www.mdpi.com/2072-4292/12/1/70/pdf)
- Flores (2016). Estimating surfzone wave transformation and wave setup from remote sensing data. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2016.04.008](https://doi.org/10.1016/j.coastaleng.2016.04.008)
- Simarro (2021). UCalib: Cameras Autocalibration on Coastal Video Monitoring Systems. *Remote Sensing*. [doi:10.3390/rs13142795](https://doi.org/10.3390/rs13142795) [published version, CC BY](https://www.mdpi.com/2072-4292/13/14/2795/pdf)
- Santos (2025). Deep Learning-Based Semantic Segmentation for Automatic Shoreline Extraction in Coastal Video Monitoring Systems. *Remote Sensing*. [doi:10.3390/rs17233865](https://doi.org/10.3390/rs17233865) [published version, CC BY](https://www.mdpi.com/2072-4292/17/23/3865/pdf)
- Gerd Masselink (2014). Role of wave forcing, storms and NAO in outer bar dynamics on a high-energy, macro-tidal beach. *Geomorphology*. [doi:10.1016/j.geomorph.2014.07.025](https://doi.org/10.1016/j.geomorph.2014.07.025) [submitted manuscript, read only](http://hdl.handle.net/10026.1/3093)
- Ibaceta (2024). Data-driven modelling of coastal storm erosion for real-time forecasting at a wave-dominated embayed beach. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2024.104596](https://doi.org/10.1016/j.coastaleng.2024.104596) [published version, CC BY](https://api.elsevier.com/content/article/PII:S0378383924001443?httpAccept=text/xml)
- Rafaël Almar (2018). A new remote predictor of wave reflection based on runup asymmetry. *Estuarine Coastal and Shelf Science*. [doi:10.1016/j.ecss.2018.10.018](https://doi.org/10.1016/j.ecss.2018.10.018) [accepted manuscript, read only](https://purehost.bath.ac.uk/ws/portalfiles/portal/189538102/Manuscript_20181011.pdf)
