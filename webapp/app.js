/*
 * Design studio and literature browser.
 *
 * Two halves that only make sense together. The left half sizes a structure
 * with the pyCoastal relations; the right half shows what the corpus says
 * about the ground those relations stand on, including where they stop
 * being valid.
 */

var P = globalThis.PYCOASTAL;
var D = globalThis.DRAW;

var STATE = {
  module: "seawall",
  knowledge: null,
  knowledgePending: false,
  vectors: null,
  topic: null,
  verified: null
};

/* ------------------------------------------------------------------ */
/* Module definitions: inputs, run, and how to present the answer      */
/* ------------------------------------------------------------------ */

var MODULES = {
  seawall: {
    label: "Seawall",
    note: "Gravity L-wall: crest from EurOtop, base from Goda and the backfill, stem as an RC cantilever.",
    inputs: [
      { key: "Hm0", label: "Wave height Hm0", unit: "m", min: 0.5, max: 8, step: 0.1, value: 2.0 },
      { key: "Tp", label: "Peak period Tp", unit: "s", min: 4, max: 18, step: 0.1, value: 8.0 },
      { key: "swl", label: "Still water level", unit: "m CD", min: -1, max: 6, step: 0.1, value: 2.5 },
      { key: "bed", label: "Seabed level", unit: "m CD", min: -20, max: 2, step: 0.1, value: -1.0 },
      { key: "use", label: "Tolerable overtopping", type: "select", value: "trained_staff",
        options: ["pedestrians_unaware", "pedestrians_aware", "harbour_quay_equipment",
                  "trained_staff", "vehicles_low_speed"] },
      { key: "beta", label: "Wave angle", unit: "deg", min: 0, max: 60, step: 5, value: 0 },
      { key: "scour", label: "Scour coefficient", unit: "", min: 0, max: 0.6, step: 0.05, value: 0.4 },
      { key: "backfill", label: "Backfill material", type: "select",
        value: "medium_sand", options: ["silt", "very_fine_sand", "fine_sand", "medium_sand",
                  "coarse_sand", "fine_gravel", "coarse_gravel",
                  "rock_fill", "soft_clay", "stiff_clay"] },
      { key: "table", label: "Water table below surface", unit: "m", min: 0, max: 16, step: 0.5, value: 0 },
      { key: "surcharge", label: "Surcharge on the promenade", unit: "kPa", min: 0, max: 60, step: 5, value: 10 },
      { key: "bearing", label: "Allowable bearing", unit: "kPa", min: 100, max: 800, step: 25, value: 300 }
    ],
    run: function (v) {
      var c = P.conditionsFromPeak(v.Hm0, v.Tp, v.swl - v.bed, 6 * 3600);
      return P.designSeawall(c, v.swl, v.bed, {
        tolerable_use: v.use, beta_degrees: v.beta, scour_coefficient: v.scour,
        backfill: v.backfill, water_table: v.table, surcharge: v.surcharge,
        allowable_bearing: v.bearing
      });
    },
    draw: function (host, d, w, h) { D.drawSeawall(host, d, w, h); },
    checks: function (d) {
      return [
        { name: "Sliding", value: fos(d.sliding_FoS), target: "FoS ≥ 1.20",
          eta: 1.2 / d.sliding_FoS, ok: d.sliding_FoS >= 1.2 },
        { name: "Overturning", value: fos(d.overturning_FoS), target: "FoS ≥ 1.50",
          eta: 1.5 / d.overturning_FoS, ok: d.overturning_FoS >= 1.5 },
        { name: "Resultant", value: (d.bearing.e >= 0 ? "+" : "") + d.bearing.e.toFixed(2) + " m",
          target: "|e| ≤ B/6 = " + (d.base_width / 6).toFixed(2) + " m",
          eta: Math.abs(d.bearing.e) / (d.base_width / 6), ok: d.bearing.middle_third },
        { name: "Bearing", value: d.bearing.p_max.toFixed(0) + " kPa",
          target: "≤ " + d.allowable_bearing.toFixed(0) + " kPa",
          eta: d.bearing.p_max / d.allowable_bearing,
          ok: d.bearing.p_max <= d.allowable_bearing * 1.0001 },
        { name: "Overtopping", value: d.q_upper.toPrecision(3) + " l/s/m",
          target: "≤ " + P.TOLERABLE_DISCHARGE[d.governing_limit][0] + " l/s/m",
          eta: d.q_upper / P.TOLERABLE_DISCHARGE[d.governing_limit][0],
          ok: d.q_upper <= P.TOLERABLE_DISCHARGE[d.governing_limit][0] * 1.001 },
        { name: "Drawdown sliding",
          value: fos(d.drawdown.sliding_FoS), target: "FoS ≥ 1.20",
          eta: 1.2 / d.drawdown.sliding_FoS,
          ok: d.drawdown.sliding_FoS >= 1.2 },
        { name: "Drawdown overturning",
          value: fos(d.drawdown.overturning_FoS), target: "FoS ≥ 1.50",
          eta: 1.5 / d.drawdown.overturning_FoS,
          ok: d.drawdown.overturning_FoS >= 1.5 },
        { name: "Drawdown resultant",
          value: (d.drawdown.bearing.e >= 0 ? "+" : "") + d.drawdown.bearing.e.toFixed(2) + " m",
          target: "|e| ≤ B/6 = " + (d.base_width / 6).toFixed(2) + " m",
          eta: Math.abs(d.drawdown.bearing.e) / (d.base_width / 6),
          ok: d.drawdown.bearing.middle_third },
        { name: "Drawdown bearing", value: d.drawdown.bearing.p_max.toFixed(0) + " kPa",
          target: "≤ " + d.allowable_bearing.toFixed(0) + " kPa",
          eta: d.drawdown.bearing.p_max / d.allowable_bearing,
          ok: d.drawdown.bearing.p_max <= d.allowable_bearing * 1.0001 },
        { name: "Stem", value: d.stem_thickness.toFixed(2) + " m",
          target: "≥ " + d.stem.thickness.toFixed(2) + " m for M_Ed, V_Ed",
          eta: d.stem.thickness / d.stem_thickness,
          ok: d.stem_thickness >= d.stem.thickness - 1e-9 },
        { name: "Retained height", value: d.retained_height.toFixed(1) + " m",
          target: "≤ 8 m for an L-wall",
          eta: d.retained_height / 8, ok: d.retained_height <= 8,
          warn: d.retained_height > 8 },
        { name: "Governs", value: d.governing_case,
          target: d.governing_case === "drawdown" ? "backfill, not wave" : "wave, not backfill",
          ok: true, neutral: true },
        { name: "Pore water share",
          value: (100 * d.earth_driving.water_fraction).toFixed(0) + "%",
          target: "of the back pressure",
          ok: d.earth_driving.water_fraction <= 0.6,
          warn: d.earth_driving.water_fraction > 0.6 }
      ];
    },
    report: function (d) {
      var q = d.quantities;
      return [
        ["Crest level", fmt(d.crest_level) + " m CD"],
        ["Crest freeboard Rc", d.crest_freeboard.toFixed(2) + " m"],
        ["Founding level", fmt(d.founding_level) + " m CD"],
        ["Embedment", d.embedment.toFixed(2) + " m"],
        ["Predicted scour", d.scour_depth.toFixed(2) + " m"],
        ["Wall height", d.wall_height.toFixed(2) + " m"],
        ["Base width B", d.base_width.toFixed(2) + " m"],
        ["Stem, base thickness", d.stem_thickness.toFixed(2) + ", " + d.base_thickness.toFixed(2) + " m"],
        ["  stem M_Ed", d.stem.moment.toFixed(0) + " kNm/m"],
        ["  stem V_Ed", d.stem.shear.toFixed(0) + " kN/m"],
        [null, null],
        ["Goda Hmax", d.pressures.Hmax.toFixed(2) + " m" + (d.pressures.depth_limited ? " (breaking)" : "")],
        ["Goda p1", d.pressures.p1.toFixed(1) + " kPa"],
        ["Uplift pu", d.pressures.pu.toFixed(1) + " kPa"],
        ["Wave force", d.wave_force.toFixed(0) + " kN/m"],
        ["Lever arm", d.wave_arm.toFixed(2) + " m"],
        ["Total weight", d.weight.toFixed(0) + " kN/m"],
        ["Hydrostatic uplift", d.static_uplift.toFixed(0) + " kN/m"],
        ["Bearing p max", d.bearing.p_max.toFixed(0) + " / " + d.drawdown.bearing.p_max.toFixed(0) + " kPa"],
        [null, null],
        ["Backfill", d.backfill.name],
        ["  friction angle", d.backfill.friction_angle.toFixed(0) + " deg"],
        ["  retained height", d.retained_height.toFixed(2) + " m"],
        ["  water table", fmt(d.back_water_level) + " m CD"],
        ["  K used", d.earth_driving.K.toFixed(3) + " (" + d.earth_driving.kind.replace("_", " ") + ")"],
        ["  soil force", d.earth_driving.soil.toFixed(0) + " kN/m"],
        ["  pore water force", d.earth_driving.water.toFixed(0) + " kN/m"],
        ["  total, at", d.earth_driving.total.toFixed(0) + " kN/m @ " + d.earth_driving.arm.toFixed(2) + " m"],
        [null, null],
        ["Trough level", fmt(d.drawdown.trough_level) + " m CD"],
        ["Water left in front", d.drawdown.front_force.toFixed(0) + " kN/m"],
        ["Net seaward push", d.drawdown.net_force.toFixed(0) + " kN/m"],
        [null, null],
        ["Toe rock Dn50", d.toe_Dn50.toFixed(2) + " m (Tanimoto)"],
        ["Toe rock M50", (d.toe_M50 / 1000).toFixed(2) + " t"],
        ["Concrete", q.concrete_total_m3_per_m.toFixed(1) + " m3/m"],
        ["Backfill", q.backfill_m3_per_m.toFixed(1) + " m3/m"],
        ["Excavation", q.excavation_m3_per_m.toFixed(1) + " m3/m"]
      ];
    }
  },

  breakwater: {
    label: "Breakwater",
    note: "Rock by Van der Meer (Van Gent 2003 form), concrete units by their own formulae, crest by EurOtop, crown wall by Pedersen.",
    inputs: [
      { key: "Hm0", label: "Wave height Hm0", unit: "m", min: 0.5, max: 9, step: 0.1, value: 4.0 },
      { key: "Tp", label: "Peak period Tp", unit: "s", min: 4, max: 18, step: 0.1, value: 11.0 },
      { key: "depth", label: "Depth at toe", unit: "m", min: 2, max: 40, step: 0.5, value: 12.0 },
      { key: "cot", label: "Seaward slope 1 :", unit: "", min: 1.5, max: 4, step: 0.25, value: 2.0 },
      { key: "storm", label: "Storm duration", unit: "h", min: 1, max: 48, step: 1, value: 6 },
      { key: "damage", label: "Damage level S", unit: "", min: 2, max: 17, step: 1, value: 2 },
      { key: "use", label: "Tolerable overtopping", type: "select", value: "trained_staff",
        options: ["pedestrians_unaware", "pedestrians_aware", "harbour_quay_equipment",
                  "trained_staff", "vehicles_low_speed"] },
      { key: "armour", label: "Armour type", type: "select", value: "rock_two_layer_permeable",
        options: ["rock_two_layer_permeable", "rock_two_layer_impermeable",
                  "cubes_two_layer_random", "tetrapod", "accropode", "xbloc"] },
      { key: "bed", label: "Seabed material", type: "select",
        value: "medium_sand", options: ["silt", "very_fine_sand", "fine_sand", "medium_sand",
                  "coarse_sand", "fine_gravel", "coarse_gravel",
                  "rock_fill", "soft_clay", "stiff_clay"] },
      { key: "section", label: "Section", type: "select", value: "trunk",
        options: ["trunk", "head"] }
    ],
    run: function (v) {
      var c = P.conditionsFromPeak(v.Hm0, v.Tp, v.depth, v.storm * 3600);
      var trunk = P.designRubbleMound(c, {
        cot_alpha: v.cot, damage: v.damage, tolerable_use: v.use, armour: v.armour
      });
      var d = v.section === "head" ? P.roundhead(trunk) : trunk;
      d._trunk = trunk;
      d._swl = 0.0;
      d._bed = -v.depth;
      d._foundation = P.moundFoundation(d, v.depth, { bed: v.bed });
      d._crown = P.crownWall(d, 0.0);
      d.warnings = (d.warnings || []).concat(d._crown.warnings);
      d._scour = d._foundation.scour;
      d._bedMaterial = P.sediment(v.bed);
      return d;
    },
    draw: function (host, d, w, h) { D.drawBreakwater(host, d, d._swl, d._bed, w, h); },
    checks: function (d) {
      return [
        { name: "Regime", value: d.regime,
          target: d.concrete ? "concrete unit" : "Van der Meer, Van Gent form",
          ok: true, neutral: true },
        { name: "Overtopping", value: d.q_upper.toPrecision(3) + " l/s/m",
          target: "≤ " + P.TOLERABLE_DISCHARGE[d.governing_limit][0] + " l/s/m",
          eta: d.q_upper / P.TOLERABLE_DISCHARGE[d.governing_limit][0],
          ok: d.q_upper <= P.TOLERABLE_DISCHARGE[d.governing_limit][0] * 1.001 },
        d.concrete
          ? { name: "Unit mass", value: (d.M50 / 1000).toFixed(1) + " t",
              target: d.regime, ok: true, neutral: true }
          : { name: "Stone mass", value: (d.M50 / 1000).toFixed(1) + " t",
              target: "≤ 15 t, quarry limit", eta: d.M50 / 1000 / 15,
              ok: d.M50 / 1000 <= 15 },
        { name: "Depth at toe", value: "Hm0/h = " + (d.conditions.Hm0 / d.conditions.depth).toFixed(2),
          target: "≤ 0.60, the wave must reach the toe",
          eta: d.conditions.Hm0 / d.conditions.depth / 0.6,
          ok: d.conditions.Hm0 / d.conditions.depth <= 0.6 },
        { name: "Crown sliding", value: fos(d._crown.sliding_FoS), target: "FoS ≥ 1.20",
          eta: 1.2 / d._crown.sliding_FoS, ok: d._crown.sliding_FoS >= 1.2 },
        { name: "Crown overturning", value: fos(d._crown.overturning_FoS), target: "FoS ≥ 1.50",
          eta: 1.5 / d._crown.overturning_FoS, ok: d._crown.overturning_FoS >= 1.5 },
        { name: "Surf similarity", value: d.xi.toFixed(2), target: "ξ m-1,0",
          ok: true, neutral: true },
        { name: "Reflection", value: d._scour.reflection.toFixed(2),
          target: "Kr, Seelig and Ahrens", ok: true, neutral: true },
        { name: "Toe scour", value: d._scour.depth.toFixed(2) + " m",
          target: d._scour.mobility.regime || "screening",
          eta: d._scour.depth / d.Dn50, ok: d._scour.depth < d.Dn50,
          warn: d._scour.depth >= d.Dn50 },
        { name: "Blanket reach", value: d._foundation.bedding_extension.toFixed(1) + " m",
          target: "≥ 2 x scour depth",
          eta: 2 * d._scour.depth / d._foundation.bedding_extension,
          ok: d._foundation.bedding_extension >= 2 * d._scour.depth },
        { name: "Toe berm stone",
          value: (d._foundation.toe_M50 / 1000).toFixed(1) + " t",
          target: "filter grade", ok: true, neutral: true },
        { name: "Section", value: d.section || "trunk",
          target: d.kd_ratio
            ? "KD " + d.kd_ratio.toFixed(2) + " of trunk"
            : "reference section",
          ok: true, neutral: true }
      ];
    },
    report: function (d) {
      var rows = [
        ["Section", d.section || "trunk"],
        ["Armour Dn50", d.Dn50.toFixed(2) + " m"],
        ["Armour M50", (d.M50 / 1000).toFixed(1) + " t"],
        ["Stability relation", d.regime],
        ["Unit density", d.density.toFixed(0) + " kg/m3"],
        ["Layer thickness", d.layer.thickness.toFixed(2) + " m"],
        ["Stones per m2", d.layer.stones_per_m2.toFixed(2)],
        [null, null],
        ["Crest freeboard Rc", d.crest_freeboard.toFixed(2) + " m"],
        ["Rc / Hm0", (d.crest_freeboard / d.conditions.Hm0).toFixed(2)],
        ["Mean discharge", d.q_mean.toPrecision(3) + " l/s/m"],
        ["Upper bound", d.q_upper.toPrecision(3) + " l/s/m"],
        [null, null],
        ["Surf similarity", d.xi.toFixed(2)],
        ["Waves in storm", Math.round(d.conditions.wave_count)],
        [null, null],
        ["Seabed", d._bedMaterial.name],
        ["  bed regime", d._scour.mobility.regime || "cohesive"],
        ["  reflection Kr", d._scour.reflection.toFixed(2)],
        ["  toe scour", d._scour.depth.toFixed(2) + " m"],
        ["  at a vertical wall", d._scour.unlimited_depth.toFixed(2) + " m"],
        ["  apron width", d._scour.apron_width.toFixed(1) + " m"],
        [null, null],
        ["Bedding blanket", d._foundation.bedding.name],
        ["  thickness", d._foundation.bedding_thickness.toFixed(2) + " m"],
        ["  reach past toe", d._foundation.bedding_extension.toFixed(1) + " m"],
        ["Toe berm Dn50", d._foundation.toe_Dn50.toFixed(2) + " m"],
        ["  M50", (d._foundation.toe_M50 / 1000).toFixed(1) + " t"],
        ["  width x thickness", d._foundation.toe_width.toFixed(1) + " x "
          + d._foundation.toe_thickness.toFixed(2) + " m"],
        [null, null],
        ["Crown parapet", fmt(d._crown.parapet_top) + " m CD"],
        ["Crown deck", fmt(d._crown.deck_level) + " m CD"],
        ["Crown founded at", fmt(d._crown.base_level) + " m CD"],
        ["Crown concrete", d._crown.concrete_m3_per_m.toFixed(1) + " m3/m"],
        ["  armour berm in front", d._crown.berm_width.toFixed(1) + " m"],
        ["  deck width", d._crown.deck_width.toFixed(2) + " m"],
        ["  Pedersen Fh", d._crown.loads.Fh.toFixed(0) + " kN/m"],
        ["  uplift pb", d._crown.loads.pb.toFixed(1) + " kPa"],
        ["  run-up Ru,0.1%", d._crown.loads.Ru.toFixed(2) + " m"]
      ];
      if (d.section === "head") {
        rows.splice(3, 0,
          ["  trunk M50", (d._trunk.M50 / 1000).toFixed(1) + " t"],
          ["  head / trunk", (d.M50 / d._trunk.M50).toFixed(2) + " x"],
          ["  KD ratio", d.kd_ratio.toFixed(2)]);
      }
      return rows;
    }
  },

  channel: {
    label: "Channel",
    note: "PIANC depth chain and width build-up.",
    inputs: [
      { key: "length", label: "Vessel length", unit: "m", min: 80, max: 400, step: 5, value: 336 },
      { key: "beam", label: "Beam", unit: "m", min: 12, max: 62, step: 0.5, value: 48.2 },
      { key: "draught", label: "Draught", unit: "m", min: 3, max: 20, step: 0.1, value: 14.5 },
      { key: "cb", label: "Block coefficient", unit: "", min: 0.5, max: 0.9, step: 0.01, value: 0.68 },
      { key: "speed", label: "Speed", unit: "kn", min: 3, max: 14, step: 0.5, value: 8 },
      { key: "wl", label: "Design water level", unit: "m CD", min: -1, max: 4, step: 0.1, value: 1.2 },
      { key: "Hs", label: "Wave height in channel", unit: "m", min: 0, max: 4, step: 0.1, value: 1.8 },
      { key: "factor", label: "Wave response factor", unit: "", min: 0.2, max: 0.8, step: 0.05, value: 0.5 },
      { key: "net", label: "Net clearance", unit: "m", min: 0.3, max: 2, step: 0.1, value: 0.8 },
      { key: "bed", label: "Existing bed", unit: "m CD", min: -25, max: -5, step: 0.5, value: -11.5 },
      { key: "twoway", label: "Two-way traffic", type: "toggle", value: true },
      { key: "material", label: "Bed material", type: "select",
        value: "medium_sand", options: ["silt", "very_fine_sand", "fine_sand", "medium_sand",
                  "coarse_sand", "fine_gravel", "coarse_gravel",
                  "rock_fill", "soft_clay", "stiff_clay"] }
    ],
    run: function (v) {
      var vessel = P.makeVessel("Design vessel", v.length, v.beam, v.draught, v.cb);
      return P.designChannel(vessel, v.speed, v.wl, {
        Hs: v.Hs, Tp: 9.0, wave_factor: v.factor, net_clearance: v.net,
        existing_bed: v.bed, two_way: v.twoway, bed: v.material,
        conditions: { crosswind: "moderate", crosscurrent: "low",
                      waves: v.Hs > 1 ? "moderate" : "low",
                      depth_of_waterway: "shallow" }
      });
    },
    draw: function (host, d, w, h) { D.drawChannel(host, d, w, h, 8); },
    checks: function (d) {
      var ratio = d.required_depth / d.vessel.draught;
      return [
        { name: "Depth / draught", value: ratio.toFixed(2), target: "≥ 1.10",
          eta: 1.1 / ratio, ok: ratio >= 1.1 },
        { name: "Froude number", value: d.squat.froude.toFixed(2), target: "< 0.70",
          eta: d.squat.froude / 0.7, ok: d.squat.froude < 0.7 },
        { name: "Width", value: d.width_result.width_in_beams.toFixed(1) + " B",
          target: d.width_result.lanes + "-way", ok: true, neutral: true },
        { name: "Assumed classes", value: String(d.width_result.assumed.length),
          target: "stated below", ok: d.width_result.assumed.length === 0,
          warn: d.width_result.assumed.length > 0 },
        { name: "Side slope", value: "1 : " + d.side_slope.toFixed(1),
          target: d.bed ? "from " + d.bed.name : "given", ok: true, neutral: true }
      ];
    },
    report: function (d) {
      var rows = [["Static draught", d.vessel.draught.toFixed(2) + " m"]];
      for (var k in d.clearance.components) {
        if (d.clearance.components[k] > 0) {
          rows.push(["  " + k, d.clearance.components[k].toFixed(2) + " m"]);
        }
      }
      rows.push(["Required depth", d.required_depth.toFixed(2) + " m"]);
      rows.push([null, null]);
      if (d.bed) {
        rows.push([null, null]);
        rows.push(["Bed material", d.bed.name]);
        rows.push(["  friction angle", d.bed.friction_angle.toFixed(0) + " deg"]);
        rows.push(["  side slope", "1 : " + d.side_slope.toFixed(1)]);
        rows.push([null, null]);
      }
      rows.push(["Dredge level", fmt(d.dredge_level) + " m CD"]);
      rows.push(["Bed width", Math.round(d.width) + " m"]);
      rows.push(["Top width", Math.round(d.top_width) + " m"]);
      if (d.existing_bed !== null) {
        rows.push(["Dredge depth", Math.max(d.existing_bed - d.dredge_level, 0).toFixed(2) + " m"]);
        rows.push(["Volume", Math.round(d.volume_per_km / 1000).toLocaleString() + " k m3/km"]);
      }
      return rows;
    }
  },

  monopile: {
    label: "Monopile",
    note: "Morison loads on a stream function wave, swept through the cycle; scour under waves and current.",
    inputs: [
      { key: "diameter", label: "Pile diameter", unit: "m", min: 0.5, max: 12, step: 0.1, value: 8.0 },
      { key: "H", label: "Wave height H", unit: "m", min: 1, max: 20, step: 0.5, value: 12 },
      { key: "T", label: "Period T", unit: "s", min: 4, max: 20, step: 0.5, value: 13 },
      { key: "depth", label: "Water depth", unit: "m", min: 5, max: 60, step: 1, value: 30 },
      { key: "current", label: "Tidal current", unit: "m/s", min: 0, max: 2.5, step: 0.1, value: 1.0 },
      { key: "rough", label: "Marine growth", type: "toggle", value: true },
      { key: "bed", label: "Seabed material", type: "select",
        value: "medium_sand", options: ["silt", "very_fine_sand", "fine_sand", "medium_sand",
                  "coarse_sand", "fine_gravel", "coarse_gravel",
                  "rock_fill", "soft_clay", "stiff_clay"] }
    ],
    run: function (v) {
      return P.designMonopile(v.diameter, v.H, v.T, v.depth,
                              { rough: v.rough, phases: 121, points: 300,
                                bed: v.bed, current: v.current });
    },
    draw: function (host, r, w, h) { drawPile(host, r, w, h); },
    checks: function (r) {
      var d = r.load;
      return [
        { name: "Morison valid", value: "D/L = " + d.diffraction_ratio.toFixed(3),
          target: "< 0.20",
          eta: d.diffraction_ratio / 0.2, ok: d.diffraction_ratio < 0.2 },
        { name: "Not breaking", value: "H/h = " + (d.H / d.depth).toFixed(2),
          target: "< 0.78",
          eta: d.H / d.depth / 0.78, ok: d.H / d.depth < 0.78 },
        { name: "Wave theory", value: d.theory,
          target: d.theory === "linear" ? "fallback at breaking" : "Fenton (1988)",
          ok: d.theory !== "linear", warn: d.theory === "linear" },
        { name: "Regime", value: d.regime, target: "KC = " + d.KC.toFixed(1),
          ok: true, neutral: true },
        { name: "Crest phase", value: (100 * r.crest_underestimate).toFixed(0) + "% low",
          target: "≤ 2%, else sweep the phase",
          eta: r.crest_underestimate / 0.02, ok: r.crest_underestimate <= 0.02,
          warn: r.crest_underestimate > 0.02 },
        { name: "Bed regime",
          value: (r.scour.mobility && r.scour.mobility.regime) || "not set",
          target: "gates the scour", ok: true, neutral: true },
        { name: "Scour", value: r.scour.depth.toFixed(2) + " m (Ucw " + r.scour.current_ratio.toFixed(2) + ")",
          target: "< 0.5 D (" + (r.scour.ratio).toFixed(2) + " D)",
          eta: r.scour.depth / (0.5 * d.diameter), ok: r.scour.depth < 0.5 * d.diameter,
          warn: r.scour.depth >= 0.5 * d.diameter }
      ];
    },
    report: function (r) {
      var d = r.load;
      return [
        ["Wave theory", d.theory],
        ["Surface at worst phase", (d.eta >= 0 ? "+" : "") + d.eta.toFixed(2) + " m"],
        ["Keulegan-Carpenter", d.KC.toFixed(1) + " at the surface"],
        ["Regime", d.regime],
        ["Cd, Cm", d.Cd.toFixed(2) + ", " + d.Cm.toFixed(2)],
        [null, null],
        ["Worst phase", (d.phase * 180 / Math.PI).toFixed(0) + " deg"],
        ["Base shear", (d.force / 1e3).toFixed(0) + " kN"],
        ["Mudline moment", (d.moment / 1e6).toFixed(1) + " MNm"],
        ["Lever arm", d.arm.toFixed(2) + " m"],
        ["Inertia share", (100 * d.inertia_fraction).toFixed(0) + "%"],
        [null, null],
        ["At the crest", (r.crest_load.moment / 1e6).toFixed(1) + " MNm"],
        ["Crest understates by", (100 * r.crest_underestimate).toFixed(0) + "%"],
        [null, null],
        ["Scour", r.scour.depth.toFixed(2) + " m"],
        ["Scour / D", r.scour.ratio.toFixed(2)],
        ["  Hs for scour", r.scour.Hs.toFixed(2) + " m (H / 1.86)"],
        ["  bed velocity Um", r.scour.Um.toFixed(2) + " m/s"],
        ["  KC at the bed", r.scour.KC.toFixed(2)],
        ["  Ucw", r.scour.current_ratio.toFixed(2)],
        ["Bed regime", (r.scour.mobility && r.scour.mobility.regime) || "not set"],
        ["Mobility", (r.scour.mobility && isFinite(r.scour.mobility.mobility))
          ? r.scour.mobility.mobility.toFixed(1) + " x threshold" : "n/a"]
      ];
    }
  },

  nourishment: {
    label: "Nourishment",
    note: "What a borrow source is worth, on Dean's equilibrium profile.",
    inputs: [
      { key: "native", label: "Native beach sand", type: "select",
        value: "medium_sand", options: ["silt", "very_fine_sand", "fine_sand", "medium_sand",
                  "coarse_sand", "fine_gravel", "coarse_gravel"] },
      { key: "borrow", label: "Borrow source", type: "select",
        value: "coarse_sand", options: ["silt", "very_fine_sand", "fine_sand", "medium_sand",
                  "coarse_sand", "fine_gravel", "coarse_gravel"] },
      { key: "volume", label: "Placed volume", unit: "m3/m", min: 20, max: 1200, step: 10, value: 250 },
      { key: "berm", label: "Berm height", unit: "m", min: 0.5, max: 5, step: 0.1, value: 2.0 },
      { key: "closure", label: "Depth of closure", unit: "m", min: 2, max: 14, step: 0.5, value: 6.0 },
      { key: "view", label: "View", type: "select", value: "profile",
        options: ["profile", "planform"] },
      { key: "length", label: "Fill length (planform)", unit: "m",
        min: 200, max: 6000, step: 50, value: 1500 },
      { key: "Hb", label: "Breaking wave height (planform)", unit: "m",
        min: 0.3, max: 3.0, step: 0.1, value: 1.2 }
    ],
    run: function (v) {
      var An = P.deanScale(v.native);
      var Af = P.deanScale(v.borrow);
      var r = P.shorelineAdvance(An, Af, v.volume, v.berm, v.closure);
      r.A_native = An;
      r.A_fill = Af;
      r.berm_height = v.berm;
      r.closure_depth = v.closure;
      r.native_name = P.sediment(v.native).name;
      r.borrow_name = P.sediment(v.borrow).name;
      r.borrow_d50 = P.sediment(v.borrow).d50;
      r.match = P.grainCompatibility(v.native, v.borrow);
      r.overfill = P.profileOverfillFactor(v.native, v.borrow, v.berm,
                                           v.closure, Math.max(r.advance, 1));

      // The plan is the same design seen from above. It needs a width to
      // spread, so a fill that produced no dry beach gets no planform.
      r.view = v.view;
      r.plan_length = v.length;
      r.plan_width = r.advance;
      if (r.advance > 0) {
        var fill = P.makeFill(v.length, r.advance, 0.1 * v.length,
                              v.closure, v.berm);
        var climate = P.makeClimate(v.Hb, 8.0, 0.0);
        r.plan = P.planformEvolution(fill, climate);
      }
      return r;
    },
    draw: function (host, r, w, h) {
      if (r.view === "planform" && r.plan) D.drawNourishmentPlan(host, r, w, h);
      else D.drawNourishment(host, r, w, h);
    },
    checks: function (r) {
      return [
        { name: "Dry beach", value: r.advance.toFixed(1) + " m",
          target: r.volume.toFixed(0) + " m3/m placed",
          ok: r.advance > 0, warn: r.advance === 0 },
        { name: "Profile", value: r.kind,
          target: r.kind === "submerged" ? "no dry beach" : "Dean (1991)",
          ok: r.kind !== "submerged", neutral: r.kind !== "submerged" },
        { name: "Overfill factor", value: r.overfill.factor.toFixed(2),
          target: "≤ 1.05 x native volume",
          eta: r.overfill.factor / 1.05, ok: r.overfill.factor <= 1.05, warn: r.overfill.factor > 1.05 },
        { name: "Grain match",
          value: (r.match.delta >= 0 ? "+" : "") + r.match.delta.toFixed(2),
          target: "native sigma-phi",
          ok: r.match.coarser, warn: !r.match.coarser },
        { name: "Critical volume",
          value: r.critical_volume > 0 ? r.critical_volume.toFixed(0) + " m3/m" : "none",
          target: "for any dry beach",
          ok: r.critical_volume === 0, warn: r.critical_volume > 0 },
        { name: "Spreading half-life",
          value: r.plan ? r.plan.half_life.toFixed(2) + " yr" : "n/a",
          target: "half the width lost",
          ok: !!(r.plan && r.plan.half_life >= 2.0),
          warn: !!(r.plan && r.plan.half_life < 2.0) }
      ];
    },
    report: function (r) {
      return [
        ["Native", r.native_name],
        ["  phi", r.match.phi_native.toFixed(2)],
        ["  A native", r.A_native.toFixed(3)],
        ["Borrow", r.borrow_name],
        ["  phi", r.match.phi_borrow.toFixed(2)],
        ["  A borrow", r.A_fill.toFixed(3)],
        [null, null],
        ["Planform", r.plan ? "" : "no dry beach to spread"],
        ["  diffusivity", r.plan
          ? (r.plan.diffusivity * P.SECONDS_PER_YEAR / 1e3).toFixed(0)
            + " thousand m2/yr" : "n/a"],
        ["  half-life", r.plan ? r.plan.half_life.toFixed(2) + " yr" : "n/a"],
        ["  width left", r.plan
          ? (100 * r.plan.retained).toFixed(0) + "% at "
            + r.plan.years[r.plan.years.length - 1] + " yr" : "n/a"],
        ["  spread to", r.plan ? r.plan.spread.toFixed(0) + " m" : "n/a"],
        [null, null],
        ["Compatibility", r.match.coarser ? "coarser" : "finer"],
        ["  delta", (r.match.delta >= 0 ? "+" : "") + r.match.delta.toFixed(2)],
        ["  sorting ratio", r.match.sorting_ratio.toFixed(2)],
        ["  verdict", r.match.verdict.split(",")[0]],
        [null, null],
        ["Placed volume", r.volume.toFixed(0) + " m3/m"],
        ["Dry beach gained", r.advance.toFixed(1) + " m"],
        ["Profile type", r.kind],
        ["Critical volume", r.critical_volume.toFixed(0) + " m3/m"],
        [null, null],
        ["For the same width", ""],
        ["  with this borrow", r.overfill.borrow_volume.toFixed(0) + " m3/m"],
        ["  with native sand", r.overfill.native_volume.toFixed(0) + " m3/m"],
        ["  overfill factor", r.overfill.factor.toFixed(2)]
      ];
    }
  },

  extremes: {
    label: "Return values",
    note: "Generalised Pareto tail above a storm threshold.",
    inputs: [
      { key: "threshold", label: "Threshold", unit: "m", min: 0.5, max: 8, step: 0.1, value: 2.5 },
      { key: "scale", label: "Scale", unit: "m", min: 0.1, max: 3, step: 0.05, value: 0.55 },
      { key: "shape", label: "Shape", unit: "", min: -0.4, max: 0.4, step: 0.01, value: -0.08 },
      { key: "rate", label: "Peaks per year", unit: "", min: 0.5, max: 30, step: 0.5, value: 6 },
      { key: "record", label: "Record length", unit: "yr", min: 5, max: 100, step: 1, value: 40 },
      { key: "period", label: "Design return period", unit: "yr", min: 5, max: 500, step: 5, value: 100 }
    ],
    run: function (v) {
      var periods = [], values = [];
      for (var i = 0; i <= 120; i++) {
        var T = Math.pow(10, -0.7 + (Math.log10(500) + 0.7) * i / 120);
        periods.push(T);
        values.push(P.gpdReturnValue(v.threshold, v.scale, v.shape, v.rate, T));
      }
      return {
        input: v, periods: periods, values: values,
        design: P.gpdReturnValue(v.threshold, v.scale, v.shape, v.rate, v.period),
        ceiling: v.shape < 0 ? v.threshold - v.scale / v.shape : null
      };
    },
    draw: function (host, r, w, h) { drawReturnCurve(host, r, w, h); },
    checks: function (r) {
      var v = r.input;
      var reach = v.period / v.record;
      return [
        { name: "Extrapolation", value: reach.toFixed(1) + "x record",
          target: "≤ 3x", eta: reach / 3, ok: reach <= 3, warn: reach > 3 },
        { name: "Tail", value: v.shape >= 0 ? "unbounded" : "bounded",
          target: "shape " + (v.shape >= 0 ? "≥ 0" : "< 0"), ok: true, neutral: true },
        { name: "Peaks in record", value: Math.round(v.rate * v.record) + "",
          target: "≥ 30",
          eta: 30 / (v.rate * v.record), ok: v.rate * v.record >= 30 },
        { name: "Rate", value: v.rate.toFixed(1) + "/yr", target: "≥ 1/yr",
          eta: 1 / v.rate, ok: v.rate >= 1 }
      ];
    },
    report: function (r) {
      var v = r.input;
      var rows = [
        ["Threshold u", v.threshold.toFixed(2) + " m"],
        ["Scale", v.scale.toFixed(3) + " m"],
        ["Shape", (v.shape >= 0 ? "+" : "") + v.shape.toFixed(3)],
        ["Peak rate", v.rate.toFixed(1) + " /yr"],
        [null, null]
      ];
      [10, 50, 100, 200].forEach(function (T) {
        rows.push([T + "-year value",
                   P.gpdReturnValue(v.threshold, v.scale, v.shape, v.rate, T).toFixed(2) + " m"]);
      });
      rows.push([null, null]);
      rows.push(["Design " + v.period + "-year", r.design.toFixed(2) + " m"]);
      if (r.ceiling !== null) {
        rows.push(["Upper limit of tail", r.ceiling.toFixed(2) + " m"]);
      }
      return rows;
    }
  }
};

/* ------------------------------------------------------------------ */
/* Charts for the two modules whose answer is a curve                  */
/* ------------------------------------------------------------------ */

function drawPile(host, r, w, h) {
  var svg = D.newSheet(host, w, h);
  var d = r.load, sweep = r.sweep;
  var gap = 26;
  var left = { x: 56, y: 26, w: (w - 150) * 0.42, h: h - 96 };
  var right = { x: left.x + left.w + 84, y: 26, w: w - left.x - left.w - 120, h: h - 96 };

  // Load profile at the worst phase.
  var gl = D.chartFrame(svg, left, "load (kN/m)", "elevation (m)");
  var wet = [], zs = [], tot = [], ine = [];
  for (var i = 0; i < d.z.length; i++) {
    if (d.z[i] <= d.eta) { zs.push(d.z[i]); tot.push(d.total[i] / 1e3); ine.push(d.inertia[i] / 1e3); }
  }
  var maxLoad = Math.max.apply(null, tot.map(Math.abs));
  var xlim = [Math.min(0, -maxLoad * 0.05), Math.max(maxLoad * 1.1, 1)];
  // Headroom above the surface, so the free-surface line is not welded to
  // the top of the frame.
  var top = Math.max(d.eta, 1);
  var zlim = [-d.depth, top + 0.12 * (top + d.depth)];
  D.axis(gl, left, xlim[0], xlim[1], true, function (v) { return v.toFixed(0); });
  D.axis(gl, left, zlim[0], zlim[1], false, function (v) { return v.toFixed(0); });

  // The band between the load curve and zero. Trace the curve, then come
  // back along the zero line at the same elevations, so the polygon closes
  // on itself instead of sweeping the whole panel.
  var zeroX = left.x + left.w * (0 - xlim[0]) / (xlim[1] - xlim[0]);
  function py(z) {
    return left.y + left.h * (1 - (z - zlim[0]) / (zlim[1] - zlim[0]));
  }
  var areaPts = "";
  for (i = 0; i < zs.length; i++) {
    var px = left.x + left.w * (tot[i] - xlim[0]) / (xlim[1] - xlim[0]);
    areaPts += (i ? "L" : "M") + px.toFixed(1) + "," + py(zs[i]).toFixed(1);
  }
  for (i = zs.length - 1; i >= 0; i--) {
    areaPts += "L" + zeroX.toFixed(1) + "," + py(zs[i]).toFixed(1);
  }
  areaPts += " Z";
  D.el("path", { d: areaPts, fill: "#9fc4d6", opacity: 0.55, stroke: "none" }, gl);
  D.polyline(gl, left, tot, zs, xlim, zlim, { stroke: "#0b3554", width: 2 });

  var etaY = py(d.eta);
  D.el("path", { d: "M" + left.x + "," + etaY + " H" + (left.x + left.w),
                 stroke: "#8a2f24", "stroke-width": 1.2, "stroke-dasharray": "5 3" }, gl);
  label(gl, left.x + 6, etaY - 5, "surface " + fmt(d.eta) + " m", "#8a2f24");
  title(svg, left.x, 18, "Load at the worst phase, " +
        (d.phase * 180 / Math.PI).toFixed(0) + " deg");

  // Moment through the cycle.
  var gr = D.chartFrame(svg, right, "wave phase (deg, crest at 0)", "mudline moment (MNm)");
  var deg = sweep.phase.map(function (p) { return p * 180 / Math.PI; });
  var mom = sweep.moment.map(function (m) { return m / 1e6; });
  var mmax = Math.max.apply(null, mom.map(Math.abs)) * 1.15;
  D.axis(gr, right, 0, 360, true, function (v) { return v.toFixed(0); });
  D.axis(gr, right, -mmax, mmax, false, function (v) { return v.toFixed(0); });
  var zeroY = right.y + right.h * 0.5;
  D.el("path", { d: "M" + right.x + "," + zeroY + " H" + (right.x + right.w),
                 stroke: "#c9c7c0", "stroke-width": 1 }, gr);
  D.polyline(gr, right, deg, mom, [0, 360], [-mmax, mmax], { stroke: "#8a2f24", width: 2 });

  function mark(phaseDeg, value, fill, text) {
    var px = right.x + right.w * phaseDeg / 360;
    var py = right.y + right.h * (1 - (value + mmax) / (2 * mmax));
    D.el("circle", { cx: px, cy: py, r: 5, fill: fill, stroke: "#16181a",
                     "stroke-width": 1 }, gr);
    label(gr, px + 9, py - 6, text, "#16181a");
  }
  mark(0, r.crest_load.moment / 1e6, "#ffffff",
       "crest " + (r.crest_load.moment / 1e6).toFixed(0));
  mark(sweep.phase_of_max_moment * 180 / Math.PI, d.moment / 1e6, "#c47f1a",
       "worst " + (d.moment / 1e6).toFixed(0) + " MNm");
  title(svg, right.x, 18, "Moment through the wave cycle");

  D.sheetFrame(svg, w, h, {
    bubble: "B", title: "Monopile wave loads",
    scale: d.regime + ", " + (100 * d.inertia_fraction).toFixed(0) + "% inertia"
  });
}

function drawReturnCurve(host, r, w, h) {
  var svg = D.newSheet(host, w, h);
  var box = { x: 66, y: 30, w: w - 110, h: h - 100 };
  var g = D.chartFrame(svg, box, "return period (years)", "value (m)");
  var v = r.input;
  var lx = r.periods.map(function (T) { return Math.log10(T); });
  var xlim = [lx[0], lx[lx.length - 1]];
  var lo = Math.min.apply(null, r.values);
  var hi = Math.max.apply(null, r.values);
  var ylim = [lo - 0.1 * (hi - lo), hi + 0.15 * (hi - lo)];

  D.axis(g, box, xlim[0], xlim[1], true, function (u) {
    var T = Math.pow(10, u);
    return T < 1 ? T.toFixed(1) : String(Math.round(T));
  });
  D.axis(g, box, ylim[0], ylim[1], false, function (u) { return u.toFixed(1); });

  if (r.ceiling !== null && r.ceiling < ylim[1]) {
    var cy = box.y + box.h * (1 - (r.ceiling - ylim[0]) / (ylim[1] - ylim[0]));
    D.el("path", { d: "M" + box.x + "," + cy + " H" + (box.x + box.w),
                   stroke: "#a8641a", "stroke-width": 1.2,
                   "stroke-dasharray": "6 4" }, g);
    label(g, box.x + 8, cy - 6,
          "tail cannot exceed " + r.ceiling.toFixed(2) + " m", "#a8641a");
  }

  var rx = box.x + box.w * (Math.log10(v.record) - xlim[0]) / (xlim[1] - xlim[0]);
  D.el("path", { d: "M" + rx + "," + box.y + " V" + (box.y + box.h),
                 stroke: "#54514b", "stroke-width": 1, "stroke-dasharray": "3 3" }, g);
  label(g, rx + 6, box.y + 14, v.record + "-year record", "#54514b");
  D.el("rect", { x: rx, y: box.y, width: box.x + box.w - rx, height: box.h,
                 fill: "#8a2f24", opacity: 0.05 }, g);

  D.polyline(g, box, lx, r.values, xlim, ylim, { stroke: "#0b3554", width: 2.2 });

  var dx = box.x + box.w * (Math.log10(v.period) - xlim[0]) / (xlim[1] - xlim[0]);
  var dy = box.y + box.h * (1 - (r.design - ylim[0]) / (ylim[1] - ylim[0]));
  D.el("circle", { cx: dx, cy: dy, r: 6, fill: "#c47f1a", stroke: "#16181a",
                   "stroke-width": 1.2 }, g);
  label(g, dx + 10, dy - 8, v.period + "-year: " + r.design.toFixed(2) + " m", "#16181a", 700);

  title(svg, box.x, 20, "Return level, generalised Pareto tail");
  D.sheetFrame(svg, w, h, {
    bubble: "C", title: "Design return value",
    scale: "shaded region is beyond the record"
  });
}

function label(g, x, y, text, fill, weight) {
  var t = D.el("text", {
    x: x, y: y, "font-size": 10, fill: fill || "#16181a",
    "font-weight": weight || 400,
    "font-family": "'IBM Plex Mono', ui-monospace, monospace"
  }, g);
  t.textContent = T(text);
  return t;
}

function title(svg, x, y, text) {
  var t = D.el("text", {
    x: x, y: y, "font-size": 11, fill: "#16181a", "font-weight": 700,
    "letter-spacing": "0.03em",
    "font-family": "'Archivo', system-ui, sans-serif"
  }, svg);
  t.textContent = T(text).toUpperCase();
  return t;
}

function fmt(v) { return (v >= 0 ? "+" : "") + v.toFixed(2); }

/* A factor of safety can genuinely be infinite: the case cannot drive the
   wall at all. Saying so beats printing a made-up large number. */
function fos(v) { return isFinite(v) ? v.toFixed(2) : "no demand"; }

/* ------------------------------------------------------------------ */
/* Rendering                                                           */
/* ------------------------------------------------------------------ */

function values(module) {
  var out = {};
  MODULES[module].inputs.forEach(function (input) {
    out[input.key] = input.value;
  });
  return out;
}

function renderInputs() {
  var host = document.getElementById("inputs");
  host.innerHTML = "";
  var module = MODULES[STATE.module];
  module.inputs.forEach(function (input) {
    var row = document.createElement("div");
    row.className = "field";

    var lab = document.createElement("label");
    lab.className = "field-label";
    lab.setAttribute("for", "in-" + input.key);
    lab.textContent = T(input.label);
    row.appendChild(lab);

    if (input.type === "select") {
      var sel = document.createElement("select");
      sel.id = "in-" + input.key;
      input.options.forEach(function (option) {
        var o = document.createElement("option");
        o.value = option;
        o.textContent = T(option.replace(/_/g, " "));
        if (option === input.value) o.selected = true;
        sel.appendChild(o);
      });
      sel.addEventListener("change", function () {
        input.value = sel.value;
        run();
      });
      row.appendChild(sel);
    } else if (input.type === "toggle") {
      var wrap = document.createElement("div");
      wrap.className = "toggle";
      var btn = document.createElement("button");
      btn.id = "in-" + input.key;
      btn.type = "button";
      btn.className = "toggle-btn" + (input.value ? " on" : "");
      btn.setAttribute("aria-pressed", String(!!input.value));
      btn.textContent = T(input.value ? "Yes" : "No");
      btn.addEventListener("click", function () {
        input.value = !input.value;
        btn.className = "toggle-btn" + (input.value ? " on" : "");
        btn.setAttribute("aria-pressed", String(!!input.value));
        btn.textContent = T(input.value ? "Yes" : "No");
        run();
      });
      wrap.appendChild(btn);
      row.appendChild(wrap);
    } else {
      var line = document.createElement("div");
      line.className = "slider-row";
      var range = document.createElement("input");
      range.type = "range";
      range.id = "in-" + input.key;
      range.min = input.min; range.max = input.max;
      range.step = input.step; range.value = input.value;
      var out = document.createElement("output");
      out.className = "readout";
      out.textContent = format(input.value) + (input.unit ? " " + input.unit : "");
      range.addEventListener("input", function () {
        input.value = parseFloat(range.value);
        out.textContent = format(input.value) + (input.unit ? " " + input.unit : "");
        run();
      });
      line.appendChild(range);
      line.appendChild(out);
      row.appendChild(line);
    }
    host.appendChild(row);
  });
}

function format(v) {
  if (typeof v !== "number") return String(v);
  return Math.abs(v) >= 100 ? v.toFixed(0) : v.toFixed(Math.abs(v) < 1 ? 2 : 1);
}

function run() {
  var module = MODULES[STATE.module];
  var host = document.getElementById("sheet");
  var errorHost = document.getElementById("error");
  var v = values(STATE.module);

  // Everything, including the drawing, is inside the guard. A drawing that
  // throws used to leave the sheet blank with nothing on screen to say why,
  // which is indistinguishable from a page that simply has no drawing.
  try {
    var result = module.run(v);
    module.draw(host, result, 980, 560);
    if (!host.firstChild) throw new Error("the drawing produced no output");
    renderChecks(module.checks(result));
    renderReport(module.report(result));
    renderWarnings(result);
    errorHost.hidden = true;
  } catch (err) {
    errorHost.hidden = false;
    errorHost.textContent = T("Could not draw this section") + ": " +
      String(err && err.message ? err.message : err);
    host.innerHTML = "";
    document.getElementById("checks").innerHTML = "";
    document.getElementById("report").innerHTML = "";
  }
}

function renderChecks(checks) {
  var host = document.getElementById("checks");
  host.innerHTML = "";
  var table = document.createElement("table");
  table.className = "check-table";
  var head = table.createTHead().insertRow();
  ["Check", "Result", "Criterion", "η", ""].forEach(function (text, i) {
    var th = document.createElement("th");
    th.textContent = T(text);
    if (i === 3) th.title = T("Utilization, demand over capacity");
    head.appendChild(th);
  });
  var body = table.createTBody();
  checks.forEach(function (check) {
    var tone = check.neutral ? "neutral" : (check.ok ? "pass" : (check.warn ? "warn" : "fail"));
    var row = body.insertRow();
    row.className = "check-" + tone;
    var eta = check.eta;
    var cells = [
      check.name,
      check.value,
      check.target,
      eta == null ? "" : (isFinite(eta) ? eta.toFixed(2) : "–"),
      { pass: "OK", warn: "Review", fail: "Fails", neutral: "" }[tone]
    ];
    cells.forEach(function (text, i) {
      var td = row.insertCell();
      td.textContent = T(text);
      if (i === 1 || i === 3) td.className = "num";
      if (i === 4) td.className = "status";
    });
  });
  host.appendChild(table);
}

function renderReport(rows) {
  var host = document.getElementById("report");
  host.innerHTML = "";
  rows.forEach(function (row) {
    if (row[0] === null) {
      host.appendChild(document.createElement("hr"));
      return;
    }
    var line = document.createElement("div");
    line.className = "report-row";
    var k = document.createElement("span");
    k.textContent = T(row[0]);
    var val = document.createElement("span");
    val.className = "report-value";
    val.textContent = T(row[1]);
    line.appendChild(k);
    line.appendChild(val);
    host.appendChild(line);
  });
}

function renderWarnings(result) {
  var host = document.getElementById("warnings");
  host.innerHTML = "";
  var list = (result.warnings || (result.load && result.load.warnings) || []);
  if (!list.length && result.note) list = [result.note];
  if (!list.length) { host.hidden = true; return; }
  host.hidden = false;
  list.forEach(function (text) {
    var item = document.createElement("p");
    item.className = "warning";
    item.textContent = T(text);
    host.appendChild(item);
  });
}

/* ------------------------------------------------------------------ */
/* Literature                                                          */
/* ------------------------------------------------------------------ */

var SECTION_ORDER = [
  ["validated_ranges", "Validated ranges"],
  ["well_established", "Well established"],
  ["governing_physics", "Governing physics"],
  ["major_equations", "Major equations"],
  ["dimensionless_parameters", "Dimensionless parameters"],
  ["typical_methods", "Typical methods"],
  ["limitations", "Limitations"],
  ["disagreements", "Disagreements"],
  ["open_questions", "Open questions"],
  ["recent_advances", "Recent advances"],
  ["numerical_models", "Numerical models"],
  ["experimental_datasets", "Experimental datasets"],
  ["seminal_papers", "Seminal papers"]
];

var MODULE_TO_KEY = {
  seawall: "seawall", breakwater: "structures", channel: "channel",
  monopile: "piles", extremes: "extremes", nourishment: "nourishment"
};

function renderTopics() {
  var host = document.getElementById("topics");
  host.innerHTML = "";
  if (!STATE.knowledge) return;
  var key = MODULE_TO_KEY[STATE.module];
  var entry = STATE.knowledge.modules[key];
  if (!entry) return;
  var available = entry.topics.filter(function (t) { return STATE.knowledge.topics[t]; });
  if (!available.length) return;
  if (available.indexOf(STATE.topic) === -1) STATE.topic = available[0];

  available.forEach(function (tid) {
    var topic = STATE.knowledge.topics[tid];
    var tab = document.createElement("button");
    tab.type = "button";
    tab.className = "topic-tab" + (tid === STATE.topic ? " active" : "");
    tab.setAttribute("aria-pressed", String(tid === STATE.topic));
    var name = document.createElement("span");
    name.textContent = topic.label;
    var count = document.createElement("span");
    count.className = "topic-count";
    count.textContent = topic.papers;
    tab.appendChild(name);
    tab.appendChild(count);
    tab.addEventListener("click", function () {
      STATE.topic = tid;
      renderTopics();
      renderKnowledge();
    });
    host.appendChild(tab);
  });
}

function renderKnowledge() {
  var host = document.getElementById("knowledge");
  host.innerHTML = "";
  if (!STATE.knowledge || !STATE.topic) return;
  var topic = STATE.knowledge.topics[STATE.topic];
  if (!topic) return;

  var head = document.createElement("div");
  head.className = "k-head";
  var h = document.createElement("h3");
  h.textContent = topic.label;
  var meta = document.createElement("p");
  meta.className = "k-meta";
  meta.textContent = T(topic.papers + " papers · " + topic.claims.length +
    " claims · " + topic.equations.length + " equations");
  head.appendChild(h);
  head.appendChild(meta);
  if (topic.description) {
    var desc = document.createElement("p");
    desc.className = "k-desc";
    desc.textContent = topic.description;
    head.appendChild(desc);
  }
  host.appendChild(head);

  SECTION_ORDER.forEach(function (pair) {
    var text = topic.synthesis[pair[0]];
    if (!text) return;
    var block = document.createElement("details");
    block.className = "k-section";
    if (pair[0] === "validated_ranges" || pair[0] === "limitations") block.open = true;
    var summary = document.createElement("summary");
    summary.textContent = T(pair[1]);
    var body = document.createElement("p");
    body.textContent = text;
    block.appendChild(summary);
    block.appendChild(body);
    host.appendChild(block);
  });

  if (topic.equations.length) {
    var eqWrap = document.createElement("details");
    eqWrap.className = "k-section";
    var eqSum = document.createElement("summary");
    eqSum.textContent = T("Equations (" + topic.equations.length + ")");
    eqWrap.appendChild(eqSum);
    topic.equations.forEach(function (eq) {
      var card = document.createElement("div");
      card.className = "eq";
      var name = document.createElement("div");
      name.className = "eq-name";
      name.textContent = eq.name;
      var code = document.createElement("code");
      code.className = "eq-latex";
      code.textContent = eq.latex;
      card.appendChild(name);
      card.appendChild(code);
      if (eq.regime) {
        var regime = document.createElement("p");
        regime.className = "regime";
        regime.textContent = eq.regime;
        card.appendChild(regime);
      }
      card.appendChild(citation(eq.paper));
      eqWrap.appendChild(card);
    });
    host.appendChild(eqWrap);
  }

  if (topic.claims.length) {
    var clWrap = document.createElement("details");
    clWrap.className = "k-section";
    clWrap.open = true;
    var clSum = document.createElement("summary");
    clSum.textContent = T("Claims (" + topic.claims.length + ")");
    clWrap.appendChild(clSum);
    topic.claims.forEach(function (claim) {
      var card = document.createElement("div");
      card.className = "claim";
      var text = document.createElement("p");
      text.className = "claim-text";
      text.textContent = claim.text;
      card.appendChild(text);
      if (claim.regime) {
        var regime = document.createElement("p");
        regime.className = "regime";
        regime.textContent = T("Applies") + ": " + claim.regime;
        card.appendChild(regime);
      }
      card.appendChild(citation(claim.paper));
      clWrap.appendChild(card);
    });
    host.appendChild(clWrap);
  }
}

function citation(paperId) {
  var wrap = document.createElement("div");
  wrap.className = "cite";
  var paper = STATE.knowledge.papers[String(paperId)];
  if (!paper) {
    wrap.textContent = T("source not in the extract");
    return wrap;
  }
  var lead = (paper.a ? paper.a : "Anon") + (paper.y ? " (" + paper.y + ")" : "");
  var strong = document.createElement("span");
  strong.className = "cite-lead";
  strong.textContent = lead;
  wrap.appendChild(strong);
  var title = document.createElement("span");
  title.className = "cite-title";
  title.textContent = paper.t;
  wrap.appendChild(title);
  if (paper.j) {
    var journal = document.createElement("span");
    journal.className = "cite-journal";
    journal.textContent = paper.j;
    wrap.appendChild(journal);
  }
  if (paper.doi) {
    var link = document.createElement("a");
    link.className = "cite-doi";
    link.href = "https://doi.org/" + paper.doi;
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    link.textContent = paper.doi;
    wrap.appendChild(link);
  }
  if (paper.oa) {
    var open = document.createElement("a");
    open.className = "cite-doi";
    open.href = paper.oa;
    open.target = "_blank";
    open.rel = "noopener noreferrer";
    open.textContent = T("open copy");
    open.title = T({ vor: "published version", am: "accepted manuscript",
                     sm: "submitted manuscript", pp: "preprint" }[paper.v] || "open copy") +
                 ", " + T(paper.l);
    wrap.appendChild(open);
  }
  return wrap;
}

/* ------------------------------------------------------------------ */
/* The engine check, repeated in the browser                           */
/* ------------------------------------------------------------------ */

function runCase(spec) {
  var args = spec.args ? spec.args.slice() : [];
  if (spec.conditions) {
    var c = P.conditionsFromPeak(spec.conditions[0], spec.conditions[1],
                                 spec.conditions[2], spec.conditions[3]);
    if (spec.design_first) {
      args[0] = P.designRubbleMound(c, args[0]);
    } else {
      args.unshift(c);
    }
  }
  if (spec.fill) {
    args.unshift(P.makeClimate(spec.climate[0], spec.climate[1],
                               spec.climate[2]));
    args.unshift(P.makeFill(spec.fill[0], spec.fill[1], spec.fill[2],
                            spec.fill[3], spec.fill[4]));
  }
  if (spec.vessel) {
    args.unshift(P.makeVessel(spec.vessel[0], spec.vessel[1], spec.vessel[2],
                              spec.vessel[3], spec.vessel[4]));
  }
  var fn = P[spec.fn];
  if (!fn) throw new Error("no such function: " + spec.fn);
  var out = fn.apply(null, args);
  if (typeof out === "number" || typeof out === "boolean") return { value: out };
  return out;
}

/* Non-finite values travel as markers, because JSON has no way to write
   them and the reference file has to stay parseable. */
function finite(value) {
  if (typeof value !== "number") return value;
  if (value === Infinity) return "inf";
  if (value === -Infinity) return "-inf";
  if (value !== value) return "nan";
  return value;
}

function pluck(result, key) {
  if (result === null || result === undefined) return undefined;
  // The nested cases come first. `squat`, `scour` and `assumed` all name a
  // sub-object or an array on the result as well as the number the
  // reference case wants, and a generic lookup would hand back the wrong
  // one and report a false failure.
  if (key === "squat" && result.squat && typeof result.squat === "object") {
    return result.squat.squat;
  }
  if (key === "scour" && result.scour && typeof result.scour === "object") {
    return result.scour.depth;
  }
  if (key === "assumed" && result.assumed && result.assumed.length !== undefined) {
    return result.assumed.length;
  }
  if (key === "earth_total" && result.earth_driving) return result.earth_driving.total;
  if (key === "earth_arm" && result.earth_driving) return result.earth_driving.arm;
  if (key === "drawdown_sliding" && result.drawdown) return result.drawdown.sliding_FoS;
  if (key === "drawdown_net" && result.drawdown) return result.drawdown.net_force;
  if (key === "drawdown_overturning" && result.drawdown) return result.drawdown.overturning_FoS;
  if (key === "drawdown_p_max" && result.drawdown && result.drawdown.bearing) {
    return result.drawdown.bearing.p_max;
  }
  if (key === "bearing_p_max" && result.bearing) return result.bearing.p_max;
  if (key === "stem_moment" && result.stem) return result.stem.moment;
  if (key === "crown_Fh" && result.loads) return result.loads.Fh;
  if (key === "theory" && result.load) return result.load.theory;
  if (key in result) return result[key];
  if (key === "layer_thickness" && result.layer) return result.layer.thickness;
  if (key === "concrete" && result.quantities) return result.quantities.concrete_total_m3_per_m;
  if (result.sweep && (key === "max_moment" || key === "max_force" ||
                       key === "phase_of_max_moment")) return result.sweep[key];
  if (key === "l1") return result[0];
  if (key === "l2") return result[1];
  if (key === "l3") return result[2];
  if (key === "l4") return result[3];
  return undefined;
}

function verify(vectors) {
  var total = 0, failed = 0, firstFailure = null;
  vectors.cases.forEach(function (entry) {
    var got;
    try {
      got = runCase(entry.call);
    } catch (err) {
      Object.keys(entry.expect).forEach(function () { total++; failed++; });
      if (!firstFailure) firstFailure = entry.name + " raised " + err.message;
      return;
    }
    Object.keys(entry.expect).forEach(function (key) {
      total++;
      var expected = entry.expect[key];
      var actual = finite(pluck(got, key));
      var ok;
      if (typeof expected === "number") {
        ok = typeof actual === "number" &&
             Math.abs(expected - actual) <= Math.max(1e-12, 1e-9 * Math.abs(expected));
      } else {
        ok = expected === actual;
      }
      if (!ok) {
        failed++;
        if (!firstFailure) {
          firstFailure = entry.name + ": " + key + " expected " + expected +
                         ", got " + actual;
        }
      }
    });
  });
  return { total: total, failed: failed, first: firstFailure };
}

function renderVerification() {
  var chip = document.getElementById("verify");
  if (!STATE.verified) { chip.hidden = true; return; }
  var v = STATE.verified;
  chip.hidden = false;
  chip.className = "verify " + (v.failed ? "verify-fail" : "verify-pass");
  chip.textContent = T(v.failed
    ? v.failed + " of " + v.total + " values differ from pyCoastal"
    : "Engine checked: " + v.total + " values match pyCoastal");
  chip.title = v.first || T("Every reference value produced by pyCoastal is " +
    "reproduced by this page to within 1e-9 relative.");
}

/* ------------------------------------------------------------------ */
/* Boot                                                                */
/* ------------------------------------------------------------------ */

function selectModule(name) {
  STATE.module = name;
  if (history.replaceState) history.replaceState(null, "", "#" + name);
  STATE.topic = null;
  document.querySelectorAll(".rail-item").forEach(function (b) {
    var active = b.dataset.module === name;
    b.classList.toggle("active", active);
    b.setAttribute("aria-current", active ? "true" : "false");
  });
  document.getElementById("module-note").textContent = T(MODULES[name].note);
  var sheetLabel = document.getElementById("sheet-label");
  if (sheetLabel) sheetLabel.textContent = T("Drawing");
  renderInputs();
  run();
  renderTopics();
  renderKnowledge();
}

function buildRail() {
  var host = document.getElementById("rail");
  host.innerHTML = "";
  Object.keys(MODULES).forEach(function (name) {
    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "rail-item";
    btn.dataset.module = name;
    btn.textContent = T(MODULES[name].label);
    btn.addEventListener("click", function () { selectModule(name); });
    host.appendChild(btn);
  });
}

function wireEnlarge() {
  var button = document.getElementById("enlarge");
  if (!button) return;
  button.addEventListener("click", function () {
    var on = document.body.classList.toggle("focus");
    button.setAttribute("aria-pressed", String(on));
    button.textContent = T(on ? "Exit" : "Enlarge");
  });
  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && document.body.classList.contains("focus")) {
      document.body.classList.remove("focus");
      button.setAttribute("aria-pressed", "false");
      button.textContent = T("Enlarge");
    }
  });
}

function boot() {
  var langHost = document.getElementById("lang");
  if (langHost) I18N.picker(langHost);
  I18N.apply();
  I18N.onChange(function () {
    buildRail();
    selectModule(STATE.module);
    renderVerification();
    showCorpusStat();
    var enlarge = document.getElementById("enlarge");
    if (enlarge) enlarge.textContent = T(document.body.classList.contains("focus") ? "Exit" : "Enlarge");
  });
  buildRail();
  wireEnlarge();
  /* A module can be linked to directly, as index.html#breakwater. */
  var linked = location.hash.replace("#", "");
  selectModule(MODULES.hasOwnProperty(linked) ? linked : "seawall");

  fetch("vectors.json").then(function (r) { return r.json(); }).then(function (v) {
    STATE.vectors = v;
    STATE.verified = verify(v);
    renderVerification();
  }).catch(function () {
    STATE.verified = null;
    renderVerification();
  });

  wireTheory();
}

/* The literature corpus is 1.7 MB and most sittings never open it, so it
   is fetched the first time somebody asks and not before. Until then the
   page is a tool and nothing else. */
function loadKnowledge() {
  if (STATE.knowledge || STATE.knowledgePending) return;
  STATE.knowledgePending = true;
  var stat = document.getElementById("corpus-stat");
  if (stat) stat.textContent = T("Loading\u2026");

  fetch("knowledge.json").then(function (r) { return r.json(); }).then(function (k) {
    STATE.knowledge = k;
    STATE.knowledgePending = false;
    showCorpusStat();
    renderTopics();
    renderKnowledge();
  }).catch(function () {
    STATE.knowledgePending = false;
    if (stat) stat.textContent = T("Literature extract did not load");
  });
}

function showCorpusStat() {
  var stat = document.getElementById("corpus-stat");
  var k = STATE.knowledge;
  if (!stat || !k) return;
  stat.textContent = T(k.corpus.papers + " papers \u00b7 " +
    k.corpus.knowledge_claims + " claims \u00b7 " + k.corpus.topics + " topics");
}

function wireTheory() {
  var panel = document.getElementById("theory");
  var veil = document.getElementById("theory-veil");
  var open = document.getElementById("theory-open");
  var close = document.getElementById("theory-close");
  if (!panel || !open) return;

  function show(on) {
    panel.hidden = !on;
    if (veil) veil.hidden = !on;
    open.setAttribute("aria-expanded", String(on));
    if (on) {
      loadKnowledge();
      renderTopics();
      renderKnowledge();
      if (close) close.focus();
    } else {
      open.focus();
    }
  }

  open.addEventListener("click", function () { show(panel.hidden); });
  if (close) close.addEventListener("click", function () { show(false); });
  if (veil) veil.addEventListener("click", function () { show(false); });
  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && !panel.hidden) show(false);
  });
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", boot);
} else {
  boot();
}
