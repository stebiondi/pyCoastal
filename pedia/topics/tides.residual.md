# Residual circulation

`tides.residual` | Tidally averaged transport.

Parent: [Tides and coastal circulation](tides.md)

Papers: 12. Claims: 10. Equations: 5.

## Synthesis

**Well established.** Residual circulation is the nonzero flow and transport remaining after tidal averaging. In estuaries and inlets it commonly reflects density-driven exchange, nonlinear tidal asymmetry, freshwater input, mixing, and geometry rather than the oscillatory tide alone.

**Governing physics.** Longitudinal baroclinic pressure gradients drive exchange flow, while vertical and lateral mixing, tidally averaged advection, sills, constrictions, basin interconnection, river discharge, and ebb-flood asymmetry set its magnitude and vertical or lateral structure.

**Dimensionless parameters.** Important controls include Rayleigh number, Fischer number, the lateral-advection parameter, depth-to-width aspect ratio, ratios of lateral to vertical mixing, and comparisons between cross-sectional mixing time and the tidal averaging interval.

**Major equations.** The reviewed frameworks use tidally averaged momentum and salt conservation, advection-diffusion equations, Hansen-Rattray/Pritchard exchange-flow theory, one-dimensional gradient-dispersion closure, and two- or three-dimensional numerical mass and momentum balances.

**Typical methods.** Evidence combines current, water-level, salinity and water-quality observations with analytical reduction, nondimensional regime analysis, breadth-averaged finite differences, and calibrated three-dimensional unstructured-grid modeling.

**Numerical models.** Models span one-dimensional tidally averaged dispersion, idealized Hansen-Rattray inlet circulation, multilevel breadth-averaged vertical-plane transport, and three-dimensional unstructured-grid Puget Sound circulation.

**Experimental datasets.** Key evidence includes multi-station observations across Gazi Bay, historical and 2006 Puget Sound velocity-salinity profiles, Oosterschelde salinity and velocity distributions, and Gulf of Khambhat hydrodynamic and transport information.

**Validated ranges.** Validated or demonstrated regimes range from 3-4 h residence and 60-90% exchange per tide in shallow Gazi Bay to fjordal and partially mixed Puget Sound sub-basins; analytical results also cover constant-section inlets and mixing/advection regimes defined by nondimensional parameters.

**Recent advances.** Recent analytical work shows that lateral mixing and tidally averaged advection fundamentally control gravitational exchange through Fischer and advection parameters, including a negative feedback in which stronger advection suppresses its driving lateral salinity gradients.

**Disagreements.** There is no single transferable closure: simple analytical exchange models can reveal controls but require site-specific parameterization in complex sill-basin systems, while gradient-dispersion closure fails when averaging is too short relative to cross-sectional mixing or residual cells dominate dispersion.

**Limitations.** Tidal averaging can conceal intratidal covariance and asymmetry. Breadth or section averaging suppresses lateral structure, idealized constant geometry limits inlet solutions, and calibrated three-dimensional models remain sensitive to bathymetry, mixing closure, boundaries, and sparse long-term observations.

**Open questions.** Priority questions concern interactions among tides, stratification, wind, waves, river flow and morphology; transfer of mixing closures across sites; spring-neap and seasonal modulation; and uncertainty in translating Eulerian residual flow into net material transport and residence time.

**Seminal papers.** The 1978 high-Rayleigh inlet solution and 1982 conditions for gradient-type tidally averaged dispersion provide early analytical foundations; the Gazi Bay and Puget Sound studies anchor field and multi-model evidence.

## Equations

### Hansen-Rattray coastal-plain estuary model

$$
\overline{\mathbf{u}}=f(\nabla \overline{S},K_m,K_s,Q_r,\mathcal{G},T)
$$

Regime: Idealized constant-width, constant-depth coastal inlets using Pritchard/Hansen-Rattray equations; numerical solutions without the earlier Rayleigh-number restriction.

Variables: `u_bar` tidally averaged velocity; `S_bar` mean salinity; `K_m` momentum mixing coefficient; `K_s` salt mixing coefficient; `Q_r` river discharge; `G` geometry and bathymetry; `T` tidal forcing; normalized dependency statement, not a recovered coefficient equation

Source: (Muralikrishna 1978, [doi:10.1016/0378-3839(78)90011-x](https://doi.org/10.1016/0378-3839(78)90011-x))

### FVCOM

$$
\overline{\mathbf{u}}=f(\nabla \overline{S},K_m,K_s,Q_r,\mathcal{G},T)
$$

Regime: Fjordal and partially mixed Puget Sound sub-basins; comparison to historical composite profiles and 2006 observations; year-long numerical application.

Variables: `u_bar` tidally averaged velocity; `S_bar` mean salinity; `K_m` momentum mixing coefficient; `K_s` salt mixing coefficient; `Q_r` river discharge; `G` geometry and bathymetry; `T` tidal forcing; normalized dependency statement, not a recovered coefficient equation

Source: (Khangaonkar 2011, [doi:10.1016/j.ecss.2011.04.016](https://doi.org/10.1016/j.ecss.2011.04.016))

### one-dimensional tidally averaged advection-dispersion model

$$
\overline{\mathbf{u}}=f(\nabla \overline{S},K_m,K_s,Q_r,\mathcal{G},T)
$$

Regime: One-dimensional cross-sectionally and tidally averaged transport, illustrated with Oosterschelde salinity and velocity observations.

Variables: `u_bar` tidally averaged velocity; `S_bar` mean salinity; `K_m` momentum mixing coefficient; `K_s` salt mixing coefficient; `Q_r` river discharge; `G` geometry and bathymetry; `T` tidal forcing; normalized dependency statement, not a recovered coefficient equation

Source: (Dronkers 1982, [doi:10.1016/s0302-3524(82)80002-9](https://doi.org/10.1016/s0302-3524(82)80002-9))

### three-dimensional tidally averaged estuarine circulation model

$$
\overline{\mathbf{u}}=f(\nabla \overline{S},K_m,K_s,Q_r,\mathcal{G},T)
$$

Regime: Idealized steady gravitational estuarine circulation with lateral transport; regimes organized by Fischer number and advection parameter.

Variables: `u_bar` tidally averaged velocity; `S_bar` mean salinity; `K_m` momentum mixing coefficient; `K_s` salt mixing coefficient; `Q_r` river discharge; `G` geometry and bathymetry; `T` tidal forcing; normalized dependency statement, not a recovered coefficient equation

Source: (Tobias Kukulka 2025, [doi:10.1175/jpo-d-24-0158.1](https://doi.org/10.1175/jpo-d-24-0158.1))

### multilevel breadth-averaged circulation-transport model

$$
\overline{\mathbf{u}}=f(\nabla \overline{S},K_m,K_s,Q_r,\mathcal{G},T)
$$

Regime: Gulf of Khambhat, approximately 3120 km2; breadth-averaged vertical-plane representation.

Variables: `u_bar` tidally averaged velocity; `S_bar` mean salinity; `K_m` momentum mixing coefficient; `K_s` salt mixing coefficient; `Q_r` river discharge; `G` geometry and bathymetry; `T` tidal forcing; normalized dependency statement, not a recovered coefficient equation

Source: (Jena 2008, [doi:10.2112/05-0496.1](https://doi.org/10.2112/05-0496.1))

## Claims

- **C265.** In shallow Gazi Bay, a wide unrestricted entrance enabled 60-90% volume exchange per tidal cycle and 3-4 h residence times, while ebb-dominant mangrove-creek currents promoted net export toward seagrass beds. *Regime: Shallow semi-enclosed Gazi Bay; mangrove creeks, seagrass beds, and coral-reef zone; observed currents about 0.6 m/s in creeks and below 0.30 m/s offshore..* [direct_finding, field] (Kitheka 1997, [doi:10.1006/ecss.1996.0189](https://doi.org/10.1006/ecss.1996.0189))
- **C266.** Across Puget Sound sub-basins, residual two-layer circulation depends on sills and basin geometry plus freshwater-driven salinity gradients; a calibrated 3-D unstructured-grid model reproduced observed inter-basin velocity and salinity-profile differences that a simple analytical model required site-specific parameters to represent. *Regime: Fjordal and partially mixed Puget Sound sub-basins; comparison to historical composite profiles and 2006 observations; year-long numerical application..* [direct_finding, mixed] (Khangaonkar 2011, [doi:10.1016/j.ecss.2011.04.016](https://doi.org/10.1016/j.ecss.2011.04.016))
- **C267.** Gradient-type dispersion in a one-dimensional tidally averaged estuary model is justified when the averaging interval, measured in tidal periods, exceeds the cross-sectional mixing timescale; the requirement can be weaker when residual vertical or horizontal circulations do not dominate dispersion. *Regime: One-dimensional cross-sectionally and tidally averaged transport, illustrated with Oosterschelde salinity and velocity observations..* [direct_finding, mixed] (Dronkers 1982, [doi:10.1016/s0302-3524(82)80002-9](https://doi.org/10.1016/s0302-3524(82)80002-9))
- **C268.** Tidally averaged gravitational estuarine circulation depends on both the Fischer number and a lateral-advection parameter; as advection strengthens it suppresses the lateral salinity gradients driving lateral flow, producing a negative feedback that approaches a limiting exchange-flow structure. *Regime: Idealized steady gravitational estuarine circulation with lateral transport; regimes organized by Fischer number and advection parameter..* [direct_finding, analytical] (Tobias Kukulka 2025, [doi:10.1175/jpo-d-24-0158.1](https://doi.org/10.1175/jpo-d-24-0158.1))
- **C269.** A fully nonlinear multilevel breadth-averaged model using a semi-explicit finite-difference scheme jointly represented tidal circulation, salinity intrusion, and suspended-sediment transport in the Gulf of Khambhat, subject to the limitations of a vertical-plane breadth average. *Regime: Gulf of Khambhat, approximately 3120 km2; breadth-averaged vertical-plane representation..* [direct_finding, numerical] (Jena 2008, [doi:10.2112/05-0496.1](https://doi.org/10.2112/05-0496.1))
- **C270.** In an idealized constant-width and constant-depth coastal inlet, increasing Rayleigh number strengthens vertical advection, homogenizes salinity within the upper and lower layers, and sharpens a halocline near mid-depth. *Regime: Idealized constant-width, constant-depth coastal inlets using Pritchard/Hansen-Rattray equations; numerical solutions without the earlier Rayleigh-number restriction..* [direct_finding, analytical] (Muralikrishna 1978, [doi:10.1016/0378-3839(78)90011-x](https://doi.org/10.1016/0378-3839(78)90011-x))
- **C1243.** At Paopao Bay, weak tides near amphidromic points allowed episodic wave setup to dominate reef–lagoon exchange; the inferred capture width was about 2.3 km and large waves suppressed two-layer pass exchange. *Regime: Episodic circulation and exchange in a wave‐driven coral reef and lagoon system.* [direct_finding, mixed] (James L. Hench 2008, [doi:10.4319/lo.2008.53.6.2681](https://doi.org/10.4319/lo.2008.53.6.2681))
- **C1248.** A 5′ Sea of Okhotsk model found over 60% of diurnal tidal energy dissipated in Shelikhov Bay and Penzhinskaya Guba, while nonlinear diurnal interaction over Kashevarov Bank generated residual flow near 10 cm/s and much of local M2 current. *Regime: Tides in the Sea of Okhotsk.* [direct_finding, mixed] (Zygmunt Kowalik 1998, [doi:10.1175/1520-0485(1998)028<1389:titsoo>2.0.co;2](https://doi.org/10.1175/1520-0485(1998)028<1389:titsoo>2.0.co;2))
- **C1249.** A Changjiang review finds tides, bathymetry, discharge, winds and remote shelf currents jointly control momentum, freshwater pathways, plume expansion and cross-shelf exchange, with seasonally reversing coastal circulation. *Regime: Advances on Coastal and Estuarine Circulations Around the Changjiang Estuary in the Recent Decades (2000–2020).* [direct_finding, mixed] (Zhiqiang Liu 2021, [doi:10.3389/fmars.2021.615929](https://doi.org/10.3389/fmars.2021.615929))
- **C1534.** Abstract Tidal rivers are a vital and little studied nexus between physical oceanography and hydrology. *Regime: The study system, forcing, data and methods stated in the indexed abstract..* [literature_review_statement, mixed] (A.J.F. Hoitink 2016, [doi:10.1002/2015rg000507](https://doi.org/10.1002/2015rg000507))

## Papers

- James L. Hench (2008). Episodic circulation and exchange in a wave‐driven coral reef and lagoon system. *Limnology and Oceanography*. [doi:10.4319/lo.2008.53.6.2681](https://doi.org/10.4319/lo.2008.53.6.2681)
- Zygmunt Kowalik (1998). Tides in the Sea of Okhotsk. *Journal of Physical Oceanography*. [doi:10.1175/1520-0485(1998)028<1389:titsoo>2.0.co;2](https://doi.org/10.1175/1520-0485(1998)028<1389:titsoo>2.0.co;2)
- Kitheka (1997). Coastal Tidally-driven Circulation and the Role of Water Exchange in the Linkage Between Tropical Coastal Ecosystems. *Estuarine, Coastal and Shelf Science*. [doi:10.1006/ecss.1996.0189](https://doi.org/10.1006/ecss.1996.0189)
- Khangaonkar (2011). Tidally averaged circulation in Puget Sound sub-basins: Comparison of historical data, analytical model, and numerical model. *Estuarine, Coastal and Shelf Science*. [doi:10.1016/j.ecss.2011.04.016](https://doi.org/10.1016/j.ecss.2011.04.016)
- Zhiqiang Liu (2021). Advances on Coastal and Estuarine Circulations Around the Changjiang Estuary in the Recent Decades (2000–2020). *Frontiers in Marine Science*. [doi:10.3389/fmars.2021.615929](https://doi.org/10.3389/fmars.2021.615929)
- Dronkers (1982). Conditions for gradient-type dispersive transport in one-dimensional, tidally averaged transport models. *Estuarine, Coastal and Shelf Science*. [doi:10.1016/s0302-3524(82)80002-9](https://doi.org/10.1016/s0302-3524(82)80002-9)
- Tobias Kukulka (2025). Tidally Averaged Models of the Gravitationally Driven Estuarine Circulation with Lateral Transport. *Journal of Physical Oceanography*. [doi:10.1175/jpo-d-24-0158.1](https://doi.org/10.1175/jpo-d-24-0158.1)
- Jena (2008). A Breadth-Averaged Model for Tidal Circulation and Sediment Transport in the Gulf of Khambhat, West Coast of India. *Journal of Coastal Research*. [doi:10.2112/05-0496.1](https://doi.org/10.2112/05-0496.1)
- Muralikrishna (1978). Circulation and salinity distribution in coastal inlets. *Coastal Engineering*. [doi:10.1016/0378-3839(78)90011-x](https://doi.org/10.1016/0378-3839(78)90011-x)
- A.J.F. Hoitink (2016). Tidal river dynamics: Implications for deltas. *Reviews of Geophysics*. [doi:10.1002/2015rg000507](https://doi.org/10.1002/2015rg000507)
- Casella (2020). Coastal Current Intrusions from Satellite Altimetry. *Remote Sensing*. [doi:10.3390/rs12223686](https://doi.org/10.3390/rs12223686)
- Liu (2024). A theoretical model for wave attenuation by vegetation considering current effects. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2024.104508](https://doi.org/10.1016/j.coastaleng.2024.104508)
