# Nearshore bars

`morphodynamics.bars` | Bar formation and migration.

Parent: [Coastal morphodynamics](morphodynamics.md)

Papers: 18. Claims: 16. Equations: 7.

## Synthesis

**Well established.** Nearshore bars are dynamic sediment reservoirs whose growth, decay and migration emerge from feedback among wave breaking, undertow, nonlinear wave-driven onshore transport, sediment availability and evolving bathymetry; they need not remain coupled to a fixed break point.

**Governing physics.** Energetic waves and undertow commonly drive bar growth and offshore migration, while milder asymmetric waves favor onshore recovery. Settling, suspension, bedload, wave groups, infragravity motions, profile slope, depth-dependent forcing and morphology-controlled breaking modify this balance.

**Dimensionless parameters.** Important controls include H/h breaking ratio, Shields mobility, Dean or fall-velocity parameter, relative bar depth and height, bar concentration, profile slope, nourishment concentration and relative placement, relative lifetime Ln/Tr, transport asymmetry, and normalized model errors.

**Major equations.** Core formulations combine sediment continuity (Exner), wave action and breaking, transport closures partitioning onshore wave-asymmetry and offshore undertow effects, equilibrium-bar volume or position laws, breakpoint criteria based on wave-height-to-depth ratio, and PCA/EOF decompositions for migration cycles.

**Typical methods.** Methods include repeated bathymetric profiles, Argus or remote sensing, wave-current arrays, large mobile-bed flumes, sediment-flux reconstruction, morphometric tracking, process-based modeling, equilibrium reduced models, PCA/EOF separation, and multi-site hindcast validation.

**Numerical models.** Models include cross-shore transport-balance calculations, COAST2D with overtopping, an equilibrium two-bar volume model, PCA nourishment-lifetime separation, breakpoint diagnostics, and nonhydrostatic XBeach variants whose simplified bar-crest breaking can bias landward waves and morphology.

**Experimental datasets.** Evidence includes two breakpoint field experiments, three CIEM large-scale erosive-accretive datasets, a 15 x 30 m overtopping basin, ten years of 12 km Terschelling bathymetry, sixteen Dutch profile datasets with 21 nourishments, and Duck plus two feeder-mound sites.

**Validated ranges.** Explicit regimes include a 2 million m3 nourishment and 6-7 year migration arrest; a 1:15-style large-flume class with three datasets; 21 nourishments and bar-cycle periods of 1-15 years; Sea Palling's nine breakwaters; and outer/inner-bar errors epsilon=0.39/0.51 and NMSE=0.24/0.29.

**Recent advances.** Recent work separates nourishment interference from natural cycles across many sites and uses fast equilibrium models for multi-bar and feeder-mound evolution, while explicit model comparisons identify why transient inner bars and landward-of-crest hydrodynamics remain less predictable.

**Disagreements.** Field evidence rejects universal fixed-breakpoint coupling. Erosive offshore evolution follows a comparatively consistent height-location relation, whereas accretive onshore migration may decay or persist. Individual nourishment variables do not explain lifetime, but joint design-and-system variables have moderate skill.

**Limitations.** Bars are three-dimensional, path dependent and site specific. Annual profiles alias events, laboratory recovery evidence is sparse, PCA can mix modes near inlets or trends, equilibrium models simplify inner bars, and depth-averaged wave models may misrepresent crest breaking and turbulence.

**Open questions.** Priorities include prediction of inner-bar and accretive recovery, uncertainty propagation from wave boundary layers to decadal migration, three-dimensional rhythmicity, nourishment and structure interactions, climate-driven cycle changes, and consistent validation across event and management scales.

**Seminal papers.** The 1989 breakpoint test established that bars can evolve landward of initial breaking. The 2005 Terschelling study quantified multi-year nourishment arrest, while later large-scale experiments separated robust erosive behavior from non-unique accretive modes.

## Equations

### break-point hypothesis test

$$
\frac{\partial z_b}{\partial t}+\frac{1}{1-p}\frac{\partial q_s}{\partial x}=0
$$

Regime: Two field experiments with coincident cross-surf-zone waves and evolving nearshore bars; inner-surf-zone edge diagnosed from wave-height-to-depth ratio.

Variables: `zb` bed elevation; `p` bed porosity; `qs` cross-shore sediment transport rate; normalized Exner representation

Source: (Sallenger 1989, [doi:10.1016/0378-3839(89)90009-4](https://doi.org/10.1016/0378-3839(89)90009-4))

### Terschelling bar morphometric and transport-balance analysis

$$
\frac{\partial z_b}{\partial t}+\frac{1}{1-p}\frac{\partial q_s}{\partial x}=0
$$

Regime: Terschelling, Netherlands; 12 km alongshore bathymetry for 10 years after a 1993 nourishment placed between middle and outer bars.

Variables: `zb` bed elevation; `p` bed porosity; `qs` cross-shore sediment transport rate; normalized Exner representation

Source: (Grunnet 2005, [doi:10.1016/j.coastaleng.2004.09.006](https://doi.org/10.1016/j.coastaleng.2004.09.006))

### COAST2D overtopping morphodynamic model

$$
\frac{\partial z_b}{\partial t}+\frac{1}{1-p}\frac{\partial q_s}{\partial x}=0
$$

Regime: Validation in a 15 x 30 m basin with a 5 m trapezoidal breakwater on a 1:20 beach; November 2006 storm at Sea Palling with nine segmented breakwaters.

Variables: `zb` bed elevation; `p` bed porosity; `qs` cross-shore sediment transport rate; normalized Exner representation

Source: (Du 2010, [doi:10.1016/j.coastaleng.2010.04.005](https://doi.org/10.1016/j.coastaleng.2010.04.005))

### erosive-accretive breaker-bar evolution parameterization

$$
\frac{\partial z_b}{\partial t}+\frac{1}{1-p}\frac{\partial q_s}{\partial x}=0
$$

Regime: Three CIEM large-scale morphodynamic datasets with more than 20 cross-shore water-level locations per experiment, compared with additional large-scale profile datasets.

Variables: `zb` bed elevation; `p` bed porosity; `qs` cross-shore sediment transport rate; normalized Exner representation

Source: (Sonja Eichentopf 2018, [doi:10.1016/j.coastaleng.2018.04.010](https://doi.org/10.1016/j.coastaleng.2018.04.010))

### PCA shoreface-nourishment lifetime model

$$
\frac{\partial z_b}{\partial t}+\frac{1}{1-p}\frac{\partial q_s}{\partial x}=0
$$

Regime: Sixteen Dutch profile datasets and 21 nourishments; annual profiles from 1965-2017, typically spaced 200-250 m; global bar-cycle return periods cited as 1-15 years.

Variables: `zb` bed elevation; `p` bed porosity; `qs` cross-shore sediment transport rate; normalized Exner representation

Source: (Gijsman 2019, [doi:10.1016/j.coastaleng.2019.103521](https://doi.org/10.1016/j.coastaleng.2019.103521))

### equilibrium-based two-bar volume model

$$
\frac{\partial z_b}{\partial t}+\frac{1}{1-p}\frac{\partial q_s}{\partial x}=0
$$

Regime: Duck, North Carolina two-bar system plus feeder mounds at Silver Strand, California and Cocoa Beach, Florida; years-to-decades scale.

Variables: `zb` bed elevation; `p` bed porosity; `qs` cross-shore sediment transport rate; normalized Exner representation

Source: (Marinho 2020, [doi:10.1016/j.coastaleng.2020.103722](https://doi.org/10.1016/j.coastaleng.2020.103722))

### IBW-PAN multi-bar process framework

$$
\frac{\partial z_b}{\partial t}+\frac{1}{1-p}\frac{\partial q_s}{\partial x}=0
$$

Regime: Natural mildly sloping multiple-bar sandy shore at Lubiatowo, Poland, with D50 approximately 0.22 mm.

Variables: `zb` bed elevation; `p` bed porosity; `qs` cross-shore sediment transport rate; normalized Exner representation

Source: (Kaczmarek 2005, [doi:10.1016/j.ecss.2004.09.006](https://doi.org/10.1016/j.ecss.2004.09.006))

## Claims

- **C251.** After a 2 million m3 Terschelling shoreface nourishment filled the middle-to-outer-bar trough, the monitored 12 km bar system developed pronounced three-dimensionality and its migration stopped for 6-7 years; migration then resumed at the autonomous rate as trough deepening restored the pre-nourishment cross-shore transport distribution. *Regime: Terschelling, Netherlands; 12 km alongshore bathymetry for 10 years after a 1993 nourishment placed between middle and outer bars..* [direct_finding, mixed] (Grunnet 2005, [doi:10.1016/j.coastaleng.2004.09.006](https://doi.org/10.1016/j.coastaleng.2004.09.006))
- **C252.** In one of two field experiments, a nearshore bar became better developed and migrated offshore while remaining landward of initial outer-surf-zone breaking, demonstrating that bar development and migration are not necessarily coupled to the break point; the second experiment could not exclude break-point influence. *Regime: Two field experiments with coincident cross-surf-zone waves and evolving nearshore bars; inner-surf-zone edge diagnosed from wave-height-to-depth ratio..* [direct_finding, field] (Sallenger 1989, [doi:10.1016/0378-3839(89)90009-4](https://doi.org/10.1016/0378-3839(89)90009-4))
- **C253.** For the mildly sloping, wave-dominated multi-bar coast at Lubiatowo with D50 approximately 0.22 mm, the reviewed IBW-PAN program shows that physical modeling and field-data analysis provide complementary constraints on wave-current sediment transport and bar evolution rather than interchangeable evidence. *Regime: Natural mildly sloping multiple-bar sandy shore at Lubiatowo, Poland, with D50 approximately 0.22 mm..* [literature_review_statement, review] (Kaczmarek 2005, [doi:10.1016/j.ecss.2004.09.006](https://doi.org/10.1016/j.ecss.2004.09.006))
- **C254.** Across three large-scale experiments and supporting datasets, breaker-bar height varied linearly with offshore position under erosive waves, whereas subsequent accretive onshore migration followed two distinct modes—decaying or non-decaying—depending on feedback between morphology, wave breaking location, and sediment transport. *Regime: Three CIEM large-scale morphodynamic datasets with more than 20 cross-shore water-level locations per experiment, compared with additional large-scale profile datasets..* [direct_finding, experimental] (Sonja Eichentopf 2018, [doi:10.1016/j.coastaleng.2018.04.010](https://doi.org/10.1016/j.coastaleng.2018.04.010))
- **C255.** For laboratory tests on a 1:20 beach and the November 2006 Sea Palling storm around nine segmented breakwaters, COAST2D agreed with measured hydrodynamics and morphological change only when structure overtopping was represented; overtopping materially altered circulation, sediment transport, and predicted bed change. *Regime: Validation in a 15 x 30 m basin with a 5 m trapezoidal breakwater on a 1:20 beach; November 2006 storm at Sea Palling with nine segmented breakwaters..* [direct_finding, mixed] (Du 2010, [doi:10.1016/j.coastaleng.2010.04.005](https://doi.org/10.1016/j.coastaleng.2010.04.005))
- **C256.** For 21 shoreface nourishments isolated from natural migration using PCA on 16 long-term Dutch profile datasets, no individual design parameter explained lifetime; bar-cycle return period alone gave r2=0.41, while a joint linear model reached r2=0.67 with positive effects of nourishment concentration and depth and negative effects of bar concentration and cycle period. *Regime: Sixteen Dutch profile datasets and 21 nourishments; annual profiles from 1965-2017, typically spaced 200-250 m; global bar-cycle return periods cited as 1-15 years..* [direct_finding, field] (Gijsman 2019, [doi:10.1016/j.coastaleng.2019.103521](https://doi.org/10.1016/j.coastaleng.2019.103521))
- **C257.** In years-to-decades validation at Duck, the equilibrium-based two-bar model predicted outer-bar volume more skillfully (epsilon=0.39, NMSE=0.24) than the more transient inner bar (epsilon=0.51, NMSE=0.29), and reproduced feeder-mound decay at two other sites by assigning artificial bars zero equilibrium volume. *Regime: Duck, North Carolina two-bar system plus feeder mounds at Silver Strand, California and Cocoa Beach, Florida; years-to-decades scale..* [direct_finding, numerical] (Marinho 2020, [doi:10.1016/j.coastaleng.2020.103722](https://doi.org/10.1016/j.coastaleng.2020.103722))
- **C1177.** Across Duck, Hasaki and Egmond cases lasting 10 days to 3.5 months, a coupled cross-shore model achieved profile skill of 0.50–0.88 and reproduced storm-driven offshore and skewness/bedload-driven onshore sandbar migration. *Regime: Modeling cross‐shore sandbar behavior on the timescale of weeks.* [direct_finding, mixed] (Gerben Ruessink 2007, [doi:10.1029/2006jf000730](https://doi.org/10.1029/2006jf000730))
- **C1180.** Linear stability analysis indicates sediment heterogeneity damps alternate-bar growth and migration, shortens wavelength, and reproduces qualitative coarse-grain accumulation at bar crests relative to uniform sediment. *Regime: Grain sorting and bar instability.* [direct_finding, mixed] (Stefano Lanzoni 1999, [doi:10.1017/s0022112099005583](https://doi.org/10.1017/s0022112099005583))
- **C1181.** Surf-zone feedback under oblique waves can generate up- or down-current rhythmic bars with spacing near to several times surf-zone width and e-folding growth times from hours to days in intermediate beach states. *Regime: Nearshore oblique sand bars.* [direct_finding, mixed] (Francesca Ribas 2003, [doi:10.1029/2001jc000985](https://doi.org/10.1029/2001jc000985))
- **C1185.** Three summers of Truc Vert mapping describe a four-phase ridge-and-runnel cycle from nearshore-bar formation through shoreward welding and organization, with rhythmic systems migrating southward alongshore. *Regime: Morphodynamics of Ridge and Runnel Systems during Summer.* [direct_finding, mixed] (D. De Melo Apoluceno 2002, [doi:10.2112/1551-5036-36.sp1.222](https://doi.org/10.2112/1551-5036-36.sp1.222))
- **C1186.** During five low-energy weeks, 0.35–0.50 m ridges moved less than 5 m; landward wave transport was balanced by undertow, tidal currents, along-trough transport and ebb drainage-channel export. *Regime: Low-energy Morphodynamics of a Ridge and Runnel System.* [direct_finding, mixed] (Jaime C. Dawson 2002, [doi:10.2112/1551-5036-36.sp1.198](https://doi.org/10.2112/1551-5036-36.sp1.198))
- **C1187.** FHyL fusion of hyperspectral imagery, lidar and in-situ spectra classified shallow Sabaudia sandbars using depth, slope, convexity and concavity and supported an operational coastal-data standard. *Regime: Nearshore Sandbar Classification of Sabaudia (Italy) with LiDAR Data: The FHyL Approach.* [direct_finding, mixed] (Andrea Taramelli 2020, [doi:10.3390/rs12071053](https://doi.org/10.3390/rs12071053))
- **C1343.** A process-based model reproduces onshore sandbar migration only when velocity and acceleration skewness act jointly; velocity-skewness bed stress dominates shoaling while acceleration-skewness pressure gradients dominate inner-surf-zone transport. *Regime: Onshore sandbar migration in the surf zone: New insights into the wave‐induced sediment transport mechanisms.* [direct_finding, mixed] (Àngels Fernández-Mora 2015, [doi:10.1002/2014gl063004](https://doi.org/10.1002/2014gl063004))
- **C1766.** On a high-energy macro-tidal beach, outer-bar state responds to cumulative disequilibrium rather than individual storms: sustained energetic waves drive offshore/upstate transitions, whereas several months of low energy are needed for onshore/downstate recovery because the bar is active only around low tide. *Regime: Double-barred, high-energy, shore-normally forced macro-tidal Perranporth beach, southwest England, observed over 15-16 years with detailed surveys over two years..* [direct_finding, field] (Gerd Masselink 2014, [doi:10.1016/j.geomorph.2014.07.025](https://doi.org/10.1016/j.geomorph.2014.07.025))
- **C1769.** In the linear alternate-bar model, sediment heterogeneity produces an overall stabilizing effect through weaker longitudinal transport response, stronger transverse stabilizing transport, and sorting-induced damping; preferential coarsening upstream of bar crests reduces bar growth and migration and shortens wavelength relative to uniform sediment. *Regime: Incipient alternate bars in a wide straight channel with cohesionless heterogeneous bedload, depth-averaged two-dimensional flow, small topographic and grain-size perturbations, and negligible suspended load; the worked mechanism comparison uses beta=15, mean Shields parameter 0.08, dimensionless mean grain size 0.001, and geometric sorting spread 2..* [direct_finding, analytical] (Stefano Lanzoni 1999, [doi:10.1017/s0022112099005583](https://doi.org/10.1017/s0022112099005583))

## Papers

- Gerd Masselink (2014). Role of wave forcing, storms and NAO in outer bar dynamics on a high-energy, macro-tidal beach. *Geomorphology*. [doi:10.1016/j.geomorph.2014.07.025](https://doi.org/10.1016/j.geomorph.2014.07.025) [submitted manuscript, read only](http://hdl.handle.net/10026.1/3093)
- Gerben Ruessink (2007). Modeling cross‐shore sandbar behavior on the timescale of weeks. *Journal of Geophysical Research: Earth Surface*. [doi:10.1029/2006jf000730](https://doi.org/10.1029/2006jf000730) [published version, read only](https://onlinelibrary.wiley.com/doi/pdfdirect/10.1029/2006JF000730)
- Àngels Fernández-Mora (2015). Onshore sandbar migration in the surf zone: New insights into the wave‐induced sediment transport mechanisms. *Geophysical Research Letters*. [doi:10.1002/2014gl063004](https://doi.org/10.1002/2014gl063004) [published version, read only](https://onlinelibrary.wiley.com/doi/pdfdirect/10.1002/2014GL063004)
- Grunnet (2005). Morphodynamic response of nearshore bars to a shoreface nourishment. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2004.09.006](https://doi.org/10.1016/j.coastaleng.2004.09.006) [accepted manuscript, read only](https://www.researchgate.net/publication/222552385_Morphodynamic_response_of_nearshore_bars_to_a_shoreface_nourishment)
- Stefano Lanzoni (1999). Grain sorting and bar instability. *Journal of Fluid Mechanics*. [doi:10.1017/s0022112099005583](https://doi.org/10.1017/s0022112099005583) [submitted manuscript, read only](https://www.research.unipd.it/bitstream/11577/128705/1/Lanzoni_Tubino_JFM99.pdf)
- Francesca Ribas (2003). Nearshore oblique sand bars. *Journal of Geophysical Research: Oceans*. [doi:10.1029/2001jc000985](https://doi.org/10.1029/2001jc000985) [submitted manuscript, CC BY-NC-ND](https://upcommons.upc.edu/bitstreams/ac877939-adad-4223-bae6-8bf323100c2c/download)
- Sallenger (1989). Nearshore bars and the break-point hypothesis. *Coastal Engineering*. [doi:10.1016/0378-3839(89)90009-4](https://doi.org/10.1016/0378-3839(89)90009-4)
- Kaczmarek (2005). Selected problems of sediment transport and morphodynamics of a multi-bar nearshore zone. *Estuarine, Coastal and Shelf Science*. [doi:10.1016/j.ecss.2004.09.006](https://doi.org/10.1016/j.ecss.2004.09.006)
- Sonja Eichentopf (2018). Breaker bar morphodynamics under erosive and accretive wave conditions in large-scale experiments. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2018.04.010](https://doi.org/10.1016/j.coastaleng.2018.04.010) [submitted manuscript, CC BY-NC-ND](https://hdl.handle.net/10044/1/58915)
- Du (2010). Modelling the effect of wave overtopping on nearshore hydrodynamics and morphodynamics around shore-parallel breakwaters. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2010.04.005](https://doi.org/10.1016/j.coastaleng.2010.04.005)
- D. De Melo Apoluceno (2002). Morphodynamics of Ridge and Runnel Systems during Summer. *Journal of Coastal Research*. [doi:10.2112/1551-5036-36.sp1.222](https://doi.org/10.2112/1551-5036-36.sp1.222) [published version, read only](https://bioone.org/journals/Journal-of-Coastal-Research-JCR/volume-36/issue-sp1/1551-5036-36.sp1.222/Morphodynamics-of-Ridge-and-Runnel-Systems-during-Summer/10.2112/1551-5036-36.sp1.222.pdf)
- Andrea Taramelli (2020). Nearshore Sandbar Classification of Sabaudia (Italy) with LiDAR Data: The FHyL Approach. *Remote Sensing*. [doi:10.3390/rs12071053](https://doi.org/10.3390/rs12071053) [published version, CC BY](https://mdpi-res.com/d_attachment/remotesensing/remotesensing-12-01053/article_deploy/remotesensing-12-01053.pdf)
- Jaime C. Dawson (2002). Low-energy Morphodynamics of a Ridge and Runnel System. *Journal of Coastal Research*. [doi:10.2112/1551-5036-36.sp1.198](https://doi.org/10.2112/1551-5036-36.sp1.198) [published version, read only](https://bioone.org/journals/journal-of-coastal-research/volume-36/issue-sp1/1551-5036-36.sp1.198/Low-energy-Morphodynamics-of-a-Ridge-and-Runnel-System/10.2112/1551-5036-36.sp1.198.pdf)
- Gijsman (2019). The lifetime of shoreface nourishments in fields with nearshore sandbar migration. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2019.103521](https://doi.org/10.1016/j.coastaleng.2019.103521)
- Marinho (2020). Cross-shore modelling of multiple nearshore bars at a decadal scale. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2020.103722](https://doi.org/10.1016/j.coastaleng.2020.103722) [open copy, read only](https://ria.ua.pt/bitstream/10773/36970/1/Cross-shore%20modelling%20of%20multiple%20nearshore%20bars%20at%20a%20decadal%20scale.pdf)
- A. Pacheco (2014). Retrieval of nearshore bathymetry from Landsat 8 images: A tool for coastal monitoring in shallow waters. *Remote Sensing of Environment*. [doi:10.1016/j.rse.2014.12.004](https://doi.org/10.1016/j.rse.2014.12.004) [published version, read only](https://www.sciencedirect.com/science/article/pii/S0034425714004878)
- Shari L. Gallop (2020). Geologically controlled sandy beaches: Their geomorphology, morphodynamics and classification. *The Science of The Total Environment*. [doi:10.1016/j.scitotenv.2020.139123](https://doi.org/10.1016/j.scitotenv.2020.139123) [published version, read only](https://ars.els-cdn.com/content/image/1-s2.0-S0048969720326401-ga1_lrg.jpg)
- Elsayed (2022). Nonhydrostatic Numerical Modeling of Fixed and Mobile Barred Beaches: Limitations of Depth-Averaged Wave Resolving Models around Sandbars. *Journal of Waterway, Port, Coastal, and Ocean Engineering*. [doi:10.1061/(asce)ww.1943-5460.0000685](https://doi.org/10.1061/(asce)ww.1943-5460.0000685) [published version, CC BY](https://ascelibrary.org/doi/pdf/10.1061/%28ASCE%29WW.1943-5460.0000685)
