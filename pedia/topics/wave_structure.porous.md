# Porous structures

`wave_structure.porous` | Flow and waves through porous media.

Parent: [Wave-structure interaction](wave_structure.md)

Subtopics: [Porous-flow resistance](wave_structure.porous.resistance.md), [Transmission through porous structures](wave_structure.porous.transmission.md)

Papers: 19. Claims: 19. Equations: 0.

Used by pyCoastal design modules: Breakwater design.

## Synthesis

**Well established.** Porous coastal structures redistribute incident wave energy among reflection, transmission and dissipation through pressure-driven flow in connected voids; both viscous and inertial resistance matter.

**Governing physics.** Pressure gradients drive oscillatory pore flow. Viscous drag dominates low pore Reynolds number, inertial and turbulent losses grow with velocity, and geometry couples exterior waves to internal flow, phase lag, attenuation and forces.

**Dimensionless parameters.** Controls include porosity, permeability, pore Reynolds and Keulegan–Carpenter numbers, relative width and depth, wave steepness, submergence, incidence angle, layer count, resistance coefficients, current ratio and structure spacing.

**Major equations.** Macroscopic models use volume-averaged Navier–Stokes or RANS equations with porosity and Darcy–Forchheimer or Van Gent resistance; alternatives include Brinkman, Sollitt–Cross, eigenfunction matching, VOF and porous-media SPH formulations.

**Typical methods.** Methods combine flume tests, field reflection monitoring, analytical scattering solutions, VARANS–VOF CFD, SPH, volume-averaged floating-body models, resistance sensitivity studies and data-driven parameter calibration or surrogates.

**Numerical models.** The branch includes Navier–Stokes–Brinkman, VARANS–VOF/OpenFOAM, weakly compressible SPH mixture theory, eigenfunction matching, Sollitt–Cross theory, depth-averaged porous-barrier solutions and neural or surrogate calibration frameworks.

**Experimental datasets.** Evidence spans submerged permeable slopes and blocks, vertical screens and perforated plates, multilayer rubble or trapezoidal breakwaters, floating porous bodies, wall-adjacent traps, rubble-mound overtopping cases and a year-long Chabahar field record.

**Validated ranges.** Validation covers regular, irregular, solitary and oblique waves; thin perforated elements and thick porous zones; fixed, submerged and floating geometries; single and multilayer structures; and cases with current, uneven bottom or nearby walls.

**Recent advances.** Recent work adds SPH mixture formulations, porous floating structures, current-modified trapping, nonlinear submerged-breakwater tests, machine-learned resistance calibration and fast surrogate-assisted porous CFD.

**Disagreements.** Equivalent porous coefficients are formulation-dependent: depth-averaging choices, unresolved evanescent modes, thin-screen versus volumetric representations and alternative inertial-drag laws can reproduce one observable while differing internally.

**Limitations.** Porous coefficients often require case calibration, internal velocity and pressure data are sparse, scale effects alter viscous and turbulent losses, and many validations remain two-dimensional or regular-wave based.

**Open questions.** Transferable resistance closure, uncertainty quantification, irregular and directional seas, evolving/damaged grading, air entrainment, three-dimensional edge effects, fluid–structure motion and coupling to overtopping and sediment remain open.

**Seminal papers.** Brinkman and Sollitt–Cross formulations established macroscopic porous-wave theory; later volume-averaged RANS and VOF methods enabled nonlinear free-surface interaction with realistic breakwater geometries.

## Claims

- **C884.** Depth-averaged pressure-drop formulations for a vertical porous barrier give analytical reflection and transmission solutions whose accuracy depends on the treatment of evanescent modes and porous resistance. *Regime: Comparison of analytical and numerical solutions for wave interaction with a vertical porous barrier.* [direct_finding, analytical] (Ed Mackay 2020, [doi:10.1016/j.oceaneng.2020.107032](https://doi.org/10.1016/j.oceaneng.2020.107032))
- **C885.** Dimensional analysis and experiments show that permeability changes wave reflection, runup, internal flow and energy dissipation relative to impermeable slopes. *Regime: 2D water-wave interaction with permeable and impermeable slopes: Dimensional analysis and experimental overview.* [direct_finding, mixed] (Pilar Díaz-Carrasco 2020, [doi:10.1016/j.coastaleng.2020.103682](https://doi.org/10.1016/j.coastaleng.2020.103682))
- **C886.** A volumetric porous-zone CFD representation can reproduce wave interaction with thin perforated sheets and cylinders without explicitly resolving every opening. *Regime: Using a porous-media approach for CFD modelling of wave interaction with thin perforated structures.* [direct_finding, numerical] (Anna Feichtner 2020, [doi:10.1007/s40722-020-00183-7](https://doi.org/10.1007/s40722-020-00183-7))
- **C887.** VARANS–VOF simulation resolves solitary-wave transformation and flow around a permeable submerged breakwater. *Regime: Numerical Simulation of Solitary Wave Induced Flow Motion around a Permeable Submerged Breakwater.* [direct_finding, numerical] (Jisheng Zhang 2012, [doi:10.1155/2012/508754](https://doi.org/10.1155/2012/508754))
- **C888.** A derived Navier–Stokes–Brinkman system represents viscous progressive-wave interaction with a submerged rectangular porous breakwater. *Regime: Navier-Stokes-Brinkman system for interaction of viscous waves with a submerged porous structure.* [direct_finding, analytical] (Lemi Guta 2010, [doi:10.5556/j.tkjm.41.2010.722](https://doi.org/10.5556/j.tkjm.41.2010.722))
- **C889.** A volume-averaged model resolves wave interaction with a movable floating porous structure assembled from uniform spheres. *Regime: Numerical modeling of wave interaction with a porous floating structure consisting of uniform spheres.* [direct_finding, numerical] (Yiyong Dong 2024, [doi:10.1063/5.0222161](https://doi.org/10.1063/5.0222161))
- **C890.** Porous trapezoidal breakwaters near a rigid wall can trap waves, with performance controlled by current, porosity, geometry, spacing and wave conditions. *Regime: Wave trapping by porous breakwater near a rigid wall under the influence of ocean current.* [direct_finding, analytical] (K. C. Swami 2024, [doi:10.1038/s41598-024-68384-w](https://doi.org/10.1038/s41598-024-68384-w))
- **C891.** Regular-wave tests quantify dynamic pressures and forces on pile-supported breakwaters fitted with inclined perforated plates. *Regime: Wave forces and dynamic pressures on pile-supported breakwaters with inclined perforated plates under regular waves.* [direct_finding, mixed] (Ziwang Li 2024, [doi:10.3389/fmars.2024.1499685](https://doi.org/10.3389/fmars.2024.1499685))
- **C892.** Physical and numerical tests show that porosity modifies nonlinear wave evolution, turbulence and attenuation over a permeable submerged breakwater. *Regime: Experimental and Numerical Study of the Nonlinear Evolution of Regular Waves over a Permeable Submerged Breakwater.* [direct_finding, mixed] (Wang Ping 2023, [doi:10.3390/jmse11081610](https://doi.org/10.3390/jmse11081610))
- **C893.** Eigenfunction matching predicts oblique-wave scattering and wall forces for arrays of variable porous breakwaters over uneven bathymetry. *Regime: Wave Forces on a Partially Reflecting Wall by Oblique Bragg Scattering with Porous Breakwaters over Uneven Bottoms.* [direct_finding, analytical] (Jen-Yi Chang 2022, [doi:10.3390/jmse10030409](https://doi.org/10.3390/jmse10030409))
- **C894.** A weakly compressible SPH porous-media formulation based on mixture theory and intrinsic phase averaging simulates free surfaces and permeable-breakwater interaction. *Regime: A weakly-compressible SPH-porous media model to simulate wave–breakwater interactions.* [direct_finding, numerical] (Mojtaba Jandaghian 2025, [doi:10.1016/j.coastaleng.2025.104811](https://doi.org/10.1016/j.coastaleng.2025.104811))
- **C895.** Neural-network calibration estimates porosity and Forchheimer coefficients for VARANS models from wave–coastal-structure response data. *Regime: Neural Network calibration method for VARANS models to simulate wave-coastal structures interaction.* [direct_finding, numerical] (Pilar Díaz-Carrasco 2023, [doi:10.1016/j.coastaleng.2023.104443](https://doi.org/10.1016/j.coastaleng.2023.104443))
- **C896.** Rubble-mound overtopping predictions are sensitive to the Van Gent porous-friction parameters used in an OpenFOAM model. *Regime: Influence of Van Gent Parameters on the Overtopping Discharge of a Rubble Mound Breakwater.* [direct_finding, numerical] (Federico Castiglione 2023, [doi:10.3390/jmse11081600](https://doi.org/10.3390/jmse11081600))
- **C897.** A semi-analytical linear pressure-drop model predicts mean drift forces on impermeable body arrays surrounded by thin porous surfaces. *Regime: Mean Drift Wave Forces on Arrays of Bodies Surrounded by Thin Porous Surfaces.* [direct_finding, analytical] (Dimitrios N. Konispoliatis 2023, [doi:10.3390/jmse11071269](https://doi.org/10.3390/jmse11071269))
- **C898.** Linear-wave analysis characterizes reflection and transmission by a multilayer trapezoidal porous breakwater under irregular spectra. *Regime: Performance of multilayered porous breakwater under irregular waves having different wave spectrum.* [direct_finding, analytical] (Santanu Kumar Dash 2024, [doi:10.1002/eng2.12964](https://doi.org/10.1002/eng2.12964))
- **C899.** Sollitt–Cross porous-flow theory predicts oblique scattering by a slotted porous floating breakwater above a sill-shaped seabed. *Regime: Oblique wave scattering by a rectangular porous floating breakwater with slotted screens over a sill-type seabed.* [direct_finding, analytical] (Kottala Panduranga 2022, [doi:10.2495/cmem-v10-n2-172-186](https://doi.org/10.2495/cmem-v10-n2-172-186))
- **C900.** A year of field measurements at Chabahar Bay documents seasonal wave reflection from a rubble-mound breakwater and its relation to incident wave conditions. *Regime: Monsoonal patterns of wave reflection from rubble mound breakwater of Chabahar Bay.* [direct_finding, field] (Seyed Masoud Mahmoudof 2024, [doi:10.5697/ecmx9318](https://doi.org/10.5697/ecmx9318))
- **C901.** A surrogate-assisted macroscopic CFD framework predicts wave interaction with porous marine structures governed by equivalent pressure-drop resistance. *Regime: A surrogate-assisted numerical framework for predicting wave interaction with porous marine structures.* [direct_finding, numerical] (Qiang Liu 2026, [doi:10.1080/19942060.2026.2682123](https://doi.org/10.1080/19942060.2026.2682123))
- **C1731.** IHFOAM implements mass-conserving two-phase VARANS porous-media flow, wave generation and active absorption in OpenFOAM; dam-break, 2D breakwater, and 3D wave-basin tests validate free-surface, pressure, and porous-structure interaction behavior. *Regime: Two-phase free-surface flow through porous media, including dam-break transients and regular or solitary waves interacting with 2D and 3D porous coastal structures..* [direct_finding, mixed] (Higuera 2014, [doi:10.1016/j.coastaleng.2013.08.010](https://doi.org/10.1016/j.coastaleng.2013.08.010))

## Papers

- Higuera (2014). Three-dimensional interaction of waves and porous coastal structures using OpenFOAM®. Part I: Formulation and validation. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2013.08.010](https://doi.org/10.1016/j.coastaleng.2013.08.010)
- Ed Mackay (2020). Comparison of analytical and numerical solutions for wave interaction with a vertical porous barrier. *Ocean Engineering*. [doi:10.1016/j.oceaneng.2020.107032](https://doi.org/10.1016/j.oceaneng.2020.107032)
- Pilar Díaz-Carrasco (2020). 2D water-wave interaction with permeable and impermeable slopes: Dimensional analysis and experimental overview. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2020.103682](https://doi.org/10.1016/j.coastaleng.2020.103682)
- Anna Feichtner (2020). Using a porous-media approach for CFD modelling of wave interaction with thin perforated structures. *Journal of Ocean Engineering and Marine Energy*. [doi:10.1007/s40722-020-00183-7](https://doi.org/10.1007/s40722-020-00183-7)
- Jisheng Zhang (2012). Numerical Simulation of Solitary Wave Induced Flow Motion around a Permeable Submerged Breakwater. *Journal of Applied Mathematics*. [doi:10.1155/2012/508754](https://doi.org/10.1155/2012/508754)
- Lemi Guta (2010). Navier-Stokes-Brinkman system for interaction of viscous waves with a submerged porous structure. *Tamkang Journal of Mathematics*. [doi:10.5556/j.tkjm.41.2010.722](https://doi.org/10.5556/j.tkjm.41.2010.722)
- Yiyong Dong (2024). Numerical modeling of wave interaction with a porous floating structure consisting of uniform spheres. *Physics of Fluids*. [doi:10.1063/5.0222161](https://doi.org/10.1063/5.0222161)
- K. C. Swami (2024). Wave trapping by porous breakwater near a rigid wall under the influence of ocean current. *Scientific Reports*. [doi:10.1038/s41598-024-68384-w](https://doi.org/10.1038/s41598-024-68384-w)
- Ziwang Li (2024). Wave forces and dynamic pressures on pile-supported breakwaters with inclined perforated plates under regular waves. *Frontiers in Marine Science*. [doi:10.3389/fmars.2024.1499685](https://doi.org/10.3389/fmars.2024.1499685)
- Wang Ping (2023). Experimental and Numerical Study of the Nonlinear Evolution of Regular Waves over a Permeable Submerged Breakwater. *Journal of Marine Science and Engineering*. [doi:10.3390/jmse11081610](https://doi.org/10.3390/jmse11081610)
- Jen-Yi Chang (2022). Wave Forces on a Partially Reflecting Wall by Oblique Bragg Scattering with Porous Breakwaters over Uneven Bottoms. *Journal of Marine Science and Engineering*. [doi:10.3390/jmse10030409](https://doi.org/10.3390/jmse10030409)
- Mojtaba Jandaghian (2025). A weakly-compressible SPH-porous media model to simulate wave–breakwater interactions. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2025.104811](https://doi.org/10.1016/j.coastaleng.2025.104811)
- Pilar Díaz-Carrasco (2023). Neural Network calibration method for VARANS models to simulate wave-coastal structures interaction. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2023.104443](https://doi.org/10.1016/j.coastaleng.2023.104443)
- Federico Castiglione (2023). Influence of Van Gent Parameters on the Overtopping Discharge of a Rubble Mound Breakwater. *Journal of Marine Science and Engineering*. [doi:10.3390/jmse11081600](https://doi.org/10.3390/jmse11081600)
- Dimitrios N. Konispoliatis (2023). Mean Drift Wave Forces on Arrays of Bodies Surrounded by Thin Porous Surfaces. *Journal of Marine Science and Engineering*. [doi:10.3390/jmse11071269](https://doi.org/10.3390/jmse11071269)
- Santanu Kumar Dash (2024). Performance of multilayered porous breakwater under irregular waves having different wave spectrum. *Engineering Reports*. [doi:10.1002/eng2.12964](https://doi.org/10.1002/eng2.12964)
- Kottala Panduranga (2022). Oblique wave scattering by a rectangular porous floating breakwater with slotted screens over a sill-type seabed. *International Journal of Computational Methods and Experimental Measurements*. [doi:10.2495/cmem-v10-n2-172-186](https://doi.org/10.2495/cmem-v10-n2-172-186)
- Seyed Masoud Mahmoudof (2024). Monsoonal patterns of wave reflection from rubble mound breakwater of Chabahar Bay. *Oceanologia*. [doi:10.5697/ecmx9318](https://doi.org/10.5697/ecmx9318)
- Qiang Liu (2026). A surrogate-assisted numerical framework for predicting wave interaction with porous marine structures. *Engineering Applications of Computational Fluid Mechanics*. [doi:10.1080/19942060.2026.2682123](https://doi.org/10.1080/19942060.2026.2682123)
