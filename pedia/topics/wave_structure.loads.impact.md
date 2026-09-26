# Impact and impulsive loads

`wave_structure.loads.impact` | Slamming and short-duration loading.

Parent: [Wave-structure interaction](wave_structure.md) > [Wave loads](wave_structure.loads.md)

Papers: 7. Claims: 4. Equations: 2.

Used by pyCoastal design modules: Pile wave loads.

## Synthesis

**Well established.** Impulsive wave loads arise when breaking crests, bores or rapidly rising water strike structures over short durations; peak pressure, total impulse, rise time and spatial coherence must be distinguished from slower quasi-static wave and buoyancy loads.

**Governing physics.** Impact depends on local free-surface geometry and velocity, entrapped and entrained air, compressibility, ventilation, structural clearance and orientation. Air can cushion a direct impact or amplify oscillatory pressure as pockets compress, fragment and vent.

**Dimensionless parameters.** Controls include relative clearance, wave height and crest elevation, breaker type, Froude and Weber numbers, impact velocity normalized by sqrt(gL), air-pocket volume and compressibility, rise time relative to structural period, impulse coefficient, scale ratio and spatial pressure-correlation length.

**Major equations.** Engineering descriptions combine momentum or pressure-impulse balances with force integration over wetted area; dimensionless peak-force and impulse relations scale with density, velocity, gravity, characteristic length and clearance, while coupled hydroelastic equations add structural inertia, stiffness and damping.

**Typical methods.** Experiments synchronize wave gauges, high-rate pressure arrays, load cells and video, classify impact regimes, correct sensor and structural ringing, separate impulsive and quasi-static components, integrate pressure and force, repeat nominal conditions statistically and test scale and hydroelastic sensitivity.

**Numerical models.** Relevant approaches include pressure-impulse and semi-analytical slamming models, multiphase CFD with compressible or entrained air, fully nonlinear potential-flow kinematics and coupled CFD–FEM hydroelasticity; these direct model papers remain in the lawful-full-text queue.

**Experimental datasets.** Reviewed evidence includes a 1:25 exposed-jetty physical model with wavelet-corrected deck and beam forces and wave-in-deck experiments separating direct, large-air-pocket, small-air-pocket and bubble-plume regimes.

**Validated ranges.** Current reviewed support is limited to one scaled exposed-jetty configuration and one deck-impact regime study. It does not establish universal peak coefficients for monopiles, caissons, bridge groups, ships or flexible converters.

**Recent advances.** Recent advances combine ultrafast imaging and dense pressure arrays, compressible multiphase CFD, fully nonlinear incident kinematics, pressure-impulse models, coupled CFD–FEM simulation, Bayesian impact-regime classification and probabilistic load-duration design.

**Disagreements.** Peak pressure is highly sensitive to sensor bandwidth, local geometry, air and repeatability, so pressure peaks scale less robustly than impulse or global force. Air entrapment may cushion or amplify loads depending on pocket size, compression and venting.

**Limitations.** Scale effects in air compressibility, viscosity, surface tension and structural elasticity; uncertain breaker geometry; sparse pressure sampling; ringing; non-repeatability; and short records limit transfer. Rigid models cannot prove hydroelastic response or fatigue demand.

**Open questions.** Priorities include full-scale validation, probabilistic regime transitions, compressible multiphase scaling, spatial coherence, repeated-impact fatigue, flexible response, compound debris impact, uncertainty factors and transferable design metrics based on force, impulse and duration.

**Seminal papers.** Classical water-entry and Wagner impact theory established rapidly expanding wetted-area loads; pressure-impulse theory and breaking-wave experiments extended concepts to walls, decks and cylinders, followed by air-entrapment and hydroelastic studies.

## Equations

### dimensionless jetty deck and beam load equations

$$
\mathbf{F}(t)=\int_A -p\mathbf{n}\,dA+\mathbf{F}_{D,I}
$$

Regime: 1:25 exposed-jetty head with 2-D and 3-D configurations, inundation, and down-standing beams; excludes tsunami and waves with period above 25 s.

Variables: `F` resultant structural load; `p` hydrodynamic or pneumatic pressure; `n` surface normal; `A` wetted or impacted area; `F_D,I` drag/inertia contribution where applicable; normalized load balance

Source: (Cuomo 2007, [doi:10.1016/j.coastaleng.2007.01.010](https://doi.org/10.1016/j.coastaleng.2007.01.010))

### multiscale air-entrapped wave-impact model

$$
\mathbf{F}(t)=\int_A -p\mathbf{n}\,dA+\mathbf{F}_{D,I}
$$

Regime: Flat-deck wave impact with air structures from tens of microns/millimetres to several/dozens of metres; validated using a typical dam-break impact case.

Variables: `F` resultant structural load; `p` hydrodynamic or pneumatic pressure; `n` surface normal; `A` wetted or impacted area; `F_D,I` drag/inertia contribution where applicable; normalized load balance

Source: (Zhou 2024, [doi:10.1016/j.coastaleng.2023.104431](https://doi.org/10.1016/j.coastaleng.2023.104431))

## Claims

- **C281.** For a 1:25 exposed-jetty model, wavelet-corrected measurements separated quasi-static and impulsive deck and beam loads; the new dimensionless method reduced relative prediction error for quasi-static external-deck uplift to 0.050, versus 0.080-0.344 for the compared methods. *Regime: Exposed pile-supported jetties and similar suspended decks under irregular waves within the tested relative geometry and clearance regime..* [direct_finding, experimental] (Cuomo 2007, [doi:10.1016/j.coastaleng.2007.01.010](https://doi.org/10.1016/j.coastaleng.2007.01.010))
- **C286.** Wave-in-deck impacts separate into direct, large-air-pocket, small-air-pocket, and bubble-plume regimes, whose compression and breakup can produce either cushioning or load amplification. *Regime: Flat-deck wave impact with air structures from tens of microns/millimetres to several/dozens of metres; validated using a typical dam-break impact case..* [direct_finding, numerical] (Zhou 2024, [doi:10.1016/j.coastaleng.2023.104431](https://doi.org/10.1016/j.coastaleng.2023.104431))
- **C1565.** The applicability of pressure-impulse theory is evaluated for predicting wave impact loading magnitudes for non-breaking standing wave impacts on vertical hydraulic structures with relatively short overhangs. *Regime: The study system, forcing, data and methods stated in the indexed abstract..* [literature_review_statement, mixed] (Ermano de Almeida 2020, [doi:10.1016/j.coastaleng.2020.103702](https://doi.org/10.1016/j.coastaleng.2020.103702))
- **C1567.** This paper presents results from an experiment designed to improve the understanding of the relationship between extreme breaking waves and their mechanical loading on heritage offshore lighthouses. *Regime: The study system, forcing, data and methods stated in the indexed abstract..* [literature_review_statement, mixed] (Jean‐François Filipot 2019, [doi:10.1098/rsta.2019.0008](https://doi.org/10.1098/rsta.2019.0008))

## Papers

- Cuomo (2007). Wave-in-deck loads on exposed jetties. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2007.01.010](https://doi.org/10.1016/j.coastaleng.2007.01.010) [published version, read only](https://www.researchgate.net/publication/223859400_Wave-in-deck_loads_on_exposed_jetties)
- Zhou (2024). Multiscale air entrainment in wave-in-deck loads. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2023.104431](https://doi.org/10.1016/j.coastaleng.2023.104431)
- K.M. Theresa Kleefsman (2005). A Volume-of-Fluid based simulation method for wave impact problems. *Journal of Computational Physics*. [doi:10.1016/j.jcp.2004.12.007](https://doi.org/10.1016/j.jcp.2004.12.007) [published version, read only](https://www.sciencedirect.com/science/article/pii/S0021999104005170)
- Mohsen Azadbakht (2016). Effect of trapped air on wave forces on coastal bridge superstructures. *Journal of Ocean Engineering and Marine Energy*. [doi:10.1007/s40722-016-0043-9](https://doi.org/10.1007/s40722-016-0043-9) [published version, read only](https://link.springer.com/content/pdf/10.1007/s40722-016-0043-9.pdf)
- Ermano de Almeida (2020). Validation of pressure-impulse theory for standing wave impact loading on vertical hydraulic structures with short overhangs. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2020.103702](https://doi.org/10.1016/j.coastaleng.2020.103702) [published version, CC BY](https://www.sciencedirect.com/science/article/pii/S0378383919306003?via%3Dihub)
- David J. McGovern (2022). Large-scale experiments on tsunami inundation and overtopping forces at vertical sea walls. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2022.104222](https://doi.org/10.1016/j.coastaleng.2022.104222) [published version, CC BY](https://www.sciencedirect.com/science/article/pii/S0378383922001351/pdf)
- Jean‐François Filipot (2019). La Jument lighthouse: a real-scale laboratory for the study of giant waves and their loading on marine structures. *Philosophical Transactions of the Royal Society A Mathematical Physical and Engineering Sciences*. [doi:10.1098/rsta.2019.0008](https://doi.org/10.1098/rsta.2019.0008) [published version, read only](https://royalsocietypublishing.org/doi/pdf/10.1098/rsta.2019.0008)
