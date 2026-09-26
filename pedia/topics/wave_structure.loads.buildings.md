# Loads on coastal buildings

`wave_structure.loads.buildings` | Forces on buildings and arrays.

Parent: [Wave-structure interaction](wave_structure.md) > [Wave loads](wave_structure.loads.md)

Papers: 4. Claims: 2. Equations: 2.

## Synthesis

**Well established.** Coastal-building loads are governed by incident and breaking-wave kinematics, inundation depth, exposed area, openings and elevation, but surrounding buildings and debris can strongly alter the local flow and invalidate isolated-solid-building assumptions.

**Governing physics.** Loads combine hydrostatic, drag, inertia, impact, uplift, buoyancy, and downward components. Breaking and bore fronts create impulses; openings relieve pressure unless blocked; upstream structures shield or redirect flow; debris adds impacts and can form sustained blockage dams.

**Dimensionless parameters.** Important controls include relative inundation and clearance, Froude number, wave-height-to-depth ratio, building-width-to-wavelength ratio, opening ratio, spacing and arrangement ratios, blockage fraction, debris size and concentration, and vertical-load normalization by displaced-water or dynamic-force scales.

**Major equations.** Engineering descriptions integrate pressure over wetted surfaces, use hydrostatic-plus-dynamic or drag/inertia balances, quantify impulse and cantilever arm, and increasingly employ CFD-trained surrogate functions of wave, surge, clearance, opening, and plan geometry.

**Typical methods.** Evidence uses scaled wave/bore flumes, pressure and multi-axis force sensing, high-speed imaging, building-array layouts, debris ensembles, Reynolds-averaged or volume-of-fluid CFD, design-of-experiment sampling, and ensemble machine learning.

**Numerical models.** Relevant tools include pressure-integrating CFD for surge and waves, ensemble load surrogates trained on designed CFD samples, and design equations that require local—not bare-earth—water levels when buildings alter breaking flow.

**Experimental datasets.** The reviewed base includes 1:20 urban-array breaking/nonbreaking tests with measured peak pressure and shielding, laboratory free-standing open-building tests with log and container debris, and 256 CFD cases for elevated-building vertical loading.

**Validated ranges.** Urban-array shielding reduced downstream peak pressure by 40%-70% in the source's idealized breaking-wave configurations; debris results cover logs and containers around an open building; elevated-building prediction spans a 256-case regular-wave CFD design domain whose detailed bounds remain source-table limited.

**Recent advances.** Recent work replaces single isolated-building coefficients with geometry-aware CFD ensembles and explicitly treats urban shielding, local breaking, openings, and debris dams as interacting modifiers of horizontal, vertical, and impulsive loading.

**Disagreements.** Openings generally reduce wave load, but debris blockage can remove that benefit. Bare-earth water-level inputs may be nonconservative in breaking-wave arrays even when standard equations perform for nonbreaking cases, showing that local flow modification governs transferability.

**Limitations.** Current evidence is sparse across building types and often uses idealized rigid geometry, regular or bore-like waves, limited debris shapes, and laboratory/CFD scales. Air, structural failure, scour, floating debris rotation, multi-building urban complexity, and uncertainty in prototype roughness remain underrepresented.

**Open questions.** Needed work includes common array benchmarks, irregular hurricane wave-plus-surge loading, probabilistic debris blockage, coupled scour and failure, vertical-load validation, opening and foundation optimization, and uncertainty-aware translation from CFD or scale models to codes.

**Seminal papers.** Within the extracted corpus, the 2016 urban-array experiment establishes quantified shielding and breaking-wave limitations; the 2020 debris-damming study shows reversal of opening benefits; the 2023 study adds CFD-trained vertical-load estimation for elevated buildings.

## Equations

### CFD-trained ensemble load surrogate

$$
\mathbf{F}(t)=\int_A -p\mathbf{n}\,dA+\mathbf{F}_{D,I}
$$

Regime: Elevated coastal-building geometries and regular-wave hurricane loading represented by a 256-case CFD design space; exact ranges require full-text tables.

Variables: `F` resultant structural load; `p` hydrodynamic or pneumatic pressure; `n` surface normal; `A` wetted or impacted area; `F_D,I` drag/inertia contribution where applicable; normalized load balance

Source: (Moeini 2023, [doi:10.1016/j.coastaleng.2023.104325](https://doi.org/10.1016/j.coastaleng.2023.104325))

### postpeak debris-load assessment methodology

$$
\mathbf{F}(t)=\int_A -p\mathbf{n}\,dA+\mathbf{F}_{D,I}
$$

Regime: Free-standing building with openings under laboratory unsteady long-wave flow; wooden logs and shipping-container debris configurations.

Variables: `F` resultant structural load; `p` hydrodynamic or pneumatic pressure; `n` surface normal; `A` wetted or impacted area; `F_D,I` drag/inertia contribution where applicable; normalized load balance

Source: (Davide Wüthrich 2020, [doi:10.1061/(asce)ww.1943-5460.0000541](https://doi.org/10.1061/(asce)ww.1943-5460.0000541))

## Claims

- **C285.** For a free-standing building with openings under unsteady long-wave flow, container debris produced severe impact peaks, whereas interlocking logs formed compact dams that caused higher and longer-lasting postpeak hydrodynamic forces. *Regime: Free-standing building with openings under laboratory unsteady long-wave flow; wooden logs and shipping-container debris configurations..* [direct_finding, experimental] (Davide Wüthrich 2020, [doi:10.1061/(asce)ww.1943-5460.0000541](https://doi.org/10.1061/(asce)ww.1943-5460.0000541))
- **C288.** Across a 256-case CFD design space for elevated coastal buildings under regular hurricane-representative waves, ensemble learning captured geometry- and wave-dependent vertical surge and wave forces. *Regime: Elevated coastal-building geometries and regular-wave hurricane loading represented by a 256-case CFD design space; exact ranges require full-text tables..* [direct_finding, mixed] (Moeini 2023, [doi:10.1016/j.coastaleng.2023.104325](https://doi.org/10.1016/j.coastaleng.2023.104325))

## Papers

- Tomiczek (2016). Physical modelling of tsunami onshore propagation, peak pressures, and shielding effects in an urban building array. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2016.07.003](https://doi.org/10.1016/j.coastaleng.2016.07.003) [published version, read only](https://doi.org/10.1016/j.coastaleng.2016.07.003)
- Davide Wüthrich (2020). Effect of Debris Damming on Wave-Induced Hydrodynamic Loads against Free-Standing Buildings with Openings. *Journal of Waterway, Port, Coastal, and Ocean Engineering*. [doi:10.1061/(asce)ww.1943-5460.0000541](https://doi.org/10.1061/(asce)ww.1943-5460.0000541) [submitted manuscript, CC BY-NC-ND](https://infoscience.epfl.ch/handle/20.500.14299/163135)
- Moeini (2023). Estimating hurricane-induced vertical surge and wave loads on elevated coastal buildings based on CFD simulations and ensemble learning. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2023.104325](https://doi.org/10.1016/j.coastaleng.2023.104325)
- Deming Zhu (2020). Experimental and 3D numerical investigation of solitary wave forces on coastal bridges. *Ocean Engineering*. [doi:10.1016/j.oceaneng.2020.107499](https://doi.org/10.1016/j.oceaneng.2020.107499) [published version, read only](https://www.sciencedirect.com/science/article/pii/S0029801820305126)
