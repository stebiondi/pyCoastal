"""
Render each module's drawing to SVG and PNG, without a browser.

`verify_app.py` proves the browser code runs. It cannot see what the code
draws, which is how a sheet that paints its own background last, over the
whole drawing, passes every check and shows the user a blank page.

This runs draw.js in QuickJS behind a DOM stub that serialises to real SVG,
writes the markup out, and rasterises it so the result can be looked at.

    pip install quickjs svglib
    python webapp/render_preview.py --out media/webapp
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

HERE = Path(__file__).parent

# A DOM stub that keeps enough structure to serialise. getBBox is estimated
# from the text length, since there is no font engine here; the pads come
# out approximately right, which is all they need to be for a look.
DOM_STUB = r"""
function Node(tag) {
  this.tag = tag;
  this.attrs = {};
  this.children = [];
  this.textContent = "";
  this.dataset = {};
  this.style = {};
  this.hidden = false;
  this.className = "";
}
Node.prototype.appendChild = function (child) {
  this.children.push(child); return child;
};
Node.prototype.insertBefore = function (child, ref) {
  var i = this.children.indexOf(ref);
  if (i < 0) this.children.push(child); else this.children.splice(i, 0, child);
  return child;
};
Node.prototype.setAttribute = function (k, v) { this.attrs[k] = v; };
Node.prototype.getAttribute = function (k) { return this.attrs[k]; };
Node.prototype.addEventListener = function () {};
Node.prototype.querySelectorAll = function () { return []; };
Node.prototype.getBBox = function () {
  var size = parseFloat(this.attrs["font-size"] || 10);
  var w = (this.textContent || "").length * size * 0.56;
  var h = size * 1.1;
  var x = parseFloat(this.attrs.x || 0);
  var y = parseFloat(this.attrs.y || 0);
  var anchor = this.attrs["text-anchor"];
  if (anchor === "middle") x -= w / 2;
  else if (anchor === "end") x -= w;
  return { x: x, y: y - size * 0.82, width: w, height: h };
};
Object.defineProperty(Node.prototype, "innerHTML", {
  get: function () { return ""; },
  set: function () { this.children = []; }
});
Object.defineProperty(Node.prototype, "classList", {
  get: function () { return { toggle: function () {}, add: function () {},
                              remove: function () {} }; }
});

var document = {
  readyState: "loading",
  createElement: function (t) { return new Node(t); },
  createElementNS: function (ns, t) { return new Node(t); },
  getElementById: function () { return new Node("div"); },
  querySelectorAll: function () { return []; },
  addEventListener: function () {}
};
var window = globalThis;
function fetch() {
  return { then: function () { return this; }, catch: function () { return this; } };
}

var VOID_OK = {};
function escapeXml(s) {
  return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;")
                  .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}
function serialise(node) {
  var out = "<" + node.tag;
  for (var k in node.attrs) {
    out += " " + k + '="' + escapeXml(node.attrs[k]) + '"';
  }
  if (node.tag === "svg") out += ' xmlns="http://www.w3.org/2000/svg"';
  out += ">";
  if (node.textContent) out += escapeXml(node.textContent);
  for (var i = 0; i < node.children.length; i++) {
    out += serialise(node.children[i]);
  }
  return out + "</" + node.tag + ">";
}
"""

HARNESS = """
function inputsFor(name, overrideJson) {
  var mod = MODULES[name];
  var v = {};
  mod.inputs.forEach(function (input) { v[input.key] = input.value; });
  var over = overrideJson ? JSON.parse(overrideJson) : {};
  for (var k in over) {
    if (!(k in v)) throw new Error(name + " has no input " + k);
    v[k] = over[k];
  }
  return v;
}

function renderModule(name, w, h, overrideJson) {
  var mod = MODULES[name];
  var v = inputsFor(name, overrideJson);
  var result = mod.run(v);
  var host = document.createElement("div");
  mod.draw(host, result, w, h);
  if (!host.children.length) throw new Error("nothing was drawn");
  var svg = host.children[host.children.length - 1];
  return serialise(svg);
}

function countShapes(name, w, h, overrideJson) {
  var mod = MODULES[name];
  var v = inputsFor(name, overrideJson);
  var host = document.createElement("div");
  mod.draw(host, mod.run(v), w, h);
  var svg = host.children[host.children.length - 1];
  var tally = {};
  (function walk(node) {
    tally[node.tag] = (tally[node.tag] || 0) + 1;
    node.children.forEach(walk);
  })(svg);
  return JSON.stringify(tally);
}
"""


# Every drawing the app can put on screen, including the ones that need a
# non-default input to reach. A view nobody renders is a view nobody has
# looked at.
VIEWS = [
    ("seawall", "seawall", {}),
    ("breakwater", "breakwater_trunk", {}),
    ("breakwater", "breakwater_head", {"section": "head"}),
    ("channel", "channel", {}),
    ("monopile", "monopile", {}),
    ("nourishment", "nourishment_profile", {}),
    ("nourishment", "nourishment_planform", {"view": "planform"}),
    ("extremes", "extremes", {}),
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("media/webapp"))
    parser.add_argument("--width", type=int, default=980)
    parser.add_argument("--height", type=int, default=560)
    parser.add_argument("--no-png", action="store_true")
    args = parser.parse_args()

    try:
        import quickjs
    except ImportError:
        print("quickjs is not installed. pip install quickjs")
        return 2

    context = quickjs.Context()
    context.eval("var globalThis = this;")
    context.eval(DOM_STUB)
    for name in ("engine.js", "draw.js", "app.js"):
        context.eval((HERE / name).read_text(encoding="utf-8"))
    context.eval(HARNESS)

    render = context.get("renderModule")
    tally = context.get("countShapes")
    args.out.mkdir(parents=True, exist_ok=True)

    problems = 0
    for module, label, overrides in VIEWS:
        try:
            markup = render(module, args.width, args.height,
                            json.dumps(overrides))
        except Exception as err:  # noqa: BLE001
            print(f"  {label:<22} FAILED: {err}")
            problems += 1
            continue

        svg_path = args.out / f"{label}.svg"
        svg_path.write_text(markup, encoding="utf-8")
        counts = json.loads(tally(module, args.width, args.height,
                                  json.dumps(overrides)))

        # A sheet that draws only its own frame is the blank-page failure.
        drawn = counts.get("path", 0) + counts.get("circle", 0) + counts.get("rect", 0)
        note = ""
        if drawn < 12:
            note = "  LOOKS EMPTY"
            problems += 1
        print(f"  {label:<22} {len(markup) // 1024:>4} kB markup, "
              f"{drawn:>4} shapes, {counts.get('text', 0):>3} labels{note}")

        if not args.no_png:
            # PDF rather than PNG: reportlab's raster backend wants cairo,
            # which is not here, and a PDF is just as viewable.
            try:
                from reportlab.graphics import renderPDF
                from svglib.svglib import svg2rlg

                drawing = svg2rlg(str(svg_path))
                renderPDF.drawToFile(drawing, str(args.out / f"{label}.pdf"))
            except Exception as err:  # noqa: BLE001
                print(f"    (render failed: {type(err).__name__}: {err})")

    print(f"\nwrote {args.out}")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
