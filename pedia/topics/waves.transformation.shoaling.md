# Shoaling

`waves.transformation.shoaling` | Depth-induced amplitude and kinematic change.

Parent: [Waves and wave transformation](waves.md) > [Wave transformation](waves.transformation.md)

Papers: 12. Claims: 9. Equations: 6.

## Synthesis

**Well established.** As surface gravity waves enter decreasing depth, reduced group speed and depth-dependent kinematics transform height, wavelength, shape, energy distribution, and momentum flux before and through breaking. Linear shoaling is reliable only within restricted amplitude and bathymetric regimes.

**Governing physics.** Energy or action-flux conservation drives nondissipative height change; nonlinearity sharpens crests and transfers energy among harmonics; refraction redistributes flux directionally; reflection, bottom friction, breaking, vegetation drag, infragravity modulation, and currents add sinks or couplings.

**Dimensionless parameters.** Regime selection uses relative depth h/L or kh, deep-water steepness H0/L0, local relative height H/h, Ursell number, bed slope, breaker index, directional angle, vegetation submergence and density, and bandwidth or spectral shape.

**Major equations.** Core descriptions include Green's law for long waves, linear energy-flux shoaling coefficients, matched linear-cnoidal theory, random-wave height distributions with breaking, depth-limited surf-zone relations, radiation-stress/momentum-flux balances, and phase-resolving nonhydrostatic equations.

**Typical methods.** Studies combine analytical conservation laws and asymptotic expansions, wave-flume measurements, natural-beach arrays, stochastic transformation models, barred-beach calculations, and three-dimensional nonhydrostatic simulation.

**Numerical models.** Model classes include linear and cnoidal transformation tables, stochastic breaking-height/vegetation-drag formulations, depth-limited surf-zone decay, 3-D momentum-flux theory, and nonhydrostatic phase-resolving models for combined shoaling, refraction, diffraction, and breaking.

**Experimental datasets.** Reviewed benchmarks include variable-geometry and regular-wave laboratory shoaling, no-free-second-harmonic linear/cnoidal tests, exposed dissipative-beach surf-zone observations, and source-specific vegetation-force calculations or comparisons.

**Validated ranges.** The matched linear/cnoidal model agreed very well without free second harmonics for H0/L0 up to about 0.03-0.04, using linear theory above h/L0=0.10 and cnoidal theory below; other demonstrations cover small-amplitude variable transitions, dissipative-beach surf zones, rigid vegetation, and nondissipative barred bathymetry.

**Recent advances.** Recent nonhydrostatic models jointly resolve shoaling, refraction, diffraction, and breaking in three dimensions, creating a route to test reduced coefficients against complex transformations while retaining computationally practical coastal domains.

**Disagreements.** No single shoaling coefficient spans all regimes. Linear theory departs at greater steepness, local H/h is not constant throughout surf zones, and depth-integrated radiation stress obscures vertical flux structure needed by 3-D circulation models.

**Limitations.** Common exclusions are reflection, friction, breaking, free harmonics, broad bandwidth, currents, directional spreading, flexible vegetation, rotational flow, and complex three-dimensional bathymetry. Field depth limitation mixes shoaling, breaking, setup, and infragravity variability.

**Open questions.** Needs include common uncertainty-aware benchmarks across shoaling and breaking, broadband nonlinear directionality, wave-current and vegetation flexibility, consistent 3-D momentum coupling, bathymetric-history effects, and efficient model-selection criteria for engineering applications.

**Seminal papers.** The 1968 Green/linear laboratory comparison and 1977 linear-cnoidal matching study establish early engineering transformations; the 1992 field study demonstrates nonconstant surf-zone H/h, while later work extends forcing vertically and to vegetation.

## Equations

### Green's law

$$
H(x)=K_s(h/L,H/L,\beta,\mathcal{D})H_0
$$

Regime: Small-amplitude waves over variable-geometry shallow-water transitions; reflection and friction omitted in the intermediate/deep-water comparison.

Variables: `H` local wave height; `K_s` shoaling/transformation factor; `h` local depth; `L` wavelength; `beta` bed slope; `D` dissipation, directionality, or vegetation terms; normalized dependency statement

Source: (Bourodimos 1968, [doi:10.1016/0029-8018(68)90016-4](https://doi.org/10.1016/0029-8018(68)90016-4))

### linear-cnoidal matched shoaling model

$$
H(x)=K_s(h/L,H/L,\beta,\mathcal{D})H_0
$$

Regime: Regular waves without free second-harmonic components; linear theory for h/L0>0.10, cnoidal theory for h/L0<0.10; H0/L0 up to 0.03-0.04 for very good agreement.

Variables: `H` local wave height; `K_s` shoaling/transformation factor; `h` local depth; `L` wavelength; `beta` bed slope; `D` dissipation, directionality, or vegetation terms; normalized dependency statement

Source: (Svendsen 1977, [doi:10.1016/0378-3839(77)90018-7](https://doi.org/10.1016/0378-3839(77)90018-7))

### depth-limited surf-zone wave-height model

$$
H(x)=K_s(h/L,H/L,\beta,\mathcal{D})H_0
$$

Regime: Natural exposed dissipative beach within the surf zone; field analysis of local depth and breaker-line distance effects.

Variables: `H` local wave height; `K_s` shoaling/transformation factor; `h` local depth; `L` wavelength; `beta` bed slope; `D` dissipation, directionality, or vegetation terms; normalized dependency statement

Source: (Nelson 1992, [doi:10.1016/0378-3839(92)90013-k](https://doi.org/10.1016/0378-3839(92)90013-k))

### 3-D wave-induced momentum-flux formulation

$$
H(x)=K_s(h/L,H/L,\beta,\mathcal{D})H_0
$$

Regime: Irrotational, nondissipative three-dimensional waves over two-dimensional irregular bathymetry, illustrated for a barred beach.

Variables: `H` local wave height; `K_s` shoaling/transformation factor; `h` local depth; `L` wavelength; `beta` bed slope; `D` dissipation, directionality, or vegetation terms; normalized dependency statement

Source: (Herman 2006, [doi:10.1016/j.coastaleng.2005.12.001](https://doi.org/10.1016/j.coastaleng.2005.12.001))

### Mendez random-wave height distribution and vegetation-drag model

$$
H(x)=K_s(h/L,H/L,\beta,\mathcal{D})H_0
$$

Regime: Stationary narrow-band random waves in shallow water over rigid vegetation; shoaling and breaking represented by the Mendez et al. wave-height distribution.

Variables: `H` local wave height; `K_s` shoaling/transformation factor; `h` local depth; `L` wavelength; `beta` bed slope; `D` dissipation, directionality, or vegetation terms; normalized dependency statement

Source: (Henry 2013, [doi:10.1016/j.coastaleng.2013.03.004](https://doi.org/10.1016/j.coastaleng.2013.03.004))

### Wave-energy transformation balance

$$
\nabla\cdot(E\mathbf{C}_g)=-D_b-D_f
$$

Regime: The 225 irregular-wave tests on the reported mobile-bed parallel-contour hydraulic model.

Variables: `E` wave energy density; `C_g` group velocity; `D_b` breaking dissipation; `D_f` bottom-friction or other dissipation

Source: (Kamphuis 1991, [doi:10.1016/0378-3839(91)90001-w](https://doi.org/10.1016/0378-3839(91)90001-w))

## Claims

- **C271.** For regular waves without free second harmonics, a wave-height-continuous linear/cnoidal shoaling model agreed very well with experiments up to H0/L0 about 0.03-0.04, whereas linear theory failed at larger steepness in the h/L0>0.10 region. *Regime: Regular waves without free second-harmonic components; linear theory for h/L0>0.10, cnoidal theory for h/L0<0.10; H0/L0 up to 0.03-0.04 for very good agreement..* [direct_finding, mixed] (Svendsen 1977, [doi:10.1016/0378-3839(77)90018-7](https://doi.org/10.1016/0378-3839(77)90018-7))
- **C272.** For stationary narrow-band random waves over rigid vegetation, empirical regular-wave drag coefficients combined with a stochastic shoaling-and-breaking height distribution provide a practical vegetation-force estimate across different slopes. *Regime: Stationary narrow-band random waves in shallow water over rigid vegetation; shoaling and breaking represented by the Mendez et al. wave-height distribution..* [direct_finding, analytical] (Henry 2013, [doi:10.1016/j.coastaleng.2013.03.004](https://doi.org/10.1016/j.coastaleng.2013.03.004))
- **C273.** On an exposed dissipative beach, surf-zone wave-height-to-depth ratios decayed with both local mean water depth and distance from the breaker line, indicating an infragravity-associated decay process in addition to breaking turbulence. *Regime: Natural exposed dissipative beach within the surf zone; field analysis of local depth and breaker-line distance effects..* [direct_finding, field] (Nelson 1992, [doi:10.1016/0378-3839(92)90013-k](https://doi.org/10.1016/0378-3839(92)90013-k))
- **C274.** For small-amplitude waves propagating through variable-geometry transitions, Green's law and a reflection- and friction-free linear transformation model showed fair agreement with laboratory shoaling measurements. *Regime: Small-amplitude waves over variable-geometry shallow-water transitions; reflection and friction omitted in the intermediate/deep-water comparison..* [direct_finding, mixed] (Bourodimos 1968, [doi:10.1016/0029-8018(68)90016-4](https://doi.org/10.1016/0029-8018(68)90016-4))
- **C275.** For irrotational nondissipative waves over alongshore-uniform irregular bathymetry, vertically varying wave-induced momentum flux balances other vertically varying forcing terms, leaving a depth-invariant total forcing governed by wave-energy and water-depth gradients. *Regime: Irrotational, nondissipative three-dimensional waves over two-dimensional irregular bathymetry, illustrated for a barred beach..* [direct_finding, analytical] (Herman 2006, [doi:10.1016/j.coastaleng.2005.12.001](https://doi.org/10.1016/j.coastaleng.2005.12.001))
- **C340.** In 225 irregular-wave hydraulic-model tests on a mobile-bed beach with parallel contours, Snell refraction described turning, linear theory slightly overpredicted shoaling, bottom friction and percolation were small, and saturation-limited breaking attenuation was essential. *Regime: The 225 irregular-wave tests on the reported mobile-bed parallel-contour hydraulic model..* [direct_finding, experimental] (Kamphuis 1991, [doi:10.1016/0378-3839(91)90001-w](https://doi.org/10.1016/0378-3839(91)90001-w))
- **C372.** For modeled nonbreaking regular waves, horizontal-bed stream-function theory described nonlinear shoaling and de-shoaling on a very gentle cot(beta)=1200 foreshore, whereas steeper de-shoaling released free waves that violated the constant-form approximation. *Regime: Nonbreaking normally incident regular waves over gentle and steep foreshores, including de-shoaling slope cot(beta)=1200..* [direct_finding, numerical] (Mads Røge Eldrup 2020, [doi:10.3390/jmse8050334](https://doi.org/10.3390/jmse8050334))
- **C1277.** Stochastic and deterministic Boussinesq models reproduce observed nonlinear transformation of continuous wave spectra over a natural barred beach; shoaling depends on nonlinearity, incident spectral shape and bottom profile. *Regime: Nonlinear Evolution of Surface Wave Spectra on a Beach.* [direct_finding, mixed] (Craig A. Norheim 1998, [doi:10.1175/1520-0485(1998)028<1534:neosws>2.0.co;2](https://doi.org/10.1175/1520-0485(1998)028<1534:neosws>2.0.co;2))
- **C1535.** A 2 week field experiment was conducted to measure surface wave dissipation on a barrier reef at Kaneohe Bay, Oahu, Hawaii. *Regime: The study system, forcing, data and methods stated in the indexed abstract..* [literature_review_statement, mixed] (Lowe 2005, [doi:10.1029/2004jc002711](https://doi.org/10.1029/2004jc002711))

## Papers

- Craig A. Norheim (1998). Nonlinear Evolution of Surface Wave Spectra on a Beach. *Journal of Physical Oceanography*. [doi:10.1175/1520-0485(1998)028<1534:neosws>2.0.co;2](https://doi.org/10.1175/1520-0485(1998)028<1534:neosws>2.0.co;2) [published version, read only](https://journals.ametsoc.org/downloadpdf/journals/phoc/28/7/1520-0485_1998_028_1534_neosws_2.0.co_2.pdf)
- Svendsen (1977). The wave height variation for regular waves in shoaling water. *Coastal Engineering*. [doi:10.1016/0378-3839(77)90018-7](https://doi.org/10.1016/0378-3839(77)90018-7)
- Kamphuis (1991). Wave transformation. *Coastal Engineering*. [doi:10.1016/0378-3839(91)90001-w](https://doi.org/10.1016/0378-3839(91)90001-w)
- Henry (2013). Wave-induced drag force on vegetation under shoaling random waves. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2013.03.004](https://doi.org/10.1016/j.coastaleng.2013.03.004)
- Nelson (1992). Surf zone transformation of wave height to water depth ratios. *Coastal Engineering*. [doi:10.1016/0378-3839(92)90013-k](https://doi.org/10.1016/0378-3839(92)90013-k)
- Mads Røge Eldrup (2020). Numerical Study on Regular Wave Shoaling, De-Shoaling and Decomposition of Free/Bound Waves on Gentle and Steep Foreshores. *Journal of Marine Science and Engineering*. [doi:10.3390/jmse8050334](https://doi.org/10.3390/jmse8050334) [published version, CC BY](https://mdpi-res.com/d_attachment/jmse/jmse-08-00334/article_deploy/jmse-08-00334.pdf)
- Bourodimos (1968). Gravity wave shoaling and transformation in shallow water. *Ocean Engineering*. [doi:10.1016/0029-8018(68)90016-4](https://doi.org/10.1016/0029-8018(68)90016-4)
- Shirkavand (2025). A 3D non-hydrostatic model for simulating coastal wave transformations: shoaling, diffraction, and refraction. *Scientific Reports*. [doi:10.1038/s41598-025-23341-z](https://doi.org/10.1038/s41598-025-23341-z) [published version, CC BY](https://d-nb.info/1386515426/34)
- Herman (2006). Three-dimensional structure of wave-induced momentum flux in irrotational waves in combined shoaling-refraction conditions. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2005.12.001](https://doi.org/10.1016/j.coastaleng.2005.12.001)
- Lowe (2005). Spectral wave dissipation over a barrier reef. *Journal of Geophysical Research Atmospheres*. [doi:10.1029/2004jc002711](https://doi.org/10.1029/2004jc002711) [published version, read only](https://onlinelibrary.wiley.com/doi/pdfdirect/10.1029/2004JC002711)
- Chazel (2010). Numerical Simulation of Strongly Nonlinear and Dispersive Waves Using a Green–Naghdi Model. *Journal of Scientific Computing*. [doi:10.1007/s10915-010-9395-9](https://doi.org/10.1007/s10915-010-9395-9) [preprint, read only](https://arxiv.org/pdf/1004.3436)
- Binbin Zhao (2014). High-level Green–Naghdi wave models for nonlinear wave transformation in three dimensions. *Journal of Ocean Engineering and Marine Energy*. [doi:10.1007/s40722-014-0009-8](https://doi.org/10.1007/s40722-014-0009-8) [published version, read only](https://link.springer.com/content/pdf/10.1007/s40722-014-0009-8.pdf)
