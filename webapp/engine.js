/*
 * pyCoastal engineering core, ported to JavaScript.
 *
 * This is a transliteration of the Python, function for function, so the
 * browser can run a design without a Python runtime. It is not a rewrite:
 * where the Python bisects, this bisects; where the Python iterates on the
 * base width, this iterates on the base width.
 *
 * A transliteration is only worth anything if it can be shown to agree with
 * the original, so `make_vectors.py` dumps reference cases straight out of
 * pyCoastal and `verify_engine.py` runs this file against them. The app
 * re-runs the same check in the browser on load and says so on screen: a
 * second implementation that nobody checks is a liability, not a feature.
 *
 * Units follow the Python: metres, seconds, newtons, and litres per second
 * per metre for overtopping.
 */

var G = 9.81;
var RHO_W = 1025.0;
var RHO_C = 2400.0;
var RHO_S = 2650.0;
var KNOT = 0.514444;
var RHO_CONCRETE = 2400.0;
/* Tm-1,0 / Tm for a JONSWAP spectrum: Tp = 1.1 Tm-1,0 = 1.28 Tm. */
var SPECTRAL_TO_MEAN_PERIOD = 1.28 / 1.1;

/* ------------------------------------------------------------------ */
/* Waves                                                               */
/* ------------------------------------------------------------------ */

/* Linear dispersion by Newton-Raphson, from the Fenton and McKee (1990)
 * start. The fixed-point form this replaced in the Python diverged. */
function dispersion(T, h, tol) {
  tol = tol === undefined ? 1e-12 : tol;
  if (!(T > 0) || !(h > 0)) throw new Error("Period and depth must be positive");
  var omega = 2 * Math.PI / T;
  var k0 = omega * omega / G;
  var k = k0 / Math.pow(Math.tanh(Math.pow(k0 * h, 0.75)), 2 / 3);
  for (var i = 0; i < 100; i++) {
    var th = Math.tanh(k * h);
    var f = G * k * th - omega * omega;
    var df = G * th + G * k * h * (1 - th * th);
    var dk = f / df;
    k -= dk;
    if (Math.abs(dk) < tol * Math.abs(k)) break;
  }
  return 2 * Math.PI / k;
}

function conditionsFromPeak(Hm0, Tp, depth, stormDuration) {
  return makeConditions(Hm0, Tp / 1.1, depth, stormDuration);
}

function makeConditions(Hm0, Tm10, depth, stormDuration) {
  if (!(Hm0 > 0)) throw new Error("Wave height must be positive");
  if (!(Tm10 > 0)) throw new Error("Wave period must be positive");
  if (!(depth > 0)) throw new Error("Depth must be positive");
  stormDuration = stormDuration === undefined ? 6 * 3600 : stormDuration;
  var c = {
    Hm0: Hm0, Tm10: Tm10, depth: depth, storm_duration: stormDuration
  };
  c.mean_period = Tm10 / SPECTRAL_TO_MEAN_PERIOD;
  c.wave_count = Math.min(stormDuration / c.mean_period, 7500.0);
  c.meanSteepness = function () {
    return c.Hm0 / (G * c.mean_period * c.mean_period / (2 * Math.PI));
  };
  c.L0 = G * Tm10 * Tm10 / (2 * Math.PI);
  c.wavelength = dispersion(Tm10, depth);
  c.breakerParameter = function (cotAlpha) {
    var s0 = c.Hm0 / c.L0;
    return (1.0 / cotAlpha) / Math.sqrt(s0);
  };
  return c;
}

/* ------------------------------------------------------------------ */
/* Roughness and tolerable discharge                                   */
/* ------------------------------------------------------------------ */

var ROUGHNESS_FACTORS = {
  smooth_concrete: 1.0, grass: 1.0, asphalt: 1.0,
  rock_one_layer_impermeable: 0.6, rock_two_layer_impermeable: 0.55,
  rock_two_layer_permeable: 0.4, cubes_one_layer_flat: 0.49,
  cubes_two_layer_random: 0.47, antifer: 0.47, tetrapod: 0.38,
  accropode: 0.46, core_loc: 0.44, xbloc: 0.45, dolos: 0.43
};

var TOLERABLE_DISCHARGE = {
  pedestrians_unaware: [0.03, "Unaware pedestrians, narrow walkway, clear view of the sea"],
  pedestrians_aware: [0.1, "Aware pedestrians, able to see and avoid the hazard"],
  trained_staff: [1.0, "Trained staff, well shod and protected, wide walkway"],
  buildings_structural: [1.0, "Structural damage to buildings behind the defence"],
  vehicles_low_speed: [10.0, "Vehicles at low speed on a road behind the crest"],
  vehicles_moderate_speed: [50.0, "Driving at moderate speed, overtopping by pulsating flows"],
  embankment_seaward: [50.0, "Damage to a maintained grass or armoured embankment"],
  harbour_quay_equipment: [0.4, "Damage to equipment set back 5 to 10 m from the crest"]
};

/* ------------------------------------------------------------------ */
/* Rock armour                                                         */
/* ------------------------------------------------------------------ */

function rockArmourVanDerMeer(c, cotAlpha, opts) {
  opts = opts || {};
  var Delta = opts.Delta === undefined ? 1.585 : opts.Delta;
  var P = opts.permeability === undefined ? 0.4 : opts.permeability;
  var S = opts.damage === undefined ? 2.0 : opts.damage;
  var safety = opts.safety_factor === undefined ? 1.0 : opts.safety_factor;
  var ratio = opts.height_ratio === undefined ? 1.4 : opts.height_ratio;

  if (!(cotAlpha > 0)) throw new Error("cot(alpha) must be positive");
  if (!(P > 0 && P <= 0.7)) throw new Error("Permeability P must be in (0, 0.7]");
  if (!(S > 0)) throw new Error("Damage level S must be positive");
  if (!(ratio >= 1)) throw new Error("H2%/Hs must be at least 1");

  /* Van der Meer as modified by Van Gent et al. (2003): Tm-1,0 and H2%. */
  var N = c.wave_count;
  var xi = c.breakerParameter(cotAlpha);
  var tanAlpha = 1.0 / cotAlpha;
  var cp = 8.4 / safety;
  var cs = 1.3 / safety;
  var xiCr = Math.pow((cp / cs) * Math.pow(P, 0.31) * Math.sqrt(tanAlpha),
                      1.0 / (P + 0.5));
  var damageTerm = Math.pow(S / Math.sqrt(N), 0.2) / ratio;

  var regime, stability;
  if (xi < xiCr) {
    regime = "plunging";
    stability = cp * Math.pow(P, 0.18) * damageTerm * Math.pow(xi, -0.5);
  } else {
    regime = "surging";
    stability = cs * Math.pow(P, -0.13) * damageTerm *
                Math.sqrt(cotAlpha) * Math.pow(xi, P);
  }
  var Dn50 = c.Hm0 / (Delta * stability);
  return {
    Dn50: Dn50, M50: RHO_S * Dn50 * Dn50 * Dn50, regime: regime,
    xi: xi, xi_cr: xiCr, stability_number: stability
  };
}

function armourLayer(Dn50, nLayers, layerCoefficient, porosity, density) {
  nLayers = nLayers === undefined ? 2 : nLayers;
  layerCoefficient = layerCoefficient === undefined ? 1.0 : layerCoefficient;
  porosity = porosity === undefined ? 0.37 : porosity;
  density = density === undefined ? RHO_S : density;
  var thickness = nLayers * layerCoefficient * Dn50;
  var perArea = nLayers * layerCoefficient * (1 - porosity) / (Dn50 * Dn50);
  return {
    thickness: thickness, stones_per_m2: perArea,
    mass_per_m2: perArea * density * Dn50 * Dn50 * Dn50
  };
}

var CONCRETE_UNITS = {
  cubes_two_layer_random: { formula: "cubes", layers: 2, k: 1.10, porosity: 0.47, cot: 1.5 },
  cubes_one_layer_flat: { formula: "cubes", layers: 1, k: 1.00, porosity: 0.30, cot: 1.5 },
  antifer: { formula: "cubes", layers: 2, k: 1.10, porosity: 0.46, cot: 1.5 },
  tetrapod: { formula: "tetrapods", layers: 2, k: 1.04, porosity: 0.50, cot: 1.5 },
  accropode: { formula: "Ns", Ns: 2.7, layers: 1, k: 1.51, porosity: 0.52, cot: 1.33 },
  core_loc: { formula: "Ns", Ns: 2.8, layers: 1, k: 1.51, porosity: 0.60, cot: 1.33 },
  xbloc: { formula: "Ns", Ns: 2.8, layers: 1, k: 1.40, porosity: 0.58, cot: 1.33 },
  dolos: { formula: "hudson", KD: 16.0, layers: 2, k: 0.94, porosity: 0.56, cot: 2.0 }
};

function fmtG(v) { return String(Number(v.toPrecision(6))); }

function concreteArmour(c, unit, cotAlpha, opts) {
  opts = opts || {};
  var damage = opts.damage === undefined ? 0.5 : opts.damage;
  var density = opts.density === undefined ? RHO_CONCRETE : opts.density;
  var safety = opts.safety_factor === undefined ? 1.0 : opts.safety_factor;
  if (!(unit in CONCRETE_UNITS)) throw new Error("Unknown concrete unit " + unit);
  if (!(damage > 0)) throw new Error("Damage Nod must be positive");
  var spec = CONCRETE_UNITS[unit];
  var Delta = density / RHO_W - 1.0;
  var N = c.wave_count;
  var som = c.meanSteepness();
  var Ns, source;
  if (spec.formula === "cubes") {
    Ns = (6.7 * Math.pow(damage, 0.4) / Math.pow(N, 0.3) + 1.0) * Math.pow(som, -0.1);
    source = "Van der Meer (1988), cubes";
  } else if (spec.formula === "tetrapods") {
    Ns = (3.75 * Math.pow(damage, 0.5) / Math.pow(N, 0.25) + 0.85) * Math.pow(som, -0.2);
    source = "Van der Meer (1988), tetrapods";
  } else if (spec.formula === "Ns") {
    Ns = spec.Ns;
    source = "design Ns = " + fmtG(spec.Ns);
  } else {
    Ns = Math.pow(spec.KD * cotAlpha, 1 / 3);
    source = "Hudson, KD = " + fmtG(spec.KD);
  }
  Ns /= safety;
  var Dn = c.Hm0 / (Delta * Ns);
  var note = null;
  if (Math.abs(cotAlpha - spec.cot) > 0.26) {
    note = unit.replace(/_/g, " ") + " stability was established on a 1:" +
      fmtG(spec.cot) + " slope; this section is 1:" + fmtG(cotAlpha) + ".";
  }
  return {
    Dn50: Dn, M50: density * Dn * Dn * Dn, stability_number: Ns,
    source: source, Delta: Delta, density: density, slope_note: note,
    xi: c.breakerParameter(cotAlpha)
  };
}

function layerFor(armour, Dn50, density) {
  var spec = CONCRETE_UNITS[armour];
  if (!spec) return armourLayer(Dn50, 2, 1.0, 0.37, density);
  return armourLayer(Dn50, spec.layers, spec.k, spec.porosity, density);
}

/* ------------------------------------------------------------------ */
/* Overtopping                                                         */
/* ------------------------------------------------------------------ */

function overtoppingSloped(c, Rc, cotAlpha, gf, gbeta, gb, gv) {
  gf = gf === undefined ? 1 : gf;
  gbeta = gbeta === undefined ? 1 : gbeta;
  gb = gb === undefined ? 1 : gb;
  gv = gv === undefined ? 1 : gv;
  if (!(Rc > 0)) throw new Error("These formulae need a positive freeboard");

  var Hm0 = c.Hm0;
  var xi = c.breakerParameter(cotAlpha);
  var tanAlpha = 1.0 / cotAlpha;
  var scale = Math.sqrt(G * Hm0 * Hm0 * Hm0);

  var breaking = (0.023 / Math.sqrt(tanAlpha)) * gb * xi *
    Math.exp(-Math.pow(2.7 * Rc / (xi * Hm0 * gb * gf * gbeta * gv), 1.3));
  var nonBreaking = 0.09 *
    Math.exp(-Math.pow(1.5 * Rc / (Hm0 * gf * gbeta), 1.3));

  var qStar, governing;
  if (breaking <= nonBreaking) { qStar = breaking; governing = "breaking"; }
  else { qStar = nonBreaking; governing = "non-breaking"; }

  return {
    q: qStar * scale * 1000.0, q_dimensionless: qStar,
    governing: governing, xi: xi, relative_freeboard: Rc / Hm0
  };
}

function overtoppingVertical(c, Rc, gbeta) {
  gbeta = gbeta === undefined ? 1 : gbeta;
  if (!(Rc > 0)) throw new Error("Needs a positive freeboard");
  var Hm0 = c.Hm0, h = c.depth;
  var hStar = 1.35 * (h / Hm0) * (2 * Math.PI * h / (G * c.Tm10 * c.Tm10));
  var qStar = 0.047 * Math.exp(-Math.pow(2.35 * Rc / (Hm0 * gbeta), 1.3));
  return {
    q: qStar * Math.sqrt(G * Hm0 * Hm0 * Hm0) * 1000.0,
    q_dimensionless: qStar, h_star: hStar, impulsive: hStar < 0.23,
    relative_freeboard: Rc / Hm0
  };
}

function overtoppingWithUncertainty(result, factor) {
  factor = factor === undefined ? 3.0 : factor;
  var q = result.q;
  return { q_mean: q, q_lower: q / factor, q_upper: q * factor };
}

/* Bisection, exactly as the Python does it: the two branches make an
 * analytic inverse awkward and a solver is not worth the risk. */
function requiredCrestFreeboard(c, qAllowable, cotAlpha, opts) {
  opts = opts || {};
  var gf = opts.gamma_f === undefined ? 1 : opts.gamma_f;
  var gbeta = opts.gamma_beta === undefined ? 1 : opts.gamma_beta;
  var gb = opts.gamma_b === undefined ? 1 : opts.gamma_b;
  var gv = opts.gamma_v === undefined ? 1 : opts.gamma_v;
  var vertical = !!opts.vertical;
  var tolerance = opts.tolerance === undefined ? 1e-4 : opts.tolerance;
  if (!(qAllowable > 0)) throw new Error("Allowable discharge must be positive");

  function discharge(Rc) {
    return vertical ? overtoppingVertical(c, Rc, gbeta).q
                    : overtoppingSloped(c, Rc, cotAlpha, gf, gbeta, gb, gv).q;
  }

  var low = 1e-3, high = 1.0;
  while (discharge(high) > qAllowable) {
    high *= 2.0;
    if (high > 1000.0 * c.Hm0) {
      throw new Error("No freeboard within 1000 Hm0 achieves the allowable discharge.");
    }
  }
  while (high - low > tolerance) {
    var mid = 0.5 * (low + high);
    if (discharge(mid) > qAllowable) low = mid; else high = mid;
  }
  return high;
}

function assessOvertopping(q) {
  var keys = Object.keys(TOLERABLE_DISCHARGE);
  keys.sort(function (a, b) {
    return TOLERABLE_DISCHARGE[a][0] - TOLERABLE_DISCHARGE[b][0];
  });
  return keys.map(function (k) {
    return {
      key: k, limit: TOLERABLE_DISCHARGE[k][0],
      description: TOLERABLE_DISCHARGE[k][1],
      acceptable: q <= TOLERABLE_DISCHARGE[k][0]
    };
  });
}

/* ------------------------------------------------------------------ */
/* Rubble mound                                                        */
/* ------------------------------------------------------------------ */

function depthLimitWarnings(c) {
  var ratio = c.Hm0 / c.depth;
  if (ratio > 0.6) {
    return ["Hm0 = " + c.Hm0.toFixed(2) + " m is " + ratio.toFixed(2) + " of the " +
      c.depth.toFixed(1) + " m toe depth. A significant height above about 0.6 h " +
      "cannot reach the toe without breaking; the design wave and the depth are " +
      "inconsistent and the sizing is not meaningful until one of them is corrected."];
  }
  if (ratio > 0.2) {
    return ["Hm0/h = " + ratio.toFixed(2) + ": the toe is in shallow water. H2% is " +
      "taken as 1.4 Hs from the Rayleigh distribution, which overstates it here " +
      "and errs on the heavy side; Battjes and Groenendijk (2000) with the " +
      "foreshore slope gives the real ratio."];
  }
  return [];
}

function designRubbleMound(c, opts) {
  opts = opts || {};
  var cotAlpha = opts.cot_alpha === undefined ? 2.0 : opts.cot_alpha;
  var armour = opts.armour || "rock_two_layer_permeable";
  var damage = opts.damage === undefined ? 2.0 : opts.damage;
  var P = opts.permeability === undefined ? 0.4 : opts.permeability;
  var Delta = opts.Delta === undefined ? 1.585 : opts.Delta;
  var use = opts.tolerable_use || "trained_staff";
  var safety = opts.safety_factor === undefined ? 1.0 : opts.safety_factor;
  var scatter = opts.scatter_factor === undefined ? 3.0 : opts.scatter_factor;
  var unitDamage = opts.unit_damage === undefined ? 0.5 : opts.unit_damage;
  var concreteDensity = opts.concrete_density === undefined ? RHO_CONCRETE : opts.concrete_density;

  if (!(armour in ROUGHNESS_FACTORS)) throw new Error("Unknown armour " + armour);
  if (!(use in TOLERABLE_DISCHARGE)) throw new Error("Unknown use " + use);

  var warnings = depthLimitWarnings(c);
  var stability, regime, density;
  if (armour in CONCRETE_UNITS) {
    stability = concreteArmour(c, armour, cotAlpha, {
      damage: unitDamage, density: concreteDensity, safety_factor: safety
    });
    regime = stability.source;
    density = concreteDensity;
    if (stability.slope_note) warnings.push(stability.slope_note);
  } else {
    stability = rockArmourVanDerMeer(c, cotAlpha, {
      Delta: Delta, permeability: P, damage: damage, safety_factor: safety
    });
    regime = stability.regime;
    density = RHO_W * (1 + Delta);
  }
  var gf = ROUGHNESS_FACTORS[armour];
  var qLimit = TOLERABLE_DISCHARGE[use][0];

  var Rc = requiredCrestFreeboard(c, qLimit / scatter, cotAlpha, { gamma_f: gf });
  var q = overtoppingSloped(c, Rc, cotAlpha, gf);
  var band = overtoppingWithUncertainty(q, scatter);
  var M50 = density * Math.pow(stability.Dn50, 3);

  return {
    conditions: c, cot_alpha: cotAlpha, Dn50: stability.Dn50,
    M50: M50, regime: regime, xi: stability.xi,
    crest_freeboard: Rc, q_mean: band.q_mean, q_upper: band.q_upper,
    layer: layerFor(armour, stability.Dn50, density), armour_type: armour,
    governing_limit: use, density: density, warnings: warnings,
    concrete: armour in CONCRETE_UNITS,
    underlayer_Dn50: Math.pow(M50 / 10 / RHO_S, 1 / 3)
  };
}

/* ------------------------------------------------------------------ */
/* Seawall                                                             */
/* ------------------------------------------------------------------ */

function godaBreakingHeight(T, depth, slope, coefficient) {
  coefficient = coefficient === undefined ? 0.17 : coefficient;
  if (!(T > 0) || !(depth > 0)) throw new Error("Period and depth must be positive");
  var L0 = G * T * T / (2 * Math.PI);
  return coefficient * L0 * (1 - Math.exp(-1.5 * Math.PI * depth / L0 *
    (1 + 15 * Math.pow(Math.abs(slope), 4 / 3))));
}

function godaPressures(o) {
  var Hm0 = o.Hm0, T = o.T, depth = o.depth;
  var wallToeDepth = o.wall_toe_depth;
  var bermDepth = o.berm_depth === undefined ? null : o.berm_depth;
  var Rc = o.crest_freeboard === undefined ? 5.0 : o.crest_freeboard;
  var betaDeg = o.beta_degrees === undefined ? 0.0 : o.beta_degrees;
  var slope = o.slope === undefined ? 1 / 30 : o.slope;
  var HmaxFactor = o.Hmax_factor === undefined ? 1.8 : o.Hmax_factor;
  var depthLimit = o.depth_limit === undefined ? true : o.depth_limit;

  if (!(Hm0 > 0)) throw new Error("Hm0 must be positive");
  if (!(T > 0)) throw new Error("T must be positive");
  if (!(depth > 0)) throw new Error("depth must be positive");
  if (!(wallToeDepth > 0)) throw new Error("Wall toe depth must be positive");

  var d = bermDepth === null ? wallToeDepth : bermDepth;
  if (!(d > 0)) throw new Error("Berm depth must be positive");

  var beta = betaDeg * Math.PI / 180;
  var hb = depth + 5.0 * Hm0 * slope;
  var Hmax = HmaxFactor * Hm0;
  var breaking = depthLimit ? godaBreakingHeight(T, hb, slope) : null;
  if (breaking !== null) Hmax = Math.min(Hmax, breaking);
  var L = dispersion(T, depth);
  var kh = 2 * Math.PI * depth / L;

  var alpha1 = 0.6 + 0.5 * Math.pow(2 * kh / Math.sinh(2 * kh), 2);
  var alpha2 = Math.min((hb - d) / (3.0 * hb) * Math.pow(Hmax / d, 2),
                        2.0 * d / Hmax);
  var alpha3 = 1.0 - (wallToeDepth / depth) * (1.0 - 1.0 / Math.cosh(kh));

  var etaStar = 0.75 * (1 + Math.cos(beta)) * Hmax;
  var p1 = 0.5 * (1 + Math.cos(beta)) *
           (alpha1 + alpha2 * Math.pow(Math.cos(beta), 2)) * RHO_W * G * Hmax;
  var p3 = alpha3 * p1;
  var hcStar = Math.min(etaStar, Rc);
  var p4 = etaStar > 0 ? p1 * (1 - hcStar / etaStar) : 0;
  var pu = 0.5 * (1 + Math.cos(beta)) * alpha1 * alpha3 * RHO_W * G * Hmax;

  var Fabove = 0.5 * (p1 + p4) * hcStar;
  var Fbelow = 0.5 * (p1 + p3) * wallToeDepth;
  var F = Fabove + Fbelow;
  var armAbove = wallToeDepth + hcStar * (2 * p1 + p4) / (3 * (p1 + p4));
  var armBelow = wallToeDepth * (p1 + 2 * p3) / (3 * (p1 + p3));
  var arm = F > 0 ? (Fabove * armAbove + Fbelow * armBelow) / F : 0;

  return {
    p1: p1 / 1000, p3: p3 / 1000, p4: p4 / 1000, pu: pu / 1000,
    eta_star: etaStar, hc_star: hcStar, Hmax: Hmax, breaking_height: breaking,
    depth_limited: breaking !== null && Hmax < HmaxFactor * Hm0,
    wavelength: L, alpha1: alpha1, alpha2: alpha2, alpha3: alpha3,
    F: F / 1000, arm: arm, U_per_width: 0.5 * pu / 1000
  };
}

function scourDepthVerticalWall(Hm0, T, depth, coefficient) {
  coefficient = coefficient === undefined ? 0.4 : coefficient;
  if (coefficient < 0) throw new Error("Coefficient must be non-negative");
  var L = dispersion(T, depth);
  var kh = 2 * Math.PI * depth / L;
  return coefficient * Hm0 / Math.pow(Math.sinh(kh), 1.35);
}

function toeStoneSize(Hm0, toeDepth, waterDepth, Delta, damage) {
  Delta = Delta === undefined ? 1.585 : Delta;
  damage = damage === undefined ? 0.5 : damage;
  if (!(toeDepth > 0) || !(waterDepth > 0)) throw new Error("Depths must be positive");
  if (!(damage > 0)) throw new Error("Damage number must be positive");
  var ratio = toeDepth / waterDepth;
  var stability = (2.0 + 6.2 * Math.pow(ratio, 2.7)) * Math.pow(damage, 0.15);
  var Dn50 = Hm0 / (Delta * stability);
  return {
    Dn50: Dn50, M50: RHO_S * Dn50 * Dn50 * Dn50,
    stability_number: stability, depth_ratio: ratio,
    within_range: ratio >= 0.4 - 1e-9 && ratio <= 0.9 + 1e-9
  };
}

function toeStoneTanimoto(Hs, T, bermDepth, bermWidth, Delta, betaDeg, alphaS) {
  Delta = Delta === undefined ? 1.585 : Delta;
  betaDeg = betaDeg === undefined ? 0 : betaDeg;
  alphaS = alphaS === undefined ? 0.45 : alphaS;
  if (!(Hs > 0) || !(T > 0)) throw new Error("Wave height and period must be positive");
  if (!(bermDepth > 0) || bermWidth < 0) {
    throw new Error("Berm depth must be positive and width non-negative");
  }
  var L = dispersion(T, bermDepth);
  var twoKh = 4 * Math.PI * bermDepth / L;
  var kappa1 = twoKh / Math.sinh(twoKh);
  var beta = betaDeg * Math.PI / 180;
  var a = 2 * Math.PI * bermWidth / L * Math.cos(beta);
  var kappa2 = Math.max(alphaS * Math.pow(Math.sin(beta), 2) * Math.pow(Math.cos(a), 2),
                        Math.pow(Math.cos(beta), 2) * Math.pow(Math.sin(a), 2));
  var kappa = Math.max(kappa1 * kappa2, 1e-6);
  var r = bermDepth / Hs;
  var root = Math.pow(kappa, 1 / 3);
  var Ns = Math.max(1.8, 1.3 * (1 - kappa) / root * r +
    1.8 * Math.exp(-1.5 * Math.pow(1 - kappa, 2) / root * r));
  var Dn50 = Hs / (Delta * Ns);
  return { Dn50: Dn50, M50: RHO_S * Dn50 * Dn50 * Dn50, stability_number: Ns,
           kappa: kappa, wavelength: L };
}

function slidingSafety(F, weight, uplift, friction) {
  friction = friction === undefined ? 0.6 : friction;
  if (!(F > 0)) throw new Error("Horizontal force must be positive");
  var net = weight - uplift;
  if (net <= 0) return 0.0;
  return friction * net / F;
}

function overturningSafety(F, arm, restoringMoment, uplift, baseWidth) {
  if (!(F > 0) || !(arm > 0)) throw new Error("Overturning needs a positive force and lever arm");
  if (!(baseWidth > 0)) throw new Error("Base width must be positive");
  var net = restoringMoment - uplift * (2 / 3) * baseWidth;
  if (net <= 0) return 0.0;
  return net / (F * arm);
}

function bearingPressures(normal, baseWidth, netMoment) {
  if (!(baseWidth > 0)) throw new Error("Base width must be positive");
  if (normal <= 0) {
    return { p_max: Infinity, p_min: 0, e: NaN, middle_third: false };
  }
  var xRes = netMoment / normal;
  var e = 0.5 * baseWidth - xRes;
  if (Math.abs(e) <= baseWidth / 6) {
    return {
      p_max: normal / baseWidth * (1 + 6 * Math.abs(e) / baseWidth),
      p_min: normal / baseWidth * (1 - 6 * Math.abs(e) / baseWidth),
      e: e, middle_third: true
    };
  }
  var a = Math.min(xRes, baseWidth - xRes);
  if (a <= 0) return { p_max: Infinity, p_min: 0, e: e, middle_third: false };
  return { p_max: 2 * normal / (3 * a), p_min: 0, e: e, middle_third: false };
}

var F_CK = 35.0, F_YK = 500.0, REINFORCEMENT_RATIO = 0.01;
var COVER_TO_STEEL = 0.10, ULS_FACTOR = 1.35, L_WALL_PRACTICAL_HEIGHT = 8.0;

function upliftUnder(frontHead, backHead, baseWidth) {
  var hf = Math.max(frontHead, 0), hb = Math.max(backHead, 0);
  var force = 0.5 * GAMMA_W * (hf + hb) * baseWidth;
  if (hf + hb <= 0) return { force: 0, x: 0.5 * baseWidth };
  return { force: force, x: baseWidth * (hf + 2 * hb) / (3 * (hf + hb)) };
}

function stemSection(moment, shear, fck, fyk, rho, cover) {
  fck = fck === undefined ? F_CK : fck;
  fyk = fyk === undefined ? F_YK : fyk;
  rho = rho === undefined ? REINFORCEMENT_RATIO : rho;
  cover = cover === undefined ? COVER_TO_STEEL : cover;
  if (moment < 0 || shear < 0) throw new Error("Design moment and shear must be non-negative");
  var fyd = fyk / 1.15;
  var dM = moment > 0 ? Math.sqrt(moment * 1e3 / (0.9 * rho * fyd * 1e6)) : 0;
  var dV = 0.2;
  for (var i = 0; i < 50; i++) {
    var k = Math.min(1 + Math.sqrt(200 / (dV * 1000)), 2);
    var vrd = Math.max(0.12 * k * Math.pow(100 * rho * fck, 1 / 3),
                       0.035 * Math.pow(k, 1.5) * Math.sqrt(fck));
    var next = shear * 1e3 / (vrd * 1e6);
    if (Math.abs(next - dV) < 1e-5) { dV = next; break; }
    dV = Math.max(next, 0.05);
  }
  var dReq = Math.max(dM, dV);
  var thickness = Math.ceil((dReq + cover) / 0.05 - 1e-9) * 0.05;
  return { d_bending: dM, d_shear: dV, thickness: thickness, moment: moment, shear: shear };
}

function stemLoads(backfill, pressures, waveArm, baseThickness, retained,
                   waterTable, surcharge, trough, swl, baseTop) {
  if (retained <= 0) return [0, 0];
  var atRest = lateralEarthForce(backfill, retained, waterTable, surcharge, "at_rest");
  var active = lateralEarthForce(backfill, retained, waterTable, surcharge, "active");
  var frontTrough = hydrostaticForce(Math.max(trough - baseTop, 0));
  var frontSwl = hydrostaticForce(Math.max(swl - baseTop, 0));
  var Vout = atRest.total - frontTrough.force;
  var Mout = atRest.moment - frontTrough.force * frontTrough.arm;
  var F = pressures.F;
  var arm = Math.max(waveArm - baseThickness, 0);
  var Vin = F + frontSwl.force - active.total;
  var Min = F * arm + frontSwl.force * frontSwl.arm - active.moment;
  return [Math.max(Math.abs(Mout), Math.abs(Min)), Math.max(Math.abs(Vout), Math.abs(Vin))];
}

function designSeawall(c, stillWaterLevel, seabedLevel, opts) {
  opts = opts || {};
  var use = opts.tolerable_use || "pedestrians_aware";
  var betaDeg = opts.beta_degrees === undefined ? 0 : opts.beta_degrees;
  var friction = opts.friction === undefined ? 0.6 : opts.friction;
  var targetSliding = opts.target_sliding === undefined ? 1.2 : opts.target_sliding;
  var targetOverturning = opts.target_overturning === undefined ? 1.5 : opts.target_overturning;
  var requireMiddleThird = opts.require_middle_third === undefined ? true : opts.require_middle_third;
  var allowable = opts.allowable_bearing === undefined ? 300.0 : opts.allowable_bearing;
  var scourCoefficient = opts.scour_coefficient === undefined ? 0.4 : opts.scour_coefficient;
  var minEmbedment = opts.minimum_embedment === undefined ? 1.0 : opts.minimum_embedment;
  var maxEmbedment = opts.maximum_embedment === undefined ? 3.0 : opts.maximum_embedment;
  var stemThickness = opts.stem_thickness === undefined ? 0.5 : opts.stem_thickness;
  var baseThickness = opts.base_thickness === undefined ? 0.6 : opts.base_thickness;
  var promenadeFreeboard = opts.promenade_freeboard === undefined ? 1.0 : opts.promenade_freeboard;
  var fixedWidth = opts.toe_berm_width === undefined ? null : opts.toe_berm_width;
  var seabedSlope = opts.seabed_slope === undefined ? 1 / 30 : opts.seabed_slope;
  var scatter = opts.scatter_factor === undefined ? 3.0 : opts.scatter_factor;
  var maxBaseWidth = opts.max_base_width === undefined ? 30.0 : opts.max_base_width;
  var step = opts.step === undefined ? 0.1 : opts.step;
  var backfill = sediment(opts.backfill || "medium_sand");
  var waterTable = opts.water_table === undefined ? 0.0 : opts.water_table;
  var surcharge = opts.surcharge === undefined ? 10.0 : opts.surcharge;
  var drivingKind = opts.earth_pressure_driving || "at_rest";
  var resistingKind = opts.earth_pressure_resisting || "active";
  var creditEarth = opts.credit_earth_pressure === undefined ? true : opts.credit_earth_pressure;
  var drawdownLevel = opts.drawdown_level === undefined ? null : opts.drawdown_level;

  if (stillWaterLevel <= seabedLevel) throw new Error("Still water level must be above the seabed");
  if (!(use in TOLERABLE_DISCHARGE)) throw new Error("Unknown use " + use);
  if (!(step > 0)) throw new Error("Sizing step must be positive");
  if (allowable !== null && !(allowable > 0)) throw new Error("Allowable bearing must be positive");

  var warnings = [];
  var depth = stillWaterLevel - seabedLevel;
  var Tgoda = c.Tm10 * 1.1;

  /* 1. Crest level, against the upper bound of the scatter band. */
  var qLimit = TOLERABLE_DISCHARGE[use][0];
  var Rc = requiredCrestFreeboard(c, qLimit / scatter, 0.0, { vertical: true });
  var crestLevel = stillWaterLevel + Rc;
  var q = overtoppingVertical(c, Rc);
  var band = overtoppingWithUncertainty(q, scatter);
  if (q.impulsive) {
    warnings.push("h* = " + q.h_star.toFixed(2) + " is below 0.23, so the " +
      "conditions are impulsive. The non-impulsive EurOtop formula used for the " +
      "crest level understates the discharge, and Goda understates the load; " +
      "check against the impulsive formulae before fixing the section.");
  }

  /* 2. Founding level. */
  var scour = scourDepthVerticalWall(c.Hm0, Tgoda, depth, scourCoefficient);
  var embedment = Math.min(Math.max(scour, minEmbedment), maxEmbedment);
  var foundingLevel = seabedLevel - embedment;
  if (scour > maxEmbedment) {
    warnings.push("Predicted scour " + scour.toFixed(2) + " m exceeds the " +
      fmtG(maxEmbedment) + " m embedment limit. The section relies on the toe " +
      "protection to keep the scour hole away from the wall.");
  }

  /* 3. Toe protection, Tanimoto in front of a vertical wall. */
  var toeThickness = 0.8;
  var width = fixedWidth !== null ? fixedWidth : 2.0;
  var toe = null;
  for (var t = 0; t < 20; t++) {
    toe = toeStoneTanimoto(c.Hm0, Tgoda, Math.max(depth - toeThickness, 0.2 * depth),
                           width, 1.585, betaDeg);
    var newThickness = Math.max(2.0 * toe.Dn50, 0.5);
    var newWidth = fixedWidth !== null ? fixedWidth
      : Math.max(3.0 * toe.Dn50, 0.4 * c.Hm0, 2.0);
    if (Math.abs(newThickness - toeThickness) < 1e-4 && Math.abs(newWidth - width) < 1e-4) break;
    toeThickness = newThickness;
    width = newWidth;
  }
  var toeBermWidth = width;
  var bermDepth = Math.max(depth - toeThickness, 0.2 * depth);
  var quarter = 0.25 * dispersion(Tgoda, depth);
  if (toeBermWidth < quarter) {
    warnings.push("The " + toeBermWidth.toFixed(1) + " m toe berm sits close to the " +
      "wall, where the standing wave moves the bed least, which is why Tanimoto " +
      "allows " + (toe.M50 / 1000).toFixed(2) + " t stone. The scour hole forms " +
      "about a quarter wavelength out, " + quarter.toFixed(0) + " m from the face; " +
      "widen the berm to reach it if the toe is also the scour protection, and the " +
      "stone will grow.");
  }

  /* 4. Wave pressures; they do not depend on the base width. */
  var pressures = godaPressures({
    Hm0: c.Hm0, T: Tgoda, depth: depth, wall_toe_depth: depth,
    berm_depth: bermDepth, crest_freeboard: Rc, beta_degrees: betaDeg,
    slope: seabedSlope
  });
  var waveArm = pressures.arm + embedment;
  var F = pressures.F;

  var promenadeLevel = crestLevel - promenadeFreeboard;
  var retainedHeight = promenadeLevel - foundingLevel;
  var ceiling = Math.max(promenadeLevel - stillWaterLevel, 0);
  if (waterTable > ceiling + 1e-9) {
    warnings.push("A water table " + waterTable.toFixed(2) + " m below the promenade " +
      "would sit below the still water level, which the sea keeps the fill up to; " +
      ceiling.toFixed(2) + " m is used.");
  }
  var table = Math.min(waterTable, ceiling);
  var backWaterLevel = promenadeLevel - table;
  var earthDriving = lateralEarthForce(backfill, retainedHeight, table, surcharge, drivingKind);
  var earthResisting = lateralEarthForce(backfill, retainedHeight, table, surcharge, resistingKind);
  if (!creditEarth) {
    earthResisting = {
      soil: 0, water: 0, total: 0, moment: 0, arm: 0,
      K: earthResisting.K, kind: earthResisting.kind,
      diagram: earthResisting.diagram, water_fraction: 0
    };
  }

  var trough = Math.min(drawdownLevel !== null ? drawdownLevel
                        : stillWaterLevel - 0.5 * c.Hm0, stillWaterLevel);

  /* 5. Stem and base thickness from the cantilever. */
  function stemDemand(baseT) {
    var top = foundingLevel + baseT;
    var retained = promenadeLevel - top;
    var mv = stemLoads(backfill, pressures, waveArm, baseT, retained,
                       Math.min(table, Math.max(retained, 0)), surcharge, trough,
                       stillWaterLevel, top);
    return stemSection(ULS_FACTOR * mv[0], ULS_FACTOR * mv[1]);
  }
  var minStem = stemThickness, minBase = baseThickness;
  baseThickness = Math.max(minBase, minStem);
  var stem = null;
  for (var it = 0; it < 8; it++) {
    stem = stemDemand(baseThickness);
    var newStem = Math.max(minStem, stem.thickness);
    var newBase = Math.max(minBase, newStem);
    if (Math.abs(newStem - stemThickness) < 1e-9 && Math.abs(newBase - baseThickness) < 1e-9) break;
    stemThickness = newStem;
    baseThickness = newBase;
  }
  stem = stemDemand(baseThickness);
  if (stem.thickness > stemThickness + 1e-9) {
    stemThickness = stem.thickness;
    baseThickness = Math.max(baseThickness, stemThickness);
  }
  var baseTop = foundingLevel + baseThickness;

  if (retainedHeight > L_WALL_PRACTICAL_HEIGHT) {
    warnings.push("The wall retains " + retainedHeight.toFixed(1) + " m. A cantilever " +
      "L-wall is ordinary practice up to about " + fmtG(L_WALL_PRACTICAL_HEIGHT) +
      " m; beyond that a counterforted wall, a caisson or an anchored sheet-pile " +
      "wall is the usual form, and the stem here (" + stemThickness.toFixed(2) +
      " m) shows why.");
  }

  var headBack = backWaterLevel - foundingLevel;
  var frontCrest = hydrostaticForce(Math.max(stillWaterLevel - foundingLevel, 0));
  var frontTrough = hydrostaticForce(Math.max(trough - foundingLevel, 0));

  /* 6. Base width. */
  var baseWidth = Math.min(
    Math.max(0.5 * (crestLevel - foundingLevel), stemThickness + 0.5), maxBaseWidth);
  var sliding = 0, overturning = 0, weight = 0, uplift = 0, staticUplift = 0;
  var bearing = null, drawdown = {}, iterations = 0;

  function passes(fs, fo, bear) {
    var ok = fs >= targetSliding && fo >= targetOverturning;
    if (requireMiddleThird) ok = ok && bear.middle_third;
    if (allowable !== null) ok = ok && bear.p_max <= allowable;
    return ok;
  }

  for (iterations = 1; iterations <= 2000; iterations++) {
    var B = baseWidth;
    var fillHeight = Math.max(promenadeLevel - baseTop, 0);
    var wet = Math.min(Math.max(backWaterLevel - baseTop, 0), fillHeight);
    var dry = fillHeight - wet;
    var heel = B - stemThickness;
    var parts = [
      [GAMMA_C * B * baseThickness, 0.5 * B],
      [GAMMA_C * stemThickness * (crestLevel - baseTop), 0.5 * stemThickness],
      [(backfill.dry_unit_weight * dry + backfill.saturated_unit_weight * wet) * heel,
       stemThickness + 0.5 * heel]
    ];
    weight = 0;
    var aboutToe = 0, aboutHeel = 0;
    for (var i = 0; i < parts.length; i++) {
      weight += parts[i][0];
      aboutToe += parts[i][0] * parts[i][1];
      aboutHeel += parts[i][0] * (B - parts[i][1]);
    }

    /* Case 1: the crest, pushing landward. */
    var up1 = upliftUnder(stillWaterLevel - foundingLevel, headBack, B);
    uplift = pressures.U_per_width * B;
    staticUplift = up1.force;
    var N1 = weight - up1.force - uplift;
    var H1 = F + frontCrest.force - earthResisting.total;
    var drive1 = F * waveArm + frontCrest.force * frontCrest.arm +
                 up1.force * (B - up1.x) + uplift * (2 / 3) * B;
    var resist1 = aboutHeel + earthResisting.moment;
    sliding = H1 > 1e-6 ? (N1 > 0 ? friction * N1 / H1 : 0) : Infinity;
    overturning = drive1 > 0 ? resist1 / drive1 : Infinity;
    bearing = bearingPressures(N1, B, resist1 - drive1);

    /* Case 2: the trough, pushed seaward by a backfill that has not drained. */
    var up2 = upliftUnder(trough - foundingLevel, headBack, B);
    var N2 = weight - up2.force;
    var H2 = earthDriving.total - frontTrough.force;
    var drive2 = earthDriving.moment + up2.force * up2.x;
    var resist2 = aboutToe + frontTrough.force * frontTrough.arm;
    var slidingOut = H2 > 1e-6 ? (N2 > 0 ? friction * N2 / H2 : 0) : Infinity;
    var overturningOut = drive2 > 0 ? resist2 / drive2 : Infinity;
    var bearingOut = bearingPressures(N2, B, resist2 - drive2);
    drawdown = {
      trough_level: trough, front_depth: Math.max(trough - foundingLevel, 0),
      front_force: frontTrough.force, front_arm: frontTrough.arm,
      earth_force: earthDriving.total, earth_arm: earthDriving.arm,
      uplift: up2.force, net_force: H2, normal: N2,
      sliding_FoS: slidingOut, overturning_FoS: overturningOut, bearing: bearingOut
    };

    if (passes(sliding, overturning, bearing) &&
        passes(slidingOut, overturningOut, bearingOut)) break;
    if (baseWidth >= maxBaseWidth) {
      warnings.push("Base width reached the " + fmtG(maxBaseWidth) + " m limit with " +
        "sliding FoS " + sliding.toFixed(2) + " landward and " + slidingOut.toFixed(2) +
        " seaward, overturning " + overturning.toFixed(2) + " and " +
        overturningOut.toFixed(2) + ", and peak bearing " + bearing.p_max.toFixed(0) +
        " and " + bearingOut.p_max.toFixed(0) + " kPa. A gravity wall is the wrong " +
        "form for these conditions; consider a piled or anchored wall, or a " +
        "rubble-mound revetment.");
      break;
    }
    baseWidth += step;
  }

  var waveMargin = Math.min(sliding / targetSliding, overturning / targetOverturning);
  var outMargin = Math.min(drawdown.sliding_FoS / targetSliding,
                           drawdown.overturning_FoS / targetOverturning);
  var governingCase = waveMargin <= outMargin ? "wave crest" : "drawdown";

  if (earthDriving.water_fraction > 0.6) {
    var drained = lateralEarthForce(backfill, retainedHeight, ceiling, surcharge,
                                    drivingKind).total;
    warnings.push("Pore water is " + (100 * earthDriving.water_fraction).toFixed(0) +
      "% of the pressure on the back of the wall. A drain holding the water table " +
      "at still water level would cut the total from " + earthDriving.total.toFixed(0) +
      " to about " + drained.toFixed(0) + " kN/m.");
  }
  if (governingCase === "drawdown") {
    warnings.push("The drawdown case governs: the wall is sized by the saturated " +
      "backfill pushing it seaward at the trough, so the backfill grading and the " +
      "drainage detail set the base width more than the design wave does.");
  }
  if (backfill.cohesive) {
    warnings.push(backfill.name + " is cohesive. The active pressure here uses " +
      "the drained parameters and cuts off the tension zone; an undrained " +
      "short-term check and a long-term swelling check are separate and can " +
      "both govern.");
  }

  var heelWidth = baseWidth - stemThickness;
  var wallHeight = crestLevel - foundingLevel;
  var baseArea = baseWidth * baseThickness;
  var stemArea = stemThickness * (wallHeight - baseThickness);
  var fillArea = heelWidth * Math.max(promenadeLevel - baseTop, 0);
  var bermArea = toeBermWidth * toeThickness;

  return {
    conditions: c,
    still_water_level: stillWaterLevel, seabed_level: seabedLevel,
    water_depth: depth,
    crest_level: crestLevel, crest_freeboard: Rc,
    promenade_level: promenadeLevel,
    base_width: baseWidth, stem_thickness: stemThickness,
    base_thickness: baseThickness, founding_level: foundingLevel,
    embedment: embedment, scour_depth: scour, wall_height: wallHeight,
    heel_width: heelWidth,
    toe_berm_width: toeBermWidth, toe_berm_thickness: toeThickness,
    toe_Dn50: toe.Dn50, toe_M50: toe.M50, toe_stability_number: toe.stability_number,
    pressures: pressures, wave_force: F, wave_arm: waveArm,
    weight: weight, uplift: uplift, static_uplift: staticUplift,
    sliding_FoS: sliding, overturning_FoS: overturning, bearing: bearing,
    allowable_bearing: allowable,
    backfill: backfill, retained_height: retainedHeight,
    water_table: table, back_water_level: backWaterLevel, surcharge: surcharge,
    earth_driving: earthDriving, earth_resisting: earthResisting,
    drawdown: drawdown, governing_case: governingCase, stem: stem,
    q_mean: band.q_mean, q_upper: band.q_upper, governing_limit: use,
    impulsive: q.impulsive, iterations: iterations, warnings: warnings,
    quantities: {
      concrete_base_m3_per_m: baseArea,
      concrete_stem_m3_per_m: stemArea,
      concrete_total_m3_per_m: baseArea + stemArea,
      concrete_mass_t_per_m: (baseArea + stemArea) * RHO_C / 1000,
      backfill_m3_per_m: fillArea,
      toe_rock_m3_per_m: bermArea,
      toe_rock_t_per_m: bermArea * (1 - 0.37) * RHO_S / 1000,
      excavation_m3_per_m: baseWidth * embedment
    }
  };
}

/* ------------------------------------------------------------------ */
/* Navigation channel                                                  */
/* ------------------------------------------------------------------ */

var MANOEUVRING_LANE = { good: 1.3, moderate: 1.5, poor: 1.8 };

var WIDTH_COMPONENTS = {
  speed: { fast: [0.1, 0.1], moderate: [0.0, 0.0], slow: [0.0, 0.0] },
  crosswind: { mild: [0.1, 0.1], moderate: [0.3, 0.4], severe: [0.6, 0.8] },
  crosscurrent: { negligible: [0.0, 0.0], low: [0.2, 0.3], moderate: [0.5, 0.7], strong: [1.0, 1.3] },
  longitudinal_current: { low: [0.0, 0.0], moderate: [0.1, 0.1], strong: [0.2, 0.2] },
  waves: { low: [0.0, 0.0], moderate: [0.5, 0.0], high: [1.0, 0.0] },
  aids_to_navigation: { excellent: [0.0, 0.0], good: [0.2, 0.2], moderate: [0.4, 0.4] },
  bottom_surface: { smooth_and_soft: [0.1, 0.1], smooth_or_sloping: [0.1, 0.1], rough_and_hard: [0.2, 0.2] },
  depth_of_waterway: { deep: [0.0, 0.0], moderate: [0.1, 0.2], shallow: [0.2, 0.4] },
  cargo_hazard: { low: [0.0, 0.0], medium: [0.5, 0.4], high: [1.0, 0.8] }
};

var BANK_CLEARANCE = {
  sloping_channel_edges: { fast: 0.7, moderate: 0.5, slow: 0.3 },
  sloping_and_shoals: { fast: 0.7, moderate: 0.5, slow: 0.3 },
  steep_and_hard: { fast: 1.3, moderate: 1.0, slow: 0.5 }
};

var PASSING_DISTANCE = { fast: 2.0, moderate: 1.6, slow: 1.2 };

function makeVessel(name, length, beam, draught, blockCoefficient, lengthPp) {
  if (!(length > 0) || !(beam > 0) || !(draught > 0)) {
    throw new Error("Vessel dimensions must be positive");
  }
  if (!(blockCoefficient >= 0.3 && blockCoefficient <= 1.0)) {
    throw new Error("Block coefficient outside 0.3 to 1.0");
  }
  var lpp = lengthPp === undefined || lengthPp === null ? 0.96 * length : lengthPp;
  var volume = blockCoefficient * lpp * beam * draught;
  return {
    name: name, length: length, beam: beam, draught: draught,
    block_coefficient: blockCoefficient, length_pp: lpp,
    displaced_volume: volume, displacement: volume * 1.025
  };
}

function squatIcorels(vessel, speed, depth, coefficient) {
  coefficient = coefficient === undefined ? 2.4 : coefficient;
  if (speed < 0) throw new Error("Speed must be non-negative");
  if (!(depth > 0)) throw new Error("Depth must be positive");
  var u = speed * KNOT;
  var froude = u / Math.sqrt(G * depth);
  if (froude >= 0.99) {
    throw new Error("Depth Froude number " + froude.toFixed(2) +
      " is at or above the critical speed; the squat formula has no meaning there");
  }
  var squat = coefficient * vessel.displaced_volume /
    (vessel.length_pp * vessel.length_pp) *
    froude * froude / Math.sqrt(1 - froude * froude);
  return { squat: squat, froude: froude, speed_ms: u, beyond_range: froude >= 0.7 };
}

function squatBarrass(vessel, speed, depth, confined) {
  if (speed < 0) throw new Error("Speed must be non-negative");
  if (!(depth > 0)) throw new Error("Depth must be positive");
  var divisor = confined ? 50.0 : 100.0;
  return {
    squat: vessel.block_coefficient * speed * speed / divisor,
    froude: speed * KNOT / Math.sqrt(G * depth), confined: !!confined
  };
}

function waveResponseAllowance(Hs, factor, period, vessel) {
  factor = factor === undefined ? 0.5 : factor;
  if (Hs < 0) throw new Error("Wave height must be non-negative");
  if (!(factor >= 0 && factor <= 1.5)) throw new Error("Factor outside any defensible range");
  var out = { allowance: factor * Hs, factor: factor };
  if (period !== undefined && period !== null && vessel) {
    var wavelength = G * period * period / (2 * Math.PI);
    out.wavelength = wavelength;
    out.length_ratio = wavelength / vessel.length;
    out.near_resonant = out.length_ratio >= 0.7 && out.length_ratio <= 1.4;
  }
  return out;
}

function underkeelClearance(vessel, squat, waveAllowance, o) {
  o = o || {};
  var parts = {
    "squat": squat,
    "wave response": waveAllowance,
    "density": o.density_allowance === undefined ? 0 : o.density_allowance,
    "net clearance": o.net_clearance === undefined ? 0.6 : o.net_clearance,
    "water level uncertainty": o.water_level_allowance === undefined ? 0 : o.water_level_allowance,
    "dredging tolerance": o.dredging_tolerance === undefined ? 0.3 : o.dredging_tolerance,
    "survey tolerance": o.survey_tolerance === undefined ? 0.2 : o.survey_tolerance,
    "siltation": o.siltation_allowance === undefined ? 0.2 : o.siltation_allowance
  };
  var gross = 0;
  for (var k in parts) {
    if (parts[k] < 0) throw new Error("Allowance " + k + " must be non-negative");
    gross += parts[k];
  }
  return {
    components: parts, gross: gross,
    required_depth: vessel.draught + gross, draught: vessel.draught
  };
}

function channelWidth(vessel, o) {
  o = o || {};
  var manoeuvrability = o.manoeuvrability || "moderate";
  var section = o.section || "outer";
  var twoWay = !!o.two_way;
  var speedClass = o.speed_class || "moderate";
  var bank = o.bank || "sloping_channel_edges";
  var conditions = o.conditions || {};

  if (!(manoeuvrability in MANOEUVRING_LANE)) throw new Error("Unknown manoeuvrability");
  if (section !== "outer" && section !== "inner") throw new Error("Section must be outer or inner");
  if (!(speedClass in PASSING_DISTANCE)) throw new Error("Unknown speed class");
  if (!(bank in BANK_CLEARANCE)) throw new Error("Unknown bank type");

  var column = section === "outer" ? 0 : 1;
  var components = {};
  var assumed = [];
  var basic = MANOEUVRING_LANE[manoeuvrability] * vessel.beam;
  components["basic manoeuvring lane"] = basic;

  var additional = 0;
  var names = Object.keys(WIDTH_COMPONENTS);
  for (var i = 0; i < names.length; i++) {
    var name = names[i];
    var classes = WIDTH_COMPONENTS[name];
    var key;
    if (name in conditions) {
      key = conditions[name];
      if (!(key in classes)) throw new Error("Unknown " + name + " class " + key);
    } else {
      var best = null;
      for (var candidate in classes) {
        if (best === null || classes[candidate][column] < classes[best][column]) best = candidate;
      }
      key = best;
      assumed.push(name + " = " + key);
    }
    var value = classes[key][column] * vessel.beam;
    if (value > 0) components[name + " (" + key + ")"] = value;
    additional += value;
  }

  var lanes = twoWay ? 2 : 1;
  var clearance = BANK_CLEARANCE[bank][speedClass] * vessel.beam;
  components["bank clearance, each side"] = clearance;
  var passing = twoWay ? PASSING_DISTANCE[speedClass] * vessel.beam : 0;
  if (twoWay) components["passing distance"] = passing;

  var width = lanes * (basic + additional) + passing + 2 * clearance;
  return {
    width: width, width_in_beams: width / vessel.beam,
    components: components, assumed: assumed, lanes: lanes, section: section
  };
}

function designChannel(vessel, speed, designWaterLevel, o) {
  o = o || {};
  var Hs = o.Hs === undefined ? 0 : o.Hs;
  var Tp = o.Tp === undefined ? null : o.Tp;
  var waveFactor = o.wave_factor === undefined ? 0.5 : o.wave_factor;
  var squatCoefficient = o.squat_coefficient === undefined ? 2.4 : o.squat_coefficient;
  var bed = sediment(o.bed || "medium_sand");
  var slopeAdvice = dredgedSideSlope(bed);
  var sideSlope = (o.side_slope === undefined || o.side_slope === null)
    ? slopeAdvice.cot_beta : o.side_slope;
  var existingBed = o.existing_bed === undefined ? null : o.existing_bed;
  var seabedSlope = o.seabed_slope === undefined ? 1 / 30 : o.seabed_slope;

  if (speed < 0) throw new Error("Speed must be non-negative");

  var warnings = [];
  if (o.side_slope !== undefined && o.side_slope !== null &&
      o.side_slope < slopeAdvice.cot_beta - 1e-9) {
    warnings.push("A 1:" + o.side_slope + " side slope is steeper than the 1:" +
      slopeAdvice.cot_beta.toFixed(1) + " this method gives for " + bed.name +
      ". It will slump into the channel and have to be dredged again.");
  }
  var waves = waveResponseAllowance(Hs, waveFactor, Tp, vessel);
  if (waves.near_resonant) {
    warnings.push("Wave length is " + waves.length_ratio.toFixed(2) +
      " times the vessel length, which is the worst case for vertical motion. " +
      "A wave factor above the " + waveFactor.toFixed(2) + " used here is likely.");
  }

  // design_channel has its own allowance defaults, and they are not the
  // same as underkeel_clearance's: a design water level carries 0.3 m of
  // uncertainty here, where the bare clearance function assumes none.
  var allowances = {
    net_clearance: o.net_clearance === undefined ? 0.6 : o.net_clearance,
    water_level_allowance: o.water_level_allowance === undefined ? 0.3 : o.water_level_allowance,
    dredging_tolerance: o.dredging_tolerance === undefined ? 0.3 : o.dredging_tolerance,
    survey_tolerance: o.survey_tolerance === undefined ? 0.2 : o.survey_tolerance,
    siltation_allowance: o.siltation_allowance === undefined ? 0.2 : o.siltation_allowance,
    density_allowance: o.density_allowance === undefined ? 0 : o.density_allowance
  };

  var subcritical = Math.pow(speed * KNOT / 0.8, 2) / G;
  var depth = Math.max(vessel.draught + 1.0, subcritical);
  var squat = null, clearance = null;

  for (var i = 0; i < 80; i++) {
    var froude = speed * KNOT / Math.sqrt(G * depth);
    if (froude >= 0.95) {
      var workable = 0.6 * Math.sqrt(G * depth) / KNOT;
      throw new Error("At " + speed + " knots the depth chain converges on about " +
        depth.toFixed(1) + " m, where the depth Froude number is " +
        froude.toFixed(2) + ". The vessel would be at the critical speed in her " +
        "own channel, and no squat formula applies. Reduce the design speed " +
        "below about " + workable.toFixed(0) + " knots, or fix the channel " +
        "depth by another means.");
    }
    squat = squatIcorels(vessel, speed, depth, squatCoefficient);
    clearance = underkeelClearance(vessel, squat.squat, waves.allowance, allowances);
    var newDepth = clearance.required_depth;
    if (Math.abs(newDepth - depth) < 1e-4) { depth = newDepth; break; }
    depth = newDepth;
  }

  if (squat.beyond_range) {
    warnings.push("Depth Froude number " + squat.froude.toFixed(2) +
      " is above 0.7, where the squat formula is no longer reliable. Reduce " +
      "the design speed or check with a manoeuvring simulation.");
  }
  if (depth / vessel.draught < 1.1) {
    warnings.push("Depth is only " + (depth / vessel.draught).toFixed(2) +
      " times the draught. Squat and manoeuvrability both degrade sharply " +
      "below about 1.1.");
  }
  var screening = squatBarrass(vessel, speed, depth, false);
  if (screening.squat > 2 * squat.squat) {
    warnings.push("Barrass screening gives " + screening.squat.toFixed(2) +
      " m of squat against the ICORELS " + squat.squat.toFixed(2) +
      " m. Check which is appropriate for this channel before fixing the dredge level.");
  }

  var width = channelWidth(vessel, o);
  var dredgeLevel = designWaterLevel - depth;
  if (existingBed !== null && existingBed < dredgeLevel) {
    warnings.push("The existing bed at " + existingBed.toFixed(2) +
      " m CD is already below the dredge level " + dredgeLevel.toFixed(2) +
      " m CD. No capital dredging is needed for depth.");
  }

  var rise = existingBed === null ? 0 : Math.max(existingBed - dredgeLevel, 0);
  var topWidth = existingBed === null ? width.width
    : width.width + 2 * sideSlope * rise;
  var area = width.width * rise + sideSlope * rise * rise;

  return {
    vessel: vessel, bed: bed, speed: speed, design_water_level: designWaterLevel,
    dredge_level: dredgeLevel, required_depth: depth,
    clearance: clearance, squat: squat, waves: waves, width_result: width,
    width: width.width, top_width: topWidth, side_slope: sideSlope,
    existing_bed: existingBed, dredge_area: area,
    volume_per_km: area * 1000.0, warnings: warnings
  };
}

/* ------------------------------------------------------------------ */
/* Piles                                                               */
/* ------------------------------------------------------------------ */

function waveKinematics(H, T, depth, z, phase, stretching) {
  phase = phase === undefined ? 0 : phase;
  stretching = stretching || "wheeler";
  if (!(H > 0) || !(T > 0) || !(depth > 0)) {
    throw new Error("Height, period and depth must be positive");
  }
  var L = dispersion(T, depth);
  var k = 2 * Math.PI / L;
  var omega = 2 * Math.PI / T;
  var a = 0.5 * H;
  var eta = a * Math.cos(phase);

  var u = new Array(z.length), dudt = new Array(z.length), wet = new Array(z.length);
  for (var i = 0; i < z.length; i++) {
    wet[i] = z[i] <= eta;
    var zEval;
    if (stretching === "wheeler") zEval = (z[i] - eta) * depth / (depth + eta);
    else if (stretching === "none") zEval = Math.min(z[i], 0);
    else zEval = z[i];
    var shape = Math.cosh(k * (zEval + depth)) / Math.sinh(k * depth);
    u[i] = wet[i] ? a * omega * shape * Math.cos(phase) : 0;
    dudt[i] = wet[i] ? a * omega * omega * shape * Math.sin(phase) : 0;
  }
  return { u: u, dudt: dudt, eta: eta, wavelength: L, k: k, omega: omega, wet: wet };
}

/* Fenton (1988) stream function wave: Newton on the full nonlinear
   free-surface problem, height raised in steps from a linear start. */
function sinhRatio(j, y, D) {
  return (Math.exp(j * (y - D)) - Math.exp(-j * (y + D))) / (1 + Math.exp(-2 * j * D));
}
function coshRatio(j, y, D) {
  return (Math.exp(j * (y - D)) + Math.exp(-j * (y + D))) / (1 + Math.exp(-2 * j * D));
}

function solveLinear(A, b) {
  var n = b.length, M = [], i, j, k;
  for (i = 0; i < n; i++) { M.push(A[i].slice()); M[i].push(b[i]); }
  for (k = 0; k < n; k++) {
    var piv = k, best = Math.abs(M[k][k]);
    for (i = k + 1; i < n; i++) {
      if (Math.abs(M[i][k]) > best) { best = Math.abs(M[i][k]); piv = i; }
    }
    if (!(best > 0)) return null;
    if (piv !== k) { var tmp = M[k]; M[k] = M[piv]; M[piv] = tmp; }
    for (i = k + 1; i < n; i++) {
      var f = M[i][k] / M[k][k];
      if (f === 0) continue;
      for (j = k; j <= n; j++) M[i][j] -= f * M[k][j];
    }
  }
  var x = new Array(n);
  for (i = n - 1; i >= 0; i--) {
    var sum = M[i][n];
    for (j = i + 1; j < n; j++) sum -= M[i][j] * x[j];
    x[i] = sum / M[i][i];
  }
  return x;
}

function StreamFunctionWave(H, T, depth, N, steps, tolerance) {
  N = N === undefined ? 20 : N;
  steps = steps === undefined ? 6 : steps;
  tolerance = tolerance === undefined ? 1e-10 : tolerance;
  if (!(H > 0) || !(T > 0) || !(depth > 0)) throw new Error("Height, period and depth must be positive");
  this.H = H; this.T = T; this.depth = depth; this.N = N;
  this.converged = false;
  var Hd = H / depth, HgT2 = H / (G * T * T);
  var kd = 2 * Math.PI / dispersion(T, depth) * depth;
  var prev = null, prev2 = null, z = null, s, i;
  for (s = 1; s <= steps; s++) {
    var frac = s / steps;
    if (prev === null) z = this._linear(kd, frac * Hd * kd);
    else if (prev2 === null) z = prev.slice();
    else { z = new Array(prev.length); for (i = 0; i < z.length; i++) z[i] = 2 * prev[i] - prev2[i]; }
    z = this._newton(z, frac * Hd, frac * HgT2, tolerance);
    if (z === null) return;
    prev2 = prev; prev = z;
  }
  this.z = z;
  this.converged = true;
  this.k = z[0] / depth;
  this.celerity = z[3] * Math.sqrt(G / this.k);
  this.wavelength = 2 * Math.PI / this.k;
  this._E = new Array(N + 1);
  for (var j = 0; j <= N; j++) {
    var sum = 0;
    for (var m = 0; m <= N; m++) {
      var w = (m === 0 || m === N) ? 0.5 : 1;
      sum += w * z[9 + m] * Math.cos(j * m * Math.PI / N);
    }
    this._E[j] = 2 / N * sum;
  }
  this.crest = z[9] / this.k - depth;
  this.trough = z[9 + N] / this.k - depth;
}

StreamFunctionWave.prototype._linear = function (kd, kH) {
  var N = this.N, z = new Array(2 * N + 10);
  for (var i = 0; i < z.length; i++) z[i] = 0;
  var c = Math.sqrt(Math.tanh(kd));
  z[0] = kd; z[1] = kH; z[3] = c; z[2] = 2 * Math.PI / c; z[4] = 0;
  z[5] = c; z[6] = c; z[7] = c * kd; z[8] = 0.5 * c * c + kd;
  for (var m = 0; m <= N; m++) z[9 + m] = kd + 0.5 * kH * Math.cos(m * Math.PI / N);
  z[10 + N] = 0.5 * kH * c / Math.tanh(kd);
  return z;
};

StreamFunctionWave.prototype._residual = function (z, Hd, HgT2) {
  var N = this.N, f = new Array(2 * N + 10), m, j;
  f[0] = z[1] - z[0] * Hd;
  f[1] = z[1] - HgT2 * z[2] * z[2];
  f[2] = z[2] * z[3] - 2 * Math.PI;
  f[3] = z[4] + z[6] - z[3];
  f[4] = z[5] + z[7] / z[0] - z[3];
  f[5] = z[4];
  var inner = 0;
  for (m = 1; m < N; m++) inner += z[9 + m];
  f[6] = z[9] + z[9 + N] + 2 * inner - 2 * N * z[0];
  f[7] = z[9] - z[9 + N] - z[1];
  for (m = 0; m <= N; m++) {
    var theta = m * Math.PI / N, eta = z[9 + m];
    var psi = 0, u = -z[6], v = 0;
    for (j = 1; j <= N; j++) {
      var B = z[9 + N + j];
      var cj = Math.cos(j * theta), sj = Math.sin(j * theta);
      var sr = sinhRatio(j, eta, z[0]), cr = coshRatio(j, eta, z[0]);
      psi += B * sr * cj;
      u += j * B * cr * cj;
      v += j * B * sr * sj;
    }
    f[8 + m] = psi - z[6] * eta + z[7];
    f[9 + N + m] = 0.5 * (u * u + v * v) + eta - z[8];
  }
  return f;
};

StreamFunctionWave.prototype._newton = function (z, Hd, HgT2, tolerance) {
  var n = z.length, it, i, r;
  for (it = 0; it < 40; it++) {
    var f = this._residual(z, Hd, HgT2);
    var J = new Array(n);
    for (r = 0; r < n; r++) J[r] = new Array(n);
    for (i = 0; i < n; i++) {
      var h = 1e-7 * Math.max(Math.abs(z[i]), 1e-3);
      var zp = z.slice();
      zp[i] += h;
      var fp = this._residual(zp, Hd, HgT2);
      for (r = 0; r < n; r++) J[r][i] = (fp[r] - f[r]) / h;
    }
    var rhs = new Array(n);
    for (r = 0; r < n; r++) rhs[r] = -f[r];
    var dz = solveLinear(J, rhs);
    if (dz === null) return null;
    var biggest = 0;
    for (i = 0; i < n; i++) {
      z[i] += dz[i];
      if (!isFinite(z[i])) return null;
      biggest = Math.max(biggest, Math.abs(dz[i]));
    }
    if (biggest < tolerance) return z;
  }
  var res = this._residual(z, Hd, HgT2), worst = 0;
  for (i = 0; i < res.length; i++) worst = Math.max(worst, Math.abs(res[i]));
  return worst < 1e-6 ? z : null;
};

StreamFunctionWave.prototype.surface = function (phase) {
  var N = this.N, sum = 0;
  for (var j = 0; j <= N; j++) {
    var w = (j === 0 || j === N) ? 0.5 : 1;
    sum += w * this._E[j] * Math.cos(j * phase);
  }
  return sum / this.k - this.depth;
};

StreamFunctionWave.prototype.kinematics = function (z, phase) {
  var N = this.N, D = this.z[0], eta = this.surface(phase);
  var su = Math.sqrt(G / this.k), sa = this.z[3] * G;
  var u = new Array(z.length), dudt = new Array(z.length), wet = new Array(z.length);
  for (var i = 0; i < z.length; i++) {
    wet[i] = z[i] <= eta;
    u[i] = 0; dudt[i] = 0;
    if (!wet[i]) continue;
    var ky = this.k * (Math.min(z[i], eta) + this.depth);
    var su1 = this.z[4], sa1 = 0;
    for (var j = 1; j <= N; j++) {
      var B = this.z[9 + N + j], cr = coshRatio(j, ky, D);
      su1 += j * B * cr * Math.cos(j * phase);
      sa1 += j * j * B * cr * Math.sin(j * phase);
    }
    u[i] = su * su1;
    dudt[i] = sa * sa1;
  }
  return { u: u, dudt: dudt, eta: eta, wavelength: this.wavelength, k: this.k,
           omega: 2 * Math.PI / this.T, wet: wet };
};

var STREAM_CACHE = {};
function streamFunctionWave(H, T, depth, N) {
  N = N === undefined ? 20 : N;
  var key = [H.toFixed(9), T.toFixed(9), depth.toFixed(9), N].join("|");
  if (!(key in STREAM_CACHE)) {
    if (Object.keys(STREAM_CACHE).length > 64) STREAM_CACHE = {};
    STREAM_CACHE[key] = new StreamFunctionWave(H, T, depth, N);
  }
  return STREAM_CACHE[key];
}

function bedKeuleganCarpenter(Hs, T, depth, diameter) {
  if (!(diameter > 0) || !(Hs > 0) || !(T > 0) || !(depth > 0)) {
    throw new Error("Diameter, height, period and depth must be positive");
  }
  var L = dispersion(T, depth);
  var Um = Math.PI * Hs / (T * Math.sinh(2 * Math.PI * depth / L));
  return { Um: Um, KC: Um * T / diameter };
}

function keuleganCarpenter(H, T, depth, diameter) {
  if (!(diameter > 0)) throw new Error("Diameter must be positive");
  var kin = waveKinematics(H, T, depth, [0], 0, "none");
  return Math.abs(kin.u[0]) * T / diameter;
}

function dragInertiaCoefficients(KC, rough) {
  rough = rough === undefined ? true : rough;
  if (!(KC > 0)) throw new Error("KC must be positive");
  var Cd = rough ? 1.05 : 0.65;
  var regime, Cm;
  if (KC < 3.0) { regime = "inertia dominated"; Cm = 2.0; }
  else if (KC < 15.0) { regime = "mixed"; Cm = 2.0 - 0.04 * (KC - 3.0); }
  else { regime = "drag dominated"; Cm = Math.max(1.5, 2.0 - 0.04 * (KC - 3.0)); }
  return { Cd: Cd, Cm: Cm, regime: regime, KC: KC, rough: rough };
}

function trapezoid(y, x) {
  var total = 0;
  for (var i = 1; i < x.length; i++) {
    total += 0.5 * (y[i] + y[i - 1]) * (x[i] - x[i - 1]);
  }
  return total;
}

function morisonPileLoad(diameter, H, T, depth, o) {
  o = o || {};
  var phase = o.phase === undefined ? 0 : o.phase;
  var points = o.points === undefined ? 400 : o.points;
  var stretching = o.stretching || "wheeler";
  var rough = o.rough === undefined ? true : o.rough;
  var airGap = o.air_gap === undefined ? 0 : o.air_gap;
  var theory = o.theory || "stream";
  if (points < 2) throw new Error("Need at least two points");
  if (theory !== "stream" && theory !== "linear") throw new Error("Unknown wave theory " + theory);

  var KC = keuleganCarpenter(H, T, depth, diameter);
  var coefficients = dragInertiaCoefficients(KC, rough);
  var Cd = o.Cd === undefined || o.Cd === null ? coefficients.Cd : o.Cd;
  var Cm = o.Cm === undefined || o.Cm === null ? coefficients.Cm : o.Cm;

  var warnings = [];
  var wave = null;
  if (theory === "stream" && H < 0.78 * depth) {
    wave = streamFunctionWave(H, T, depth);
    if (!wave.converged) {
      warnings.push("The stream function wave did not converge, which puts this " +
        "wave at breaking. Linear theory with Wheeler stretching is used instead " +
        "and understates the crest kinematics.");
      wave = null;
    }
  }
  var top = (wave !== null ? wave.crest : 0.5 * H) + airGap;
  var z = new Array(points);
  for (var i = 0; i < points; i++) {
    z[i] = -depth + (top + depth) * i / (points - 1);
  }
  var kin = wave !== null ? wave.kinematics(z, phase)
                          : waveKinematics(H, T, depth, z, phase, stretching);

  var drag = new Array(points), inertia = new Array(points), total = new Array(points);
  for (i = 0; i < points; i++) {
    drag[i] = 0.5 * RHO_W * Cd * diameter * kin.u[i] * Math.abs(kin.u[i]);
    inertia[i] = RHO_W * Cm * 0.25 * Math.PI * diameter * diameter * kin.dudt[i];
    total[i] = drag[i] + inertia[i];
  }
  var force = trapezoid(total, z);
  var lever = new Array(points);
  for (i = 0; i < points; i++) lever[i] = total[i] * (z[i] + depth);
  var moment = trapezoid(lever, z);
  var arm = force !== 0 ? moment / force : 0;

  var inertiaAbs = Math.abs(trapezoid(inertia, z));
  var dragAbs = Math.abs(trapezoid(drag, z));
  var split = inertiaAbs + dragAbs;

  var ratio = diameter / kin.wavelength;
  if (ratio > 0.2) {
    warnings.push("D / L = " + ratio.toFixed(2) + " is above 0.2, so the pile " +
      "diffracts the wave and the Morison equation does not apply. Use a " +
      "diffraction method such as MacCamy and Fuchs.");
  }
  if (H > 0.78 * depth) {
    warnings.push("H = " + H.toFixed(2) + " m exceeds 0.78 of the " +
      depth.toFixed(1) + " m depth, so the wave has broken. Breaking wave " +
      "slam is a separate and much larger load, and is not computed here.");
  }

  return {
    diameter: diameter, H: H, T: T, depth: depth, phase: phase,
    z: z, drag: drag, inertia: inertia, total: total,
    force: force, moment: moment, arm: arm, eta: kin.eta,
    Cd: Cd, Cm: Cm, KC: KC, regime: coefficients.regime,
    diffraction_ratio: ratio,
    inertia_fraction: split > 0 ? inertiaAbs / split : NaN,
    warnings: warnings, theory: wave !== null ? "stream function" : "linear"
  };
}

function phaseSweep(diameter, H, T, depth, phases, o) {
  phases = phases === undefined ? 181 : phases;
  if (phases < 3) throw new Error("Need at least three phases");
  o = o || {};
  var angles = new Array(phases), force = new Array(phases), moment = new Array(phases);
  for (var i = 0; i < phases; i++) {
    angles[i] = 2 * Math.PI * i / (phases - 1);
    var opts = {
      phase: angles[i], points: o.points, stretching: o.stretching,
      rough: o.rough, Cd: o.Cd, Cm: o.Cm, theory: o.theory
    };
    var r = morisonPileLoad(diameter, H, T, depth, opts);
    force[i] = r.force;
    moment[i] = r.moment;
  }
  var iF = 0, iM = 0;
  for (i = 1; i < phases; i++) {
    if (Math.abs(force[i]) > Math.abs(force[iF])) iF = i;
    if (Math.abs(moment[i]) > Math.abs(moment[iM])) iM = i;
  }
  return {
    phase: angles, force: force, moment: moment,
    max_force: Math.abs(force[iF]), max_moment: Math.abs(moment[iM]),
    phase_of_max_force: angles[iF], phase_of_max_moment: angles[iM],
    same_phase: iF === iM
  };
}

function scourDepthPile(diameter, KC, currentOnly, liveBed, bed, Hs, T, depth, currentRatio) {
  currentRatio = currentRatio === undefined ? 0 : currentRatio;
  if (!(diameter > 0)) throw new Error("Diameter must be positive");
  if (!(KC > 0)) throw new Error("KC must be positive");
  if (!(currentRatio >= 0 && currentRatio <= 1)) throw new Error("Ucw must be in [0, 1]");
  /* Sumer and Fredsoe (2001), combined waves and current. */
  var A = 0.03 + 0.75 * Math.pow(currentRatio, 2.6);
  var Bc = 6.0 * Math.exp(-4.7 * currentRatio);
  var ratio;
  if (currentOnly || currentRatio >= 1) ratio = 1.3;
  else if (KC <= Bc) ratio = 0.0;
  else ratio = 1.3 * (1 - Math.exp(-A * (KC - Bc)));
  var result = {
    depth: ratio * diameter, ratio: ratio, KC: KC, current_ratio: currentRatio,
    no_scour: !currentOnly && ratio === 0,
    standard_deviation: currentOnly ? 0.7 * diameter : null,
    live_bed: liveBed === undefined ? true : liveBed
  };
  if (bed !== undefined && bed !== null &&
      Hs !== undefined && T !== undefined && depth !== undefined) {
    var mobility = bedMobility(bed, Hs, T, depth);
    result.mobility = mobility;
    result.note = mobility.note;
    if (mobility.regime === "cohesive") { result.depth = 0; result.applies = false; }
    else if (!mobility.mobile && currentRatio === 0) { result.depth *= 0.5; result.applies = false; }
    else { result.applies = true; }
  }
  return result;
}

function designMonopile(diameter, H, T, depth, o) {
  o = o || {};
  var phases = o.phases === undefined ? 181 : o.phases;
  var current = o.current === undefined ? 0 : o.current;
  if (current < 0) throw new Error("Current must be non-negative");
  var Hs = o.Hs === undefined || o.Hs === null ? H / 1.86 : o.Hs;
  var sweep = phaseSweep(diameter, H, T, depth, phases, o);
  var worst = morisonPileLoad(diameter, H, T, depth,
    { phase: sweep.phase_of_max_moment, rough: o.rough, stretching: o.stretching,
      points: o.points, theory: o.theory });
  var crest = morisonPileLoad(diameter, H, T, depth,
    { phase: 0, rough: o.rough, stretching: o.stretching, points: o.points,
      theory: o.theory });
  var bedKc = bedKeuleganCarpenter(Hs, T, depth, diameter);
  var Ucw = current + bedKc.Um > 0 ? current / (current + bedKc.Um) : 0;
  var scour = scourDepthPile(diameter, bedKc.KC, false, true, o.bed || null,
                             Hs, T, depth, Ucw);
  scour.Um = bedKc.Um;
  scour.Hs = Hs;
  var missed = (Math.abs(worst.moment) - Math.abs(crest.moment)) / Math.abs(worst.moment);
  if (missed > 0.02) {
    worst.warnings.push("The worst moment is " + (100 * missed).toFixed(0) +
      "% larger than the moment at the crest phase. Designing on the crest " +
      "alone would have understated it.");
  }
  if (current === 0) {
    worst.warnings.push("No current was given, so the scour is for waves alone. A " +
      "tidal current of even 0.5 m/s usually dominates monopile scour and takes it " +
      "towards 1.3 D; give the site current before relying on this number.");
  }
  return {
    load: worst, crest_load: crest, sweep: sweep, scour: scour,
    crest_underestimate: missed, cantilever_increase: scour.depth
  };
}


/* ------------------------------------------------------------------ */
/* Sediment and soil                                                   */
/* ------------------------------------------------------------------ */

var GAMMA_W = RHO_W * G / 1000.0;   /* kN/m3 */
var GAMMA_C = RHO_C * G / 1000.0;   /* kN/m3 */
var NU = 1.19e-6;

function makeSediment(name, d50, opts) {
  opts = opts || {};
  var s = {
    name: name,
    d50: d50,
    specific_gravity: opts.specific_gravity === undefined ? 2.65 : opts.specific_gravity,
    porosity: opts.porosity === undefined ? 0.40 : opts.porosity,
    friction_angle: opts.friction_angle === undefined ? 32.0 : opts.friction_angle,
    cohesion: opts.cohesion === undefined ? 0.0 : opts.cohesion,
    description: opts.description || ""
  };
  s.relative_density = s.specific_gravity - 1.0;
  s.dry_unit_weight = (1 - s.porosity) * s.specific_gravity * GAMMA_W;
  s.saturated_unit_weight = s.dry_unit_weight + s.porosity * GAMMA_W;
  s.submerged_unit_weight = s.saturated_unit_weight - GAMMA_W;
  s.phi_sorting = opts.phi_sorting === undefined ? 0.6 : opts.phi_sorting;
  s.cohesive = s.cohesion > 0;
  return s;
}

var SEDIMENTS = {
  soft_clay: makeSediment("Soft clay", 0.0, {
    specific_gravity: 2.70, porosity: 0.55, friction_angle: 22.0, cohesion: 15.0,
    phi_sorting: 2.0,
    description: "normally consolidated, undrained strength governs" }),
  stiff_clay: makeSediment("Stiff clay", 0.0, {
    specific_gravity: 2.72, porosity: 0.42, friction_angle: 26.0, cohesion: 40.0,
    phi_sorting: 2.0,
    description: "overconsolidated" }),
  silt: makeSediment("Silt", 0.03e-3, {
    porosity: 0.48, friction_angle: 28.0,
    phi_sorting: 1.6,
    description: "mobile at almost any wave" }),
  very_fine_sand: makeSediment("Very fine sand", 0.09e-3, {
    porosity: 0.45, friction_angle: 29.0,
    phi_sorting: 0.55,
    description: "suspends readily, high siltation" }),
  fine_sand: makeSediment("Fine sand", 0.19e-3, {
    porosity: 0.43, friction_angle: 31.0,
    phi_sorting: 0.45,
    description: "the usual beach and nearshore sand" }),
  medium_sand: makeSediment("Medium sand", 0.38e-3, {
    porosity: 0.40, friction_angle: 33.0, phi_sorting: 0.55,
    description: "typical dredged fill" }),
  coarse_sand: makeSediment("Coarse sand", 0.75e-3, {
    porosity: 0.38, friction_angle: 35.0, phi_sorting: 0.7,
    description: "good drained backfill" }),
  fine_gravel: makeSediment("Fine gravel", 6.0e-3, {
    porosity: 0.35, friction_angle: 38.0, phi_sorting: 0.95,
    description: "free draining" }),
  coarse_gravel: makeSediment("Coarse gravel", 30.0e-3, {
    porosity: 0.35, friction_angle: 40.0, phi_sorting: 1.1,
    description: "shingle beach" }),
  rock_fill: makeSediment("Quarry rock fill", 150.0e-3, {
    porosity: 0.37, friction_angle: 42.0,
    phi_sorting: 1.4,
    description: "engineered granular backfill" })
};

function sediment(key) {
  if (typeof key !== "string") return key;
  if (!(key in SEDIMENTS)) {
    throw new Error("Unknown sediment " + key + ". Options: " +
                    Object.keys(SEDIMENTS).sort().join(", "));
  }
  return SEDIMENTS[key];
}

function dimensionlessGrainSize(material, viscosity) {
  viscosity = viscosity === undefined ? NU : viscosity;
  var grains = sediment(material);
  if (!(grains.d50 > 0)) {
    throw new Error(grains.name + " is cohesive: grain size does not govern " +
      "its behaviour, and a Shields threshold is meaningless for it");
  }
  return grains.d50 * Math.pow(G * grains.relative_density / (viscosity * viscosity),
                               1 / 3);
}

function criticalShields(material, viscosity) {
  var d = dimensionlessGrainSize(material, viscosity);
  return 0.30 / (1 + 1.2 * d) + 0.055 * (1 - Math.exp(-0.020 * d));
}

function fallVelocity(material, viscosity) {
  viscosity = viscosity === undefined ? NU : viscosity;
  var grains = sediment(material);
  var d = dimensionlessGrainSize(grains, viscosity);
  return (viscosity / grains.d50) *
         (Math.sqrt(10.36 * 10.36 + 1.049 * d * d * d) - 10.36);
}

function waveOrbitalVelocity(Hs, T, depth, wavelength) {
  if (!(Hs > 0) || !(T > 0) || !(depth > 0)) {
    throw new Error("Wave height, period and depth must be positive");
  }
  var L = wavelength === undefined || wavelength === null
    ? dispersion(T, depth) : wavelength;
  var k = 2 * Math.PI / L;
  return Math.PI * Hs / (T * Math.sinh(k * depth));
}

function waveShields(material, Hs, T, depth, wavelength) {
  var grains = sediment(material);
  var u = waveOrbitalVelocity(Hs, T, depth, wavelength);
  var excursion = u * T / (2 * Math.PI);
  var roughness = 2.5 * grains.d50;
  var ratio = Math.max(excursion / roughness, 1.0);
  var fw = Math.min(Math.exp(5.213 * Math.pow(ratio, -0.194) - 5.977), 0.3);
  var shear = 0.5 * RHO_W * fw * u * u;
  var theta = shear / ((grains.specific_gravity - 1) * RHO_W * G * grains.d50);
  var thetaCr = criticalShields(grains);
  return {
    orbital_velocity: u, excursion: excursion, friction_factor: fw,
    shear_stress: shear, shields: theta, critical_shields: thetaCr,
    mobility: thetaCr > 0 ? theta / thetaCr : Infinity,
    mobile: theta > thetaCr
  };
}

var MOBILITY_NOTES = {
  "live bed": "Bed is in motion away from the structure; live-bed scour relations apply.",
  "near threshold": "Bed is only just mobile. Scour will develop slowly and the equilibrium depth is uncertain.",
  "clear water": "Bed is below its threshold in the approach flow. Scour can still occur where the structure amplifies the flow, but live-bed relations will overstate it."
};

function bedMobility(material, Hs, T, depth) {
  var grains = sediment(material);
  if (grains.cohesive) {
    return {
      mobile: false, regime: "cohesive", mobility: NaN,
      note: grains.name + " is cohesive. Scour is governed by erodibility " +
            "and duration, not by a Shields threshold, and needs a " +
            "site-specific erosion test."
    };
  }
  var result = waveShields(grains, Hs, T, depth);
  result.regime = result.mobile
    ? (result.mobility > 2.0 ? "live bed" : "near threshold")
    : "clear water";
  result.note = MOBILITY_NOTES[result.regime];
  return result;
}

function earthPressureCoefficient(frictionAngle, kind, wallFriction, backslope) {
  kind = kind || "active";
  wallFriction = wallFriction || 0;
  backslope = backslope || 0;
  if (["active", "at_rest", "passive"].indexOf(kind) < 0) {
    throw new Error("Unknown earth pressure kind " + kind);
  }
  if (!(frictionAngle >= 0 && frictionAngle < 60)) {
    throw new Error("Friction angle " + frictionAngle + " is outside 0 to 60");
  }
  var phi = frictionAngle * Math.PI / 180;

  if (kind === "at_rest") return 1 - Math.sin(phi);

  if (Math.abs(backslope) > 1e-9) {
    var beta = backslope * Math.PI / 180;
    if (Math.abs(beta) >= phi) {
      throw new Error("A backslope of " + backslope + " deg cannot stand in a " +
        "soil with phi' = " + frictionAngle + " deg");
    }
    var root = Math.sqrt(Math.pow(Math.cos(beta), 2) - Math.pow(Math.cos(phi), 2));
    if (kind === "active") {
      return Math.cos(beta) * (Math.cos(beta) - root) / (Math.cos(beta) + root);
    }
    return Math.cos(beta) * (Math.cos(beta) + root) / (Math.cos(beta) - root);
  }

  if (Math.abs(wallFriction) > 1e-9) {
    var delta = wallFriction * Math.PI / 180;
    var num = Math.pow(Math.cos(phi), 2);
    var inner = Math.sqrt(Math.sin(phi + delta) * Math.sin(phi) / Math.cos(delta));
    var den = kind === "active"
      ? Math.cos(delta) * Math.pow(1 + inner, 2)
      : Math.cos(delta) * Math.pow(1 - inner, 2);
    return num / den;
  }

  if (kind === "active") return (1 - Math.sin(phi)) / (1 + Math.sin(phi));
  return (1 + Math.sin(phi)) / (1 - Math.sin(phi));
}

function lateralEarthPressure(material, height, waterTable, surcharge, kind,
                              wallFriction, points) {
  var grains = sediment(material);
  waterTable = waterTable || 0;
  surcharge = surcharge || 0;
  kind = kind || "active";
  points = points || 201;
  if (!(height > 0)) throw new Error("Retained height must be positive");
  if (waterTable < 0) throw new Error("Water table depth must be non-negative");
  if (surcharge < 0) throw new Error("Surcharge must be non-negative");
  if (points < 3) throw new Error("Need at least three points");

  var K = earthPressureCoefficient(grains.friction_angle, kind, wallFriction);
  var z = new Array(points), effective = new Array(points), pore = new Array(points),
      total = new Array(points);
  for (var i = 0; i < points; i++) {
    z[i] = height * i / (points - 1);
    var dry = Math.min(z[i], waterTable);
    var wet = Math.max(z[i] - waterTable, 0);
    var vertical = surcharge + grains.dry_unit_weight * dry +
                   grains.submerged_unit_weight * wet;
    var horizontal = K * vertical;
    if (grains.cohesive) {
      horizontal = Math.max(horizontal - 2 * grains.cohesion * Math.sqrt(K), 0);
    }
    effective[i] = horizontal;
    pore[i] = GAMMA_W * wet;
    total[i] = horizontal + pore[i];
  }
  return { depth: z, effective: effective, pore: pore, total: total,
           K: K, kind: kind, sediment: grains };
}

function lateralEarthForce(material, height, waterTable, surcharge, kind,
                           wallFriction, points) {
  points = points || 401;
  var diagram = lateralEarthPressure(material, height, waterTable, surcharge,
                                     kind, wallFriction, points);
  var z = diagram.depth;
  var lever = new Array(z.length);
  for (var i = 0; i < z.length; i++) lever[i] = diagram.total[i] * (height - z[i]);

  var soil = trapezoid(diagram.effective, z);
  var water = trapezoid(diagram.pore, z);
  var total = soil + water;
  var moment = trapezoid(lever, z);
  return {
    soil: soil, water: water, total: total, moment: moment,
    arm: total > 0 ? moment / total : 0,
    K: diagram.K, kind: diagram.kind, diagram: diagram,
    water_fraction: total > 0 ? water / total : 0
  };
}

function hydrostaticForce(depth, unitWeight) {
  unitWeight = unitWeight === undefined ? GAMMA_W : unitWeight;
  if (depth < 0) throw new Error("Depth must be non-negative");
  return { force: 0.5 * unitWeight * depth * depth, arm: depth / 3 };
}

function reflectionCoefficient(cotAlpha, surfSimilarity, permeable) {
  if (!(surfSimilarity > 0)) throw new Error("Surf similarity must be positive");
  permeable = permeable === undefined ? true : permeable;
  var a = permeable ? 0.6 : 1.0;
  var b = permeable ? 6.6 : 5.5;
  var xi2 = surfSimilarity * surfSimilarity;
  return Math.min(a * xi2 / (b + xi2), 1.0);
}

function toeScour(bed, Hs, T, depth, reflection, coefficient, exponent) {
  reflection = reflection === undefined ? 1.0 : reflection;
  coefficient = coefficient === undefined ? 0.4 : coefficient;
  exponent = exponent === undefined ? 1.35 : exponent;
  var grains = sediment(bed);
  if (!(reflection >= 0 && reflection <= 1)) {
    throw new Error("Reflection coefficient must be in [0,1]");
  }
  if (coefficient < 0) throw new Error("Coefficient must be non-negative");

  var L = dispersion(T, depth);
  var kh = 2 * Math.PI * depth / L;
  var unlimited = coefficient * reflection * Hs /
                  Math.pow(Math.sinh(kh), exponent);
  var mobility = bedMobility(grains, Hs, T, depth);

  if (grains.cohesive) {
    return { depth: 0, unlimited_depth: unlimited, reflection: reflection,
             mobility: mobility, applies: false, screening_only: true,
             note: mobility.note };
  }
  return {
    depth: mobility.mobile ? unlimited : 0.5 * unlimited,
    unlimited_depth: unlimited, reflection: reflection, relative_depth: kh,
    mobility: mobility, applies: mobility.mobile, screening_only: true,
    note: mobility.note
  };
}

function breakwaterToeScour(design, depth, bed, permeable) {
  bed = bed || "medium_sand";
  var xi = design.conditions.breakerParameter(design.cot_alpha);
  var Kr = reflectionCoefficient(design.cot_alpha, xi, permeable);
  var result = toeScour(bed, design.conditions.Hm0, design.conditions.Tm10,
                        depth, Kr);
  result.surf_similarity = xi;
  result.apron_width = Math.max(2 * result.depth, 1.5 * design.Dn50, 2.0);
  return result;
}

var ROUNDHEAD_KD_RATIO = {
  rock:      { 1.5: 0.95, 2.0: 0.80, 3.0: 0.65 },
  cubes:     { 1.5: 0.85, 2.0: 0.75, 3.0: 0.60 },
  tetrapod:  { 1.5: 0.72, 2.0: 0.64, 3.0: 0.50 },
  accropode: { 1.5: 0.80, 2.0: 0.75, 3.0: 0.65 },
  dolos:     { 1.5: 0.65, 2.0: 0.58, 3.0: 0.45 }
};

var ARMOUR_FAMILY = {
  rock_one_layer_impermeable: "rock", rock_two_layer_impermeable: "rock",
  rock_two_layer_permeable: "rock", cubes_one_layer_flat: "cubes",
  cubes_two_layer_random: "cubes", antifer: "cubes", tetrapod: "tetrapod",
  accropode: "accropode", core_loc: "accropode", xbloc: "accropode",
  dolos: "dolos", smooth_concrete: "rock", grass: "rock", asphalt: "rock"
};

function roundheadKdRatio(armour, cotAlpha) {
  var table = ROUNDHEAD_KD_RATIO[ARMOUR_FAMILY[armour] || "rock"];
  var slopes = Object.keys(table).map(Number).sort(function (a, b) { return a - b; });
  if (cotAlpha <= slopes[0]) return table[slopes[0]];
  if (cotAlpha >= slopes[slopes.length - 1]) return table[slopes[slopes.length - 1]];
  for (var i = 0; i < slopes.length - 1; i++) {
    var low = slopes[i], high = slopes[i + 1];
    if (cotAlpha >= low && cotAlpha <= high) {
      var span = (cotAlpha - low) / (high - low);
      return table[low] + span * (table[high] - table[low]);
    }
  }
  return table[slopes[slopes.length - 1]];
}

/* The head takes heavier armour than the trunk: it is attacked from more
   directions, its convex face gives each unit less support from its
   neighbours, and the run-down concentrates where the flow turns. Hudson
   puts Dn50 at KD to the minus a third, so a KD ratio r gives M50 / r. */
function roundhead(design, kdRatio, raiseCrest) {
  raiseCrest = raiseCrest || 0;
  if (kdRatio === undefined || kdRatio === null) {
    kdRatio = roundheadKdRatio(design.armour_type, design.cot_alpha);
  }
  if (!(kdRatio > 0 && kdRatio <= 1)) {
    throw new Error("KD ratio must be in (0, 1]; got " + kdRatio +
      ". Above one would make the head lighter than the trunk.");
  }
  if (raiseCrest < 0) throw new Error("Crest rise must be non-negative");

  var Dn50 = design.Dn50 / Math.pow(kdRatio, 1 / 3);
  var head = {};
  for (var k in design) head[k] = design[k];
  head.Dn50 = Dn50;
  head.M50 = design.density * Dn50 * Dn50 * Dn50;
  head.layer = layerFor(design.armour_type, Dn50, design.density);
  head.underlayer_Dn50 = Math.pow(head.M50 / 10 / RHO_S, 1 / 3);
  head.crest_freeboard = design.crest_freeboard + raiseCrest;
  head.section = "head";
  head.kd_ratio = kdRatio;
  return head;
}

function moundFoundation(design, depth, opts) {
  opts = opts || {};
  var bed = opts.bed || "medium_sand";
  var permeable = opts.permeable === undefined ? true : opts.permeable;
  var blanket = sediment(opts.bedding_material || "coarse_sand");
  var settlement = opts.settlement_allowance || 0;
  if (settlement < 0) throw new Error("Settlement allowance must be non-negative");

  var scour = breakwaterToeScour(design, depth, bed, permeable);

  /* The toe berm takes filter stone, not armour: it sits low, where the
     orbital velocities are far smaller than at the waterline. */
  var DnFilter = design.underlayer_Dn50;
  var toeThickness = 2.0 * DnFilter;
  var toeWidth = Math.max(3.0 * DnFilter, 0.5 * design.conditions.Hm0, 2.0);
  var beddingThickness = Math.max(0.6, 1.5 * DnFilter) + settlement;
  var extension = Math.max(scour.apron_width, 2.0 * scour.depth, 3.0);

  return {
    scour: scour, toe_Dn50: DnFilter, toe_M50: 2650.0 * Math.pow(DnFilter, 3),
    toe_width: toeWidth, toe_thickness: toeThickness,
    bedding: blanket, bedding_thickness: beddingThickness,
    bedding_extension: extension, settlement_allowance: settlement,
    geotextile: true
  };
}

function pedersenCrownLoads(c, cotAlpha, Ac, bermWidth, hProt, fc) {
  if (!(bermWidth > 0)) throw new Error("Berm width must be positive");
  var Hs = c.Hm0;
  var Lom = G * c.mean_period * c.mean_period / (2 * Math.PI);
  var alpha = Math.atan(1 / cotAlpha);
  var xiM = Math.tan(alpha) / Math.sqrt(Hs / Lom);
  var Ru = xiM <= 1.5 ? 1.12 * Hs * xiM : 1.34 * Hs * Math.pow(xiM, 0.55);
  var pm = Math.max(RHO_W * G * (Ru - Ac) / 1000, 0);
  var r15 = 15 * Math.PI / 180;
  var y = Math.max((Ru - Ac) / Math.sin(alpha) * Math.sin(r15) / Math.cos(alpha - r15), 0);
  var yEff = Math.min(y / 2, fc);
  var A = 1.0;
  var scale = 0.21 * Math.sqrt(Lom / bermWidth);
  var Fh = scale * (1.6 * pm * yEff + A * pm / 2 * hProt);
  var M = 0.55 * (hProt + yEff) * Fh;
  var outside = [];
  var checks = [["xi_m", xiM, 1.1, 5.2],
                ["Hm0/Ac", Ac > 0 ? Hs / Ac : Infinity, 0.5, 1.5],
                ["Ac/B", Ac / bermWidth, 1.0, 2.6],
                ["cot a", cotAlpha, 1.5, 3.5],
                ["Hm0/h", Hs / c.depth, 0.16, 0.35]];
  for (var i = 0; i < checks.length; i++) {
    var k = checks[i];
    if (!(k[1] >= k[2] && k[1] <= k[3])) {
      outside.push(k[0] + " = " + k[1].toFixed(2) + " (tested " + fmtG(k[2]) +
                   " to " + fmtG(k[3]) + ")");
    }
  }
  return { Fh: Fh, M: M, pb: A * pm, p_m: pm, Ru: Ru, xi_m: xiM, y: y,
           y_eff: yEff, A: A, Lom: Lom, outside: outside };
}

function crownWall(design, stillWaterLevel, opts) {
  opts = opts || {};
  var deckWidth = opts.deck_width === undefined ? 7.5 : opts.deck_width;
  var parapetWidth = opts.parapet_width === undefined ? 2.0 : opts.parapet_width;
  var friction = opts.friction === undefined ? 0.6 : opts.friction;
  var targetSliding = opts.target_sliding === undefined ? 1.2 : opts.target_sliding;
  var targetOverturning = opts.target_overturning === undefined ? 1.5 : opts.target_overturning;
  var maxDeck = opts.max_deck_width === undefined ? 25.0 : opts.max_deck_width;
  var step = opts.step === undefined ? 0.25 : opts.step;
  var crest = stillWaterLevel + design.crest_freeboard;
  var parapetHeight = opts.parapet_height === undefined
    ? Math.max(0.3 * design.conditions.Hm0, 1.0) : opts.parapet_height;
  var baseBelow = opts.base_below_crest === undefined
    ? design.layer.thickness : opts.base_below_crest;
  var bermWidth = opts.berm_width === undefined
    ? Math.max(3.0 * design.Dn50, 2.0) : opts.berm_width;
  if (deckWidth <= 0 || parapetWidth <= 0) {
    throw new Error("Deck and parapet widths must be positive");
  }
  var baseLevel = crest - baseBelow;
  var parapetTop = crest + parapetHeight;
  var loads = pedersenCrownLoads(design.conditions, design.cot_alpha,
                                 design.crest_freeboard, bermWidth, baseBelow,
                                 parapetHeight);
  var gammaC = RHO_CONCRETE * G / 1000, gammaW = RHO_W * G / 1000;
  function blockWeight(z0, z1, w) {
    var wet = Math.min(Math.max(stillWaterLevel - z0, 0), z1 - z0);
    return (gammaC * (z1 - z0) - gammaW * wet) * w;
  }
  var warnings = [], sliding = 0, overturning = 0, W = 0, uplift = 0, total = 0;
  for (;;) {
    total = parapetWidth + deckWidth;
    var parts = [[blockWeight(baseLevel, parapetTop, parapetWidth), total - 0.5 * parapetWidth],
                 [blockWeight(baseLevel, crest, deckWidth), 0.5 * deckWidth]];
    W = parts[0][0] + parts[1][0];
    uplift = 0.5 * loads.pb * total;
    if (loads.Fh > 0) {
      sliding = friction * Math.max(W - uplift, 0) / loads.Fh;
      var resisting = parts[0][0] * parts[0][1] + parts[1][0] * parts[1][1] -
                      uplift * (2 / 3) * total;
      overturning = Math.max(resisting, 0) / loads.M;
    } else {
      sliding = Infinity; overturning = Infinity;
    }
    if (sliding >= targetSliding && overturning >= targetOverturning) break;
    if (deckWidth >= maxDeck) {
      warnings.push("The crown block reached a " + total.toFixed(1) + " m width with " +
        "sliding " + sliding.toFixed(2) + " and overturning " + overturning.toFixed(2) +
        ". Lower the parapet, widen the armour berm in front of it or key the base " +
        "into the core.");
      break;
    }
    deckWidth += step;
  }
  if (loads.outside.length) {
    warnings.push("Pedersen crown wall loads applied outside the tested range: " +
                  loads.outside.join("; ") + ".");
  }
  var area = parapetWidth * (parapetTop - baseLevel) + deckWidth * (crest - baseLevel);
  return {
    base_level: baseLevel, deck_level: crest, parapet_top: parapetTop,
    parapet_width: parapetWidth, deck_width: deckWidth,
    total_width: parapetWidth + deckWidth, berm_width: bermWidth,
    concrete_m3_per_m: area, concrete_t_per_m: area * RHO_CONCRETE / 1000,
    loads: loads, weight: W, uplift: uplift,
    sliding_FoS: sliding, overturning_FoS: overturning, warnings: warnings
  };
}

function dredgedSideSlope(bed, factor) {
  factor = factor === undefined ? 2.0 : factor;
  var grains = sediment(bed);
  if (!(factor > 0)) throw new Error("Factor must be positive");
  if (grains.cohesive) {
    return { cot_beta: 3.0, governed_by: "cohesion",
             note: grains.name + " is cohesive; a drained friction slope does " +
                   "not govern it. 1:3 is a placeholder pending an undrained " +
                   "stability analysis." };
  }
  return {
    cot_beta: factor / Math.tan(grains.friction_angle * Math.PI / 180),
    governed_by: "friction", friction_angle: grains.friction_angle,
    note: "Steepest defensible slope in " + grains.name + " with a factor of " +
          factor + " on tan(phi')."
  };
}

/* ------------------------------------------------------------------ */
/* Beach nourishment, cross-shore                                      */
/* ------------------------------------------------------------------ */

function phiSize(d50) {
  if (!(d50 > 0)) throw new Error("Grain size must be positive");
  return -Math.log(d50 * 1000) / Math.LN2;
}

function sizeFromPhi(phi) { return Math.pow(2, -phi) / 1000; }

/* A = 0.067 w^0.44 with w in cm/s (Kriebel, Kraus and Larson 1991), so the
   profile scale comes from the same fall velocity the scour work uses. */
function deanScale(material, viscosity) {
  var grains = sediment(material);
  if (grains.cohesive || !(grains.d50 > 0)) {
    throw new Error(grains.name + " is cohesive. An equilibrium sand profile " +
      "does not describe it, and a beach cannot be built from it.");
  }
  return 0.067 * Math.pow(fallVelocity(grains, viscosity) * 100, 0.44);
}

function equilibriumProfile(A, y) {
  if (!(A > 0)) throw new Error("Profile scale must be positive");
  return A * Math.pow(Math.max(y, 0), 2 / 3);
}

function profileWidth(A, depth) {
  if (!(A > 0) || depth < 0) {
    throw new Error("Scale must be positive and depth non-negative");
  }
  return Math.pow(depth / A, 1.5);
}

/* The offset between the nourished and native profiles, integrated over
   depth to the closure contour, plus the dry berm. With matched sand every
   term but the first two vanishes and this is exactly (B + h*) a. */
function fillVolumeForAdvance(Anative, Afill, advance, bermHeight, closureDepth) {
  if (advance < 0) throw new Error("Advance must be non-negative");
  if (bermHeight < 0) throw new Error("Berm height must be non-negative");
  if (!(closureDepth > 0)) throw new Error("Closure depth must be positive");
  if (!(Anative > 0) || !(Afill > 0)) throw new Error("Profile scales must be positive");

  var kn = Math.pow(Anative, -1.5);
  var kf = Math.pow(Afill, -1.5);
  var meetingDepth = null, intersects = false;
  if (kf < kn) {
    meetingDepth = advance > 0 ? Math.pow(advance / (kn - kf), 2 / 3) : 0;
    intersects = meetingDepth <= closureDepth;
  }
  var limit = meetingDepth !== null ? Math.min(meetingDepth, closureDepth)
                                    : closureDepth;
  var volume = bermHeight * advance + advance * limit +
               0.4 * Math.pow(limit, 2.5) * (kf - kn);
  var meeting = null;
  if (intersects && meetingDepth !== null && meetingDepth > 0) {
    meeting = advance + Math.pow(meetingDepth / Afill, 1.5);
  }
  return {
    volume: volume, berm_volume: bermHeight * advance, limit_depth: limit,
    meeting_depth: intersects ? meetingDepth : null, meeting: meeting,
    intersects: intersects
  };
}

function criticalVolume(Anative, Afill, bermHeight, closureDepth) {
  if (Afill >= Anative) return 0;
  return fillVolumeForAdvance(Anative, Afill, 0, bermHeight, closureDepth).volume;
}

function shorelineAdvance(Anative, Afill, volume, bermHeight, closureDepth, tol) {
  tol = tol === undefined ? 1e-4 : tol;
  if (volume < 0) throw new Error("Volume must be non-negative");

  var critical = criticalVolume(Anative, Afill, bermHeight, closureDepth);
  if (volume <= critical) {
    return {
      advance: 0, kind: "submerged", critical_volume: critical, volume: volume,
      meeting: null, meeting_depth: null, limit_depth: closureDepth,
      note: volume.toFixed(0) + " m3/m of fill this fine does not reach the " +
        "critical " + critical.toFixed(0) + " m3/m, so none of it appears as " +
        "dry beach. It forms a submerged terrace instead."
    };
  }

  var low = 0, high = 10;
  while (fillVolumeForAdvance(Anative, Afill, high, bermHeight, closureDepth).volume < volume) {
    high *= 2;
    if (high > 1e5) throw new Error("No advance within 100 km delivers that volume");
  }
  while (high - low > tol) {
    var mid = 0.5 * (low + high);
    if (fillVolumeForAdvance(Anative, Afill, mid, bermHeight, closureDepth).volume < volume) {
      low = mid;
    } else {
      high = mid;
    }
  }
  var advance = 0.5 * (low + high);
  var detail = fillVolumeForAdvance(Anative, Afill, advance, bermHeight, closureDepth);

  var kind, note;
  if (Math.abs(Afill - Anative) < 1e-9) {
    kind = "matched";
    note = "The borrow matches the native sand, so the profile simply " +
      "translates seaward and every cubic metre buys the same width.";
  } else if (detail.intersects) {
    kind = "intersecting";
    note = "The fill is coarser than the native sand, so it stands steeper " +
      "and meets the native profile " + detail.meeting.toFixed(0) +
      " m offshore, at " + detail.meeting_depth.toFixed(1) + " m depth. " +
      "Every cubic metre works on the visible beach.";
  } else {
    kind = "non-intersecting";
    note = "The fill is finer than the native sand, so it lies flatter and " +
      "never meets the native profile: the placement runs all the way to " +
      "closure, and part of it does nothing for the dry beach.";
  }
  return {
    advance: advance, kind: kind, critical_volume: critical, volume: volume,
    meeting: detail.meeting, meeting_depth: detail.meeting_depth,
    limit_depth: detail.limit_depth, note: note
  };
}

function profileOverfillFactor(native, borrow, bermHeight, closureDepth, advance) {
  advance = advance === undefined ? 30 : advance;
  var An = deanScale(native), Ab = deanScale(borrow);
  var nativeVolume = fillVolumeForAdvance(An, An, advance, bermHeight, closureDepth).volume;
  var borrowVolume = fillVolumeForAdvance(An, Ab, advance, bermHeight, closureDepth).volume;
  return {
    factor: nativeVolume > 0 ? borrowVolume / nativeVolume : Infinity,
    native_volume: nativeVolume, borrow_volume: borrowVolume,
    A_native: An, A_borrow: Ab, advance: advance
  };
}

function grainCompatibility(native, borrow) {
  native = sediment(native);
  borrow = sediment(borrow);
  [native, borrow].forEach(function (g) {
    if (g.cohesive || !(g.d50 > 0)) {
      throw new Error(g.name + " is not a beach material");
    }
  });
  var phiNative = phiSize(native.d50);
  var phiBorrow = phiSize(borrow.d50);
  var delta = (phiBorrow - phiNative) / native.phi_sorting;
  var ratio = borrow.phi_sorting / native.phi_sorting;

  var verdict;
  if (delta <= -0.5) verdict = "coarser than native, well suited";
  else if (delta < 0.25) verdict = "close to native, suitable";
  else if (delta < 1.0) verdict = "finer than native, expect losses";
  else verdict = "much finer than native, poorly suited";
  if (ratio > 1.5 && delta > -0.5) {
    verdict += "; also more poorly sorted, so the fines will winnow out";
  }
  return {
    phi_native: phiNative, phi_borrow: phiBorrow, delta: delta,
    sorting_ratio: ratio, coarser: delta < 0, verdict: verdict
  };
}

/* ------------------------------------------------------------------ */
/* Extreme values                                                      */
/* ------------------------------------------------------------------ */

function lMoments(sample, count) {
  count = count === undefined ? 4 : count;
  if (count < 1 || count > 4) throw new Error("Can return 1 to 4 L-moments");
  var x = sample.slice().sort(function (a, b) { return a - b; });
  var n = x.length;
  if (n < count) throw new Error("Need at least " + count + " points");

  var b = [0, 0, 0, 0];
  var sum = 0;
  for (var i = 0; i < n; i++) sum += x[i];
  b[0] = sum / n;
  var s1 = 0;
  for (i = 0; i < n; i++) s1 += (i) / (n - 1) * x[i];
  b[1] = s1 / n;
  if (count > 2) {
    var s2 = 0;
    for (i = 0; i < n; i++) s2 += (i) * (i - 1) / ((n - 1) * (n - 2)) * x[i];
    b[2] = s2 / n;
  }
  if (count > 3) {
    var s3 = 0;
    for (i = 0; i < n; i++) {
      s3 += (i) * (i - 1) * (i - 2) / ((n - 1) * (n - 2) * (n - 3)) * x[i];
    }
    b[3] = s3 / n;
  }
  var lam = [b[0]];
  if (count > 1) lam.push(2 * b[1] - b[0]);
  if (count > 2) lam.push(6 * b[2] - 6 * b[1] + b[0]);
  if (count > 3) lam.push(20 * b[3] - 30 * b[2] + 12 * b[1] - b[0]);
  return lam;
}

function fitGpd(excesses) {
  if (excesses.length < 2) throw new Error("Need at least two excesses to fit");
  for (var i = 0; i < excesses.length; i++) {
    if (excesses[i] < 0) throw new Error("Excesses must be non-negative");
  }
  var lam = lMoments(excesses, 2);
  var l1 = lam[0], l2 = lam[1];
  if (l1 <= 0 || l2 <= 0) throw new Error("Excesses have no spread");
  var tau = l2 / l1;
  var shape = 2.0 - 1.0 / tau;
  var scale = l1 * (1.0 - shape);
  if (scale <= 0) throw new Error("Fitted scale is not positive; try a higher threshold");
  return { scale: scale, shape: shape };
}

function gpdReturnValue(threshold, scale, shape, rate, returnPeriod) {
  if (!(scale > 0)) throw new Error("Scale must be positive");
  if (!(rate > 0)) throw new Error("Peak rate must be positive");
  if (!(returnPeriod > 0)) throw new Error("Return periods must be positive");
  var m = rate * returnPeriod;
  if (Math.abs(shape) < 1e-8) return threshold + scale * Math.log(m);
  return threshold + scale / shape * (Math.pow(m, shape) - 1.0);
}

function gevReturnValue(location, scale, shape, returnPeriod) {
  if (!(scale > 0)) throw new Error("Scale must be positive");
  if (!(returnPeriod > 1.0)) throw new Error("Block maxima return periods must exceed one block");
  var y = -Math.log(-Math.log(1.0 - 1.0 / returnPeriod));
  if (Math.abs(shape) < 1e-8) return location + scale * y;
  return location + scale / shape * (Math.exp(shape * y) - 1.0);
}


/* ------------------------------------------------------------------ */
/* Beach nourishment, planform                                         */
/* ------------------------------------------------------------------ */

/* erf to double precision, via the incomplete gamma function.
 *
 * The usual pocket approximations (Abramowitz and Stegun 7.1.26 and
 * friends) are good to about 1e-7, which is fine for a picture and useless
 * here: verify_engine.py holds this file to 1e-9 against Python's
 * math.erf, and a 1e-7 erf would show up as a real disagreement. The
 * series and continued fraction below both converge to machine epsilon.
 */
var _LN_GAMMA_HALF = 0.5723649429247001;   /* ln(sqrt(pi)) */

function _gammpSeries(a, x) {
  var ap = a, sum = 1.0 / a, del = sum;
  for (var n = 1; n <= 300; n++) {
    ap += 1.0;
    del *= x / ap;
    sum += del;
    if (Math.abs(del) < Math.abs(sum) * 1e-17) break;
  }
  return sum * Math.exp(-x + a * Math.log(x) - _LN_GAMMA_HALF);
}

function _gammqFraction(a, x) {
  var tiny = 1e-300;
  var b = x + 1.0 - a, c = 1.0 / tiny, d = 1.0 / b, h = d;
  for (var i = 1; i <= 300; i++) {
    var an = -i * (i - a);
    b += 2.0;
    d = an * d + b;
    if (Math.abs(d) < tiny) d = tiny;
    c = b + an / c;
    if (Math.abs(c) < tiny) c = tiny;
    d = 1.0 / d;
    var del = d * c;
    h *= del;
    if (Math.abs(del - 1.0) < 1e-17) break;
  }
  return Math.exp(-x + a * Math.log(x) - _LN_GAMMA_HALF) * h;
}

function erf(x) {
  if (x === 0) return 0;
  if (!isFinite(x)) return x > 0 ? 1 : -1;
  var ax = Math.abs(x), z = ax * ax;
  var value = z < 1.5 ? _gammpSeries(0.5, z) : 1.0 - _gammqFraction(0.5, z);
  return x < 0 ? -value : value;
}

var SECONDS_PER_YEAR = 365.25 * 24 * 3600.0;

function cercCoefficient(K, s, gammaB, g) {
  K = K === undefined ? 0.39 : K;
  s = s === undefined ? 2.65 : s;
  gammaB = gammaB === undefined ? 0.78 : gammaB;
  g = g === undefined ? 9.81 : g;
  return K * Math.sqrt(g / gammaB) / (16.0 * (s - 1.0));
}

var KCERC_DEFAULT = cercCoefficient();

function makeClimate(Hb, T, alpha0, Kcerc) {
  Hb = Hb === undefined ? 1.0 : Hb;
  T = T === undefined ? 8.0 : T;
  if (Hb <= 0) throw new Error("Breaking wave height must be positive");
  if (T <= 0) throw new Error("Wave period must be positive");
  return {
    Hb: Hb, T: T,
    alpha0: alpha0 === undefined ? 0.0 : alpha0,
    Kcerc: Kcerc === undefined ? KCERC_DEFAULT : Kcerc
  };
}

function makeFill(length, bermWidth, taper, D, B, porosity) {
  if (length <= 0) throw new Error("Fill length must be positive");
  if (bermWidth <= 0) throw new Error("Berm width must be positive");
  taper = taper === undefined ? 100.0 : taper;
  if (taper < 0) throw new Error("Taper cannot be negative");
  porosity = porosity === undefined ? 0.4 : porosity;
  if (porosity < 0 || porosity >= 1) throw new Error("Porosity must be in [0,1)");
  D = D === undefined ? 8.0 : D;
  B = B === undefined ? 2.0 : B;
  return {
    length: length, berm_width: bermWidth, taper: taper,
    D: D, B: B, porosity: porosity,
    active_height: D + B,
    placed_volume: bermWidth * (length + taper) * (D + B)
  };
}

function longshoreDiffusivity(climate, design) {
  return 2.0 * climate.Kcerc * Math.pow(climate.Hb, 2.5)
    / ((1.0 - design.porosity) * design.active_height);
}

/* Pelnard-Considere (1956): a rectangular fill spreading by diffusion. */
function pelnardConsidere(x, t, design, climate) {
  var a = 0.5 * design.length, out = new Array(x.length), i;
  if (t <= 0) {
    for (i = 0; i < x.length; i++) {
      out[i] = Math.abs(x[i]) <= a ? design.berm_width : 0.0;
    }
    return out;
  }
  var denom = 2.0 * Math.sqrt(longshoreDiffusivity(climate, design) * t);
  for (i = 0; i < x.length; i++) {
    out[i] = 0.5 * design.berm_width
      * (erf((a - x[i]) / denom) + erf((a + x[i]) / denom));
  }
  return out;
}

/* erfinv(1/2): the argument at which the centre width is halved. */
var ERFINV_HALF = 0.4769362762044698733814;

function spreadingHalfLife(design, climate) {
  var half = 0.5 * design.length;
  return half * half
    / (4.0 * ERFINV_HALF * ERFINV_HALF * longshoreDiffusivity(climate, design));
}

function planMargin(design, climate, years) {
  var longest = Math.max.apply(null, years) * SECONDS_PER_YEAR;
  var spread = longest > 0
    ? Math.sqrt(longshoreDiffusivity(climate, design) * longest) : 0.0;
  return Math.max(1.4 * spread, 0.6 * design.length, 200.0);
}

function planYears(design, climate) {
  var h = spreadingHalfLife(design, climate) / SECONDS_PER_YEAR;
  var out = [0.0], f = [0.5, 1.0, 2.0, 4.0], i;
  for (i = 0; i < f.length; i++) out.push(Math.round(f[i] * h * 100) / 100);
  return out;
}

/* Everything the plan view and its summary need, from one call. */
function planformEvolution(design, climate, years, samples) {
  years = years || planYears(design, climate);
  samples = samples || 601;
  var margin = planMargin(design, climate, years);
  var half = 0.5 * design.length;
  var x0 = -half - margin, x1 = half + margin;
  var x = new Array(samples), i;
  for (i = 0; i < samples; i++) x[i] = x0 + (x1 - x0) * i / (samples - 1);

  var curves = [], peak = 0.0;
  for (i = 0; i < years.length; i++) {
    var y = pelnardConsidere(x, years[i] * SECONDS_PER_YEAR, design, climate);
    var c = 0.0, j;
    for (j = 0; j < y.length; j++) if (y[j] > c) c = y[j];
    if (c > peak) peak = c;
    curves.push({ year: years[i], y: y, centre: y[(samples - 1) / 2 | 0] });
  }
  var longest = Math.max.apply(null, years) * SECONDS_PER_YEAR;
  return {
    x: x, x0: x0, x1: x1, curves: curves, peak: peak, margin: margin,
    years: years,
    diffusivity: longshoreDiffusivity(climate, design),
    half_life: spreadingHalfLife(design, climate) / SECONDS_PER_YEAR,
    spread: longest > 0
      ? Math.sqrt(longshoreDiffusivity(climate, design) * longest) : 0.0,
    centre_now: curves[0].centre,
    centre_last: curves[curves.length - 1].centre,
    retained: curves[curves.length - 1].centre / design.berm_width
  };
}

/* Node and browser both, without assuming either. */
var PYCOASTAL = {
  dispersion: dispersion,
  makeConditions: makeConditions,
  conditionsFromPeak: conditionsFromPeak,
  ROUGHNESS_FACTORS: ROUGHNESS_FACTORS,
  TOLERABLE_DISCHARGE: TOLERABLE_DISCHARGE,
  MANOEUVRING_LANE: MANOEUVRING_LANE,
  WIDTH_COMPONENTS: WIDTH_COMPONENTS,
  BANK_CLEARANCE: BANK_CLEARANCE,
  PASSING_DISTANCE: PASSING_DISTANCE,
  rockArmourVanDerMeer: rockArmourVanDerMeer,
  armourLayer: armourLayer,
  CONCRETE_UNITS: CONCRETE_UNITS,
  concreteArmour: concreteArmour,
  layerFor: layerFor,
  depthLimitWarnings: depthLimitWarnings,
  overtoppingSloped: overtoppingSloped,
  overtoppingVertical: overtoppingVertical,
  requiredCrestFreeboard: requiredCrestFreeboard,
  assessOvertopping: assessOvertopping,
  designRubbleMound: designRubbleMound,
  godaPressures: godaPressures,
  godaBreakingHeight: godaBreakingHeight,
  scourDepthVerticalWall: scourDepthVerticalWall,
  toeStoneSize: toeStoneSize,
  toeStoneTanimoto: toeStoneTanimoto,
  stemSection: stemSection,
  slidingSafety: slidingSafety,
  overturningSafety: overturningSafety,
  bearingPressures: bearingPressures,
  designSeawall: designSeawall,
  makeVessel: makeVessel,
  squatIcorels: squatIcorels,
  squatBarrass: squatBarrass,
  waveResponseAllowance: waveResponseAllowance,
  underkeelClearance: underkeelClearance,
  channelWidth: channelWidth,
  designChannel: designChannel,
  waveKinematics: waveKinematics,
  StreamFunctionWave: StreamFunctionWave,
  streamFunctionWave: streamFunctionWave,
  bedKeuleganCarpenter: bedKeuleganCarpenter,
  keuleganCarpenter: keuleganCarpenter,
  dragInertiaCoefficients: dragInertiaCoefficients,
  morisonPileLoad: morisonPileLoad,
  phaseSweep: phaseSweep,
  scourDepthPile: scourDepthPile,
  designMonopile: designMonopile,
  SEDIMENTS: SEDIMENTS,
  sediment: sediment,
  makeSediment: makeSediment,
  dimensionlessGrainSize: dimensionlessGrainSize,
  criticalShields: criticalShields,
  fallVelocity: fallVelocity,
  waveOrbitalVelocity: waveOrbitalVelocity,
  waveShields: waveShields,
  bedMobility: bedMobility,
  earthPressureCoefficient: earthPressureCoefficient,
  lateralEarthPressure: lateralEarthPressure,
  lateralEarthForce: lateralEarthForce,
  hydrostaticForce: hydrostaticForce,
  reflectionCoefficient: reflectionCoefficient,
  toeScour: toeScour,
  breakwaterToeScour: breakwaterToeScour,
  dredgedSideSlope: dredgedSideSlope,
  moundFoundation: moundFoundation,
  roundhead: roundhead,
  roundheadKdRatio: roundheadKdRatio,
  ROUNDHEAD_KD_RATIO: ROUNDHEAD_KD_RATIO,
  crownWall: crownWall,
  pedersenCrownLoads: pedersenCrownLoads,
  phiSize: phiSize,
  sizeFromPhi: sizeFromPhi,
  deanScale: deanScale,
  equilibriumProfile: equilibriumProfile,
  profileWidth: profileWidth,
  fillVolumeForAdvance: fillVolumeForAdvance,
  criticalVolume: criticalVolume,
  shorelineAdvance: shorelineAdvance,
  profileOverfillFactor: profileOverfillFactor,
  erf: erf,
  cercCoefficient: cercCoefficient,
  makeClimate: makeClimate,
  makeFill: makeFill,
  longshoreDiffusivity: longshoreDiffusivity,
  pelnardConsidere: pelnardConsidere,
  spreadingHalfLife: spreadingHalfLife,
  planMargin: planMargin,
  planYears: planYears,
  planformEvolution: planformEvolution,
  SECONDS_PER_YEAR: SECONDS_PER_YEAR,
  grainCompatibility: grainCompatibility,
  lMoments: lMoments,
  fitGpd: fitGpd,
  gpdReturnValue: gpdReturnValue,
  gevReturnValue: gevReturnValue
};

if (typeof module !== "undefined" && module.exports) module.exports = PYCOASTAL;
if (typeof globalThis !== "undefined") globalThis.PYCOASTAL = PYCOASTAL;
