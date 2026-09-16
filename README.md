
<p align="center">
  <img src="media/pyCoastal_logo.png"  width="400">
</p>

A Python module for Coastal Engineering calculations, and to play around with numerics.

Copyright (c) 2025 Stefano Biondi
Licensed under the MIT License. See LICENSE file for details.

# Install via pip:

```bash
pip install pyCoastal
```
# Or clone and Install in editable mode

```bash
git clone https://github.com/stebiondi/pyCoastal.git
cd pyCoastal
pip install -e .
```
---

##  Simulation Preview

circular wave propagation from a central disturbance:

<p align="center">
  <img src="media/water_drop.gif" alt="2D Wave Animation" width="600">
</p>

---

## Applications

Scenario-level simulators built on the numerics, physics and tools layers.
Each takes an engineering design and reports the quantities a project
actually turns on.

### Beach nourishment

```python
from pyCoastal.applications.nourishment import (
    NourishmentDesign, WaveClimate, SECONDS_PER_YEAR,
    simulate_nourishment, renourishment_schedule,
)

design = NourishmentDesign(length=3000, berm_width=30, taper=200, D=8, B=2)
climate = WaveClimate(Hb=1.0, T=8.0, alpha0=0.0)

result = simulate_nourishment(design, climate, duration=20 * SECONDS_PER_YEAR)
result.design_life() / SECONDS_PER_YEAR   # years until 50% of the fill is gone
result.retained_fraction                  # volume retained vs time
result.berm_width                         # shoreline width at the fill centre

plan = renourishment_schedule(design, climate, horizon=30 * SECONDS_PER_YEAR)
plan["interval"], plan["n_renourishments"], plan["total_volume"]
```

The fill is evolved with the one-line model in `pyCoastal.tools.shoreline`.
`pelnard_considere` gives the linearized analytical solution for a rectangular
fill, which the test suite uses to verify the solver.

<p align="center">
  <img src="media/nourishment_design.png" alt="Nourishment design study" width="800">
</p>

Worked example: `examples/nourishment_design.py`

### Port layout

Phase-resolved wave propagation into a harbour. Breakwaters are rasterized as
structures with a settable absorption, waves enter from a soft source, and the
open boundaries are sponge layers.

```python
import numpy as np
from pyCoastal.applications.port import IncidentWave, harbour_layout, simulate_port

layout = harbour_layout(gap=130, arm_length=300, back_wall=True, absorption=0.35)
wave = IncidentWave(height=1.5, period=9.0, direction=np.deg2rad(0))

result = simulate_port(layout, wave, sponge_sides=("west", "north", "south"))

result.disturbance_coefficient          # Kd = H / H_incident over the whole basin
result.probe((1120, 450))               # Kd at one point
result.berth_report({"quay": (1120, 450)})
result.operable_fraction({"quay": (1120, 450)}, limit=0.5)
```

The celerity comes from the linear dispersion relation at the run period, so
the wavelength is correct in intermediate water rather than the shallow-water
approximation. Against a semi-infinite breakwater the solver gives a deep quiet
shadow, Kd near 0.5 on the geometric shadow boundary, and Fresnel fringes in
the illuminated field.

<p align="center">
  <img src="media/port_diffraction.gif" alt="Wave diffraction into a harbour" width="700">
</p>

<p align="center">
  <img src="media/port_disturbance.png" alt="Harbour disturbance coefficient" width="700">
</p>

Worked example: `examples/port_diffraction.py`


### 📚 Citation

If you use **pyCoastal** in a scientific publication, please cite:

> **Biondi, S.** (2025)  
> _pyCoastal: a Python package for Coastal Engineering_  
> GitHub: [https://github.com/stebiondi/pyCoastal](https://github.com/stebiondi/pyCoastal)  
> Version: v0.1.1  

You can also use this BibTeX entry:

```bibtex
@software{pyCoastal2025,
  author  = {Biondi, Stefano},
  title   = {{pyCoastal}: Modular Coastal Process Modeling in Python},
  year    = {2025},
  url     = {https://github.com/stebiondi/pyCoastal},
  version = {v0.1.1}
}
