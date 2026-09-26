# Wave setup contribution to storm surge

`storm_surge.coupling.wave_setup` | Breaking-wave radiation-stress contributions to storm water levels, including interactions with tides, currents, and coastal morphology.

Parent: [Storm surge and coastal flooding](storm_surge.md) > [Wave-surge-tide coupling](storm_surge.coupling.md)

Papers: 5. Claims: 15. Equations: 1.

Used by pyCoastal design modules: Storm surge and flooding.

## Synthesis

**Well established.** Breaking-wave energy loss transfers onshore momentum through radiation-stress or vortex-force gradients; across the reviewed events this contribution raised mean water levels and altered hurricane or extratropical-storm flooding.

**Governing physics.** Setup is controlled by where wave energy dissipates relative to the shoreline, ebb delta, inlet and shelf. The resulting wave force is primarily balanced by a barotropic pressure gradient; tide changes water depth and breaking location, while currents can provide a smaller secondary feedback in the Klaus inlet tests.

**Dimensionless parameters.** Wave-setup importance is commonly expressed through relative contributions such as setup divided by peak surge or total water level, flooded-area increment divided by total flooded area, grid spacing relative to surf-zone width, and wave-force magnitude relative to pressure-gradient or stress terms. These ratios are diagnostic and event-specific rather than universal similarity laws.

**Major equations.** The studies introduce wave effects through spectral-wave momentum forcing of the circulation equations. Process experiments diagnose setup by differencing otherwise comparable simulations with and without wave forces; this difference can contain nonlinear tide-level feedback unless stationary level tests isolate it.

**Typical methods.** Credible event attribution combines a spectral wave model with a wetting-and-drying circulation model, compares wave-on and wave-off configurations, validates component waves and water levels, and uses phase-averaged or phase-resolving profile models when setup must be separated from swash.

**Numerical models.** Reviewed configurations couple WAM-STWAVE-ADCIRC for Katrina/Rita, MIKE 21 SW-HD FM plus XBeach 1D for Iota, and WWMII-SCHISM with a 3D vortex-force formulation for Klaus.

**Experimental datasets.** Available validation evidence includes 399 Katrina regional high-water marks, Rita hydrographs/high-water marks and wave buoys, Iota wave and water-level sensors along a 7.196 km island profile, and Klaus tide-gauge and wave observations at two Bay of Biscay inlets.

**Validated ranges.** Event-specific magnitudes are substantial but use different response measures: the Klaus study attributes 40% and 23% of peak surge to setup at Adour and Arcachon; the Iota study attributes 11.45 ha, or 14.93% of total modeled Providencia flooded area, to adding setup; and the Katrina study identifies a local unresolved setup contribution as large as 0.5 m near 17th Street Canal.

**Recent advances.** The progression from sequential radiation-stress coupling and regional HWM validation to fully coupled 3D inlet momentum diagnostics and explicit setup/runup flood-component scenarios enables more defensible attribution, but also reveals that operational-resolution and ensemble-cost gaps remain.

**Disagreements.** The reviewed percentages do not constitute a physical disagreement: Klaus reports setup as a fraction of peak surge, Iota reports its contribution to inundated area, and the Iota profile reports setup-plus-swash runup as a fraction of peak water level. Site morphology and response definitions must be aligned before comparing magnitudes.

**Limitations.** Grid resolution is a first-order limitation: the Katrina regional model missed localized setup, and the Klaus 35 m beach result exceeded 200 m and 1000 m results by 30% and 65%. The Klaus authors offer roughly five elements across the surf zone only as a case-derived guideline, not a universal convergence rule. Probabilistic hazard products remain incomplete when waves are omitted: the Iota reconstruction included setup, but its 738-event synthetic ensemble excluded setup for computational reasons and therefore cannot quantify total wave-inclusive flood hazard.

**Open questions.** Priorities are computationally affordable wave-inclusive ensembles, event observations that separate mean setup from swash and infragravity motions, morphology-aware grid convergence, and transfer tests across open beaches, reefed islands, lagoons and estuaries.

**Seminal papers.** Radiation-stress theory established that gradients in wave momentum flux drive mean-water-level setup; later spectral-wave and circulation coupling embedded that forcing in storm-surge models. The reviewed Katrina/Rita application represents an early high-resolution regional validation, followed by process-resolving inlet attribution and component-based island flood reconstruction.

## Equations

### Model-difference setup diagnostic

$$
\eta_{setup}=\eta_{waves+tide+atmosphere}-\eta_{tide+atmosphere}
$$

Regime: Storm Klaus process-suppression experiments; nonlinear tide-level feedback requires separate stationary tests.

Variables: `eta_setup` modeled wave-induced water-level contribution; `eta_waves+tide+atmosphere` fully coupled water level; `eta_tide+atmosphere` water level without wave forces

Source: (Laura Lavaud 2020, [doi:10.1016/j.ocemod.2020.101710](https://doi.org/10.1016/j.ocemod.2020.101710))

## Claims

- **C72.** In the SL15 system, STWAVE radiation stresses from depth-limited wave breaking are applied to ADCIRC and can modify surge magnitude, peak timing, and drawdown. *Regime: Sequential WAM-STWAVE-ADCIRC Katrina/Rita configuration for Louisiana and Mississippi..* [direct_finding, numerical] (Bunya 2010, [doi:10.1175/2009mwr2906.1](https://doi.org/10.1175/2009mwr2906.1))
- **C73.** For Katrina, 70% of 206 USACE and 73% of 193 URS/FEMA still-water high-water marks were reproduced within 0.5 m by the coupled model. *Regime: Hurricane Katrina regional hindcast and the two reported HWM datasets..* [direct_finding, mixed] (Bunya 2010, [doi:10.1175/2009mwr2906.1](https://doi.org/10.1175/2009mwr2906.1))
- **C74.** At the 17th Street Canal the regional model underpredicted peak surge by about 0.6 m, while cited local Boussinesq modeling indicated as much as 0.5 m of wave-driven setup absent at the regional resolution. *Regime: South shore of Lake Pontchartrain during Katrina; this is a local diagnosis, not a basin-wide setup value..* [direct_finding, mixed] (Bunya 2010, [doi:10.1175/2009mwr2906.1](https://doi.org/10.1175/2009mwr2906.1))
- **C75.** The authors attribute localized setup underprediction along the south shore of Lake Pontchartrain and near raised features partly to inadequate wave and circulation grid resolution. *Regime: Locations with unresolved wave gradients, levees, roads, or hydraulic connections in SL15..* [direct_finding, numerical] (Bunya 2010, [doi:10.1175/2009mwr2906.1](https://doi.org/10.1175/2009mwr2906.1))
- **C76.** For Hurricane Iota on Providencia, adding modeled wave setup to storm tide increased flooded area from 65.23 ha to 76.68 ha; the authors report 11.45 ha, or 14.93% of total modeled flooded area, as the setup contribution. *Regime: Providencia/Santa Catalina during Iota, coupled HD FM-SW setup without swash..* [direct_finding, numerical] (Wilmer Rey 2021, [doi:10.3389/fmars.2021.766258](https://doi.org/10.3389/fmars.2021.766258))
- **C77.** At the eastern Providencia profile during Iota peak, the modeled contributions to maximum water level were -3.01% astronomical tide, 46.36% storm surge, and 56.55% wave runup including setup and swash. *Regime: One eastern-island profile and the modeled storm peak; runup is broader than wave setup alone..* [direct_finding, numerical] (Wilmer Rey 2021, [doi:10.3389/fmars.2021.766258](https://doi.org/10.3389/fmars.2021.766258))
- **C78.** The coupled MIKE 21 configuration adds radiation-stress setup but omits swash, whereas the XBeach 1D configuration resolves setup-plus-swash runup along a selected profile. *Regime: The paper's Iota configuration; these outputs must not be interpreted as the same response variable..* [direct_finding, numerical] (Wilmer Rey 2021, [doi:10.3389/fmars.2021.766258](https://doi.org/10.3389/fmars.2021.766258))
- **C79.** Wave setup was excluded from the 738 synthetic and hypothetical-event surge simulations because of computational cost, so their probabilistic maps underrepresent wave contributions by construction. *Regime: The synthetic and hypothetical hazard ensembles, not the dedicated Iota reconstruction..* [direct_finding, numerical] (Wilmer Rey 2021, [doi:10.3389/fmars.2021.766258](https://doi.org/10.3389/fmars.2021.766258))
- **C80.** During storm Klaus, wave setup accounted for 40% of peak surge in the Adour Estuary and 23% in Arcachon Lagoon, and including wave forces improved surge predictions by 50-60%. *Regime: Storm Klaus hindcast at the two Bay of Biscay inlets..* [direct_finding, numerical] (Laura Lavaud 2020, [doi:10.1016/j.ocemod.2020.101710](https://doi.org/10.1016/j.ocemod.2020.101710))
- **C81.** At the Arcachon inlet ebb delta, modeled wave force was one order of magnitude larger than bottom and surface stress and was balanced mainly by the barotropic pressure gradient. *Regime: Arcachon outer inlet during storm-peak forcing..* [direct_finding, numerical] (Laura Lavaud 2020, [doi:10.1016/j.ocemod.2020.101710](https://doi.org/10.1016/j.ocemod.2020.101710))
- **C82.** Adour setup in stationary Klaus-wave tests decreased from 0.60 m at a -1.5 m imposed water level to 0.45 m at +1.5 m, whereas Arcachon modulation was only about 0.07 m. *Regime: The two inlet bathymetries and imposed -1.5 to +1.5 m level range; the contrast is site-specific..* [direct_finding, numerical] (Laura Lavaud 2020, [doi:10.1016/j.ocemod.2020.101710](https://doi.org/10.1016/j.ocemod.2020.101710))
- **C83.** On the exposed beach near Arcachon, peak surge with the 35 m grid was 30% and 65% higher than with 200 m and 1000 m grids because coarse grids poorly represented setup. *Regime: Storm Klaus adjacent beach with roughly 1 km-wide surf zone..* [direct_finding, numerical] (Laura Lavaud 2020, [doi:10.1016/j.ocemod.2020.101710](https://doi.org/10.1016/j.ocemod.2020.101710))
- **C84.** The study proposes a rough requirement of at least five computational elements across the surf zone to represent setup in surge models. *Regime: Case-derived guideline whose required spacing varies with surf-zone width, slope, and wave height..* [inferred_relationship, numerical] (Laura Lavaud 2020, [doi:10.1016/j.ocemod.2020.101710](https://doi.org/10.1016/j.ocemod.2020.101710))
- **C1651.** For Typhoon Morakot in the Taiwan Strait, coupled ADCIRC-SWAN simulations show wave-current interaction improves agreement with observed water levels and significant wave height; breaking-wave radiation-stress gradients create nearshore setup while water level and current modulate waves. *Regime: Typhoon Morakot (2009) across the Taiwan Strait and shallow nearshore/estuarine waters of coastal Fujian..* [direct_finding, mixed] (Xiaolong Yu 2017, [doi:10.1016/j.csr.2017.08.009](https://doi.org/10.1016/j.csr.2017.08.009))
- **C1714.** A coupled surge-wave hindcast for Typhoon 7010 in Kochi shows radiation-stress wave setup materially raises coastal water levels and inundation, while an offshore breakwater reduces wave setup and the flooded area. *Regime: Typhoon 7010 storm surge, waves, setup, and inundation in Kochi under historical and offshore-breakwater configurations..* [direct_finding, numerical] (MIMURA 2010, [doi:10.2208/kaigan.66.216](https://doi.org/10.2208/kaigan.66.216))

## Papers

- Bunya (2010). A High-Resolution Coupled Riverine Flow, Tide, Wind, Wind Wave, and Storm Surge Model for Southern Louisiana and Mississippi. Part I: Model Development and Validation. *Monthly Weather Review*. [doi:10.1175/2009mwr2906.1](https://doi.org/10.1175/2009mwr2906.1) [published version, read only](https://journals.ametsoc.org/downloadpdf/journals/mwre/138/2/2009mwr2906.1.pdf)
- Xiaolong Yu (2017). Effects of wave-current interaction on storm surge in the Taiwan Strait: Insights from Typhoon Morakot. *Continental Shelf Research*. [doi:10.1016/j.csr.2017.08.009](https://doi.org/10.1016/j.csr.2017.08.009) [submitted manuscript, read only](https://ueaeprints.uea.ac.uk/id/eprint/64582/1/Accepted_manuscript.pdf)
- Laura Lavaud (2020). The contribution of short-wave breaking to storm surges: The case Klaus in the Southern Bay of Biscay. *Ocean Modelling*. [doi:10.1016/j.ocemod.2020.101710](https://doi.org/10.1016/j.ocemod.2020.101710) [published version, read only](https://api.elsevier.com/content/article/PII:S1463500320302122?httpAccept=text/xml)
- Wilmer Rey (2021). Hurricane Flood Hazard Assessment for the Archipelago of San Andres, Providencia and Santa Catalina, Colombia. *Frontiers in Marine Science*. [doi:10.3389/fmars.2021.766258](https://doi.org/10.3389/fmars.2021.766258) [published version, CC BY](https://www.frontiersin.org/articles/10.3389/fmars.2021.766258/pdf)
- MIMURA (2010). Effectivity of Storm Surge - Wave Hindcasting Coupling Model on Estimation of Storm Surge at T7010. *Journal of Japan Society of Civil Engineers, Ser. B2 (Coastal Engineering)*. [doi:10.2208/kaigan.66.216](https://doi.org/10.2208/kaigan.66.216) [published version, read only](https://www.jstage.jst.go.jp/article/kaigan/66/1/66_1_216/_pdf)
