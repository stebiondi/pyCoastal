# Scour protection

`scour.protection` | Countermeasures and performance.

Parent: [Scour and erosion](scour.md)

Papers: 10. Claims: 10. Equations: 0.

Used by pyCoastal design modules: Seawall design.

## Synthesis

**Well established.** Marine scour countermeasures either increase bed resistance, alter the erosive flow, improve soil, or deliberately manage burial. Protection performance includes local scour reduction, armor and filter stability, edge response, deformation, and coupled foundation capacity.

**Governing physics.** Controls include horseshoe and lee vortices, downflow and side acceleration, bed shear, pressure and suction beneath armor, wave-current ratio, KC and Shields mobility, permeability, thickness, grading, surcharge, confinement, and wake interactions.

**Dimensionless parameters.** Important groups include Shields and KC numbers, wave-current ratio, protection-to-base grain and thickness ratios, footprint-to-pile diameter, permeability, relative collar elevation and width, armor grading, surcharge, and turbine clearance.

**Major equations.** Design frameworks use armor stability numbers and sizing, Shields and KC mobility thresholds, deformation and timescale relations, flow-reduction metrics, p-y and load-utilization curves, finite elements, LES, and CFD-DEM particle transport.

**Typical methods.** Methods combine wave-current flumes with underside observation, centrifuge and lateral-load tests, physical-model data reanalysis, LES, CFD-DEM, finite-element parametrics, micro/macro countermeasure reviews, and foundation capacity assessment.

**Numerical models.** LES resolves collar-modified vortices, CFD-DEM resolves permeable-net flow and grains, and finite elements quantify protection-induced confinement and stiffness. These models answer different coupled hydraulic and structural questions and are not interchangeable.

**Experimental datasets.** Evidence includes glass-bottom armor-suction tests, centrifuge monopile loading, optimized fishnet laboratory tests, CFD-DEM nets with permeability 0.681-0.802, more than 100 rock-fill simulations, and multi-study rock-deformation datasets.

**Validated ranges.** Reported results include over 30% lateral-capacity gain for a 5D/15 kPa layer, 10% capacity gain from thicker/heavier rock, fishnet shear/depth reductions of 14%/38.2%, net permeability 0.681-0.802, and collar side-flow/area reductions of 24.3%/93.3%.

**Recent advances.** Recent advances use underside visualization, CFD-DEM nets, collar LES, finite-element load utilization, cross-study deformation reanalysis, and turbine-specific reviews to treat protection as a coupled seabed-foundation system.

**Disagreements.** Protection can be both hydraulic countermeasure and structural component, but stiffness credit is geometry-dependent: large piles gained little except with heavy, tall rock, while width and sand accretion contributed under 1%. Hydraulic protection alone does not justify universal foundation credit.

**Limitations.** Edge scour, filter migration, base suction, liquefaction, armor settlement, installation variability, oblique and reversing forcing, extreme waves, array wakes, ecology, aging, and prototype structural response remain incompletely validated.

**Open questions.** Needs include coupled edge-filter-base failure, lifecycle deformation and repair, seismic and cyclic liquefaction, hybrid and eco-integrated systems, array-scale wakes, monitoring standards, and reliability-based optimization across hydraulic and structural functions.

**Seminal papers.** The branch builds on riprap stability and filter concepts, horseshoe-vortex control, collar and sacrificial-pile flow alteration, and armor deformation, extended by bio-soil treatment, permeable nets, structural stiffness credit, and rotor-wake conditions.

## Claims

- **C493.** Monopile countermeasures divide into armoring that strengthens the bed, flow alteration that weakens downflow and vortices, and soil improvement such as MICP, with distinct sizing and reduction evidence. *Regime: offshore-wind monopiles with riprap, collars, sacrificial piles, caissons, and MICP.* [literature_review_statement, review] (Tang 2022, [doi:10.1016/j.wse.2021.12.010](https://doi.org/10.1016/j.wse.2021.12.010))
- **C494.** A scour-protection layer 5 pile diameters wide with 15 kPa surcharge increased monopile lateral capacity by more than 30%, reduced accumulated deflection by over 100%, and could permit 10% less embedment. *Regime: monopile in dense and loose sand with protection layer.* [direct_finding, mixed] (Amin Askarinejad 2021, [doi:10.1016/j.oceaneng.2021.110377](https://doi.org/10.1016/j.oceaneng.2021.110377))
- **C495.** Across more than 100 simulations, rock fill restored monopile stiffness and thicker, heavier protection increased static capacity by about 10%, whereas width or sand densification changed capacity by less than 1% and large piles benefited less. *Regime: small- and large-diameter offshore-wind monopiles.* [direct_finding, numerical] (Carlos Menéndez-Vicente 2024, [doi:10.1016/j.enggeo.2024.107835](https://doi.org/10.1016/j.enggeo.2024.107835))
- **C496.** Sediment suction beneath monopile protection depends on pile KC, wave-current ratio, and protection-to-base thickness, with lower critical mobility under wave-dominated than current-dominated or combined conditions. *Regime: monopile protection over a thin mobile base layer.* [direct_finding, experimental] (Anders Wedel Nielsen 2018, [doi:10.3390/jmse6030100](https://doi.org/10.3390/jmse6030100))
- **C497.** For monopile protection nets with permeability 0.681-0.802, CFD-DEM showed reduced velocity and front downflow; protection was strongest inside the net and outside performance improved as permeability increased. *Regime: monopile nets with permeability 0.681-0.802.* [direct_finding, numerical] (Ning Zhang 2024, [doi:10.3390/jmse12050692](https://doi.org/10.3390/jmse12050692))
- **C498.** An optimized fishnet countermeasure reduced maximum seabed shear by 14% numerically and maximum monopile scour depth by 38.2% in laboratory tests. *Regime: offshore-wind monopile with varied net size, thread, and elevation.* [direct_finding, mixed] (Bo Yang 2019, [doi:10.3390/app9235023](https://doi.org/10.3390/app9235023))
- **C499.** Collar LES reduced monopile side-flow intensity by 24.3% and accelerated-flow area by 93.3%, but protection weakened as a 14% inflow increase raised turbulence intensity by 159%. *Regime: monopile with collar over flat and equilibrium-scoured beds.* [direct_finding, numerical] (Lei Wu 2025, [doi:10.3390/jmse13101841](https://doi.org/10.3390/jmse13101841))
- **C500.** For tidal-stream foundations, rotor operation, small tip clearance, and helical wakes can intensify near-bed erosion beyond static monopiles, requiring mitigation that accounts for reversing tides, waves, pore pressure, and array effects. *Regime: tidal-stream monopile, tripod, jacket, and gravity foundations.* [literature_review_statement, review] (Ruihuan Liu 2025, [doi:10.3390/jmse13122376](https://doi.org/10.3390/jmse13122376))
- **C501.** A reanalysis of monopile rock-protection tests found deformation patterns and magnitude governed by Shields number and wave-current ratio, negligible effects over the low tested KC range, and slower timescales than live-bed scour. *Regime: monopile rock protection under waves and currents.* [literature_review_statement, review] (Anders Wedel Nielsen 2026, [doi:10.59490/jchs.2025.0051](https://doi.org/10.59490/jchs.2025.0051))
- **C1241.** A biomineralization review reports 2–4 MICP cycles reduced maximum scour depth 84–100% under 0.3 m/s unidirectional currents and increased coastal-soil strength, while field delivery and environmental compatibility remain design constraints. *Regime: Recent Developments on Biomineralization for Erosion Control.* [direct_finding, mixed] (Shan Liu 2025, [doi:10.3390/app15126591](https://doi.org/10.3390/app15126591))

## Papers

- Tang (2022). Countermeasures for local scour at offshore wind turbine monopile foundations: A review. *Water Science and Engineering*. [doi:10.1016/j.wse.2021.12.010](https://doi.org/10.1016/j.wse.2021.12.010)
- Amin Askarinejad (2021). Influence of scour protection layers on the lateral response of monopile in dense sand. *Ocean Engineering*. [doi:10.1016/j.oceaneng.2021.110377](https://doi.org/10.1016/j.oceaneng.2021.110377)
- Carlos Menéndez-Vicente (2024). Numerical study on the stiffening properties of scour protection around monopiles for Offshore Wind Turbines. *Engineering Geology*. [doi:10.1016/j.enggeo.2024.107835](https://doi.org/10.1016/j.enggeo.2024.107835)
- Anders Wedel Nielsen (2018). Onset of Motion of Sediment underneath Scour Protection around a Monopile. *Journal of Marine Science and Engineering*. [doi:10.3390/jmse6030100](https://doi.org/10.3390/jmse6030100)
- Ning Zhang (2024). Numerical Investigation of Local Scour Protection around the Foundation of an Offshore Wind Turbine. *Journal of Marine Science and Engineering*. [doi:10.3390/jmse12050692](https://doi.org/10.3390/jmse12050692)
- Bo Yang (2019). A Feasibility Study for Using Fishnet to Protect Offshore Wind Turbine Monopile Foundations from Damage by Scouring. *Applied Sciences*. [doi:10.3390/app9235023](https://doi.org/10.3390/app9235023)
- Shan Liu (2025). Recent Developments on Biomineralization for Erosion Control. *Applied Sciences*. [doi:10.3390/app15126591](https://doi.org/10.3390/app15126591)
- Lei Wu (2025). Numerical Investigation of Flow Field Characteristics Around a Monopile Foundation with Collar Protection. *Journal of Marine Science and Engineering*. [doi:10.3390/jmse13101841](https://doi.org/10.3390/jmse13101841)
- Ruihuan Liu (2025). Local Scour Around Tidal Stream Turbine Foundations: A State-of-the-Art Review and Perspective. *Journal of Marine Science and Engineering*. [doi:10.3390/jmse13122376](https://doi.org/10.3390/jmse13122376)
- Anders Wedel Nielsen (2026). Re-analysis of the deformation of rock-based scour protections around monopiles exposed to waves and current. *Journal of Coastal and Hydraulic Structures*. [doi:10.59490/jchs.2025.0051](https://doi.org/10.59490/jchs.2025.0051)
