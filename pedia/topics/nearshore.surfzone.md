# Surf-zone circulation

`nearshore.surfzone` | Wave-driven circulation within the surf zone.

Parent: [Nearshore hydrodynamics](nearshore.md)

Papers: 19. Claims: 15. Equations: 0.

## Synthesis

**Well established.** The surf zone transforms incident waves through shoaling, breaking, rollers, reflection, bottom friction, and nonlinear interactions. These processes drive setup, undertow, alongshore flow, turbulence, eddies, dispersion, and sediment transport.

**Governing physics.** Key controls are breaker type and location, wave height and period, directional spread, crest length, roller geometry, turbulence production and advection, vorticity cascades, undertow, bed roughness, slope, reflection, wind, and water depth.

**Dimensionless parameters.** Important groups include breaker index, Iribarren-type slope and steepness measures, relative depth, reflection coefficient, roller geometry and density, roughness ratio, directional spread, normalized dissipation, and eddy scale relative to surf-zone width.

**Major equations.** Frameworks use wave-energy and roller balances, hydraulic-jump dissipation, RANS or k-epsilon turbulence closures, Boussinesq phase-resolving equations, vortex-force circulation, Lagrangian dispersion statistics, and setup momentum balances.

**Typical methods.** Methods include dense drifter releases, LDA/ADV velocity profiles, field LiDAR rollers, storm arrays, phase-resolving Boussinesq models, vertical turbulence models, two-phase air-water RANS, Radon wave separation, and 3-D vortex-force circulation.

**Numerical models.** Models span wave-resolving Boussinesq dispersion, vertical k-epsilon circulation, phase-resolving reflection, roller dissipation, coupled three-dimensional vortex-force circulation, and air-water two-phase breaking with wind.

**Experimental datasets.** Evidence includes about 70 drifter releases, Duck94, a 4 s and 0.85 m large-scale barred-beach breaker at 12 stations, prototype BARDEXII reflection tests, LiDAR roller observations, and a shore-platform array from 10 m depth to shore.

**Validated ranges.** Reported regimes include Hs=0.5-1.4 m drifter days, 5-50 m observed eddies, 5-10 m enstrophy and 20-100 m inverse-cascade scales, undertow to 0.8 m/s, reflection-driven gamma changes to 40%, and roughness-driven setup contributions to 26%.

**Recent advances.** Recent advances directly measure roller geometry, resolve wave-by-wave reflection, observe scale-dependent drifter dispersion, quantify residual breaker-bar turbulence, and separate roughness effects on dissipation from circulation-driven setup.

**Disagreements.** Bulk or equilibrium closures can fail locally: roller-area formulae overestimated measured dissipation, log-profile stress inference fails when breaking homogenizes shear, and outgoing swash waves materially change wave ratios and undertow that incident-only analyses omit.

**Limitations.** Laboratory scale, two-dimensionality, fixed morphology, uncertain aeration and roller density, sparse vertical observations, wind and roughness parameterization, reflection separation, and intermittent directional breaking limit transfer.

**Open questions.** Needs include unified bubble-roller-turbulence energetics, three-dimensional breaking and cascades, morphology feedback, wind-wave-current coupling, rough natural platforms, reflection under random storms, and operational dispersion uncertainty.

**Seminal papers.** The branch connects bore and roller energy concepts, breaking turbulence closures, Boussinesq wave-resolving circulation, and Lagrangian dispersion theory; exact historical formulation lineage remains a full-text task.

## Claims

- **C462.** About 70 surf-zone drifter releases showed anisotropic time-dependent dispersion, 5-50 m eddies, relative dispersion proportional to time^(3/2), and scale-dependent diffusivity proportional to separation^(2/3). *Regime: alongshore-uniform beach within 200 m of shore and depths below 5 m; Hs=0.5 and 1.4 m.* [direct_finding, field] (Matthew S. Spydell 2007, [doi:10.1175/2007jpo3580.1](https://doi.org/10.1175/2007jpo3580.1))
- **C463.** A vertical turbulence model showed that breaking-wave turbulence substantially reduces surf-zone vertical shear, so fitting a logarithmic current profile can misestimate bottom stress even when mean alongshore flow is reproduced. *Regime: 4.5 m depth sandy beach and Duck94 cross-shore transect.* [direct_finding, numerical] (Falk Feddersen 2005, [doi:10.1175/jpo2800.1](https://doi.org/10.1175/jpo2800.1))
- **C464.** A Boussinesq model reproduced observed drifter dispersion through breaking-generated rotational flow, with an enstrophy cascade at about 5-10 m and inverse-energy cascade at 20-100 m that strengthened with wave directional spread. *Regime: uniform natural beach under small normally incident directionally spread waves.* [direct_finding, mixed] (Matthew S. Spydell 2008, [doi:10.1175/2008jpo3892.1](https://doi.org/10.1175/2008jpo3892.1))
- **C465.** In a large-scale barred-beach experiment, a 4 s, 0.85 m plunging wave generated undertow to 0.8 m/s, persistent turbulence reaching the bed, and undertow TKE transport about an order of magnitude larger than wave and turbulent fluxes. *Regime: T=4 s, H=0.85 m regular wave over fixed barred beach at 12 stations.* [direct_finding, experimental] (Dominic van der A 2017, [doi:10.1002/2016jc012072](https://doi.org/10.1002/2016jc012072))
- **C466.** For prototype-scale beaches steeper than 1:9, swash reflection changed individual wave-height-to-depth ratios by up to 25-40%, altered significant-wave ratios by 15%, strengthened undertow, and generated near-bed onshore streaming. *Regime: prototype-scale steep beach with tan(beta)>1:9 under regular and irregular waves.* [direct_finding, numerical] (Martins 2017, [doi:10.1016/j.coastaleng.2017.01.006](https://doi.org/10.1016/j.coastaleng.2017.01.006))
- **C467.** Direct LiDAR roller measurements showed that common roller-area formulations overestimate inner-surf-zone dissipation, which was close to but below an equal-height hydraulic jump and was better represented using roller-density effects. *Regime: broken waves in the inner surf zone.* [direct_finding, mixed] (Kévin Martins 2018, [doi:10.1029/2017jc013369](https://doi.org/10.1029/2017jc013369))
- **C468.** On a storm-exposed shore platform, bottom friction caused about 40% of wave dissipation, while roughness both reduced setup through prebreaking attenuation and increased circulation-driven setup by up to 26% on a 1:20 slope. *Regime: gently sloping shore platform instrumented from 10 m depth to shore.* [direct_finding, mixed] (Laura Lavaud 2022, [doi:10.1029/2021jf006466](https://doi.org/10.1029/2021jf006466))
- **C469.** Two-phase modelling over a 1:35 beach showed that wind increases vorticity and water-particle velocity and causes spilling and plunging waves to break earlier and farther seaward. *Regime: periodic breakers over a 1:35 beach with wind.* [direct_finding, numerical] (Zhihua Xie 2017, [doi:10.1007/s10236-017-1086-8](https://doi.org/10.1007/s10236-017-1086-8))
- **C1206.** Linear stability analysis shows radiation-stress-driven circulation can amplify crescentic surf-zone bed patterns, while allowing breaker-line displacement suppresses a giant-cusp mode but leaves crescentic growth largely unchanged. *Regime: A mechanism for the generation of wave‐driven rhythmic patterns in the surf zone.* [direct_finding, mixed] (Albert Falqués 2000, [doi:10.1029/2000jc900100](https://doi.org/10.1029/2000jc900100))
- **C1208.** On a reflective beach with 26–32 m cusps, meiofauna, macrofauna, zooplankton and fish distributions differed between horns, bays, rip-current margins and rip heads, linking circulation and morphology to habitat use. *Regime: Faunal response to morphology and water circulation of a sandy beach with cusps.* [direct_finding, mixed] (A. McLachlan 1984, [doi:10.3354/meps019133](https://doi.org/10.3354/meps019133))
- **C1212.** Validated SPH simulations show intersecting short-crested waves generate undertow, rip currents, isolated breaking crests, multiple low-frequency circulation cells and three-dimensional vorticity under both discrete and directional wavefields. *Regime: Short‐crested waves in the surf zone.* [direct_finding, mixed] (Zhangping Wei 2017, [doi:10.1002/2016jc012485](https://doi.org/10.1002/2016jc012485))
- **C1213.** WAMFlow optical processing resolved kilometre-alongshore surf-zone currents and captured longshore flows, rips and gyres; filtered velocities had about 0.1 m/s RMSE against drifters. *Regime: Quantifying Optically Derived Two-Dimensional Wave-Averaged Currents in the Surf Zone.* [direct_finding, mixed] (Dylan Anderson 2021, [doi:10.3390/rs13040690](https://doi.org/10.3390/rs13040690))
- **C1217.** A calibrated Sète model found breakwater-edge differential breaking drove 0.4 m/s circulation and suppressed inner-bar rip-channel development and offshore bar transport in the lee; longshore current RMSE was 0.07 m/s. *Regime: Modeling the Impact of the Implementation of a Submerged Structure on Surf Zone Sandbar Dynamics.* [direct_finding, mixed] (Clément Bouvier 2019, [doi:10.3390/jmse7040117](https://doi.org/10.3390/jmse7040117))
- **C1618.** A time-averaged surf-zone model using roller-inclusive approximations for energy flux, radiation stress and dissipation reproduces measured wave-height and mean-water-level setup and interprets the post-breaking transition through shoreward roller transport. *Regime: Regular breaking waves and the laboratory surf-zone measurements evaluated in the article..* [direct_finding, analytical] (Svendsen 1984, [doi:10.1016/0378-3839(84)90028-0](https://doi.org/10.1016/0378-3839(84)90028-0))
- **C1643.** A wave-current interaction review finds mean bed shear may increase, decrease or remain unchanged depending on nonlinear interaction, relaminarization or linear superposition; non-collinear waves can rotate currents with depth, while common eddy-viscosity and URANS models remain weakly validated outside near-bed regions. *Regime: Turbulent wave-current interaction in nearshore boundary layers, including collinear and oblique forcing..* [literature_review_statement, review] (Xuan Zhang 2021, [doi:10.1016/j.oceaneng.2021.110202](https://doi.org/10.1016/j.oceaneng.2021.110202))

## Papers

- Svendsen (1984). Wave heights and set-up in a surf zone. *Coastal Engineering*. [doi:10.1016/0378-3839(84)90028-0](https://doi.org/10.1016/0378-3839(84)90028-0)
- Albert Falqués (2000). A mechanism for the generation of wave‐driven rhythmic patterns in the surf zone. *Journal of Geophysical Research: Oceans*. [doi:10.1029/2000jc900100](https://doi.org/10.1029/2000jc900100)
- Matthew S. Spydell (2007). Observing Surf-Zone Dispersion with Drifters. *Journal of Physical Oceanography*. [doi:10.1175/2007jpo3580.1](https://doi.org/10.1175/2007jpo3580.1)
- Falk Feddersen (2005). The Effect of Wave Breaking on Surf-Zone Turbulence and Alongshore Currents: A Modeling Study*. *Journal of Physical Oceanography*. [doi:10.1175/jpo2800.1](https://doi.org/10.1175/jpo2800.1)
- Matthew S. Spydell (2008). Lagrangian Drifter Dispersion in the Surf Zone: Directionally Spread, Normally Incident Waves. *Journal of Physical Oceanography*. [doi:10.1175/2008jpo3892.1](https://doi.org/10.1175/2008jpo3892.1)
- Xuan Zhang (2021). A review of the state of research on wave-current interaction in nearshore areas. *Ocean Engineering*. [doi:10.1016/j.oceaneng.2021.110202](https://doi.org/10.1016/j.oceaneng.2021.110202)
- A. McLachlan (1984). Faunal response to morphology and water circulation of a sandy beach with cusps. *Marine Ecology Progress Series*. [doi:10.3354/meps019133](https://doi.org/10.3354/meps019133)
- Dominic van der A (2017). Large‐scale laboratory study of breaking wave hydrodynamics over a fixed bar. *Journal of Geophysical Research Oceans*. [doi:10.1002/2016jc012072](https://doi.org/10.1002/2016jc012072)
- Martins (2017). The influence of swash-based reflection on surf zone hydrodynamics: a wave-by-wave approach. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2017.01.006](https://doi.org/10.1016/j.coastaleng.2017.01.006)
- Kévin Martins (2018). Energy Dissipation in the Inner Surf Zone: New Insights From Li <scp>DAR</scp> ‐Based Roller Geometry Measurements. *Journal of Geophysical Research Oceans*. [doi:10.1029/2017jc013369](https://doi.org/10.1029/2017jc013369)
- Zhangping Wei (2017). Short‐crested waves in the surf zone. *Journal of Geophysical Research: Oceans*. [doi:10.1002/2016jc012485](https://doi.org/10.1002/2016jc012485)
- Dylan Anderson (2021). Quantifying Optically Derived Two-Dimensional Wave-Averaged Currents in the Surf Zone. *Remote Sensing*. [doi:10.3390/rs13040690](https://doi.org/10.3390/rs13040690)
- Zhihua Xie (2017). Numerical modelling of wind effects on breaking waves in the surf zone. *Ocean Dynamics*. [doi:10.1007/s10236-017-1086-8](https://doi.org/10.1007/s10236-017-1086-8)
- Clément Bouvier (2019). Modeling the Impact of the Implementation of a Submerged Structure on Surf Zone Sandbar Dynamics. *Journal of Marine Science and Engineering*. [doi:10.3390/jmse7040117](https://doi.org/10.3390/jmse7040117)
- Laura Lavaud (2022). Wave Dissipation and Mean Circulation on a Shore Platform Under Storm Wave Conditions. *Journal of Geophysical Research: Earth Surface*. [doi:10.1029/2021jf006466](https://doi.org/10.1029/2021jf006466)
- Philip D. Osborne (1992). Frequency dependent cross-shore suspended sediment transport. 1. A non-barred shoreface. *Marine Geology*. [doi:10.1016/0025-3227(92)90052-j](https://doi.org/10.1016/0025-3227(92)90052-j)
- Àngels Fernández-Mora (2015). Onshore sandbar migration in the surf zone: New insights into the wave‐induced sediment transport mechanisms. *Geophysical Research Letters*. [doi:10.1002/2014gl063004](https://doi.org/10.1002/2014gl063004)
- Troels Aagaard (2002). Cross-shore suspended sediment transport in the surf zone: a field-based parameterization. *Marine Geology*. [doi:10.1016/s0025-3227(02)00193-7](https://doi.org/10.1016/s0025-3227(02)00193-7)
- Brian Greenwood (1990). Vertical and horizontal structure in cross-shore flows: An example of undertow and wave set-up on a barred beach. *Coastal Engineering*. [doi:10.1016/0378-3839(90)90034-t](https://doi.org/10.1016/0378-3839(90)90034-t)
