# Local scour at structures

`scour.structures` | Scour around piles, foundations, and walls.

Parent: [Scour and erosion](scour.md)

Papers: 14. Claims: 14. Equations: 0.

Used by pyCoastal design modules: Seawall design, Pile wave loads.

## Synthesis

**Well established.** Local scour forms where structures accelerate flow and organize horseshoe, wake, contraction or overtopping jets that increase bed stress and sediment export; depth and footprint depend on forcing history, sediment mobility, geometry and feedback as the scour hole changes the flow.

**Governing physics.** Downflow and horseshoe vortices erode upstream toes, wake vortices remove sediment downstream, wave orbital reversal and currents alter symmetry, and tsunami overflow can drive intense leeward jets. Avalanching, armoring, seepage and deposition govern approach to equilibrium or progressive failure.

**Dimensionless parameters.** Controls include Shields and mobility numbers, Froude number, Keulegan-Carpenter number, wave-current ratio, relative submergence, structure-width-to-depth and width-to-grain ratios, sediment gradation, densimetric Froude number, scour depth normalized by width and time normalized by scour timescale.

**Major equations.** Assessment combines sediment continuity with bedload or suspended-load transport, critical Shields mobility and empirical equilibrium-depth/time-scale relations using structure width, flow depth, velocity, wave orbital motion and sediment size. Practical fragility links scour depth to foundation embedment and armor stability.

**Typical methods.** Studies use mobile-bed flumes with repeated bed scans and synchronized velocity or wave measurements, vary current and wave combinations and geometry, check scale and sediment mobility, fit time evolution and equilibrium depth, validate morphology models and compare with post-event surveys and foundation damage.

**Numerical models.** The reviewed branch provides a field-informed practical scour model. Related evidence includes coupled RANS-VOF, bedload and moving-bed morphology for vertical structures, but broad pile-specific CFD, compound-pile and twin-pile formulations are not yet reviewed here.

**Experimental datasets.** Reviewed primary evidence comprises post-2011 Tohoku coastal-defense surveys followed by hydraulic experiments used to refine a practical tsunami scour-depth model. Direct pile and jacket datasets remain in the lawful-full-text queue.

**Validated ranges.** Support is specific to surveyed Tohoku defenses and the associated hydraulic experiments. It does not validate equilibrium formulas for steady-current piles, random waves, combined flow, jackets or different soils and foundation configurations.

**Recent advances.** Recent advances use high-resolution sonar and photogrammetry, particle-resolving CFD-DEM, coupled hydro-morphodynamic and geotechnical simulation, probabilistic surrogate models, digital-twin monitoring and adaptive scour protection.

**Disagreements.** Equilibrium formulas differ over whether wave-current effects combine through peak velocity, effective shear or vortex regime. Laboratory scale can distort sediment mobility and turbulence, while field failure often couples scour with armor displacement, soil response and structural damage.

**Limitations.** Single-source primary coverage, uncertain event hydrographs, post-event survey timing, soil heterogeneity, scale effects, armoring, cohesive sediment, debris, three-dimensional geometry, storm sequences and backfilling restrict transfer. Maximum depth alone omits footprint and foundation demand.

**Open questions.** Priorities include transient compound wave-current-tsunami forcing, complex pile groups and jackets, layered/cohesive beds, scour–structure interaction, probabilistic time-dependent fragility, monitoring assimilation, countermeasure degradation and full-scale benchmark datasets.

**Seminal papers.** Classical bridge-pier and marine-pile experiments established horseshoe and wake-vortex mechanisms and equilibrium scaling; pipeline and breakwater studies extended wave and toe regimes, followed by RANS morphology and structure–soil interaction models.

## Claims

- **C381.** Post-2011 Tohoku surveys identified six coastal-defense failure modes, with leeward toe scour dominant at most surveyed locations; a practical scour-depth model using field-measurable tsunami, soil, and structure quantities was subsequently refined with hydraulic experiments. *Regime: Level-2 Tohoku tsunami damage to dikes, seawalls, and breakwaters in Miyagi and Fukushima..* [direct_finding, mixed] (Mantripathi Prabath Ravindra Jayaratne 2016, [doi:10.1142/s0578563416400179](https://doi.org/10.1142/s0578563416400179))
- **C1233.** A 3D RANS morphodynamic model found omitting suspended load reduced equilibrium cylinder scour depth by 50%, while vortex shedding mainly affected the earliest stage; horseshoe and lee-wake vortices organized transport. *Regime: Numerical investigation of flow and scour around a vertical circular cylinder.* [direct_finding, mixed] (Cüneyt Baykal 2015, [doi:10.1098/rsta.2014.0104](https://doi.org/10.1098/rsta.2014.0104))
- **C1234.** A monopile review synthesizes current-, wave-, combined-, and complex-loading scour mechanisms and equations and prioritizes unsteady-tide experiments, CFD–DEM, and artificial intelligence. *Regime: Local scour at offshore windfarm monopile foundations: A review.* [direct_finding, mixed] (Dawei Guan 2022, [doi:10.1016/j.wse.2021.12.006](https://doi.org/10.1016/j.wse.2021.12.006))
- **C1235.** Validated CFD–DEM shows offshore-pile scour depends on velocity, gravity, fluid and drag forces, and particle contact; maximum average drag occurred near 90° but maximum scour near 45° to the incoming flow. *Regime: Local Scour Mechanism of Offshore Wind Power Pile Foundation Based on CFD-DEM.* [direct_finding, mixed] (Qin Liu 2022, [doi:10.3390/jmse10111724](https://doi.org/10.3390/jmse10111724))
- **C1236.** A dimensionless 1D CNN for complex bridge-pier clear-water scour achieved R²=0.85, RMSE=0.1125, MAE=0.1078 and low bias on unseen data, outperforming FDOT, HEC-18 and Coleman equations. *Regime: A CNN deep learning approach to scour depth estimation around complex bridge piers in steady flow environments.* [direct_finding, mixed] (Ngoc Thi Huynh 2025, [doi:10.1186/s43251-025-00170-8](https://doi.org/10.1186/s43251-025-00170-8))
- **C1237.** A methodological synthesis concludes scour remains incompletely understood across bridges, pipelines and offshore wind foundations and requires complementary laboratory, numerical, and field approaches. *Regime: Experimental, Numerical and Field Approaches to Scour Research.* [direct_finding, mixed] (Yee-Meng Chiew 2020, [doi:10.3390/w12061749](https://doi.org/10.3390/w12061749))
- **C1239.** A 3D SWASH/flume study attributes about 75–80% of total bridge-pier scour depth predominantly to flow and 15–30% to redistribution of longitudinal velocity, alongside direct impact and horseshoe-vortex suction. *Regime: Study on the Mechanism of Local Scour Around Bridge Piers.* [direct_finding, mixed] (Haiyang Dong 2025, [doi:10.3390/jmse13061021](https://doi.org/10.3390/jmse13061021))
- **C1240.** Tests and models found unprotected monopile scour slightly exceeded pile diameter, open-jacket scour was lower, and SEDSCOUR predicted sandy beds with up to 30% mud; caisson scour required geometry-resolving treatment. *Regime: Scour near Offshore Monopiles, Jacket-Type and Caisson-Type Structures.* [direct_finding, mixed] (Leo C. van Rijn 2025, [doi:10.3390/jmse13020266](https://doi.org/10.3390/jmse13020266))
- **C1397.** A review of wave-driven pier scour synthesizes governing hydrodynamics, sediment response, experimental and numerical methods, and unresolved needs for coastal foundation design. *Regime: Scour around Piers under Waves: Current Status of Research and Its Future Prospect.* [literature_review_statement, review] (Ainal Hoque Gazi 2019, [doi:10.3390/w11112212](https://doi.org/10.3390/w11112212))
- **C1422.** Experiments show that seabed scour changes the lateral resistance of offshore wind-turbine monopiles and therefore must be represented in foundation assessment. *Regime: Impact of scour on lateral resistance of wind turbine monopiles: an experimental study.* [direct_finding, experimental] (Qiang Li 2020, [doi:10.1139/cgj-2020-0219](https://doi.org/10.1139/cgj-2020-0219))
- **C1423.** Scour and scour protection modify the stiffness of monopile foundations in sand, linking evolving seabed geometry to offshore structural response. *Regime: Influence of scour and scour protection on the stiffness of monopile foundations in sand.* [direct_finding, mixed] (Jann-Eike Saathoff 2024, [doi:10.1016/j.apor.2024.103920](https://doi.org/10.1016/j.apor.2024.103920))
- **C1521.** A bioinspired design framework translates root-system anchorage, adaptability, and soil interaction into concepts for resilient coastal foundations. *Regime: Root Systems Research for Bioinspired Resilient Design: A Concept Framework for Foundation and Coastal Engineering.* [literature_review_statement, review] (Elena Stachew 2021, [doi:10.3389/frobt.2021.548444](https://doi.org/10.3389/frobt.2021.548444))
- **C1615.** For experimental toe-scour data at sloping seawalls with shingle foreshores, support-vector regression was the best of four tested machine-learning methods (R-squared 0.74, RMSE 0.28, MAE 0.17), while Iribarren number was the most influential predictor. *Regime: Relative toe-scour depth at sloping seawalls with shingle foreshores within the source experimental dataset..* [direct_finding, mixed] (M. A. Habib 2024, [doi:10.3389/fbuil.2024.1343398](https://doi.org/10.3389/fbuil.2024.1343398))
- **C1715.** Coupling large-eddy free-surface flow with bed-load transport reproduces initial tsunami scour at revetment toes and behind overtopped seawalls, but equilibrium scour requires longer simulations and suspended-sediment transport. *Regime: Tsunami impingement and overtopping at near-vertical revetments and sharp-edged seawalls with mobile beds..* [direct_finding, numerical] (NAKAYAMA 2015, [doi:10.2208/kaigan.71.i_811](https://doi.org/10.2208/kaigan.71.i_811))

## Papers

- Cüneyt Baykal (2015). Numerical investigation of flow and scour around a vertical circular cylinder. *Philosophical Transactions of the Royal Society A: Mathematical, Physical and Engineering Sciences*. [doi:10.1098/rsta.2014.0104](https://doi.org/10.1098/rsta.2014.0104)
- Dawei Guan (2022). Local scour at offshore windfarm monopile foundations: A review. *Water Science and Engineering*. [doi:10.1016/j.wse.2021.12.006](https://doi.org/10.1016/j.wse.2021.12.006)
- Mantripathi Prabath Ravindra Jayaratne (2016). Failure Mechanisms and Local Scour at Coastal Structures Induced by Tsunami. *Coastal Engineering Journal*. [doi:10.1142/s0578563416400179](https://doi.org/10.1142/s0578563416400179)
- M. A. Habib (2024). Efficient data-driven machine learning models for scour depth predictions at sloping sea defences. *Frontiers in Built Environment*. [doi:10.3389/fbuil.2024.1343398](https://doi.org/10.3389/fbuil.2024.1343398)
- Qiang Li (2020). Impact of scour on lateral resistance of wind turbine monopiles: an experimental study. *Canadian Geotechnical Journal*. [doi:10.1139/cgj-2020-0219](https://doi.org/10.1139/cgj-2020-0219)
- Elena Stachew (2021). Root Systems Research for Bioinspired Resilient Design: A Concept Framework for Foundation and Coastal Engineering. *Frontiers in Robotics and AI*. [doi:10.3389/frobt.2021.548444](https://doi.org/10.3389/frobt.2021.548444)
- Qin Liu (2022). Local Scour Mechanism of Offshore Wind Power Pile Foundation Based on CFD-DEM. *Journal of Marine Science and Engineering*. [doi:10.3390/jmse10111724](https://doi.org/10.3390/jmse10111724)
- Ainal Hoque Gazi (2019). Scour around Piers under Waves: Current Status of Research and Its Future Prospect. *Water*. [doi:10.3390/w11112212](https://doi.org/10.3390/w11112212)
- Jann-Eike Saathoff (2024). Influence of scour and scour protection on the stiffness of monopile foundations in sand. *Applied Ocean Research*. [doi:10.1016/j.apor.2024.103920](https://doi.org/10.1016/j.apor.2024.103920)
- Ngoc Thi Huynh (2025). A CNN deep learning approach to scour depth estimation around complex bridge piers in steady flow environments. *Advances in Bridge Engineering*. [doi:10.1186/s43251-025-00170-8](https://doi.org/10.1186/s43251-025-00170-8)
- Yee-Meng Chiew (2020). Experimental, Numerical and Field Approaches to Scour Research. *Water*. [doi:10.3390/w12061749](https://doi.org/10.3390/w12061749)
- Haiyang Dong (2025). Study on the Mechanism of Local Scour Around Bridge Piers. *Journal of Marine Science and Engineering*. [doi:10.3390/jmse13061021](https://doi.org/10.3390/jmse13061021)
- Leo C. van Rijn (2025). Scour near Offshore Monopiles, Jacket-Type and Caisson-Type Structures. *Journal of Marine Science and Engineering*. [doi:10.3390/jmse13020266](https://doi.org/10.3390/jmse13020266)
- NAKAYAMA (2015). Large Eddy Simulation of Scour Due to Tsunami Flow Overtopping Seawall and Revetment. *Journal of Japan Society of Civil Engineers, Ser. B2 (Coastal Engineering)*. [doi:10.2208/kaigan.71.i_811](https://doi.org/10.2208/kaigan.71.i_811)
