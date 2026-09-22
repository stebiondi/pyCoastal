# Urban macro-roughness

`tsunami.inundation.urban_roughness` | Modification of tsunami runup and overland flow by building layouts and other large obstacles.

Parent: [Tsunamis and long waves](tsunami.md) > [Tsunami inundation](tsunami.inundation.md)

Papers: 2. Claims: 5. Equations: 2.

## Synthesis

**Well established.** In the reviewed regular arrays, greater longshore obstruction and generally more rows reduced maximum runup; 45-degree rotation changed runup more than aligned-versus-staggered placement.

**Governing physics.** Building arrays redistribute rather than simply remove hazard: reflection and turbulent losses reduce distal runup, while contraction, retained water, delayed drainage, and local impact can increase water levels or pressures within the built zone.

**Dimensionless parameters.** Longshore obstruction psi_ls, cross-shore obstruction psi_cs, surf similarity xi, wave nonlinearity a/h0, row count, and obstacle rotation organize the reviewed runup experiments.

**Major equations.** Depth-averaged mass and momentum equations represent inundation, with resolved obstacles imposing solid boundaries or subgrid approaches adding drag and blockage sink terms. Array response is summarized through runup ratios and obstruction measures in cross-shore and longshore directions.

**Typical methods.** Studies generate controlled long waves over a plane beach, place rigid obstacle arrays with varied rows, alignment, rotation and obstruction, record free surface and runup throughout and behind the array, compare unobstructed references and construct configuration-specific response nomograms.

**Numerical models.** The reviewed source is experiment-centered and yields empirical runup nomograms. Depth-averaged models can resolve individual buildings or parameterize subgrid blockage and drag, but those urban formulations remain outside reviewed journal evidence for this node.

**Experimental datasets.** Reviewed evidence comprises sinusoidal long-wave tests on a 1:40 beach with rigid 0.10 m cubes arranged in one, five and ten rows, aligned or staggered and at zero or 45-degree rotation, over surf-similarity 7.69-10.49.

**Validated ranges.** Goseberg's nomograms cover single sinusoidal waves with xi=7.69-10.49 on a 1:40 beach, rigid 0.10 m cubes, one/five/ten rows, and 0 or 45 degree rotation.

**Recent advances.** Recent advances use lidar-derived building geometry, anisotropic subgrid porosity and drag, GPU-resolved city models, movable debris and failure, hybrid regional-to-building nests, uncertainty ensembles and validation against pressure, momentum flux and drainage as well as depth.

**Disagreements.** Bulk Manning roughness is simple but does not separately represent blockage, directional porosity, shocks, storage or channelization. Explicit buildings resolve pathways but require fine grids and geometry; subgrid drag offers efficiency yet needs configuration- and regime-aware validation.

**Limitations.** Neither total runup reduction nor downstream pressure shielding is safely transferable to real cities without accounting for heterogeneous geometry, structural failure, debris, sediment, overtopping, complex topography, and the incident-wave regime.

**Open questions.** A common benchmark spanning array-scale runup, building-scale pressure and force, movable debris and sediment, failure, and realistic urban geometry remains needed.

**Seminal papers.** Classical porous-media and drag analogies treated urban resistance in depth-averaged flow; post-tsunami flume arrays and field surveys established shielding, channelization, storage and directional blockage, motivating explicit-building and subgrid urban models.

## Equations

### Longshore obstruction ratio

$$
\psi_{ls}=\frac{\hat b_{mr}}{\hat b_{mr}+b_{st}}
$$

Regime: Regular cubic macro-roughness arrays without overtopping.

Variables: `psi_ls` longshore obstruction ratio; `b_hat_mr` effective obstacle width including rotation; `b_st` clear street width

Source: (Goseberg 2013, [doi:10.5194/nhess-13-2991-2013](https://doi.org/10.5194/nhess-13-2991-2013))

### Cross-shore obstruction ratio

$$
\psi_{cs}=\frac{L_{mr}}{n\hat b_{mr}}
$$

Regime: Regular cubic macro-roughness arrays without overtopping.

Variables: `psi_cs` cross-shore obstruction ratio; `L_mr` cross-shore length of obstacle zone; `n` number of obstacle rows; `b_hat_mr` effective rotated obstacle width

Source: (Goseberg 2013, [doi:10.5194/nhess-13-2991-2013](https://doi.org/10.5194/nhess-13-2991-2013))

## Claims

- **C52.** Across the tested arrays, increasing longshore obstruction and generally increasing the number of building rows reduced maximum long-wave runup relative to the unobstructed beach. *Regime: Rigid 0.10 m cubes on a 1:40 beach, single sinusoidal waves with surf similarity 7.69-10.49, and one, five, or ten rows..* [direct_finding, experimental] (Goseberg 2013, [doi:10.5194/nhess-13-2991-2013](https://doi.org/10.5194/nhess-13-2991-2013))
- **C53.** For staggered arrays rotated 45 degrees, additional runup reduction relative to the non-rotated reference ranged from 4.2% to 21.4% with five rows and from 13.1% to 19.6% with ten rows across the stated obstruction cases. *Regime: The paper's staggered cube configurations and tested obstruction ratios; percentages are differences between configurations, not total attenuation..* [direct_finding, experimental] (Goseberg 2013, [doi:10.5194/nhess-13-2991-2013](https://doi.org/10.5194/nhess-13-2991-2013))
- **C54.** Changing cube rotation had a stronger effect on runup reduction than changing between aligned and staggered rows in the tested configurations. *Regime: Five- and ten-row regular arrays with 0 or 45 degree rotation on the tested beach..* [direct_finding, experimental] (Goseberg 2013, [doi:10.5194/nhess-13-2991-2013](https://doi.org/10.5194/nhess-13-2991-2013))
- **C55.** The first obstacle row generated an offshore-propagating shock, while water retained within and behind the array drained with a time lag and could have higher local levels than the unobstructed case. *Regime: The measured rigid-array cases, especially the five-row staggered rotated example with psi_ls=0.739..* [direct_finding, experimental] (Goseberg 2013, [doi:10.5194/nhess-13-2991-2013](https://doi.org/10.5194/nhess-13-2991-2013))
- **C56.** The reported nomograms should not be transferred directly to heterogeneous real cities with building failure, debris, sediment transport, overtopping, or complex three-dimensional topography. *Regime: Prototype application beyond the idealized flume geometry..* [direct_finding, review] (Goseberg 2013, [doi:10.5194/nhess-13-2991-2013](https://doi.org/10.5194/nhess-13-2991-2013))

## Papers

- Goseberg (2013). Reduction of maximum tsunami run-up due to the interaction with beachfront development – application of single sinusoidal waves. *Natural Hazards and Earth System Sciences*. [doi:10.5194/nhess-13-2991-2013](https://doi.org/10.5194/nhess-13-2991-2013)
- Tomiczek (2016). Physical modelling of tsunami onshore propagation, peak pressures, and shielding effects in an urban building array. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2016.07.003](https://doi.org/10.1016/j.coastaleng.2016.07.003)
