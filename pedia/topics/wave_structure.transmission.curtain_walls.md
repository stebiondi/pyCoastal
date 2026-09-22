# Partially immersed curtain walls

`wave_structure.transmission.curtain_walls` | Wave passage beneath surface-piercing plates and curtain-type breakwaters.

Parent: [Wave-structure interaction](wave_structure.md) > [Transmission and reflection](wave_structure.transmission.md)

Papers: 2. Claims: 4. Equations: 1.

## Synthesis

**Well established.** A curtain wall attenuates waves by reflecting the upper water-column motion while permitting flow beneath its lower edge; transmission generally decreases with increasing draft, but reflection, dissipation, gap flow and structural load trade off.

**Governing physics.** A surface-piercing curtain reflects the upper wave mass while allowing underflow through the bottom gap; increasing draft strengthens reflection and reduces transmitted energy.

**Dimensionless parameters.** Principal controls include draft-to-depth and gap-to-depth ratios, kh, wave steepness or relative solitary-wave amplitude, curtain spacing and thickness relative to wavelength, transmission and reflection coefficients, dissipated-energy fraction and incidence angle.

**Major equations.** The reviewed study evaluates amplitude coefficients Kt=at/ai and Kr=ar/ai as functions of normalized curtain draft z/H.

**Typical methods.** Studies generate incident waves in a flume, separate incident and reflected signals with multiple gauges, measure lee waves and water levels near the gap, vary draft and bottom-mounted versus hanging orientation, compute energy coefficients, test conservation and document forces and three-dimensional leakage where available.

**Numerical models.** The current evidence is experiment-centered and evaluated with amplitude and energy coefficients. Potential-flow eigenfunction or boundary-integral models, CFD and double-curtain chamber models are represented only by title-only queue records pending full-text review.

**Experimental datasets.** Reviewed evidence comprises solitary-wave tests for a thin channel-spanning semi-submerged curtain and a fully submerged bottom-mounted barrier, including illustrated 14 cm water-depth cases with zero and 5 cm curtain draft.

**Validated ranges.** Explicit illustrated cases use H=14 cm and curtain drafts z=0 and 5 cm; the paper presents additional response points graphically but does not tabulate a complete numeric test matrix.

**Recent advances.** Recent advances use multi-curtain and perforated hybrids, resonant chambers, optimization across spectra, oblique-wave boundary-integral models, viscous CFD, flexible curtains and integrated wave-energy or harbor-protection concepts.

**Disagreements.** Greater draft reduces transmission but may increase reflection and wave force; adding chambers or multiple plates can enhance dissipation yet introduce resonance. Solitary-wave performance does not directly predict irregular spectral, oblique, current-affected or overtopping behavior.

**Limitations.** The reported maximum 60% energy dissipation applies to rigid thin channel-spanning walls under solitary waves and does not establish performance for irregular seas, oblique incidence, structural motion, or prototype scale.

**Open questions.** A fully tabulated parameter matrix and force measurements are needed across gap ratio, draft, wave nonlinearity, irregular spectra, oblique incidence, currents, and flexible or porous curtains.

**Seminal papers.** Linear potential-flow solutions for partial-depth barriers established reflection and transmission versus gap and kh; flume studies extended these relations to nonlinear waves, curtain breakwaters, double walls and chamber resonance.

## Equations

### Amplitude transmission and reflection

$$
K_t=a_t/a_i,\quad K_r=a_r/a_i
$$

Regime: Separated solitary waves before and after a thin vertical barrier.

Variables: `Kt` amplitude transmission coefficient; `Kr` amplitude reflection coefficient; `ai` incident solitary-wave amplitude; `at` transmitted amplitude; `ar` reflected amplitude

Source: (Горбань 2022, [doi:10.31471/2304-7399-2022-17(64)-118-132](https://doi.org/10.31471/2304-7399-2022-17(64)-118-132))

## Claims

- **C60.** Increasing the relative draft of the partially immersed curtain wall increased solitary-wave reflection and reduced transmitted-wave energy. *Regime: One-centimeter-thick full-width rigid curtain wall in the paper's horizontal flume and solitary-wave conditions..* [direct_finding, experimental] (Горбань 2022, [doi:10.31471/2304-7399-2022-17(64)-118-132](https://doi.org/10.31471/2304-7399-2022-17(64)-118-132))
- **C62.** The semi-submerged curtain wall dissipated up to 60% of incident solitary-wave energy, compared with up to 20% for the fully submerged bottom-mounted barrier. *Regime: The paper's thin vertical barriers and tested solitary waves; maxima should not be generalized to other spectra or geometries..* [direct_finding, experimental] (Горбань 2022, [doi:10.31471/2304-7399-2022-17(64)-118-132](https://doi.org/10.31471/2304-7399-2022-17(64)-118-132))
- **C63.** At zero curtain draft, most water passed below the wall with negligible or very small reflected wave; a 5 cm draft in 14 cm water produced stronger reflection and weaker transmission. *Regime: The illustrated H=14 cm curtain-wall trials..* [direct_finding, experimental] (Горбань 2022, [doi:10.31471/2304-7399-2022-17(64)-118-132](https://doi.org/10.31471/2304-7399-2022-17(64)-118-132))
- **C1694.** For the tested curtain-wall pile breakwater, reflection increases with wall-depth ratio and wave steepness: raising h/d from 0 to 0.7 increased Cr from about 0.21 to 0.49 at Hi/L=0.0097 and from about 0.36 to 0.60 at Hi/L=0.0499. *Regime: The tested precast curtain-wall pile-breakwater geometry, wall-depth ratios 0-0.7, and incident steepness cases Hi/L 0.0097 and 0.0499..* [direct_finding, mixed] (Khaldirian 2025, [doi:10.22146/jcef.15085](https://doi.org/10.22146/jcef.15085))

## Papers

- Горбань (2022). ВЗАЄМОДІЯ ПОВЕРХНЕВОЇ ПООДИНОКОЇ ХВИЛІ ІЗ ЗАНУРЕНИМ ТА НАПІВЗАНУРЕНИМ ХВИЛЕГАСНИКАМИ. *PRECARPATHIAN BULLETIN OF THE SHEVCHENKO SCIENTIFIC SOCIETY Number*. [doi:10.31471/2304-7399-2022-17(64)-118-132](https://doi.org/10.31471/2304-7399-2022-17(64)-118-132)
- Khaldirian (2025). Numerical Study of Wave Reflection by The Curtain Wall-Pile Breakwater Using the SPH Model. *Journal of the Civil Engineering Forum*. [doi:10.22146/jcef.15085](https://doi.org/10.22146/jcef.15085)
