# Pipeline and cable scour

`scour.pipelines` | Scour beneath linear infrastructure.

Parent: [Scour and erosion](scour.md)

Papers: 18. Claims: 18. Equations: 0.

Used by pyCoastal design modules: Pile wave loads.

## Synthesis

**Well established.** Pipeline scour progresses through onset, tunnel erosion, and lee-wake erosion and can develop into unsupported free spans. Governing response differs among steady current, waves, combined flow, bidirectional tide, live-bed, clear-water, seepage, and multi-pipe configurations.

**Governing physics.** Controls include bed shear and pressure gradients, piping and seepage, horseshoe and lee vortices, shedding, turbulence, phase lag, sediment mobility and avalanching, initial clearance, embedment, pipe diameter, gaps, and cyclic reversal.

**Dimensionless parameters.** Key groups are Shields and Keulegan-Carpenter numbers, current-to-wave velocity ratio, Reynolds number, gap-to-diameter and embedment-to-diameter ratios, hydraulic gradient, relative grain size, live-bed mobility, and nondimensional scour depth and time.

**Major equations.** Frameworks include URANS and RANS turbulence closures, Euler-Euler two-phase momentum, CFD-DEM particle dynamics, morphodynamic sediment continuity, critical Shields and KC relations, scour timescales, equilibrium-depth fits, and data-driven predictors.

**Typical methods.** Methods combine steady, oscillatory, combined-flow, and reversible flumes; profile imaging; two-phase CFD, URANS, CFD-DEM, SedFoam, and FLOW-3D; empirical and machine-learning prediction; and protection/free-span review.

**Numerical models.** Two-phase and particle models resolve sediment concentration and interaction without prescribed bedload layers, but predictions depend strongly on turbulence and vortex representation; black-box models may score well while retaining dataset-limited uncertainty.

**Experimental datasets.** Evidence includes single and tandem pipes, 1:20 bidirectional tides tied to Cezhen field data, piggyback geometry, solidified-soil protection under waves and currents, and validation cases spanning live-bed, clear-water, sheet-flow, tunnel, and lee-wake stages.

**Validated ranges.** Explicit findings include live-bed depth of 0.6-0.8D with seepage, tandem gaps of 1-4D, tidal depth averaging 80% of equivalent steady-current scour, a piggyback maximum near G/D=0.1, and loss of gap influence at KC=5.6 without shedding.

**Recent advances.** Recent advances resolve individual grains, seepage and piping, tandem interference, reversible tides, piggyback geometry, data-driven uncertainty, and protective-soil tradeoffs, moving toward coupled hydraulic and geotechnical assessment.

**Disagreements.** Model structure matters physically: one rheological two-phase model overdeposited sediment when vortex shedding was absent, while SedFoam results changed strongly with turbulence cross-diffusion. Good scour-rate agreement does not prove correct lee-wake mechanics.

**Limitations.** Most evidence is two-dimensional, idealized, uniform-sediment, rigid-pipe, and short-duration. Field-scale span propagation, vibration coupling, heterogeneous and cohesive beds, soil liquefaction, cyclic storms, and protection aging remain weakly validated.

**Open questions.** Needs include coupled scour-vibration-span growth, poromechanical seabed response, three-dimensional end effects, reversal history, layered beds, uncertainty transfer, inspection assimilation, and protection reliability under liquefaction and degradation.

**Seminal papers.** The branch builds on classical onset, tunnel and lee-wake staging, Shields and KC scaling, equilibrium depth, and self-burial concepts, extended by two-phase, particle-resolved, seepage, tandem, and tidal-reversal models.

## Claims

- **C478.** A three-dimensional rheology-based two-phase model reproduced measured pipeline scour rate but overpredicted lee deposition because it did not capture vortex shedding, with strong sensitivity to turbulence parameters. *Regime: pipeline in sheet-flow sediment.* [direct_finding, numerical] (Cheng-Hsien Lee 2016, [doi:10.1063/1.4948987](https://doi.org/10.1063/1.4948987))
- **C479.** For tandem pipelines with gap ratios 1-4, weak-current scour resembled pure-wave response, equal wave-current strength resembled pure-current response, and small gaps delayed downstream scour except at KC=5.6 where vortex shedding was absent. *Regime: two tandem pipes; KC and gap ratio 1-4 under waves plus currents.* [direct_finding, numerical] (Yuzhu Pearl Li 2019, [doi:10.1016/j.coastaleng.2019.103619](https://doi.org/10.1016/j.coastaleng.2019.103619))
- **C480.** Upward seepage increased equilibrium scour width beneath a pipeline; live-bed depth remained about 0.6-0.8 pipe diameters, while large gradients slightly reduced clear-water depth. *Regime: live-bed and clear-water pipeline scour under hydraulic gradients.* [direct_finding, numerical] (Yuzhu Pearl Li 2020, [doi:10.1016/j.coastaleng.2019.103624](https://doi.org/10.1016/j.coastaleng.2019.103624))
- **C481.** SedFoam pipeline-scour predictions were insensitive to granular-stress choice but strongly dependent on turbulence cross-diffusion, indicating that the sediment transport layer behaves more like a shear layer than a boundary layer. *Regime: pipeline tunnel and lee-wake scour.* [direct_finding, numerical] (Antoine Mathieu 2019, [doi:10.3390/w11081727](https://doi.org/10.3390/w11081727))
- **C482.** An MLP optimized by colliding bodies predicted wave-driven pipeline scour expansion better than PSO-, whale-, regression-, and empirical alternatives for the tested dataset. *Regime: wave, sediment, and pipeline geometry inputs.* [direct_finding, numerical] (Mohammad Ehteram 2020, [doi:10.3390/w12030902](https://doi.org/10.3390/w12030902))
- **C483.** A free-span review identified wave-current scour as the main driver and compared retrenching, structural support, bionic vegetation, and spoiler or choke-plate self-burial treatments. *Regime: offshore pipelines exposed to wave-current scour and other span causes.* [literature_review_statement, review] (Bo Zhang 2020, [doi:10.3390/jmse8050329](https://doi.org/10.3390/jmse8050329))
- **C484.** A validated Euler-Euler model reproduced wave-induced tunnel-scour profiles and showed intense turbulence-driven transport with phase lag between scour-hole and free-stream velocity. *Regime: pipeline on plane erodible bed under oscillatory flow.* [direct_finding, numerical] (Mohammad Hossein Kazeminezhad 2011, [doi:10.1061/(asce)hy.1943-7900.0000540](https://doi.org/10.1061/(asce)hy.1943-7900.0000540))
- **C485.** Optimized ANFIS using Shields number, Keulegan-Carpenter number, and embedment ratio gave the best tested prediction, with larger clear-water uncertainty driven more by input combination than model structure. *Regime: Shields, KC, and embedment ratio inputs.* [direct_finding, numerical] (Ahmad Sharafati 2020, [doi:10.2166/hydro.2020.184](https://doi.org/10.2166/hydro.2020.184))
- **C486.** Flume tests found ionic-stabilizer solidified soil effective for pipeline scour protection, but its dense crust can increase accumulated-liquefaction risk in underlying noncohesive soil. *Regime: ISS-solidified layer around a pipeline over noncohesive subsoil.* [direct_finding, experimental] (Ruigeng Hu 2022, [doi:10.3390/jmse10010076](https://doi.org/10.3390/jmse10010076))
- **C487.** A coupled CFD-DEM solver matched measured pipeline scour-depth evolution while resolving individual-particle motion through onset, tunnel erosion, and lee-wake erosion. *Regime: subsea pipeline over granular bed.* [direct_finding, numerical] (Seongjin Song 2022, [doi:10.3390/jmse10050556](https://doi.org/10.3390/jmse10050556))
- **C488.** In 1:20 tests tied to Cezhen field data, bidirectional tidal scour was more symmetric and averaged 80% of the depth under a steady unidirectional current with the same peak velocity. *Regime: Hangzhou Bay pipeline tidal cycle.* [direct_finding, experimental] (Zhiyong Zhang 2021, [doi:10.3390/jmse9121421](https://doi.org/10.3390/jmse9121421))
- **C489.** Validated FLOW-3D simulations identified bed shear as the primary pipeline-scour driver and showed significant effects of velocity, grain size, pipe diameter, and initial seabed clearance. *Regime: pipeline with varied flow, grain size, diameter, and initial gap.* [direct_finding, numerical] (Ke Hu 2023, [doi:10.3390/jmse11010234](https://doi.org/10.3390/jmse11010234))
- **C490.** Pipeline protection methods divide into preventing scour onset and stimulating self-burial; prevention is widely studied but mechanistically incomplete, while spoiler-assisted burial has broad experimental, numerical, and project evidence. *Regime: underwater pipelines and engineering protection projects.* [literature_review_statement, review] (Liquan Xie 2018, [doi:10.32732/jcec.2018.7.4.171](https://doi.org/10.32732/jcec.2018.7.4.171))
- **C491.** For a piggyback pipeline, equilibrium scour increased as gap ratio rose from 0 to 0.1 and then declined, while stronger current ratio, KC, Reynolds number, and Shields parameter increased depth. *Regime: piggyback pipe under waves and current.* [direct_finding, experimental] (Ruigeng Hu 2022, [doi:10.3390/jmse10030350](https://doi.org/10.3390/jmse10030350))
- **C492.** An open-source multiphase CFD model computed pipeline sediment transport without imposed bedload and suspended-load layers and reproduced seepage, piping onset, and vortex-driven deposition. *Regime: submerged pipeline with sediment transport and deposition.* [direct_finding, numerical] (Subiyanto Subiyanto 2024, [doi:10.37934/cfdl.16.7.150165](https://doi.org/10.37934/cfdl.16.7.150165))
- **C1528.** A review integrates hydrodynamic loading, corrosion, design, and maintenance risks for risers, umbilicals, and cables in floating offshore production systems. *Regime: Pipeline Systems in Floating Offshore Production Systems: Hydrodynamics, Corrosion, Design and Maintenance.* [literature_review_statement, review] (Jin Yan 2026, [doi:10.3390/jmse14020176](https://doi.org/10.3390/jmse14020176))
- **C1529.** A review synthesizes dynamic loading and displacement of offshore pipelines impacted by submarine debris flows and turbidity currents. *Regime: A State-of-the-Art Review of the Hydrodynamics of Offshore Pipelines Under Submarine Gravity Flows and Their Interactions.* [literature_review_statement, review] (Cheng Zhang 2025, [doi:10.3390/jmse13091654](https://doi.org/10.3390/jmse13091654))
- **C1724.** Reanalysis of weakly cohesive-bed experiments finds normalized pipeline scour depends directly on Keulegan-Carpenter number and, for clay content below 5%, inversely on clay content; adding initial burial substantially improves fit, while wide clay ranges require liquidity-index information. *Regime: Pipelines on weakly cohesive beds exposed to combined waves and currents, with varying clay fraction and initial burial..* [direct_finding, mixed] (Postacchini 2015, [doi:10.1016/j.apor.2015.04.010](https://doi.org/10.1016/j.apor.2015.04.010))

## Papers

- Cheng-Hsien Lee (2016). Multi-dimensional rheology-based two-phase model for sediment transport and applications to sheet flow and pipeline scour. *Physics of Fluids*. [doi:10.1063/1.4948987](https://doi.org/10.1063/1.4948987)
- Yuzhu Pearl Li (2019). Numerical investigation of wave-plus-current induced scour beneath two submarine pipelines in tandem. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2019.103619](https://doi.org/10.1016/j.coastaleng.2019.103619)
- Yuzhu Pearl Li (2020). CFD investigations of scour beneath a submarine pipeline with the effect of upward seepage. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2019.103624](https://doi.org/10.1016/j.coastaleng.2019.103624)
- Antoine Mathieu (2019). Two-Phase Flow Simulation of Tunnel and Lee-Wake Erosion of Scour below a Submarine Pipeline. *Water*. [doi:10.3390/w11081727](https://doi.org/10.3390/w11081727)
- Mohammad Ehteram (2020). Pipeline Scour Rates Prediction-Based Model Utilizing a Multilayer Perceptron-Colliding Body Algorithm. *Water*. [doi:10.3390/w12030902](https://doi.org/10.3390/w12030902)
- Bo Zhang (2020). Causes and Treatment Measures of Submarine Pipeline Free-Spanning. *Journal of Marine Science and Engineering*. [doi:10.3390/jmse8050329](https://doi.org/10.3390/jmse8050329)
- Mohammad Hossein Kazeminezhad (2011). Two-Phase Simulation of Wave-Induced Tunnel Scour beneath Marine Pipelines. *Journal of Hydraulic Engineering*. [doi:10.1061/(asce)hy.1943-7900.0000540](https://doi.org/10.1061/(asce)hy.1943-7900.0000540)
- Postacchini (2015). Scour depth under pipelines placed on weakly cohesive soils. *Applied Ocean Research*. [doi:10.1016/j.apor.2015.04.010](https://doi.org/10.1016/j.apor.2015.04.010)
- Ahmad Sharafati (2020). Application of nature-inspired optimization algorithms to ANFIS model to predict wave-induced scour depth around pipelines. *Journal of Hydroinformatics*. [doi:10.2166/hydro.2020.184](https://doi.org/10.2166/hydro.2020.184)
- Seongjin Song (2022). Unresolved CFD and DEM Coupled Simulations on Scour around a Subsea Pipeline. *Journal of Marine Science and Engineering*. [doi:10.3390/jmse10050556](https://doi.org/10.3390/jmse10050556)
- Ruigeng Hu (2022). Scour Protection of Submarine Pipelines Using Ionic Soil Stabilizer Solidified Soil. *Journal of Marine Science and Engineering*. [doi:10.3390/jmse10010076](https://doi.org/10.3390/jmse10010076)
- Zhiyong Zhang (2021). Scale Model Experiment on Local Scour around Submarine Pipelines under Bidirectional Tidal Currents. *Journal of Marine Science and Engineering*. [doi:10.3390/jmse9121421](https://doi.org/10.3390/jmse9121421)
- Ke Hu (2023). Numerical Simulation on the Local Scour Processing and Influencing Factors of Submarine Pipeline. *Journal of Marine Science and Engineering*. [doi:10.3390/jmse11010234](https://doi.org/10.3390/jmse11010234)
- Liquan Xie (2018). Scour Protection of Underwater Pipelines. *Journal of Civil Engineering and Construction*. [doi:10.32732/jcec.2018.7.4.171](https://doi.org/10.32732/jcec.2018.7.4.171)
- Ruigeng Hu (2022). Scour Characteristics and Equilibrium Scour Depth Prediction around a Submarine Piggyback Pipeline. *Journal of Marine Science and Engineering*. [doi:10.3390/jmse10030350](https://doi.org/10.3390/jmse10030350)
- Jin Yan (2026). Pipeline Systems in Floating Offshore Production Systems: Hydrodynamics, Corrosion, Design and Maintenance. *Journal of Marine Science and Engineering*. [doi:10.3390/jmse14020176](https://doi.org/10.3390/jmse14020176)
- Cheng Zhang (2025). A State-of-the-Art Review of the Hydrodynamics of Offshore Pipelines Under Submarine Gravity Flows and Their Interactions. *Journal of Marine Science and Engineering*. [doi:10.3390/jmse13091654](https://doi.org/10.3390/jmse13091654)
- Subiyanto Subiyanto (2024). Numerical Simulation of Pipeline Scour and Sedimentation around Submerged Pipelines with an Open-Source Multiphase-CFD Model. *CFD letters*. [doi:10.37934/cfdl.16.7.150165](https://doi.org/10.37934/cfdl.16.7.150165)
