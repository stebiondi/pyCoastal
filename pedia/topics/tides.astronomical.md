# Tidal propagation

`tides.astronomical` | Amplitude, phase, and constituent propagation.

Parent: [Tides and coastal circulation](tides.md)

Papers: 12. Claims: 8. Equations: 0.

## Synthesis

**Well established.** Astronomical tides are predictable responses to gravitational forcing whose coastal amplitude and phase are transformed by basin geometry, depth, friction, resonance, rotation and nonlinear interaction; local prediction therefore requires both constituent forcing and regional calibration or validation.

**Governing physics.** Lunar and solar gravitational potential excites barotropic waves that propagate, reflect and resonate; Coriolis acceleration, bathymetric convergence, bottom friction, wetting/drying and nonlinear advection reshape constituents and generate overtides and compound shallow-water harmonics.

**Dimensionless parameters.** Controls include tidal amplitude-to-depth ratio, friction or Stokes number, basin length relative to tidal wavelength, Rossby number, resonance detuning, constituent signal-to-noise, admittance, amplitude and phase error, datum offset and ensemble spread-to-error ratios.

**Major equations.** Core formulations are rotating shallow-water mass and momentum equations with astronomical potential or open-boundary constituents, and harmonic representation eta(t)=Z0+sum f_n A_n cos(omega_n t+V_n+u_n-phi_n), including nodal factors and phase corrections.

**Typical methods.** Methods use long tide-gauge records, harmonic analysis, satellite altimetry and optical shoreline constraints, global or regional hydrodynamic models, constituent interpolation or assimilation, datum reconciliation, coastal ranking or ensembles, and independent validation of amplitudes, phases and reconstructed levels.

**Numerical models.** Current evidence evaluates and ensembles ten global tide models at the coast rather than endorsing one universal model; underlying models differ in grids, bathymetry, friction, assimilation and constituent sets, producing spatially varying strengths and common failure regions.

**Experimental datasets.** The reviewed evidence uses ten global tide models, satellite altimetry, optical NDWI water masks and Australian tide gauges to rank local members and construct coastal ensembles; direct basin-specific propagation datasets remain unreviewed in this node.

**Validated ranges.** Direct evidence is Australia-wide but restricted to locations supported by the satellite and gauge evaluation. Ensemble benefit is conditional on at least some competent members and cannot rescue coasts where all contributing models share large errors.

**Recent advances.** Recent advances combine coastal altimetry, optical shoreline occurrence, unstructured high-resolution models, data assimilation, locally ranked multi-model ensembles and probabilistic prediction to improve tides near complex and data-sparse coasts.

**Disagreements.** Pure harmonic prediction is efficient for stationary constituents, while hydrodynamic models better represent spatial propagation and nonlinear generation but depend on bathymetry and friction. Local ensembles reduce model-selection error yet may hide common bias and do not replace physics or observations.

**Limitations.** Limitations include short or gappy gauges, datum mismatch, coastal altimetry contamination, optical cloud and water-index uncertainty, unresolved channels, inaccurate bathymetry and friction, missing constituents, nodal and seasonal modulation, nonstationary morphology and shared bias among global models.

**Open questions.** Priorities include seamless coast–estuary constituent propagation, uncertainty-calibrated ensembles, datum automation, nonstationary morphology and sea-level effects, compound tide–surge–river interaction without double counting, optical constraints in turbid coasts and prediction where gauges are absent.

**Seminal papers.** Equilibrium tide theory, Laplace tidal equations and classical harmonic analysis established constituent prediction; amphidromic mapping, shallow-water harmonic theory and assimilative global tide models extended it to spatially varying coastal propagation.

## Claims

- **C146.** Across Australia, locally ranked ensembles of ten global tide models using altimetry and optical NDWI consistently outperformed individual models against tide gauges, but cannot provide reliable output where all contributing models are poor. *Regime: Australian coastal EO applications; NDWI ranks phase more directly than amplitude and sun-synchronous sampling limits some constituents..* [direct_finding, mixed] (Bishop-Taylor 2026, [doi:10.1080/01431161.2026.2666912](https://doi.org/10.1080/01431161.2026.2666912))
- **C1244.** A coastal water-level review finds interactions among mean sea level, tides, surge, waves and flooding vary strongly in space and time and can alter levels by several tens of centimeters, positively or negatively. *Regime: Interactions Between Mean Sea Level, Tide, Surge, Waves and Flooding: Mechanisms and Contributions to Sea Level Variations at the Coast.* [direct_finding, mixed] (Déborah Idier 2019, [doi:10.1007/s10712-019-09549-5](https://doi.org/10.1007/s10712-019-09549-5))
- **C1246.** In mixed-tide estuaries, principal-tide duration asymmetry combines with internally generated harmonics; skewness unifies amplitude/phase metrics and shows morphology must overcome mouth-imposed asymmetry before local ebb or flood dominance develops. *Regime: Tidal asymmetry in estuaries with mixed semidiurnal/diurnal tides.* [direct_finding, mixed] (Nicholas J. Nidzieko 2010, [doi:10.1029/2009jc005864](https://doi.org/10.1029/2009jc005864))
- **C1402.** FES2014 combines global hydrodynamic modeling and data assimilation to produce a validated high-resolution ocean-tide atlas for major and minor constituents. *Regime: FES2014 global ocean tide atlas: design and performance.* [direct_finding, mixed] (Florent Lyard 2021, [doi:10.5194/os-17-615-2021](https://doi.org/10.5194/os-17-615-2021))
- **C1403.** A high-resolution global dataset jointly represents extreme sea levels, tides and storm surges and supplies future projections for consistent coastal hazard analysis. *Regime: A High-Resolution Global Dataset of Extreme Sea Levels, Tides, and Storm Surges, Including Future Projections.* [direct_finding, numerical] (Sanne Muis 2020, [doi:10.3389/fmars.2020.00263](https://doi.org/10.3389/fmars.2020.00263))
- **C1547.** Abstract One of the most challenging areas in tidal analysis is the study of nonstationary signals with a tidal component, as they confront both current analysis methods and dynamical understanding. *Regime: The study system, forcing, data and methods stated in the indexed abstract..* [literature_review_statement, mixed] (Pascal Matte 2012, [doi:10.1175/jtech-d-12-00016.1](https://doi.org/10.1175/jtech-d-12-00016.1))
- **C1551.** Abstract This study examines the integrated influence of sea level rise (SLR) and future morphology on tidal hydrodynamics along the Northern Gulf of Mexico (NGOM) coast including seven embayments and three ecologically and economically significant estuaries. *Regime: The study system, forcing, data and methods stated in the indexed abstract..* [literature_review_statement, mixed] (Davina L. Passeri 2016, [doi:10.1002/2015ef000332](https://doi.org/10.1002/2015ef000332))
- **C1684.** In semi-closed convergent tidal channels, cross-section convergence and friction control resonant amplification and shift water-level and velocity nodes and antinodes; a multi-reach analytical solution incorporates longitudinal depth variation at negligible cost relative to full numerical simulation. *Regime: Semi-closed convergent channels with width/depth variation representable by piecewise reaches and tides within the linearized one-dimensional assumptions..* [direct_finding, analytical] (Cai 2016, [doi:10.1142/s0578563416500091](https://doi.org/10.1142/s0578563416500091))

## Papers

- Florent Lyard (2021). FES2014 global ocean tide atlas: design and performance. *Ocean science*. [doi:10.5194/os-17-615-2021](https://doi.org/10.5194/os-17-615-2021) [published version, CC BY](https://os.copernicus.org/articles/17/615/2021/os-17-615-2021.pdf)
- Sanne Muis (2020). A High-Resolution Global Dataset of Extreme Sea Levels, Tides, and Storm Surges, Including Future Projections. *Frontiers in Marine Science*. [doi:10.3389/fmars.2020.00263](https://doi.org/10.3389/fmars.2020.00263) [published version, CC BY](https://www.frontiersin.org/articles/10.3389/fmars.2020.00263/pdf)
- Nicholas J. Nidzieko (2010). Tidal asymmetry in estuaries with mixed semidiurnal/diurnal tides. *Journal of Geophysical Research: Oceans*. [doi:10.1029/2009jc005864](https://doi.org/10.1029/2009jc005864) [published version, read only](https://onlinelibrary.wiley.com/doi/pdfdirect/10.1029/2009JC005864)
- Déborah Idier (2019). Interactions Between Mean Sea Level, Tide, Surge, Waves and Flooding: Mechanisms and Contributions to Sea Level Variations at the Coast. *Surveys in Geophysics*. [doi:10.1007/s10712-019-09549-5](https://doi.org/10.1007/s10712-019-09549-5) [published version, CC BY](https://link.springer.com/content/pdf/10.1007/s10712-019-09549-5.pdf)
- Cai (2016). An Analytical Approach to Determining Resonance in Semi-Closed Convergent Tidal Channels. *Coastal Engineering Journal*. [doi:10.1142/s0578563416500091](https://doi.org/10.1142/s0578563416500091) [published version, CC BY](https://www.tandfonline.com/doi/pdf/10.1142/S0578563416500091?needAccess=true)
- Bishop-Taylor (2026). Optimising coastal tide predictions: an ensemble satellite altimetry and optical remote sensing approach. *International Journal of Remote Sensing*. [doi:10.1080/01431161.2026.2666912](https://doi.org/10.1080/01431161.2026.2666912) [published version, CC BY](https://www.tandfonline.com/doi/pdf/10.1080/01431161.2026.2666912)
- Pascal Matte (2012). Adaptation of Classical Tidal Harmonic Analysis to Nonstationary Tides, with Application to River Tides. *Journal of Atmospheric and Oceanic Technology*. [doi:10.1175/jtech-d-12-00016.1](https://doi.org/10.1175/jtech-d-12-00016.1) [published version, read only](https://journals.ametsoc.org/downloadpdf/journals/atot/30/3/jtech-d-12-00016_1.pdf)
- Davina L. Passeri (2016). Tidal hydrodynamics under future sea level rise and coastal morphology in the Northern Gulf of Mexico. *Earth s Future*. [doi:10.1002/2015ef000332](https://doi.org/10.1002/2015ef000332) [published version, CC BY-NC-ND](https://agupubs.onlinelibrary.wiley.com/doi/pdfdirect/10.1002/2015EF000332)
- David A. Jay (2009). Asymmetry of Columbia River tidal plume fronts. *Journal of Marine Systems*. [doi:10.1016/j.jmarsys.2008.11.015](https://doi.org/10.1016/j.jmarsys.2008.11.015) [published version, read only](https://depts.washington.edu/uwefm/publications/Jay_etal_JMS2009.pdf)
- Alejandro J. Souza (2001). Tidal mixing modulation of sea-surface temperature and diatom abundance in Southern California. *Continental Shelf Research*. [doi:10.1016/s0278-4343(00)00105-9](https://doi.org/10.1016/s0278-4343(00)00105-9) [published version, read only](https://www.sciencedirect.com/science/article/pii/S0278434300001059)
- Marcellin Samou Seujip (2024). Impact of mangrove on tidal propagation in a tropical coastal lagoon. *Environmental Earth Sciences*. [doi:10.1007/s12665-023-11349-5](https://doi.org/10.1007/s12665-023-11349-5) [submitted manuscript, read only](https://univ-rochelle.hal.science/hal-04882993v1/document)
- Pilar Díaz-Carrasco (2019). Non-cohesive and cohesive sediment transport due to tidal currents and sea waves: A case study. *Continental Shelf Research*. [doi:10.1016/j.csr.2019.06.008](https://doi.org/10.1016/j.csr.2019.06.008) [accepted manuscript, read only](https://digibug.ugr.es/bitstream/10481/95129/1/PAPER_CSR_2019_Non%20cohesive%20and%20cohesive%20sediment%20transport%20due%20to%20tidal%20currents%20and%20sea%20waves_A%20case%20study-1.pdf)
