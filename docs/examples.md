# pyCoastal examples

Every script runs from the repository root (`python examples/<name>.py`). The engineering examples print a design report and write figures to `media/`; their captured output is in `docs/manual/outputs/`. The numerical examples animate on screen and read `examples/configs/*.yaml`.

## [`examples/numerics/water_drop.py`](../examples/numerics/water_drop.py)

water_drop.py 2D linear wave equation: η_tt = c² ∇²η

## [`examples/waves2D.py`](../examples/waves2D.py)

waves2D.py 2D depth-averaged wave propagation model with observation points.

## [`examples/wave2D_irregular.py`](../examples/wave2D_irregular.py)

waves2D_irregular.py 2D depth-averaged wave model with irregular forcing at y=0. Uses pyCoastal: - UniformGrid for spatial mesh - generate_irregular_wave for η(t) boundary condition - YAML config for setup

## [`examples/current.py`](../examples/current.py)

current.py 2D passive x-direction current advection with: - Dirichlet inlet (west), Neumann outlet (east) - UniformGrid mesh - Upwind scheme for u_t + c·u_x = 0 - Real-time animation + time series at a gauge - Parameters from YAML config

## [`examples/pollutant.py`](../examples/pollutant.py)

pollutant.py 2D pollutant advection–diffusion in a shallow pond: - UniformGrid from pyCoastal - Operators: gradient, laplacian - Upwind advection, central diffusion - Neumann (zero-flux) boundary conditions - Animated visualization of scalar field

## [`examples/numerics/viscous_fluid.py`](../examples/numerics/viscous_fluid.py)

viscous_fluid.py 2D incompressible Navier–Stokes simulation with: - Two counter-rotating vortices - Central-difference convection and diffusion - Forward Euler time integration - Periodic boundary conditions - Real-time animation of speed field

## [`examples/numerics/2D_irr_turb.py`](../examples/numerics/2D_irr_turb.py)



## [`examples/equilibrium_shoreline.py`](../examples/equilibrium_shoreline.py)

Equilibrium shoreline built from three arcs: - left lateral arc (shoreline -> inner toe T1 -> bay point S0) - central arc (T2 -> apex S -> T3) - right lateral arc (T4 -> bay point S1 -> shoreline) Inputs are read from examples/configs/equilibrium_shoreline.yaml. Computation uses helper utilities in pyCoastal.tools.morphodynamics.

## [`examples/design_wave.py`](../examples/design_wave.py)

From a wave record to a design wave, and on to a structure. Takes a 40-year synthetic hindcast of significant wave height, chooses a storm threshold with the standard diagnostics, fits a peaks-over-threshold model, cross-checks it against annual maxima, and hands the 100-year wave to the seawall designer.

Captured output: [`docs/manual/outputs/design_wave.txt`](manual/outputs/design_wave.txt)

## [`examples/breakwater_design.py`](../examples/breakwater_design.py)

Rubble-mound breakwater design check. Sizes armour with Van der Meer, sets the crest from an EurOtop overtopping limit, and plots the two design curves an engineer actually reads: stone size against slope, and overtopping against crest freeboard.

Captured output: [`docs/manual/outputs/breakwater_design.txt`](manual/outputs/breakwater_design.txt)

## [`examples/seawall_section.py`](../examples/seawall_section.py)

Seawall design, from a design condition to a drawing. Sizes an L-shaped gravity seawall for a promenade, prints the design report, and writes the dimensioned cross-section plus a DXF of the geometry.

Captured output: [`docs/manual/outputs/seawall_section.txt`](manual/outputs/seawall_section.txt)

## [`examples/port_diffraction.py`](../examples/port_diffraction.py)

Port layout study: phase-resolved wave diffraction into a harbour. Propagates a monochromatic swell into a two-arm harbour, writes an animated GIF of the instantaneous surface so the diffraction into the basin is visible wave by wave, and reports the disturbance coefficient at a set of berths.

Captured output: [`docs/manual/outputs/port_diffraction.txt`](manual/outputs/port_diffraction.txt)

## [`examples/port_layout_comparison.py`](../examples/port_layout_comparison.py)

Compare the built-in port layouts under the same design wave. Runs every layout in ``pyCoastal.applications.port.LAYOUTS``, maps the disturbance coefficient, and ranks them by how quiet they keep the basin.

Captured output: [`docs/manual/outputs/port_layout_comparison.txt`](manual/outputs/port_layout_comparison.txt)

## [`examples/pile_wave_loads.py`](../examples/pile_wave_loads.py)

Wave loads on a monopile: where the load is, and when it peaks. Computes the Morison load distribution on an offshore wind monopile, sweeps the wave phase for the worst base shear and the worst overturning moment, and shows why they do not happen at the same instant.

Captured output: [`docs/manual/outputs/pile_wave_loads.txt`](manual/outputs/pile_wave_loads.txt)

## [`examples/pier_scour.py`](../examples/pier_scour.py)

Scour at an estuary pier: tide, river and waves, and where the base sits. A bridge pier in an estuary is asked to stand in a flow that reverses twice a day, is biased seaward by the river, changes depth under a four metre tide, and carries a wind chop on top. None of those peak together.

Captured output: [`docs/manual/outputs/pier_scour.txt`](manual/outputs/pier_scour.txt)

## [`examples/bridge_scour.py`](../examples/bridge_scour.py)

Total scour at an estuary crossing: all three HEC-18 components. Local scour at a pier is the one everybody computes, and on a contracted crossing it is routinely the smallest of the three. HEC-18 splits total scour into contraction, local and abutment, and this works all three over a tidal cycle.

Captured output: [`docs/manual/outputs/bridge_scour.txt`](manual/outputs/bridge_scour.txt)

## [`examples/backwater.py`](../examples/backwater.py)

Backwater at a bridge, and the flow split that feeds contraction scour. Two things this example is for.

Captured output: [`docs/manual/outputs/backwater.txt`](manual/outputs/backwater.txt)

## [`examples/navigation_channel.py`](../examples/navigation_channel.py)

Approach channel design: how deep, how wide, and how much dredging. Sizes an approach channel for a post-Panamax container ship, prints the depth chain and the width build-up, and issues the cross-section as a drawing sheet.

Captured output: [`docs/manual/outputs/navigation_channel.txt`](manual/outputs/navigation_channel.txt)

## [`examples/berth_fenders.py`](../examples/berth_fenders.py)

Berthing energy and fender selection for a container terminal. A berth fails in three different ways and only one of them is about energy.

Captured output: [`docs/manual/outputs/berth_fenders.txt`](manual/outputs/berth_fenders.txt)

## [`examples/nourishment_design.py`](../examples/nourishment_design.py)

Beach nourishment design study. Evolves a beach fill with the one-line model, compares it against the Pelnard-Considere analytical solution, and reports design life and a renourishment schedule over a 30-year planning horizon.

Captured output: [`docs/manual/outputs/nourishment_design.txt`](manual/outputs/nourishment_design.txt)

## [`examples/nourishment_profile.py`](../examples/nourishment_profile.py)

Beach nourishment: what the borrow source is worth. The planform model in `examples/nourishment_design.py` answers how long a fill lasts. This answers the question asked before it: how much dry beach does a given volume buy, and how much does that depend on where the sand comes from.

Captured output: [`docs/manual/outputs/nourishment_profile.txt`](manual/outputs/nourishment_profile.txt)

## [`examples/storm_surge_flooding.py`](../examples/storm_surge_flooding.py)

Storm surge water level and flood mapping. Builds the water-level budget for a design storm, maps the flooded area on a synthetic barrier-island terrain, and shows the difference between a plain elevation threshold and a hydraulically connected flood map.

Captured output: [`docs/manual/outputs/storm_surge_flooding.txt`](manual/outputs/storm_surge_flooding.txt)
