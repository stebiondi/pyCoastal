# Warning and evacuation

`risk.evacuation` | Risk communication and evacuation behavior.

Parent: [Coastal hazards and risk](risk.md)

Papers: 10. Claims: 10. Equations: 7.

## Synthesis

**Well established.** Life safety depends on completing protective action before hazardous inundation or wind arrives. Warning issuance alone is insufficient: people must receive and understand the message, believe the threat and recommended action, decide and mobilize, traverse a capacity-limited network, and reach a safe, acceptable destination.

**Governing physics.** Storm-surge and tsunami depth, velocity, arrival time and spatial extent define unsafe areas and available lead time. Human and network processes—decision delay, walking or vehicle speed, route capacity, density, queues, shelter capacity and train movements—consume that lead time and can create secondary congestion risk.

**Dimensionless parameters.** Key measures include evacuation participation probability, warning reach and comprehension, compliance, normalized decision/clearance time relative to available lead time, volume-to-capacity ratio, pedestrian density, shelter occupancy ratio, completion fraction and casualty fraction.

**Major equations.** A clearance margin can be written M=T_arrival−T_warning−T_decision−T_clearance. Behavioral studies use logistic P(evacuate|x); network models use shortest paths, capacity and queue conservation; agent models update individual motion and density; railway assignment constrains each train to safe or evacuable stations before local arrival.

**Typical methods.** Evidence combines household questionnaires, map tests, pre/post-event interviews, logistic regression, Protective Action Decision Model variables, hydraulic-model coupling, GIS and network assignment, agent-based pedestrian simulation, supercomputing, route/shelter optimization and strategy scenarios.

**Numerical models.** THESEUS links hydraulic forecast fields to city evacuation plans and clearance simulation. The Japanese large-scale model resolves individuals, routes and shelters. The Sri Lanka algorithm assigns trains under spatially variable tsunami arrival, while logistic/PADM models estimate behavioral and shelter-use response.

**Experimental datasets.** The branch includes Texas hurricane-map surveys, typhoon storm-surge scenario interviews, pre-event and post-Iyonada records from two Kochi communities, Bordeaux and Cesenatico planning cases, a 340,000-agent urban tsunami simulation, Sri Lankan coastal rail operations and 391 Ramgati residents.

**Validated ranges.** Findings are bounded to their cases: only 36% of surveyed Texans located the correct map zone; the Japanese model represented about 340,000 evacuees and found an approximately 40-minute initiation allowance only under its maximum-tsunami, forecast-controlled assumptions; the Bangladesh survey included 391 residents.

**Recent advances.** Recent advances use hundreds of thousands of individual agents and real-time inundation forecasts to manage congestion, and apply PADM-informed multichannel communication analysis to shelter barriers. The field is moving toward coupled physical, behavioral and operational digital decision support.

**Disagreements.** Better risk-map self-location did not predict Texas evacuation expectations, showing that information accuracy alone may not change intended action. Conversely, Bangladesh evidence associates direct, multi-channel institutional communication with better shelter perceptions. These results concern different communication stages and are not contradictory.

**Limitations.** Stated intentions differ from actual behavior; post-event recall is biased; coefficients are culturally and event specific. Models simplify compliance, disability, tourists, family reunification, vehicles, debris, power and communications failure. Forecast and inundation errors propagate directly into route and timing advice.

**Open questions.** Priorities include end-to-end validation in drills and events, forecast-conditioned dynamic routing, mixed pedestrian–vehicle evacuation, evacuation of tourists and mobility-limited people, spontaneous shelter choice, warning ambiguity, network damage, vertical evacuation, equitable shelter design and calibrated behavioral uncertainty.

**Seminal papers.** The 2006 Texas study showed that correct zone-map reading is not equivalent to evacuation intention. The 2014 THESEUS study provided a coastal-engineering chain from hydraulic forecasts to mass-evacuation clearance, complementing behavioral survey evidence.

## Equations

### Evacuation clearance margin

$$
M=T_{arrival}-T_{warning}-T_{decision}-T_{clearance}
$$

Regime: Residents of Okitsu and Mangyo responding to the 2014 Iyonada earthquake.

Variables: `M` remaining safety margin; `T_arrival` hazard arrival time; `T_warning` warning issuance or reception time; `T_decision` decision and mobilization delay; `T_clearance` travel and congestion clearance time

Source: (Sun 2017, [doi:10.1007/s11069-016-2562-z](https://doi.org/10.1007/s11069-016-2562-z))

### Evacuation clearance margin

$$
M=T_{arrival}-T_{warning}-T_{decision}-T_{clearance}
$$

Regime: Bordeaux pilot planning and Cesenatico evacuation-time trial with the source data and assumptions.

Variables: `M` remaining safety margin; `T_arrival` hazard arrival time; `T_warning` warning issuance or reception time; `T_decision` decision and mobilization delay; `T_clearance` travel and congestion clearance time

Source: (Hissel 2014, [doi:10.1016/j.coastaleng.2013.11.015](https://doi.org/10.1016/j.coastaleng.2013.11.015))

### Evacuation clearance margin

$$
M=T_{arrival}-T_{warning}-T_{decision}-T_{clearance}
$$

Regime: The surveyed coastal population and hypothetical typhoon storm-surge scenarios used by the authors.

Variables: `M` remaining safety margin; `T_arrival` hazard arrival time; `T_warning` warning issuance or reception time; `T_decision` decision and mobilization delay; `T_clearance` travel and congestion clearance time

Source: (Pan 2020, [doi:10.1016/j.ijdrr.2020.101522](https://doi.org/10.1016/j.ijdrr.2020.101522))

### Evacuation clearance margin

$$
M=T_{arrival}-T_{warning}-T_{decision}-T_{clearance}
$$

Regime: 391 surveyed residents in cyclone-prone Ramgati and the communication/shelter variables measured.

Variables: `M` remaining safety margin; `T_arrival` hazard arrival time; `T_warning` warning issuance or reception time; `T_decision` decision and mobilization delay; `T_clearance` travel and congestion clearance time

Source: (Zakaria 2025, [doi:10.1016/j.ijdrr.2025.105867](https://doi.org/10.1016/j.ijdrr.2025.105867))

### Evacuation clearance margin

$$
M=T_{arrival}-T_{warning}-T_{decision}-T_{clearance}
$$

Regime: Sri Lanka southern coastal railway topology, communications and tsunami scenarios represented in the study.

Variables: `M` remaining safety margin; `T_arrival` hazard arrival time; `T_warning` warning issuance or reception time; `T_decision` decision and mobilization delay; `T_clearance` travel and congestion clearance time

Source: (Sirisoma 2015, [doi:10.1061/(asce)nh.1527-6996.0000134](https://doi.org/10.1061/(asce)nh.1527-6996.0000134))

### Evacuation clearance margin

$$
M=T_{arrival}-T_{warning}-T_{decision}-T_{clearance}
$$

Regime: Surveyed Texas coastal residents and the risk-area maps supplied in the study.

Variables: `M` remaining safety margin; `T_arrival` hazard arrival time; `T_warning` warning issuance or reception time; `T_decision` decision and mobilization delay; `T_clearance` travel and congestion clearance time

Source: (Arlikatti 2006, [doi:10.1177/0013916505277603](https://doi.org/10.1177/0013916505277603))

### Evacuation clearance margin

$$
M=T_{arrival}-T_{warning}-T_{decision}-T_{clearance}
$$

Regime: Approximately 340,000 agents, the study city network and maximum-class tsunami scenario.

Variables: `M` remaining safety margin; `T_arrival` hazard arrival time; `T_warning` warning issuance or reception time; `T_decision` decision and mobilization delay; `T_clearance` travel and congestion clearance time

Source: (MAKINOSHIMA 2018, [doi:10.2208/kaigan.74.i_409](https://doi.org/10.2208/kaigan.74.i_409))

## Claims

- **C312.** Among surveyed Texas coastal residents, only 36% correctly identified their hurricane risk area and another 28% were off by one area; map-location accuracy was not correlated with evacuation expectations, which instead varied with prior hazard experience and the expected evacuation context. *Regime: Surveyed Texas coastal residents and the risk-area maps supplied in the study..* [direct_finding, mixed] (Arlikatti 2006, [doi:10.1177/0013916505277603](https://doi.org/10.1177/0013916505277603))
- **C313.** A coastal-resident survey under alternative typhoon storm-surge scenarios identified demographic, risk-cognition, destination-choice and evacuation-context variables and combined them in a binary logistic model of evacuation choice. *Regime: The surveyed coastal population and hypothetical typhoon storm-surge scenarios used by the authors..* [direct_finding, mixed] (Pan 2020, [doi:10.1016/j.ijdrr.2020.101522](https://doi.org/10.1016/j.ijdrr.2020.101522))
- **C314.** After the 2014 Iyonada earthquake, many residents in Okitsu and Mangyo quickly evacuated or prepared to evacuate, but interviews revealed substantial differences from their prior plans, including unanticipated triggering cues and vehicle use. *Regime: Residents of Okitsu and Mangyo responding to the 2014 Iyonada earthquake..* [direct_finding, mixed] (Sun 2017, [doi:10.1007/s11069-016-2562-z](https://doi.org/10.1007/s11069-016-2562-z))
- **C315.** A mass-evacuation planning workflow coupled hydraulic-model flood inputs, population and route data, action-plan generation and evacuation-time simulation; it was applied in Bordeaux and trialled in Cesenatico to compare management strategies and warning-time requirements. *Regime: Bordeaux pilot planning and Cesenatico evacuation-time trial with the source data and assumptions..* [direct_finding, mixed] (Hissel 2014, [doi:10.1016/j.coastaleng.2013.11.015](https://doi.org/10.1016/j.coastaleng.2013.11.015))
- **C316.** A supercomputer simulation of approximately 340,000 evacuees identified route delays and shelter overcrowding; controlling movement with tsunami-inundation forecasts greatly reduced congestion and, for the maximum-class scenario studied, preserved casualty-free evacuation with about 40 minutes from earthquake occurrence to evacuation initiation. *Regime: Approximately 340,000 agents, the study city network and maximum-class tsunami scenario..* [direct_finding, mixed] (MAKINOSHIMA 2018, [doi:10.2208/kaigan.74.i_409](https://doi.org/10.2208/kaigan.74.i_409))
- **C317.** For Sri Lanka’s partly single-track southern coastal railway, a scenario procedure assigned trains to safe stations or to stations permitting onward evacuation while accounting for uncertain tsunami arrival, passenger concern, and weak communications and signalling. *Regime: Sri Lanka southern coastal railway topology, communications and tsunami scenarios represented in the study..* [direct_finding, mixed] (Sirisoma 2015, [doi:10.1061/(asce)nh.1527-6996.0000134](https://doi.org/10.1061/(asce)nh.1527-6996.0000134))
- **C318.** In a cross-sectional survey of 391 residents in cyclone-prone Ramgati, Bangladesh, most respondents reported strongly negative shelter perceptions; reliance on mass media without government or NGO information was associated with greater concern, while multi-channel and direct institutional communication supported more positive shelter perceptions and evacuation response. *Regime: 391 surveyed residents in cyclone-prone Ramgati and the communication/shelter variables measured..* [direct_finding, mixed] (Zakaria 2025, [doi:10.1016/j.ijdrr.2025.105867](https://doi.org/10.1016/j.ijdrr.2025.105867))
- **C1514.** A Belgian-coast survey shows public flood-risk perception is a material input to effective mitigation, communication, and safety policy. *Regime: An Analysis of the Public Perception of Flood Risk on the Belgian Coast.* [direct_finding, field] (Wim Kellens 2011, [doi:10.1111/j.1539-6924.2010.01571.x](https://doi.org/10.1111/j.1539-6924.2010.01571.x))
- **C1515.** Post-hurricane survey analysis relates evacuation decisions to perceived risk, information, and household location in metropolitan Houston. *Regime: Who Evacuates When Hurricanes Approach? The Role of Risk, Information, and Location*.* [direct_finding, field] (Robert M. Stein 2010, [doi:10.1111/j.1540-6237.2010.00721.x](https://doi.org/10.1111/j.1540-6237.2010.00721.x))
- **C1517.** Coastal-city surveys evaluate how tsunami hazard proximity influences perceived risk and residents' ability to identify their exposure. *Regime: Hazard proximity and risk perception of tsunamis in coastal cities: Are people able to identify their risk?.* [direct_finding, field] (Juan Pablo Arias 2017, [doi:10.1371/journal.pone.0186455](https://doi.org/10.1371/journal.pone.0186455))

## Papers

- Wim Kellens (2011). An Analysis of the Public Perception of Flood Risk on the Belgian Coast. *Risk Analysis*. [doi:10.1111/j.1539-6924.2010.01571.x](https://doi.org/10.1111/j.1539-6924.2010.01571.x)
- Arlikatti (2006). Risk Area Accuracy and Hurricane Evacuation Expectations of Coastal Residents. *Environment and Behavior*. [doi:10.1177/0013916505277603](https://doi.org/10.1177/0013916505277603)
- Robert M. Stein (2010). Who Evacuates When Hurricanes Approach? The Role of Risk, Information, and Location*. *Social Science Quarterly*. [doi:10.1111/j.1540-6237.2010.00721.x](https://doi.org/10.1111/j.1540-6237.2010.00721.x)
- Juan Pablo Arias (2017). Hazard proximity and risk perception of tsunamis in coastal cities: Are people able to identify their risk?. *PLoS ONE*. [doi:10.1371/journal.pone.0186455](https://doi.org/10.1371/journal.pone.0186455)
- Pan (2020). Study on the decision-making behavior of evacuation for coastal residents under typhoon storm surge disaster. *International Journal of Disaster Risk Reduction*. [doi:10.1016/j.ijdrr.2020.101522](https://doi.org/10.1016/j.ijdrr.2020.101522)
- Sun (2017). Tsunami evacuation behavior of coastal residents in Kochi Prefecture during the 2014 Iyonada Earthquake. *Natural Hazards*. [doi:10.1007/s11069-016-2562-z](https://doi.org/10.1007/s11069-016-2562-z)
- Hissel (2014). Early warning and mass evacuation in coastal cities. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2013.11.015](https://doi.org/10.1016/j.coastaleng.2013.11.015)
- MAKINOSHIMA (2018). INVESTIGATION OF TSUNAMI EVACUATION RISK AND RISK MITIGATION STRATEGY IN COASTAL URBAN CITY USING LARGE-SCALE EVACUATION SIMULATION. *Journal of Japan Society of Civil Engineers, Ser. B2 (Coastal Engineering)*. [doi:10.2208/kaigan.74.i_409](https://doi.org/10.2208/kaigan.74.i_409)
- Sirisoma (2015). An Approach to Coastal Railway Line Evacuation under a Tsunami Warning. *Natural Hazards Review*. [doi:10.1061/(asce)nh.1527-6996.0000134](https://doi.org/10.1061/(asce)nh.1527-6996.0000134)
- Zakaria (2025). Enhancing evacuation resilience: The impact of communication on shaping perceptions toward cyclone shelter and evacuation behavior among at-risk coastal communities. *International Journal of Disaster Risk Reduction*. [doi:10.1016/j.ijdrr.2025.105867](https://doi.org/10.1016/j.ijdrr.2025.105867)
