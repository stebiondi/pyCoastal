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

- Kaustubha Raghukumar (2019). Performance Characteristics of “Spotter,” a Newly Developed Real-Time Wave Measurement Buoy. *Journal of Atmospheric and Oceanic Technology*. [doi:10.1175/jtech-d-18-0151.1](https://doi.org/10.1175/jtech-d-18-0151.1) [published version, read only](https://journals.ametsoc.org/downloadpdf/journals/atot/36/6/jtech-d-18-0151.1.pdf)
- Stockdon (2006). Empirical parameterization of setup, swash, and runup. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2005.12.005](https://doi.org/10.1016/j.coastaleng.2005.12.005)
- Aron Roland (2014). On the developments of spectral wave models: numerics and parameterizations for the coastal ocean. *Ocean Dynamics*. [doi:10.1007/s10236-014-0711-z](https://doi.org/10.1007/s10236-014-0711-z) [published version, read only](https://link.springer.com/content/pdf/10.1007/s10236-014-0711-z.pdf)
- Apotsos (2007). Effects of wave rollers and bottom stress on wave setup. *Journal of Geophysical Research: Oceans*. [doi:10.1029/2006jc003549](https://doi.org/10.1029/2006jc003549) [accepted manuscript, read only](https://falk.ucsd.edu/pdf/Apotsos2007JGR.pdf)
- Anon. (2012). Remote Sensing of Coastal and Ocean Currents: An Overview. *Journal of Coastal Research*. [doi:10.2112/jcoastres-d-11-00197.1](https://doi.org/10.2112/jcoastres-d-11-00197.1) [published version, read only](https://www.researchgate.net/publication/235324827_Remote_Sensing_of_Coastal_and_Ocean_Currents_An_Overview)
- Xuan Zhang (2021). A review of the state of research on wave-current interaction in nearshore areas. *Ocean Engineering*. [doi:10.1016/j.oceaneng.2021.110202](https://doi.org/10.1016/j.oceaneng.2021.110202) [accepted manuscript, read only](https://discovery.ucl.ac.uk/10141597/1/Manuscript%20%28clean%29%20--%20final%20version.pdf)
- Brian Greenwood (1990). Vertical and horizontal structure in cross-shore flows: An example of undertow and wave set-up on a barred beach. *Coastal Engineering*. [doi:10.1016/0378-3839(90)90034-t](https://doi.org/10.1016/0378-3839(90)90034-t) [published version, read only](https://utoronto.scholaris.ca/bitstreams/b9e51059-fa11-42b4-b0c2-284e6bea5445/download)
- Safak (2020). Coupling breakwalls with oyster restoration structures enhances living shoreline performance along energetic shorelines. *Ecological Engineering*. [doi:10.1016/j.ecoleng.2020.106071](https://doi.org/10.1016/j.ecoleng.2020.106071) [published version, read only](https://static1.squarespace.com/static/5f846d5a4adb627cffa90b1d/t/605264c5adf28e2b134cdacf/1616012497142/Safak%2Bet%2Bal.%2B2020%2B-%2BCouplingBreakwalls.pdf)
- Xiaolong Yu (2017). Effects of wave-current interaction on storm surge in the Taiwan Strait: Insights from Typhoon Morakot. *Continental Shelf Research*. [doi:10.1016/j.csr.2017.08.009](https://doi.org/10.1016/j.csr.2017.08.009) [submitted manuscript, read only](https://ueaeprints.uea.ac.uk/id/eprint/64582/1/Accepted_manuscript.pdf)
- Jadhav (2013). Probability distribution of wave heights attenuated by salt marsh vegetation during tropical cyclone. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2013.08.006](https://doi.org/10.1016/j.coastaleng.2013.08.006)
- Postacchini (2015). Scour depth under pipelines placed on weakly cohesive soils. *Applied Ocean Research*. [doi:10.1016/j.apor.2015.04.010](https://doi.org/10.1016/j.apor.2015.04.010) [accepted manuscript, read only](https://iris.univpm.it/bitstream/11566/227974/6/Postacchini_Brocchini_apor2015%20-%20post-print.pdf)
- Safak (2020). Wave transmission through living shoreline breakwalls. *Continental Shelf Research*. [doi:10.1016/j.csr.2020.104268](https://doi.org/10.1016/j.csr.2020.104268) [accepted manuscript, CC BY](https://repository.library.noaa.gov/view/noaa/34021/noaa_34021_DS1.pdf?download=1)
- Romano-Moreno (2023). Multimodal harbor wave climate characterization based on wave agitation spectral types. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2022.104271](https://doi.org/10.1016/j.coastaleng.2022.104271) [published version, CC BY-NC-ND](https://api.elsevier.com/content/article/PII:S0378383922001843?httpAccept=text/xml)
- Bué (2020). Evaluation of HF Radar Wave Measurements in Iberian Peninsula by Comparison with Satellite Altimetry and in Situ Wave Buoy Observations. *Remote Sensing*. [doi:10.3390/rs12213623](https://doi.org/10.3390/rs12213623) [published version, CC BY](https://www.mdpi.com/2072-4292/12/21/3623/pdf)
- Mitsopoulos (2023). Characterizing Coastal Wind Speed and Significant Wave Height Using Satellite Altimetry and Buoy Data. *Remote Sensing*. [doi:10.3390/rs15040987](https://doi.org/10.3390/rs15040987) [published version, CC BY](https://www.mdpi.com/2072-4292/15/4/987/pdf)
- YAMAGUCHI (1985). NUMERICAL MODELS FOR WAVE TRANSFORMATION DUE TO CURRENT-DEPTH REFRACTION. *Doboku Gakkai Ronbunshu*. [doi:10.2208/jscej.1985.357_187](https://doi.org/10.2208/jscej.1985.357_187) [published version, read only](https://www.jstage.jst.go.jp/article/jscej1984/1985/357/1985_357_187/_pdf)
- Abeshima (2005). Mooring Limit of Small Fishing Boat at Kumaishi Fishing Port. *The Journal of Japan Institute of Navigation*. [doi:10.9749/jin.112.345](https://doi.org/10.9749/jin.112.345) [published version, read only](https://www.jstage.jst.go.jp/article/jin/112/0/112_KJ00004696786/_pdf)
- Jacobsen (2026). Wave attenuation through a saltmarsh: Heterogeneous vegetation characteristics and seasonal variability. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2026.105099](https://doi.org/10.1016/j.coastaleng.2026.105099)
- Bieri (2026). Designing restored oyster reefs to enhance coastal protection benefits. *Estuarine, Coastal and Shelf Science*. [doi:10.1016/j.ecss.2026.110156](https://doi.org/10.1016/j.ecss.2026.110156) [submitted manuscript, read only](https://papers.ssrn.com/sol3/Delivery.cfm/efdb6ddd-282e-43ff-bebf-31f0a0de97e2-MECA.pdf?abstractid=6110269&mirid=1)
- OKI (2008). Development of Multidirectional Random Wave Transformation Model in Wave-Current Coexisting Field. *PROCEEDINGS OF COASTAL ENGINEERING, JSCE*. [doi:10.2208/proce1989.55.1](https://doi.org/10.2208/proce1989.55.1) [published version, read only](https://www.jstage.jst.go.jp/article/proce1989/55/0/55_0_1/_pdf)
- Lee (2005). Analysis of Numerical Model Wave Predictions for Coastal Waters at Gunsan-Janghang Harbor Entrance. *Journal of Navigation and Port Research*. [doi:10.5394/kinpr.2005.29.7.627](https://doi.org/10.5394/kinpr.2005.29.7.627) [published version, read only](http://koreascience.or.kr:80/article/JAKO200507521962270.pdf)
