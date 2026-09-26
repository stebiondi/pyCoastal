# Wave setup

`waves.transformation.breaking.setup` | Breaking-induced mean water-level response.

Parent: [Waves and wave transformation](waves.md) > [Wave transformation](waves.transformation.md) > [Breaking](waves.transformation.breaking.md)

Papers: 23. Claims: 30. Equations: 4.

## Synthesis

**Well established.** For intermediate and reflective natural beaches, shoreline setup increases with local foreshore slope when offshore wave height and wavelength are held fixed; the widely used field form is mean eta=0.35 beta_f sqrt(H0 L0).

**Governing physics.** The cross-shore gradient of breaking-wave momentum flux is balanced principally by the mean-water-level pressure gradient, with bottom stress and roller-delayed momentum transfer modifying the detailed profile. Beach slope changes the available cross-shore distance and depth pattern over which breaking and momentum loss occur.

**Dimensionless parameters.** Surf similarity or Iribarren scaling combines slope and wave steepness, beta/sqrt(H0/L0). It organizes the transition between dissipative and more reflective regimes, but slope definition—foreshore, surf-zone, local, or profile-averaged—is part of the model and not a neutral preprocessing choice.

**Major equations.** Two slope relations describe different quantities: Stockdon's shoreline elevation eta_bar=0.35 beta_f sqrt(H0 L0) is linear in local foreshore slope, whereas Van Dorn's m=3.4 S^2 describes the cross-shore gradient of the mean setup profile on smooth uniform laboratory slopes. They are not interchangeable shoreline predictions.

**Typical methods.** Slope dependence is evaluated using filtered mean-level profiles on fixed laboratory beaches, video-derived mean shoreline elevations across natural beaches, buried pressure-gauge arrays on evolving barred profiles, and phase-resolving numerical matrices that independently vary beta and wave spectra.

**Numerical models.** The SandyDuck wave-averaged model solves a cross-shore balance among radiation stress, setup pressure gradient, roller energy and bottom stress; funwaveC resolves nonlinear wave transformation and shoreline motion with Boussinesq equations, eddy-viscosity breaking, and a thin-layer wetting treatment.

**Experimental datasets.** The reviewed evidence includes twelve smooth-slope periodic-wave combinations, ten natural-beach video campaigns, ninety days of SandyDuck setup and undertow observations, and 180 idealized Boussinesq simulations.

**Validated ranges.** Van Dorn tested slopes 0.022, 0.040 and 0.083 with periods 1.65-4.80 s; Guza-Feddersen tested beta=0.02-0.04, Hs=0.4-2.5 m and fp=0.06-0.14 Hz; SandyDuck observations span Hrms=0.20-2.10 m, depths 0.3-6 m and setup -0.03 to 0.50 m. These ranges do not establish behavior for arbitrary steep, composite, reef, or mobile profiles.

**Recent advances.** Recent advances resolve setup within wave-resolving XBeach and SWASH, incorporate breaking-wave rollers and roughness-dependent bottom stress, couple radiation-stress forcing to storm surge, derive slope- and direction-aware empirical predictors, and translate setup into probabilistic reef and coastal-flood assessments.

**Disagreements.** Slope dependence is regime- and definition-dependent rather than universal. Stockdon's general field coefficient is 0.35, while the idealized Boussinesq regression gives 0.53; fully dissipative field cases use a slope-independent offshore-wave scale; and the gentle-flume quadratic law concerns setup gradient rather than shoreline elevation.

**Limitations.** Slope-only predictors cannot reproduce detailed setup on an evolving barred beach: SandyDuck required bottom-stress and roller/profile physics, and excluding bottom stress tripled shallow-water mean error under the tested closure. Setup must not be conflated with swash or total runup. Guza-Feddersen found no obvious slope dependence for normalized infragravity runup over beta=0.02-0.04, even though mean setup was better predicted with beta; Stockdon likewise uses a separate slope-independent infragravity term. On the steep laboratory slope S=0.083, setup gradient became period dependent and mean elevation was difficult to define under violent breaking, so the gentle-slope frequency-independent relation cannot be extrapolated safely.

**Open questions.** Needed evidence includes time-varying local slope during storms, independent extreme-event validation, mobile and barred profiles, directional and oblique waves, reefs and composite slopes, and a physically consistent transition between general and fully dissipative parameterizations.

**Seminal papers.** Van Dorn (1976) isolates slope and period in controlled setup/runup tests; Stockdon et al. (2006) supplies the standard ten-campaign field parameterization; Apotsos et al. (2007) adds natural-beach bottom-stress and roller physics; Guza and Feddersen (2012) independently tests the slope scaling in a phase-resolving matrix.

## Equations

### Gentle-beach setup-profile slope fit

$$
m=\frac{d\bar{\eta}}{dx}=3.4S^2
$$

Regime: Compiled smooth fixed-slope laboratory beaches; frequency independence observed only for S<=0.040.

Variables: `m` mean water-surface setup gradient; `eta_bar` mean surface elevation; `x` cross-shore coordinate; `S` uniform beach slope

Source: (William G. Van Dorn 1976, [doi:10.9753/icce.v15.41](https://doi.org/10.9753/icce.v15.41))

### Cross-shore setup momentum balance

$$
\frac{\partial S_{xx}}{\partial x}+\rho g(\bar{\eta}+d)\frac{\partial\bar{\eta}}{\partial x}+\tau_B=0
$$

Regime: Alongshore-uniform bathymetry and waves with negligible wind stress.

Variables: `Sxx` cross-shore wave radiation stress including optional roller energy; `eta_bar` time-mean setup; `d` still-water depth; `tauB` bottom stress; `rho` water density; `g` gravitational acceleration

Source: (Apotsos 2007, [doi:10.1029/2006jc003549](https://doi.org/10.1029/2006jc003549))

### Modeled shoreline setup regression

$$
\bar{R}=0.53\,\beta(H_{s,0}L_0)^{1/2}
$$

Regime: The 180 funwaveC simulations, mostly dissipative, beta=0.02-0.04.

Variables: `Rbar` time- and alongshore-mean shoreline setup; `beta` planar beach slope; `Hs0` deep-water significant wave height; `L0` deep-water wavelength from peak frequency

Source: (Guza 2012, [doi:10.1029/2012gl051959](https://doi.org/10.1029/2012gl051959))

### Stockdon shoreline setup parameterization

$$
\bar{\eta}=0.35\,\beta_f(H_0L_0)^{1/2}
$$

Regime: General natural-beach branch across ten field campaigns; fully dissipative beaches use a slope-independent branch.

Variables: `eta_bar` time-mean non-tidal shoreline setup; `beta_f` local foreshore slope; `H0` deep-water significant wave height; `L0` deep-water wavelength from peak period

Source: (Stockdon 2006, [doi:10.1016/j.coastaleng.2005.12.005](https://doi.org/10.1016/j.coastaleng.2005.12.005))

## Claims

- **C85.** For smooth planar slopes S=0.022 and 0.040, the measured mean setup profile was approximately linear across the surf zone and its gradient was independent of wave period within experimental error. *Regime: Plate-glass laboratory beaches, S<=0.040, periods 1.65-4.80 s, periodic breaking waves..* [direct_finding, experimental] (William G. Van Dorn 1976, [doi:10.9753/icce.v15.41](https://doi.org/10.9753/icce.v15.41))
- **C86.** Across the study and compiled comparison data, the authors proposed m=3.4 S^2 for setup-profile gradient m versus uniform beach slope S. *Regime: Smooth uniform slopes represented by the compiled laboratory data; not a universal shoreline-setup formula..* [proposed_hypothesis, experimental] (William G. Van Dorn 1976, [doi:10.9753/icce.v15.41](https://doi.org/10.9753/icce.v15.41))
- **C87.** On the steepest tested slope S=0.083, setup gradient appeared to increase with wave period and mean elevation became poorly defined for the longest, violently turbulent breaking cases. *Regime: S=0.083 plate-glass beach; especially periods 3.43 and 4.80 s..* [direct_finding, experimental] (William G. Van Dorn 1976, [doi:10.9753/icce.v15.41](https://doi.org/10.9753/icce.v15.41))
- **C88.** Integrating the fitted setup-gradient relation to predict shoreline setup produced discrepancies too large for the proposed expression to be considered a satisfactory prediction method. *Regime: The study's three uniform slopes and breaking-wave cases..* [direct_finding, experimental] (William G. Van Dorn 1976, [doi:10.9753/icce.v15.41](https://doi.org/10.9753/icce.v15.41))
- **C89.** Across the 90-day SandyDuck dataset, a setup model including rollers and undertow-related bottom stress achieved squared correlations above 0.59 and agreement within about 30% over depths to 6 m. *Regime: Barred natural beach; Hrms 0.20-2.10 m, angles within 35 degrees, setup -0.03 to 0.50 m..* [direct_finding, mixed] (Apotsos 2007, [doi:10.1029/2006jc003549](https://doi.org/10.1029/2006jc003549))
- **C90.** Neglecting bottom stress tripled mean setup error in 0.3-1.0 m water depth and increased shallow-water underprediction. *Regime: The paper's vertically uniform eddy-viscosity and undertow closure at SandyDuck..* [direct_finding, mixed] (Apotsos 2007, [doi:10.1029/2006jc003549](https://doi.org/10.1029/2006jc003549))
- **C91.** Removing the wave roller changed average setup by less than about 10% but shifted the setdown-to-setup transition shoreward by approximately 6 m. *Regime: The SandyDuck bar amplitudes and tested roller closures; several-meter bars may behave differently..* [direct_finding, mixed] (Apotsos 2007, [doi:10.1029/2006jc003549](https://doi.org/10.1029/2006jc003549))
- **C92.** The field evidence shows that a planar slope and radiation-stress gradient alone do not determine natural-beach setup because bars, bottom stress, and evolving shallow bathymetry change the cross-shore balance. *Regime: Natural barred beaches comparable to SandyDuck..* [inferred_relationship, mixed] (Apotsos 2007, [doi:10.1029/2006jc003549](https://doi.org/10.1029/2006jc003549))
- **C93.** Across 180 planar-beach simulations with slope 0.02-0.04, setup was better explained by beta sqrt(Hs0 L0) (r2=0.71, RMS error 0.07 m) than by sqrt(Hs0 L0) alone (r2=0.58, RMS error 0.09 m). *Regime: Mostly dissipative conditions; Hs=0.4-2.5 m, fp=0.06-0.14 Hz, slopes 0.02-0.04..* [direct_finding, numerical] (Guza 2012, [doi:10.1029/2012gl051959](https://doi.org/10.1029/2012gl051959))
- **C94.** The model best-fit shoreline-setup coefficient was 0.53 in Rbar=coefficient beta sqrt(Hs0 L0), compared with the Stockdon field coefficient 0.35. *Regime: Idealized funwaveC planar beaches and the reported parameter matrix..* [direct_finding, numerical] (Guza 2012, [doi:10.1029/2012gl051959](https://doi.org/10.1029/2012gl051959))
- **C96.** Across ten natural-beach field experiments, shoreline setup was best parameterized with foreshore slope, deep-water significant wave height, and deep-water wavelength rather than surf-zone slope. *Regime: The ten dynamically diverse natural-beach campaigns; detailed full-text ranges are not available in this extraction..* [direct_finding, field] (Stockdon 2006, [doi:10.1016/j.coastaleng.2005.12.005](https://doi.org/10.1016/j.coastaleng.2005.12.005))
- **C97.** The reported general shoreline-setup parameterization is mean eta=0.35 beta_f sqrt(H0 L0), implying linear dependence on local foreshore slope at fixed deep-water wave scale. *Regime: General natural-beach branch; not the fully dissipative branch and not infragravity swash..* [direct_finding, field] (Stockdon 2006, [doi:10.1016/j.coastaleng.2005.12.005](https://doi.org/10.1016/j.coastaleng.2005.12.005))
- **C98.** For infragravity-dominated dissipative beaches, the study found setup and swash depended on sqrt(H0 L0) without a statistically significant linear dependence on foreshore or surf-zone slope. *Regime: Fully dissipative, infragravity-dominated beaches in the field dataset..* [direct_finding, field] (Stockdon 2006, [doi:10.1016/j.coastaleng.2005.12.005](https://doi.org/10.1016/j.coastaleng.2005.12.005))
- **C1325.** Improved XBeach group forcing separates setup, infragravity and incident-band swash more accurately; nonhydrostatic runup deviated at most 15% in a high-quality flume test but underestimated low overtopping rates. *Regime: Improving predictions of swash dynamics in XBeach: The role of groupiness and incident-band runup.* [direct_finding, mixed] (Dano Roelvink 2018, [doi:10.1016/j.coastaleng.2017.07.004](https://doi.org/10.1016/j.coastaleng.2017.07.004))
- **C1326.** Eleven Torrey Pines field runs under 0.6-1.6 m deep-water significant waves yielded shoreline setup approximately equal to 0.17 times deep-water significant wave height; the inferred setup slope increased very near shore, but the regression excluded one unexplained outlier and lacked a surveyed common datum between offshore and shoreline sensors. *Regime: Nearly normally incident spilling and mixed breaking waves on the gently sloping, fine-sand Torrey Pines beach during the measured 1978 conditions..* [direct_finding, field] (Guza 1981, [doi:10.1029/jc086ic05p04133](https://doi.org/10.1029/jc086ic05p04133))
- **C1327.** Guam reef-flat setup correlated above 0.95 with incident waves, scaled near shore to about 35% of incident RMS height, and reached 1.3 m during Tropical Storm Man-Yi. *Regime: Wave setup over a Pacific Island fringing reef.* [direct_finding, field] (Oliver J. Vetter 2010, [doi:10.1029/2010jc006455](https://doi.org/10.1029/2010jc006455))
- **C1328.** Reef roughness reduced setup-producing radiation-stress gradients by 18% but generated mean bottom stress that increased predicted setup by 16%, leaving rough and smooth reef-flat setup within 7% on average. *Regime: Wave Setup over a Fringing Reef with Large Bottom Roughness.* [direct_finding, experimental] (Mark L. Buckley 2016, [doi:10.1175/jpo-d-15-0148.1](https://doi.org/10.1175/jpo-d-15-0148.1))
- **C1329.** A 55 m flume study found linear-theory radiation stress underpredicted reef setdown and setup, especially for large waves and low water; adding a breaking-wave roller improved magnitude and forcing location. *Regime: Dynamics of Wave Setup over a Steeply Sloping Fringing Reef.* [direct_finding, experimental] (Mark L. Buckley 2015, [doi:10.1175/jpo-d-15-0067.1](https://doi.org/10.1175/jpo-d-15-0067.1))
- **C1330.** Chesapeake sensitivity tests found wave setup up to 0.19 m and dependent on offshore height, breaking angle, profile morphology and mesh resolution, while friction and wetting parameters also materially altered levels. *Regime: Storm Surge Modeling in Large Estuaries: Sensitivity Analyses to Parameters and Physical Processes in the Chesapeake Bay.* [direct_finding, mixed] (Juan Garzon 2016, [doi:10.3390/jmse4030045](https://doi.org/10.3390/jmse4030045))
- **C1331.** Australian extreme-water analysis shows shoreline setup equations and local beach slope materially affect the estimated wind-wave contribution to mean total water level. *Regime: Extreme Water Levels for Australian Beaches Using Empirical Equations for Shoreline Wave Setup.* [direct_finding, mixed] (J. G. O'Grady 2019, [doi:10.1029/2018jc014871](https://doi.org/10.1029/2018jc014871))
- **C1332.** Wave-resolving XBeach reproduced setup and swash components better than wave-averaged XBeach on an intermediate-reflective beach, including incident-band motion and larger infragravity swash. *Regime: Simulating wave runup on an intermediate–reflective beach using a wave-resolving and a wave-averaged version of XBeach.* [direct_finding, mixed] (A.F. de Beer 2021, [doi:10.1016/j.coastaleng.2020.103788](https://doi.org/10.1016/j.coastaleng.2020.103788))
- **C1333.** Barrier-island observations show back-barrier water-level gradients can overcome the cross-shore gradient from wave setup and reverse inundation flow, while breaking dissipates both short and infragravity waves. *Regime: Observations of waves and currents during barrier island inundation.* [direct_finding, mixed] (A. Engelstad 2017, [doi:10.1002/2016jc012545](https://doi.org/10.1002/2016jc012545))
- **C1334.** Validated SWASH simulations found Puerto Morelos lagoon setup strongly correlated with offshore sea-swell energy, while geometry controlled infragravity resonance and whether the reef protected or enhanced inundation. *Regime: Wave-induced extreme water levels in the Puerto Morelos fringing reef lagoon.* [direct_finding, mixed] (Alec Torres‐Freyermuth 2012, [doi:10.5194/nhess-12-3765-2012](https://doi.org/10.5194/nhess-12-3765-2012))
- **C1335.** Coupled wave–surge simulation added 0.3–0.5 m of Ivan-like Tampa Bay surge through wave-induced forces, while surge increased nearshore significant wave height by about 1.0–1.5 m. *Regime: Coupling of surge and waves for an Ivan‐like hurricane impacting the Tampa Bay, Florida region.* [direct_finding, mixed] (Yong Huang 2010, [doi:10.1029/2009jc006090](https://doi.org/10.1029/2009jc006090))
- **C1336.** In Martinique, radiation-stress-driven wave setup contributed up to 100% of total modeled surge in cases where the narrow shelf limited wind-driven water accumulation. *Regime: Assessing storm surge hazard and impact of sea level rise in the Lesser Antilles case study of Martinique.* [direct_finding, mixed] (Yann Krien 2017, [doi:10.5194/nhess-17-1559-2017](https://doi.org/10.5194/nhess-17-1559-2017))
- **C1337.** During Cyclone Tauktae, setup exceeded 0.6 m near steep Chellanam profiles and combined with long and short waves to cause severe flooding even at low tide with negligible surge. *Regime: Wave induced coastal flooding along the southwest coast of India during tropical cyclone Tauktae.* [direct_finding, mixed] (R. Ramakrishnan 2022, [doi:10.1038/s41598-022-24557-z](https://doi.org/10.1038/s41598-022-24557-z))
- **C1338.** A field technique measured shoreline setup increasing approximately linearly with incident wave height, agreeing with theory based on surf-zone wave decay and reaching about 40 cm. *Regime: Observations of wave‐induced set‐up on a natural beach.* [direct_finding, field] (King 1990, [doi:10.1029/jc095ic12p22289](https://doi.org/10.1029/jc095ic12p22289))
- **C1339.** Hundreds of XBeach-NH+ simulations produced validated equations for setup and incident, infragravity and total runup across 1–12 m waves, 6–16 s periods and beach slopes from 1:100 to 1:5. *Regime: A Model-Derived Empirical Formulation for Wave Run-Up on Naturally Sloping Beaches.* [direct_finding, mixed] (Maarten van Ormondt 2021, [doi:10.3390/jmse9111185](https://doi.org/10.3390/jmse9111185))
- **C1340.** Numerical experiments show ambient-current bottom stress changes setup: offshore currents create onshore stress that increases setup, whereas onshore currents create offshore stress that decreases it. *Regime: Numerical Experiments of Bottom Stress on Wave Setup.* [direct_finding, mixed] (Liu 2012, [doi:10.4028/www.scientific.net/amm.212-213.1108](https://doi.org/10.4028/www.scientific.net/amm.212-213.1108))
- **C1648.** On a barred beach, eleven current meters and fifteen wave staffs measured offshore undertow up to about 0.20 m/s and onshore velocity skewness up to 0.60; shoreline setup explained up to 82% of mean-flow variability and incident wave height explained 86% of setup variability. *Regime: Nontidal low-relief barred surf zone during the observed storm growth and decay..* [direct_finding, field] (Brian Greenwood 1990, [doi:10.1016/0378-3839(90)90034-t](https://doi.org/10.1016/0378-3839(90)90034-t))

## Papers

- Stockdon (2006). Empirical parameterization of setup, swash, and runup. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2005.12.005](https://doi.org/10.1016/j.coastaleng.2005.12.005)
- Guza (1981). Wave set‐up on a natural beach. *Journal of Geophysical Research: Oceans*. [doi:10.1029/jc086ic05p04133](https://doi.org/10.1029/jc086ic05p04133) [published version, read only](https://www.researchgate.net/publication/240484899_Wave_Set-Up_on_a_Natural_Beach)
- Dano Roelvink (2018). Improving predictions of swash dynamics in XBeach: The role of groupiness and incident-band runup. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2017.07.004](https://doi.org/10.1016/j.coastaleng.2017.07.004) [published version, CC BY](https://www.sciencedirect.com/science/article/pii/S0378383917301321/pdf)
- Gourlay (2005). Wave-generated flow on coral reefs—an analysis for two-dimensional horizontal reef-tops with steep faces. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2004.11.007](https://doi.org/10.1016/j.coastaleng.2004.11.007)
- Apotsos (2007). Effects of wave rollers and bottom stress on wave setup. *Journal of Geophysical Research: Oceans*. [doi:10.1029/2006jc003549](https://doi.org/10.1029/2006jc003549) [accepted manuscript, read only](https://falk.ucsd.edu/pdf/Apotsos2007JGR.pdf)
- Guza (2012). Effect of wave frequency and directional spread on shoreline runup. *Geophysical Research Letters*. [doi:10.1029/2012gl051959](https://doi.org/10.1029/2012gl051959) [accepted manuscript, read only](https://falk.ucsd.edu/pdf/GuzaFeddersen2012GRL.pdf)
- Oliver J. Vetter (2010). Wave setup over a Pacific Island fringing reef. *Journal of Geophysical Research: Oceans*. [doi:10.1029/2010jc006455](https://doi.org/10.1029/2010jc006455) [published version, read only](https://onlinelibrary.wiley.com/doi/pdfdirect/10.1029/2010JC006455)
- Mark L. Buckley (2016). Wave Setup over a Fringing Reef with Large Bottom Roughness. *Journal of Physical Oceanography*. [doi:10.1175/jpo-d-15-0148.1](https://doi.org/10.1175/jpo-d-15-0148.1) [published version, read only](https://api.research-repository.uwa.edu.au/ws/files/14681806/Buckley_JPO2016_ReefRoughnessSetup.pdf)
- Mark L. Buckley (2015). Dynamics of Wave Setup over a Steeply Sloping Fringing Reef. *Journal of Physical Oceanography*. [doi:10.1175/jpo-d-15-0067.1](https://doi.org/10.1175/jpo-d-15-0067.1) [published version, read only](https://journals.ametsoc.org/downloadpdf/journals/phoc/45/12/jpo-d-15-0067.1.pdf)
- Juan Garzon (2016). Storm Surge Modeling in Large Estuaries: Sensitivity Analyses to Parameters and Physical Processes in the Chesapeake Bay. *Journal of Marine Science and Engineering*. [doi:10.3390/jmse4030045](https://doi.org/10.3390/jmse4030045) [published version, CC BY](https://mdpi-res.com/d_attachment/jmse/jmse-04-00045/article_deploy/jmse-04-00045.pdf)
- Brian Greenwood (1990). Vertical and horizontal structure in cross-shore flows: An example of undertow and wave set-up on a barred beach. *Coastal Engineering*. [doi:10.1016/0378-3839(90)90034-t](https://doi.org/10.1016/0378-3839(90)90034-t) [published version, read only](https://utoronto.scholaris.ca/bitstreams/b9e51059-fa11-42b4-b0c2-284e6bea5445/download)
- Alec Torres‐Freyermuth (2012). Wave-induced extreme water levels in the Puerto Morelos fringing reef lagoon. *Natural Hazards and Earth System Sciences*. [doi:10.5194/nhess-12-3765-2012](https://doi.org/10.5194/nhess-12-3765-2012) [published version, CC BY](https://nhess.copernicus.org/articles/12/3765/2012/nhess-12-3765-2012.pdf)
- A.F. de Beer (2021). Simulating wave runup on an intermediate–reflective beach using a wave-resolving and a wave-averaged version of XBeach. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2020.103788](https://doi.org/10.1016/j.coastaleng.2020.103788) [published version, public domain](https://www.sciencedirect.com/science/article/pii/S0378383920304749)
- A. Engelstad (2017). Observations of waves and currents during barrier island inundation. *Journal of Geophysical Research: Oceans*. [doi:10.1002/2016jc012545](https://doi.org/10.1002/2016jc012545) [published version, CC BY-NC-ND](https://api.wiley.com/onlinelibrary/tdm/v1/articles/10.1002%2F2016JC012545)
- J. G. O'Grady (2019). Extreme Water Levels for Australian Beaches Using Empirical Equations for Shoreline Wave Setup. *Journal of Geophysical Research: Oceans*. [doi:10.1029/2018jc014871](https://doi.org/10.1029/2018jc014871) [published version, read only](https://onlinelibrary.wiley.com/doi/pdfdirect/10.1029/2018JC014871)
- Yong Huang (2010). Coupling of surge and waves for an Ivan‐like hurricane impacting the Tampa Bay, Florida region. *Journal of Geophysical Research: Oceans*. [doi:10.1029/2009jc006090](https://doi.org/10.1029/2009jc006090) [accepted manuscript, read only](https://digitalcommons.usf.edu/cgi/viewcontent.cgi?article=1172&context=msc_facpub)
- King (1990). Observations of wave‐induced set‐up on a natural beach. *Journal of Geophysical Research: Oceans*. [doi:10.1029/jc095ic12p22289](https://doi.org/10.1029/jc095ic12p22289)
- Yann Krien (2017). Assessing storm surge hazard and impact of sea level rise in the Lesser Antilles case study of Martinique. *Natural Hazards and Earth System Sciences*. [doi:10.5194/nhess-17-1559-2017](https://doi.org/10.5194/nhess-17-1559-2017) [published version, CC BY](https://nhess.copernicus.org/articles/17/1559/2017/nhess-17-1559-2017.pdf)
- R. Ramakrishnan (2022). Wave induced coastal flooding along the southwest coast of India during tropical cyclone Tauktae. *Scientific Reports*. [doi:10.1038/s41598-022-24557-z](https://doi.org/10.1038/s41598-022-24557-z) [published version, CC BY](https://www.nature.com/articles/s41598-022-24557-z.pdf)
- Maarten van Ormondt (2021). A Model-Derived Empirical Formulation for Wave Run-Up on Naturally Sloping Beaches. *Journal of Marine Science and Engineering*. [doi:10.3390/jmse9111185](https://doi.org/10.3390/jmse9111185) [published version, CC BY](https://mdpi-res.com/d_attachment/jmse/jmse-09-01185/article_deploy/jmse-09-01185.pdf)
- William G. Van Dorn (1976). SET-UP AND RUN-UP IN SHOALING BREAKERS. *Coastal Engineering Proceedings*. [doi:10.9753/icce.v15.41](https://doi.org/10.9753/icce.v15.41) [published version, CC BY](https://journals.tdl.org/icce/index.php/icce/article/download/3090/2755)
- Liu (2012). Numerical Experiments of Bottom Stress on Wave Setup. *Applied Mechanics and Materials*. [doi:10.4028/www.scientific.net/amm.212-213.1108](https://doi.org/10.4028/www.scientific.net/amm.212-213.1108) [published version, CC BY](https://www.scientific.net/AMM.212-213.1108)
- Svendsen (1984). Wave heights and set-up in a surf zone. *Coastal Engineering*. [doi:10.1016/0378-3839(84)90028-0](https://doi.org/10.1016/0378-3839(84)90028-0) [published version, read only](https://repository.tudelft.nl/file/File_0a117cc6-9ce5-4556-a7c6-ff700403272f)
