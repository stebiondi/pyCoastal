# Mooring hydrodynamics

`ports.mooring` | Mooring loads and berth conditions.

Parent: [Ports and harbors](ports.md)

Papers: 10. Claims: 8. Equations: 0.

Used by pyCoastal design modules: Navigation channel.

## Synthesis

**Well established.** A berth mooring system must limit vessel motions, line tensions, fender reactions and access interruptions under the local directional wave, wind, current, tide and operational load environment; nominal vessel fit or calm-water capacity alone is insufficient.

**Governing physics.** Environmental forces and moments excite surge, sway, heave, roll, pitch and yaw, while nonlinear mooring stiffness, pretension, geometry, fender contact, damping, under-keel conditions and berth hydrodynamics distribute and sometimes amplify response.

**Dimensionless parameters.** Relevant normalized controls include wave length and draft relative to basin depth, line pretension-to-breaking strength, demand-to-capacity and safety factors, fender compression ratio, vessel-motion-to-operational-limit ratio, natural-period-to-forcing-period ratio and spectral exceedance probability.

**Major equations.** Analysis combines six-degree-of-freedom vessel dynamics with hydrodynamic mass, damping and excitation, nonlinear line force–extension and catenary geometry, fender reaction, wind and current drag, and equilibrium or time-domain compatibility at fairleads and berth contact points.

**Typical methods.** Methods characterize directional berth forcing, select vessel loading states, define line and fender properties and operational limits, compute frequency- or time-domain response, test environmental combinations and failures, perform configuration sensitivity, and validate motions or tensions where observations exist.

**Numerical models.** Evidence includes spectral-type reduction intended to drive response and downtime studies and a coupled berth safety assessment used to compare mooring configuration improvements for ferries exceeding original berth capacity.

**Experimental datasets.** The reviewed slice contains a 40-year reconstructed harbor spectral climate at seven control points and a Jeju Port passenger-ferry/berth safety assessment; neither source alone supplies a broad measured moored-vessel benchmark archive.

**Validated ranges.** Applicability is limited to the Africa-basin spectral classification and the evaluated Jeju passenger ships, berth geometry, configurations and environmental cases; exact vessel and line ranges are unavailable from the indexed abstract.

**Recent advances.** Recent advances integrate long spectral climates, coupled ship–fender–mooring simulation, configuration optimization, mixture models for snap extremes, fatigue reliability and sensor-supported digital assessment, though most remain outside the currently accessible evidence slice.

**Disagreements.** Frequency-domain approaches are efficient for linear response and long climate integration, while time-domain models are needed for nonlinear lines, fender contact, slack–snap behavior and transient failures. Conservative static safety factors may not reproduce dynamic extremes or operational downtime.

**Limitations.** Current reviewed evidence lacks direct measured line tension and six-degree-of-freedom validation, detailed snap and fatigue treatment, passing-ship forcing, line aging and failure, probabilistic joint environmental extremes, human operations and transfer across berth and vessel classes.

**Open questions.** Priorities include open full-scale motion–tension datasets, directional multimodal forcing, nonlinear snap and fatigue, line/fender degradation, passing ships, automated line handling, climate nonstationarity, cascading failure and probabilistic downtime thresholds.

**Seminal papers.** Classical static line equilibrium, catenary mechanics, linear vessel-response theory and early terminal design criteria established mooring analysis; nonlinear time-domain simulation and measured harbor spectra later connected line design to operational response.

## Claims

- **C107.** Improved prediction of moored-ship response and port downtime is an intended application of the spectral-type method, but this paper does not validate ship motions or operational gains. *Regime: Interpretive limitation on the Africa-basin methodology and all proposed operational applications..* [direct_finding, numerical] (Romano-Moreno 2023, [doi:10.1016/j.coastaleng.2022.104271](https://doi.org/10.1016/j.coastaleng.2022.104271))
- **C1125.** A Jeju Port assessment identified risks for car ferries exceeding berth design capacity and used sensitivity analysis to confirm that a revised mooring configuration improved the evaluated safety response. *Regime: A Study on the Improvement of Mooring Configuration through Mooring Safety Assessment for Passenger Ship Berth.* [direct_finding, numerical] (Kim 2022, [doi:10.20481/kscdp.2022.9.2.145](https://doi.org/10.20481/kscdp.2022.9.2.145))
- **C1496.** Assessment of future ultra-large container vessels shows increasing ship dimensions impose higher demands on port mooring equipment, layouts, and infrastructure. *Regime: Analysis of the Mooring Effects of Future Ultra-Large Container Vessels (ULCV) on Port Infrastructures.* [direct_finding, mixed] (Sara Sanz Sáenz 2023, [doi:10.3390/jmse11040856](https://doi.org/10.3390/jmse11040856))
- **C1497.** Simplified response graphs estimate moored-ship motions and line loads for harbor-tranquillity evaluation without full time-consuming simulation. *Regime: Effect of mooring system on moored ship motions and harbour tranquillity.* [direct_finding, numerical] (Shigeki SAKAKIBARA 2008, [doi:10.1504/ijosm.2008.017783](https://doi.org/10.1504/ijosm.2008.017783))
- **C1498.** Wave-flume tests compare two barge-breakwater mooring arrangements through wave dissipation and anchor-chain force measurements. *Regime: Experimental Study on Hydrodynamic Characteristics of Barge-Type Breakwaters under Different Mooring Methods.* [direct_finding, experimental] (Xiaofei Cheng 2023, [doi:10.3390/jmse11051016](https://doi.org/10.3390/jmse11051016))
- **C1499.** A standards-based synthesis organizes mooring and berthing actions required for structural design of port infrastructure. *Regime: Port structures - the distribution of forces on infrastructure due to mooring and berthing of vessels.* [literature_review_statement, review] (C. COMIN 2017, [doi:10.1590/s1983-41952017000300005](https://doi.org/10.1590/s1983-41952017000300005))
- **C1500.** Numerical calculations estimate wave-induced response of a berth-moored ship protected by a stilling pool for engineering design. *Regime: Sea wave impact on a ship moored at the berth with a stilling pool.* [direct_finding, numerical] (Konstantin K. Semenov 2015, [doi:10.5862/mce.55.7](https://doi.org/10.5862/mce.55.7))
- **C1721.** A mobile-harbor concept adds relative-position stabilization to shipboard winches in a four-point ship-to-ship mooring arrangement to support container transfer alongside a large anchored vessel through sea state 3. *Regime: A crane-equipped mobile-harbor vessel moored alongside a large anchored container ship during offshore cargo transfer..* [direct_finding, review] (Lee 2010, [doi:10.5394/kinpr.2010.34.5.311](https://doi.org/10.5394/kinpr.2010.34.5.311))

## Papers

- Sara Sanz Sáenz (2023). Analysis of the Mooring Effects of Future Ultra-Large Container Vessels (ULCV) on Port Infrastructures. *Journal of Marine Science and Engineering*. [doi:10.3390/jmse11040856](https://doi.org/10.3390/jmse11040856) [published version, CC BY](https://www.mdpi.com/2077-1312/11/4/856/pdf?version=1681900107)
- Shigeki SAKAKIBARA (2008). Effect of mooring system on moored ship motions and harbour tranquillity. *International Journal of Ocean Systems Management*. [doi:10.1504/ijosm.2008.017783](https://doi.org/10.1504/ijosm.2008.017783) [published version, read only](https://doi.org/10.1504/ijosm.2008.017783)
- Xiaofei Cheng (2023). Experimental Study on Hydrodynamic Characteristics of Barge-Type Breakwaters under Different Mooring Methods. *Journal of Marine Science and Engineering*. [doi:10.3390/jmse11051016](https://doi.org/10.3390/jmse11051016) [published version, CC BY](https://www.mdpi.com/2077-1312/11/5/1016/pdf?version=1683716680)
- Lee (2010). Conceptual Design for Mooring Stability System and Equipments of Mobile Harbor. *Journal of Korean navigation and port research*. [doi:10.5394/kinpr.2010.34.5.311](https://doi.org/10.5394/kinpr.2010.34.5.311) [published version, read only](http://koreascience.or.kr:80/article/JAKO201027042827721.pdf)
- C. COMIN (2017). Port structures - the distribution of forces on infrastructure due to mooring and berthing of vessels. *Revista IBRACON de Estruturas e Materiais*. [doi:10.1590/s1983-41952017000300005](https://doi.org/10.1590/s1983-41952017000300005) [published version, CC BY](http://www.scielo.br/pdf/riem/v10n3/1983-4195-riem-10-03-00626.pdf)
- Kim (2022). A Study on the Improvement of Mooring Configuration through Mooring Safety Assessment for Passenger Ship Berth. *Korea Society of Coastal Disaster Prevention*. [doi:10.20481/kscdp.2022.9.2.145](https://doi.org/10.20481/kscdp.2022.9.2.145) [published version, CC BY-NC](http://jcdp.or.kr/upload/pdf/kscdp-2022-9-2-145.pdf)
- Konstantin K. Semenov (2015). Sea wave impact on a ship moored at the berth with a stilling pool. *Magazine of Civil Engineering*. [doi:10.5862/mce.55.7](https://doi.org/10.5862/mce.55.7) [published version, CC BY-NC](https://engstroy.spbstu.ru/userfiles/files/2015/3(55)/07.pdf)
- Peng Jin (2023). Optimization and evaluation of a semi-submersible wind turbine and oscillating body wave energy converters hybrid system. *Energy*. [doi:10.1016/j.energy.2023.128889](https://doi.org/10.1016/j.energy.2023.128889) [accepted manuscript, read only](https://catalog.lib.kyushu-u.ac.jp/opac_download_md/6796381/6796381.pdf)
- Arefeh Emami (2024). Further development of offshore floating solar and its design requirements. *Marine Structures*. [doi:10.1016/j.marstruc.2024.103730](https://doi.org/10.1016/j.marstruc.2024.103730) [accepted manuscript, CC BY](https://pureadmin.qub.ac.uk/ws/files/619849948/Revised_Clean_9-19-2024.pdf)
- Romano-Moreno (2023). Multimodal harbor wave climate characterization based on wave agitation spectral types. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2022.104271](https://doi.org/10.1016/j.coastaleng.2022.104271) [published version, CC BY-NC-ND](https://api.elsevier.com/content/article/PII:S0378383922001843?httpAccept=text/xml)
