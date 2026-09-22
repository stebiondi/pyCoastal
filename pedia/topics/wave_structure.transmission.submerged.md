# Submerged barriers

`wave_structure.transmission.submerged` | Transmission, reflection, dissipation, and loading for structures whose crests remain below or near the free surface.

Parent: [Wave-structure interaction](wave_structure.md) > [Transmission and reflection](wave_structure.transmission.md)

Papers: 8. Claims: 13. Equations: 4.

## Synthesis

**Well established.** Submergence relative to water depth and wave height strongly controls transmission: deeper water cover generally increases passage, while a crest near the still-water level can maximize breaking and dissipation for some rigid geometries.

**Governing physics.** Submerged structures transform waves through partial blockage, shoaling over the crest, reflection at depth changes, nonlinear free-surface motion, breaking and turbulent separation; greater water cover usually reduces interaction, while crest-level conditions can maximize breaking and dissipation.

**Dimensionless parameters.** Reviewed controls include crest cover Rc/d and Rc/Hi, crest width B/L, wave steepness, relative depth kd, relative barrier height h/H, solitary-wave interaction a/(H-h), and the composite beta=Rc^2 sqrt(L)/(d Hi sqrt(B)).

**Major equations.** Common response measures are Kt=Ht/Hi, Kr=Hr/Hi, and an energy remainder based on 1-Kt^2-Kr^2; care is needed because some studies report the remainder itself while others report its square root as an amplitude-like loss coefficient.

**Typical methods.** Studies measure incident, reflected and transmitted waves with gauge arrays, vary water depth, cover, crest width and shape, separate waves and compute amplitude and energy coefficients, test regular, irregular or solitary forcing, compare material volume and validate empirical dimensionless fits independently.

**Numerical models.** The reviewed branch emphasizes laboratory response and empirical logarithmic transmission/reflection fits. Potential-flow, eigenfunction, CFD and practical fixed-structure models are represented by title-only queue records pending lawful full-text review.

**Experimental datasets.** Reviewed evidence includes solitary waves at 11-14 cm height, 75 JONSWAP tests with periods 1.1-1.9 s and cover 0.05-0.15 m across five smooth sections, and 216 regular-wave tests spanning 0.02-0.38 m height, 0.8-2.5 s period and B/L 0.17-1.22.

**Validated ranges.** The reviewed experiments cover solitary-wave examples at H=11-14 cm; 75 JONSWAP tests with Tp=1.1-1.9 s, d=0.30-0.40 m, Rc=0.05-0.15 m and steepness 0.018-0.055; and 216 regular-wave semicircular tests with Hi=0.02-0.38 m, T=0.8-2.5 s, d/h=0.667-1.667 and B/L=0.17-1.22.

**Recent advances.** Recent advances optimize shape and material volume across irregular spectra, use high-resolution free-surface imaging and PIV, couple RANS/VOF with turbulence and air, explore metamaterial or resonant plates and apply probabilistic multiobjective design under tidal water-level variation.

**Disagreements.** Reported maximum attenuation is not directly comparable across geometries and forcing: the solitary-wave submerged plate dissipated up to 20%, whereas the crest-level semicircular barrier reached up to 90% energy dissipation for short regular waves; these values reflect different response definitions, spectra, widths, and immersion states.

**Limitations.** The reviewed ranges remain laboratory- and geometry-specific; none resolves irregular oblique waves with currents, tidal water-level variation, sediment response, structural motion or failure, and field-scale validation together.

**Open questions.** Transferable design requires harmonized coefficient definitions and experiments spanning geometry, permeability, spectra, obliquity, currents, sediment, structural loading, and changing water levels.

**Seminal papers.** Linear potential-flow and eigenfunction solutions established plate and submerged-barrier coefficients; laboratory studies introduced breaking and nonlinear regimes, followed by empirical low-crested-breakwater formulas and phase-resolving or viscous numerical models.

## Equations

### Submerged-barrier interaction coefficient

$$
K_{int}=a/(H-h)
$$

Regime: Solitary wave crossing a thin bottom-mounted submerged plate.

Variables: `Kint` wave-barrier interaction coefficient; `a` incident wave amplitude; `H` still-water depth; `h` bottom-mounted barrier height

Source: (Горбань 2022, [doi:10.31471/2304-7399-2022-17(64)-118-132](https://doi.org/10.31471/2304-7399-2022-17(64)-118-132))

### Wave coefficients

$$
K_t=H_t/H_i,\quad K_r=H_r/H_i,\quad K_d=1-K_t^2-K_r^2
$$

Regime: Spectrally separated irregular waves around an impermeable submerged breakwater.

Variables: `Kt` wave-height transmission coefficient; `Kr` wave-height reflection coefficient; `Kd` energy dissipation fraction; `Hi` incident significant wave height; `Ht` transmitted significant wave height; `Hr` reflected significant wave height

Source: (Mahmoudof 2021, [doi:10.1016/j.oceano.2021.05.002](https://doi.org/10.1016/j.oceano.2021.05.002))

### Composite submerged-breakwater parameter

$$
\beta=R_c^2 L^{1/2}/(d H_i B^{1/2})
$$

Regime: Smooth impermeable rectangular-section breakwaters in the reported ranges; trapezoids require different fitted coefficients.

Variables: `beta` composite response parameter; `Rc` crest submergence; `L` local wavelength; `d` local water depth; `Hi` incident wave height; `B` crest width

Source: (Mahmoudof 2021, [doi:10.1016/j.oceano.2021.05.002](https://doi.org/10.1016/j.oceano.2021.05.002))

### Semicircular-breakwater wave coefficients

$$
C_T=H_T/H_i,\quad C_R=H_R/H_i,\quad C_L=\sqrt{1-C_T^2-C_R^2}
$$

Regime: Regular-wave measurements around the tested impermeable semicircular breakwater.

Variables: `CT` wave-height transmission coefficient; `CR` reflection coefficient; `CL` energy-loss coefficient; `HT` transmitted height; `HR` reflected height; `Hi` incident height

Source: (Al-Towayti 2024, [doi:10.3390/jmse12071105](https://doi.org/10.3390/jmse12071105))

## Claims

- **C61.** For the bottom-mounted submerged plate, the interaction changed from smooth soliton splitting to intense local free-surface oscillation when incident amplitude divided by water cover over the plate crossed a critical value near one. *Regime: Thin submerged vertical plate and solitary waves; reported threshold is approximate..* [direct_finding, experimental] (Горбань 2022, [doi:10.31471/2304-7399-2022-17(64)-118-132](https://doi.org/10.31471/2304-7399-2022-17(64)-118-132))
- **C64.** Seventy-five JONSWAP tests covered peak periods 1.1-1.9 s, local depths 0.30-0.40 m, crest submergence 0.05-0.15 m, and wave steepness 0.018-0.055 across five smooth impermeable sections. *Regime: Two-dimensional normally incident irregular waves; 0.25 m high smooth PVC barriers..* [direct_finding, experimental] (Mahmoudof 2021, [doi:10.1016/j.oceano.2021.05.002](https://doi.org/10.1016/j.oceano.2021.05.002))
- **C65.** Relative submergence Rc/d was the most influential individual dimensionless control on measured transmission and reflection among the simple ratios evaluated. *Regime: The four rectangular/toothed sections and reported JONSWAP tests..* [direct_finding, experimental] (Mahmoudof 2021, [doi:10.1016/j.oceano.2021.05.002](https://doi.org/10.1016/j.oceano.2021.05.002))
- **C66.** For rectangular sections, beta=Rc^2 sqrt(L)/(d Hi sqrt(B)) produced a single increasing logarithmic Kt fit with R2=0.97 and a decreasing logarithmic Kr fit with R2=0.86. *Regime: The reported smooth rectangular and toothed sections; coefficients are geometry-specific outside that family..* [direct_finding, experimental] (Mahmoudof 2021, [doi:10.1016/j.oceano.2021.05.002](https://doi.org/10.1016/j.oceano.2021.05.002))
- **C67.** A 0.60 m wide rectangular wedge transmitted about 30% less and dissipated about 40% more energy than a trapezoidal wedge with the same upper width at 0.40 m water depth, while using about 45% less material volume. *Regime: Specific BS2 versus BS5 geometries at d=0.40 m; not a universal rectangle-versus-trapezoid rule..* [direct_finding, experimental] (Mahmoudof 2021, [doi:10.1016/j.oceano.2021.05.002](https://doi.org/10.1016/j.oceano.2021.05.002))
- **C68.** The 216 physical tests spanned incident heights 0.02-0.38 m, periods 0.8-2.5 s, steepness 0.02-0.06, relative depth d/h=0.667-1.667, and relative width B/L=0.17-1.22. *Regime: R=h=0.6 m semicircular concrete model under regular waves..* [direct_finding, experimental] (Al-Towayti 2024, [doi:10.3390/jmse12071105](https://doi.org/10.3390/jmse12071105))
- **C69.** At crest-level submergence d/h=1.0, short-period regular waves experienced up to 70% incident-height reduction and up to 90% energy dissipation. *Regime: The tested semicircular breakwater and shorter-period portion of T=0.8-2.5 s; not all B/L and steepness combinations attained these maxima..* [direct_finding, mixed] (Al-Towayti 2024, [doi:10.3390/jmse12071105](https://doi.org/10.3390/jmse12071105))
- **C70.** Fully submerged cases transmitted substantially more wave height: CT ranged 0.59-0.99 at d/h=1.333 and 0.68-0.98 at d/h=1.667. *Regime: The study's regular waves and semicircular model..* [direct_finding, mixed] (Al-Towayti 2024, [doi:10.3390/jmse12071105](https://doi.org/10.3390/jmse12071105))
- **C71.** Energy-dissipation performance deteriorated as immersion depth increased beyond the crest-level configuration. *Regime: d/h=1.0, 1.333, and 1.667 for the tested regular-wave matrix..* [direct_finding, mixed] (Al-Towayti 2024, [doi:10.3390/jmse12071105](https://doi.org/10.3390/jmse12071105))
- **C1580.** With the recent development from grey infrastructures to green infrastructures, artificial reefs become more popular in coastal protection projects. *Regime: The study system, forcing, data and methods stated in the indexed abstract..* [direct_finding, numerical] (Cuiping Kuang 2023, [doi:10.3390/w15213832](https://doi.org/10.3390/w15213832))
- **C1584.** Abstract To address the survivability and energy capture efficiency of Oscillating Wave Surge Converters (OWSCs) under extreme sea states, this study develops a high-fidelity numerical model coupling Riemann-based Weakly Compressible Smoothed Particle Hydrodynamics (Riemann-based WCSPH) with multi-body dynamics. *Regime: The study system, forcing, data and methods stated in the indexed abstract..* [literature_review_statement, mixed] (Miaomiao Guo 2026, [doi:10.1038/s41598-026-69055-8](https://doi.org/10.1038/s41598-026-69055-8))
- **C1585.** Tsunami wave overtopping remains a major challenge for conventional vertical seawalls. *Regime: The study system, forcing, data and methods stated in the indexed abstract..* [direct_finding, mixed] (Weixiao Jiang 2026, [doi:10.28991/cej-2026-012-04-01](https://doi.org/10.28991/cej-2026-012-04-01))
- **C1733.** DELOS synthesis of more than 2,300 tests yields regime-specific low-crested-structure transmission formulas: rubble-mound transmission is nearly insensitive to obliquity, whereas smooth structures show cosine-dependent transmission and cap transmitted direction near 45 degrees for larger incident angles. *Regime: Smooth and rubble-mound low-crested or submerged structures under random waves, varying relative crest width and oblique incidence..* [direct_finding, mixed] (van der Meer 2005, [doi:10.1016/j.coastaleng.2005.09.005](https://doi.org/10.1016/j.coastaleng.2005.09.005))

## Papers

- van der Meer (2005). Wave transmission and reflection at low-crested structures: Design formulae, oblique wave attack and spectral change. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2005.09.005](https://doi.org/10.1016/j.coastaleng.2005.09.005)
- Mahmoudof (2021). Experimental study of hydraulic response of smooth submerged breakwaters to irregular waves. *Oceanologia*. [doi:10.1016/j.oceano.2021.05.002](https://doi.org/10.1016/j.oceano.2021.05.002)
- Al-Towayti (2024). Hydrodynamic Performance Assessment of Emerged, Alternatively Submerged and Submerged Semicircular Breakwater: An Experimental and Computational Study. *Journal of Marine Science and Engineering*. [doi:10.3390/jmse12071105](https://doi.org/10.3390/jmse12071105)
- Горбань (2022). ВЗАЄМОДІЯ ПОВЕРХНЕВОЇ ПООДИНОКОЇ ХВИЛІ ІЗ ЗАНУРЕНИМ ТА НАПІВЗАНУРЕНИМ ХВИЛЕГАСНИКАМИ. *PRECARPATHIAN BULLETIN OF THE SHEVCHENKO SCIENTIFIC SOCIETY Number*. [doi:10.31471/2304-7399-2022-17(64)-118-132](https://doi.org/10.31471/2304-7399-2022-17(64)-118-132)
- Rahman (2014). The Effect of Porosity of Submerged and Emerged Breakwater on Wave Transmission. *International Journal of Environmental Science and Development*. [doi:10.7763/ijesd.2014.v5.530](https://doi.org/10.7763/ijesd.2014.v5.530)
- Cuiping Kuang (2023). Numerical Modelling of Beach Profile Evolution with and without an Artificial Reef. *Water*. [doi:10.3390/w15213832](https://doi.org/10.3390/w15213832)
- Miaomiao Guo (2026). Numerical study of the nonlinear interaction and energy capture of an OWSC under multi-frequency focused freak waves using Riemann-SPH. *Scientific Reports*. [doi:10.1038/s41598-026-69055-8](https://doi.org/10.1038/s41598-026-69055-8)
- Weixiao Jiang (2026). Numerical Assessment of Integrated Perforated and Recurved Seawall Designs for Tsunami Mitigation. *Civil Engineering Journal*. [doi:10.28991/cej-2026-012-04-01](https://doi.org/10.28991/cej-2026-012-04-01)
