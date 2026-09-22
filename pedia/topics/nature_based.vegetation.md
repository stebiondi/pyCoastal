# Vegetation and wave attenuation

`nature_based.vegetation` | Marsh, mangrove, and flexible vegetation effects.

Parent: [Nature-based coastal protection](nature_based.md)

Papers: 32. Claims: 22. Equations: 4.

## Synthesis

**Well established.** Vegetation attenuates waves through hydrodynamic work on stems, roots, and canopies, but performance is jointly controlled by plant geometry, density, flexibility, vertical submergence, spatial layout, wave nonlinearity, current, patch length, and seasonal state.

**Governing physics.** Drag depends on relative water-plant velocity and wetted frontal area; flexibility redistributes motion and dissipation vertically; nonlinear orbital kinematics, current-modified group velocity, diffraction through gaps, breaking, and canopy submergence alter spatial decay.

**Dimensionless parameters.** Key controls include Ursell number, Cauchy number, excursion ratio, Keulegan-Carpenter and Reynolds numbers, relative plant/root height and submergence, solid volume fraction, current-to-orbital velocity ratio, effective-length ratio, and layout spacing Sr.

**Major equations.** Common formulations balance wave-energy flux against vegetation drag, use transmission or decay coefficients, Ursell and Cauchy scaling, Euler-Bernoulli stem response, a corrected work factor chi, current-aware reciprocal-to-exponential decay, and Weibull statistics for attenuated random heights.

**Typical methods.** Studies use plant-mimic and live-plant flumes, field pressure arrays during storms, simultaneous stem-motion and velocity measurements, energy-balance theory, RANS or phase-resolving validation, spectral-wave implementation, and stochastic vegetation-property sampling.

**Numerical models.** Models include Dalrymple/Kobayashi and modified Weibull relations, SWASH, Euler-Bernoulli quasi-flexible damping, NEWFLUME RANS, spacing/diffraction energy balance, and momentum-coupled frequency-distributed MIKE SW.

**Experimental datasets.** Evidence spans four flexible species analogues, a 17.5 m mangrove array, 112 component-resolved tests, 24 simultaneous motion/velocity cases, 177 Tropical Storm Lee wave records, four spatial layouts, five-species validation, and 1205 seasonal plant measurements.

**Validated ranges.** Reported ranges include 20-76% reduction over 1 m, transmission 0.21-0.83, Ur about 20-250, quasi-flexible applicability L>1.4 and Ca<700, current ratio -1.5 to 3.0, Sr transition at one, and storm Hs to 0.4 m in 0.8 m depth; each is experiment-specific.

**Recent advances.** Recent work replaces locally tuned damping with measurable mechanics, adds current-induced asymmetry and layout uniformity, and embeds seasonal heterogeneous vegetation into spectral models while preserving field-scale computational efficiency.

**Disagreements.** Apparent conflicts over whether larger or longer waves attenuate more arise because nonlinearity, submergence, flexibility, current, and normalization length vary together. Likewise, local heterogeneity can matter for gaps and extremes even when mean plant properties suffice for bulk engineering attenuation.

**Limitations.** Most evidence uses idealized cylindrical vegetation, short patches, regular or narrow condition sets, fixed beds, and calibrated or assumed force coefficients. Extreme folding, breakage, mortality, currents, directional spectra, morphodynamics, and cross-site ecological variability remain weakly constrained.

**Open questions.** Priorities include storm-scale field validation across species and seasons, flexible layered architecture under reversing currents, damage and recovery, directional gap effects, uncertainty in extreme tails, and coupling attenuation to sediment, morphology, and ecological persistence.

**Seminal papers.** Within this screened slice, the 2013 tropical-storm Weibull study provides rare extreme-event field statistics, while the 2014 flexible-vegetation experiments establish multi-trait attenuation ranges beyond rigid-cylinder assumptions.

## Equations

### Vegetation-modified Weibull wave-height distribution

$$
p(H)=\frac{k}{\lambda}(H/\lambda)^{k-1}e^{-(H/\lambda)^k}
$$

Regime: Storm waves attenuated through the measured Spartina marsh.

Variables: `H` zero-crossing wave height; `k` shape parameter; `lambda` scale parameter dependent on k

Source: (Jadhav 2013, [doi:10.1016/j.coastaleng.2013.08.006](https://doi.org/10.1016/j.coastaleng.2013.08.006))

### Ursell number

$$
Ur=H_sL^2/h^3
$$

Regime: Wave conditions at the mangrove-field edge.

Variables: `Ur` Ursell number; `H_s` significant wave height; `L` wavelength; `h` water depth

Source: (Phan 2019, [doi:10.1016/j.coastaleng.2019.01.004](https://doi.org/10.1016/j.coastaleng.2019.01.004))

### Corrected flexible-vegetation work-factor dissipation

$$
D_f=\chi D_r
$$

Regime: Quasi-flexible cylindrical vegetation with L>1.4 and Ca<700.

Variables: `D_f` flexible-vegetation dissipation; `chi` work factor restored by corrigendum; `D_r` corresponding rigid-vegetation dissipation

Source: (van Veelen 2021, [doi:10.1016/j.coastaleng.2020.103820](https://doi.org/10.1016/j.coastaleng.2020.103820))

### Current-aware mixed vegetation decay law

$$
H(x)=H_0\,\mathcal{G}(x;U/u_o,C_D,c_g)
$$

Regime: Emergent uniform vegetation with -1.5<=U/u_o<=3.0.

Variables: `H` wave height; `H_0` incident height; `U` current speed; `u_o` wave orbital velocity; `C_D` drag coefficient; `c_g` current-modified group velocity

Source: (Liu 2024, [doi:10.1016/j.coastaleng.2024.104508](https://doi.org/10.1016/j.coastaleng.2024.104508))

## Claims

- **C171.** Across four flexible salt-marsh vegetation analogues, measured wave-height reduction over a 1 m patch ranged from 20% to 76%; damping depended jointly on plant geometry, density, flexibility, submergence, and wave conditions rather than marsh width alone. *Regime: The tested flexible mimics, one-metre patch, irregular waves, and submerged-to-emergent conditions..* [direct_finding, experimental] (Anderson 2014, [doi:10.1016/j.coastaleng.2013.10.004](https://doi.org/10.1016/j.coastaleng.2013.10.004))
- **C172.** In 200-400 stem/m2 mangrove analogues, increasing Ursell number from about 50 to 250 increased wave-height attenuation by roughly 20 percentage points over one wavelength and 35 over three, while sensitivity weakened above about Ur=250. *Regime: Rigid arrays, Ur approximately 20-250, tested broken/non-broken regular and irregular waves..* [direct_finding, mixed] (Phan 2019, [doi:10.1016/j.coastaleng.2019.01.004](https://doi.org/10.1016/j.coastaleng.2019.01.004))
- **C173.** Across 112 stem-root-canopy experiments, vegetation transmission coefficients ranged from 0.21 to 0.83; roots contributed significantly when relative root height exceeded 0.167, and attenuation peaked when still water lay near the canopy centroid. *Regime: Fixed-period waves and the tested idealized seven-model, four-density component geometries..* [direct_finding, experimental] (He 2019, [doi:10.1016/j.coastaleng.2019.103509](https://doi.org/10.1016/j.coastaleng.2019.103509))
- **C174.** For quasi-flexible cylindrical vegetation with excursion ratio L>1.4 and Cauchy number Ca<700, damping was governed by relative water-stem velocity in the upright lower stem, and the model reproduced the order of damping across five species without species-specific drag calibration. *Regime: Regular waves, cylindrical vegetation, L>1.4, Ca<700, without extreme folding..* [direct_finding, mixed] (van Veelen 2021, [doi:10.1016/j.coastaleng.2020.103820](https://doi.org/10.1016/j.coastaleng.2020.103820))
- **C175.** During a tropical storm, 177 wave records across 28 m of Spartina marsh showed an upper-tail deficit relative to Rayleigh statistics; a vegetation-modified Weibull distribution fit the local heights for Hs up to 0.4 m in 0.8 m depth. *Regime: The measured tropical-storm event, inundated Spartina marsh, and local wave/depth range..* [direct_finding, field] (Jadhav 2013, [doi:10.1016/j.coastaleng.2013.08.006](https://doi.org/10.1016/j.coastaleng.2013.08.006))
- **C176.** For emerged vegetation and current-to-orbital velocity ratios from -1.5 to 3.0, opposing currents attenuated waves more than equal following currents; increasing current shifted decay from reciprocal toward exponential and made strong-current decay insensitive to incident amplitude. *Regime: Uniform emergent vegetation, steady following/opposing current, tested velocity-ratio interval..* [direct_finding, mixed] (Liu 2024, [doi:10.1016/j.coastaleng.2024.104508](https://doi.org/10.1016/j.coastaleng.2024.104508))
- **C177.** In four flexible-vegetation layouts, the combined spacing parameter separated laterally uniform attenuation at Sr<1 from nonuniform attenuation at Sr>1, and a staggered layout matched full-coverage uniformity with a smaller vegetation footprint. *Regime: The tested half, segmented, staggered, and full layouts and the study's Sr definition..* [direct_finding, mixed] (Wang 2026, [doi:10.1016/j.coastaleng.2025.104937](https://doi.org/10.1016/j.coastaleng.2025.104937))
- **C178.** A momentum-coupled MIKE SW vegetation model validated against laboratory and Tropical Storm Lee data reproduced significant wave height and spectral period without prescribed Cdis; analysis of 1205 plant measurements found spatial mean vegetation properties sufficient for engineering predictions despite seasonal lognormal variability. *Regime: The tested flexible saltmarsh canopies, fixed force coefficients Cm=0.5 and Cd=2.0, and validated laboratory/field conditions..* [direct_finding, mixed] (Jacobsen 2026, [doi:10.1016/j.coastaleng.2026.105099](https://doi.org/10.1016/j.coastaleng.2026.105099))
- **C179.** The formal corrigendum states that work factor chi was omitted from printed Eq. 32 of the quasi-flexible vegetation model; implementations must use the corrected expression containing chi. *Regime: Any implementation of Eq. 32 in the corrected 2021 quasi-flexible vegetation model..* [direct_finding, analytical] (van Veelen 2022, [doi:10.1016/j.coastaleng.2022.104165](https://doi.org/10.1016/j.coastaleng.2022.104165))
- **C370.** For validated vegetated-wave cases, a depth-varying velocity drag formulation matched fully expanded Boussinesq results, while the linear analytical solution agreed except near-emergent or emergent vegetation and the abstract's stated Ur<5 regime. *Regime: Vegetated laboratory cases and Hurricane Isaac peak-wave simulations; linear comparison degraded for stem-height/depth above 0.75 and Ur<5 as stated in the abstract..* [direct_finding, mixed] (Agnimitro Chakrabarti 2017, [doi:10.1002/2016jc012093](https://doi.org/10.1002/2016jc012093))
- **C380.** In a 1:12 model Rhizophora forest, root-zone velocity decreased by up to 50% and turbulence increased fivefold; velocity and individual-tree drag reached fully developed behavior by the fifth row, and properly scaled drag coefficients collapsed as a Reynolds-number function. *Regime: Thirty-two 1:12 Rhizophora models with 24 prop roots each in a 2.5 m staggered forest..* [direct_finding, experimental] (María Maza 2017, [doi:10.1002/2017jc012945](https://doi.org/10.1002/2017jc012945))
- **C1196.** Living-shoreline marshes aged 12–38 years sequestered 58–283 g C m⁻² yr⁻¹, with lower rates at older sites, showing that shoreline stabilization can add blue-carbon benefits but age affects long-term estimates. *Regime: Living Shorelines: Coastal Resilience with a Blue Carbon Benefit.* [direct_finding, mixed] (Jenny Davis 2015, [doi:10.1371/journal.pone.0142595](https://doi.org/10.1371/journal.pone.0142595))
- **C1202.** At three of four Port Phillip Bay sites kelp beds attenuated less wave energy than urchin-barren controls; only under northerly winds at the fourth site was kelp attenuation about 10% greater, showing substrate and kelp effects must be separated. *Regime: Kelp beds as coastal protection: wave attenuation of Ecklonia radiata in a shallow coastal bay.* [direct_finding, mixed] (Rebecca L. Morris 2019, [doi:10.1093/aob/mcz127](https://doi.org/10.1093/aob/mcz127))
- **C1348.** Global process-based valuation estimates mangroves avert more than US$65 billion in flood damage annually and protect 15 million people from annual flooding, with many urban coastal stretches exceeding US$250 million in yearly benefit. *Regime: The Global Flood Protection Benefits of Mangroves.* [direct_finding, mixed] (Pelayo Menéndez 2020, [doi:10.1038/s41598-020-61136-6](https://doi.org/10.1038/s41598-020-61136-6))
- **C1350.** High-resolution flood-loss models estimate northeastern U.S. wetlands avoided US$625 million in direct Hurricane Sandy damage and reduced average annual Barnegat Bay flood losses by 16%. *Regime: The Value of Coastal Wetlands for Flood Damage Reduction in the Northeastern USA.* [direct_finding, mixed] (Siddharth Narayan 2017, [doi:10.1038/s41598-017-09269-z](https://doi.org/10.1038/s41598-017-09269-z))
- **C1351.** Ten months of saltmarsh observations found 92% mean wave-height attenuation over 310 m; the first 10 m of vegetation dissipated 2.1% per metre on a ramped edge versus 1.1% at a cliffed edge, with seasonal variation. *Regime: Wave dissipation over macro-tidal saltmarshes: Effects of marsh edge typology and vegetation change.* [direct_finding, field] (Iris Möller 2002, [doi:10.2112/1551-5036-36.sp1.506](https://doi.org/10.2112/1551-5036-36.sp1.506))
- **C1619.** Field measurements on two salt marshes and a calibrated SWAN model show that vegetation remains effective under severe storm inundation: with bulk drag coefficient about 0.4, vegetation added 25-50% significant-wave-height reduction relative to breaking and bottom friction alone. *Regime: Spartina anglica and Scirpus maritimus salt marshes and modeled sloping foreshores under the tested storm loads and vegetation states..* [direct_finding, mixed] (Vincent Vuik 2016, [doi:10.1016/j.coastaleng.2016.06.001](https://doi.org/10.1016/j.coastaleng.2016.06.001))
- **C1635.** Large-flume tests with flexible vegetation mimics show that stiffness and bending-controlled dynamic frontal area, not biomass alone, govern wave drag; an effective-leaf-length model reproduced regular and irregular force time series but missed extra drag from close-neighbor interaction. *Regime: Artificial vegetation arrangements of varied stiffness, frontal area and volume under tested regular and irregular wave orbital velocities..* [direct_finding, experimental] (Paul 2016, [doi:10.1016/j.coastaleng.2016.07.004](https://doi.org/10.1016/j.coastaleng.2016.07.004))
- **C1661.** Under comparable inundation in a subtropical estuary, saltmarsh and mangrove edges both trap mudflat-derived suspended sediment, but the saltmarsh edge traps more because mangrove-induced flow rotation diverts normal flux; settling and direct capture on plant surfaces jointly build deposits. *Regime: Adjacent bare mudflat, mangrove and saltmarsh stands with similar hydroperiod in a subtropical estuary during the observed spring tide..* [direct_finding, field] (Yining Chen 2018, [doi:10.1016/j.geomorph.2018.06.018](https://doi.org/10.1016/j.geomorph.2018.06.018))
- **C1664.** Temperate kelps are ecosystem engineers whose holdfasts, stipes, blades and understory modify physical conditions, support diverse and abundant assemblages and trophic links, and provide coastal-defense and other ecosystem services, but their habitat function varies strongly among species and regions. *Regime: Canopy-forming kelps on temperate and subpolar intertidal and shallow-subtidal rocky reefs represented in the reviewed literature..* [literature_review_statement, review] (Harry Teagle 2017, [doi:10.1016/j.jembe.2017.01.017](https://doi.org/10.1016/j.jembe.2017.01.017))
- **C1677.** Wakes from adjacent emergent vegetation patches remain locally patch-specific but merge downstream; in staggered layouts the downstream patch shortens and distorts the upstream wake, and density controls interpatch velocity, turbulence and potential sediment/propagule retention. *Regime: Two circular emergent rigid vegetation patches under the tested steady flume flow, densities and side-by-side/staggered spacing..* [direct_finding, experimental] (Vasileios Kitsikoudis 2020, [doi:10.1007/s10652-020-09746-6](https://doi.org/10.1007/s10652-020-09746-6))
- **C1728.** A coupled three-dimensional nonhydrostatic model predicts that a surf-zone vegetation patch damps breaking-wave turbulence, reduces sediment pickup, confines suspended material near the bed, and reverses net transport from seaward outside the patch to shoreward within it. *Regime: A finite vegetation patch in the surf zone under breaking waves, with canopy drag, turbulence production, suspended sediment, and bed exchange..* [direct_finding, numerical] (Anon. 2014, [doi:10.9753/icce.v34.sediment.17](https://doi.org/10.9753/icce.v34.sediment.17))

## Papers

- Harry Teagle (2017). The role of kelp species as biogenic habitat formers in coastal marine ecosystems. *Journal of Experimental Marine Biology and Ecology*. [doi:10.1016/j.jembe.2017.01.017](https://doi.org/10.1016/j.jembe.2017.01.017)
- Pelayo Menéndez (2020). The Global Flood Protection Benefits of Mangroves. *Scientific Reports*. [doi:10.1038/s41598-020-61136-6](https://doi.org/10.1038/s41598-020-61136-6)
- Siddharth Narayan (2017). The Value of Coastal Wetlands for Flood Damage Reduction in the Northeastern USA. *Scientific Reports*. [doi:10.1038/s41598-017-09269-z](https://doi.org/10.1038/s41598-017-09269-z)
- Anderson (2014). Wave attenuation by flexible, idealized salt marsh vegetation. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2013.10.004](https://doi.org/10.1016/j.coastaleng.2013.10.004)
- Vincent Vuik (2016). Nature-based flood protection: The efficiency of vegetated foreshores for reducing wave loads on coastal dikes. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2016.06.001](https://doi.org/10.1016/j.coastaleng.2016.06.001)
- Iris Möller (2002). Wave dissipation over macro-tidal saltmarshes: Effects of marsh edge typology and vegetation change. *Journal of Coastal Research*. [doi:10.2112/1551-5036-36.sp1.506](https://doi.org/10.2112/1551-5036-36.sp1.506)
- Jenny Davis (2015). Living Shorelines: Coastal Resilience with a Blue Carbon Benefit. *PLOS ONE*. [doi:10.1371/journal.pone.0142595](https://doi.org/10.1371/journal.pone.0142595)
- Yining Chen (2018). Differential sediment trapping abilities of mangrove and saltmarsh vegetation in a subtropical estuary. *Geomorphology*. [doi:10.1016/j.geomorph.2018.06.018](https://doi.org/10.1016/j.geomorph.2018.06.018)
- Phan (2019). The effects of wave non-linearity on wave attenuation by vegetation. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2019.01.004](https://doi.org/10.1016/j.coastaleng.2019.01.004)
- Paul (2016). Plant stiffness and biomass as drivers for drag forces under extreme wave loading: A flume study on mimics. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2016.07.004](https://doi.org/10.1016/j.coastaleng.2016.07.004)
- María Maza (2017). Velocity and Drag Evolution From the Leading Edge of a Model Mangrove Forest. *Journal of Geophysical Research Oceans*. [doi:10.1002/2017jc012945](https://doi.org/10.1002/2017jc012945)
- He (2019). Surface wave attenuation by vegetation with the stem, root and canopy. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2019.103509](https://doi.org/10.1016/j.coastaleng.2019.103509)
- van Veelen (2021). Modelling wave attenuation by quasi-flexible coastal vegetation. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2020.103820](https://doi.org/10.1016/j.coastaleng.2020.103820)
- Jadhav (2013). Probability distribution of wave heights attenuated by salt marsh vegetation during tropical cyclone. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2013.08.006](https://doi.org/10.1016/j.coastaleng.2013.08.006)
- Vasileios Kitsikoudis (2020). Experimental analysis of flow and turbulence in the wake of neighboring emergent vegetation patches with different densities. *Environmental Fluid Mechanics*. [doi:10.1007/s10652-020-09746-6](https://doi.org/10.1007/s10652-020-09746-6)
- Agnimitro Chakrabarti (2017). Boussinesq modeling of wave‐induced hydrodynamics in coastal wetlands. *Journal of Geophysical Research: Oceans*. [doi:10.1002/2016jc012093](https://doi.org/10.1002/2016jc012093)
- Rebecca L. Morris (2019). Kelp beds as coastal protection: wave attenuation of Ecklonia radiata in a shallow coastal bay. *Annals of Botany*. [doi:10.1093/aob/mcz127](https://doi.org/10.1093/aob/mcz127)
- Liu (2024). A theoretical model for wave attenuation by vegetation considering current effects. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2024.104508](https://doi.org/10.1016/j.coastaleng.2024.104508)
- Wang (2026). Vegetation layouts influence the spatial uniformity of wave attenuation: Laboratory insights. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2025.104937](https://doi.org/10.1016/j.coastaleng.2025.104937)
- Anon. (2014). MODELING WAVE DAMPING AND SEDIMENT TRANSPORT WITHIN A PATCH OF VEGETATION. **. [doi:10.9753/icce.v34.sediment.17](https://doi.org/10.9753/icce.v34.sediment.17)
- Jacobsen (2026). Wave attenuation through a saltmarsh: Heterogeneous vegetation characteristics and seasonal variability. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2026.105099](https://doi.org/10.1016/j.coastaleng.2026.105099)
- van Veelen (2022). Corrigendum to “Modelling wave attenuation by quasi-flexible coastal vegetation” [Coast. Eng. 164 (2021) 103820]. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2022.104165](https://doi.org/10.1016/j.coastaleng.2022.104165)
- John W. Day (2008). Consequences of Climate Change on the Ecogeomorphology of Coastal Wetlands. *Estuaries and Coasts*. [doi:10.1007/s12237-008-9047-6](https://doi.org/10.1007/s12237-008-9047-6)
- Hladik (2013). Salt marsh elevation and habitat mapping using hyperspectral and LIDAR data. *Remote Sensing of Environment*. [doi:10.1016/j.rse.2013.08.003](https://doi.org/10.1016/j.rse.2013.08.003)
- Erik Horstman (2014). Tidal-scale flow routing and sedimentation in mangrove forests: Combining field data and numerical modelling. *Geomorphology*. [doi:10.1016/j.geomorph.2014.08.011](https://doi.org/10.1016/j.geomorph.2014.08.011)
- ... and 7 more in `pycoapedia.sqlite` (table `paper_topics`).
