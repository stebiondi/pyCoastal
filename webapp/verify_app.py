"""
Exercise the browser code without a browser.

The engine is checked against pyCoastal by `verify_engine.py`. This goes a
step further and loads the page's own scripts into QuickJS behind a stub
DOM, so the module definitions, the run functions, the report and check
builders, and the in-page verification routine are all executed at least
once before the page is published. It will not catch a layout mistake, but
it catches the things that actually break a static page: a typo in a
function name, an input key that no run function reads, a check that throws
on the default values.

    python webapp/verify_app.py
"""

from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).parent

DOM_STUB = """
var __nodes = 0;
function makeNode(tag) {
  return {
    tagName: tag, style: {}, dataset: {}, childNodes: [], attributes: {},
    textContent: "", innerHTML: "", className: "", hidden: false,
    appendChild: function (c) { this.childNodes.push(c); return c; },
    insertBefore: function (c) { this.childNodes.push(c); return c; },
    setAttribute: function (k, v) { this.attributes[k] = v; },
    getAttribute: function (k) { return this.attributes[k]; },
    addEventListener: function () {},
    getBBox: function () { return { x: 0, y: 0, width: 10, height: 10 }; },
    classList: { toggle: function () {}, add: function () {}, remove: function () {} },
    querySelectorAll: function () { return []; }
  };
}
var document = {
  readyState: "loading",
  createElement: function (t) { __nodes++; return makeNode(t); },
  createElementNS: function (ns, t) { __nodes++; return makeNode(t); },
  getElementById: function () { return makeNode("div"); },
  querySelectorAll: function () { return []; },
  addEventListener: function () {}
};
var window = globalThis;
function fetch() { return { then: function () { return this; }, catch: function () { return this; } }; }
"""

HARNESS = """
function exercise() {
  var out = { modules: [], errors: [] };
  var names = Object.keys(MODULES);
  for (var i = 0; i < names.length; i++) {
    var name = names[i];
    var mod = MODULES[name];
    try {
      var v = {};
      mod.inputs.forEach(function (input) { v[input.key] = input.value; });

      // Every declared input must be read by the run function, or the
      // control is decoration.
      var touched = {};
      var probe = {};
      Object.keys(v).forEach(function (k) {
        Object.defineProperty(probe, k, {
          get: function () { touched[k] = true; return v[k]; },
          enumerable: true
        });
      });

      var result = mod.run(probe);
      var checks = mod.checks(result);
      var report = mod.report(result);
      var host = document.createElement("div");
      mod.draw(host, result, 980, 560);

      // Read after every stage, since an input can legitimately be used by
      // the checks rather than by the sizing itself.
      var unused = Object.keys(v).filter(function (k) { return !touched[k]; });

      out.modules.push({
        name: name, checks: checks.length, report: report.length,
        unused: unused,
        failing: checks.filter(function (c) {
          return !c.neutral && !c.warn && !c.ok;
        }).map(function (c) { return c.name; })
      });
    } catch (err) {
      out.errors.push(name + ": " + (err && err.message ? err.message : String(err))
                      + (err && err.stack ? " | " + err.stack.split("\\n")[0] : ""));
    }
  }
  return JSON.stringify(out);
}

function selfCheck(vectorsJson) {
  var v = JSON.parse(vectorsJson);
  return JSON.stringify(verify(v));
}
"""


def main() -> int:
    try:
        import quickjs
    except ImportError:
        print("quickjs is not installed. pip install quickjs")
        return 2

    context = quickjs.Context()
    context.eval("var globalThis = this;")
    context.eval(DOM_STUB)
    for name in ("engine.js", "draw.js", "app.js"):
        source = (HERE / name).read_text(encoding="utf-8")
        try:
            context.eval(source)
        except Exception as err:  # noqa: BLE001 - report and stop
            print(f"{name} failed to load: {err}")
            return 1
        print(f"loaded {name}")

    context.eval(HARNESS)

    report = json.loads(context.get("exercise")())
    problems = 0

    for entry in report["modules"]:
        bits = [f"{entry['checks']} checks", f"{entry['report']} report rows"]
        if entry["failing"]:
            bits.append("failing on defaults: " + ", ".join(entry["failing"]))
        if entry["unused"]:
            bits.append("UNUSED INPUTS: " + ", ".join(entry["unused"]))
            problems += 1
        print(f"  {entry['name']:<12} {'; '.join(bits)}")

    for line in report["errors"]:
        print(f"  ERROR {line}")
        problems += 1

    expected = {"seawall", "breakwater", "channel", "monopile", "extremes"}
    got = {entry["name"] for entry in report["modules"]}
    missing = expected - got
    if missing:
        print(f"  modules that never ran: {sorted(missing)}")
        problems += 1

    vectors = (HERE / "vectors.json").read_text(encoding="utf-8")
    check = json.loads(context.get("selfCheck")(vectors))
    print(f"\nin-page verification: {check['total'] - check['failed']}"
          f"/{check['total']} values match pyCoastal")
    if check["failed"]:
        print(f"  first disagreement: {check['first']}")
        problems += 1

    if problems:
        print(f"\n{problems} problem(s) found")
        return 1
    print("\nbrowser code runs clean")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
