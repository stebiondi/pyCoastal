# Storm-driven beach response

`beaches.storms` | Erosion and recovery during storms.

Parent: [Beaches and shoreline evolution](beaches.md)

Papers: 15. Claims: 15. Equations: 3.

## Synthesis

**Well established.** Storm beach response is a redistribution problem governed jointly by hydrodynamic forcing and antecedent/local morphology: elevated waves erode the subaerial beach or dune and move sediment, but the magnitude and even sign of local shoreline change vary with exposure, orientation, reefs, currents, and sediment supply.

**Governing physics.** Integrated wave energy and duration organize storm demand, while direction controls longshore-current forcing and antecedent width/profile controls available sediment and exposure. Local refraction, wave focusing, rips, river input, and reefs can amplify erosion or produce adjacent deposition.

**Dimensionless parameters.** The foundational reviewed scaling parameter is relative fall velocity H/(Tw), combining wave height, period, and sediment settling velocity. Correlation, explained skill, and return probability are statistical rather than universal physical similarity parameters and must retain their site/sample definition.

**Major equations.** Reviewed formulations range from Vellinga's fall-velocity similitude H/(Tw), through Leont'yev's zone-dependent q=qW+qR transport decomposition, to storm indices SPI=Hs^2 t and TSWE=integral(Pw dt), shoreline rates NSM/EPR/LRR, and empirical multilinear or extreme-value response models.

**Typical methods.** Current evidence combines mobile-bed flumes, process-based cross-shore transport models, high-frequency video or profile monitoring, satellite/DSAS shoreline analysis, spectral wave downscaling, regression forecasting, extreme-value analysis, and event-scale 3D morphology mapping.

**Numerical models.** The reviewed model spectrum spans Vellinga's equilibrium-profile safety method, Leont'yev's cross-shore qW/qR process decomposition, site-specific multilinear forecasting, nested SWAN diagnostics, DSAS shoreline statistics, and empirical extreme-value/amplification curves; these models answer different temporal and spatial questions.

**Experimental datasets.** Reviewed datasets include random-wave Delta Flume mobile-bed tests up to Hs=2 m, 276 monitored Narrabeen-Collaroy storms, 48 years of five Narrabeen profiles plus six high-resolution storm responses, and 18 Iztuzu shorelines at 819 transects paired with a modeled 2013-2022 storm record.

**Validated ranges.** Quantitative skill is currently site-bound: the 2024 Narrabeen multilinear forecast reports RMSE 3.7-6.4 m over 276 events; the 2026 Narrabeen analysis spans 48 years but only six high-resolution events; Iztuzu uses 18 images over ten years and explicitly reports broad confidence intervals; Vellinga's large-scale waves reached Hs=2 m.

**Recent advances.** Recent advances combine high-frequency morphology with fast site-specific forecasting, direction-resolved satellite/model attribution, and full-beach 3D amplification analysis that exposes erosion maxima missed by conventional sparse transects.

**Disagreements.** Water level appears minor in the 2024 wave-dominated Narrabeen event regression, whereas storm-surge elevation is fundamental to Vellinga's dune-attack experiments. This is a regime difference, not evidence that water level is generally unimportant. Likewise, positive energy-erosion relations at exposed sectors coexist with deposition at sheltered or sediment-supplied Iztuzu sectors.

**Limitations.** The evidence is dominated by Dutch, Narrabeen, and Iztuzu cases. Sparse profiles can miss 3D hotspots, sparse images weaken correlation inference, abstract-only model records hide calibration ranges, and site-trained regressions may not extrapolate to surge-dominated, different-sediment, or differently oriented coasts.

**Open questions.** Major needs are transferable event models with uncertainty, simultaneous waves-water levels-currents-sediment observations, prediction of localized 3D amplification, separation of storm clusters from single events, field validation at data-poor coasts, and recovery-aware forecasting after erosion.

**Seminal papers.** Vellinga (1982) is the foundational reviewed journal study in this slice, establishing large-scale mobile-bed storm-dune experiments and fall-velocity similitude for Dutch dune safety assessment.

## Equations

### Storm power index

$$
SPI=H_s^2 t
$$

Regime: Modeled Iztuzu storms exceeding the study threshold for at least 12 hours.

Variables: `H_s` storm significant wave height; `t` storm duration in hours

Source: (Kılar 2025, [doi:10.1016/j.ocecoaman.2025.107748](https://doi.org/10.1016/j.ocecoaman.2025.107748))

### Total storm wave energy

$$
TSWE=\int_i^n P_w(t)\,dt
$$

Regime: Time-integrated modeled wave-power proxy for each identified storm.

Variables: `P_w` wave energy flux; `i,n` storm integration bounds

Source: (Kılar 2025, [doi:10.1016/j.ocecoaman.2025.107748](https://doi.org/10.1016/j.ocecoaman.2025.107748))

### Deep-water wave energy flux

$$
P_w=\frac{\rho g^2}{64\pi}H_s^2T_e
$$

Regime: Wave-power calculation used in the paper's storm-energy metric.

Variables: `rho` water density; `g` gravitational acceleration; `H_s` significant wave height; `T_e` energy period

Source: (Kılar 2025, [doi:10.1016/j.ocecoaman.2025.107748](https://doi.org/10.1016/j.ocecoaman.2025.107748))

## Claims

- **C111.** At Iztuzu Zones III-V, southern-storm duration, storm power index, and total storm wave energy correlated above 0.8 with end-point shoreline-change rate and above 0.7 with linear-regression rate. *Regime: Five-zone Iztuzu analysis over 2013-2022 using 18 manually digitized images and modeled storms; many 95% confidence intervals were wide because sample size was small..* [direct_finding, mixed] (Kılar 2025, [doi:10.1016/j.ocecoaman.2025.107748](https://doi.org/10.1016/j.ocecoaman.2025.107748))
- **C112.** Storms from the southern sector were more strongly associated with erosion of Iztuzu's southwest-facing central zones than storms from the south-southwest sector. *Regime: Iztuzu Zones II-IV, their reported orientations, modeled storm directions, and 2013-2022 shoreline record; sediment transport was inferred rather than measured..* [inferred_relationship, mixed] (Kılar 2025, [doi:10.1016/j.ocecoaman.2025.107748](https://doi.org/10.1016/j.ocecoaman.2025.107748))
- **C114.** A stronger storm metric did not imply erosion everywhere at Iztuzu: reef- and river-outlet-influenced sectors showed negative correlations consistent with local wave-energy sheltering or sediment deposition. *Regime: Specific northern and reef-adjacent Iztuzu transects; causal sediment supply and transport were proposed but not directly observed..* [inferred_relationship, mixed] (Kılar 2025, [doi:10.1016/j.ocecoaman.2025.107748](https://doi.org/10.1016/j.ocecoaman.2025.107748))
- **C116.** The Iztuzu near-annual correlations often lacked significance at the 95% level because only a small number of high-resolution image intervals were available. *Regime: This study's 18-image, ten-year correlation design; absence of significance does not establish absence of storm influence..* [direct_finding, mixed] (Kılar 2025, [doi:10.1016/j.ocecoaman.2025.107748](https://doi.org/10.1016/j.ocecoaman.2025.107748))
- **C117.** Vellinga's large-scale Delta Flume tests used random waves up to 2 m significant height and supported mobile-bed similitude based on the dimensionless fall-velocity parameter H/(T w). *Regime: The paper's sandy mobile-bed 2D/3D program and Delta Flume storm-surge tests; transfer outside the tested sediment and profile regimes is not established here..* [direct_finding, experimental] (Vellinga 1982, [doi:10.1016/0378-3839(82)90007-2](https://doi.org/10.1016/0378-3839(82)90007-2))
- **C120.** Across 276 Narrabeen-Collaroy storm events, cumulative storm wave energy was the dominant erosion predictor, followed by pre-storm beach width and wave direction; water level contributed only weakly at this site. *Regime: Wave-dominated Narrabeen-Collaroy Beach and the observed 276-event predictor domain; the ranking is not universal for surge-dominated coasts..* [direct_finding, field] (Ibaceta 2024, [doi:10.1016/j.coastaleng.2024.104596](https://doi.org/10.1016/j.coastaleng.2024.104596))
- **C122.** During the 2016 Narrabeen-Collaroy storm, the measured local maximum erosion reached 235 m3/m above mean sea level and 58.3 m of shoreline retreat. *Regime: June 2016 event and the paper's above-MSL volume/shoreline definitions at Narrabeen-Collaroy..* [direct_finding, field] (Mitchell D. Harley 2026, [doi:10.1016/j.coastaleng.2026.104976](https://doi.org/10.1016/j.coastaleng.2026.104976))
- **C124.** Localized reef-related wave focusing and a migrating rip current produced erosion hotspots that were not represented by the five fixed historical profile locations. *Regime: The six high-resolution Narrabeen-Collaroy storm datasets and site-specific reef/rip morphology..* [direct_finding, mixed] (Mitchell D. Harley 2026, [doi:10.1016/j.coastaleng.2026.104976](https://doi.org/10.1016/j.coastaleng.2026.104976))
- **C1356.** After the 2013/14 winter, 38 southwest England beaches showed mechanism-dependent recovery: more than 200 m³/m offshore loss at exposed sand beaches, overwash loss at gravel barriers, and rotation at obliquely forced sites. *Regime: The extreme 2013/2014 winter storms: Beach recovery along the southwest coast of England.* [direct_finding, field] (Tim Scott 2016, [doi:10.1016/j.margeo.2016.10.011](https://doi.org/10.1016/j.margeo.2016.10.011))
- **C1434.** The 2013–2014 southwest England storms produced strongly site-dependent erosion and rotation governed by storm track, tide timing, coastal orientation, and embayment. *Regime: The extreme 2013/2014 winter storms: hydrodynamic forcing and coastal response along the southwest coast of England.* [direct_finding, field] (Gerd Masselink 2015, [doi:10.1002/esp.3836](https://doi.org/10.1002/esp.3836))
- **C1435.** During consecutive storms, antecedent morphology initially controlled beach response, while tide and surge became more important later and cumulative dune erosion persisted. *Regime: Beach erosion and recovery during consecutive storms at a steep‐sloping, meso‐tidal beach.* [direct_finding, field] (Michalis Vousdoukas 2011, [doi:10.1002/esp.2264](https://doi.org/10.1002/esp.2264))
- **C1436.** Post-storm beach recovery along Atlantic Europe was site-specific and multi-annual, with energetic winters stalling recovery and moderate winters accelerating it. *Regime: Beach recovery from extreme storm activity during the 2013–14 winter along the Atlantic coast of Europe.* [direct_finding, field] (Guillaume Dodet 2018, [doi:10.1002/esp.4500](https://doi.org/10.1002/esp.4500))
- **C1437.** LiDAR observations classify extreme-storm beach response by exposure, wave-approach angle, embayment, net volume change, and alongshore variability. *Regime: Classification of beach response to extreme storms.* [direct_finding, field] (Olivier Burvingt 2017, [doi:10.1016/j.geomorph.2017.07.022](https://doi.org/10.1016/j.geomorph.2017.07.022))
- **C1438.** XBeach-G reproduced gravel-beach storm responses from berm building to barrier rollover, and acceleration forces materially improved predictive skill. *Regime: Modelling the morphodynamics of gravel beaches during storms with XBeach-G.* [direct_finding, numerical] (Robert McCall 2015, [doi:10.1016/j.coastaleng.2015.06.002](https://doi.org/10.1016/j.coastaleng.2015.06.002))
- **C1591.** A storm-hazard matrix jointly classifies coastal flooding and beach erosion so events with different combinations of water-level and morphological impact are not reduced to a single hazard metric. *Regime: A storm hazard matrix combining coastal flooding and beach erosion.* [direct_finding, mixed] (Christopher K. Leaman 2021, [doi:10.1016/j.coastaleng.2021.104001](https://doi.org/10.1016/j.coastaleng.2021.104001))

## Papers

- Gerd Masselink (2015). The extreme 2013/2014 winter storms: hydrodynamic forcing and coastal response along the southwest coast of England. *Earth Surface Processes and Landforms*. [doi:10.1002/esp.3836](https://doi.org/10.1002/esp.3836) [published version, CC BY](https://onlinelibrary.wiley.com/doi/pdfdirect/10.1002/esp.3836)
- Tim Scott (2016). The extreme 2013/2014 winter storms: Beach recovery along the southwest coast of England. *Marine Geology*. [doi:10.1016/j.margeo.2016.10.011](https://doi.org/10.1016/j.margeo.2016.10.011) [published version, CC BY](https://www.sciencedirect.com/science/article/pii/S0025322716302766/pdf)
- Michalis Vousdoukas (2011). Beach erosion and recovery during consecutive storms at a steep‐sloping, meso‐tidal beach. *Earth Surface Processes and Landforms*. [doi:10.1002/esp.2264](https://doi.org/10.1002/esp.2264) [published version, read only](https://onlinelibrary.wiley.com/doi/pdfdirect/10.1002/esp.2264)
- Vellinga (1982). Beach and dune erosion during storm surges. *Coastal Engineering*. [doi:10.1016/0378-3839(82)90007-2](https://doi.org/10.1016/0378-3839(82)90007-2) [published version, read only](https://publications.deltares.nl/Pub276.pdf)
- Guillaume Dodet (2018). Beach recovery from extreme storm activity during the 2013–14 winter along the Atlantic coast of Europe. *Earth Surface Processes and Landforms*. [doi:10.1002/esp.4500](https://doi.org/10.1002/esp.4500) [published version, read only](https://onlinelibrary.wiley.com/doi/pdfdirect/10.1002/esp.4500)
- Olivier Burvingt (2017). Classification of beach response to extreme storms. *Geomorphology*. [doi:10.1016/j.geomorph.2017.07.022](https://doi.org/10.1016/j.geomorph.2017.07.022) [published version, CC BY](https://www.sciencedirect.com/science/article/pii/S0169555X17302970/pdf)
- Robert McCall (2015). Modelling the morphodynamics of gravel beaches during storms with XBeach-G. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2015.06.002](https://doi.org/10.1016/j.coastaleng.2015.06.002) [published version, CC BY](https://www.sciencedirect.com/science/article/pii/S0378383915001052/pdf)
- Christopher K. Leaman (2021). A storm hazard matrix combining coastal flooding and beach erosion. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2021.104001](https://doi.org/10.1016/j.coastaleng.2021.104001) [submitted manuscript, CC BY](https://eartharxiv.org/repository/object/1753/download/3719/)
- Leont'yev (1996). Numerical modelling of beach erosion during storm event. *Coastal Engineering*. [doi:10.1016/s0378-3839(96)00029-4](https://doi.org/10.1016/s0378-3839(96)00029-4)
- Ibaceta (2024). Data-driven modelling of coastal storm erosion for real-time forecasting at a wave-dominated embayed beach. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2024.104596](https://doi.org/10.1016/j.coastaleng.2024.104596) [published version, CC BY](https://api.elsevier.com/content/article/PII:S0378383924001443?httpAccept=text/xml)
- Kılar (2025). Wave storm impacts on shoreline evolution: A case study of Iztuzu beach. *Ocean &amp; Coastal Management*. [doi:10.1016/j.ocecoaman.2025.107748](https://doi.org/10.1016/j.ocecoaman.2025.107748) [published version, read only](https://acikerisim.uludag.edu.tr/bitstreams/c85bd685-4a66-457d-88b3-ab395a726911/download)
- Mitchell D. Harley (2026). Three-dimensional amplification of storm-driven beach erosion: Implications for setback lines at Narrabeen-Collaroy Beach, Australia. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2026.104976](https://doi.org/10.1016/j.coastaleng.2026.104976) [published version, CC BY](https://api.elsevier.com/content/article/PII:S037838392600030X?httpAccept=text/xml)
- Gerd Masselink (2014). Role of wave forcing, storms and NAO in outer bar dynamics on a high-energy, macro-tidal beach. *Geomorphology*. [doi:10.1016/j.geomorph.2014.07.025](https://doi.org/10.1016/j.geomorph.2014.07.025) [submitted manuscript, read only](http://hdl.handle.net/10026.1/3093)
- Lemke (2021). Role of Storm Erosion Potential and Beach Morphology in Controlling Dune Erosion. *Journal of Marine Science and Engineering*. [doi:10.3390/jmse9121428](https://doi.org/10.3390/jmse9121428) [published version, CC BY](https://mdpi-res.com/bookfiles/book/6169/BeachDune_System_Morphodynamics.pdf)
- Riccardo Briganti (2022). Wave overtopping at near-vertical seawalls: Influence of foreshore evolution during storms. *Ocean Engineering*. [doi:10.1016/j.oceaneng.2022.112024](https://doi.org/10.1016/j.oceaneng.2022.112024) [published version, CC BY](https://www.sciencedirect.com/science/article/pii/S0029801822013555/pdf)
