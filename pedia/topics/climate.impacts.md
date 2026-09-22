# Coastal impacts of climate change

`climate.impacts` | Changing hazards and morphology.

Parent: [Sea-level rise and climate adaptation](climate.md)

Papers: 46. Claims: 29. Equations: 8.

## Synthesis

**Well established.** Coastal climate impacts arise through interacting changes in mean sea level, extremes, waves, rainfall and groundwater, then propagate through shoreline position, overtopping, drainage, habitats, assets, economies, water security and institutions. Adaptation materially changes outcomes but is itself constrained by governance and local context.

**Governing physics.** Rising mean water level reduces structure freeboard, shifts groundwater upward, increases boundary head on drainage, exposes shorelines to profile adjustment and intensifies coastal squeeze where landward habitat migration is blocked. Coincident tide, waves, rainfall and groundwater make impacts nonlinear and spatially heterogeneous.

**Dimensionless parameters.** Useful controls include relative sea-level rise to freeboard, relative wave height and steepness, exceedance probability, return-period ratio, groundwater depth normalized by relief, rainfall-to-drainage-capacity ratio, recession normalized by active-profile width, benefit-cost ratio and fractional avoided loss.

**Major equations.** Core formulations include joint extreme-value probability for waves and water levels, overtopping discharge as a nonlinear function of relative freeboard, two-dimensional shallow-water continuity and momentum, Bruun-rule equilibrium shoreline translation, and discounted impact-adaptation objective functions that combine damage and intervention cost.

**Typical methods.** Methods span climate-model ensembles, downscaling, joint probability and extreme-value analysis, HEC-RAS 2D inundation, GIS exposure mapping, equilibrium-profile rules, integrated assessment and optimization, systematic reviews, policy robustness assessment and Indigenous community-centered adaptation frameworks.

**Numerical models.** Extracted models include an integrated offshore-to-overtopping chain using EurOtop, HEC-RAS 5.0.7 2D, GCM ensembles coupled to Bruun-rule/GIS translation, and pyCIAM. Conceptual and review frameworks cover indirect impacts, WAMPUM, habitat-compensation robustness and institutional barriers.

**Experimental datasets.** This branch is dominated by field-derived and scenario datasets rather than laboratory experiments: the 2007 Walcott flood, Oakland topography/groundwater/rainfall data, 13 Indian port-adjacent beach segments, UK habitat-compensation records, Chinese coastal economic/geographic inputs and reviewed Australian and Tribal adaptation evidence.

**Validated ranges.** Quantitative findings are bounded to their sources: Walcott 0.35–1 m SLR cases; Oakland 1 m SLR, 1.94 m high tide and 2-year rainfall; Indian RCP4.5/RCP8.5 projections through 2100; and pyCIAM strategies along China's segmented coast. These ranges are scenarios, not universal thresholds.

**Recent advances.** Recent work couples groundwater emergence with urban rainfall flooding, evaluates flexible adaptation portfolios at national scale, tests ecological compensation against robustness principles, centers Tribal sovereignty and water security, and systematically diagnoses institutional barriers rather than treating adaptation as an unconstrained model choice.

**Disagreements.** The literature differs less on whether impacts grow than on representation and response: static area accounting versus ecological function, autonomous optimization versus governance feasibility, equilibrium shoreline rules versus process-rich morphology, and generic technical planning versus sovereign community-grounded adaptation.

**Limitations.** Recurring limitations are climate and socioeconomic scenario uncertainty, static exposure, omitted compound drivers, simplified groundwater or morphology, empirical overtopping, discounting and valuation choices, incomplete monitoring, publication bias, qualitative causal chains and transfer of governance conclusions across communities.

**Open questions.** Priorities include coupled groundwater-surface-coastal validation, dynamic morphology and habitat succession, correlated extremes, adaptation tipping points, distributional and indirect losses, Indigenous data sovereignty, monitoring of compensation performance, governance implementation and transparent propagation of deep uncertainty.

**Seminal papers.** The 2012 Walcott analysis demonstrated how modest freeboard loss can radically change overtopping recurrence, while the UK indirect-impact study broadened coastal assessment beyond direct local damage. Together they frame physical amplification and cross-border propagation.

## Equations

### Climate-conditioned coastal impact mapping

$$
I = f(\Delta S, H_s, T, P, G, E, V, A)
$$

Regime: Peer-reviewed literature on Australian coastal settlements included by the review protocol.

Variables: `I` coastal impact metric; `Delta S` sea-level change; `H_s` wave climate; `T` tide and surge; `P` precipitation; `G` groundwater response; `E` exposure; `V` vulnerability; `A` adaptation

Source: (Kazeminia 2026, [doi:10.1002/wcc.70053](https://doi.org/10.1002/wcc.70053))

### Climate-conditioned coastal impact mapping

$$
I = f(\Delta S, H_s, T, P, G, E, V, A)
$$

Regime: pyCIAM coastal segments, modeled protection/retreat/no-adaptation choices and Chinese geographic/economic inputs through 2100.

Variables: `I` coastal impact metric; `Delta S` sea-level change; `H_s` wave climate; `T` tide and surge; `P` precipitation; `G` groundwater response; `E` exposure; `V` vulnerability; `A` adaptation

Source: (Wang 2025, [doi:10.1016/j.accre.2025.06.005](https://doi.org/10.1016/j.accre.2025.06.005))

### Climate-conditioned coastal impact mapping

$$
I = f(\Delta S, H_s, T, P, G, E, V, A)
$$

Regime: Walcott seawall geometry, mesotidal setting, selected future climate projections and 0.35–1.0 m sea-level-rise cases.

Variables: `I` coastal impact metric; `Delta S` sea-level change; `H_s` wave climate; `T` tide and surge; `P` precipitation; `G` groundwater response; `E` exposure; `V` vulnerability; `A` adaptation

Source: (Chini 2012, [doi:10.1016/j.coastaleng.2012.02.009](https://doi.org/10.1016/j.coastaleng.2012.02.009))

### Climate-conditioned coastal impact mapping

$$
I = f(\Delta S, H_s, T, P, G, E, V, A)
$$

Regime: UK Habitats Directive compensation and Shoreline Management Plan context.

Variables: `I` coastal impact metric; `Delta S` sea-level change; `H_s` wave climate; `T` tide and surge; `P` precipitation; `G` groundwater response; `E` exposure; `V` vulnerability; `A` adaptation

Source: (Brown 2022, [doi:10.1016/j.ocecoaman.2022.106072](https://doi.org/10.1016/j.ocecoaman.2022.106072))

### Climate-conditioned coastal impact mapping

$$
I = f(\Delta S, H_s, T, P, G, E, V, A)
$$

Regime: Selected sandy beach segments near 13 Indian ports, GCM ensemble projections and equilibrium-profile assumptions through 2100.

Variables: `I` coastal impact metric; `Delta S` sea-level change; `H_s` wave climate; `T` tide and surge; `P` precipitation; `G` groundwater response; `E` exposure; `V` vulnerability; `A` adaptation

Source: (Patil 2020, [doi:10.1061/(asce)ww.1943-5460.0000586](https://doi.org/10.1061/(asce)ww.1943-5460.0000586))

### Climate-conditioned coastal impact mapping

$$
I = f(\Delta S, H_s, T, P, G, E, V, A)
$$

Regime: UK exposure to overseas coastal impacts under alternative climate, socioeconomic and adaptation outcomes.

Variables: `I` coastal impact metric; `Delta S` sea-level change; `H_s` wave climate; `T` tide and surge; `P` precipitation; `G` groundwater response; `E` exposure; `V` vulnerability; `A` adaptation

Source: (Nicholls 2012, [doi:10.1080/14693062.2012.728792](https://doi.org/10.1080/14693062.2012.728792))

### Climate-conditioned coastal impact mapping

$$
I = f(\Delta S, H_s, T, P, G, E, V, A)
$$

Regime: Eastern US coastal Tribal contexts; principles require Nation-specific governance and knowledge protocols.

Variables: `I` coastal impact metric; `Delta S` sea-level change; `H_s` wave climate; `T` tide and surge; `P` precipitation; `G` groundwater response; `E` exposure; `V` vulnerability; `A` adaptation

Source: (Leonard 2021, [doi:10.1080/17565529.2020.1862739](https://doi.org/10.1080/17565529.2020.1862739))

### Climate-conditioned coastal impact mapping

$$
I = f(\Delta S, H_s, T, P, G, E, V, A)
$$

Regime: Oakland Flatlands topography, prescribed groundwater-inundation footprint, 1.94 m high tide, 1 m SLR and 2-year precipitation.

Variables: `I` coastal impact metric; `Delta S` sea-level change; `H_s` wave climate; `T` tide and surge; `P` precipitation; `G` groundwater response; `E` exposure; `V` vulnerability; `A` adaptation

Source: (Rahimi 2020, [doi:10.3390/w12102776](https://doi.org/10.3390/w12102776))

## Claims

- **C330.** For the Walcott seawall case, the estimated return period of an overtopping event comparable to the November 2007 event fell from 100 years to about 5 years under 0.35 m of sea-level rise and to just over 1 year under 1 m; projected overtopping change was more sensitive to water-level change than to significant-wave-height change. *Regime: Walcott seawall geometry, mesotidal setting, selected future climate projections and 0.35–1.0 m sea-level-rise cases..* [direct_finding, numerical] (Chini 2012, [doi:10.1016/j.coastaleng.2012.02.009](https://doi.org/10.1016/j.coastaleng.2012.02.009))
- **C331.** In the modeled Oakland Flatlands case, combining 1 m sea-level rise, sea-level-driven groundwater rise, high tide and a 2-year precipitation event exceeded drainage capacity and flooded more than 700 acres of built infrastructure, substantially more than scenarios omitting compound groundwater effects. *Regime: Oakland Flatlands topography, prescribed groundwater-inundation footprint, 1.94 m high tide, 1 m SLR and 2-year precipitation..* [direct_finding, numerical] (Rahimi 2020, [doi:10.3390/w12102776](https://doi.org/10.3390/w12102776))
- **C332.** A United Kingdom assessment found that overseas coastal climate impacts can propagate nationally through supply-chain disruption, migration and security pressures, finance and insurance losses, while also creating export opportunities for coastal-hazard and management expertise; outcomes depend on climate, socioeconomic change and adaptation success. *Regime: UK exposure to overseas coastal impacts under alternative climate, socioeconomic and adaptation outcomes..* [literature_review_statement, review] (Nicholls 2012, [doi:10.1080/14693062.2012.728792](https://doi.org/10.1080/14693062.2012.728792))
- **C333.** The WAMPUM framework argues that sea-level-rise adaptation for eastern coastal Tribal Nations must center Indigenous knowledge, sovereignty, cultural values and relationships to water rather than apply externally imposed technical planning alone. *Regime: Eastern US coastal Tribal contexts; principles require Nation-specific governance and knowledge protocols..* [direct_finding, mixed] (Leonard 2021, [doi:10.1080/17565529.2020.1862739](https://doi.org/10.1080/17565529.2020.1862739))
- **C334.** Across beach segments near 13 Indian ports, projected absolute sea-level-rise rates were 3.38–5.16 mm/yr under RCP4.5 and 5.36–7.20 mm/yr under RCP8.5; Bruun-rule recession by 2100 was 14.10–29.22 m and 21.05–45.40 m, respectively. *Regime: Selected sandy beach segments near 13 Indian ports, GCM ensemble projections and equilibrium-profile assumptions through 2100..* [direct_finding, analytical] (Patil 2020, [doi:10.1061/(asce)ww.1943-5460.0000586](https://doi.org/10.1061/(asce)ww.1943-5460.0000586))
- **C335.** For United Kingdom shoreline-management habitat compensation, simple area-based balance sheets can overstate adaptation progress because they omit uncertainty and ecological functioning, integrity and coherence; robust compensation requires monitoring, transparency, flexible pathways and scenario-based planning. *Regime: UK Habitats Directive compensation and Shoreline Management Plan context..* [literature_review_statement, review] (Brown 2022, [doi:10.1016/j.ocecoaman.2022.106072](https://doi.org/10.1016/j.ocecoaman.2022.106072))
- **C336.** In a refined pyCIAM assessment of China's coast, locally optimized adaptation reduced cumulative national sea-level-rise losses by 2100 from about US$4.5 trillion without adaptation to below US$0.9 trillion; flexible strategies reduced losses by up to 86%, with especially large modeled reductions in Shanghai, Jiangsu and Zhejiang. *Regime: pyCIAM coastal segments, modeled protection/retreat/no-adaptation choices and Chinese geographic/economic inputs through 2100..* [direct_finding, numerical] (Wang 2025, [doi:10.1016/j.accre.2025.06.005](https://doi.org/10.1016/j.accre.2025.06.005))
- **C337.** A systematic review of Australian coastal-settlement adaptation identified unclear and inconsistent national/state guidance and weak stakeholder coordination as recurring institutional barriers that foster adaptation inertia; it calls for integrated governance, inter-agency communication and coordinated policy. *Regime: Peer-reviewed literature on Australian coastal settlements included by the review protocol..* [literature_review_statement, review] (Kazeminia 2026, [doi:10.1002/wcc.70053](https://doi.org/10.1002/wcc.70053))
- **C1133.** Scenario projections to 2030 and 2060 place the largest absolute low-elevation coastal-zone and 100-year-flood exposure in Asia, while Africa has the highest projected rates of coastal population growth and urbanization. *Regime: Future Coastal Population Growth and Exposure to Sea-Level Rise and Coastal Flooding - A Global Assessment.* [direct_finding, mixed] (Barbara Neumann 2015, [doi:10.1371/journal.pone.0118571](https://doi.org/10.1371/journal.pone.0118571))
- **C1134.** Using the neural-network-corrected CoastalDEM triples SRTM-based global exposure estimates; under low emissions an estimated 190 million people occupy land below projected 2100 high-tide lines, and under high emissions as many as 630 million occupy land below projected annual-flood levels. *Regime: New elevation data triple estimates of global vulnerability to sea-level rise and coastal flooding.* [direct_finding, mixed] (Scott Kulp 2019, [doi:10.1038/s41467-019-12808-z](https://doi.org/10.1038/s41467-019-12808-z))
- **C1137.** Extreme-value analysis including waves, tides and surge indicates that 10–20 cm of sea-level rise expected by 2050 can more than double extreme-water-level frequency in many tropical coasts with short-tailed present-day distributions. *Regime: Doubling of coastal flooding frequency within decades due to sea-level rise.* [direct_finding, mixed] (Sean Vitousek 2017, [doi:10.1038/s41598-017-01362-7](https://doi.org/10.1038/s41598-017-01362-7))
- **C1138.** A Coastal City Flood Vulnerability Index combines exposure, susceptibility and resilience across hydro-geological, socioeconomic and politico-administrative components on a 0–1 comparative scale and was demonstrated for nine cities. *Regime: A flood vulnerability index for coastal cities and its use in assessing climate change impacts.* [direct_finding, mixed] (Stefania Balica 2012, [doi:10.1007/s11069-012-0234-1](https://doi.org/10.1007/s11069-012-0234-1))
- **C1140.** Under mean RCP8.5 with no protection or adaptation, global tide-surge-wave-setup modeling projects that land area, population and assets at risk of episodic flooding increase by 48%, 52% and 46%, respectively, by 2100. *Regime: Projections of global-scale extreme sea levels and resulting episodic coastal flooding over the 21st Century.* [direct_finding, mixed] (Ebru Kirezci 2020, [doi:10.1038/s41598-020-67736-6](https://doi.org/10.1038/s41598-020-67736-6))
- **C1141.** A Bangladesh assessment combines a 119-year cyclone record with storm-surge scenarios and qualitative erosion and backwater analyses to examine climate impacts and adaptation options. *Regime: Climate change impacts and adaptation assessment in Bangladesh.* [direct_finding, mixed] (Ahmed Ali 1999, [doi:10.3354/cr012109](https://doi.org/10.3354/cr012109))
- **C1142.** A 30 m national US framework jointly models pluvial, fluvial and coastal hazards for current, 2035 and 2050 RCP4.5 conditions; validation against local and FEMA maps produced Critical Success Index values of 0.69–0.82. *Regime: Combined Modeling of US Fluvial, Pluvial, and Coastal Flood Hazard Under Current and Future Climates.* [direct_finding, mixed] (Paul Bates 2020, [doi:10.1029/2020wr028673](https://doi.org/10.1029/2020wr028673))
- **C1143.** Of 49 low-lying Mediterranean cultural World Heritage sites, 37 are currently at risk from a 100-year flood and 42 from erosion; aggregate flood and erosion risk may rise 50% and 13% by 2100. *Regime: Mediterranean UNESCO World Heritage at risk from coastal flooding and erosion due to sea-level rise.* [direct_finding, mixed] (Lena Reimann 2018, [doi:10.1038/s41467-018-06645-9](https://doi.org/10.1038/s41467-018-06645-9))
- **C1144.** A Cape May County GIS analysis combines riverine and surge inundation with social vulnerability and shows that sea-level rise and poorly managed development increase exposure of people, property and critical facilities. *Regime: Vulnerability of coastal communities to sea-level rise: a case study of Cape May County, New Jersey, USA.* [direct_finding, mixed] (SY Wu 2002, [doi:10.3354/cr022255](https://doi.org/10.3354/cr022255))
- **C1146.** For California, integrating sea-level rise, tides, waves, storms, erosion and cliff retreat yields up to 600,000 people and more than $150 billion in property exposed by 2100—about three times the population from static sea-level analysis. *Regime: Dynamic flood modeling essential to assess the coastal impacts of climate change.* [direct_finding, mixed] (Patrick Barnard 2019, [doi:10.1038/s41598-019-40742-z](https://doi.org/10.1038/s41598-019-40742-z))
- **C1147.** Flood-threshold exceedance odds grow exponentially with sea-level rise; the present US 50-year level is projected to be exceeded annually before 2050 along about 70% of the coast and nearly daily at peak tide before 2100 along 90%. *Regime: Sea-level rise exponentially increases coastal flood frequency.* [direct_finding, mixed] (Mohsen Taherkhani 2020, [doi:10.1038/s41598-020-62188-4](https://doi.org/10.1038/s41598-020-62188-4))
- **C1409.** A review of open sandy coasts organizes climate impacts through changes in sea level, storms, waves and sediment budgets and emphasizes coupled local shoreline response. *Regime: Assessing climate change impacts on open sandy coasts: A review.* [literature_review_statement, review] (Roshanka Ranasinghe 2016, [doi:10.1016/j.earscirev.2016.07.011](https://doi.org/10.1016/j.earscirev.2016.07.011))
- **C1429.** The Baltic Sea provides a long-record test case showing how interacting warming and anthropogenic pressures can offset coastal ecosystem-management gains. *Regime: The Baltic Sea as a time machine for the future coastal ocean.* [literature_review_statement, review] (Thorsten B. H. Reusch 2018, [doi:10.1126/sciadv.aar8195](https://doi.org/10.1126/sciadv.aar8195))
- **C1430.** A global synthesis links coastal hypoxia susceptibility to stratification, nutrient and organic loading, and restricted exchange, with nonlinear ecosystem consequences. *Regime: Natural and human-induced hypoxia and consequences for coastal areas: synthesis and future development.* [literature_review_statement, review] (J. Zhang 2010, [doi:10.5194/bg-7-1443-2010](https://doi.org/10.5194/bg-7-1443-2010))
- **C1519.** A review synthesizes climate-change impacts on marine foundation species that structure coastal habitats and ecosystem services. *Regime: Impacts of Climate Change on Marine Foundation Species.* [literature_review_statement, review] (Thomas Wernberg 2023, [doi:10.1146/annurev-marine-042023-093037](https://doi.org/10.1146/annurev-marine-042023-093037))
- **C1520.** Arctic shelf observations constrain subsea-permafrost degradation and gas-migration pathways controlling methane release after marine inundation. *Regime: Current rates and mechanisms of subsea permafrost degradation in the East Siberian Arctic Shelf.* [direct_finding, field] (Natalia Shakhova 2017, [doi:10.1038/ncomms15872](https://doi.org/10.1038/ncomms15872))
- **C1662.** Eelgrass protects sedimentary organic carbon only when canopy density is high: sparse canopies allow greater erosion and carbon resuspension, oscillatory flow releases more particulate carbon than unidirectional flow, and most mobilized upper-sediment carbon can remineralize rapidly. *Regime: Laboratory eelgrass sediments with documented low/high shoot density under progressively increased unidirectional and oscillatory hydrodynamics..* [direct_finding, experimental] (Luis G. Egea 2023, [doi:10.1016/j.scitotenv.2023.165976](https://doi.org/10.1016/j.scitotenv.2023.165976))
- **C1668.** Coastal-wetland response to sea-level rise, storms and altered freshwater, sediment and nutrient input is mediated by geomorphic-biological feedbacks and human modifications; resilience depends on whether accretion, migration and ecological adjustment can keep pace with forcing. *Regime: Coastal and estuarine wetlands exposed to sea-level, storm and watershed-input changes under interacting human modification..* [literature_review_statement, review] (John W. Day 2008, [doi:10.1007/s12237-008-9047-6](https://doi.org/10.1007/s12237-008-9047-6))
- **C1690.** A national InVEST coastal-exposure index for Ireland shows exposure is locally controlled by shoreline, metocean and climate factors; modeled coastal habitats potentially reduce exposure along 38% of the assessed coast, while dense eastern populations remain highly exposed despite stronger Atlantic forcing in the west. *Regime: Relative national-scale screening of the Republic of Ireland coastline using the documented physical, climatic, habitat and population datasets..* [direct_finding, numerical] (Walsh 2026, [doi:10.1007/s11069-026-08361-w](https://doi.org/10.1007/s11069-026-08361-w))
- **C1737.** Relative sea-level rise is likely the dominant future climate threat to mangroves where sediment-surface elevation cannot keep pace and landward migration is constrained; resilience can be increased through migration space, catchment and stressor management, rehabilitation, protected-area networks, and standardized regional monitoring. *Regime: Intertidal mangrove systems worldwide, with vulnerability evidence concentrated in the western Pacific and Wider Caribbean and greatest risk where elevation is declining or inland migration is blocked..* [literature_review_statement, review] (Eric Gilman 2008, [doi:10.1016/j.aquabot.2007.12.009](https://doi.org/10.1016/j.aquabot.2007.12.009))
- **C1750.** Circum-Arctic coastal erosion is spatially heterogeneous and cannot be explained by a single mapped factor; wave and storm-surge exposure, sea-ice protection, permafrost and ground ice, sediment properties, and coastal geometry interact locally to control retreat and coastal material fluxes. *Regime: Permafrost-affected Arctic coastlines bordering the Arctic Ocean, including consolidated, unconsolidated, ice-rich, low-lying, and cliffed segments under varying sea-ice and storm exposure..* [direct_finding, field] (Hugues Lantuit 2011, [doi:10.1007/s12237-010-9362-6](https://doi.org/10.1007/s12237-010-9362-6))

## Papers

- Barbara Neumann (2015). Future Coastal Population Growth and Exposure to Sea-Level Rise and Coastal Flooding - A Global Assessment. *PLoS ONE*. [doi:10.1371/journal.pone.0118571](https://doi.org/10.1371/journal.pone.0118571)
- Scott Kulp (2019). New elevation data triple estimates of global vulnerability to sea-level rise and coastal flooding. *Nature Communications*. [doi:10.1038/s41467-019-12808-z](https://doi.org/10.1038/s41467-019-12808-z)
- Eric Gilman (2008). Threats to mangroves from climate change and adaptation options: A review. *Aquatic Botany*. [doi:10.1016/j.aquabot.2007.12.009](https://doi.org/10.1016/j.aquabot.2007.12.009)
- Sean Vitousek (2017). Doubling of coastal flooding frequency within decades due to sea-level rise. *Scientific Reports*. [doi:10.1038/s41598-017-01362-7](https://doi.org/10.1038/s41598-017-01362-7)
- Stefania Balica (2012). A flood vulnerability index for coastal cities and its use in assessing climate change impacts. *Natural Hazards*. [doi:10.1007/s11069-012-0234-1](https://doi.org/10.1007/s11069-012-0234-1)
- Ebru Kirezci (2020). Projections of global-scale extreme sea levels and resulting episodic coastal flooding over the 21st Century. *Scientific Reports*. [doi:10.1038/s41598-020-67736-6](https://doi.org/10.1038/s41598-020-67736-6)
- Thorsten B. H. Reusch (2018). The Baltic Sea as a time machine for the future coastal ocean. *Science Advances*. [doi:10.1126/sciadv.aar8195](https://doi.org/10.1126/sciadv.aar8195)
- J. Zhang (2010). Natural and human-induced hypoxia and consequences for coastal areas: synthesis and future development. *Biogeosciences*. [doi:10.5194/bg-7-1443-2010](https://doi.org/10.5194/bg-7-1443-2010)
- Hugues Lantuit (2011). The Arctic Coastal Dynamics Database: A New Classification Scheme and Statistics on Arctic Permafrost Coastlines. *Estuaries and Coasts*. [doi:10.1007/s12237-010-9362-6](https://doi.org/10.1007/s12237-010-9362-6)
- Paul Bates (2020). Combined Modeling of US Fluvial, Pluvial, and Coastal Flood Hazard Under Current and Future Climates. *Water Resources Research*. [doi:10.1029/2020wr028673](https://doi.org/10.1029/2020wr028673)
- Ahmed Ali (1999). Climate change impacts and adaptation assessment in Bangladesh. *Climate Research*. [doi:10.3354/cr012109](https://doi.org/10.3354/cr012109)
- Roshanka Ranasinghe (2016). Assessing climate change impacts on open sandy coasts: A review. *Earth-Science Reviews*. [doi:10.1016/j.earscirev.2016.07.011](https://doi.org/10.1016/j.earscirev.2016.07.011)
- Lena Reimann (2018). Mediterranean UNESCO World Heritage at risk from coastal flooding and erosion due to sea-level rise. *Nature Communications*. [doi:10.1038/s41467-018-06645-9](https://doi.org/10.1038/s41467-018-06645-9)
- SY Wu (2002). Vulnerability of coastal communities to sea-level rise: a case study of Cape May County, New Jersey, USA. *Climate Research*. [doi:10.3354/cr022255](https://doi.org/10.3354/cr022255)
- Patrick Barnard (2019). Dynamic flood modeling essential to assess the coastal impacts of climate change. *Scientific Reports*. [doi:10.1038/s41598-019-40742-z](https://doi.org/10.1038/s41598-019-40742-z)
- John W. Day (2008). Consequences of Climate Change on the Ecogeomorphology of Coastal Wetlands. *Estuaries and Coasts*. [doi:10.1007/s12237-008-9047-6](https://doi.org/10.1007/s12237-008-9047-6)
- Mohsen Taherkhani (2020). Sea-level rise exponentially increases coastal flood frequency. *Scientific Reports*. [doi:10.1038/s41598-020-62188-4](https://doi.org/10.1038/s41598-020-62188-4)
- Thomas Wernberg (2023). Impacts of Climate Change on Marine Foundation Species. *Annual Review of Marine Science*. [doi:10.1146/annurev-marine-042023-093037](https://doi.org/10.1146/annurev-marine-042023-093037)
- Natalia Shakhova (2017). Current rates and mechanisms of subsea permafrost degradation in the East Siberian Arctic Shelf. *Nature Communications*. [doi:10.1038/ncomms15872](https://doi.org/10.1038/ncomms15872)
- Chini (2012). Extreme values of coastal wave overtopping accounting for climate change and sea level rise. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2012.02.009](https://doi.org/10.1016/j.coastaleng.2012.02.009)
- Rahimi (2020). Compound Inundation Impacts of Coastal Climate Change: Sea-Level Rise, Groundwater Rise, and Coastal Precipitation. *Water*. [doi:10.3390/w12102776](https://doi.org/10.3390/w12102776)
- Luis G. Egea (2023). Loss of POC and DOC on seagrass sediments by hydrodynamics. *The Science of The Total Environment*. [doi:10.1016/j.scitotenv.2023.165976](https://doi.org/10.1016/j.scitotenv.2023.165976)
- Nicholls (2012). Indirect impacts of coastal climate change and sea-level rise: the UK example. *Climate Policy*. [doi:10.1080/14693062.2012.728792](https://doi.org/10.1080/14693062.2012.728792)
- Leonard (2021). WAMPUM Adaptation framework: eastern coastal Tribal Nations and sea level rise impacts on water security. *Climate and Development*. [doi:10.1080/17565529.2020.1862739](https://doi.org/10.1080/17565529.2020.1862739)
- Patil (2020). Sea Level Rise and Shoreline Change under Changing Climate Along the Indian Coastline. *Journal of Waterway, Port, Coastal, and Ocean Engineering*. [doi:10.1061/(asce)ww.1943-5460.0000586](https://doi.org/10.1061/(asce)ww.1943-5460.0000586)
- ... and 21 more in `pycoapedia.sqlite` (table `paper_topics`).
