# Consequences and loss

`risk.consequences` | Human, economic, and infrastructure impacts.

Parent: [Coastal hazards and risk](risk.md)

Papers: 21. Claims: 17. Equations: 1.

## Synthesis

**Well established.** Coastal consequence assessment must explicitly connect hazard intensity to exposed receptors and an impact metric. Direct physical damage, network-service loss, livelihood loss, indirect economic disruption and systemic effects are distinct endpoints and should not be collapsed without a stated aggregation rule.

**Governing physics.** Storm waves, water levels, erosion, overwash, inundation, hurricane wind, debris transport and seasonal ice govern the retained cases. Consequences emerge only after these processes interact with asset location, fragility, network topology, ecosystem production or operational exposure.

**Dimensionless parameters.** Hazard and exposure indices, conditional damage ratios, exceedance probability, return period, normalized connectivity loss and intervention-effect ratios organize comparisons; their definitions and normalization are study-specific and are not interchangeable by default.

**Major equations.** Common forms include risk as event probability times conditional consequence, indicator combinations such as CI=sqrt(i_hazard i_exposure), depth- or intensity-damage functions, Bayesian conditional probabilities, network-connectivity loss and discounted or cumulative economic-loss accounting.

**Typical methods.** The evidence spans regional indicator screening followed by process modelling, Bayesian-network surrogates, probabilistic debris and transport-network analysis, GIS exposure overlays, economic accounting, and coupled property/labor loss simulation.

**Numerical models.** XBeach and LISFLOOD-FP support detailed hotspot analysis; Bayesian networks emulate morphodynamic scenario chains; debris, fragility and graph models estimate road service loss; GIS and probabilistic hurricane models join hazard fields to spatial assets and economic quantities.

**Experimental datasets.** Case evidence covers ten European RISC-KIT sites, Ria Formosa barrier scenarios, Galveston roads and emergency facilities, Québec municipal asset inventories, Mississippi oyster landings and revenue, eastern North Carolina property and labor data, and mapped Alaskan nearshore-ice zones.

**Validated ranges.** Evidence is bounded to the reported cases: European screening sectors near 1 km and hotspots of 1–10 km; a Ria Formosa 50-year storm plus spring tide; a representative Galveston 500-year hurricane; Mississippi fishery impacts from 2005–2016; and each study's mapped asset inventory.

**Recent advances.** Recent work adds debris-mediated network disruption and jointly maps property and labor consequences, while building-level adaptive pathways update decisions as sea-level projections change. The advance is increasingly explicit coupling among physical hazards, exposed systems and decisions rather than hazard mapping alone.

**Disagreements.** The studies do not establish one universal consequence measure. Exposure-only maps omit fragility and welfare loss, asset-value loss can dominate modeled totals while obscuring social vulnerability, and hazard inventories such as ice zonation identify potential harm without estimating realized loss.

**Limitations.** Transfer is constrained by local inventories, vulnerability functions, economic valuation, network topology, scenario discretization and model-form uncertainty. Indirect, intangible, distributional and recovery consequences remain inconsistently represented, and abstract-limited sources support fewer implementation details.

**Open questions.** Priorities include transferable multi-sector consequence functions, uncertainty propagation from hazard through recovery, treatment of cascading infrastructure failures, ecosystem-service and intangible loss, distributional welfare, behavioral adaptation, and validation against observed longitudinal recovery.

**Seminal papers.** The 1981 Alaskan ice-zonation study is an early engineering-hazard inventory. The 2017–2018 CRAF and Ria Formosa studies are central to multiscale and probabilistic coastal impact assessment because they connect regional screening, process models and risk-reduction choices.

## Equations

### Coastal risk index

$$
CI=\sqrt{i_{hazard}i_{exposure}}
$$

Regime: Ten RISC-KIT European case studies; approximately 1 km regional sectors and 1–10 km detailed hotspots.

Variables: `CI` coastal index; `i_hazard` normalized hazard indicator; `i_exposure` normalized exposure indicator

Source: (Viavattene 2018, [doi:10.1016/j.coastaleng.2017.09.002](https://doi.org/10.1016/j.coastaleng.2017.09.002))

## Claims

- **C291.** Across ten European case studies, the two-stage Coastal Risk Assessment Framework screened approximately 1 km coastal sectors and then modelled selected 1–10 km hotspots, identifying high-risk areas with only small deviations from locations already recognized as high risk. *Regime: Ten RISC-KIT European case studies; approximately 1 km regional sectors and 1–10 km detailed hotspots..* [direct_finding, mixed] (Viavattene 2018, [doi:10.1016/j.coastaleng.2017.09.002](https://doi.org/10.1016/j.coastaleng.2017.09.002))
- **C292.** For a 1-in-50-year storm coincident with spring tide at the Ria Formosa barrier, the Bayesian-network surrogate estimated that partial house removal reduced overwash by 15% and erosion by 58%, nourishment reduced overwash by 16% and erosion by 96%, and the combined intervention reduced both impacts to nearly zero. *Regime: Ria Formosa coastal barrier under the tested 1-in-50-year storm plus spring tide and specified interventions..* [direct_finding, mixed] (Plomaritis 2018, [doi:10.1016/j.coastaleng.2017.07.003](https://doi.org/10.1016/j.coastaleng.2017.07.003))
- **C293.** In the Galveston transportation case for a representative 500-year hurricane, estimated loss of road connectivity to emergency facilities increased from about 2% when debris was omitted to about 17% when hurricane debris and road damage were jointly represented. *Regime: Galveston, Texas, transportation network under the study representative 500-year hurricane..* [direct_finding, mixed] (Amini 2023, [doi:10.1016/j.ress.2023.109579](https://doi.org/10.1016/j.ress.2023.109579))
- **C294.** For the Québec case municipalities, a planner-co-designed GIS workflow combined coastal characterization, projected shoreline migration, and mapped buildings and infrastructure to identify assets exposed to coastal erosion and support land-use adaptation decisions. *Regime: The studied Québec coast and mapped buildings/infrastructure under the adopted erosion projection method..* [direct_finding, mixed] (Christian Fraser 2017, [doi:10.1080/19475705.2017.1294114](https://doi.org/10.1080/19475705.2017.1294114))
- **C295.** For the Mississippi commercial oyster fishery during 2005–2016, the study estimated cumulative direct coastal-hazard impacts of nearly USD 40 million, averaging approximately USD 3.3 million per year, associated with Katrina, the Deepwater Horizon spill, Bonnet Carré Spillway opening and a harmful algal bloom. *Regime: Mississippi commercial oyster fishery, 2005–2016, in the events and economic data considered..* [direct_finding, mixed] (Posadas 2020, [doi:10.15351/2373-8456.1115](https://doi.org/10.15351/2373-8456.1115))
- **C296.** Across eastern North Carolina's Coastal Area Management Act region, integrated probabilistic hurricane simulations, property data and labor-compensation estimates showed that spatial asset value was the primary determinant of total modeled economic consequences, despite concurrent relationships with social vulnerability. *Regime: Eastern North Carolina CAMA region under the study probabilistic hurricane simulations and property/labor datasets..* [direct_finding, mixed] (Liu 2024, [doi:10.1088/1748-9326/ad6d81](https://doi.org/10.1088/1748-9326/ad6d81))
- **C297.** Along the Beaufort, Chukchi and Bering coasts of Alaska, seasonal nearshore-ice morphology maps delineated zones of statistically uniform ice behavior and related each zone to coastal processes and bathymetric configuration to identify ice features hazardous to outer-continental-shelf oil and gas development. *Regime: Seasonal nearshore ice on the Beaufort, Chukchi and Bering coasts of Alaska..* [direct_finding, mixed] (Stringer 1981, [doi:10.1016/0378-3839(81)90017-x](https://doi.org/10.1016/0378-3839(81)90017-x))
- **C1219.** Globally about 27% of road and rail assets are exposed to at least one hazard and 7.5% to a 100-year flood; direct expected annual damage is $3.1–22 billion, roughly 73% from surface and river flooding. *Regime: A global multi-hazard risk analysis of road and railway infrastructure assets.* [direct_finding, mixed] (Elco Koks 2019, [doi:10.1038/s41467-019-10442-3](https://doi.org/10.1038/s41467-019-10442-3))
- **C1224.** A 2000–2019 coastal-tourism review finds highly heterogeneous physical and socioeconomic climate impacts across destinations and methods, with important indicators and causal links still overlooked. *Regime: Climate change, coastal tourism, and impact chains – a literature review.* [direct_finding, mixed] (Anastasia Arabadzhyan 2020, [doi:10.1080/13683500.2020.1825351](https://doi.org/10.1080/13683500.2020.1825351))
- **C1228.** British flood and failure records support bridge-scour fragility curves coupled to spatial joint flood probabilities and passenger-disruption models for network-wide failure and economic risk. *Regime: A Probabilistic Model of the Economic Risk to Britain's Railway Network from Bridge Scour During Floods.* [direct_finding, mixed] (Rob Lamb 2019, [doi:10.1111/risa.13370](https://doi.org/10.1111/risa.13370))
- **C1346.** High-resolution U.S. modeling estimates climate change alone raises flood risk 26.4% by 2050 under RCP4.5; future increases disproportionately affect Black communities and remain concentrated along Atlantic and Gulf coasts. *Regime: Inequitable patterns of US flood risk in the Anthropocene.* [direct_finding, numerical] (Oliver Wing 2022, [doi:10.1038/s41558-021-01265-6](https://doi.org/10.1038/s41558-021-01265-6))
- **C1347.** A global delta dataset estimates 339 million residents in 2017; 31 million delta residents face tropical-cyclone flooding, 92% in developing or least-developed economies and 25 million on sediment-starved deltas. *Regime: Coastal flooding will disproportionately impact people on river deltas.* [direct_finding, mixed] (Douglas A. Edmonds 2020, [doi:10.1038/s41467-020-18531-4](https://doi.org/10.1038/s41467-020-18531-4))
- **C1385.** A coastal eutrophication synthesis links expanding nutrient enrichment to ecological degradation and human consequences and frames globalization of coastal nutrient pressures as a management risk. *Regime: The Globalization of Cultural Eutrophication in the Coastal Ocean: Causes and Consequences.* [literature_review_statement, review] (Thomas C. Malone 2020, [doi:10.3389/fmars.2020.00670](https://doi.org/10.3389/fmars.2020.00670))
- **C1386.** A coastal-risk review identifies population growth and spatial development as dynamic exposure drivers that can amplify future risk independently of hazard change. *Regime: Population development as a driver of coastal risk: Current trends and future pathways.* [literature_review_statement, review] (Lena Reimann 2023, [doi:10.1017/cft.2023.3](https://doi.org/10.1017/cft.2023.3))
- **C1404.** Global extreme-coastal-water-level analysis identifies widespread potential overtopping exposure and connects local extremes to tide, surge, wave and relative sea-level contributions. *Regime: A global analysis of extreme coastal water levels with implications for potential coastal overtopping.* [direct_finding, numerical] (Rafaël Almar 2021, [doi:10.1038/s41467-021-24008-9](https://doi.org/10.1038/s41467-021-24008-9))
- **C1516.** A Bangladesh coastal assessment links cyclone exposure to persistent risks for mortality and livelihoods despite large reductions in fatalities over time. *Regime: Assessing Risks from Cyclones for Human Lives and Livelihoods in the Coastal Region of Bangladesh.* [direct_finding, mixed] (Mohammad Abdul Quader 2017, [doi:10.3390/ijerph14080831](https://doi.org/10.3390/ijerph14080831))
- **C1627.** Tourism-dependent beaches face coupled erosion, infrastructure and economic losses; a review concludes that hard and soft protection must be matched to sediment and hydrodynamic processes and embedded in integrated coastal-zone management rather than selected as isolated engineering fixes. *Regime: Tourism beaches and coastal infrastructure exposed to erosion, storms and sea-level rise..* [literature_review_statement, review] (Michael R. Phillips 2005, [doi:10.1016/j.tourman.2005.10.019](https://doi.org/10.1016/j.tourman.2005.10.019))

## Papers

- Elco Koks (2019). A global multi-hazard risk analysis of road and railway infrastructure assets. *Nature Communications*. [doi:10.1038/s41467-019-10442-3](https://doi.org/10.1038/s41467-019-10442-3)
- Thomas C. Malone (2020). The Globalization of Cultural Eutrophication in the Coastal Ocean: Causes and Consequences. *Frontiers in Marine Science*. [doi:10.3389/fmars.2020.00670](https://doi.org/10.3389/fmars.2020.00670)
- Oliver Wing (2022). Inequitable patterns of US flood risk in the Anthropocene. *Nature Climate Change*. [doi:10.1038/s41558-021-01265-6](https://doi.org/10.1038/s41558-021-01265-6)
- Douglas A. Edmonds (2020). Coastal flooding will disproportionately impact people on river deltas. *Nature Communications*. [doi:10.1038/s41467-020-18531-4](https://doi.org/10.1038/s41467-020-18531-4)
- Michael R. Phillips (2005). Erosion and tourism infrastructure in the coastal zone: Problems, consequences and management. *Tourism Management*. [doi:10.1016/j.tourman.2005.10.019](https://doi.org/10.1016/j.tourman.2005.10.019)
- Anastasia Arabadzhyan (2020). Climate change, coastal tourism, and impact chains – a literature review. *Current Issues in Tourism*. [doi:10.1080/13683500.2020.1825351](https://doi.org/10.1080/13683500.2020.1825351)
- Rafaël Almar (2021). A global analysis of extreme coastal water levels with implications for potential coastal overtopping. *Nature Communications*. [doi:10.1038/s41467-021-24008-9](https://doi.org/10.1038/s41467-021-24008-9)
- Lena Reimann (2023). Population development as a driver of coastal risk: Current trends and future pathways. *Cambridge Prisms Coastal Futures*. [doi:10.1017/cft.2023.3](https://doi.org/10.1017/cft.2023.3)
- Rob Lamb (2019). A Probabilistic Model of the Economic Risk to Britain's Railway Network from Bridge Scour During Floods. *Risk Analysis*. [doi:10.1111/risa.13370](https://doi.org/10.1111/risa.13370)
- Mohammad Abdul Quader (2017). Assessing Risks from Cyclones for Human Lives and Livelihoods in the Coastal Region of Bangladesh. *International Journal of Environmental Research and Public Health*. [doi:10.3390/ijerph14080831](https://doi.org/10.3390/ijerph14080831)
- Viavattene (2018). Selecting coastal hotspots to storm impacts at the regional scale: a Coastal Risk Assessment Framework. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2017.09.002](https://doi.org/10.1016/j.coastaleng.2017.09.002)
- Plomaritis (2018). Use of a Bayesian Network for coastal hazards, impact and disaster risk reduction assessment at a coastal barrier (Ria Formosa, Portugal). *Coastal Engineering*. [doi:10.1016/j.coastaleng.2017.07.003](https://doi.org/10.1016/j.coastaleng.2017.07.003)
- Amini (2023). Probabilistic risk assessment of hurricane-induced debris impacts on coastal transportation infrastructure. *Reliability Engineering &amp; System Safety*. [doi:10.1016/j.ress.2023.109579](https://doi.org/10.1016/j.ress.2023.109579)
- Christian Fraser (2017). Development of a GIS coastal land-use planning tool for coastal erosion adaptation based on the exposure of buildings and infrastructure to coastal erosion, Québec, Canada. *Geomatics, Natural Hazards and Risk*. [doi:10.1080/19475705.2017.1294114](https://doi.org/10.1080/19475705.2017.1294114)
- Posadas (2020). Economic Impacts of Coastal Hazards on Mississippi Commercial Oyster Fishery from 2005 to 2016. *Journal of Ocean and Coastal Economics*. [doi:10.15351/2373-8456.1115](https://doi.org/10.15351/2373-8456.1115)
- Liu (2024). Unequal economic consequences of coastal hazards: hurricane impacts on North Carolina. *Environmental Research Letters*. [doi:10.1088/1748-9326/ad6d81](https://doi.org/10.1088/1748-9326/ad6d81)
- Stringer (1981). Morphology and hazards related to nearshore ice in coastal areas. *Coastal Engineering*. [doi:10.1016/0378-3839(81)90017-x](https://doi.org/10.1016/0378-3839(81)90017-x)
- Faith Ka Shun Chan (2018). Towards resilient flood risk management for Asian coastal cities: Lessons learned from Hong Kong and Singapore. *Journal of Cleaner Production*. [doi:10.1016/j.jclepro.2018.03.217](https://doi.org/10.1016/j.jclepro.2018.03.217)
- Jochen Hinkel (2010). Assessing risk of and adaptation to sea-level rise in the European Union: an application of DIVA. *Mitigation and Adaptation Strategies for Global Change*. [doi:10.1007/s11027-010-9237-y](https://doi.org/10.1007/s11027-010-9237-y)
- Leonardo Alfonso (2016). Probabilistic Flood Maps to support decision‐making: Mapping the Value of Information. *Water Resources Research*. [doi:10.1002/2015wr017378](https://doi.org/10.1002/2015wr017378)
- Han (2021). Building-level adaptation analysis under uncertain sea-level rise. *Climate Risk Management*. [doi:10.1016/j.crm.2021.100305](https://doi.org/10.1016/j.crm.2021.100305)
