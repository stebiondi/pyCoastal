# Wave and current observations

`field.waves` | Fixed and mobile hydrodynamic sensors.

Parent: [Field measurements](field.md)

Papers: 21. Claims: 2. Equations: 0.

## Synthesis

**Well established.** Field wave observations require complementary in situ and remote sensors because no platform simultaneously resolves nearshore transformation, directional spectra, extremes and broad spatial coverage; uncertainty grows near land, shallow water, breaking and vegetation or structures.

**Governing physics.** Wind-sea and swell propagate, refract, shoal, break, reflect and interact with currents, bottom stress, vegetation and structures; resulting spectra, setup, runup and attenuation depend on bathymetry, water level, directional partitions and local morphology.

**Dimensionless parameters.** Controls include relative depth, wave steepness, surf-similarity, directional spread, transmission coefficient, vegetation or reef submergence, fetch, current-to-wave celerity ratio, sensor separation relative to wavelength and error normalized by wave height.

**Major equations.** Wave observations are summarized by spectral moments, significant height, periods and directions; energy-flux and radiation-stress balances connect transformation to setup, while transmission ratios compare incident and lee energy. Validation uses bias, RMSE, correlation, scatter and distributional or spectral scores.

**Typical methods.** Campaigns collocate buoys, pressure sensors, ADCPs, wave staffs, HF radar, altimetry and shoreline measurements; synchronize clocks and datums, apply response and depth corrections, partition spectra, quality-control breaking and land contamination, quantify sampling uncertainty and validate derived quantities across sea states.

**Numerical models.** Field evidence evaluates empirical setup/runup parameterizations, roller and bottom-stress setup models, porous-transmission theory, vegetation-aware MIKE SW, harbor spectral reconstruction and remote-sensing retrieval algorithms. Models remain conditional on sensor and site coverage.

**Experimental datasets.** Reviewed evidence spans ten natural-beach setup/runup campaigns, 90 days of SandyDuck setup, living-shoreline and oyster sites, tropical-storm marsh records, a seasonal saltmarsh dataset, 40 years of harbor spectra, Iberian HF-radar/buoy/altimetry comparisons and northeastern US multi-mission altimetry.

**Validated ranges.** Iberian Sentinel-3 comparisons achieved correlations above 0.94, bias below 0.19 m and RMSE 0.17-0.42 m; SandyDuck setup agreed within about 30% to 6 m depth; other results cover their stated beaches, structures, vegetation and harbor regimes only.

**Recent advances.** Recent advances combine new coastal altimeters and SAR, compact directional buoys, distributed acoustic sensing, video and radar, autonomous vehicles, cloud-based spectral partitioning and assimilation of heterogeneous observations into operational wave models.

**Disagreements.** Buoys provide reliable point spectra but sparse spatial sampling; altimeters broaden coverage yet degrade nearshore and may miss extrema; HF radar maps coastal fields but requires local validation. Aggregated height and period can conceal materially different multimodal spectra.

**Limitations.** Mooring motion, pressure attenuation, sidelobes, currents, breaking, biofouling, gaps, clock or datum error, land contamination, satellite revisit, short campaigns and changing bathymetry create bias. Extreme-event sampling and directional validation are especially sparse.

**Open questions.** Priorities include seamless multisensor fusion, coastal altimetry and SAR calibration, directional and infragravity retrieval, uncertainty-aware extremes, affordable dense arrays, autonomous quality control, changing-bathymetry correction and standardized open benchmark campaigns.

**Seminal papers.** Pressure and buoy spectra established field wave statistics; array methods enabled direction, radiation-stress studies tied waves to setup, and satellite altimetry plus HF radar extended spatial coverage. Long-term coastal observatories connected these methods.

## Claims

- **C142.** Against Iberian buoys, Sentinel-3 significant-wave-height observations achieved correlations above 0.94, biases below 0.19 m, and RMSE of 0.17-0.42 m, enabling spatial validation of HF-radar wave retrievals. *Regime: West Iberian Sentinel-3/buoy collocations from 2017-2019; nearshore sampling and sea-state limits apply..* [direct_finding, field] (Bué 2020, [doi:10.3390/rs12213623](https://doi.org/10.3390/rs12213623))
- **C1365.** Spotter real-time buoy bulk wave statistics were within 10% of a Datawell reference across stand and field tests, enabling multi-buoy measurements of decorrelation, speed and directional spread. *Regime: Performance Characteristics of “Spotter,” a Newly Developed Real-Time Wave Measurement Buoy.* [direct_finding, mixed] (Kaustubha Raghukumar 2019, [doi:10.1175/jtech-d-18-0151.1](https://doi.org/10.1175/jtech-d-18-0151.1))

## Papers

- Kaustubha Raghukumar (2019). Performance Characteristics of “Spotter,” a Newly Developed Real-Time Wave Measurement Buoy. *Journal of Atmospheric and Oceanic Technology*. [doi:10.1175/jtech-d-18-0151.1](https://doi.org/10.1175/jtech-d-18-0151.1)
- Stockdon (2006). Empirical parameterization of setup, swash, and runup. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2005.12.005](https://doi.org/10.1016/j.coastaleng.2005.12.005)
- Aron Roland (2014). On the developments of spectral wave models: numerics and parameterizations for the coastal ocean. *Ocean Dynamics*. [doi:10.1007/s10236-014-0711-z](https://doi.org/10.1007/s10236-014-0711-z)
- Apotsos (2007). Effects of wave rollers and bottom stress on wave setup. *Journal of Geophysical Research: Oceans*. [doi:10.1029/2006jc003549](https://doi.org/10.1029/2006jc003549)
- Anon. (2012). Remote Sensing of Coastal and Ocean Currents: An Overview. *Journal of Coastal Research*. [doi:10.2112/jcoastres-d-11-00197.1](https://doi.org/10.2112/jcoastres-d-11-00197.1)
- Xuan Zhang (2021). A review of the state of research on wave-current interaction in nearshore areas. *Ocean Engineering*. [doi:10.1016/j.oceaneng.2021.110202](https://doi.org/10.1016/j.oceaneng.2021.110202)
- Brian Greenwood (1990). Vertical and horizontal structure in cross-shore flows: An example of undertow and wave set-up on a barred beach. *Coastal Engineering*. [doi:10.1016/0378-3839(90)90034-t](https://doi.org/10.1016/0378-3839(90)90034-t)
- Safak (2020). Coupling breakwalls with oyster restoration structures enhances living shoreline performance along energetic shorelines. *Ecological Engineering*. [doi:10.1016/j.ecoleng.2020.106071](https://doi.org/10.1016/j.ecoleng.2020.106071)
- Xiaolong Yu (2017). Effects of wave-current interaction on storm surge in the Taiwan Strait: Insights from Typhoon Morakot. *Continental Shelf Research*. [doi:10.1016/j.csr.2017.08.009](https://doi.org/10.1016/j.csr.2017.08.009)
- Jadhav (2013). Probability distribution of wave heights attenuated by salt marsh vegetation during tropical cyclone. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2013.08.006](https://doi.org/10.1016/j.coastaleng.2013.08.006)
- Postacchini (2015). Scour depth under pipelines placed on weakly cohesive soils. *Applied Ocean Research*. [doi:10.1016/j.apor.2015.04.010](https://doi.org/10.1016/j.apor.2015.04.010)
- Safak (2020). Wave transmission through living shoreline breakwalls. *Continental Shelf Research*. [doi:10.1016/j.csr.2020.104268](https://doi.org/10.1016/j.csr.2020.104268)
- Romano-Moreno (2023). Multimodal harbor wave climate characterization based on wave agitation spectral types. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2022.104271](https://doi.org/10.1016/j.coastaleng.2022.104271)
- Bué (2020). Evaluation of HF Radar Wave Measurements in Iberian Peninsula by Comparison with Satellite Altimetry and in Situ Wave Buoy Observations. *Remote Sensing*. [doi:10.3390/rs12213623](https://doi.org/10.3390/rs12213623)
- Mitsopoulos (2023). Characterizing Coastal Wind Speed and Significant Wave Height Using Satellite Altimetry and Buoy Data. *Remote Sensing*. [doi:10.3390/rs15040987](https://doi.org/10.3390/rs15040987)
- YAMAGUCHI (1985). NUMERICAL MODELS FOR WAVE TRANSFORMATION DUE TO CURRENT-DEPTH REFRACTION. *Doboku Gakkai Ronbunshu*. [doi:10.2208/jscej.1985.357_187](https://doi.org/10.2208/jscej.1985.357_187)
- Abeshima (2005). Mooring Limit of Small Fishing Boat at Kumaishi Fishing Port. *The Journal of Japan Institute of Navigation*. [doi:10.9749/jin.112.345](https://doi.org/10.9749/jin.112.345)
- Jacobsen (2026). Wave attenuation through a saltmarsh: Heterogeneous vegetation characteristics and seasonal variability. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2026.105099](https://doi.org/10.1016/j.coastaleng.2026.105099)
- Bieri (2026). Designing restored oyster reefs to enhance coastal protection benefits. *Estuarine, Coastal and Shelf Science*. [doi:10.1016/j.ecss.2026.110156](https://doi.org/10.1016/j.ecss.2026.110156)
- OKI (2008). Development of Multidirectional Random Wave Transformation Model in Wave-Current Coexisting Field. *PROCEEDINGS OF COASTAL ENGINEERING, JSCE*. [doi:10.2208/proce1989.55.1](https://doi.org/10.2208/proce1989.55.1)
- Lee (2005). Analysis of Numerical Model Wave Predictions for Coastal Waters at Gunsan-Janghang Harbor Entrance. *Journal of Navigation and Port Research*. [doi:10.5394/kinpr.2005.29.7.627](https://doi.org/10.5394/kinpr.2005.29.7.627)
