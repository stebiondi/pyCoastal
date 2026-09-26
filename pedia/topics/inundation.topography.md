# Topographic and bathymetric controls

`inundation.topography` | Elevation data and terrain representation.

Parent: [Flood mapping and inundation](inundation.md)

Papers: 10. Claims: 5. Equations: 1.

## Synthesis

**Well established.** Inundation mapping depends on a hydraulically conditioned, datum-consistent terrain surface that represents connected low paths, channels, barriers and openings; finer nominal resolution does not compensate for missing bathymetry, blocked drainage or incorrect structures.

**Governing physics.** Topography and bathymetry control storage, conveyance, wetting paths, channelization and hydraulic gradients, while levees, roads, buildings, dunes, culverts and embankments create thresholds whose overtopping or openings can abruptly change connectivity and extent.

**Dimensionless parameters.** Relevant normalized controls include vertical error relative to flood depth or freeboard, horizontal resolution relative to channel or barrier width, slope-to-error ratio, submergence, grid convergence, connected-to-total low-area fraction and inundation overlap or boundary-distance scores.

**Major equations.** Terrain enters shallow-water mass and momentum equations through bed elevation, depth and slope and enters static screening through elevation and connectivity tests; vertical datum transformations, interpolation, subgrid conveyance and uncertainty perturbations modify those inputs.

**Typical methods.** Workflows merge topo-bathymetry in one vertical datum, remove vegetation and artifacts, preserve or burn channels and openings, encode defenses and buildings deliberately, test connectivity, compare resolutions and terrain sources, propagate elevation uncertainty and validate extent, depth and pathways independently.

**Numerical models.** Reviewed methods include elevation-threshold propagation with hydrologic connectivity, a rapid RDM/Zero-Point Boundary coastal hindcast, and HEC-RAS 2D simulations using alternative LiDAR terrains and discharge- or volume-based corrections.

**Experimental datasets.** The evidence includes Staten Island airborne LiDAR connectivity auditing, a 5 m Tacloban terrain hindcast checked against surveyed Haiyan limits, and topographic-versus-bathymetric LiDAR comparisons for 11 Norwegian sites and multiple flood scenarios.

**Validated ranges.** Evidence spans one urban coastal island, one typhoon-affected coastal city and 11 river reaches. Findings are conditional on their resolutions, geomorphology, structures and forcing; the Norway correction results are not direct coastal validation.

**Recent advances.** Recent advances integrate topographic and bathymetric LiDAR, satellite/UAS change detection, structure and drainage conditioning, rapid terrain-driven solvers, learned depth estimation, cloud-scale DEM processing and ensembles that propagate vertical and representation uncertainty.

**Disagreements.** Bare-earth DEMs improve hydraulic ground representation but can erase buildings or defenses that matter; digital surface models retain obstacles but may falsely block flow. Explicit structures are preferable when data support them, while subgrid or roughness treatment may be more stable at coarser scales.

**Limitations.** Key limitations are vertical and horizontal error, inconsistent datums, absent submerged channels, vegetation filtering, bridges and culverts, seawall gaps, building representation, changing morphology, uncertain defense condition, grid-scale connectivity and validation focused only on maximum extent.

**Open questions.** Priorities include seamless coastal topo-bathymetry, automated connectivity conditioning with provenance, dynamic breach and culverts, uncertainty-aware subgrid structures, morphology updates, compound river–rain–surge boundaries, cross-resolution skill and open elevation-change benchmarks.

**Seminal papers.** Early bathtub mapping highlighted elevation control but ignored pathways; hydrologically connected threshold methods, LiDAR bare-earth DEMs and two-dimensional wetting/drying solvers established more defensible practice, followed by subgrid and structure-aware terrain models.

## Equations

### Zero-Point Boundary inundation depth

$$
d_i(x,y)=\max[0,\eta_{s+w}(x,y)-z_{DTM}(x,y)]
$$

Regime: Haiyan hindcast over the 5 m eastern Leyte terrain model.

Variables: `d_i` mapped inundation depth; `eta_s+w` interpolated simulated surge and wave level; `z_DTM` terrain elevation

Source: (Zerrudo 2024, [doi:10.1016/j.tcrr.2024.11.001](https://doi.org/10.1016/j.tcrr.2024.11.001))

## Claims

- **C160.** At Staten Island, auditing and enforcing drainage connectivity identified more than 11 ha of inland low terrain that simple elevation-threshold inundation could misclassify. *Regime: Static DEM-based inundation screening; dynamic timing and hydraulic resistance are not represented..* [direct_finding, numerical] (Poppenga 2015, [doi:10.3390/rs70911695](https://doi.org/10.3390/rs70911695))
- **C1127.** Across 11 Norwegian sites, inundation differences between topographic-only and bathymetric LiDAR terrain generally decreased as flood magnitude increased, but embankment overtopping, sinuosity and bank geometry altered the error pattern; volume-based terrain correction usually improved results most. *Regime: Comparison between Topographic and Bathymetric LiDAR Terrain Models in Flood Inundation Estimations.* [direct_finding, numerical] (Awadallah 2022, [doi:10.3390/rs14010227](https://doi.org/10.3390/rs14010227))
- **C1168.** Land-cover-stratified semivariogram ensembles of MERIT DEM error produced flood-inundation estimates closer to lidar benchmarks than a single deterministic DEM in Mekong Delta and Fiji tests. *Regime: Implications of Simulating Global Digital Elevation Models for Flood Inundation Studies.* [direct_finding, mixed] (Laurence Hawker 2018, [doi:10.1029/2018wr023279](https://doi.org/10.1029/2018wr023279))
- **C1176.** A physics-aware topographic constraint with multimodal class distributions mapped inundation from sparse observations more accurately and robustly than baseline spatial-classification methods in real flood applications. *Regime: Flood Inundation Mapping with Limited Observations Based on Physics-Aware Topography Constraint.* [direct_finding, mixed] (Sainju 2021, [doi:10.3389/fdata.2021.707951](https://doi.org/10.3389/fdata.2021.707951))
- **C1589.** A GIS and analytical-hierarchy assessment combines coastal geomorphic, topographic and hazard indicators to map relative vulnerability along the Puducherry coast. *Regime: Coastal vulnerability assessment of Puducherry coast, India, using the analytical hierarchical process.* [direct_finding, mixed] (R. Mani Murali 2013, [doi:10.5194/nhess-13-3291-2013](https://doi.org/10.5194/nhess-13-3291-2013))

## Papers

- R. Mani Murali (2013). Coastal vulnerability assessment of Puducherry coast, India, using the analytical hierarchical process. *Natural hazards and earth system sciences*. [doi:10.5194/nhess-13-3291-2013](https://doi.org/10.5194/nhess-13-3291-2013) [published version, CC BY](https://nhess.copernicus.org/articles/13/3291/2013/nhess-13-3291-2013.pdf)
- Laurence Hawker (2018). Implications of Simulating Global Digital Elevation Models for Flood Inundation Studies. *Water Resources Research*. [doi:10.1029/2018wr023279](https://doi.org/10.1029/2018wr023279) [published version, CC BY](https://agupubs.onlinelibrary.wiley.com/doi/pdfdirect/10.1029/2018WR023279)
- Awadallah (2022). Comparison between Topographic and Bathymetric LiDAR Terrain Models in Flood Inundation Estimations. *Remote Sensing*. [doi:10.3390/rs14010227](https://doi.org/10.3390/rs14010227) [published version, CC BY](https://mdpi-res.com/d_attachment/remotesensing/remotesensing-14-00227/article_deploy/remotesensing-14-00227.pdf)
- Poppenga (2015). Evaluation of Airborne Lidar Elevation Surfaces for Propagation of Coastal Inundation: The Importance of Hydrologic Connectivity. *Remote Sensing*. [doi:10.3390/rs70911695](https://doi.org/10.3390/rs70911695) [published version, CC BY](https://www.mdpi.com/2072-4292/7/9/11695/pdf)
- Sainju (2021). Flood Inundation Mapping with Limited Observations Based on Physics-Aware Topography Constraint. *Frontiers in Big Data*. [doi:10.3389/fdata.2021.707951](https://doi.org/10.3389/fdata.2021.707951) [published version, CC BY](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC8351936/fullTextXML)
- James Savage (2016). Quantifying the importance of spatial resolution and other factors through global sensitivity analysis of a flood inundation model. *Water Resources Research*. [doi:10.1002/2015wr018198](https://doi.org/10.1002/2015wr018198) [published version, CC BY](https://agupubs.onlinelibrary.wiley.com/doi/pdfdirect/10.1002/2015WR018198)
- James Savage (2015). When does spatial resolution become spurious in probabilistic flood inundation predictions?. *Hydrological Processes*. [doi:10.1002/hyp.10749](https://doi.org/10.1002/hyp.10749) [published version, CC BY](https://onlinelibrary.wiley.com/doi/pdfdirect/10.1002/hyp.10749)
- Gallien (2014). Urban coastal flood prediction: Integrating wave overtopping, flood defenses and drainage. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2014.04.007](https://doi.org/10.1016/j.coastaleng.2014.04.007) [published version, read only](https://cpb-us-w2.wpmucdn.com/research.seas.ucla.edu/dist/6/18/files/2020/12/1-s2.0-S0378383914000775-main.pdf)
- Leon (2014). Incorporating DEM Uncertainty in Coastal Inundation Mapping. *PLoS ONE*. [doi:10.1371/journal.pone.0108727](https://doi.org/10.1371/journal.pone.0108727) [published version, CC BY](https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0108727&type=printable)
- Zerrudo (2024). Hindcasting the typhoon haiyan storm surge in coastal eastern leyte. *Tropical Cyclone Research and Review*. [doi:10.1016/j.tcrr.2024.11.001](https://doi.org/10.1016/j.tcrr.2024.11.001) [published version, CC BY-NC-ND](https://api.elsevier.com/content/article/PII:S2225603224000559?httpAccept=text/xml)
