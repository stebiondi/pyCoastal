# Suspended sediment transport

`sediment.suspended` | Suspension and advection.

Parent: [Sediment transport](sediment.md)

Papers: 20. Claims: 12. Equations: 5.

## Synthesis

**Well established.** Suspended coastal sediment is governed by entrainment, three-dimensional advection, turbulent diffusion, settling and deposition; net flux depends on the timing and spatial structure of concentration relative to currents, waves, breakers, swash, and basin oscillations.

**Governing physics.** Core mechanisms are turbulence-driven pickup, settling lag, concentration adaptation, wave-current boundary-layer mixing, plunging-jet vortices, wave-backwash interaction, seiche advection, density or wind-driven circulation, and erosion-deposition feedback with the bed.

**Dimensionless parameters.** Important controls include suspension number or Rouse-type settling-to-mixing ratios, Shields mobility, relative settling velocity, wave-current ratio, sediment diffusivity to eddy-viscosity ratio, relative depth, breaker type, wave-group ratio, and hydrodynamic versus concentration-adjustment time and length scales.

**Major equations.** The common framework is an advection-diffusion-settling equation for concentration with erosion or reference-concentration and deposition boundary conditions, coupled to hydrodynamics ranging from shallow-water exact solutions to quasi-3-D asymptotics and three-dimensional or RANS flow solvers.

**Typical methods.** Methods combine optical or acoustic concentration measurements, pump or trap sampling, mobile-bed flumes, event-resolved flux analysis, exact and asymptotic solutions, characteristics and finite differences, RANS turbulence closure, VOF interface tracking, and comparisons among depth-averaged, 2DV, and 3-D models.

**Numerical models.** Reviewed models include a full 3-D split characteristics/finite-difference transport solver, a quasi-3-D asymptotic adjustment model, exact Lagrangian seiche solutions, and a 2-D RANS k-epsilon/VOF breaker model with advection-diffusion concentration.

**Experimental datasets.** Evidence includes lightweight-sediment laboratory dispersion, a large-flume 1:15 mobile beach under monochromatic, bichromatic, long-wave and random forcing, plunging-breaker turbulence and concentration measurements, and paired-tray two-way sediment flux at turbid Great Barrier Reef sites.

**Validated ranges.** Explicit ranges include six-run, approximately 2.4 h conditions on a 1:15 flume beach and reef two-way fluxes of 34 to more than 640 g m-2 d-1 with net sedimentation below 122 g m-2 d-1. Other studies report regime definitions but accessible sources do not expose universal numerical bounds.

**Recent advances.** Later work resolves plunging-jet turbulence and near-surface concentration and links event-scale wave-backwash interactions to profile response, while field flux methods distinguish gross two-way delivery from net sedimentation.

**Disagreements.** Reduced models can agree with 2DV and 3-D solutions inside their adjustment-scale validity domain, yet depth-averaged models are unreliable in strongly three-dimensional flows. Nominally accretive wave forcing does not necessarily imply shoreward suspended transport.

**Limitations.** Controlled experiments and idealized geometries dominate; concentration boundary conditions and turbulent diffusivity remain uncertain, cohesive and mixed sediments are underrepresented, fine mesh may be required near plunging jets, and delivery measurements do not equal net accumulation.

**Open questions.** Priorities are transferable entrainment and deposition closures, coherent treatment of cohesive mixtures and flocculation, three-dimensional irregular-breaker validation, coupled bed evolution, uncertainty-aware sensor calibration, and field tests that close suspended mass budgets.

**Seminal papers.** The 1988 full 3-D scheme and 1992 quasi-3-D wave-current theory established numerical and reduced-order foundations; the 2003 exact seiche solutions clarified settling-lag redistribution and provide reproducible benchmarks.

## Equations

### three-dimensional suspended-particulate transport model

$$
\frac{\partial c}{\partial t}+\nabla\cdot(\mathbf{u}c)=\nabla\cdot(\mathbf{K}\nabla c)-w_s\frac{\partial c}{\partial z}+S_e-S_d
$$

Regime: Complex three-dimensional coastal flows; tested with hypothetical cases and laboratory transport and dispersal of lightweight sediment.

Variables: `c` suspended sediment concentration; `u` flow velocity; `K` sediment diffusivity tensor; `ws` settling velocity; `Se` erosion or entrainment source; `Sd` deposition sink; normalized governing form

Source: (O'Connor 1988, [doi:10.1016/0378-3839(88)90003-8](https://doi.org/10.1016/0378-3839(88)90003-8))

### quasi-3-D wave-current suspended-transport model

$$
\frac{\partial c}{\partial t}+\nabla\cdot(\mathbf{u}c)=\nabla\cdot(\mathbf{K}\nabla c)-w_s\frac{\partial c}{\partial z}+S_e-S_d
$$

Regime: Logarithmic velocity profile with wave effects represented through diffusivity and the near-bed boundary condition; applicability bounded by a wave-modified suspension parameter and forcing-change scales.

Variables: `c` suspended sediment concentration; `u` flow velocity; `K` sediment diffusivity tensor; `ws` settling velocity; `Se` erosion or entrainment source; `Sd` deposition sink; normalized governing form

Source: (Katopodi 1992, [doi:10.1016/0378-3839(92)90006-g](https://doi.org/10.1016/0378-3839(92)90006-g))

### wave-backwash suspended-flux event framework

$$
\frac{\partial c}{\partial t}+\nabla\cdot(\mathbf{u}c)=\nabla\cdot(\mathbf{K}\nabla c)-w_s\frac{\partial c}{\partial z}+S_e-S_d
$$

Regime: Large flume; handmade 1:15 initial slope; each condition approximately 2.4 h in six runs; erosive and accretive wave series.

Variables: `c` suspended sediment concentration; `u` flow velocity; `K` sediment diffusivity tensor; `ws` settling velocity; `Se` erosion or entrainment source; `Sd` deposition sink; normalized governing form

Source: (Cáceres 2016, [doi:10.1016/j.coastaleng.2015.11.004](https://doi.org/10.1016/j.coastaleng.2015.11.004))

### exact seiche suspended-transport solution

$$
\frac{\partial c}{\partial t}+\nabla\cdot(\mathbf{u}c)=\nabla\cdot(\mathbf{K}\nabla c)-w_s\frac{\partial c}{\partial z}+S_e-S_d
$$

Regime: Idealized elliptical or circular basin with parabolic cross-section; coarse-sand-oriented erosion/deposition law; friction omitted from the hydrodynamic solution.

Variables: `c` suspended sediment concentration; `u` flow velocity; `K` sediment diffusivity tensor; `ws` settling velocity; `Se` erosion or entrainment source; `Sd` deposition sink; normalized governing form

Source: (Pritchard 2003, [doi:10.1016/s0378-3839(03)00046-2](https://doi.org/10.1016/s0378-3839(03)00046-2))

### RANS-VOF plunging-breaker suspended-transport model

$$
\frac{\partial c}{\partial t}+\nabla\cdot(\mathbf{u}c)=\nabla\cdot(\mathbf{K}\nabla c)-w_s\frac{\partial c}{\partial z}+S_e-S_d
$$

Regime: Two-dimensional surf-zone plunging breakers; advection-diffusion concentration with reference-concentration bottom boundary; selected fine mesh resolution.

Variables: `c` suspended sediment concentration; `u` flow velocity; `K` sediment diffusivity tensor; `ws` settling velocity; `Se` erosion or entrainment source; `Sd` deposition sink; normalized governing form

Source: (Ontowirjo 2008, [doi:10.1142/s0578563408001867](https://doi.org/10.1142/s0578563408001867))

## Claims

- **C243.** Where coastal suspended transport is governed by three-dimensional flow patterns such as harbour-entrance separation or wind and density currents, depth-averaged models can give unreliable siltation and erosion estimates; a split characteristics/finite-difference solution of the full 3-D advection-diffusion equation performed well in hypothetical and lightweight-sediment laboratory tests. *Regime: Complex three-dimensional coastal flows; tested with hypothetical cases and laboratory transport and dispersal of lightweight sediment..* [direct_finding, mixed] (O'Connor 1988, [doi:10.1016/0378-3839(88)90003-8](https://doi.org/10.1016/0378-3839(88)90003-8))
- **C244.** In large-flume tests starting from a 1:15 mobile-bed slope and lasting about 2.4 h per condition, all erosive wave cases caused shoreline retreat and a breakpoint bar, but not every nominally accretive case transported sediment shoreward; suspended flux was governed by the occurrence and number of wave-backwash interactions within a wave group. *Regime: Large flume; handmade 1:15 initial slope; each condition approximately 2.4 h in six runs; erosive and accretive wave series..* [direct_finding, experimental] (Cáceres 2016, [doi:10.1016/j.coastaleng.2015.11.004](https://doi.org/10.1016/j.coastaleng.2015.11.004))
- **C245.** Within a quasi-3-D formulation using a logarithmic velocity profile and wave-modified diffusivity and near-bed concentration, adding waves substantially increased suspended load and its adjustment time and length scales while enlarging the model's validity region; results agreed with 2DV/3-D solutions and existing measurements. *Regime: Logarithmic velocity profile with wave effects represented through diffusivity and the near-bed boundary condition; applicability bounded by a wave-modified suspension parameter and forcing-change scales..* [direct_finding, mixed] (Katopodi 1992, [doi:10.1016/0378-3839(92)90006-g](https://doi.org/10.1016/0378-3839(92)90006-g))
- **C246.** For exact fundamental seiche modes in parabolic elliptical and circular basins, settling lag generated net suspended-sediment transport from deeper toward shallower regions; the mode-specific erosion and deposition patterns were robust to the transport-law formulation and little affected by omission of hydrodynamic friction. *Regime: Idealized elliptical or circular basin with parabolic cross-section; coarse-sand-oriented erosion/deposition law; friction omitted from the hydrodynamic solution..* [direct_finding, analytical] (Pritchard 2003, [doi:10.1016/s0378-3839(03)00046-2](https://doi.org/10.1016/s0378-3839(03)00046-2))
- **C247.** For experimentally tested strong plunging breakers, a fine-grid 2-D RANS k-epsilon/VOF model with an advection-diffusion sediment equation reproduced the overturning jet and high near-surface concentration and agreed with measured surface elevation, velocity, turbulent kinetic energy, eddy viscosity, and suspended concentration. *Regime: Two-dimensional surf-zone plunging breakers; advection-diffusion concentration with reference-concentration bottom boundary; selected fine mesh resolution..* [direct_finding, mixed] (Ontowirjo 2008, [doi:10.1142/s0578563408001867](https://doi.org/10.1142/s0578563408001867))
- **C379.** A review of internal-solitary-wave sediment transport identifies bottom-boundary-layer currents and turbulence as widespread resuspension drivers, while emphasizing Reynolds mismatch, grid resolution, and quadratic-stress parameterization as primary limits on laboratory and field-scale prediction. *Regime: Continental-margin internal solitary waves and their bottom boundary layers..* [literature_review_statement, review] (Leon Boegman 2018, [doi:10.1146/annurev-fluid-122316-045049](https://doi.org/10.1146/annurev-fluid-122316-045049))
- **C1642.** Near-bed field cospectra on a non-barred shoreface show wind-wave and swell suspended transport was predominantly onshore and strengthened with shoaling, while undertow transport was offshore and dominated where oscillatory components were weak; breaking introduced strong vertical and temporal variability. *Regime: Marine non-barred shoreface under wind waves, swell, group-bound long waves and undertow during the field campaign..* [direct_finding, field] (Philip D. Osborne 1992, [doi:10.1016/0025-3227(92)90052-j](https://doi.org/10.1016/0025-3227(92)90052-j))
- **C1646.** Field data from three experiments on two beaches show onshore suspended transport under large shear stress in relatively deep, gently sloping water, but increasingly strong breaking and undertow drive offshore transport in shallower or steeper surf zones; a nondimensional flux index captures the transition. *Regime: Two-dimensional barred and gently sloping surf zones represented by three field experiments on two beaches..* [direct_finding, field] (Troels Aagaard 2002, [doi:10.1016/s0025-3227(02)00193-7](https://doi.org/10.1016/s0025-3227(02)00193-7))
- **C1663.** Without mean flow, oscillating-grid turbulence resuspends consolidated sediment according to a nonlinear interaction among consolidation time, particle size, canopy density and flexibility: sparse flexible canopies enhance turbulence and resuspension relative to rigid ones, while dense flexible canopies suppress both. *Regime: Consolidated synthetic, lake and saltmarsh sediment beds beneath modeled submerged rigid, semi-rigid and flexible canopies without mean flow..* [direct_finding, experimental] (Jordi Colomer 2019, [doi:10.1007/s10652-019-09685-x](https://doi.org/10.1007/s10652-019-09685-x))
- **C1666.** After Three Gorges Dam closure, the upper Changjiang changed from the dominant sediment source to a sink, lakes and the eroding middle-lower bed became sources, and estuarine shoals and landward marine transport gained importance, increasing future estuary-erosion sensitivity to further dams, storms and sea level. *Regime: Changjiang river-estuary depositional system before and after closure of the Three Gorges Dam in 2003..* [direct_finding, field] (Zhijun Dai 2018, [doi:10.1016/j.jhydrol.2018.09.019](https://doi.org/10.1016/j.jhydrol.2018.09.019))
- **C1695.** For idealized Punta Umbria tidal conditions, adding sea waves increased modeled suspended-sediment concentration and transport despite reducing the wave–current resultant velocity, because wave orbital motion raised maximum bed shear; cohesive sediment remained vertically mixed while non-cohesive sediment concentrated near the bed. *Regime: Idealized tidal currents, seabeds and wave conditions derived from measurements at Punta Umbria, Huelva, Spain..* [direct_finding, numerical] (Pilar Díaz-Carrasco 2019, [doi:10.1016/j.csr.2019.06.008](https://doi.org/10.1016/j.csr.2019.06.008))
- **C1760.** Tidal sediment delivery in creek-dissected mangroves shifts from creek-dominated routing at lower tides toward sheet flow at high tides; sheltered forest interiors become effective sediment sinks, but trapping capacity declines with sediment starvation, forest loss, and deeper inundation combined with lower vegetation density. *Regime: An elevated, creek-dissected mangrove forest in the Trang River estuary on Thailand's Andaman coast, evaluated over individual tides and instantaneous environmental perturbations..* [direct_finding, mixed] (Erik Horstman 2014, [doi:10.1016/j.geomorph.2014.08.011](https://doi.org/10.1016/j.geomorph.2014.08.011))

## Papers

- Zhijun Dai (2018). Fluvial sediment transfer in the Changjiang (Yangtze) river-estuary depositional system. *Journal of Hydrology*. [doi:10.1016/j.jhydrol.2018.09.019](https://doi.org/10.1016/j.jhydrol.2018.09.019) [accepted manuscript, read only](https://eprints.soton.ac.uk/425047/1/HYDROL_S_18_02211.pdf)
- Leon Boegman (2018). Sediment Resuspension and Transport by Internal Solitary Waves. *Annual Review of Fluid Mechanics*. [doi:10.1146/annurev-fluid-122316-045049](https://doi.org/10.1146/annurev-fluid-122316-045049) [published version, CC BY](https://www.annualreviews.org/doi/pdf/10.1146/annurev-fluid-122316-045049)
- Philip D. Osborne (1992). Frequency dependent cross-shore suspended sediment transport. 1. A non-barred shoreface. *Marine Geology*. [doi:10.1016/0025-3227(92)90052-j](https://doi.org/10.1016/0025-3227(92)90052-j) [published version, read only](https://utoronto.scholaris.ca/bitstreams/aef0c579-ceb5-458a-87cd-5cfe436847d9/download)
- Erik Horstman (2014). Tidal-scale flow routing and sedimentation in mangrove forests: Combining field data and numerical modelling. *Geomorphology*. [doi:10.1016/j.geomorph.2014.08.011](https://doi.org/10.1016/j.geomorph.2014.08.011) [published version, read only](https://www.sciencedirect.com/science/article/pii/S0169555X1400419X)
- Troels Aagaard (2002). Cross-shore suspended sediment transport in the surf zone: a field-based parameterization. *Marine Geology*. [doi:10.1016/s0025-3227(02)00193-7](https://doi.org/10.1016/s0025-3227(02)00193-7) [published version, read only](https://utoronto.scholaris.ca/bitstreams/23a2459a-214f-403d-a4dd-fab07b68385f/download)
- O'Connor (1988). A three-dimensional model of suspended particulate sediment transport. *Coastal Engineering*. [doi:10.1016/0378-3839(88)90003-8](https://doi.org/10.1016/0378-3839(88)90003-8)
- Cáceres (2016). Suspended sediment transport and beach dynamics induced by monochromatic conditions, long waves and wave groups. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2015.11.004](https://doi.org/10.1016/j.coastaleng.2015.11.004) [submitted manuscript, CC BY-NC-ND](https://upcommons.upc.edu/bitstreams/7779623e-1223-4cef-a11c-20ef17a02247/download)
- Katopodi (1992). Quasi-3D modelling of suspended sediment transport by currents and waves. *Coastal Engineering*. [doi:10.1016/0378-3839(92)90006-g](https://doi.org/10.1016/0378-3839(92)90006-g)
- Anon. (2012). A Field-Based Technique for Measuring Sediment Flux on Coral Reefs: Application to Turbid Reefs on the Great Barrier Reef. *Journal of Coastal Research*. [doi:10.2112/jcoastres-d-11-00171.1](https://doi.org/10.2112/jcoastres-d-11-00171.1) [published version, read only](https://researchonline.jcu.edu.au/23609/1/23609-browne-et-al-2012.pdf)
- Jordi Colomer (2019). Consolidated sediment resuspension in model vegetated canopies. *Environmental Fluid Mechanics*. [doi:10.1007/s10652-019-09685-x](https://doi.org/10.1007/s10652-019-09685-x) [submitted manuscript, read only](https://eprints.lancs.ac.uk/id/eprint/132313/1/Colomer_et_al_2019_EFM_accepted.pdf)
- Pritchard (2003). Suspended sediment transport under seiches in circular and elliptical basins. *Coastal Engineering*. [doi:10.1016/s0378-3839(03)00046-2](https://doi.org/10.1016/s0378-3839(03)00046-2) [published version, read only](https://people.maths.bris.ac.uk/~maajh/PDFPapers/CoastalSeiches.pdf)
- Pilar Díaz-Carrasco (2019). Non-cohesive and cohesive sediment transport due to tidal currents and sea waves: A case study. *Continental Shelf Research*. [doi:10.1016/j.csr.2019.06.008](https://doi.org/10.1016/j.csr.2019.06.008) [accepted manuscript, read only](https://digibug.ugr.es/bitstream/10481/95129/1/PAPER_CSR_2019_Non%20cohesive%20and%20cohesive%20sediment%20transport%20due%20to%20tidal%20currents%20and%20sea%20waves_A%20case%20study-1.pdf)
- Ontowirjo (2008). A Turbulent and Suspended Sediment Transport Model for Plunging Breakers. *Coastal Engineering Journal*. [doi:10.1142/s0578563408001867](https://doi.org/10.1142/s0578563408001867)
- Xavier Bertin (2018). Infragravity waves: From driving mechanisms to impacts. *Earth-Science Reviews*. [doi:10.1016/j.earscirev.2018.01.002](https://doi.org/10.1016/j.earscirev.2018.01.002) [accepted manuscript, read only](https://pure.plymouth.ac.uk/ws/portalfiles/portal/39461244/IG_Paper.pdf)
- Yining Chen (2018). Differential sediment trapping abilities of mangrove and saltmarsh vegetation in a subtropical estuary. *Geomorphology*. [doi:10.1016/j.geomorph.2018.06.018](https://doi.org/10.1016/j.geomorph.2018.06.018) [accepted manuscript, read only](https://eprints.soton.ac.uk/422058/1/GEOMOR_7016R2_1_.pdf)
- Linlin Li (2012). Numerical modeling of the morphological change in Lhok Nga, west Banda Aceh, during the 2004 Indian Ocean tsunami: understanding tsunami deposits using a forward modeling method. *Natural Hazards*. [doi:10.1007/s11069-012-0325-z](https://doi.org/10.1007/s11069-012-0325-z) [published version, read only](https://link.springer.com/content/pdf/10.1007/s11069-012-0325-z.pdf)
- Luis G. Egea (2023). Loss of POC and DOC on seagrass sediments by hydrodynamics. *The Science of The Total Environment*. [doi:10.1016/j.scitotenv.2023.165976](https://doi.org/10.1016/j.scitotenv.2023.165976) [submitted manuscript, CC BY-NC-ND](https://rodin.uca.es/bitstream/10498/31221/1/S0048969723046016.pdf)
- Vasileios Kitsikoudis (2020). Experimental analysis of flow and turbulence in the wake of neighboring emergent vegetation patches with different densities. *Environmental Fluid Mechanics*. [doi:10.1007/s10652-020-09746-6](https://doi.org/10.1007/s10652-020-09746-6) [published version, read only](https://link.springer.com/content/pdf/10.1007/s10652-020-09746-6.pdf)
- Anon. (2014). MODELING WAVE DAMPING AND SEDIMENT TRANSPORT WITHIN A PATCH OF VEGETATION. **. [doi:10.9753/icce.v34.sediment.17](https://doi.org/10.9753/icce.v34.sediment.17) [published version, read only](https://journals.tdl.org/icce/index.php/icce/article/download/7175/pdf_470)
- KAWANISHI (2007). Effects of Wind on Salinity Intrusion and Sediment Transport in Ohtagawa Estuary. *PROCEEDINGS OF COASTAL ENGINEERING, JSCE*. [doi:10.2208/proce1989.54.396](https://doi.org/10.2208/proce1989.54.396) [published version, read only](https://www.jstage.jst.go.jp/article/proce1989/54/0/54_0_396/_pdf)
