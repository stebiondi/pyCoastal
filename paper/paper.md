---
title: "pyCoastal: a Python package for numerical modeling in coastal engineering"
tags:
  - Python
  - numerical modeling
  - coastal engineering
  - computational fluid dynamics
authors:
  - name: Stefano Biondi
    orcid: 0009-0001-5737-6012
    affiliation: "1"
affiliations:
  - name: University of Florida, United States
    index: 1
date: 17 July 2025
bibliography: paper.bib
---

# Summary

`pyCoastal` is an open-source Python package for the generation of numerical simulations of coastal hydrodynamics and scalar transport processes. The package provides a modular and extensible platform for solving linear and nonlinear partial differential equations (PDE) relevant to coastal processes, including wave propagation, pollutant dispersion, and viscous fluid dynamics. The framework involves grid generation, boundary condition management, numerical operators, and the selection of time integration schemes. Physical modules, such as literature formulations for common coastal processes, are implemented as standalone classes and can be easily composed or extended for prototyping and research. 
`pyCoastal` emphasizes clarity and reproducibility, with a strong focus on clean code structure and pedagogical transparency. It is particularly suited for simple applications in real case scenarios and as educational tool in coastal engineering, fluid mechanics, and numerical modeling.

# Statement of need

Numerical modeling of coastal processes, such as wave propagation, shallow water dynamics, and pollutant transport, typically relies on specialized software frameworks that are often complex to configure, extend, or adapt to new applications. Tools like SWAN, ADCIRC, and OpenFOAM, although powerful and detailed, present significant barriers due to their steep learning curves and rigid internal structures. More computationally demanding models do not necessarily yield higher accuracy, especially when simpler models are tuned effectively [@Lashley2020]. In fact, some processes can be modeled simply and still produce accurate, useful results when the simpler model is well tuned. Furthermore, successful calibration of numerical models hinges on the ability to accurately represent key physical processes and structural features, which can be hard to achieve in large modeling frameworks [@Simmons2017]. This complexity poses challenges both for young research and industry applications aiming to prototype models rapidly, as well as for instructors seeking clear, demonstrable tools for teaching coastal processes.

To solve this issue, `pyCoastal` offers a lightweight and modular coastal modeling framework fully in Python. It is designed to prioritize clarity and reproducibility, allowing users to define simulations through simple YAML configuration files and execute them with minimal setup. The codebase provides reusable components for grid generation, numerical operators, time integration schemes, and boundary condition handling, supporting both classical and custom physical models with ease. Its structure is designed to support both research and industry applications or instructional use in topics such as coastal hydrodynamics, numerical modeling, and environmental fluid mechanics. Moreover, `pyCoastal` integrates numerous established coastal‑engineering formulations, such as wave run‑up, sediment transport, and boundary layer calculations, enabling users to compute essential coastal parameters with ease.

As a result, `pyCoastal` functions as a versatile library suitable for both academic research and industrial applications in coastal engineering.

# How does it work

In this section, a two examples (one numerical, one applicative) of `pyCoastal`are presented.

# Irregular wave propagation on a 2D domain 

This example shows how pyCoastal can create and propagate a realistic wave signal based on an oceanographic spectrum in a 2-dimensional domain. The example builds a time series of surface elevation with the function `generate_irregular_wave` by sampling a chosen spectrum, assigning random phases, and summing the individual harmonic components. The user specifies inputs such as significant wave height, peak period, duration, and time step. The routine then returns the time vector and the corresponding free-surface signal that can be used as boundary forcing in numerical simulations (Figure 1). This example demonstrates how a spectral description of sea states can be converted into a synthetic wave time series suitable for coastal modeling. Additionally, it is given to the user the ability to add monitoring point (buoy-style) everywhere in the domain. 

The inputs for the domain and wave generation are taken from a YAML file. These YAML files share the names of the corresponding examples and are located in `/examples/config/`. The YAML reads:

```yaml
grid:
  nx: 200
  ny: 200
  dx: 1.0
  dy: 1.0

physics:
  gravity: 9.81
  depth: 5.0

forcing:
  type: jonswap   # options: pm or jonswap
  gamma: 3.3
  Hs: 0.5         # significant wave height (m)
  Tp: 3.0         # peak period (s)

solver:
  dt: 0.1
  duration: 60.0

output:
  gauge: [100, 100]  # buoy-style observation point
```

**JONSWAP spectrum** 

As a reference, it is explained the formulation used in the source code to calculate the Jonswap spectrum [@Hasselmann1973]. This spectrum modifies the Pierson-Moskovitz spectrum with a peaked enhancement factor as:

$$
S_{J}(f) = S_{PM}(f)\;\gamma^{\displaystyle
  \exp\left[-\frac{1}{2\sigma^2}\left(\frac{f}{f_p}-1\right)^2\right]} ,
$$

where:
- $S_{J}(f)$ is the JONSWAP spectral energy density [m²/Hz]
- -$f$ is the frequency
- $\gamma$ is the peak enhancement factor (typically 3.3, but can be customized to change the spectrum shape)  
- $\sigma$ is the spectral width parameter, with $\sigma = 0.07$ for $f < f_p$ and $\sigma = 0.09$ for $f > f_p$  

Once $S(f)$ is defined, the surface elevation time series is:

$$
\eta(t) = \sum_{i} A_i \cos\bigl(2\pi f_i + \phi_i\bigr),
$$

where:
- $\eta(t)$ is the free-surface elevation at time $t$ [m]  
- $A_i$ is the wave amplitude for frequency $f_i$ [m]  
- $\phi_i$ is a random phase shift in $[0,2\pi]$  
- $\Delta f$ is the frequency resolution  

The amplitudes $A_i$ are given by:

$$
A_i = \sqrt{2\,S(f_i)\,\Delta f}.
$$

![**Figure 1:** Irregular wave field produced in the example.  
The left panel shows a top view of the wave field with waves entering from the southern boundary. Side boundaries use free slip, and the northern boundary absorbs outgoing waves. The right panel shows the surface elevation over time at selected observation points.](media/wave2D_irregular_final.png)

**Figure 1:** Irregular wave field produced in the example.  
The left panel shows a top view of the wave field with waves entering from the southern boundary. Side boundaries use free slip, and the northern boundary absorbs outgoing waves. The right panel shows the surface elevation over time at selected observation points.

To test it, run this example:

```bash
python examples/wave2D_irregular.py
```

# Equilibrium shoreline after beach protection

This example is more practical and computes the equilibrium profile of a beach subject to protection of parallel breakwaters at distance $Y_i$ from shore and assigned their length $L_b$ and Gap width $G_b$. The concepts follow the derivation of [@Hsu1989] and empirical coefficients of [@Tsai2023]. The user can  specify the inputs in the config file:

```yaml
geometry:
  Lshore: 600.0   # domain length (m)
  Gb: 80.0        # gap between breakwaters (m)
  Lb1: 80.0       # left breakwater length (m)
  Lb2: 80.0       # right breakwater length (m)
  Yi: 60.0       # breakwater offshore distance (m)

numerics:
  n_points: 400         # samples per arc
  sag_side_factor: 0.5  # lateral arc sag factor (relative to Ye)
```
And obtain as result a design of the equilibrium profile (see Figure 2), as well as the accretion volume behind the breakwaters and the shoreline retreat in the protected area.

![**Figure 2:** Equilibrium shoreline after beach protection with two parallel breakwaters separated by a gap $G_b$ = 80 m and distant from shore $Y_i$ = 60 m. the blue dashed line represents the initial condition (flat shore, for example after a nourishment) and the thin red line the equilibrium shoreline. Wave are supposed to be perpendicular to shore, and coming from the upper part of the plot.](media/equilibrium_shoreline.png)


# Conclusion Future directions
In this work, the Python module for coastal processes `pyCoastal` was presented. The module is a simple and modular Python framework for building numerical models of coastal hydrodynamics and transport. Its design emphasizes clarity, flexibility and ease of use, allowing users to prototype simulations, explore physical processes and support instructional needs with minimal overhead. Future development will include wave energy dissipation and breaking models, more complete nearshore hydrodynamics, and sediment transport processes. Additional coastal-engineering formulations and analysis tools will also be integrated, further extending the range of research and educational applications that pyCoastal can support.

# Acknowledgements
I thank professors Alberto Canestrelli (UF) and Donald Slinn (UF) for the teachings in the numerical modeling and Hydrodynamics field.

# References
see paper.bib
