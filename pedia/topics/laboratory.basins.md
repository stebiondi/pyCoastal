# Wave-basin experiments

`laboratory.basins` | Directional and three-dimensional modeling.

Parent: [Laboratory experiments](laboratory.md)

Papers: 10. Claims: 7. Equations: 0.

## Synthesis

**Well established.** Wave basins and broad physical-model facilities enable controlled spatial wave fields, structure loading, overtopping, and model coupling, but inference remains bounded by generation fidelity, basin boundaries, scale, geometry, and the measured response.

**Governing physics.** Relevant physics include directional generation and diffraction-reflection, irregular-wave grouping, evanescent modes near paddles, green-water impact and air-gap effects, dam-break bore hydraulics, overtopping depth and velocity, and drag dissipation by suspended canopies.

**Dimensionless parameters.** Important controls include Froude scale, relative depth and air gap, crest freeboard and slope cotangent, normalized force and pressure, wave steepness and spectral width, relative canopy density and spacing, transmission or reflection coefficients, and grouping statistics.

**Major equations.** Core formulations include Boussinesq-wave transfer to piston motion, spectral transfer functions, normalized impact force and pressure, shallow-water bore scaling, empirical overtopping depth-velocity-discharge relations, EurOtop guidance, XBeach non-hydrostatic dynamics, and canopy-drag energy dissipation.

**Typical methods.** Methods combine segmented or piston wavemakers, regular, irregular, focused, and multidirectional waves, spatial wave-gauge arrays, pressure and global-load sensing, optical or velocity measurements, dam-break releases, spectral analysis, deterministic numerical-physical coupling, and model-data benchmarking.

**Numerical models.** Models include MIKE 21 BW, deterministic wavemaker transfer with evanescent-mode correction, frequency-domain harbor response, XBeach non-hydrostatic, EurOtop design guidance, empirical bore relations, benthic-canopy models extended to suspended arrays, and a suspended seaweed-farm analytical model.

**Experimental datasets.** Reviewed datasets cover harbor grouping and agitation, deterministic transfer from MIKE 21 BW into physical wavemakers, 1:20 jacket green-water loads, full-scale dam-break analogues for overtopping, and an open Zenodo rigid suspended-canopy wave-dissipation campaign.

**Validated ranges.** Explicit bounds include 1:20 jacket tests with partial and full green water, dam-break analogues for 6<=cot(alpha)<=10, Tp>4 s and 1<=xc<=5 m, plus regular and random waves over tested rigid-canopy densities, lateral spacings, line spacings, and spectral widths.

**Recent advances.** Recent work uses full-geometric-scale dam-break bores to target individual hazardous overtopping flows and open configuration-rich datasets to evaluate suspended-canopy models, advancing from facility demonstration toward bounded model validation and reusable evidence.

**Disagreements.** Regular-wave coefficients may vary more than irregular-wave estimates within the main energy band, and model agreement depends on whether low-energy spectral tails, evanescent modes, air entrapment, impact peaks, and spatial canopy anisotropy are resolved.

**Limitations.** Limitations include sidewall and reflection contamination, finite directional resolution, wavemaker stroke and absorption, scale-dependent impact and aeration, limited repeat events, idealized fixed geometry, rigid instead of flexible canopies, and extrapolation outside explicit overtopping bounds.

**Open questions.** Priorities are reflection-controlled multidirectional benchmarks, uncertainty on extreme impact statistics, field validation of dam-break overtopping analogues, flexible and deforming suspended canopies, coupled current-wave forcing, and standardized open basin datasets with full calibration metadata.

**Seminal papers.** Within this branch, the 1989 harbor-basin study established grouping and spectral-response cautions, while the 2007 deterministic coupling study formalized transfer from numerical wave fields to 2D and 3D physical wavemakers.

## Claims

- **C229.** Unscaled dam-break bores reproduced non-impulsive overtopping characteristics for 6<=cot(alpha)<=10, Tp>4 s, and 1<=xc<=5 m from the crest edge, including flows capable of exceeding pedestrian-stability thresholds. *Regime: Gentle slopes 6<=cot(alpha)<=10, peak period Tp>4 s, and crestward distance 1<=xc<=5 m..* [direct_finding, experimental] (Bagg 2025, [doi:10.1016/j.coastaleng.2024.104695](https://doi.org/10.1016/j.coastaleng.2024.104695))
- **C230.** For tested rigid suspended canopies, wave dissipation increased with canopy density, wave height, wave period, narrower spectral width, and reduced lateral element spacing, while remaining relatively insensitive to cross-shore line spacing. *Regime: Tested rigid suspended-cylinder densities, wave heights, periods, spectral widths, lateral spacings, and cross-shore line spacings..* [direct_finding, experimental] (Zhang 2026, [doi:10.1016/j.coastaleng.2026.105095](https://doi.org/10.1016/j.coastaleng.2026.105095))
- **C1366.** A circular-basin experiment recreated the 25.6 m Draupner crest at scale only for large-angle crossing seas, where breaking became less crest-limiting and formed near-vertical jets. *Regime: Laboratory recreation of the Draupner wave and the role of breaking in crossing seas.* [direct_finding, experimental] (Mark L. McAllister 2018, [doi:10.1017/jfm.2018.886](https://doi.org/10.1017/jfm.2018.886))
- **C1418.** Directional wave-basin experiments and numerical simulations characterize the evolution of weakly nonlinear random directional waves. *Regime: Evolution of weakly nonlinear random directional waves: laboratory experiments and numerical simulations.* [direct_finding, experimental] (Alessandro Toffoli 2010, [doi:10.1017/s002211201000385x](https://doi.org/10.1017/s002211201000385x))
- **C1419.** Directional sea-state analysis links directional spreading and nonlinear evolution to kurtosis estimates used in freak-wave forecasting. *Regime: On the Estimation of the Kurtosis in Directional Sea States for Freak Wave Forecasting.* [direct_finding, mixed] (Mori 2011, [doi:10.1175/2011jpo4542.1](https://doi.org/10.1175/2011jpo4542.1))
- **C1420.** Field and laboratory measurements constrain maximum ocean-wave steepness and show its dependence on directional sea-state properties. *Regime: Maximum steepness of oceanic waves: Field and laboratory experiments.* [direct_finding, mixed] (Alessandro Toffoli 2010, [doi:10.1029/2009gl041771](https://doi.org/10.1029/2009gl041771))
- **C1421.** Laboratory observations and numerical calculations compare the breaking evolution of steep two-dimensional deep-water waves. *Regime: Numerical and laboratory investigation of breaking of steep two-dimensional waves in deep water.* [direct_finding, experimental] (Alexander V. Babanin 2010, [doi:10.1017/s002211200999245x](https://doi.org/10.1017/s002211200999245x))

## Papers

- Alessandro Toffoli (2010). Evolution of weakly nonlinear random directional waves: laboratory experiments and numerical simulations. *Journal of Fluid Mechanics*. [doi:10.1017/s002211201000385x](https://doi.org/10.1017/s002211201000385x) [published version, read only](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/0B1A3E4C72712BCC69C9BEF3CC79E3EA/S002211201000385Xa.pdf/div-class-title-evolution-of-weakly-nonlinear-random-directional-waves-laboratory-experiments-and-numerical-simulations-div.pdf)
- Mori (2011). On the Estimation of the Kurtosis in Directional Sea States for Freak Wave Forecasting. *Journal of Physical Oceanography*. [doi:10.1175/2011jpo4542.1](https://doi.org/10.1175/2011jpo4542.1) [published version, read only](https://journals.ametsoc.org/downloadpdf/journals/phoc/41/8/2011JPO4542.1.pdf)
- Alessandro Toffoli (2010). Maximum steepness of oceanic waves: Field and laboratory experiments. *Geophysical Research Letters*. [doi:10.1029/2009gl041771](https://doi.org/10.1029/2009gl041771) [submitted manuscript, read only](https://figshare.swinburne.edu.au/articles/journal_contribution/Maximum_steepness_of_oceanic_waves_Field_and_laboratory/26242466/1/files/47565974.pdf)
- Mark L. McAllister (2018). Laboratory recreation of the Draupner wave and the role of breaking in crossing seas. *Journal of Fluid Mechanics*. [doi:10.1017/jfm.2018.886](https://doi.org/10.1017/jfm.2018.886) [published version, CC BY](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/65EA3294DAFD97A50C8046140B45F759/S0022112018008868a.pdf/div-class-title-laboratory-recreation-of-the-draupner-wave-and-the-role-of-breaking-in-crossing-seas-div.pdf)
- Alexander V. Babanin (2010). Numerical and laboratory investigation of breaking of steep two-dimensional waves in deep water. *Journal of Fluid Mechanics*. [doi:10.1017/s002211200999245x](https://doi.org/10.1017/s002211200999245x) [published version, read only](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/7B0D24605A634F58C9C3DDE79C41CD9D/S002211200999245Xa.pdf/div-class-title-numerical-and-laboratory-investigation-of-breaking-of-steep-two-dimensional-waves-in-deep-water-div.pdf)
- Bagg (2025). Application of laboratory dam break experiments to non-impulsive wave overtopping. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2024.104695](https://doi.org/10.1016/j.coastaleng.2024.104695) [published version, CC BY](https://api.elsevier.com/content/article/PII:S0378383924002436?httpAccept=text/xml)
- Zhang (2026). Wave dissipation by rigid suspended canopies: Laboratory experiments and model evaluation. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2026.105095](https://doi.org/10.1016/j.coastaleng.2026.105095) [published version, CC BY](https://api.elsevier.com/content/article/PII:S0378383926001493?httpAccept=text/xml)
- Zhang (2007). Deterministic combination of numerical and physical coastal wave models. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2006.08.009](https://doi.org/10.1016/j.coastaleng.2006.08.009)
- AlMashan (2021). Experimental investigations on wave impact pressures under the deck and global wave forces and moments on offshore jacket platform for partial and full green water conditions. *Ocean Engineering*. [doi:10.1016/j.oceaneng.2021.109324](https://doi.org/10.1016/j.oceaneng.2021.109324)
- Quellet (1989). Wave Grouping Effect in Irregular Wave Agitation in Harbors. *Journal of Waterway, Port, Coastal, and Ocean Engineering*. [doi:10.1061/(asce)0733-950x(1989)115:3(363)](https://doi.org/10.1061/(asce)0733-950x(1989)115:3(363))
