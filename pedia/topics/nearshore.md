# Nearshore hydrodynamics

`nearshore` | Currents and water-level dynamics in the nearshore zone.

Subtopics: [Infragravity motions](nearshore.infragravity.md), [Longshore currents](nearshore.longshore.md), [Rip currents](nearshore.rips.md), [Surf-zone circulation](nearshore.surfzone.md)

Papers: 15. Claims: 1. Equations: 0.

## Synthesis

**Well established.** Breaking-wave momentum gradients drive setup, undertow, longshore currents, rip cells and vortices. Bathymetry redirects those currents, which in turn transport sediment, tracers and organisms and reshape the bed, producing strongly coupled and often nonstationary nearshore dynamics.

**Governing physics.** Radiation-stress and pressure gradients, wave mass transport, return flow, bottom friction, wave–current interaction, vorticity generation and turbulent mixing govern circulation. Directional waves, tides, headlands, reefs, bars and channels alter forcing and connectivity.

**Dimensionless parameters.** Controls include Froude and Reynolds numbers, wave steepness, relative depth, surf similarity, current-to-wave speed ratio, rip spacing relative to surf width, trough area and onshore discharge, directional spread, normalized headland/reef geometry and dispersion scaling.

**Major equations.** Depth-integrated mass and momentum balances include wave forcing, pressure, advection and bottom stress; wave action or phase-resolving equations provide breaking and radiation stress. Sediment continuity closes morphology feedback, while Lagrangian transport diagnoses exchange and dispersion.

**Typical methods.** Studies combine current meters, pressure sensors, scanning sonar, drifters, dye/turbidity, imagery and bathymetry with field or basin experiments; wave-averaged, stability, SPH and morphodynamic models test forcing and feedback. Eulerian and Lagrangian observations should be reconciled.

**Numerical models.** Representations range from depth-averaged circulation and radiation-stress models to linear morphology stability, mesh-free SPH, O(1 m) event hindcasts and coupled bar models. Phase-averaged models capture mean cells but may need explicit unsteadiness or vorticity closures.

**Experimental datasets.** Reviewed evidence includes Scripps scanning-sonar rips, longshore-uniform swell-beach drifters, dense laboratory rip trajectories, a Lake Michigan meteotsunami reconstruction, large-scale short-crested-wave validation, WAMFlow imagery, a three-week headland experiment and four North Sea campaigns.

**Validated ranges.** Case values include episodic and headland rip speeds near 0.7 m/s, WAMFlow RMSE near 0.1 m/s, submerged-structure longshore RMSE 0.07 m/s and transient rip-neck widths 20–30 m. These are site-specific measurements and validation metrics, not universal thresholds.

**Recent advances.** Recent advances use kilometre-scale optical velocimetry, dense Lagrangian arrays, high-resolution forensic hindcasts, mesh-free three-dimensional breaking simulations and coupled structure–bar models to resolve circulation modes missed by sparse instruments.

**Disagreements.** Rips may be bathymetrically controlled, transient without fixed channels, forced by directional breaking, or triggered by meteotsunamis. Mean-cell descriptions can understate intermittent exchange, and drifter velocities can differ from Eulerian flow because of Stokes drift and sampling concentration.

**Limitations.** Sparse spatial sampling, rapidly evolving bars, optical visibility, wave breaking complexity, unmeasured vertical structure, uncertain friction, scale effects and short experiments limit transfer. A model matching mean currents may still miss vortices, dispersion or hazard onset.

**Open questions.** Priorities include transient-rip predictability, compound meteotsunami and wave hazards, vertical exchange, directional spectra, morphology coevolution, headland transport beyond closure, real-time remote sensing, data assimilation and public-warning thresholds.

**Seminal papers.** Radiation-stress theory connected breaking waves to setup and mean currents; early surf-zone observations established undertow, longshore and rip cells. Morphodynamic stability theory then formalized feedback with bed patterns, while drifters and imaging exposed strong unsteadiness.

## Claims

- **C1214.** Nearshore hydrodynamics requires spatially resolved observation of nonstationary wave-averaged currents because fixed instruments can miss interacting rips, longshore currents and gyres tied to evolving morphology. *Regime: Image-visible surf-zone surface circulation at the study sites..* [direct_finding, field] (Dylan Anderson 2021, [doi:10.3390/rs13040690](https://doi.org/10.3390/rs13040690))

## Papers

- Harry Teagle (2017). The role of kelp species as biogenic habitat formers in coastal marine ecosystems. *Journal of Experimental Marine Biology and Ecology*. [doi:10.1016/j.jembe.2017.01.017](https://doi.org/10.1016/j.jembe.2017.01.017)
- Laura Airoldi (2005). An ecological perspective on the deployment and design of low-crested and other hard coastal defence structures. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2005.09.007](https://doi.org/10.1016/j.coastaleng.2005.09.007)
- Albert Falqués (2000). A mechanism for the generation of wave‐driven rhythmic patterns in the surf zone. *Journal of Geophysical Research: Oceans*. [doi:10.1029/2000jc900100](https://doi.org/10.1029/2000jc900100)
- Johnson (2004). Transient rip currents and nearshore circulation on a swell‐dominated beach. *Journal of Geophysical Research: Oceans*. [doi:10.1029/2003jc001798](https://doi.org/10.1029/2003jc001798)
- Smith (1995). Observations of nearshore circulation: Rip currents. *Journal of Geophysical Research: Oceans*. [doi:10.1029/95jc00751](https://doi.org/10.1029/95jc00751)
- A. McLachlan (1984). Faunal response to morphology and water circulation of a sandy beach with cusps. *Marine Ecology Progress Series*. [doi:10.3354/meps019133](https://doi.org/10.3354/meps019133)
- Álvaro Linares (2019). Unexpected rip currents induced by a meteotsunami. *Scientific Reports*. [doi:10.1038/s41598-019-38716-2](https://doi.org/10.1038/s41598-019-38716-2)
- Zhangping Wei (2017). Short‐crested waves in the surf zone. *Journal of Geophysical Research: Oceans*. [doi:10.1002/2016jc012485](https://doi.org/10.1002/2016jc012485)
- Andrew B. Kennedy (2004). Drifter measurements in a laboratory rip current. *Journal of Geophysical Research: Oceans*. [doi:10.1029/2003jc001927](https://doi.org/10.1029/2003jc001927)
- Dylan Anderson (2021). Quantifying Optically Derived Two-Dimensional Wave-Averaged Currents in the Surf Zone. *Remote Sensing*. [doi:10.3390/rs13040690](https://doi.org/10.3390/rs13040690)
- Vasileios Kitsikoudis (2020). Experimental analysis of flow and turbulence in the wake of neighboring emergent vegetation patches with different densities. *Environmental Fluid Mechanics*. [doi:10.1007/s10652-020-09746-6](https://doi.org/10.1007/s10652-020-09746-6)
- Arthur Mouragues (2020). High‐Energy Surf Zone Currents and Headland Rips at a Geologically Constrained Mesotidal Beach. *Journal of Geophysical Research: Oceans*. [doi:10.1029/2020jc016259](https://doi.org/10.1029/2020jc016259)
- Clément Bouvier (2019). Modeling the Impact of the Implementation of a Submerged Structure on Surf Zone Sandbar Dynamics. *Journal of Marine Science and Engineering*. [doi:10.3390/jmse7040117](https://doi.org/10.3390/jmse7040117)
- Troels Aagaard (2008). Cross-Shore Currents in the Surf Zone: Rips or Undertow?. *Journal of Coastal Research*. [doi:10.2112/04-0357.1](https://doi.org/10.2112/04-0357.1)
- Alistair G.L. Borthwick (2002). Wave-induced nearshore currents at a tri-cuspate beach in the UKCRF. *Proceedings of the Institution of Civil Engineers - Water and Maritime Engineering*. [doi:10.1680/wame.2002.154.4.251](https://doi.org/10.1680/wame.2002.154.4.251)
