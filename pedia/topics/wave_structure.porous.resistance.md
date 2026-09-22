# Porous-flow resistance

`wave_structure.porous.resistance` | Darcy, Forchheimer, and calibrated resistance formulations for wave-driven porous flow.

Parent: [Wave-structure interaction](wave_structure.md) > [Porous structures](wave_structure.porous.md)

Papers: 12. Claims: 9. Equations: 7.

## Synthesis

**Well established.** Porous coastal structures dissipate wave energy through viscous and inertial resistance to internal oscillatory flow. Resistance also changes phase, pressure, harmonics, runup, overtopping, and force transmission, so porosity alone cannot describe performance.

**Governing physics.** Linear Darcy resistance scales with velocity and viscosity/permeability, while Forchheimer resistance scales nonlinearly with velocity magnitude. Inertia, turbulence, resonance, interface exchange, material layering, reef geometry, submergence, and breaking modify the balance.

**Dimensionless parameters.** Key controls include porosity, permeability or Darcy number, Forchheimer coefficient, Reynolds number, Keulegan-Carpenter number, B/L, relative submergence, relative grain or element size, layer thickness, wave steepness, and relative depth.

**Major equations.** Continuum models combine volume-averaged mass and momentum conservation with Darcy, Brinkman, or extended Forchheimer resistance; wave-energy balances relate attenuation to drag work, while particle models couple exterior Navier-Stokes motion to porous closures.

**Typical methods.** Methods use internal velocity and pressure measurements, wave-energy-flux budgets, direct force sensing, empirical resistance calibration, analytical attenuation models, Eulerian volume-averaged CFD, and Lagrangian SPH or moving-particle solvers.

**Numerical models.** Reviewed models include ISPH/ISPHP and modified moving-particle formulations with extended Forchheimer resistance, multilayer interface treatment, and validation against porous beds, rockfill, submerged structures, permeable bars, and armored caissons.

**Experimental datasets.** The branch includes idealized internal-flow measurements that distinguish transition and transmission zones and open-access single- and multi-row cubic-reef experiments resolving in-reef velocity, directional forces, and dissipation.

**Validated ranges.** Examples include an SPH porous bed with n=0.39, d=0.55 cm, K=1.02e-8 m2 and C_F=0.51; idealized structures organized by B/L; and single-/multi-row cubic reefs under nonbreaking regular waves across several submergence depths.

**Recent advances.** Direct measurements in porous artificial reefs show drag coefficient decreases with reef Keulegan-Carpenter number and that horizontal drag work dominates nonbreaking-wave dissipation, enabling a mechanism-based analytical attenuation model.

**Disagreements.** There is no universal resistance equation or coefficient set across materials and flow regimes. Continuum closures differ in linear, inertial, Brinkman, turbulence, and interface terms, while apparent coefficients depend on velocity definition, scale, geometry, and calibration dataset.

**Limitations.** Most evidence uses regular or solitary waves, idealized two-dimensional geometry, homogeneous or simplified layering, continuum volume averaging, and source-specific coefficients. Breaking, air entrainment, movable armor, irregular spectra, scale effects, and prototype construction variability remain weakly constrained.

**Open questions.** Priorities are transferable coefficient scaling, pore-to-structure upscaling, three-dimensional and irregular-breaking validation, uncertainty propagation, coupling to stability and sediment response, and optimization of ecological geometry without losing structural performance.

**Seminal papers.** The 1995 internal-flow experiment established B/L-dependent transition and transmission regions; subsequent SPH studies built unified free/porous particle formulations and multilayer capability.

## Equations

### Darcy-Forchheimer porous resistance

$$
-\frac{\partial p}{\partial x}=\rho(\alpha+\beta u)u
$$

Regime: Unsteady flow through the homogeneous porous-breakwall idealization.

Variables: `p` pressure; `x` wave-propagation coordinate; `rho` water density; `u` horizontal pore velocity; `alpha` linear resistance coefficient; `beta` quadratic resistance coefficient

Source: (Safak 2020, [doi:10.1016/j.csr.2020.104268](https://doi.org/10.1016/j.csr.2020.104268))

### Porosity-scaled resistance coefficients

$$
\alpha=\alpha_0\frac{(1-n)^3}{n^2}\frac{\nu}{d^2},\quad \beta=\beta_0\frac{1-n}{n^3}\frac{1}{d}
$$

Regime: Madsen porous-breakwater formulation adopted for branch media.

Variables: `alpha0` dimensionless laminar drag coefficient; `beta0` dimensionless turbulent drag coefficient; `n` porosity; `nu` kinematic viscosity; `d` representative material diameter

Source: (Safak 2020, [doi:10.1016/j.csr.2020.104268](https://doi.org/10.1016/j.csr.2020.104268))

### Darcy-Forchheimer porous resistance

$$
\mathbf{R}=-\frac{\mu}{K}\mathbf{u}-\rho\frac{C_F}{\sqrt{K}}|\mathbf{u}|\mathbf{u}
$$

Regime: Idealized porous structure under oscillatory waves; regime organized by relative structure width B/L.

Variables: `R` porous resistance force per volume; `mu` dynamic viscosity; `K` intrinsic permeability; `u` volume-averaged velocity; `rho` fluid density; `C_F` nonlinear inertial resistance coefficient

Source: (Losada 1995, [doi:10.1016/0378-3839(95)00013-5](https://doi.org/10.1016/0378-3839(95)00013-5))

### Darcy-Forchheimer porous resistance

$$
\mathbf{R}=-\frac{\mu}{K}\mathbf{u}-\rho\frac{C_F}{\sqrt{K}}|\mathbf{u}|\mathbf{u}
$$

Regime: Two-dimensional laminar exterior flow; porous-bed validation with porosity 0.39, grain diameter 0.55 cm, permeability 1.02e-8 m2, and nonlinear coefficient 0.51.

Variables: `R` porous resistance force per volume; `mu` dynamic viscosity; `K` intrinsic permeability; `u` volume-averaged velocity; `rho` fluid density; `C_F` nonlinear inertial resistance coefficient

Source: (Shao 2010, [doi:10.1016/j.coastaleng.2009.10.012](https://doi.org/10.1016/j.coastaleng.2009.10.012))

### Darcy-Forchheimer porous resistance

$$
\mathbf{R}=-\frac{\mu}{K}\mathbf{u}-\rho\frac{C_F}{\sqrt{K}}|\mathbf{u}|\mathbf{u}
$$

Regime: Two-dimensional particle simulations of porous dams, regular-wave attenuation over porous seabeds, and runup/overtopping at a porous-armored caisson.

Variables: `R` porous resistance force per volume; `mu` dynamic viscosity; `K` intrinsic permeability; `u` volume-averaged velocity; `rho` fluid density; `C_F` nonlinear inertial resistance coefficient

Source: (Akbari 2013, [doi:10.1016/j.coastaleng.2012.12.002](https://doi.org/10.1016/j.coastaleng.2012.12.002))

### Darcy-Forchheimer porous resistance

$$
\mathbf{R}=-\frac{\mu}{K}\mathbf{u}-\rho\frac{C_F}{\sqrt{K}}|\mathbf{u}|\mathbf{u}
$$

Regime: Two-dimensional uniform and multilayer porous media with benchmark U-tube, rockfill, solitary-wave, submerged-structure, and triangular-bar cases.

Variables: `R` porous resistance force per volume; `mu` dynamic viscosity; `K` intrinsic permeability; `u` volume-averaged velocity; `rho` fluid density; `C_F` nonlinear inertial resistance coefficient

Source: (Akbari 2014, [doi:10.1016/j.coastaleng.2014.03.004](https://doi.org/10.1016/j.coastaleng.2014.03.004))

### Darcy-Forchheimer porous resistance

$$
\mathbf{R}=-\frac{\mu}{K}\mathbf{u}-\rho\frac{C_F}{\sqrt{K}}|\mathbf{u}|\mathbf{u}
$$

Regime: Single- and multi-row porous cubic artificial reefs under nonbreaking regular waves over multiple submergence depths.

Variables: `R` porous resistance force per volume; `mu` dynamic viscosity; `K` intrinsic permeability; `u` volume-averaged velocity; `rho` fluid density; `C_F` nonlinear inertial resistance coefficient

Source: (Huang 2025, [doi:10.1016/j.coastaleng.2024.104688](https://doi.org/10.1016/j.coastaleng.2024.104688))

## Claims

- **C276.** For solitary-wave propagation over a porous bed with n=0.39, d=0.55 cm, K=1.02e-8 m2, and nonlinear resistance coefficient 0.51, an incompressible SPH model reproduced theoretical wave-height damping while coupling exterior Navier-Stokes and interior porous flow. *Regime: Two-dimensional laminar exterior flow; porous-bed validation with porosity 0.39, grain diameter 0.55 cm, permeability 1.02e-8 m2, and nonlinear coefficient 0.51..* [direct_finding, numerical] (Shao 2010, [doi:10.1016/j.coastaleng.2009.10.012](https://doi.org/10.1016/j.coastaleng.2009.10.012))
- **C277.** A unified ISPHP formulation using Navier-Stokes flow outside and extended Forchheimer resistance inside porous media agreed with laboratory free-surface displacement, overtopping rate, and pressure for porous-bed and armored-caisson applications. *Regime: Two-dimensional particle simulations of porous dams, regular-wave attenuation over porous seabeds, and runup/overtopping at a porous-armored caisson..* [direct_finding, numerical] (Akbari 2013, [doi:10.1016/j.coastaleng.2012.12.002](https://doi.org/10.1016/j.coastaleng.2012.12.002))
- **C278.** The modified moving-particle porous-flow method reproduced benchmark behavior across uniform and multilayer media, including rockfill seepage, solitary-wave attenuation over porous beds, submerged porous structures, and permeable triangular bars. *Regime: Two-dimensional uniform and multilayer porous media with benchmark U-tube, rockfill, solitary-wave, submerged-structure, and triangular-bar cases..* [direct_finding, numerical] (Akbari 2014, [doi:10.1016/j.coastaleng.2014.03.004](https://doi.org/10.1016/j.coastaleng.2014.03.004))
- **C279.** In an idealized porous coastal structure, relative width B/L controls the transition from irregular, higher-harmonic-rich flow with little dissipation to a transmission region dominated by frictional dissipation and filtering of higher frequencies. *Regime: Idealized porous structure under oscillatory waves; regime organized by relative structure width B/L..* [direct_finding, experimental] (Losada 1995, [doi:10.1016/0378-3839(95)00013-5](https://doi.org/10.1016/0378-3839(95)00013-5))
- **C280.** For single- and multi-row porous cubic reefs under nonbreaking regular waves, drag coefficients decreased with reef Keulegan-Carpenter number and horizontal drag work dominated dissipation, while vertical drag made a secondary contribution. *Regime: Single- and multi-row porous cubic artificial reefs under nonbreaking regular waves over multiple submergence depths..* [direct_finding, mixed] (Huang 2025, [doi:10.1016/j.coastaleng.2024.104688](https://doi.org/10.1016/j.coastaleng.2024.104688))
- **C1562.** Canopy layers control momentum and solute transport to and from the overlying water surface layer. *Regime: The study system, forcing, data and methods stated in the indexed abstract..* [direct_finding, mixed] (S. Rubol 2016, [doi:10.1002/2016wr018907](https://doi.org/10.1002/2016wr018907))
- **C1573.** This paper treats the numerical modelling of the behaviour of a sand core covered by rocks and exposed to waves. *Regime: The study system, forcing, data and methods stated in the indexed abstract..* [literature_review_statement, mixed] (Niels G. Jacobsen 2016, [doi:10.1016/j.coastaleng.2016.09.003](https://doi.org/10.1016/j.coastaleng.2016.09.003))
- **C1577.** Abstract The dynamic interaction between swash and beach groundwater is fundamental to understanding wave runup and sediment transport processes. *Regime: The study system, forcing, data and methods stated in the indexed abstract..* [literature_review_statement, mixed] (Marie‐Pierre C. Delisle 2023, [doi:10.1029/2022jc019615](https://doi.org/10.1029/2022jc019615))
- **C1583.** Wave scattering over porous structures plays an important role in the design of coastal and offshore protective structures. *Regime: The study system, forcing, data and methods stated in the indexed abstract..* [literature_review_statement, mixed] (Hima Manoj Kalathil 2026, [doi:10.1038/s41598-026-70631-1](https://doi.org/10.1038/s41598-026-70631-1))

## Papers

- Shao (2010). Incompressible SPH flow model for wave interactions with porous media. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2009.10.012](https://doi.org/10.1016/j.coastaleng.2009.10.012)
- Akbari (2013). Moving particle method for modeling wave interaction with porous structures. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2012.12.002](https://doi.org/10.1016/j.coastaleng.2012.12.002)
- Akbari (2014). Modified moving particle method for modeling wave interaction with multi layered porous structures. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2014.03.004](https://doi.org/10.1016/j.coastaleng.2014.03.004)
- Losada (1995). Experimental study of wave-induced flow in a porous structure. *Coastal Engineering*. [doi:10.1016/0378-3839(95)00013-5](https://doi.org/10.1016/0378-3839(95)00013-5)
- Huang (2025). Wave dissipation induced by flow interactions with porous artificial reefs. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2024.104688](https://doi.org/10.1016/j.coastaleng.2024.104688)
- Higuera (2014). Three-dimensional interaction of waves and porous coastal structures using OpenFOAM®. Part I: Formulation and validation. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2013.08.010](https://doi.org/10.1016/j.coastaleng.2013.08.010)
- S. Rubol (2016). Vertical dispersion in vegetated shear flows. *Water Resources Research*. [doi:10.1002/2016wr018907](https://doi.org/10.1002/2016wr018907)
- Niels G. Jacobsen (2016). Numerical modelling of the erosion and deposition of sand inside a filter layer. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2016.09.003](https://doi.org/10.1016/j.coastaleng.2016.09.003)
- Safak (2020). Wave transmission through living shoreline breakwalls. *Continental Shelf Research*. [doi:10.1016/j.csr.2020.104268](https://doi.org/10.1016/j.csr.2020.104268)
- Marie‐Pierre C. Delisle (2023). A Numerical Study of Dam‐Break Driven Swash and Beach Groundwater Interactions. *Journal of Geophysical Research Oceans*. [doi:10.1029/2022jc019615](https://doi.org/10.1029/2022jc019615)
- Rahman (2014). The Effect of Porosity of Submerged and Emerged Breakwater on Wave Transmission. *International Journal of Environmental Science and Development*. [doi:10.7763/ijesd.2014.v5.530](https://doi.org/10.7763/ijesd.2014.v5.530)
- Hima Manoj Kalathil (2026). A comparative study of wave scattering by a submerged porous breakwater in wall-bounded and unbounded domains. *Scientific Reports*. [doi:10.1038/s41598-026-70631-1](https://doi.org/10.1038/s41598-026-70631-1)
