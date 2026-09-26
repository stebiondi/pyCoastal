# Tropical cyclone flooding

`storm_surge.hurricanes` | Hurricane and tropical cyclone applications.

Parent: [Storm surge and coastal flooding](storm_surge.md)

Papers: 18. Claims: 11. Equations: 3.

## Synthesis

**Well established.** Tropical-cyclone coastal flooding depends on the evolving storm track, wind and pressure fields, shelf and coastal geometry, tides, waves, and terrain; peak surge alone does not describe early rise, duration, inundation, or wave-driven contributions.

**Governing physics.** Wind stress and pressure deficit force surge; storm radius, translation speed, and approach angle control forcing duration and orientation; Coriolis and shelf geometry contribute to forerunner setup; wave radiation stress, runup, and topography modify nearshore water levels and inundation.

**Dimensionless parameters.** Useful nondimensional controls include drag coefficient, pressure-scaled surge, wind-duration-scaled lead time, normalized hydrograph time and amplitude, relative surge to tide and wave components, and normalized validation errors; none removes dependence on shelf and coastal geometry.

**Major equations.** Core formulations include depth-integrated shallow-water momentum and continuity, quadratic wind stress, spectral wave-action and radiation-stress coupling, dimensionless pressure-duration forerunner scaling, level-minus-terrain inundation depth, PCA/CNN spatial reconstruction, and beta-mixture hydrograph templates.

**Typical methods.** Typical workflows hindcast or simulate cyclone ensembles with ADCIRC and spectral waves, validate water levels and high-water marks, isolate tide/surge/wave components, derive reduced scaling or machine-learning models, and map resulting water surfaces over high-resolution terrain.

**Numerical models.** Models include ADCIRC coupled to WAM, STWAVE, or SWAN; MIKE 21 and XBeach for component-resolved inundation; RDM with Zero-Point Boundary mapping; C1PKNet for peak-field surrogacy; and k-means plus beta mixtures for temporal surge templates.

**Experimental datasets.** Reviewed evidence includes Katrina and Rita regional observations, Iota inundation and profile reconstructions, three US synthetic forerunner ensembles with Ike and Harvey, 1031 Chesapeake simulations plus three historical storms, Haiyan survey limits over 5 m terrain, and two decades of US ADCIRC hydrographs.

**Validated ranges.** Validation remains regional: Katrina high-water marks were mostly reproduced within 0.5 m; the Ike forerunner range was 0.4-2.8 m predicted versus 0.4-2.6 m observed at 24-6 h lead; and Haiyan inundation-limit accuracy was 81% on a 5 m terrain grid. These are not global error bounds.

**Recent advances.** Recent advances learn track-to-peak mappings from large ensembles, validate high-resolution typhoon inundation maps, and compress complete surge evolution into eight physically interpretable temporal templates, moving hazard analysis beyond isolated peak values.

**Disagreements.** Peak-focused surrogates are efficient for spatial hazard fields, whereas forerunner and hydrograph studies show that lead time, duration, skewness, and delayed peaks are separate engineering quantities. Likewise, surge-only inundation can be accurate in one metric yet omit wave setup, swash, rainfall, or river contributions important elsewhere.

**Limitations.** Limitations include uncertain drag at extreme winds, grid-dependent wave setup, sparse observations, synthetic-storm sampling, omitted compound sources, static terrain assumptions, region-specific machine learning, and normalized templates that may not transfer to other basins or climate states.

**Open questions.** Priorities are transferable spatiotemporal surrogates with calibrated uncertainty, joint surge-wave-tide-rain-river validation, evolving topography and sea level, observation-based hydrograph typologies, operational forerunner verification, and error propagation from atmospheric forcing to local inundation and decisions.

**Seminal papers.** Within this screened slice, the 2009 Katrina-Rita coupled validation establishes a physics-based regional benchmark, and the 2019 forerunner study reframes pre-landfall rise as a forecast quantity distinct from peak surge.

## Equations

### Parametric tropical-cyclone radial wind profile

$$
V(r)=\frac{V_{max} 2R_{mw}r}{R_{mw}^2+r^2}
$$

Regime: Symmetric gradient-level synthetic and hypothetical cyclone winds subsequently corrected to asymmetric surface winds.

Variables: `V(r)` gradient wind speed at radius r; `Vmax` maximum sustained one-minute wind; `Rmw` radius of maximum wind; `r` radial distance

Source: (Wilmer Rey 2021, [doi:10.3389/fmars.2021.766258](https://doi.org/10.3389/fmars.2021.766258))

### Dimensionless forerunner-surge scaling

$$
\Pi_\eta=\mathcal{F}(\Pi_t;\,\Delta p,R,V_f)
$$

Regime: Synthetic storms at Virginia, New York-New Jersey, and Texas model domains.

Variables: `Pi_eta` central-pressure-scaled forerunner surge; `Pi_t` wind-duration-scaled time; `Delta p` central pressure deficit; `R` storm radius; `V_f` forward translation speed

Source: (Liu 2019, [doi:10.1016/j.coastaleng.2019.01.005](https://doi.org/10.1016/j.coastaleng.2019.01.005))

### Two-component beta-mixture surge template

$$
\hat{\eta}(\tau)=wB(\tau;\alpha_1,\beta_1)+(1-w)B(\tau;\alpha_2,\beta_2)
$$

Regime: Representative normalized hydrographs derived from the US ADCIRC hindcast archive.

Variables: `eta_hat` normalized surge hydrograph; `tau` normalized event time; `B` beta density-shaped component; `w` mixture weight; `alpha_i,beta_i` shape parameters

Source: (Alipour 2026, [doi:10.1016/j.coastaleng.2026.105086](https://doi.org/10.1016/j.coastaleng.2026.105086))

## Claims

- **C167.** C1PKNet used complete tropical-cyclone track time series and 1031 Chesapeake Bay simulations to predict spatial peak surge rapidly, with evaluation against Hurricanes Isabel, Irene, and Sandy; transfer beyond the trained storm and coastal-state space remains unverified. *Regime: Chesapeake Bay and the landfalling/bypassing storm distributions represented in the training database..* [direct_finding, numerical] (Lee 2021, [doi:10.1016/j.coastaleng.2021.104024](https://doi.org/10.1016/j.coastaleng.2021.104024))
- **C168.** A pressure- and wind-duration-scaled method predicted Hurricane Ike forerunner surge 24-6 h before landfall as 0.4-2.8 m, compared with 0.4-2.6 m observed, and indicated that larger storms moving more slowly favor larger early surge. *Regime: The Virginia, New York-New Jersey, and Texas regional ensembles and storms comparable to their parameter ranges..* [direct_finding, mixed] (Liu 2019, [doi:10.1016/j.coastaleng.2019.01.005](https://doi.org/10.1016/j.coastaleng.2019.01.005))
- **C169.** For Typhoon Haiyan in Tacloban, the RDM plus Zero-Point Boundary method on a 5 m terrain model identified surveyed inundation-limit locations with 81% accuracy, but the simulation omitted compound flooding. *Regime: The Haiyan hindcast, eastern Leyte terrain, and surveyed Tacloban water limits..* [direct_finding, mixed] (Zerrudo 2024, [doi:10.1016/j.tcrr.2024.11.001](https://doi.org/10.1016/j.tcrr.2024.11.001))
- **C170.** Two decades of US ADCIRC hindcasts yielded eight normalized tropical-cyclone surge hydrograph types; Gulf cases were more diverse, and storm size, speed, approach angle, peak proximity, and bathymetric slope interacted without any single factor explaining all shape variability. *Regime: The US Gulf and Atlantic hindcast archive and its normalized hydrograph definitions..* [direct_finding, numerical] (Alipour 2026, [doi:10.1016/j.coastaleng.2026.105086](https://doi.org/10.1016/j.coastaleng.2026.105086))
- **C1282.** Synthetic hurricanes coupled to SLOSH produce a heavy-tailed surge-height distribution at the Battery; peaks-over-threshold generalized-Pareto estimates give New York return periods consistent with other regional studies. *Regime: Risk assessment of hurricane storm surge for New York City.* [direct_finding, numerical] (Ning Lin 2010, [doi:10.1029/2009jd013630](https://doi.org/10.1029/2009jd013630))
- **C1286.** End-century simulations of 21 historical U.S. hurricanes increased inundation volume for 14 storms and extent for 13, averaging +36% and +25%; no single storm property explained the locally complex changes. *Regime: Projected Climate Change Impacts on Hurricane Storm Surge Inundation in the Coastal United States.* [direct_finding, numerical] (Jeane Camelo 2020, [doi:10.3389/fbuil.2020.588049](https://doi.org/10.3389/fbuil.2020.588049))
- **C1532.** Coral reefs can provide significant coastal protection benefits to people and property. *Regime: The study system, forcing, data and methods stated in the indexed abstract..* [direct_finding, mixed] (Michael W. Beck 2018, [doi:10.1038/s41467-018-04568-z](https://doi.org/10.1038/s41467-018-04568-z))
- **C1533.** One of the most destructive natural hazards, tropical cyclone (TC)-induced coastal flooding, will worsen under climate change. *Regime: The study system, forcing, data and methods stated in the indexed abstract..* [direct_finding, mixed] (Reza Marsooli 2019, [doi:10.1038/s41467-019-11755-z](https://doi.org/10.1038/s41467-019-11755-z))
- **C1536.** Tropical cyclone damage potential, as currently defined by the Saffir-Simpson scale and the maximum sustained surface wind speed in the storm, fails to consider the area impact of winds likely to force surge and waves or cause particular levels of damage. *Regime: The study system, forcing, data and methods stated in the indexed abstract..* [literature_review_statement, mixed] (Mark D. Powell 2007, [doi:10.1175/bams-88-4-513](https://doi.org/10.1175/bams-88-4-513))
- **C1538.** Abstract A century ago, meteorologists regarded tropical cyclones as shallow vortices, extending upward only a few kilometers into the troposphere, and nothing was known about their physics save that convection was somehow involved. *Regime: The study system, forcing, data and methods stated in the indexed abstract..* [literature_review_statement, mixed] (Kerry Emanuel 2018, [doi:10.1175/amsmonographs-d-18-0016.1](https://doi.org/10.1175/amsmonographs-d-18-0016.1))
- **C1689.** For Bay of Bengal super cyclone TC05B, a parametric cyclone wind field embedded in blended background winds drives POM surge with peak water levels to the right of the track and coastal setup controlled by asymmetric wind stress, onshore Ekman transport, and basin-perimeter propagation. *Regime: Bay of Bengal response to the 1999 TC05B track and forcing, without tide or river-discharge coupling..* [direct_finding, numerical] (Yashvant Das 2015, [doi:10.1007/s40808-015-0067-5](https://doi.org/10.1007/s40808-015-0067-5))

## Papers

- Ning Lin (2010). Risk assessment of hurricane storm surge for New York City. *Journal of Geophysical Research: Atmospheres*. [doi:10.1029/2009jd013630](https://doi.org/10.1029/2009jd013630) [published version, read only](https://onlinelibrary.wiley.com/doi/pdfdirect/10.1029/2009JD013630)
- Lee (2021). Rapid prediction of peak storm surge from tropical cyclone track time series using machine learning. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2021.104024](https://doi.org/10.1016/j.coastaleng.2021.104024) [published version, read only](https://api.elsevier.com/content/article/PII:S0378383921001691?httpAccept=text/xml)
- Jeane Camelo (2020). Projected Climate Change Impacts on Hurricane Storm Surge Inundation in the Coastal United States. *Frontiers in Built Environment*. [doi:10.3389/fbuil.2020.588049](https://doi.org/10.3389/fbuil.2020.588049) [published version, CC BY](https://www.frontiersin.org/articles/10.3389/fbuil.2020.588049/full)
- Yashvant Das (2015). Development of tropical cyclone wind field for simulation of storm surge/sea surface height using numerical ocean model. *Modeling Earth Systems and Environment*. [doi:10.1007/s40808-015-0067-5](https://doi.org/10.1007/s40808-015-0067-5) [published version, CC BY](https://link.springer.com/content/pdf/10.1007/s40808-015-0067-5.pdf)
- Liu (2019). Characterization and prediction of tropical cyclone forerunner surge. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2019.01.005](https://doi.org/10.1016/j.coastaleng.2019.01.005) [published version, read only](https://api.elsevier.com/content/article/PII:S0378383918301224?httpAccept=text/xml)
- Zerrudo (2024). Hindcasting the typhoon haiyan storm surge in coastal eastern leyte. *Tropical Cyclone Research and Review*. [doi:10.1016/j.tcrr.2024.11.001](https://doi.org/10.1016/j.tcrr.2024.11.001) [published version, CC BY-NC-ND](https://api.elsevier.com/content/article/PII:S2225603224000559?httpAccept=text/xml)
- Alipour (2026). Characterization of tropical cyclone surge evolution. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2026.105086](https://doi.org/10.1016/j.coastaleng.2026.105086)
- Michael W. Beck (2018). The global flood protection savings provided by coral reefs. *Nature Communications*. [doi:10.1038/s41467-018-04568-z](https://doi.org/10.1038/s41467-018-04568-z) [published version, CC BY](https://www.nature.com/articles/s41467-018-04568-z.pdf)
- Bunya (2010). A High-Resolution Coupled Riverine Flow, Tide, Wind, Wind Wave, and Storm Surge Model for Southern Louisiana and Mississippi. Part I: Model Development and Validation. *Monthly Weather Review*. [doi:10.1175/2009mwr2906.1](https://doi.org/10.1175/2009mwr2906.1) [published version, read only](https://journals.ametsoc.org/downloadpdf/journals/mwre/138/2/2009mwr2906.1.pdf)
- Reza Marsooli (2019). Climate change exacerbates hurricane flood hazards along US Atlantic and Gulf Coasts in spatially varying patterns. *Nature Communications*. [doi:10.1038/s41467-019-11755-z](https://doi.org/10.1038/s41467-019-11755-z) [published version, CC BY](https://www.nature.com/articles/s41467-019-11755-z.pdf)
- Mark D. Powell (2007). Tropical Cyclone Destructive Potential by Integrated Kinetic Energy. *Bulletin of the American Meteorological Society*. [doi:10.1175/bams-88-4-513](https://doi.org/10.1175/bams-88-4-513) [published version, read only](https://journals.ametsoc.org/downloadpdf/journals/bams/88/4/bams-88-4-513.pdf)
- Félix Santiago-Collazo (2019). A comprehensive review of compound inundation models in low-gradient coastal watersheds. *Environmental Modelling & Software*. [doi:10.1016/j.envsoft.2019.06.002](https://doi.org/10.1016/j.envsoft.2019.06.002) [published version, read only](https://www.sciencedirect.com/science/article/am/pii/S1364815219302853)
- Kerry Emanuel (2018). 100 Years of Progress in Tropical Cyclone Research. *Meteorological Monographs*. [doi:10.1175/amsmonographs-d-18-0016.1](https://doi.org/10.1175/amsmonographs-d-18-0016.1) [submitted manuscript, CC BY-NC](https://dspace.mit.edu/bitstream/1721.1/128460/2/amsmonographs-d-18-0016.1.pdf)
- Xiaolong Yu (2017). Effects of wave-current interaction on storm surge in the Taiwan Strait: Insights from Typhoon Morakot. *Continental Shelf Research*. [doi:10.1016/j.csr.2017.08.009](https://doi.org/10.1016/j.csr.2017.08.009) [submitted manuscript, read only](https://ueaeprints.uea.ac.uk/id/eprint/64582/1/Accepted_manuscript.pdf)
- Wilmer Rey (2021). Hurricane Flood Hazard Assessment for the Archipelago of San Andres, Providencia and Santa Catalina, Colombia. *Frontiers in Marine Science*. [doi:10.3389/fmars.2021.766258](https://doi.org/10.3389/fmars.2021.766258) [published version, CC BY](https://www.frontiersin.org/articles/10.3389/fmars.2021.766258/pdf)
- Yuanchi Xiao (2019). The development and evolution of the Burdekin River estuary freshwater plume during Cyclone Debbie (2017). *Estuarine Coastal and Shelf Science*. [doi:10.1016/j.ecss.2019.04.037](https://doi.org/10.1016/j.ecss.2019.04.037) [submitted manuscript, read only](https://unsworks.unsw.edu.au/bitstreams/60df5c18-d0a4-4702-aa30-a9f58a4633c1/download)
- MIMURA (2010). Effectivity of Storm Surge - Wave Hindcasting Coupling Model on Estimation of Storm Surge at T7010. *Journal of Japan Society of Civil Engineers, Ser. B2 (Coastal Engineering)*. [doi:10.2208/kaigan.66.216](https://doi.org/10.2208/kaigan.66.216) [published version, read only](https://www.jstage.jst.go.jp/article/kaigan/66/1/66_1_216/_pdf)
- Bunya (2008). Hurricane Katrina Storm Surge Hindcast Using a Coupled Storm Surge, Wind Wave and Tidal Current Model on an Unstructured Grid. *PROCEEDINGS OF COASTAL ENGINEERING, JSCE*. [doi:10.2208/proce1989.55.316](https://doi.org/10.2208/proce1989.55.316) [published version, read only](https://www.jstage.jst.go.jp/article/proce1989/55/0/55_0_316/_pdf)
