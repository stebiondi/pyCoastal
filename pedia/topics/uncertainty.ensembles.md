# Ensemble and Bayesian methods

`uncertainty.ensembles` | Probabilistic inference and ensembles.

Parent: [Reliability and uncertainty](uncertainty.md)

Papers: 4. Claims: 3. Equations: 1.

## Synthesis

**Well established.** Coastal ensemble analysis propagates uncertain forcing, parameters, states, models and scenarios into distributions of hazards, impacts and decisions; probabilistic outputs are meaningful only when ensemble construction, dependence, weights and validation are explicit.

**Governing physics.** Aleatory variability in storms, waves, tides and climate combines with epistemic uncertainty in bathymetry, roughness, morphology, model structure and observations. Nonlinear thresholds, compound dependence and feedbacks can make output tails highly non-Gaussian and decision-sensitive.

**Dimensionless parameters.** Controls include ensemble size, coefficient of variation, effective sample size, variance-reduction factor, bias-to-sampling-error ratio, level refinement ratio, likelihood information content, posterior-to-prior variance, tail probability, reliability index and value-of-information ratio.

**Major equations.** Standard Monte Carlo estimates expectations and exceedance probabilities from samples; Bayesian inference updates prior parameter or state distributions with likelihoods, data assimilation conditions forecasts, and multilevel Monte Carlo combines many cheap coarse runs with fewer expensive fine runs to minimize variance at fixed cost.

**Typical methods.** Workflows define uncertainty sources and dependence, sample or design ensembles, run calibrated models at multiple fidelities, check convergence and tail stability, validate reliability and sharpness, decompose variance or sensitivity, update with observations and translate distributions into robust or adaptive decisions.

**Numerical models.** The set combines XBeach with multilevel Monte Carlo, inverse regional swell prediction with observation assimilation, and Monte Carlo damage simulation coupled to dynamic programming for adaptation timing.

**Experimental datasets.** Reviewed evidence includes theoretical and real XBeach runup and erosion cases, Southern California sheltered-wave observations used for inverse offshore-spectrum estimation, and Bay County building exposure under four sea-level-rise projections.

**Validated ranges.** The reported 40-or-greater multilevel speedup applies to tested XBeach cases and accuracy targets; inverse recovery depended on energetic unimodal swell and observation resolution; adaptation findings are conditional on Bay County buildings and four projections.

**Recent advances.** Recent advances combine multifidelity and multilevel ensembles, probabilistic machine-learning emulators, differentiable inference, active learning, particle and ensemble data assimilation, storylines, large climate ensembles and adaptive pathways that update as evidence changes.

**Disagreements.** Large ensembles reduce sampling error but do not correct structural bias or omitted scenarios. Bayesian posteriors can be dominated by priors or likelihood assumptions when data are sparse, and equal-weight multimodel ensembles need not represent calibrated probabilities.

**Limitations.** Computational cost, correlated members, underdispersive forcing, uncertain tails, nonstationarity, scenario incompleteness, surrogate bias, sparse validation, model discrepancy and dependence misspecification can create false precision. Decision results also depend on loss functions and update rules.

**Open questions.** Priorities include calibrated compound-event dependence, rare-event sampling, structural model discrepancy, adaptive multifidelity allocation, trustworthy surrogates, sequential observation design, nonstationary validation and decision-centered metrics for robust adaptation.

**Seminal papers.** Monte Carlo simulation established direct uncertainty propagation; Bayesian updating and ensemble Kalman methods enabled conditioning on observations, while importance sampling, polynomial chaos and multilevel Monte Carlo improved efficiency for rare or expensive coastal calculations.

## Equations

### Dynamic adaptation Bellman recursion

$$
V_t(s)=\min_a\{C_t(s,a)+\mathbb{E}[V_{t+1}(s')]\}
$$

Regime: Monetized building elevation or floodproofing decisions under sampled SLR and flood damage.

Variables: `V_t` minimum expected remaining lifecycle cost; `s` building and hazard state; `a` adaptation action; `C_t` current damage and adaptation cost; `s'` next state after hazard evolution and action

Source: (Han 2021, [doi:10.1016/j.crm.2021.100305](https://doi.org/10.1016/j.crm.2021.100305))

## Claims

- **C188.** In a Bay County building-level analysis, dynamic programming and Monte Carlo damage simulation across four sea-level-rise projections identified single- and multi-family buildings as most vulnerable and showed that adaptation decisions should update as projection information changes. *Regime: Bay County inventory, adopted depth-damage and cost functions, four SLR pathways, and monetized floodproofing/elevation options..* [direct_finding, numerical] (Han 2021, [doi:10.1016/j.crm.2021.100305](https://doi.org/10.1016/j.crm.2021.100305))
- **C367.** In Southern California swell cases, inverse assimilation of sheltered observations could recover peak offshore direction for an energetic unimodal event, but sparse low-directional-resolution coastal data could not routinely resolve offshore spectra without additional offshore constraints or restrictive priors. *Regime: Southern California Bight swell at 0.04-0.12 Hz using sheltered observations and offshore constraints..* [direct_finding, mixed] (W. C. O’Reilly 1998, [doi:10.1175/1520-0485(1998)028<0679:acwoir>2.0.co;2](https://doi.org/10.1175/1520-0485(1998)028<0679:acwoir>2.0.co;2))
- **C406.** In theoretical and real XBeach coastal-risk cases, multilevel Monte Carlo estimated runup and erosion uncertainty with speedup factors of 40 or more over standard Monte Carlo at the same accuracy, enabling exceedance probabilities for design decisions. *Regime: Theoretical and real coastal hydro-morphodynamic cases estimating runup and erosion distributions..* [direct_finding, numerical] (Mariana Clare 2022, [doi:10.1016/j.coastaleng.2022.104118](https://doi.org/10.1016/j.coastaleng.2022.104118))

## Papers

- W. C. O’Reilly (1998). Assimilating Coastal Wave Observations in Regional Swell Predictions. Part I: Inverse Methods. *Journal of Physical Oceanography*. [doi:10.1175/1520-0485(1998)028<0679:acwoir>2.0.co;2](https://doi.org/10.1175/1520-0485(1998)028<0679:acwoir>2.0.co;2)
- Mariana Clare (2022). Assessing erosion and flood risk in the coastal zone through the application of multilevel Monte Carlo methods. *Coastal Engineering*. [doi:10.1016/j.coastaleng.2022.104118](https://doi.org/10.1016/j.coastaleng.2022.104118)
- Han (2021). Building-level adaptation analysis under uncertain sea-level rise. *Climate Risk Management*. [doi:10.1016/j.crm.2021.100305](https://doi.org/10.1016/j.crm.2021.100305)
- Leon (2014). Incorporating DEM Uncertainty in Coastal Inundation Mapping. *PLoS ONE*. [doi:10.1371/journal.pone.0108727](https://doi.org/10.1371/journal.pone.0108727)
