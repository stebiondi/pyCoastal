# Dunes and overwash

`beaches.dunes` | Dune erosion, overwash, and recovery.

Parent: [Beaches and shoreline evolution](beaches.md)

Papers: 5. Claims: 9. Equations: 1.

## Synthesis

**Well established.** Storm waves and elevated water levels erode dune faces and redistribute sediment toward the beach and nearshore; whether impact remains collision and scarping or progresses to overwash and inundation depends jointly on forcing intensity and pre-storm berm–dune geometry.

**Governing physics.** In the reviewed New Jersey study, peak joint wave-water-level forcing was the dominant tested predictor of dune loss, while berm and dune morphology modulated how much forcing reached and removed the dune.

**Dimensionless parameters.** Transferable regime descriptors include water level and runup relative to dune toe and crest, freeboard normalized by wave height, surf similarity, storm duration relative to profile-adjustment time, berm and dune volume normalized by active-profile scales, and erosion or overwash volume relative to initial dune volume.

**Major equations.** Dune impact was quantified as 100 times the difference between pre- and post-storm area inside the pre-storm dune footprint divided by the pre-storm area.

**Typical methods.** One demonstrated workflow combines repeated pre/post-storm beach profiles, hindcast wave and water-level intensity indices, correlation analysis, and classification-tree ensembles with held-out testing.

**Numerical models.** A 260-tree bootstrap ensemble predicted Minor, Moderate, and Major dune-volume-loss classes with reported within-dataset accuracies of 92%, 84%, and 98%, respectively; this was not external regional validation.

**Experimental datasets.** The New Jersey Beach Profile Network supported profile-based erosion analysis for eighteen historical storms selected from a 1980-2013 erosion-potential climatology.

**Validated ranges.** The model was trained and tested for New Jersey profiles with berm volume 1.8-420.1 m3/m, dune volume 1.5-281.7 m3/m, median grain size 0.16-2.19 mm, crest elevation 2.2-7.8 m NAVD, toe elevation 1.0-4.8 m NAVD, SEI 55-3871, and PEI 24.3-163.3.

**Recent advances.** For this dataset, PEI below 69 generally separated Minor impacts and PEI above 102 generally separated Moderate/Major impacts; morphology was necessary between those thresholds.

**Disagreements.** Forcing-only thresholds can separate weak and severe impacts in some datasets, while intermediate cases require morphology; process-based profile models explain sediment redistribution but do not by themselves establish universal damage classes. These are complementary scales, not interchangeable predictors.

**Limitations.** The available reviewed evidence is geographically narrow; its data-driven thresholds and performance should not be transferred outside New Jersey or beyond the reported storm and morphology ranges without retraining or increased uncertainty.

**Open questions.** Unresolved needs include representing the timing and duration of peak erosion intensity, adding rare severe impacts, testing other beach regimes, and externally validating the model.

**Seminal papers.** Early storm-surge profile models established offshore redistribution of eroded dune sand under elevated water levels; later impact-regime concepts organized collision, overwash and inundation, and modern data-driven work quantifies how storm intensity and morphology jointly classify loss.

## Equations

### Dune volume loss percentage

$$
d_{loss}(\%) = \frac{A_{pre}-A_{post}}{A_{pre}} \times 100
$$

Regime: Profile-based storm impact classification used in this study; Minor <5%, Moderate 5-40%, Major >40% loss.

Variables: `A_pre` pre-storm cross-sectional area within the pre-storm dune footprint; `A_post` post-storm cross-sectional area within the pre-storm dune footprint

Source: (Lemke 2021, [doi:10.3390/jmse9121428](https://doi.org/10.3390/jmse9121428))

## Claims

- **C1.** Among the seven tested predictors, Peak Erosion Intensity was the most important predictor of storm-induced dune damage. *Regime: Compiled New Jersey beach-profile observations for eighteen storms, using the seven reported predictors and PEI range 24.3-163.3..* [direct_finding, field] (Lemke 2021, [doi:10.3390/jmse9121428](https://doi.org/10.3390/jmse9121428))
- **C2.** PEI below 69 generally identified Minor dune damage, whereas PEI above 102 generally identified Moderate or Major damage in the study data. *Regime: New Jersey training observations; damage defined by dune-volume loss (<5% Minor, 5-40% Moderate, >40% Major); high-PEI branch based on only 33 observations..* [direct_finding, field] (Lemke 2021, [doi:10.3390/jmse9121428](https://doi.org/10.3390/jmse9121428))
- **C3.** For intermediate storm intensity, beach-dune morphology was needed in addition to PEI to distinguish dune-damage outcomes. *Regime: New Jersey observations and the reported morphology ranges; derived from the fitted tree and ensemble, not a universal physical threshold..* [direct_finding, field] (Lemke 2021, [doi:10.3390/jmse9121428](https://doi.org/10.3390/jmse9121428))
- **C4.** Larger berm volume was associated with lower percent dune loss under comparable storm intensities in the compiled observations. *Regime: New Jersey profile/storm data, particularly PEI 69-82; association within the fitted data does not alone establish universal causality..* [direct_finding, field] (Lemke 2021, [doi:10.3390/jmse9121428](https://doi.org/10.3390/jmse9121428))
- **C118.** Under the modeled storm-surge process, eroded dune sand was transported offshore and deposited on the beach as the profile adjusted to the elevated water level. *Regime: Sandy beach-dune profiles subjected to the study's storm-surge and random-wave conditions..* [direct_finding, experimental] (Vellinga 1982, [doi:10.1016/0378-3839(82)90007-2](https://doi.org/10.1016/0378-3839(82)90007-2))
- **C1342.** Pre- and post-Sandy LiDAR across more than 800 profiles found dune faces steepened 43% without becoming vertical and only half the dune toes followed the assumed foreshore-slope trajectory, challenging common erosion-model assumptions. *Regime: Testing model parameters for wave‐induced dune erosion using observations from Hurricane Sandy.* [direct_finding, field] (Overbeck 2017, [doi:10.1002/2016gl071991](https://doi.org/10.1002/2016gl071991))
- **C1633.** Nine months of hourly Greenwich Dunes monitoring show that moderate 8-12 m/s winds delivered much of the foredune sediment, whereas only 1 of 15 large wind events produced large deposition and the strongest storms instead caused wave scarping; wind angle, fetch, moisture and snow/ice governed event effectiveness. *Regime: Greenwich Dunes, Prince Edward Island, across nine months of wind, beach and seasonal conditions..* [direct_finding, field] (Irene Delgado‐Fernández 2010, [doi:10.1016/j.geomorph.2010.11.005](https://doi.org/10.1016/j.geomorph.2010.11.005))
- **C1634.** A two-step meso-scale dune-supply model improved nine-month sediment-input predictions by first filtering winds that fail supply thresholds and then reducing potential transport for fetch and moisture; predictions matched measured deposition order of magnitude while coarse surveys missed erosion between events. *Regime: Greenwich Dunes, Prince Edward Island, with hourly wind and supply controls over nine months..* [direct_finding, mixed] (Irene Delgado‐Fernández 2011, [doi:10.1016/j.geomorph.2011.04.001](https://doi.org/10.1016/j.geomorph.2011.04.001))
- **C1775.** Across 861 Hurricane Sandy lidar profiles, dune faces steepened by 43% on average but never became vertical, half of dune toes retreated downward opposite the commonly assumed foreshore-slope trajectory, and dunes lost 41% of their volume on average, demonstrating that standard wave-impact erosion assumptions can overestimate dune stability. *Regime: Undeveloped sandy dunes in Maryland, New Jersey, and New York exposed to Hurricane Sandy collision-regime forcing, evaluated with pre/post-storm airborne lidar and a COAWST-derived total-water-level hindcast..* [direct_finding, field] (Overbeck 2017, [doi:10.1002/2016gl071991](https://doi.org/10.1002/2016gl071991))

## Papers

- Irene Delgado‐Fernández (2010). Meso-scale aeolian sediment input to coastal dunes: The nature of aeolian transport events. *Geomorphology*. [doi:10.1016/j.geomorph.2010.11.005](https://doi.org/10.1016/j.geomorph.2010.11.005) [accepted manuscript, read only](https://research.edgehill.ac.uk/ws/files/20179544/DF_DA_2011_GEOMORPHOLOGY_Events.pdf)
- Vellinga (1982). Beach and dune erosion during storm surges. *Coastal Engineering*. [doi:10.1016/0378-3839(82)90007-2](https://doi.org/10.1016/0378-3839(82)90007-2) [published version, read only](https://publications.deltares.nl/Pub276.pdf)
- Irene Delgado‐Fernández (2011). Meso-scale modelling of aeolian sediment input to coastal dunes. *Geomorphology*. [doi:10.1016/j.geomorph.2011.04.001](https://doi.org/10.1016/j.geomorph.2011.04.001) [accepted manuscript, read only](https://research.edgehill.ac.uk/ws/files/20180557/DF_2011_GEOMORPHOLOGY_MODELLING_MESO-SCALE.pdf)
- Lemke (2021). Role of Storm Erosion Potential and Beach Morphology in Controlling Dune Erosion. *Journal of Marine Science and Engineering*. [doi:10.3390/jmse9121428](https://doi.org/10.3390/jmse9121428) [published version, CC BY](https://mdpi-res.com/bookfiles/book/6169/BeachDune_System_Morphodynamics.pdf)
- Overbeck (2017). Testing model parameters for wave‐induced dune erosion using observations from Hurricane Sandy. *Geophysical Research Letters*. [doi:10.1002/2016gl071991](https://doi.org/10.1002/2016gl071991) [published version, public domain](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1002/2016GL071991)
