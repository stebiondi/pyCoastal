# Phase-averaged wave models

`numerical.phase_averaged` | Spectral wave-action models.

Parent: [Numerical modeling](numerical.md)

Papers: 11. Claims: 8. Equations: 1.

## Synthesis

**Well established.** Phase-averaged spectral models efficiently propagate random directional wave energy across large coastal domains while representing generation, dissipation, refraction, shoaling, and nonlinear source terms; their reliability depends on whether omitted phase-coherent or low-frequency processes control the site.

**Governing physics.** The spectral action balance transports energy through physical and spectral space while wind input, whitecapping, bottom friction, breaking, triad and quartet interactions, and Bragg scattering act as source terms; bathymetry controls refraction and diffraction.

**Dimensionless parameters.** No single universal dimensionless parameter governs spectral-model validity. Relative depth, spectral bandwidth, directional spreading, exposure, and ratios of local wind-sea, sea-swell, and infragravity energy define process regimes and numerical sensitivity.

**Major equations.** Core formulations are the wave-action balance and its additive source terms, the Hasselmann Boltzmann integral for resonant four-wave transfer, and mild-slope-derived directional turning used for phase-decoupled diffraction.

**Typical methods.** Typical evaluation uses analytical benchmarks, laboratory diffraction observations, exact source-term solvers, regional model intercomparison, sensitivity to spectra/bathymetry/tides, and event-scale field validation against phase-resolving alternatives.

**Numerical models.** Models include SWAN with phase-decoupled diffraction, the WRT exact quartet-interaction solver, Longuet-Higgins spectral refraction, Kirby's parabolic refraction-diffraction method, and XBeach surfbeat as a complementary low-frequency comparator.

**Experimental datasets.** Reviewed evidence includes extreme diffraction benchmarks, a roughly 300 by 300 km Southern California Bight transformation case, and TC Olwyn observations with sustained winds above 130 km/h and forereef significant waves reaching 6 m.

**Validated ranges.** Validation is case-bound: phase-decoupled diffraction is for random short-crested fields without coherent standing patterns; Bight models perform best at moderately exposed sites; and SWAN's cyclone advantage was demonstrated for a shallow Ningaloo lagoon dominated by local wind growth.

**Recent advances.** Recent work increasingly diagnoses models by process completeness rather than class alone: the 2019 reef study identifies local wind-wave generation as decisive, while related nonhydrostatic studies expose breaking-turbulence and morphodynamic errors hidden by surface-wave calibration.

**Disagreements.** The Ningaloo comparison favored phase-averaged SWAN over surfbeat XBeach because local wind growth dominated, but this does not show that infragravity resolution is generally secondary; model ranking reverses when the omitted process changes.

**Limitations.** Phase averaging excludes coherent standing-wave fields and explicit infragravity phase dynamics; exact quartet interactions are expensive; sheltered predictions are sensitive to numerical bias; and agreement in wave height alone does not validate currents, sediment transport, or morphology.

**Open questions.** Needs include efficient accurate nonlinear source terms, robust diffraction near singular obstacles, joint wind-sea and infragravity capability, uncertainty propagation from offshore spectra and bathymetry, and validation of coupled wave-current-sediment responses.

**Seminal papers.** The 1993 Southern California Bight comparison is the earliest directly reviewed regional validation in this slice; the 2003 phase-decoupled diffraction paper is a foundational extension of SWAN's coastal-process capability.

## Equations

### Third-generation spectral action source balance

$$
S_{tot}=S_{inp}+S_{wcap}+S_{nl4}+S_{fric}+S_{brk}+S_{nl3}+S_{Bragg}
$$

Regime: Third-generation spectral wave-action models; shallow-water terms apply where relevant.

Variables: `S_inp` wind input; `S_wcap` whitecapping dissipation; `S_nl4` four-wave interactions; `S_fric` bottom friction; `S_brk` depth-limited breaking; `S_nl3` triad interactions; `S_Bragg` Bragg scattering

Source: (van Vledder 2006, [doi:10.1016/j.coastaleng.2005.10.011](https://doi.org/10.1016/j.coastaleng.2005.10.011))

## Claims

- **C133.** A mild-slope-derived phase-decoupled turning-rate formulation allowed SWAN to combine random-wave diffraction with refraction, shoaling, generation, dissipation, and wave-wave interactions, with reasonable agreement in extreme diffraction tests. *Regime: Random short-crested waves without coherent standing-wave patterns; diffraction regions require adequate local resolution..* [direct_finding, numerical] (L.H. Holthuijsen 2003, [doi:10.1016/s0378-3839(03)00065-6](https://doi.org/10.1016/s0378-3839(03)00065-6))
- **C134.** The WRT method evaluates the first-principles nonlinear four-wave interaction integral for discrete spectra and serves as an accuracy reference, but its computational cost limits direct operational use. *Regime: Weakly nonlinear spectral surface-gravity waves represented on discrete frequency-direction grids..* [direct_finding, analytical] (van Vledder 2006, [doi:10.1016/j.coastaleng.2005.10.011](https://doi.org/10.1016/j.coastaleng.2005.10.011))
- **C135.** In the roughly 300 km by 300 km Southern California Bight, broader incident frequency-direction spectra reduced model sensitivity and improved agreement, but neither the refraction nor refraction-diffraction model was accurate at highly sheltered sites. *Regime: The tested Southern California Bight bathymetry and incident spectra; strongest limitation where diffraction dominates low local energy..* [direct_finding, numerical] (W. C. O’Reilly 1993, [doi:10.1016/0378-3839(93)90032-4](https://doi.org/10.1016/0378-3839(93)90032-4))
- **C139.** During category-3 TC Olwyn at Ningaloo Reef, locally generated lagoon wind waves dominated over infragravity waves, so phase-averaged SWAN was more accurate than surfbeat-resolving XBeach for this specific event because SWAN represented wind-wave growth. *Regime: TC Olwyn at the roughly 1 km wide, 1 m deep Ningaloo lagoon; infragravity importance at other reefs is not negated..* [direct_finding, mixed] (Drost 2019, [doi:10.1016/j.coastaleng.2019.103525](https://doi.org/10.1016/j.coastaleng.2019.103525))
- **C1354.** Semiempirical spectral dissipation activates breaking above an observed nondimensional threshold, represents nonlinear swell and short-wave loss, and validates wave height, period and spectra from global to coastal scales despite residual systematic defects. *Regime: Semiempirical Dissipation Source Functions for Ocean Waves. Part I: Definition, Calibration, and Validation.* [direct_finding, mixed] (Fabrice Ardhuin 2010, [doi:10.1175/2010jpo4324.1](https://doi.org/10.1175/2010jpo4324.1))
- **C1360.** SWAN verification across five increasingly complex coastal field cases produced average RMS errors of 0.30 m in significant wave height and 0.7 s in mean period, about 10% of incident values. *Regime: A third‐generation wave model for coastal regions: 2. Verification.* [direct_finding, mixed] (R.C. Ris 1999, [doi:10.1029/1998jc900123](https://doi.org/10.1029/1998jc900123))
- **C1669.** Coastal WAVEWATCH III accuracy improves when currents, reflection and spatially varying bottom sediment are represented on efficient unstructured grids, but sub-100-m surf-zone resolution still requires better numerical schemes and coupled forcing. *Regime: French Atlantic, Channel and North Sea coastal wave fields on regional unstructured grids with currents, reflection and mapped bottom type..* [direct_finding, mixed] (Aron Roland 2014, [doi:10.1007/s10236-014-0711-z](https://doi.org/10.1007/s10236-014-0711-z))
- **C1703.** Third-generation spectral wave modeling has reduced bias in integral parameters, but improving spectral shape—especially high-frequency tails, extreme-condition physics, wave–current interaction and coastal boundary treatment—remains central to better forecasts and coupled applications. *Regime: Phase-averaged wind-wave modeling from deep water through shallow/coastal applications within spectral-model assumptions..* [literature_review_statement, review] (Luigi Cavaleri 2007, [doi:10.1016/j.pocean.2007.05.005](https://doi.org/10.1016/j.pocean.2007.05.005))

## Papers

- Fabrice Ardhuin (2010). Semiempirical Dissipation Source Functions for Ocean Waves. Part I: Definition, Calibration, and Validation. *Journal of Physical Oceanography*. [doi:10.1175/2010jpo4324.1](https://doi.org/10.1175/2010jpo4324.1)
- R.C. Ris (1999). A third‐generation wave model for coastal regions: 2. Verification. *Journal of Geophysical Research Atmospheres*. [doi:10.1029/1998jc900123](https://doi.org/10.1029/1998jc900123)
- Luigi Cavaleri (2007). Wave modelling – The state of the art. *Progress In Oceanography*. [doi:10.1016/j.pocean.2007.05.005](https://doi.org/10.1016/j.pocean.2007.05.005)
- L.H. Holthuijsen (2003). Phase-decoupled refraction–diffraction for spectral wave models. *Coastal Engineering*. [doi:10.1016/s0378-3839(03)00065-6](https://doi.org/10.1016/s0378-3839(03)00065-6)
- Aron Roland (2014). On the developments of spectral wave models: numerics and parameterizations for the coastal ocean. *Ocean Dynamics*. [doi:10.1007/s10236-014-0711-z](https://doi.org/10.1007/s10236-014-0711-z)
- W. C. O’Reilly (1993). A comparison of two spectral wave models in the Southern California Bight. *Coastal Engineering*. [doi:10.1016/0378-3839(93)90032-4](https://doi.org/10.1016/0378-3839(93)90032-4)
- van Vledder (2006). The WRT method for the computation of non-linear four-wave interactions in discrete spectral wave models. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2005.10.011](https://doi.org/10.1016/j.coastaleng.2005.10.011)
- Drost (2019). Predicting the hydrodynamic response of a coastal reef-lagoon system to a tropical cyclone using phase-averaged and surfbeat-resolving wave models. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2019.103525](https://doi.org/10.1016/j.coastaleng.2019.103525)
- Anna Nikishova (2017). Uncertainty quantification and sensitivity analysis applied to the wind wave model SWAN. *Environmental Modelling & Software*. [doi:10.1016/j.envsoft.2017.06.030](https://doi.org/10.1016/j.envsoft.2017.06.030)
- Kılar (2025). Wave storm impacts on shoreline evolution: A case study of Iztuzu beach. *Ocean &amp; Coastal Management*. [doi:10.1016/j.ocecoaman.2025.107748](https://doi.org/10.1016/j.ocecoaman.2025.107748)
- Jacobsen (2026). Wave attenuation through a saltmarsh: Heterogeneous vegetation characteristics and seasonal variability. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2026.105099](https://doi.org/10.1016/j.coastaleng.2026.105099)
