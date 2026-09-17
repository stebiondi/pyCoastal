"""
Run engine.js against the pyCoastal reference cases and report any drift.

The browser app carries a JavaScript transliteration of the design modules.
This is what keeps it honest: it executes the actual JavaScript, in QuickJS,
against the values pyCoastal produced, and fails loudly on any disagreement
beyond floating-point noise.

    pip install quickjs
    python webapp/make_vectors.py
    python webapp/verify_engine.py

The same comparison runs in the browser on load, so a user sees the result
too. A second implementation nobody checks is a liability, not a feature.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

HERE = Path(__file__).parent

# Relative tolerance. The two implementations do the same arithmetic in the
# same order, so anything beyond rounding is a real difference.
RTOL = 1e-9
ATOL = 1e-12


def dispatch_source() -> str:
    """A JavaScript shim that turns a case description into a call."""
    return """
function runCase(spec) {
  var fn = spec.fn;
  var args = spec.args ? spec.args.slice() : [];
  var target;
  if (spec.conditions) {
    var c = PYCOASTAL.conditionsFromPeak(spec.conditions[0], spec.conditions[1],
                                         spec.conditions[2], spec.conditions[3]);
    if (spec.design_first) {
      // The first argument is the options for a mound, not the conditions:
      // build the design and pass that instead.
      args[0] = PYCOASTAL.designRubbleMound(c, args[0]);
    } else {
      args.unshift(c);
    }
  }
  if (spec.fill) {
    var f = spec.fill;
    var cl = spec.climate;
    args.unshift(PYCOASTAL.makeClimate(cl[0], cl[1], cl[2]));
    args.unshift(PYCOASTAL.makeFill(f[0], f[1], f[2], f[3], f[4]));
  }
  if (spec.vessel) {
    var v = PYCOASTAL.makeVessel(spec.vessel[0], spec.vessel[1], spec.vessel[2],
                                 spec.vessel[3], spec.vessel[4]);
    args.unshift(v);
  }
  target = PYCOASTAL[fn];
  if (!target) throw new Error("no such function: " + fn);
  var out = target.apply(null, args);
  if (typeof out === "number" || typeof out === "boolean") return {value: out};
  return out;
}

function finite(value) {
  if (typeof value !== "number") return value;
  if (value === Infinity) return "inf";
  if (value === -Infinity) return "-inf";
  if (value !== value) return "nan";
  return value;
}

function flatten(result) {
  // Pull out the few fields the reference cases check, including the ones
  // that live one level down.
  var flat = {};
  for (var k in result) {
    var v = result[k];
    if (typeof v === "number" || typeof v === "string" || typeof v === "boolean") {
      flat[k] = finite(v);
    }
  }
  if (result.layer && typeof result.layer.thickness === "number") {
    flat.layer_thickness = result.layer.thickness;
  }
  if (result.quantities) flat.concrete = result.quantities.concrete_total_m3_per_m;
  if (result.sweep) {
    flat.max_moment = result.sweep.max_moment;
    flat.max_force = result.sweep.max_force;
    flat.phase_of_max_moment = result.sweep.phase_of_max_moment;
  }
  if (result.scour && typeof result.scour.depth === "number") {
    flat.scour = result.scour.depth;
  }
  if (result.squat && typeof result.squat.squat === "number") {
    flat.squat = result.squat.squat;
  }
  if (result.assumed && result.assumed.length !== undefined) {
    flat.assumed = result.assumed.length;
  }
  if (typeof result.volume_per_km === "number") {
    flat.volume_per_km = result.volume_per_km;
  }
  if (result.earth_driving) {
    flat.earth_total = result.earth_driving.total;
    flat.earth_arm = result.earth_driving.arm;
  }
  if (result.drawdown) {
    flat.drawdown_sliding = finite(result.drawdown.sliding_FoS);
    flat.drawdown_net = finite(result.drawdown.net_force);
  }
  if (typeof result.cot_beta === "number") flat.cot_beta = result.cot_beta;
  if (result.length !== undefined && typeof result[0] === "number") {
    // An L-moment array.
    flat.l1 = result[0]; flat.l2 = result[1];
    flat.l3 = result[2]; flat.l4 = result[3];
  }
  return flat;
}

function evaluate(specJson) {
  var spec = JSON.parse(specJson);
  try {
    return JSON.stringify({ok: true, got: flatten(runCase(spec))});
  } catch (err) {
    return JSON.stringify({ok: false, error: String(err && err.message || err)});
  }
}
"""


def close_enough(expected, got) -> bool:
    if isinstance(expected, bool) or isinstance(got, bool):
        return bool(expected) == bool(got)
    if isinstance(expected, str) or isinstance(got, str):
        return expected == got
    if expected is None or got is None:
        return expected == got
    if isinstance(expected, (int, float)) and isinstance(got, (int, float)):
        if math.isnan(expected) and math.isnan(got):
            return True
        if math.isinf(expected) or math.isinf(got):
            return expected == got
        return abs(expected - got) <= max(ATOL, RTOL * abs(expected))
    return expected == got


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine", type=Path, default=HERE / "engine.js")
    parser.add_argument("--vectors", type=Path, default=HERE / "vectors.json")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    try:
        import quickjs
    except ImportError:
        print("quickjs is not installed. pip install quickjs")
        return 2

    context = quickjs.Context()
    context.eval("var globalThis = this;")
    context.eval(args.engine.read_text(encoding="utf-8"))
    context.eval(dispatch_source())
    evaluate = context.get("evaluate")

    vectors = json.loads(args.vectors.read_text(encoding="utf-8"))
    failures: list[str] = []
    checked = 0

    for entry in vectors["cases"]:
        raw = evaluate(json.dumps(entry["call"]))
        result = json.loads(raw)
        if not result["ok"]:
            failures.append(f"{entry['name']}: raised {result['error']}")
            continue
        got = result["got"]
        for key, expected in entry["expect"].items():
            checked += 1
            if key not in got:
                failures.append(f"{entry['name']}: JavaScript returned no {key!r}")
                continue
            if not close_enough(expected, got[key]):
                failures.append(
                    f"{entry['name']}: {key} python={expected!r} js={got[key]!r}"
                )
            elif args.verbose:
                print(f"  ok  {entry['name']}: {key} = {expected}")

    print(f"{len(vectors['cases'])} cases, {checked} values compared")
    if failures:
        print(f"\n{len(failures)} disagreement(s):")
        for line in failures:
            print(f"  {line}")
        return 1
    print("engine.js agrees with pyCoastal on every value")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
