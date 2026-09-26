# Transmission through porous structures

`wave_structure.porous.transmission` | Wave-height and energy transmission controlled by permeability, porosity, geometry, and flow resistance.

Parent: [Wave-structure interaction](wave_structure.md) > [Porous structures](wave_structure.porous.md)

Papers: 3. Claims: 5. Equations: 2.

## Synthesis

**Well established.** Porous coastal structures partition incident wave energy among reflection, transmission and dissipation through internal flow resistance; performance depends jointly on porosity, material scale, thickness, submergence, water depth, incident spectrum and external breaking.

**Governing physics.** The adopted Darcy-Forchheimer resistance combines linear viscous and quadratic turbulent terms scaled by porosity and representative material diameter.

**Dimensionless parameters.** Porosity n, relative structure height hs/h, and dimensionless laminar and turbulent coefficients alpha0 and beta0 are central controls in the reviewed formulation.

**Major equations.** Observed wave-height transmission is Kt=sqrt(Ft/Fi), while the adopted equivalent-linearized porous theory gives Kt=1/(1+lambda) with lambda determined by wavenumber, porous width, porosity, and friction resistance.

**Typical methods.** Studies measure synchronized incident and lee waves across water levels and sea states, estimate spectral energy transmission, characterize porosity and geometry, calibrate Darcy–Forchheimer resistance, test emergence and submergence, close reflection–transmission–dissipation budgets and validate independently.

**Numerical models.** The reviewed model is an equivalent-linearized porous-transmission formulation using Darcy–Forchheimer resistance with fixed laminar and calibrated turbulent coefficients; it omits explicit external breaking and bottom friction.

**Experimental datasets.** Reviewed evidence comprises 290 boat-wake observations at a bundled-branch living-shoreline breakwall with estimated porosity 0.7, alongside a contrasting unbundled 0.9-porosity site whose geometry and tidal setting differed.

**Validated ranges.** With alpha0=1140 fixed and beta0=2.7 calibrated, the theory produced 16% mean absolute relative discrepancy across 290 GTM boat wakes; this is calibration performance, not independent validation.

**Recent advances.** Recent advances combine field-scale living structures, spectral transmission, porous RANS/VOF and resolved-element CFD, morphology and maintenance monitoring, uncertainty-aware calibration and hybrid formulations that couple internal resistance with external breaking.

**Disagreements.** Porosity alone cannot explain field transmission when bundling, thickness, material, water level, site and tidal range covary. Internal resistance models may perform while submerged but overtransmit near emergence where external breaking and friction dominate.

**Limitations.** Porous-only transmission theory overestimated transmitted energy near emergence because it omitted breaking and external bottom friction; its reliability deteriorated precisely where shallow-water dissipation became important.

**Open questions.** Independent validation is needed across materials, porosities, spectra, oblique incidence, storms, emergence states, and structures whose external breaking and overtopping interact with internal porous flow.

**Seminal papers.** Darcy and Forchheimer resistance established linear and quadratic porous-flow losses; rubble-mound wave theories coupled those losses to reflection and transmission, followed by equivalent-linear, volume-averaged and porous-media CFD formulations.

## Equations

### Observed wave-height transmission coefficient

$$
K_{T,data}=\sqrt{F_t/F_i}
$$

Regime: Linear-wave energy reconstruction from pressure/velocity at sensors immediately offshore and onshore of the breakwall.

Variables: `K_T_data` wave-height transmission coefficient derived from field data; `F_t` transmitted wave energy flux; `F_i` incident wave energy flux

Source: (Safak 2020, [doi:10.1016/j.csr.2020.104268](https://doi.org/10.1016/j.csr.2020.104268))

### Theoretical porous-breakwall transmission

$$
K_{T,theory}=H_t/H_i=1/(1+\lambda)
$$

Regime: Linearized Madsen theory with equivalent-linearized porous friction; omits shallow-water breaking and external bottom friction.

Variables: `H_t` transmitted wave height; `H_i` incident wave height; `lambda` dimensionless resistance term depending on wavenumber, width, friction factor, and porosity

Source: (Safak 2020, [doi:10.1016/j.csr.2020.104268](https://doi.org/10.1016/j.csr.2020.104268))

## Claims

- **C36.** For the 0.7-porosity bundled breakwall, wave-energy transmission increased with water depth most clearly when breakwall height divided by depth was approximately 0.5-1. *Regime: GTM deployment and its 1-1.5 m semidiurnal tide; not a universal depth law for all porous structures..* [direct_finding, field] (Safak 2020, [doi:10.1016/j.csr.2020.104268](https://doi.org/10.1016/j.csr.2020.104268))
- **C37.** With alpha0 fixed at 1140 and beta0 calibrated to 2.7, porous-transmission theory had 16% mean absolute relative discrepancy over 290 GTM wakes. *Regime: Madsen-type theory applied to the GTM 0.7-porosity breakwall and the 290 wakes used in calibration; this is not independent validation..* [direct_finding, mixed] (Safak 2020, [doi:10.1016/j.csr.2020.104268](https://doi.org/10.1016/j.csr.2020.104268))
- **C38.** The calibrated porous theory overpredicted transmitted energy most strongly in shallow water as the breakwall emerged, where omitted breaking and bottom friction became important. *Regime: Shallow/emergent GTM wake cases under the paper's theory; breaking and bottom-friction contributions were inferred, not separately measured..* [inferred_relationship, mixed] (Safak 2020, [doi:10.1016/j.csr.2020.104268](https://doi.org/10.1016/j.csr.2020.104268))
- **C39.** The observed transmission contrast between porosity 0.7 and 0.9 cannot be attributed to porosity alone because bundling, site, and tidal range also differed. *Regime: Comparison between GTM and NP; this bounds causal interpretation of the reported averages..* [inferred_relationship, field] (Safak 2020, [doi:10.1016/j.csr.2020.104268](https://doi.org/10.1016/j.csr.2020.104268))
- **C1722.** Two-dimensional flume tests show porous-breakwater transmission, reflection, and energy loss depend jointly on porosity, relative submergence, and width; the lowest transmission occurred for the least porous emerged case, while the lowest reflection occurred for the most porous submerged case. *Regime: Fixed vertical thick porous breakwaters at relative heights hb/h=0.8, 1.0, and 1.2 under regular waves..* [direct_finding, experimental] (Rahman 2014, [doi:10.7763/ijesd.2014.v5.530](https://doi.org/10.7763/ijesd.2014.v5.530))

## Papers

- Safak (2020). Wave transmission through living shoreline breakwalls. *Continental Shelf Research*. [doi:10.1016/j.csr.2020.104268](https://doi.org/10.1016/j.csr.2020.104268) [accepted manuscript, CC BY](https://repository.library.noaa.gov/view/noaa/34021/noaa_34021_DS1.pdf?download=1)
- Rahman (2014). The Effect of Porosity of Submerged and Emerged Breakwater on Wave Transmission. *International Journal of Environmental Science and Development*. [doi:10.7763/ijesd.2014.v5.530](https://doi.org/10.7763/ijesd.2014.v5.530) [published version, read only](http://www.ijesd.org/papers/530-G2001.pdf)
- van der Meer (2005). Wave transmission and reflection at low-crested structures: Design formulae, oblique wave attack and spectral change. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2005.09.005](https://doi.org/10.1016/j.coastaleng.2005.09.005) [published version, read only](https://www.vandermeerconsulting.nl/downloads/functional_b/2005_vandermeer_briganti.pdf)
