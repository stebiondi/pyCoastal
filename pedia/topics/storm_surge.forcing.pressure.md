# Atmospheric pressure forcing

`storm_surge.forcing.pressure` | Inverse barometer and pressure gradients.

Parent: [Storm surge and coastal flooding](storm_surge.md) > [Surge forcing](storm_surge.forcing.md)

Papers: 11. Claims: 12. Equations: 0.

Used by pyCoastal design modules: Storm surge and flooding.

## Synthesis

**Well established.** Atmospheric pressure forces coastal water levels through quasi-static inverse-barometer adjustment and dynamic gradients; moving disturbances can resonantly generate long waves that amplify on shelves and in bays and harbours.

**Governing physics.** A pressure deficit raises the equilibrium sea surface, while horizontal pressure gradients accelerate water. When disturbance translation approaches shallow-water wave speed, Proudman resonance accumulates energy; shelf, bay and harbour modes then amplify or reshape the wave.

**Dimensionless parameters.** Key controls are pressure anomaly, disturbance length and translation speed, water depth, Froude number based on atmospheric and shallow-water wave speeds, shelf width, incidence angle, and shelf, bay or harbour modal periods.

**Major equations.** Pressure enters shallow-water momentum as a surface-pressure gradient. The inverse-barometer approximation relates sea-level rise inversely to pressure anomaly, while moving-forcing solutions and nonlinear shallow-water models represent resonant generation, propagation and inundation.

**Typical methods.** Studies combine high-frequency barometers, tide gauges and current measurements with spectral or wavelet analysis, analytical moving-pressure solutions, pressure-only and wind-only sensitivity experiments, and nested shallow-water or regional ocean models.

**Numerical models.** Numerical approaches range from idealized analytical and nonlinear shallow-water models to NAMI DANCE SUITE, regional three-dimensional ocean models and coupled atmosphere–wave–surge systems driven by parametric or full-physics pressure fields.

**Experimental datasets.** Evidence includes the east Adriatic 2003 event, Hurricane Harvey rainbands, Venice 2019 flooding, Typhoon Songda and Pacific Northwest cyclones, Persian Gulf gauges, the Gulf of Genoa record and regional Strait of Georgia and Brazilian-bay simulations.

**Validated ranges.** Reported responses span pressure perturbations of roughly 1–3 mbar producing about 0.2 m waves, a 0.5 m Genoa event, Persian Gulf residuals up to 0.75 m, Pacific Northwest surges above 0.8 m and resonantly amplified Adriatic oscillations above 1 m.

**Recent advances.** Recent studies use high-resolution colocated pressure–sea-level observations and forcing-partition experiments to identify tropical-cyclone rainband meteotsunamis, mesoscale-cyclone contributions to extreme floods and operational model sensitivity to pressure-field structure.

**Disagreements.** Wind often dominates synoptic storm surge, but pressure is not always negligible: sharp rainband or mesoscale pressure disturbances can generate resonant waves comparable to other coastal water-level components. Attribution therefore depends on time scale and geometry.

**Limitations.** Pressure and wind covary in storms, barometer and tide-gauge spacing may miss propagating fronts, atmospheric products smooth mesoscale jumps, and resonance makes results highly site- and direction-dependent.

**Open questions.** Operational thresholds for pressure-jump speed, angle and scale remain uncertain, as do pressure–wind interaction, compound tide/surge timing, nonlinear breaking and inundation, and transfer of resonance diagnostics among coastlines.

**Seminal papers.** Foundational work established inverse-barometer forcing and traveling-pressure resonance; Adriatic observations and the global meteotsunami synthesis connected Proudman resonance with shelf, bay and harbour amplification.

## Claims

- **C873.** Atmospheric gravity waves, pressure jumps, fronts and squalls generate barotropic long waves that amplify through Proudman, shelf, bay and harbour resonance; generation peaks near Froude number one. *Regime: Meteotsunamis: atmospherically induced destructive ocean waves in the tsunami frequency band.* [literature_review_statement, review] (Sebastià Monserrat 2006, [doi:10.5194/nhess-6-1035-2006](https://doi.org/10.5194/nhess-6-1035-2006))
- **C874.** A 22 m s-1 atmospheric gravity disturbance resonantly coupled to water about 50 m deep, producing sea-level oscillations above 1 m that were further amplified in funnel-shaped Adriatic bays. *Regime: Resonant coupling of a traveling air pressure disturbance with the east Adriatic coastal waters.* [direct_finding, mixed] (Ivica Vilibić 2004, [doi:10.1029/2004jc002279](https://doi.org/10.1029/2004jc002279))
- **C875.** A validated regional Strait of Georgia model assesses the atmospheric forcing factors that contribute to winter storm surges in a semi-enclosed coastal sea. *Regime: Storm Surges in the Strait of Georgia Simulated with a Regional Model.* [direct_finding, numerical] (Nancy Soontiens 2015, [doi:10.1080/07055900.2015.1108899](https://doi.org/10.1080/07055900.2015.1108899))
- **C876.** Hurricane Isaac surge predictions differ when parametric versus full-physics atmospheric wind and pressure fields force the same coupled wave–surge system. *Regime: Sensitivity of Storm Surge Predictions to Atmospheric Forcing during Hurricane Isaac.* [direct_finding, numerical] (J. C. Dietrich 2018, [doi:10.1061/(asce)ww.1943-5460.0000419](https://doi.org/10.1061/(asce)ww.1943-5460.0000419))
- **C877.** A nonlinear shallow-water model with atmospheric pressure and wind forcing reproduces analytical long-wave generation and coastal amplification by propagating pressure disturbances. *Regime: Long wave generation and coastal amplification due to propagating atmospheric pressure disturbances.* [direct_finding, numerical] (Gözde Güney Doğan 2021, [doi:10.1007/s11069-021-04625-9](https://doi.org/10.1007/s11069-021-04625-9))
- **C878.** Observed 1–3 mbar rainband pressure perturbations during Hurricane Harvey generated approximately 20-minute meteotsunamis with amplitudes around 0.2 m, showing pressure need not be negligible relative to wind. *Regime: Meteotsunamis Accompanying Tropical Cyclone Rainbands During Hurricane Harvey.* [direct_finding, mixed] (Katherine Anarde 2020, [doi:10.1029/2020jc016347](https://doi.org/10.1029/2020jc016347))
- **C879.** Persian Gulf non-tidal sea-level fluctuations up to 0.75 m reflect combined low pressure and cross-shore wind; pressure leads sea level over 1–6.4-day bands, while wind stress has the larger effect. *Regime: Relationship between the Persian Gulf Sea-Level Fluctuations and Meteorological Forcing.* [direct_finding, field] (Naghmeh Afshar-Kaveh 2020, [doi:10.3390/jmse8040285](https://doi.org/10.3390/jmse8040285))
- **C880.** A fast mesoscale cyclone produced atmosphere–ocean resonance and a meteotsunami-like wave that contributed significantly to Venice’s 1.89 m extreme water level; simulations partitioned wind and pressure contributions. *Regime: The contribution of a mesoscale cyclone and associated meteotsunami to the exceptional flood in Venice on November 12, 2019.* [direct_finding, mixed] (Christian Ferrarin 2023, [doi:10.1002/qj.4539](https://doi.org/10.1002/qj.4539))
- **C881.** Successive low-pressure systems including Typhoon Songda generated storm surges above 0.8 m and associated seiches and infragravity waves along British Columbia and Washington. *Regime: Strength in Numbers: The Tail End of Typhoon Songda Combines with Local Cyclones to Generate Extreme Sea Level Oscillations on the British Columbia and Washington Coasts during Mid-October 2016.* [direct_finding, field] (Alexander B. Rabinovich 2022, [doi:10.1175/jpo-d-22-0096.1](https://doi.org/10.1175/jpo-d-22-0096.1))
- **C882.** Nested coastal modelling identifies remotely forced meteorological signal propagation and lag as controls on water-level differences and strong currents between linked Brazilian bays. *Regime: Meteorological Signal on Hydrodynamics in the Ilha Grande and Sepetiba Bays: Lag Effects and Coastal Currents.* [direct_finding, numerical] (Nair Emmanuela da Silveira Pereira 2024, [doi:10.3390/hydrology11020015](https://doi.org/10.3390/hydrology11020015))
- **C883.** An abrupt atmospheric-pressure jump generated a Gulf of Genoa meteotsunami with maximum wave height of 0.5 m lasting about three hours. *Regime: Detection and Characterization of Meteotsunamis in the Gulf of Genoa.* [direct_finding, field] (Paola Picco 2019, [doi:10.3390/jmse7080275](https://doi.org/10.3390/jmse7080275))
- **C1773.** For Hurricane Isaac, atmospheric-forcing choice and forecast-track timing materially controlled SWAN+ADCIRC surge skill: UWIN-CM supplied improved forecast skill at least 24 hours before the official advisories, and shifting its storm timing by 6 hours reduced water-level RMS errors to 0.20-0.26 m, below the best-track parametric simulation. *Regime: Hurricane Isaac (2012) over the northern Gulf of Mexico and the marshes and floodplains of southeastern Louisiana, Mississippi, and Alabama, evaluated with observation-based, parametric, and full-physics atmospheric forcing coupled to high-resolution waves and surge..* [direct_finding, numerical] (J. C. Dietrich 2018, [doi:10.1061/(asce)ww.1943-5460.0000419](https://doi.org/10.1061/(asce)ww.1943-5460.0000419))

## Papers

- Sebastià Monserrat (2006). Meteotsunamis: atmospherically induced destructive ocean waves in the tsunami frequency band. *Natural hazards and earth system sciences*. [doi:10.5194/nhess-6-1035-2006](https://doi.org/10.5194/nhess-6-1035-2006)
- Nancy Soontiens (2015). Storm Surges in the Strait of Georgia Simulated with a Regional Model. *ATMOSPHERE-OCEAN*. [doi:10.1080/07055900.2015.1108899](https://doi.org/10.1080/07055900.2015.1108899)
- Ivica Vilibić (2004). Resonant coupling of a traveling air pressure disturbance with the east Adriatic coastal waters. *Journal of Geophysical Research: Oceans*. [doi:10.1029/2004jc002279](https://doi.org/10.1029/2004jc002279)
- J. C. Dietrich (2018). Sensitivity of Storm Surge Predictions to Atmospheric Forcing during Hurricane Isaac. *Journal of Waterway, Port, Coastal, and Ocean Engineering*. [doi:10.1061/(asce)ww.1943-5460.0000419](https://doi.org/10.1061/(asce)ww.1943-5460.0000419)
- Gözde Güney Doğan (2021). Long wave generation and coastal amplification due to propagating atmospheric pressure disturbances. *Natural Hazards*. [doi:10.1007/s11069-021-04625-9](https://doi.org/10.1007/s11069-021-04625-9)
- Katherine Anarde (2020). Meteotsunamis Accompanying Tropical Cyclone Rainbands During Hurricane Harvey. *Journal of Geophysical Research Oceans*. [doi:10.1029/2020jc016347](https://doi.org/10.1029/2020jc016347)
- Naghmeh Afshar-Kaveh (2020). Relationship between the Persian Gulf Sea-Level Fluctuations and Meteorological Forcing. *Journal of Marine Science and Engineering*. [doi:10.3390/jmse8040285](https://doi.org/10.3390/jmse8040285)
- Christian Ferrarin (2023). The contribution of a mesoscale cyclone and associated meteotsunami to the exceptional flood in Venice on November 12, 2019. *Quarterly Journal of the Royal Meteorological Society*. [doi:10.1002/qj.4539](https://doi.org/10.1002/qj.4539)
- Alexander B. Rabinovich (2022). Strength in Numbers: The Tail End of Typhoon Songda Combines with Local Cyclones to Generate Extreme Sea Level Oscillations on the British Columbia and Washington Coasts during Mid-October 2016. *Journal of Physical Oceanography*. [doi:10.1175/jpo-d-22-0096.1](https://doi.org/10.1175/jpo-d-22-0096.1)
- Nair Emmanuela da Silveira Pereira (2024). Meteorological Signal on Hydrodynamics in the Ilha Grande and Sepetiba Bays: Lag Effects and Coastal Currents. *Hydrology*. [doi:10.3390/hydrology11020015](https://doi.org/10.3390/hydrology11020015)
- Paola Picco (2019). Detection and Characterization of Meteotsunamis in the Gulf of Genoa. *Journal of Marine Science and Engineering*. [doi:10.3390/jmse7080275](https://doi.org/10.3390/jmse7080275)
