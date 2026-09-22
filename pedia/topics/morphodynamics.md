# Coastal morphodynamics

`morphodynamics` | Coupled flow, sediment, and landform evolution.

Subtopics: [Nearshore bars](morphodynamics.bars.md), [Bedforms](morphodynamics.bedforms.md), [Planform evolution](morphodynamics.planform.md), [Cross-shore profile evolution](morphodynamics.profile.md)

Papers: 17. Claims: 5. Equations: 0.

## Synthesis

**Well established.** Coastal morphology emerges from two-way feedback: waves, currents, tides, wind and gravity move heterogeneous sediment, and the evolving bed redirects those forcings. Bars, bedforms, profiles, dunes and planforms therefore exhibit thresholds, patterns, migration and multiple timescales rather than passive response.

**Governing physics.** Transport depends on bed shear, wave asymmetry, undertow, suspension, bedload, sorting and slope; divergence of transport changes elevation. Feedback can stabilize a form, create an instability, or trigger a state transition, while sediment supply and boundaries constrain long-term trajectories.

**Dimensionless parameters.** Controls include Shields parameter, mobility and suspension numbers, Rouse number, relative depth and wave height, surf similarity, sediment-size ratios, bed-slope and transport-gradient scales, bar spacing relative to surf-zone width, morphological acceleration factor and forcing-to-adjustment timescale ratio.

**Major equations.** The Exner sediment-continuity equation links bed-level change to transport divergence and sources. Hydrodynamic mass, momentum, wave-action or energy equations provide forcing; transport and sorting closures, avalanching, vegetation or aeolian terms complete models. Stability analysis linearizes coupled equations about a base state.

**Typical methods.** Studies combine repeated profiles, lidar, multibeam, seismic and imagery with wave/current/sediment measurements; infer patterns and budgets; use process-based, behavior-oriented or reduced/appropriate-complexity models; and validate migration, elevation, volume, wavelength and transitions rather than shoreline alone.

**Numerical models.** Models range from cross-shore wave–current–profile systems and linear instability theory to coastal-tract and hybrid machine-learning/process models. Numerical stability requires conservative sediment updating and controlled coupling; long-horizon models must retain critical states without resolving every short-scale process.

**Experimental datasets.** Reviewed evidence spans multiweek-to-seasonal sandbar records at Duck, Hasaki and Egmond, three summers of Truc Vert ridge-and-runnel mapping, a five-week Nova Scotia experiment, 2.5 years of monthly foredune lidar, Llobregat multibeam/seismic profiles and laboratory-to-field overwash morphometry.

**Validated ranges.** Case-specific skill for cross-shore bar profiles ranged 0.50–0.88 across four records; oblique-bar theory predicts hour-to-day growth in intermediate states; overwash scaling spans several orders of magnitude. These ranges describe distinct phenomena and are not interchangeable validation metrics.

**Recent advances.** Recent advances use dense lidar and multisensor bathymetry, data-driven transport closures, hybrid models, scale-invariant morphology, coastal-tract systems and explicit appropriate-complexity criteria to bridge event processes and management horizons.

**Disagreements.** Process-rich models may reproduce events but accumulate calibration and forcing error, while reduced models reach management timescales but can omit state changes. A model is not preferable merely because it is more detailed; adequacy depends on the behavior, scale and decision being tested.

**Limitations.** Sparse long records, uncertain sediment supply and grain mixtures, three-dimensionality, storm intermittency, ecological feedback, unresolved small scales, numerical diffusion, parameter equifinality and boundary change limit prediction. Local fit does not prove transfer or century-scale trajectory.

**Open questions.** Priorities include state-transition predictability, mixed-sediment sorting, river-to-coast supply, dune–beach–bar coupling, storm recovery, ecological feedbacks, calibrated acceleration, hybrid-model interpretability and uncertainty-aware long-term ensembles.

**Seminal papers.** Sediment continuity and energetics established profile and shoreline response; stability theory explained rhythmic bars and bedforms as feedback instabilities. Process-based coastal models then coupled waves, currents and transport, followed by behavior-oriented and systems approaches for longer scales.

## Claims

- **C1179.** Coastal morphodynamic prediction should use only the process and system complexity needed to resolve behavior and critical transitions at the management scale, with assumptions tested against observations. *Regime: Decadal-to-centennial coastal and estuarine management questions..* [literature_review_statement, review] (Jon French 2016, [doi:10.1016/j.geomorph.2015.10.005](https://doi.org/10.1016/j.geomorph.2015.10.005))
- **C1367.** A review argues local coastal adaptation requires a new generation of multiscale probabilistic change models integrating mean sea level, surge, waves and river flow because existing models do not supply reliable sub-10-km projections. *Regime: On the need for a new generation of coastal change models for the 21st century.* [literature_review_statement, review] (Roshanka Ranasinghe 2020, [doi:10.1038/s41598-020-58376-x](https://doi.org/10.1038/s41598-020-58376-x))
- **C1621.** Hydrological records and satellite imagery show that the Yellow River Delta gained 248 square kilometres and 36.45 km of coastline from 1983-2011 despite declining runoff and sediment load, with growth, retreat and recovery phases shaped by river regulation, sediment supply and lobe switching. *Regime: Yellow River Delta planform and shoreline evolution from 1983 through 2011..* [direct_finding, field] (Dongxian Kong 2014, [doi:10.1016/j.jhydrol.2014.09.038](https://doi.org/10.1016/j.jhydrol.2014.09.038))
- **C1628.** Northern Adriatic shelf evidence and BarSim modeling show that barrier overstepping probability during rapid transgression decreases with tidal amplitude: preserved systems formed near 60 and 10 mm/yr sea-level rise, while backbarrier accommodation and antecedent topography controlled failure or drowning. *Regime: Two preserved northern Adriatic barrier-lagoon systems during 15-8 ka BP rapid transgression..* [direct_finding, mixed] (J.E.A. Storms 2008, [doi:10.1016/j.quascirev.2008.02.009](https://doi.org/10.1016/j.quascirev.2008.02.009))
- **C1653.** Morphodynamic equilibrium must be specified by Exner sediment-mass conservation and analysis scale: static and two dynamic forms can be mathematically distinct in models, whereas variable forcing and landscape setting often leave real coasts and estuaries only statistical or quasi-equilibrium. *Regime: Coastal, estuarine and river morphodynamics evaluated at an explicitly selected spatial and temporal scale..* [literature_review_statement, review] (Zhou 2016, [doi:10.1016/j.earscirev.2016.12.002](https://doi.org/10.1016/j.earscirev.2016.12.002))

## Papers

- Dongxian Kong (2014). Evolution of the Yellow River Delta and its relationship with runoff and sediment load from 1983 to 2011. *Journal of Hydrology*. [doi:10.1016/j.jhydrol.2014.09.038](https://doi.org/10.1016/j.jhydrol.2014.09.038)
- J.E.A. Storms (2008). Coastal dynamics under conditions of rapid sea-level rise: Late Pleistocene to Early Holocene evolution of barrier–lagoon systems on the northern Adriatic shelf (Italy). *Quaternary Science Reviews*. [doi:10.1016/j.quascirev.2008.02.009](https://doi.org/10.1016/j.quascirev.2008.02.009)
- Roshanka Ranasinghe (2020). On the need for a new generation of coastal change models for the 21st century. *Scientific Reports*. [doi:10.1038/s41598-020-58376-x](https://doi.org/10.1038/s41598-020-58376-x)
- Zhou (2016). Is “Morphodynamic Equilibrium” an oxymoron?. *Earth-Science Reviews*. [doi:10.1016/j.earscirev.2016.12.002](https://doi.org/10.1016/j.earscirev.2016.12.002)
- Evan B. Goldstein (2019). A review of machine learning applications to coastal sediment transport and morphodynamics. *Earth-Science Reviews*. [doi:10.1016/j.earscirev.2019.04.022](https://doi.org/10.1016/j.earscirev.2019.04.022)
- Gerben Ruessink (2007). Modeling cross‐shore sandbar behavior on the timescale of weeks. *Journal of Geophysical Research: Earth Surface*. [doi:10.1029/2006jf000730](https://doi.org/10.1029/2006jf000730)
- Jon French (2016). Appropriate complexity for the prediction of coastal and estuarine geomorphic behaviour at decadal to centennial scales. *Geomorphology*. [doi:10.1016/j.geomorph.2015.10.005](https://doi.org/10.1016/j.geomorph.2015.10.005)
- Stefano Lanzoni (1999). Grain sorting and bar instability. *Journal of Fluid Mechanics*. [doi:10.1017/s0022112099005583](https://doi.org/10.1017/s0022112099005583)
- Francesca Ribas (2003). Nearshore oblique sand bars. *Journal of Geophysical Research: Oceans*. [doi:10.1029/2001jc000985](https://doi.org/10.1029/2001jc000985)
- Katherine Brodie (2019). Spatial Variability of Coastal Foredune Evolution, Part A: Timescales of Months to Years. *Journal of Marine Science and Engineering*. [doi:10.3390/jmse7050124](https://doi.org/10.3390/jmse7050124)
- Eli D. Lazarus (2016). Scaling laws for coastal overwash morphology. *Geophysical Research Letters*. [doi:10.1002/2016gl071213](https://doi.org/10.1002/2016gl071213)
- Roger Úrgeles (2007). Sediment undulations on the Llobregat prodelta: Signs of early slope instability or sedimentary bedforms?. *Journal of Geophysical Research: Solid Earth*. [doi:10.1029/2005jb003929](https://doi.org/10.1029/2005jb003929)
- D. De Melo Apoluceno (2002). Morphodynamics of Ridge and Runnel Systems during Summer. *Journal of Coastal Research*. [doi:10.2112/1551-5036-36.sp1.222](https://doi.org/10.2112/1551-5036-36.sp1.222)
- Andrea Taramelli (2020). Nearshore Sandbar Classification of Sabaudia (Italy) with LiDAR Data: The FHyL Approach. *Remote Sensing*. [doi:10.3390/rs12071053](https://doi.org/10.3390/rs12071053)
- Jaime C. Dawson (2002). Low-energy Morphodynamics of a Ridge and Runnel System. *Journal of Coastal Research*. [doi:10.2112/1551-5036-36.sp1.198](https://doi.org/10.2112/1551-5036-36.sp1.198)
- Evan B. Goldstein (2014). Data-driven components in a model of inner-shelf sorted bedforms: a new hybrid model. *Earth Surface Dynamics*. [doi:10.5194/esurf-2-67-2014](https://doi.org/10.5194/esurf-2-67-2014)
- Yun-Chih Chiang (2010). NUMERICAL SOLUTIONS OF COASTAL MORPHODYNAMIC EVOLUTION FOR COMPLEX TOPOGRAPHY. *Journal of Marine Science and Technology*. [doi:10.51400/2709-6998.1878](https://doi.org/10.51400/2709-6998.1878)
