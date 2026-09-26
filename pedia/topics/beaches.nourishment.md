# Beach nourishment

`beaches.nourishment` | Placement, spreading, and performance.

Parent: [Beaches and shoreline evolution](beaches.md)

Papers: 10. Claims: 8. Equations: 2.

Used by pyCoastal design modules: Beach nourishment.

## Synthesis

**Well established.** Nourishment creates a deliberately nonequilibrium sediment body that begins adjusting cross-shore and alongshore immediately; persistence, protection, and adverse effects depend on grain size, constructed geometry, waves, shoreface and inlet connectivity, structures, and the boundaries used for accounting.

**Governing physics.** Constructed shoreline gradients drive alongshore diffusion even in calm conditions, wave-energy disequilibrium drives cross-shore profile response, storms accelerate redistribution, and steep shorefaces, canyons, inlets, and groins create sinks or transfers that a local control volume may register as loss.

**Dimensionless parameters.** Transferable controls include relative grain size, relative fill width and length, profile-scale and equilibrium-shape parameters, wave-energy disequilibrium, relative notch position within the active swash zone, and normalized crest rise under sea-level change.

**Major equations.** Common reduced descriptions include the Dean equilibrium profile h=A x^(2/3), dynamic shoreline relaxation proportional to wave-energy disequilibrium, one-line shoreline diffusion, empirical linear or exponential volume-loss curves, and sediment control-volume balances.

**Typical methods.** Robust evaluations combine repeated topographic and bathymetric profiles, shoreline or daily video observations, wave records, UAS-SfM elevation differencing, placed-volume histories, open-boundary sediment budgets, and calibration-validation that checks parameter physics as well as fit.

**Numerical models.** One-parameter dynamic-equilibrium models can match more parameterized shoreline models at a calibrated site, while one-line volume models can retain more credible parameters than statistically adequate empirical decay curves; neither result removes the need to represent inlets, structures, or open sediment boundaries where relevant.

**Experimental datasets.** The screened evidence spans four southern California fills monitored for 4-16 years, an 1100 m Florida fill through its first calm and hurricane periods, thirty years at Nice, two years of daily video in Barcelona, nine UAS surveys at Deal, and volume histories at two South Carolina barrier beaches.

**Validated ranges.** Directly tested ranges include 500-1500 m by about 50 m southern California pads integrated to 8 m depth, an 1100 m Florida project with 45 calm days before strong storms, 558,000 m3 placed along 4.5 km at Nice, two years of daily video at Nova Icaria, nine surveys of eight groins including three notches, and 1-5 m sea-level-rise scenarios at four gravel defenses.

**Recent advances.** Recent advances use parsimonious dynamic-equilibrium prediction, multi-year regional sediment accounting, UAS-SfM diagnosis of nourishment-structure interaction, and scenario-based crest and volume design under sea-level rise.

**Disagreements.** Multi-year subaerial persistence in southern California and no net width gain after decades at Nice are conditional outcomes, not a universal contradiction: sediment size, shoreface steepness, canyon proximity, wave exposure, monitoring metric, and boundary flux differ. Likewise, statistical model fit does not establish physically credible lifecycle prediction.

**Limitations.** Evidence remains site-limited, monitoring often misses subaqueous or cross-boundary flux, storms confound early equilibration, ecological and groundwater impacts are sparse, and reduced models omit inlet, barrier, and structure interactions. Success metrics based only on dry-beach width can therefore be misleading.

**Open questions.** Priorities are prospective multi-site validation, full littoral-cell sediment budgets, predictive grain-size and profile design, coupled inlet and structure effects, ecological and groundwater thresholds, adaptive monitoring triggers, and lifecycle optimization under uncertain storms and sea-level rise.

**Seminal papers.** Within this screened branch, the 2006 Upham field study establishes simultaneous immediate planform and profile adjustment, while the 2011 Nice record provides a rare multi-decadal test of nourishment efficiency.

## Equations

### Dean equilibrium beach profile

$$
h=A x^{2/3}
$$

Regime: Idealized profile equilibration of the monitored fill.

Variables: `h` water depth; `A` sediment-dependent profile scale; `x` offshore distance

Source: (Elko 2007, [doi:10.1016/j.coastaleng.2006.08.001](https://doi.org/10.1016/j.coastaleng.2006.08.001))

### Dynamic-equilibrium shoreline response

$$
\frac{dy}{dt}=k(E_{eq}-E)
$$

Regime: Medium-to-long-term cross-shore shoreline response at Nova Icaria beach.

Variables: `y` shoreline position; `k` calibrated response-rate parameter; `E_eq` equilibrium wave energy; `E` incident wave energy

Source: (Jara 2015, [doi:10.1016/j.coastaleng.2015.02.006](https://doi.org/10.1016/j.coastaleng.2015.02.006))

## Claims

- **C190.** At four southern California nourishments, coarse subaerial pads persisted for years but redistributed across open control-volume boundaries; Torrey Pines lost about 300,000 m3 over 16 years, and Imperial Beach drift contributed to the 2016 Tijuana River mouth closure. *Regime: The four surveyed southern California fills; natural variability and open boundaries limit attribution..* [direct_finding, field] (Bonnie C. Ludka 2018, [doi:10.1016/j.coastaleng.2018.02.003](https://doi.org/10.1016/j.coastaleng.2018.02.003))
- **C191.** At the 1100 m Upham Beach project, planform adjustment began during calm conditions immediately after construction, and a subsequent strong storm caused a substantial portion of total profile equilibration, demonstrating simultaneous longshore and cross-shore adjustment. *Regime: Low-energy west Florida nourishment with strong constructed-width gradients and hurricane-influenced early months..* [direct_finding, field] (Elko 2007, [doi:10.1016/j.coastaleng.2006.08.001](https://doi.org/10.1016/j.coastaleng.2006.08.001))
- **C193.** At Nice's 4.5 km gravel beach, 558,000 m3 placed from 1976-2005 produced no significant net width increase across 50 transects and 87 surveys, implying chronic offshore loss promoted by the steep shoreface and seasonal profile flattening. *Regime: Steep reflective, almost tideless gravel beach beside narrow shoreface and canyon heads; offshore pathways were inferred..* [direct_finding, field] (Anthony 2011, [doi:10.1016/j.coastaleng.2010.11.001](https://doi.org/10.1016/j.coastaleng.2010.11.001))
- **C194.** At Deal, New Jersey, three identically notched groins stabilized adjacent shoreline but only the notch remaining near the seaward swash-zone edge promoted bidirectional bypassing; notches buried by post-nourishment widening behaved like traditional groins. *Regime: The monitored eight-groin field under northward net transport and evolving 2016 nourishment morphology..* [direct_finding, field] (Zimmerman 2021, [doi:10.1016/j.coastaleng.2021.103997](https://doi.org/10.1016/j.coastaleng.2021.103997))
- **C195.** At Folly Beach and Hunting Island, four nourishment-loss models all fit observed volumes statistically, but only the wave-linked One-Line model retained physically credible parameters at both sites; inlet and barrier-island processes remained unresolved. *Regime: Two South Carolina barrier-beach projects with measured volume time series and wave information..* [direct_finding, numerical] (Weathers 2013, [doi:10.2112/si_69_7](https://doi.org/10.2112/si_69_7))
- **C1432.** Nineteen Dutch shoreface nourishments supplied sediment landward for years, while energetic breaking waves and cross-shore transport dominated initial nourishment erosion. *Regime: Observations and Modelling of Shoreface Nourishment Behaviour.* [direct_finding, mixed] (B.J.A. Huisman 2019, [doi:10.3390/jmse7030059](https://doi.org/10.3390/jmse7030059))
- **C1433.** Fine sediment in a beach nourishment briefly elevated local surf-zone fecal indicator bacteria, followed by rapid inactivation and wave-current dispersal. *Regime: Beach Nourishment Impacts on Bacteriological Water Quality and Phytoplankton Bloom Dynamics.* [direct_finding, field] (Megan A. Rippy 2013, [doi:10.1021/es400572k](https://doi.org/10.1021/es400572k))
- **C1658.** Monitoring of the 2014 Dunkirk nourishment shows rapid initial adjustment and predominantly eastward wave-driven redistribution rather than simple loss, benefiting the downdrift recreational beach while erosion weakened during the second year. *Regime: Dredged-sand nourishment fronting the Digue des Allies at Dunkirk on a tide-dominated northern French coast..* [direct_finding, field] (Alexandra Spodar 2017, [doi:10.1007/s11852-017-0514-8](https://doi.org/10.1007/s11852-017-0514-8))

## Papers

- Bonnie C. Ludka (2018). Nourishment evolution and impacts at four southern California beaches: A sand volume analysis. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2018.02.003](https://doi.org/10.1016/j.coastaleng.2018.02.003) [published version, CC BY-NC-ND](https://api.elsevier.com/content/article/PII:S0378383917303150?httpAccept=text/xml)
- Elko (2007). Immediate profile and planform evolution of a beach nourishment project with hurricane influences. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2006.08.001](https://doi.org/10.1016/j.coastaleng.2006.08.001)
- B.J.A. Huisman (2019). Observations and Modelling of Shoreface Nourishment Behaviour. *Journal of Marine Science and Engineering*. [doi:10.3390/jmse7030059](https://doi.org/10.3390/jmse7030059) [published version, CC BY](https://www.mdpi.com/2077-1312/7/3/59/pdf?version=1551870015)
- Anthony (2011). Chronic offshore loss of nourishment on Nice beach, French Riviera: A case of over-nourishment of a steep beach?. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2010.11.001](https://doi.org/10.1016/j.coastaleng.2010.11.001)
- Alexandra Spodar (2017). Evolution of a beach nourishment project using dredged sand from navigation channel, Dunkirk, northern France. *Journal of Coastal Conservation*. [doi:10.1007/s11852-017-0514-8](https://doi.org/10.1007/s11852-017-0514-8) [submitted manuscript, read only](https://hal.science/hal-04252313/document)
- Megan A. Rippy (2013). Beach Nourishment Impacts on Bacteriological Water Quality and Phytoplankton Bloom Dynamics. *Environmental Science & Technology*. [doi:10.1021/es400572k](https://doi.org/10.1021/es400572k) [submitted manuscript, read only](https://escholarship.org/content/qt8zz952q8/qt8zz952q8.pdf?t=q146ks)
- Dornbusch (2017). Design requirement for mixed sand and gravel beach defences under scenarios of sea level rise. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2017.03.006](https://doi.org/10.1016/j.coastaleng.2017.03.006)
- Zimmerman (2021). UAS-SfM approach to evaluate the performance of notched groins within a groin field and their impact on the morphological evolution of a beach nourishment. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2021.103997](https://doi.org/10.1016/j.coastaleng.2021.103997)
- Weathers (2013). Evaluation of Beach Nourishment Evolution Models Using Data from Two South Carolina, USA Beaches: Folly Beach and Hunting Island. *Journal of Coastal Research*. [doi:10.2112/si_69_7](https://doi.org/10.2112/si_69_7)
- Jara (2015). Shoreline evolution model from a dynamic equilibrium beach profile. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2015.02.006](https://doi.org/10.1016/j.coastaleng.2015.02.006)
