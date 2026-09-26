# Extreme-event observations

`field.extreme` | Storm and tsunami field measurements.

Parent: [Field measurements](field.md)

Papers: 10. Claims: 7. Equations: 5.

Used by pyCoastal design modules: Design conditions.

## Synthesis

**Well established.** Extreme coastal events require direct observations because storm and tsunami response depends on time-varying waves, water levels, currents, sediment, bathymetry, structures and ecosystems in combinations not captured by single bulk forcing metrics.

**Governing physics.** Observed response is governed by tsunami momentum and Froude regime, wave-current interaction, spectral period and bimodality, breaking and setup, runup and overwash, vegetation drag, structure diversion, undertow, longshore currents, sediment suspension and antecedent morphology.

**Dimensionless parameters.** Important controls include Froude number, wave steepness, relative freeboard, barrier inertia, Shields mobility, relative depth, directional angle, spectral bimodality, structure or vegetation density, normalized surge, and model skill or uncertainty metrics.

**Major equations.** Field interpretation couples nonlinear shallow-water or surfbeat equations, wave-action models, sediment-flux integration, Froude scaling, overtopping and runup thresholds, vegetation drag and moment, XBeach-G wave-by-wave physics, and nonlinear data-driven waveform transfer.

**Typical methods.** Methods include post-event transects, video velocimetry, pressure and tide gauges, offshore pressure sensors, GPS buoys, movable instrument sleds, laser scanning, repeated profiles, sediment concentration arrays, remote sensing, numerical reconstruction and real-time assimilation.

**Numerical models.** Models include modified depth-integrated tsunami equations, regularized extreme learning machines, XBeach-G, SWAN and XBeach surfbeat configurations, direct suspended-flux integration, and event-specific shoreline or nourishment analyses.

**Experimental datasets.** Key datasets include a 340 km post-Tohoku survey, multi-instrument Tohoku waveforms, five Duck storm sediment transects, two Lake Michigan storm-current campaigns, 2 Hz Loe Bar overwash scans, Upham hurricane nourishment surveys and Ningaloo cyclone reef-lagoon observations.

**Validated ranges.** Explicit regimes include Sendai U=6.2 m/s and Fr=1.14-1.4; Duck Hm0 to 3.5 m and transport to 1780 m3/h; Loe Bar Hs=4 m, Hmax=8 m and Tp=10-15 s with under-5% hydrodynamic error; and barred-beach currents to 1.8 m/s.

**Recent advances.** High-frequency laser scanning now resolves overwash hydraulics and morphology, nonlinear machine learning accelerates near-field tsunami waveform forecasts, and coupled observations reveal when local wind waves, vegetation, structures or antecedent morphology dominate expected hazard response.

**Disagreements.** The CERC longshore formula alternated between over- and underprediction during storms. A surfbeat-resolving model was not superior during TC Olwyn because locally generated wind waves dominated. Hard structures can shield locally yet divert and concentrate damaging flow elsewhere.

**Limitations.** Extreme measurements are sparse, dangerous and often opportunistic; instruments fail or perturb flow, post-event marks mix processes, bedload may be unmeasured, pier effects and changing morphology bias transects, and event-calibrated models may not transfer to different spectra or sites.

**Open questions.** Priorities include redundant interoperable sensors, rapid bathymetry updates, bedload measurement during storms, uncertainty-aware real-time assimilation, compound-event observations, standardized post-event protocols, and validation across events larger than the calibration record.

**Seminal papers.** The 1981 barred-beach storms and 1999 Duck transport campaign established quasi-synoptic and flux-resolving storm observations; the 2011 Tohoku event enabled unprecedented regional surveys and multi-gauge tsunami reconstruction.

## Equations

### barred-beach longshore-current field dataset

$$
y(t,\mathbf{x})=\mathcal{M}[\mathbf{o}(t),\mathbf{b},\mathbf{p}]
$$

Regime: Profiles every about 3 h for 24 and 28 h; incident angle about 30 degrees; Hrms breaker height <=1.5 m; bar about 30 m offshore and 0.75 m deep in calm conditions.

Variables: `y` predicted or derived coastal response; `o` event observations; `b` bathymetry or beach state; `p` model or instrument parameters; normalized observation-model mapping

Source: (Allender 1981, [doi:10.1016/0378-3839(81)90020-x](https://doi.org/10.1016/0378-3839(81)90020-x))

### modified 2-D tsunami shallow-water model

$$
y(t,\mathbf{x})=\mathcal{M}[\mathbf{o}(t),\mathbf{b},\mathbf{p}]
$$

Regime: Twenty-five locations over about 340 km; detailed Misawa vegetated-dune and Hachinohe seawall/forest cases; Sendai video evidence.

Variables: `y` predicted or derived coastal response; `o` event observations; `b` bathymetry or beach state; `p` model or instrument parameters; normalized observation-model mapping

Source: (Nandasena 2012, [doi:10.1016/j.coastaleng.2012.03.009](https://doi.org/10.1016/j.coastaleng.2012.03.009))

### regularized extreme learning machine tsunami forecaster

$$
y(t,\mathbf{x})=\mathcal{M}[\mathbf{o}(t),\mathbf{b},\mathbf{p}]
$$

Regime: 2011 Tohoku waveforms from four OBP gauges plus GPS buoys, wave gauges and tide gauges; example inversion window 35 min.

Variables: `y` predicted or derived coastal response; `o` event observations; `b` bathymetry or beach state; `p` model or instrument parameters; normalized observation-model mapping

Source: (Mulia 2016, [doi:10.1016/j.coastaleng.2015.11.010](https://doi.org/10.1016/j.coastaleng.2015.11.010))

### XBeach-G gravel-barrier overwash model

$$
y(t,\mathbf{x})=\mathcal{M}[\mathbf{o}(t),\mathbf{b},\mathbf{p}]
$$

Regime: Loe Bar D50=2-4 mm; offshore Hs=4 m, Hmax=8 m, Tp=10-15 s, spring high tide 2.45 m and surge about 0.15 m.

Variables: `y` predicted or derived coastal response; `o` event observations; `b` bathymetry or beach state; `p` model or instrument parameters; normalized observation-model mapping

Source: (Almeida 2017, [doi:10.1016/j.coastaleng.2016.11.009](https://doi.org/10.1016/j.coastaleng.2016.11.009))

### SIS storm longshore-transport measurement framework

$$
y(t,\mathbf{x})=\mathcal{M}[\mathbf{o}(t),\mathbf{b},\mathbf{p}]
$$

Regime: At least nine cross-shore positions over five storms; Hm0 up to 3.5 m; SIS operable above Hs=3 m, wind 20 m/s, and currents 2 m/s.

Variables: `y` predicted or derived coastal response; `o` event observations; `b` bathymetry or beach state; `p` model or instrument parameters; normalized observation-model mapping

Source: (Miller 1999, [doi:10.1016/s0378-3839(99)00010-1](https://doi.org/10.1016/s0378-3839(99)00010-1))

## Claims

- **C258.** For 2011 Great East Japan tsunami evidence along about 340 km, modeling identified the vegetated dune as the primary mitigation at Misawa and showed that straight versus crooked access roads changed velocity; at Hachinohe, seawall diversion kept vegetation moments below 0.2 kNm behind the wall but produced 2-4 kNm in exposed areas, while Sendai video implied 6.2 m/s flow 1 km inland and Fr about 1.14-1.4. *Regime: Twenty-five locations over about 340 km; detailed Misawa vegetated-dune and Hachinohe seawall/forest cases; Sendai video evidence..* [direct_finding, mixed] (Nandasena 2012, [doi:10.1016/j.coastaleng.2012.03.009](https://doi.org/10.1016/j.coastaleng.2012.03.009))
- **C260.** Across five Duck storm transects with waves up to Hm0=3.5 m, directly integrated suspended-load longshore transport reached 1780 m3/h and usually peaked near breaking at the bar and beach; CERC estimates were sometimes high and sometimes low, indicating missing short-term storm controls. *Regime: At least nine cross-shore positions over five storms; Hm0 up to 3.5 m; SIS operable above Hs=3 m, wind 20 m/s, and currents 2 m/s..* [direct_finding, field] (Miller 1999, [doi:10.1016/s0378-3839(99)00010-1](https://doi.org/10.1016/s0378-3839(99)00010-1))
- **C261.** For 2011 Tohoku records from ocean-bottom pressure, GPS buoy, wave, and tide gauges, a regularized nonlinear extreme-learning-machine forecast outperformed standard linear waveform inversion without materially increasing computing time, and consecutive random-weight runs showed insignificant variability. *Regime: 2011 Tohoku waveforms from four OBP gauges plus GPS buoys, wave gauges and tide gauges; example inversion window 35 min..* [direct_finding, numerical] (Mulia 2016, [doi:10.1016/j.coastaleng.2015.11.010](https://doi.org/10.1016/j.coastaleng.2015.11.010))
- **C262.** During the 1 February 2014 Loe Bar storm (Hs=4 m, Hmax=8 m, Tp=10-15 s), 2 Hz laser observations validated XBeach-G overwash hydrodynamics to less than 5% error; simulations showed that long-period or strongly bimodal spectra reduce overtopping and overwash thresholds by enhancing runup. *Regime: Loe Bar D50=2-4 mm; offshore Hs=4 m, Hmax=8 m, Tp=10-15 s, spring high tide 2.45 m and surge about 0.15 m..* [direct_finding, mixed] (Almeida 2017, [doi:10.1016/j.coastaleng.2016.11.009](https://doi.org/10.1016/j.coastaleng.2016.11.009))
- **C263.** During two Lake Michigan storms sampled every approximately 3 h for 24 and 28 h, incident angles near 30 degrees and Hrms breaker heights no greater than 1.5 m produced time-averaged longshore currents up to 1.8 m/s that were often nearly uniform across the surf zone despite barred bathymetry. *Regime: Profiles every about 3 h for 24 and 28 h; incident angle about 30 degrees; Hrms breaker height <=1.5 m; bar about 30 m offshore and 0.75 m deep in calm conditions..* [direct_finding, field] (Allender 1981, [doi:10.1016/0378-3839(81)90020-x](https://doi.org/10.1016/0378-3839(81)90020-x))
- **C382.** Force-balanced dynamically scaled tank experiments showed that storm waves can form the characteristic features of imbricated coastal boulder deposits, so even megagravel deposits cannot be treated as de facto tsunami indicators. *Regime: Dynamically scaled storm-wave interaction with imbricated coastal boulders..* [direct_finding, experimental] (Rónadh Cox 2019, [doi:10.1038/s41598-019-47254-w](https://doi.org/10.1038/s41598-019-47254-w))
- **C1373.** During 6–8 m Atlantic storms, cliff-top vertical ground motion exceeded 50–100 μm and two-week cliff loss was two orders of magnitude above the long-term rate, showing strongly episodic erosion. *Regime: Coastal cliff ground motions and response to extreme storm waves.* [direct_finding, field] (Claire Earlie 2015, [doi:10.1002/2014gl062534](https://doi.org/10.1002/2014gl062534))

## Papers

- Nandasena (2012). Modeling field observations of the 2011 Great East Japan tsunami: Efficacy of artificial and natural structures on tsunami mitigation. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2012.03.009](https://doi.org/10.1016/j.coastaleng.2012.03.009)
- Miller (1999). Field measurements of longshore sediment transport during storms. *Coastal Engineering*. [doi:10.1016/s0378-3839(99)00010-1](https://doi.org/10.1016/s0378-3839(99)00010-1)
- Claire Earlie (2015). Coastal cliff ground motions and response to extreme storm waves. *Geophysical Research Letters*. [doi:10.1002/2014gl062534](https://doi.org/10.1002/2014gl062534) [submitted manuscript, read only](http://hdl.handle.net/10026.1/3226)
- Rónadh Cox (2019). Imbricated Coastal Boulder Deposits are Formed by Storm Waves, and Can Preserve a Long-Term Storminess Record. *Scientific Reports*. [doi:10.1038/s41598-019-47254-w](https://doi.org/10.1038/s41598-019-47254-w) [published version, CC BY](https://www.nature.com/articles/s41598-019-47254-w.pdf)
- Mulia (2016). Real-time forecasting of near-field tsunami waveforms at coastal areas using a regularized extreme learning machine. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2015.11.010](https://doi.org/10.1016/j.coastaleng.2015.11.010)
- Almeida (2017). Storm overwash of a gravel barrier: Field measurements and XBeach-G modelling. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2016.11.009](https://doi.org/10.1016/j.coastaleng.2016.11.009) [accepted manuscript, read only](https://researchportal.plymouth.ac.uk/files/39160668/alm_al_CE_2016_OpenAccess.pdf)
- Allender (1981). Field measurements of longshore currents on a barred beach. *Coastal Engineering*. [doi:10.1016/0378-3839(81)90020-x](https://doi.org/10.1016/0378-3839(81)90020-x)
- Hendrik J. Bruins (2007). Geoarchaeological tsunami deposits at Palaikastro (Crete) and the Late Minoan IA eruption of Santorini. *Journal of Archaeological Science*. [doi:10.1016/j.jas.2007.08.017](https://doi.org/10.1016/j.jas.2007.08.017) [accepted manuscript, read only](https://pure.rug.nl/ws/files/6712369/2008JArchaeolSciBruins.pdf)
- Elko (2007). Immediate profile and planform evolution of a beach nourishment project with hurricane influences. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2006.08.001](https://doi.org/10.1016/j.coastaleng.2006.08.001)
- Drost (2019). Predicting the hydrodynamic response of a coastal reef-lagoon system to a tropical cyclone using phase-averaged and surfbeat-resolving wave models. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2019.103525](https://doi.org/10.1016/j.coastaleng.2019.103525) [published version, read only](https://api.elsevier.com/content/article/PII:S0378383918301352?httpAccept=text/xml)
