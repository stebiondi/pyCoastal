# Breakwaters

`structures.breakwaters` | Detached, attached, and floating breakwaters.

Parent: [Coastal structures](structures.md)

Papers: 10. Claims: 7. Equations: 3.

Used by pyCoastal design modules: Breakwater design.

## Synthesis

**Well established.** Breakwaters protect coasts and ports by reflecting, diffracting, dissipating, and transmitting incident-wave energy. Their performance cannot be reduced to wave-height attenuation alone: armour and toe stability, overtopping, foundation response, lee-side spectra, navigation, morphology, maintenance, and cost interact.

**Governing physics.** Key processes include refraction and diffraction around heads and gaps, reflection from structures and beaches, transmission through and over permeable or low crests, depth-limited breaking, bottom friction, wave-current interaction, armour-unit motion, toe scour, settlement, and lee-side sediment redistribution.

**Dimensionless parameters.** Important controls include relative freeboard Rc/Hs, relative crest width, relative depth h/Hs, stability number Hs/(Delta Dn50), damage level, Iribarren number, directional spread, relative wavelength and gap, porosity, structure-height-to-depth ratio, toe geometry, and layout-to-shoreline ratios.

**Major equations.** Common frameworks include Hudson or Van-der-Meer-type armour stability relations, toe-stability and damage formulations, wave-action balance with phase-decoupled diffraction, mild-slope equations for harbour propagation, porous resistance and transmission relations, and constrained optimization objectives.

**Typical methods.** Methods combine 2-D flumes and 3-D basins, armour-damage surveys, prototype inspections, directional wave arrays, spectral and phase-resolving models, pressure and force measurements, empirical stability formulae, and genetic or multiobjective layout optimization.

**Numerical models.** Models include SWAN with phase-decoupled diffraction, mild-slope wave propagation coupled to a genetic algorithm, COBRAS-UC for loads and pressures, empirical armour and toe stability formulae, and porous-transmission theory.

**Experimental datasets.** Reviewed evidence includes Aalborg depth-limited short-crested and oblique stability tests on a 1:25 foreshore, laboratory multidirectional diffraction at a breakwater shoulder, seven Elmer field spectra around six detached breakwaters, 1:20 crown-wall load tests, and 290 living-breakwall wake cases.

**Validated ranges.** Explicit evidence covers a 1:25 foreshore and 0.5 m plateau for low-crested stability, seven wind-sea/bimodal/swell field spectra at Elmer with 2.9-5.3 m tides, one- and two-segment Beirut layouts, 1:20 low-mound and crown-wall tests, and porous breakwalls of estimated porosity 0.7 and 0.9.

**Recent advances.** Later work embeds wave mechanics within layout optimization, resolves pressure and load fields numerically, and extends breakwater concepts toward porous living systems whose performance and maintenance can be measured under field wakes.

**Disagreements.** Phase-averaged diffraction improves lee wave heights but performs less well for narrow low-frequency swell unless reflection and transmission are represented. Calibrated porous theory overpredicts energy as an emergent breakwall enters shallow-water breaking and friction regimes.

**Limitations.** Laboratory scale, armour placement, seabed mobility, finite storm duration, incomplete field spectra, model physics, uncertain porosity, construction tolerances, and optimization objectives restrict transfer. Prototype applications without measured validation remain demonstrations, not field validation.

**Open questions.** Needs include joint reliability-based optimization of stability, agitation, navigation, morphology, ecology, carbon, maintenance and cost; climate-adjusted design waves and water levels; better toe and foundation failure models; and transferable field validation for multidirectional extremes.

**Seminal papers.** Within this branch, the 2006 low-crested stability synthesis connects controlled testing to prototype foundation failure, and the 2007 SWAN study provides rare laboratory-plus-field validation of multidirectional transformation around detached structures.

## Equations

### low-crested breakwater armour and toe stability formulation

$$
D=f(H_s,T_p,R_c,h,\Delta,D_{n50},N)
$$

Regime: Detached rock-armoured low-crested structures; Aalborg 3-D tests used a 1:25 foreshore and 0.5 m plateau; evidence also includes 2-D depth-limited tests and prototype sites.

Variables: `D` damage measure where applicable; `N` wave action density or test count by context; `x` breakwater node-coordinate vector; `J` normalized optimization objective; `P` constraint penalty; normalized form, not a recovered coefficient equation

Source: (Burcharth 2006, [doi:10.1016/j.coastaleng.2005.10.023](https://doi.org/10.1016/j.coastaleng.2005.10.023))

### SWAN phase-decoupled refraction-diffraction model

$$
\frac{\partial N}{\partial t}+\nabla_{x,y}\cdot(\mathbf{c}_gN)+\frac{\partial(c_\theta N)}{\partial\theta}=S/\sigma
$$

Regime: Laboratory shoulder-diffraction data and seven Elmer field cases: three wind-sea, two bimodal swell-sea, and two narrow swell spectra around six detached breakwaters.

Variables: `D` damage measure where applicable; `N` wave action density or test count by context; `x` breakwater node-coordinate vector; `J` normalized optimization objective; `P` constraint penalty; normalized form, not a recovered coefficient equation

Source: (Suzana Ilić 2007, [doi:10.1016/j.coastaleng.2007.05.002](https://doi.org/10.1016/j.coastaleng.2007.05.002))

### genetic-algorithm and mild-slope detached-breakwater optimizer

$$
J(\mathbf{x})=L(\mathbf{x})+P_{wave}(\mathbf{x})+P_{nav}(\mathbf{x})
$$

Regime: Port of Beirut; one- and two-segment breakwaters under simplified constant-depth and real bathymetry, within a prescribed search space and navigational constraints.

Variables: `D` damage measure where applicable; `N` wave action density or test count by context; `x` breakwater node-coordinate vector; `J` normalized optimization objective; `P` constraint penalty; normalized form, not a recovered coefficient equation

Source: (Elchahal 2013, [doi:10.1016/j.oceaneng.2013.01.021](https://doi.org/10.1016/j.oceaneng.2013.01.021))

## Claims

- **C248.** For detached rock-armoured low-crested breakwaters tested under depth-limited short-crested head-on and oblique waves, a shallow-water formula characterized initiation of armour damage and an existing toe-stability formula agreed with tests; prototype observations additionally showed that toe scour or sinking and insufficient berm volume can initiate regressive armour-layer erosion. *Regime: Detached rock-armoured low-crested structures; Aalborg 3-D tests used a 1:25 foreshore and 0.5 m plateau; evidence also includes 2-D depth-limited tests and prototype sites..* [direct_finding, mixed] (Burcharth 2006, [doi:10.1016/j.coastaleng.2005.10.023](https://doi.org/10.1016/j.coastaleng.2005.10.023))
- **C249.** Across laboratory tests and seven Elmer field spectra, adding phase-decoupled diffraction to SWAN improved wave-height prediction behind detached breakwaters and reproduced broad spectra best, but performance worsened for narrow low-frequency swell where beach reflection and transmission through or over the structures were important. *Regime: Laboratory shoulder-diffraction data and seven Elmer field cases: three wind-sea, two bimodal swell-sea, and two narrow swell spectra around six detached breakwaters..* [direct_finding, mixed] (Suzana Ilić 2007, [doi:10.1016/j.coastaleng.2007.05.002](https://doi.org/10.1016/j.coastaleng.2007.05.002))
- **C250.** For the Port of Beirut design cases, a genetic algorithm coupled to a mild-slope wave model optimized one- and two-segment detached-breakwater node coordinates while enforcing wave-disturbance and navigation constraints under both simplified and real bathymetry; accessible evidence does not establish superiority outside that search space and objective definition. *Regime: Port of Beirut; one- and two-segment breakwaters under simplified constant-depth and real bathymetry, within a prescribed search space and navigational constraints..* [direct_finding, numerical] (Elchahal 2013, [doi:10.1016/j.oceaneng.2013.01.021](https://doi.org/10.1016/j.oceaneng.2013.01.021))
- **C1571.** This paper presents a numerical study of the solitary wave interaction with a submerged breakwater using the Consistent Particle Method (CPM). *Regime: The study system, forcing, data and methods stated in the indexed abstract..* [direct_finding, numerical] (Yaru Ren 2019, [doi:10.3390/w11020261](https://doi.org/10.3390/w11020261))
- **C1579.** Abstract In this paper, a novel hybrid wave energy converter (WEC)‐floating breakwater system consisting of three floating pontoons with power take‐off (PTO) modules is developed to extract wave energy from heave motion and attenuate waves to protect the coast. *Regime: The study system, forcing, data and methods stated in the indexed abstract..* [literature_review_statement, mixed] (Wei Peng 2021, [doi:10.1049/rpg2.12214](https://doi.org/10.1049/rpg2.12214))
- **C1582.** As a kind of technical equipment for wave prevention and wave dissipation, floating breakwater has attracted more and more attention of researchers.Starting from the research progress and application status of the floating breakwater, this paper combs the research status of the floating breakwater, summarizes the application status of the floating breakwater, and obtains the key points of the technical improvement of the floating breakwater.Finally, the future development of the new type of floating breakwater is summarized in terms of its application prospect, wave dissipation principle and application of new materials, which provides a strong reference for the relevant research of the floating breakwater. *Regime: The study system, forcing, data and methods stated in the indexed abstract..* [literature_review_statement, mixed] (Taoran Zhou 2020, [doi:10.31873/ijeas.7.06.10](https://doi.org/10.31873/ijeas.7.06.10))
- **C1654.** Low-crested and other hard coastal defenses create artificial hard-bottom habitat while disrupting adjacent soft sediment; their proliferation can alter regional connectivity, native assemblages and non-native-species spread, so ecological objectives and monitoring must enter planning, design and maintenance. *Regime: Low-crested and other hard defenses placed in soft-bottom coastal landscapes, including repeated structures along developed coastlines..* [literature_review_statement, review] (Laura Airoldi 2005, [doi:10.1016/j.coastaleng.2005.09.007](https://doi.org/10.1016/j.coastaleng.2005.09.007))

## Papers

- Laura Airoldi (2005). An ecological perspective on the deployment and design of low-crested and other hard coastal defence structures. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2005.09.007](https://doi.org/10.1016/j.coastaleng.2005.09.007) [submitted manuscript, read only](https://digital.csic.es/bitstream/10261/39822/3/Airoldi%20et%20al%202005.pdf)
- Burcharth (2006). Structural stability of detached low crested breakwaters. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2005.10.023](https://doi.org/10.1016/j.coastaleng.2005.10.023) [published version, read only](https://vbn.aau.dk/da/publications/structural-stability-of-detached-low-crested-breakwaters/)
- Suzana Ilić (2007). Multidirectional wave transformation around detached breakwaters. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2007.05.002](https://doi.org/10.1016/j.coastaleng.2007.05.002) [submitted manuscript, read only](https://eprints.lancs.ac.uk/id/eprint/28146/2/FiguresCENG-D-06-00037Ilicetal.pdf)
- Elchahal (2013). Optimization of coastal structures: Application on detached breakwaters in ports. *Ocean Engineering*. [doi:10.1016/j.oceaneng.2013.01.021](https://doi.org/10.1016/j.oceaneng.2013.01.021)
- Talia Schoonees (2019). Hard Structures for Coastal Protection, Towards Greener Designs. *Estuaries and Coasts*. [doi:10.1007/s12237-019-00551-z](https://doi.org/10.1007/s12237-019-00551-z) [published version, read only](https://link.springer.com/content/pdf/10.1007/s12237-019-00551-z.pdf)
- Guanche (2009). Numerical analysis of wave loads for coastal structure stability. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2008.11.003](https://doi.org/10.1016/j.coastaleng.2008.11.003) [accepted manuscript, CC BY](https://zenodo.org/records/18215170/files/AAP_Guanche_Losada_Lara_2008.pdf?download=1)
- Yaru Ren (2019). Consistent Particle Method Simulation of Solitary Wave Interaction with a Submerged Breakwater. *Water*. [doi:10.3390/w11020261](https://doi.org/10.3390/w11020261) [published version, CC BY](https://mdpi-res.com/d_attachment/water/water-11-00261/article_deploy/water-11-00261.pdf)
- Safak (2020). Wave transmission through living shoreline breakwalls. *Continental Shelf Research*. [doi:10.1016/j.csr.2020.104268](https://doi.org/10.1016/j.csr.2020.104268) [accepted manuscript, CC BY](https://repository.library.noaa.gov/view/noaa/34021/noaa_34021_DS1.pdf?download=1)
- Wei Peng (2021). Experimental investigation of a triple pontoon wave energy converter and breakwater hybrid system. *IET Renewable Power Generation*. [doi:10.1049/rpg2.12214](https://doi.org/10.1049/rpg2.12214) [published version, CC BY](https://onlinelibrary.wiley.com/doi/pdfdirect/10.1049/rpg2.12214)
- Taoran Zhou (2020). Research and application of floating breakwater. *International Journal of Engineering and Applied Sciences (IJEAS)*. [doi:10.31873/ijeas.7.06.10](https://doi.org/10.31873/ijeas.7.06.10) [published version, read only](https://doi.org/10.31873/ijeas.7.06.10)
