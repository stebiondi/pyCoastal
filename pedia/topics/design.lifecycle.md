# Lifecycle and maintenance

`design.lifecycle` | Durability, inspection, and intervention.

Parent: [Coastal engineering design](design.md)

Papers: 10. Claims: 10. Equations: 0.

## Synthesis

**Well established.** Lifecycle management links condition inspection, deterioration prediction, safety or reliability targets, maintenance and repair actions, replacement, and discounted whole-life cost rather than treating each decision independently.

**Governing physics.** Assets transition among condition states as loading and exposure accumulate damage. Inspections observe state imperfectly; maintenance changes condition or transition rate; delayed action increases future failure and repair consequences.

**Dimensionless parameters.** Decision controls include inspection interval/service life, transition and failure probabilities, false-positive/false-negative rates, intervention effectiveness, discount rate, cost ratios, reliability index and value-of-information ratios.

**Major equations.** Core tools include Markov transition matrices, partially observable or sequential decision processes, reliability and hazard functions, Bayesian state updating, discounted/average life-cycle cost, and constrained or multiobjective policy optimization.

**Typical methods.** Methods use periodic condition surveys, deterioration-curve calibration, Markov simulation, inspection-error models, maintenance-action matrices, dynamic or linear programming, reliability constraints, cost–benefit analysis and scenario sensitivity.

**Numerical models.** Models include homogeneous and time-varying Markov chains, continuous two-stage deterioration, partially observed maintenance decisions, data-driven condition curves, life-cycle-cost calculators and optimal preventive-timing frameworks.

**Experimental datasets.** The retained abstract evidence uses long-term condition and maintenance records for generic civil infrastructure, concrete bridges and pavements; direct breakwater, seawall and coastal-bridge records remain lawful-access targets.

**Validated ranges.** Evidence spans component and network decisions, discrete and continuous deterioration, perfect and imperfect inspection, fixed and changing transition rates, preventive and reactive actions, and short inspection intervals through multi-decade horizons.

**Recent advances.** Recent work uses data-calibrated and time-varying deterioration, explicit two-dimensional inspection error, timing-sensitive preventive maintenance, and integrated cost, environmental and reliability objectives.

**Disagreements.** Constant transition rates are convenient but may misstate aging and environment changes; fixed inspection schedules are simple but can waste resources; condition thresholds alone may omit consequences, while cost-only policies may violate reliability or sustainability goals.

**Limitations.** Coastal validation is presently weak in the lawful corpus; storm shocks, armor rearrangement, chloride and corrosion, scour, sea-level rise and adaptation are not captured by generic gradual-deterioration models; action-effect data are sparse.

**Open questions.** Priorities include coastal condition-state standards, event-driven deterioration, spatial dependence, remote inspection error, climate nonstationarity, adaptation flexibility, residual value, embodied carbon, ecological co-benefits and robust decision-making.

**Seminal papers.** Markov inspection–maintenance–replacement scheduling established sequential lifecycle decisions; later reliability and partially observable formulations incorporated safety and imperfect information.

## Claims

- **C959.** Markov-chain deterioration and average-cost sequential decision methods yield optimal inspection, maintenance, and replacement policies. *Regime: Transferable infrastructure lifecycle methodology; coastal calibration required..* [direct_finding, analytical] (Klein 1962, [doi:10.1287/mnsc.9.1.25](https://doi.org/10.1287/mnsc.9.1.25))
- **C960.** Condition-based maintenance for two-stage continuous deterioration must account jointly for false condition classification and measurement error in inspections. *Regime: Transferable infrastructure lifecycle methodology; coastal calibration required..* [direct_finding, analytical] (Wang 2024, [doi:10.1002/qre.3613](https://doi.org/10.1002/qre.3613))
- **C961.** A life-cycle-cost framework links periodic condition diagnosis, intervention planning, safety, and long-term infrastructure budgets. *Regime: Transferable infrastructure lifecycle methodology; coastal calibration required..* [direct_finding, analytical] (Oh 2023, [doi:10.3390/buildings13081983](https://doi.org/10.3390/buildings13081983))
- **C962.** Markov deterioration curves calibrated from condition data support life-cycle maintenance-cost estimates for concrete infrastructure. *Regime: Transferable infrastructure lifecycle methodology; coastal calibration required..* [direct_finding, numerical] (Petroutsatou 2025, [doi:10.3390/buildings15050807](https://doi.org/10.3390/buildings15050807))
- **C963.** Allowing Markov transition probabilities to change over time alters predicted deterioration and optimal maintenance intervention schedules. *Regime: Transferable infrastructure lifecycle methodology; coastal calibration required..* [direct_finding, numerical] (D 2020, [doi:10.47890/jceid/2020/dfernando/12045781](https://doi.org/10.47890/jceid/2020/dfernando/12045781))
- **C964.** Data-driven pavement deterioration and life-cycle cost analysis show preventive maintenance benefit is highly sensitive to intervention timing. *Regime: Transferable infrastructure lifecycle methodology; coastal calibration required..* [direct_finding, numerical] (Kim 2026, [doi:10.3390/su18084116](https://doi.org/10.3390/su18084116))
- **C1522.** A synthesis evaluates how offshore platforms and pipelines alter seascape ecological connectivity and how decommissioning choices affect those functions. *Regime: Influence of offshore oil and gas structures on seascape ecological connectivity.* [literature_review_statement, review] (Dianne McLean 2022, [doi:10.1111/gcb.16134](https://doi.org/10.1111/gcb.16134))
- **C1524.** A multi-purpose offshore-infrastructure assessment examines shared energy and aquaculture uses together with environmental pressures in the northern Adriatic. *Regime: Boosting Blue Growth in a Mild Sea: Analysis of the Synergies Produced by a Multi-Purpose Offshore Installation in the Northern Adriatic, Italy.* [literature_review_statement, review] (Barbara Zanuttigh 2015, [doi:10.3390/su7066804](https://doi.org/10.3390/su7066804))
- **C1525.** A review identifies flooding, storm surge, and hurricane mechanisms that threaten buried pipelines, tunnels, and culverts and organizes resilience measures. *Regime: Impact of flooding events on buried infrastructures: a review.* [literature_review_statement, review] (Ruth Abegaz 2024, [doi:10.3389/fbuil.2024.1357741](https://doi.org/10.3389/fbuil.2024.1357741))
- **C1602.** British coast-protection experience attributes important concrete deterioration to abrasion, chemical exposure, reinforcement corrosion and construction quality while finding frost, biological attack and alkali-aggregate reaction secondary in the reviewed cases. *Regime: DURABILITY OF CONCRETE IN COAST PROTECTION WORKS.* [direct_finding, field] (Allen 1968, [doi:10.9753/icce.v11.75](https://doi.org/10.9753/icce.v11.75))

## Papers

- Klein (1962). Inspection—Maintenance—Replacement Schedules Under Markovian Deterioration. *Management Science*. [doi:10.1287/mnsc.9.1.25](https://doi.org/10.1287/mnsc.9.1.25)
- Dianne McLean (2022). Influence of offshore oil and gas structures on seascape ecological connectivity. *Global Change Biology*. [doi:10.1111/gcb.16134](https://doi.org/10.1111/gcb.16134) [published version, CC BY-NC-ND](https://onlinelibrary.wiley.com/doi/pdfdirect/10.1111/gcb.16134)
- Barbara Zanuttigh (2015). Boosting Blue Growth in a Mild Sea: Analysis of the Synergies Produced by a Multi-Purpose Offshore Installation in the Northern Adriatic, Italy. *Sustainability*. [doi:10.3390/su7066804](https://doi.org/10.3390/su7066804) [published version, CC BY](https://www.mdpi.com/2071-1050/7/6/6804/pdf?version=1432812321)
- Wang (2024). Condition‐based maintenance management for two‐stage continuous deterioration with two‐dimensional inspection errors. *Quality and Reliability Engineering International*. [doi:10.1002/qre.3613](https://doi.org/10.1002/qre.3613)
- Ruth Abegaz (2024). Impact of flooding events on buried infrastructures: a review. *Frontiers in Built Environment*. [doi:10.3389/fbuil.2024.1357741](https://doi.org/10.3389/fbuil.2024.1357741) [published version, CC BY](https://www.frontiersin.org/articles/10.3389/fbuil.2024.1357741/pdf?isPublishedV2=False)
- Oh (2023). Life Cycle Cost Method for Safe and Effective Infrastructure Asset Management. *Buildings*. [doi:10.3390/buildings13081983](https://doi.org/10.3390/buildings13081983) [published version, CC BY](https://doi.org/10.3390/buildings13081983)
- Allen (1968). DURABILITY OF CONCRETE IN COAST PROTECTION WORKS. *Coastal Engineering Proceedings*. [doi:10.9753/icce.v11.75](https://doi.org/10.9753/icce.v11.75) [published version, CC BY](https://icce-ojs-tamu.tdl.org/icce/index.php/icce/article/download/2578/2243)
- Petroutsatou (2025). Life-Cycle Maintenance Cost Model for Concrete Bridges Using Markovian Deterioration Curves. *Buildings*. [doi:10.3390/buildings15050807](https://doi.org/10.3390/buildings15050807) [published version, CC BY](https://doi.org/10.3390/buildings15050807)
- D (2020). A Markovian-based methodology for the life-cycle cost analysis of bridge maintenance interventions under changing deterioration rates. *Journal of Civil Engineering Inter Disciplinaries*. [doi:10.47890/jceid/2020/dfernando/12045781](https://doi.org/10.47890/jceid/2020/dfernando/12045781)
- Kim (2026). Optimal Preventive Maintenance Timing for Expressway Asphalt Pavements Based on PMS Deterioration Modeling and Life-Cycle Cost Analysis. *Sustainability*. [doi:10.3390/su18084116](https://doi.org/10.3390/su18084116) [published version, CC BY](https://doi.org/10.3390/su18084116)
