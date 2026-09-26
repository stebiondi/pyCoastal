# Tsunami generation

`tsunami.generation` | Seismic, landslide, and volcanic sources.

Parent: [Tsunamis and long waves](tsunami.md)

Papers: 19. Claims: 15. Equations: 2.

## Synthesis

**Well established.** Tsunami generation converts rapid displacement of water by fault motion, landslides, volcanic processes or impact into an initial free-surface and velocity field; source geometry, kinematics and coupling determine amplitude, spectrum and directivity before propagation physics acts.

**Governing physics.** Seismic sources deform the seabed through elastic fault slip, while landslides transfer momentum through moving, deforming solid or granular masses; generation depends on displacement rate relative to gravity-wave response, water depth, compressibility or air effects, rheology and bathymetry.

**Dimensionless parameters.** Controls include source length and width relative to depth, displacement-to-depth ratio, rise time over gravity-wave time, slide Froude number, relative slide thickness and density, slope, aspect ratio, submergence, mobility, Mach or compressibility effects where relevant, and normalized wave amplitude.

**Major equations.** Common formulations combine elastic dislocation or prescribed moving-bottom kinematics with shallow-water, Boussinesq, potential-flow or Navier–Stokes equations; landslide models add rigid-body dynamics or continuum rheology and multiphase interface coupling.

**Typical methods.** Workflows construct source geometry and kinematics, choose active moving-bottom or passive initial displacement, test conservation and resolution, validate near-source waves against analytical or laboratory data, propagate ensembles, compare with gauges/runup, and invert observations without hiding nonuniqueness.

**Numerical models.** Model classes include passive and active seismic initialization, kinematic seafloor forcing, depth-integrated landslide source terms, nonhydrostatic and potential models, depth-resolved Navier–Stokes, particle or meshless solvers, and coupled slide–water multiphase methods.

**Experimental datasets.** The reviewed slice includes canonical plane-beach and island tests used with regional seismic scenarios, a corrected two-segment Catania source, and the landslide-model benchmark literature summarized by the focused review; direct volcanic evidence is not yet reviewed.

**Validated ranges.** Current direct evidence is limited to two Eastern Mediterranean seismic scenario formulations and a review-level landslide model taxonomy; source-specific parameter ranges, laboratory scales and transfer to volcanic or impact tsunamis remain incomplete.

**Recent advances.** Recent advances use kinematic nonhydrostatic seafloors, depth-resolved landslide CFD, improved rheology, coupled multiphase solvers, fast surrogate or reduced source ensembles, high-rate geodesy and joint inversion of seismic, pressure, wave and runup observations.

**Disagreements.** Passive initial-surface displacement is efficient but can omit finite rupture and water-column dynamics; active kinematic forcing is more complete but uncertain. Depth-integrated landslide models enable ensembles but miss fine-scale generation, while depth-resolved models add physics at much higher cost.

**Limitations.** Source observations are sparse and inverse solutions nonunique; rupture, rigidity, slide volume, rheology and timing are uncertain; bathymetry filters the generated spectrum; simplified initial conditions may double-count or omit dynamics; and validation often occurs after propagation has mixed source and path errors.

**Open questions.** Priorities include finite-fault and splay rupture, horizontal displacement on slopes, deformable and fragmented slides, volcanic collapse and explosion, air and compressibility, sediment entrainment, source–propagation coupling, real-time inversion and probabilistic multi-mechanism ensembles.

**Seminal papers.** Elastic dislocation theory and passive seafloor-to-surface displacement established seismic initialization; moving-bottom long-wave solutions and laboratory slide-impact scaling established active generation, followed by depth-integrated and multiphase computational models.

## Equations

### Active tsunami-generation continuity equation

$$
\zeta_t + \nabla \cdot (h\mathbf{U}) = \zeta_{b,t}
$$

Regime: Active bottom-displacement option; the regional scenarios used passive free-surface generation.

Variables: `zeta` free-surface elevation; `h` total water depth d+zeta; `U` depth-averaged horizontal velocity vector; `zeta_b` bottom displacement

Source: (Samaras 2015, [doi:10.5194/os-11-643-2015](https://doi.org/10.5194/os-11-643-2015))

### Earthquake magnitude to initial tsunami amplitude

$$
\log_{10} \zeta_0 = 0.98M - 6.92
$$

Regime: Empirical source construction adopted from cited prior work, not newly validated here.

Variables: `zeta_0` initial wave amplitude; `M` mainshock magnitude

Source: (Samaras 2015, [doi:10.5194/os-11-643-2015](https://doi.org/10.5194/os-11-643-2015))

## Claims

- **C17.** The corrected two-segment source has seismic moment 6.41e21 Nm and moment magnitude 7.17 when rigidity is 30 GPa. *Regime: Corrected source definition for the paper's eastern-Sicily scenario; supersedes the original Table 2 caption..* [direct_finding, analytical] (Tinti 2013, [doi:10.5194/nhess-13-1795-2013](https://doi.org/10.5194/nhess-13-1795-2013))
- **C1126.** A landslide-tsunami review distinguishes efficient depth-integrated source models from computationally demanding depth-resolved approaches that represent transient fine-scale multiphase generation physics. *Regime: Numerical Modeling of Generation of Landslide Tsunamis: A Review.* [literature_review_statement, review] (Lee 2022, [doi:10.1142/s1793431122410019](https://doi.org/10.1142/s1793431122410019))
- **C1251.** Landslide-tsunami case studies show that combining marine-geological constraints with fully nonlinear generation and Boussinesq propagation models can reproduce source-to-coast behavior while preserving uncertainty in slide geometry and motion. *Regime: Landslide tsunami case studies using a Boussinesq model and a fully nonlinear tsunami generation model.* [direct_finding, mixed] (Philip Watts 2003, [doi:10.5194/nhess-3-391-2003](https://doi.org/10.5194/nhess-3-391-2003))
- **C1252.** Reconstruction of the 2018 Anak Krakatau event supports lateral collapse into a roughly 250 m deep caldera as the tsunami source and reproduces observed coastal effects, including reported runup locally reaching about 13 m. *Regime: Modelling of the tsunami from the December 22, 2018 lateral collapse of Anak Krakatau volcano in the Sunda Straits, Indonesia.* [direct_finding, mixed] (Stéphan T. Grilli 2019, [doi:10.1038/s41598-019-48327-6](https://doi.org/10.1038/s41598-019-48327-6))
- **C1253.** Marine evidence and tsunami modeling indicate that submarine mass movement may have augmented locally extreme waves during the 2011 Tohoku tsunami, although the relative landslide contribution remains uncertain. *Regime: Did a submarine landslide contribute to the 2011 Tohoku tsunami?.* [direct_finding, mixed] (David R. Tappin 2014, [doi:10.1016/j.margeo.2014.09.043](https://doi.org/10.1016/j.margeo.2014.09.043))
- **C1255.** A comprehensive observational and modeling synthesis for the 1998 Papua New Guinea tsunami supports a submarine-slump source capable of explaining the unusually severe local runup. *Regime: The Papua New Guinea tsunami of 17 July 1998: anatomy of a catastrophic event.* [direct_finding, mixed] (David R. Tappin 2008, [doi:10.5194/nhess-8-243-2008](https://doi.org/10.5194/nhess-8-243-2008))
- **C1257.** Landslide-tsunami generation and impact depend on slide volume, geometry, acceleration and kinematics; available scaling relations organize these controls but do not eliminate source and transfer uncertainty. *Regime: On the characteristics of landslide tsunamis.* [direct_finding, mixed] (Finn Løvholt 2015, [doi:10.1098/rsta.2014.0376](https://doi.org/10.1098/rsta.2014.0376))
- **C1259.** A three-dimensional Navier–Stokes collapse calculation coupled to two-dimensional Boussinesq propagation provides a multiscale framework for estimating the near-field waves from a potential Cumbre Vieja flank collapse. *Regime: Numerical modeling of tsunami waves generated by the flank collapse of the Cumbre Vieja Volcano (La Palma, Canary Islands): Tsunami source and near field effects.* [direct_finding, mixed] (Stéphane Abadie 2012, [doi:10.1029/2011jc007646](https://doi.org/10.1029/2011jc007646))
- **C1261.** Tohoku tsunami simulations show that inferred coastal response is sensitive to both heterogeneous slip distribution and assumed fault geometry, so source-model uncertainty must be propagated into hazard estimates. *Regime: Sensitivity of tsunami wave profiles and inundation simulations to earthquake slip and fault geometry for the 2011 Tohoku earthquake.* [direct_finding, mixed] (Katsuichiro Goda 2014, [doi:10.1186/1880-5981-66-105](https://doi.org/10.1186/1880-5981-66-105))
- **C1549.** Glacial retreat in recent decades has exposed unstable slopes and allowed deep water to extend beneath some of those slopes. *Regime: The study system, forcing, data and methods stated in the indexed abstract..* [direct_finding, mixed] (Bretwood Higman 2018, [doi:10.1038/s41598-018-30475-w](https://doi.org/10.1038/s41598-018-30475-w))
- **C1555.** Abstract. *Regime: The study system, forcing, data and methods stated in the indexed abstract..* [direct_finding, mixed] (H. Gary Greene 2006, [doi:10.5194/nhess-6-63-2006](https://doi.org/10.5194/nhess-6-63-2006))
- **C1604.** A smoothed-particle hydrodynamics sediment model represents deforming soil-mass motion and water coupling for landslide-tsunami generation. *Regime: SEDIMENT MODEL FOR LANDSLIDE TSUNAMIS USING SMOOTHED PARTICLE HYDRODYNAMICS.* [direct_finding, numerical] (Tsurudome 2025, [doi:10.9753/icce.v38.sediment.65](https://doi.org/10.9753/icce.v38.sediment.65))
- **C1644.** SWASH simulations across six water-body geometries show landslide-tsunami far-field decay can be correlated by wavefront length from two-dimensional confinement through three-dimensional spreading; 2D and 3D far-field heights differ by over an order of magnitude, and dispersion matters most for deeper-water Stokes-like waves. *Regime: Far-field landslide-tsunami propagation in constant-depth idealized water bodies spanning confined flumes to unconstrained basins..* [direct_finding, numerical] (Gioele Ruffini 2019, [doi:10.1016/j.coastaleng.2019.103518](https://doi.org/10.1016/j.coastaleng.2019.103518))
- **C1749.** Granular landslide impact generates a rapidly evolving three-phase flow in which slide penetration, flow separation, impact-crater collapse, and air entrainment control the initial impulse wave; non-breaking waves remain approximately irrotational, whereas breaking waves and bores develop strong vorticity. *Regime: Two-dimensional Froude-scaled granular slides impacting still water and generating non-breaking waves, separated crater flows, or dissipative transient bores..* [direct_finding, experimental] (Hermann M. Fritz 2003, [doi:10.1007/s00348-003-0659-0](https://doi.org/10.1007/s00348-003-0659-0))
- **C1751.** For the 2011 Tohoku tsunami, a geodetically inverted three-dimensional finite-element coseismic source with heterogeneous forearc structure reproduced near- and far-field observations better overall than a simpler seismic-inversion source, but accurate extreme coastal runup still required finer bathymetry, topography, and possibly additional generation mechanisms. *Regime: The Mw 9.0 2011 Tohoku-Oki coseismic tsunami from generation through trans-oceanic propagation and inundation along Japan between about 35 and 41 degrees north..* [direct_finding, numerical] (Stéphan T. Grilli 2012, [doi:10.1007/s00024-012-0528-y](https://doi.org/10.1007/s00024-012-0528-y))

## Papers

- Philip Watts (2003). Landslide tsunami case studies using a Boussinesq model and a fully nonlinear tsunami generation model. *Natural Hazards and Earth System Sciences*. [doi:10.5194/nhess-3-391-2003](https://doi.org/10.5194/nhess-3-391-2003) [published version, CC BY](https://nhess.copernicus.org/articles/3/391/2003/nhess-3-391-2003.pdf)
- Stéphan T. Grilli (2019). Modelling of the tsunami from the December 22, 2018 lateral collapse of Anak Krakatau volcano in the Sunda Straits, Indonesia. *Scientific Reports*. [doi:10.1038/s41598-019-48327-6](https://doi.org/10.1038/s41598-019-48327-6) [published version, CC BY](https://www.nature.com/articles/s41598-019-48327-6)
- David R. Tappin (2014). Did a submarine landslide contribute to the 2011 Tohoku tsunami?. *Marine Geology*. [doi:10.1016/j.margeo.2014.09.043](https://doi.org/10.1016/j.margeo.2014.09.043) [published version, CC BY](https://api.elsevier.com/content/article/PII:S0025322714002898?httpAccept=text/xml)
- David R. Tappin (2008). The Papua New Guinea tsunami of 17 July 1998: anatomy of a catastrophic event. *Natural Hazards and Earth System Sciences*. [doi:10.5194/nhess-8-243-2008](https://doi.org/10.5194/nhess-8-243-2008) [published version, CC BY-NC-SA](https://nhess.copernicus.org/articles/8/243/2008/nhess-8-243-2008.pdf)
- Finn Løvholt (2015). On the characteristics of landslide tsunamis. *Philosophical Transactions of the Royal Society A: Mathematical, Physical and Engineering Sciences*. [doi:10.1098/rsta.2014.0376](https://doi.org/10.1098/rsta.2014.0376) [published version, CC BY](https://royalsocietypublishing.org/doi/pdf/10.1098/rsta.2014.0376)
- Stéphane Abadie (2012). Numerical modeling of tsunami waves generated by the flank collapse of the Cumbre Vieja Volcano (La Palma, Canary Islands): Tsunami source and near field effects. *Journal of Geophysical Research: Oceans*. [doi:10.1029/2011jc007646](https://doi.org/10.1029/2011jc007646) [submitted manuscript, read only](https://hal.science/hal-01744811v1/file/JGR_complet.pdf)
- Hermann M. Fritz (2003). Landslide generated impulse waves.. *Experiments in Fluids*. [doi:10.1007/s00348-003-0659-0](https://doi.org/10.1007/s00348-003-0659-0) [published version, read only](https://link.springer.com/content/pdf/10.1007/s00348-003-0659-0.pdf)
- Stéphan T. Grilli (2012). Numerical Simulation of the 2011 Tohoku Tsunami Based on a New Transient FEM Co-seismic Source: Comparison to Far- and Near-Field Observations. *Pure and Applied Geophysics*. [doi:10.1007/s00024-012-0528-y](https://doi.org/10.1007/s00024-012-0528-y) [submitted manuscript, CC BY](https://webpages.sdsmt.edu/~eduke/New%20folder/publications/2013GrilliPAGEOH.pdf)
- Katsuichiro Goda (2014). Sensitivity of tsunami wave profiles and inundation simulations to earthquake slip and fault geometry for the 2011 Tohoku earthquake. *Earth, Planets and Space*. [doi:10.1186/1880-5981-66-105](https://doi.org/10.1186/1880-5981-66-105) [published version, CC BY](http://link.springer.com/content/pdf/10.1186/1880-5981-66-105.pdf)
- Gioele Ruffini (2019). Numerical modelling of landslide-tsunami propagation in a wide range of idealised water body geometries. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2019.103518](https://doi.org/10.1016/j.coastaleng.2019.103518) [accepted manuscript, read only](https://iris.uniroma1.it/bitstream/11573/1493187/4/Ruffini_Numerical-modelling-landslide_2019.pdf)
- Lee (2022). Numerical Modeling of Generation of Landslide Tsunamis: A Review. *Journal of Earthquake and Tsunami*. [doi:10.1142/s1793431122410019](https://doi.org/10.1142/s1793431122410019)
- Tsurudome (2025). SEDIMENT MODEL FOR LANDSLIDE TSUNAMIS USING SMOOTHED PARTICLE HYDRODYNAMICS. *Coastal Engineering Proceedings*. [doi:10.9753/icce.v38.sediment.65](https://doi.org/10.9753/icce.v38.sediment.65) [published version, CC BY](https://icce-ojs-tamu.tdl.org/icce/article/download/14446/13718)
- Valentin Heller (2007). Scale effects in subaerial landslide generated impulse waves. *Experiments in Fluids*. [doi:10.1007/s00348-007-0427-7](https://doi.org/10.1007/s00348-007-0427-7) [published version, read only](https://link.springer.com/content/pdf/10.1007/s00348-007-0427-7.pdf)
- Bretwood Higman (2018). The 2015 landslide and tsunami in Taan Fiord, Alaska. *Scientific Reports*. [doi:10.1038/s41598-018-30475-w](https://doi.org/10.1038/s41598-018-30475-w) [published version, CC BY](https://www.nature.com/articles/s41598-018-30475-w.pdf)
- Denys Dutykh (2011). The VOLNA code for the numerical modeling of tsunami waves: Generation, propagation and inundation. *European Journal of Mechanics - B/Fluids*. [doi:10.1016/j.euromechflu.2011.05.005](https://doi.org/10.1016/j.euromechflu.2011.05.005) [preprint, read only](https://arxiv.org/pdf/1002.4553)
- H. Gary Greene (2006). Submarine landslides in the Santa Barbara Channel as potential tsunami sources. *Natural hazards and earth system sciences*. [doi:10.5194/nhess-6-63-2006](https://doi.org/10.5194/nhess-6-63-2006) [published version, CC BY-NC-SA](https://nhess.copernicus.org/articles/6/63/2006/nhess-6-63-2006.pdf)
- Ataie‐Ashtiani (2007). A higher‐order Boussinesq‐type model with moving bottom boundary: applications to submarine landslide tsunami waves. *International Journal for Numerical Methods in Fluids*. [doi:10.1002/fld.1354](https://doi.org/10.1002/fld.1354)
- Samaras (2015). Simulation of tsunami generation, propagation and coastal inundation in the Eastern Mediterranean. *Ocean Science*. [doi:10.5194/os-11-643-2015](https://doi.org/10.5194/os-11-643-2015) [published version, CC BY](https://os.copernicus.org/articles/11/643/2015/os-11-643-2015.pdf)
- Helge Fuchs (2010). Impulse wave run-over: experimental benchmark study for numerical modelling. *Experiments in Fluids*. [doi:10.1007/s00348-010-0836-x](https://doi.org/10.1007/s00348-010-0836-x) [published version, read only](https://link.springer.com/content/pdf/10.1007/s00348-010-0836-x.pdf)
