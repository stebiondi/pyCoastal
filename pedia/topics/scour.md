# Scour and erosion

`scour` | Localized and distributed removal of bed material.

Subtopics: [Contraction and channel scour](scour.contraction.md), [Pipeline and cable scour](scour.pipelines.md), [Scour protection](scour.protection.md), [Local scour at structures](scour.structures.md)

Papers: 12. Claims: 4. Equations: 0.

## Synthesis

**Well established.** Local scour develops when structure-induced acceleration, downflow, horseshoe vortices, wake shedding and turbulence raise sediment transport above the surrounding supply. The evolving hole then modifies flow until equilibrium, time limitation, armoring or protection arrests change.

**Governing physics.** Pressure gradients drive downflow at the upstream face; horseshoe and lee vortices increase bed stress and suspension, flank acceleration redistributes sediment, and waves reverse or modulate transport. Sediment size, grading, cohesion, live-bed supply and geometry control response.

**Dimensionless parameters.** Key controls include Shields parameter, densimetric Froude number, Keulegan–Carpenter number, relative flow depth, pile-to-grain ratio, current-to-wave velocity ratio, sediment geometric spread, relative scour depth, live-bed mobility, protection stone stability and normalized time.

**Major equations.** Prediction couples Navier–Stokes or depth-resolved flow to bedload/suspended-load transport and Exner bed continuity. Engineering formulas scale equilibrium depth and timescale with geometry, flow intensity, Shields stress and wave–current parameters; reliability and surrogates quantify uncertainty or accelerate evaluation.

**Typical methods.** Evidence combines clear- and live-bed flumes, field bathymetry and monitoring, RANS/LES or CFD–DEM, morphodynamic solvers, empirical equilibrium/time formulas and learned surrogates. Validation should cover onset, temporal evolution, maximum depth, footprint and flow/sediment structure.

**Numerical models.** Models range from empirical formulas and SEDSCOUR to 2DV/3D RANS, SWASH, CFD–DEM and CNN/LSTM predictors. Continuum models efficiently resolve flow and morphology, particle models expose contacts, and learned models interpolate data but require physical scaling and domain checks.

**Experimental datasets.** Reviewed evidence includes vertical-cylinder current scour, offshore monopile literature, clear-water CFD–DEM validation, complex bridge-pier databases, bridge flumes, monopile/jacket/caisson tests plus four field cases, and biomineralization erosion experiments and demonstrations.

**Validated ranges.** Case-specific results include a 50% depth change when suspended load was omitted, unprotected monopile scour slightly above one diameter, SEDSCOUR use with up to 30% mud, CNN R² 0.85, and MICP reductions of 84–100% under 0.3 m/s currents.

**Recent advances.** Recent advances couple CFD–DEM particle mechanics, validated 3D morphodynamics, multi-structure comparisons, dimensionless deep learning, field-scale biomineralization and lifecycle monitoring to move beyond single-formula equilibrium depth.

**Disagreements.** Equilibrium formulas differ across current-, wave-, combined- and complex-loading regimes; turbulence closure and suspended-load treatment alter results. Maximum force, stress, or drag location need not coincide with deepest scour, and protection performance under one forcing does not establish lifecycle stability.

**Limitations.** Scale effects, unresolved sediment mixtures and cohesion, uncertain bed armoring, complex geometry, unsteady tides and storms, morphodynamic acceleration, limited field duration and protection degradation constrain transfer. Accuracy metrics from trained surrogates do not prove extrapolation.

**Open questions.** Priorities include combined irregular waves/currents, tidal reversals, mixed/cohesive beds, group and jacket interactions, cable/pipeline exposure, climate-driven loading, protection failure, real-time monitoring, uncertainty-aware digital twins and interpretable machine learning.

**Seminal papers.** Classical pier, pipeline and structure experiments established horseshoe-vortex mechanisms and equilibrium scaling; sediment-transport and Exner models enabled time-resolved prediction. Offshore wind growth expanded work toward large monopiles, groups, complex loading and protection.

## Claims

- **C1238.** Scour assessment requires complementary experimental, numerical, and field evidence because no single method resolves onset, transient transport, equilibrium morphology, structural response, and environmental variability across structure types. *Regime: Bridge, pipeline, offshore-wind, and related hydraulic scour problems..* [literature_review_statement, review] (Yee-Meng Chiew 2020, [doi:10.3390/w12061749](https://doi.org/10.3390/w12061749))
- **C1596.** An eleven-node single-hidden-layer neural network trained on 400 laboratory cases outperformed fitted linear and nonlinear regressions for equilibrium pier-scour depth, with pile diameter critical to prediction reliability. *Regime: Artificial Neural Network for Estimation of Local Scour Depth Around Bridge Piers.* [direct_finding, numerical] (Ahmed Ali 2021, [doi:10.2478/heem-2021-0005](https://doi.org/10.2478/heem-2021-0005))
- **C1599.** Three-dimensional finite-element simulations indicate that negative seabed slope and increasing scour depth jointly reduce lateral pile resistance and bending moment by weakening pile-soil interaction. *Regime: Numerical Investigation into the Response of a Laterally Loaded Pile in Coastal and Offshore Slopes Considering Scour Effect.* [direct_finding, numerical] (Hao Zhang 2025, [doi:10.3390/w17132032](https://doi.org/10.3390/w17132032))
- **C1607.** Experiments motivated by tsunami field failures show that nearby structures can amplify local scour under extreme transient flows, so isolated-foundation estimates may be nonconservative. *Regime: SCOUR AMPLIFICATION CAUSED BY STRUCTURE PROXIMITY IN EXTREME FLOWS.* [direct_finding, experimental] (April-LeQuéré 2023, [doi:10.9753/icce.v37.structures.11](https://doi.org/10.9753/icce.v37.structures.11))

## Papers

- Ahmed Ali (2021). Artificial Neural Network for Estimation of Local Scour Depth Around Bridge Piers. *Archives of Hydro-engineering and Environmental Mechanics*. [doi:10.2478/heem-2021-0005](https://doi.org/10.2478/heem-2021-0005) [published version, CC BY-NC-ND](https://www.sciendo.com/pdf/10.2478/heem-2021-0005)
- Hao Zhang (2025). Numerical Investigation into the Response of a Laterally Loaded Pile in Coastal and Offshore Slopes Considering Scour Effect. *Water*. [doi:10.3390/w17132032](https://doi.org/10.3390/w17132032) [published version, CC BY](https://www.mdpi.com/2073-4441/17/13/2032/pdf?version=1751861306)
- April-LeQuéré (2023). SCOUR AMPLIFICATION CAUSED BY STRUCTURE PROXIMITY IN EXTREME FLOWS. *Coastal Engineering Proceedings*. [doi:10.9753/icce.v37.structures.11](https://doi.org/10.9753/icce.v37.structures.11) [published version, CC BY](https://icce-ojs-tamu.tdl.org/icce/article/download/12867/12140)
- Hugues Lantuit (2011). The Arctic Coastal Dynamics Database: A New Classification Scheme and Statistics on Arctic Permafrost Coastlines. *Estuaries and Coasts*. [doi:10.1007/s12237-010-9362-6](https://doi.org/10.1007/s12237-010-9362-6) [published version, read only](https://pure.rug.nl/ws/portalfiles/portal/134757317/The_Arctic_Coastal_Dynamics_Database_A_New_Classification_Scheme_and_Statistics.pdf)
- Cüneyt Baykal (2015). Numerical investigation of flow and scour around a vertical circular cylinder. *Philosophical Transactions of the Royal Society A: Mathematical, Physical and Engineering Sciences*. [doi:10.1098/rsta.2014.0104](https://doi.org/10.1098/rsta.2014.0104) [published version, read only](https://royalsocietypublishing.org/doi/pdf/10.1098/rsta.2014.0104)
- Dawei Guan (2022). Local scour at offshore windfarm monopile foundations: A review. *Water Science and Engineering*. [doi:10.1016/j.wse.2021.12.006](https://doi.org/10.1016/j.wse.2021.12.006) [published version, CC BY-NC-ND](https://api.elsevier.com/content/article/PII:S167423702100123X?httpAccept=text/xml)
- Qin Liu (2022). Local Scour Mechanism of Offshore Wind Power Pile Foundation Based on CFD-DEM. *Journal of Marine Science and Engineering*. [doi:10.3390/jmse10111724](https://doi.org/10.3390/jmse10111724) [published version, CC BY](https://mdpi-res.com/d_attachment/jmse/jmse-10-01724/article_deploy/jmse-10-01724.pdf)
- Ngoc Thi Huynh (2025). A CNN deep learning approach to scour depth estimation around complex bridge piers in steady flow environments. *Advances in Bridge Engineering*. [doi:10.1186/s43251-025-00170-8](https://doi.org/10.1186/s43251-025-00170-8) [published version, CC BY](https://link.springer.com/content/pdf/10.1186/s43251-025-00170-8.pdf)
- Yee-Meng Chiew (2020). Experimental, Numerical and Field Approaches to Scour Research. *Water*. [doi:10.3390/w12061749](https://doi.org/10.3390/w12061749) [published version, CC BY](https://mdpi-res.com/d_attachment/water/water-12-01749/article_deploy/water-12-01749.pdf)
- Haiyang Dong (2025). Study on the Mechanism of Local Scour Around Bridge Piers. *Journal of Marine Science and Engineering*. [doi:10.3390/jmse13061021](https://doi.org/10.3390/jmse13061021) [published version, CC BY](https://mdpi-res.com/d_attachment/jmse/jmse-13-01021/article_deploy/jmse-13-01021.pdf)
- Leo C. van Rijn (2025). Scour near Offshore Monopiles, Jacket-Type and Caisson-Type Structures. *Journal of Marine Science and Engineering*. [doi:10.3390/jmse13020266](https://doi.org/10.3390/jmse13020266) [published version, CC BY](https://mdpi-res.com/d_attachment/jmse/jmse-13-00266/article_deploy/jmse-13-00266.pdf)
- Shan Liu (2025). Recent Developments on Biomineralization for Erosion Control. *Applied Sciences*. [doi:10.3390/app15126591](https://doi.org/10.3390/app15126591) [published version, CC BY](https://mdpi-res.com/d_attachment/applsci/applsci-15-06591/article_deploy/applsci-15-06591.pdf)
