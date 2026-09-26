# Structural and system reliability

`uncertainty.reliability` | Failure probabilities and limit states.

Parent: [Reliability and uncertainty](uncertainty.md)

Papers: 5. Claims: 3. Equations: 1.

Used by pyCoastal design modules: Design conditions.

## Synthesis

**Well established.** Coastal reliability requires a limit state connecting uncertain environmental load and uncertain resistance, followed by probability integration over an explicit time horizon. Annual design reliability, operational event probability, and observed long-term performance answer different questions and must not be conflated.

**Governing physics.** Flood-defence failure depends on water level, waves, overflow, runup/overtopping, erosion, seepage, piping and stability, while nature-based system persistence also depends on ecological degradation and shoreline change. System performance couples loads, resistance, spatial dependence and multiple mechanisms.

**Dimensionless parameters.** Reliability index beta, annual failure probability, return period, conditional event probability, load and resistance coefficients of variation, importance factors, correlation, and forecast horizon organize analyses; physical mechanisms retain overtopping, stability and wave nondimensional groups.

**Major equations.** Core forms are g(R,S)=R-S or mechanism-specific limit states, failure probability P[g<=0], conditional operational probability integrated over forecast-load distributions, fragility curves P(failure|load), and series/parallel system combinations across sections and mechanisms.

**Typical methods.** Methods include FORM/SORM, Monte Carlo and importance sampling, fragility integration, Bayesian updating, event trees, system reliability, forecast ensembles, time-dependent deterioration, inspection updating, and decision analysis based on consequences and warning lead time.

**Numerical models.** Hydra-VIJ supplies probabilistic hydraulic conditions and annual failure-frequency machinery adapted to operational windows. Broader coastal applications require hydrodynamic, wave, geotechnical, morphodynamic and damage models embedded in limit-state or fragility calculations.

**Experimental datasets.** The extracted branch includes Dutch Vecht-delta probability forecasts and Hydra-VIJ load/failure relations; long-term Louisiana oyster-reef monitoring supplies a contrasting ten-year observation of performance persistence rather than a calibrated structural failure probability.

**Validated ranges.** The operational framework was applied to dike-ring area 10 with a 1/2,000 per-year reference standard and Dutch large-ring standards from 1/10,000 to 1/1,250 per year; default mechanisms were overflow and wave runup with deterministic strength.

**Recent advances.** Current directions couple forecast ensembles, Bayesian updating, active learning and rare-event simulation with digital twins; coastal use must still demonstrate calibrated limit states, physical coverage and out-of-sample reliability rather than importing generic algorithms uncritically.

**Disagreements.** An invariant reliability index need not imply an invariant physical failure probability under inconsistent transformations or models. More generally, very small numerical probabilities are not credible when epistemic model, mechanism, dependence, or deterioration uncertainty is omitted.

**Limitations.** The screened discovery batch was dominated by generic mathematical reliability work without coastal validation. The retained dike case fixes resistance, covers limited mechanisms and one Dutch system; the oyster record demonstrates persistence uncertainty but not a formal fragility model.

**Open questions.** Needs include multi-mechanism and network reliability, correlated spatial failures, nonstationary climate loads, deterioration and inspection, nature-based degradation, joint wave-surge-rainfall forcing, operational updating, model-form uncertainty, and consequence-aware warning thresholds.

**Seminal papers.** Within this branch, the 2013 operational dike framework is the central applied reliability study because it connects probabilistic natural-load forecasts to event-window failure probability and decision support rather than reporting only an annual index.

## Equations

### Operational dike failure probability

$$
P_f(\Delta t)=\int P[g(\mathbf{R},\mathbf{s})\leq0\mid\mathbf{s}]f_{\mathbf{S}|forecast}(\mathbf{s};\Delta t)\,d\mathbf{s}
$$

Regime: Hydra-VIJ-style operational dike assessment.

Variables: `P_f` failure probability in future window; `g` limit-state function; `R` dike resistance variables; `s` hydraulic and meteorological load vector; `f_S|forecast` forecast joint load density; `Delta t` operational time window; normalized framework expression

Source: (Wojciechowska 2013, [doi:10.1016/j.ress.2012.12.022](https://doi.org/10.1016/j.ress.2012.12.022))

## Claims

- **C290.** For a primary dike in the Vecht River delta, probabilistic forecasts of river discharge, Lake IJssel level, wind speed, and wind direction were propagated through Hydra-VIJ formulas to estimate operational failure probability over a future time window for overflow and wave-runup mechanisms. *Regime: Vecht-delta primary dike and Hydra-VIJ load/failure representation; overflow and wave-runup mechanisms with deterministic strength variables..* [direct_finding, mixed] (Wojciechowska 2013, [doi:10.1016/j.ress.2012.12.022](https://doi.org/10.1016/j.ress.2012.12.022))
- **C1537.** Abstract This paper is of methodological nature, and deals with the foundations of Risk Assessment. *Regime: The study system, forcing, data and methods stated in the indexed abstract..* [literature_review_statement, mixed] (Gianfausto Salvadori 2016, [doi:10.1002/2015wr017225](https://doi.org/10.1002/2015wr017225))
- **C1552.** OWT (Offshore Wind Turbine) support structures are exposed to harsh ocean environment with significant uncertainties in soil properties and environmental loads. *Regime: The study system, forcing, data and methods stated in the indexed abstract..* [direct_finding, mixed] (L. Wang 2022, [doi:10.1016/j.rser.2022.112250](https://doi.org/10.1016/j.rser.2022.112250))

## Papers

- Wojciechowska (2013). Practical derivation of operational dike failure probabilities. *Reliability Engineering &amp; System Safety*. [doi:10.1016/j.ress.2012.12.022](https://doi.org/10.1016/j.ress.2012.12.022) [accepted manuscript, read only](https://repository.tudelft.nl/file/File_e3e60c37-e2aa-429b-8846-f935c02e420a)
- Gianfausto Salvadori (2016). A multivariate copula‐based framework for dealing with hazard scenarios and failure probabilities. *Water Resources Research*. [doi:10.1002/2015wr017225](https://doi.org/10.1002/2015wr017225) [published version, read only](https://onlinelibrary.wiley.com/doi/pdfdirect/10.1002/2015WR017225)
- L. Wang (2022). Reliability of offshore wind turbine support structures: A state-of-the-art review. *Renewable and Sustainable Energy Reviews*. [doi:10.1016/j.rser.2022.112250](https://doi.org/10.1016/j.rser.2022.112250) [published version, CC BY](https://www.sciencedirect.com/science/article/pii/S136403212200171X/pdf)
- La Peyre (2022). Long-term assessments are critical to determining persistence and shoreline protection from oyster reef nature-based coastal defenses. *Ecological Engineering*. [doi:10.1016/j.ecoleng.2022.106603](https://doi.org/10.1016/j.ecoleng.2022.106603) [published version, read only](https://www.lacoast.gov/crms/crms_public_data/publications/La%20Peyre%20et%20al%202022.pdf)
- Xiaoyuan Luo (2025). Framework for uncertainty quantification of wave–structure interaction in a flume. *Computational Particle Mechanics*. [doi:10.1007/s40571-025-00967-4](https://doi.org/10.1007/s40571-025-00967-4) [published version, CC BY](https://link.springer.com/content/pdf/10.1007/s40571-025-00967-4.pdf)
