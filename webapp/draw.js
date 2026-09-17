/*
 * SVG drawing sheets, in the same vocabulary as pyCoastal.drafting.
 *
 * The Python renders sections through matplotlib; this renders them through
 * SVG so the browser can redraw one on every keystroke. The conventions are
 * deliberately identical: hatched materials, dimension lines with tick
 * terminators, levelling triangles, slope triangles, a detail bubble and a
 * stated scale. A drawing that changes its conventions between the screen
 * and the issued sheet is two drawings.
 *
 * Model coordinates are metres, x to the right and z upward. SVG is y-down,
 * so every view carries the flip.
 */

var SVGNS = "http://www.w3.org/2000/svg";

function el(tag, attrs, parent) {
  var node = document.createElementNS(SVGNS, tag);
  if (attrs) {
    for (var k in attrs) {
      if (attrs[k] !== null && attrs[k] !== undefined) {
        node.setAttribute(k, String(attrs[k]));
      }
    }
  }
  if (parent) parent.appendChild(node);
  return node;
}

/* Materials, matching pyCoastal.drafting.MATERIALS. Each names a pattern
 * defined once in <defs> and reused, so a sheet with two hundred hatched
 * polygons is still one pattern. */
var MATERIALS = {
  armour:     { fill: "#9b978f", stroke: "#2f2d2a", pattern: null,   label: "Primary armour" },
  underlayer: { fill: "#c0bcb2", stroke: "#45433e", pattern: null,   label: "Underlayer" },
  core:       { fill: "#d5d1c6", stroke: "#54514b", pattern: "dots", label: "Quarry run core" },
  toe:        { fill: "#a8a49b", stroke: "#35332f", pattern: null,   label: "Toe protection" },
  concrete:   { fill: "#cfcbc4", stroke: "#2a2a2a", pattern: "fwd",  label: "Mass concrete" },
  reinforced: { fill: "#c4c0b8", stroke: "#1f1f1f", pattern: "cross", label: "Reinforced concrete" },
  blinding:   { fill: "#bdb9b1", stroke: "#45433e", pattern: "back", label: "Blinding layer" },
  granular:   { fill: "#ddd2b6", stroke: "#6f6343", pattern: "dots", label: "Granular backfill" },
  sand:       { fill: "#e6d5ad", stroke: "#8a7648", pattern: "dots", label: "Sand" },
  subgrade:   { fill: "#cdc0a6", stroke: "#6d6243", pattern: "fwd",  label: "In-situ seabed" },
  pavement:   { fill: "#b8b4ae", stroke: "#33322f", pattern: null,   label: "Surfacing" },
  water:      { fill: "#c3dce7", stroke: "#4d7f97", pattern: null,   label: "Water" }
};

var INK = "#16181a";

function definePatterns(svg) {
  var defs = el("defs", null, svg);
  function hatch(id, d, angle) {
    var p = el("pattern", {
      id: id, width: 7, height: 7, patternUnits: "userSpaceOnUse",
      patternTransform: "rotate(" + angle + ")"
    }, defs);
    el("path", { d: d, stroke: INK, "stroke-width": 0.5, opacity: 0.55 }, p);
  }
  hatch("hx-fwd", "M0,0 V7", 45);
  hatch("hx-back", "M0,0 V7", -45);
  var cross = el("pattern", {
    id: "hx-cross", width: 8, height: 8, patternUnits: "userSpaceOnUse",
    patternTransform: "rotate(45)"
  }, defs);
  el("path", { d: "M0,0 V8 M0,0 H8", stroke: INK, "stroke-width": 0.5, opacity: 0.5 }, cross);
  var dots = el("pattern", {
    id: "hx-dots", width: 6, height: 6, patternUnits: "userSpaceOnUse"
  }, defs);
  el("circle", { cx: 2, cy: 2, r: 0.7, fill: INK, opacity: 0.45 }, dots);
  return defs;
}

var CLIP_ID = 0;

/* Confine a group to the view box. The ground and the water are drawn well
 * past the extents on purpose, so that they have no visible ends; the clip
 * is what stops them running over the sheet furniture. */
function clipTo(svg, g, box) {
  var id = "vclip" + (CLIP_ID++);
  var cp = el("clipPath", { id: id }, svg);
  el("rect", { x: box.x, y: box.y, width: box.w, height: box.h }, cp);
  g.setAttribute("clip-path", "url(#" + id + ")");
}

/* A view maps model metres onto the SVG box at a true, stated scale, with
 * an optional vertical exaggeration that the caller is expected to print. */
function View(box, xlim, zlim, exaggeration) {
  this.box = box;
  this.exaggeration = exaggeration || 1;
  var needW = xlim[1] - xlim[0];
  var needH = (zlim[1] - zlim[0]) * this.exaggeration;
  var s = Math.min(box.w / needW, box.h / needH);
  this.s = s;
  var cx = 0.5 * (xlim[0] + xlim[1]);
  var cz = 0.5 * (zlim[0] + zlim[1]);
  this.cx = cx;
  this.cz = cz;
  // Pixels per metre horizontally; vertically it is s * exaggeration.
  this.X = function (x) { return box.x + 0.5 * box.w + (x - cx) * s; };
  this.Y = function (z) { return box.y + 0.5 * box.h - (z - cz) * s * this.exaggeration; };
  // Drawn scale, for the title block: metres of world per metre of paper,
  // assuming a nominal 96 CSS px to the inch.
  this.scaleDenominator = 1 / (s / 96 * 0.0254);
}

View.prototype.poly = function (g, points, material, label) {
  var spec = MATERIALS[material];
  var self = this;
  var d = points.map(function (p, i) {
    return (i ? "L" : "M") + self.X(p[0]).toFixed(2) + "," + self.Y(p[1]).toFixed(2);
  }).join(" ") + " Z";
  el("path", { d: d, fill: spec.fill, stroke: spec.stroke, "stroke-width": 1,
               "stroke-linejoin": "miter" }, g);
  if (spec.pattern) {
    el("path", { d: d, fill: "url(#hx-" + spec.pattern + ")", stroke: "none" }, g);
  }
  return { material: material, label: label || spec.label };
};

View.prototype.line = function (g, points, opts) {
  opts = opts || {};
  var self = this;
  var d = points.map(function (p, i) {
    return (i ? "L" : "M") + self.X(p[0]).toFixed(2) + "," + self.Y(p[1]).toFixed(2);
  }).join(" ");
  el("path", {
    d: d, fill: "none", stroke: opts.stroke || INK,
    "stroke-width": opts.width || 1,
    "stroke-dasharray": opts.dash || null
  }, g);
};

View.prototype.text = function (g, x, y, str, opts) {
  opts = opts || {};
  var t = el("text", {
    x: x, y: y, fill: opts.fill || INK,
    "font-size": opts.size || 10,
    "font-family": "'IBM Plex Mono', ui-monospace, monospace",
    "font-weight": opts.weight || 400,
    "text-anchor": opts.anchor || "start",
    transform: opts.rotate ? "rotate(" + opts.rotate + " " + x + " " + y + ")" : null
  }, g);
  t.textContent = str;
  return t;
};

/* A dimension with the architectural tick terminators the Python uses in
 * sheet mode, and the text on a small white pad so it stays readable over
 * hatching. */
View.prototype.dimH = function (g, x0, x1, z, label, extendFrom) {
  var y = this.Y(z), a = this.X(x0), b = this.X(x1);
  if (extendFrom) {
    this.line(g, [[x0, extendFrom[0]], [x0, z]], { width: 0.5, dash: "4 3" });
    this.line(g, [[x1, extendFrom[1]], [x1, z]], { width: 0.5, dash: "4 3" });
  }
  el("path", { d: "M" + a + "," + y + " H" + b, stroke: INK, "stroke-width": 0.6 }, g);
  [a, b].forEach(function (px) {
    el("path", { d: "M" + (px - 4) + "," + (y + 4) + " L" + (px + 4) + "," + (y - 4),
                 stroke: INK, "stroke-width": 0.9 }, g);
  });
  this.pad(g, 0.5 * (a + b), y - 4, label, "middle");
};

View.prototype.dimV = function (g, z0, z1, x, label, extendFrom) {
  var px = this.X(x), a = this.Y(z0), b = this.Y(z1);
  if (extendFrom) {
    this.line(g, [[extendFrom[0], z0], [x, z0]], { width: 0.5, dash: "4 3" });
    this.line(g, [[extendFrom[1], z1], [x, z1]], { width: 0.5, dash: "4 3" });
  }
  el("path", { d: "M" + px + "," + a + " V" + b, stroke: INK, "stroke-width": 0.6 }, g);
  [a, b].forEach(function (py) {
    el("path", { d: "M" + (px - 4) + "," + (py + 4) + " L" + (px + 4) + "," + (py - 4),
                 stroke: INK, "stroke-width": 0.9 }, g);
  });
  var t = this.text(g, px - 3, 0.5 * (a + b), label,
                    { size: 9, anchor: "middle", rotate: -90 });
  this.backdrop(g, t);
};

View.prototype.pad = function (g, px, py, label, anchor) {
  var t = this.text(g, px, py, label, { size: 9, anchor: anchor || "start" });
  this.backdrop(g, t);
  return t;
};

/* White pad behind a label, sized from the rendered text. */
View.prototype.backdrop = function (g, textNode) {
  try {
    var b = textNode.getBBox();
    var rect = el("rect", {
      x: b.x - 2.5, y: b.y - 1.5, width: b.width + 5, height: b.height + 3,
      fill: "#ffffff", opacity: 0.86, rx: 1.5,
      transform: textNode.getAttribute("transform")
    });
    g.insertBefore(rect, textNode);
  } catch (err) { /* getBBox throws if the node is not laid out yet */ }
};

/* The surveyor's level: a triangle with the elevation beside it. */
View.prototype.level = function (g, x, z, label, side) {
  var px = this.X(x), py = this.Y(z);
  var solid = side !== "water";
  el("path", { d: "M" + (px - 5) + "," + (py - 7) + " L" + (px + 5) + "," + (py - 7) +
                  " L" + px + "," + py + " Z",
               fill: solid ? INK : "#ffffff", stroke: INK, "stroke-width": 0.9 }, g);
  var t = this.text(g, px + 8, py - 8, label, { size: 9, weight: 600 });
  this.backdrop(g, t);
};

View.prototype.slope = function (g, x, z, cot, rise, direction, label) {
  var sign = direction === "left" ? -1 : 1;
  var run = sign * cot * rise;
  this.line(g, [[x, z], [x, z - rise], [x + run, z - rise], [x, z]], { width: 0.6 });
  this.pad(g, this.X(x + 0.5 * run), this.Y(z - rise) + 11,
           label || ("1 : " + cot), "middle");
};

/* The sheet furniture: border, detail bubble, stated scale. */
/* Border, detail bubble and stated scale. Appended last so it sits over the
 * drawing, which is why it must not paint a background: the paper is laid
 * down by newSheet, before anything is drawn on it. */
function sheetFrame(svg, w, h, opts) {
  var g = el("g", null, svg);
  el("rect", { x: 6, y: 6, width: w - 12, height: h - 12, fill: "none",
               stroke: INK, "stroke-width": 1.4 }, g);
  var by = h - 26;
  el("circle", { cx: 26, cy: by, r: 10, fill: "#ffffff", stroke: INK,
                 "stroke-width": 1.1 }, g);
  var letter = el("text", {
    x: 26, y: by + 4, "text-anchor": "middle", "font-size": 11,
    "font-family": "'Archivo', system-ui, sans-serif", "font-weight": 700, fill: INK
  }, g);
  letter.textContent = opts.bubble || "A";
  var title = el("text", {
    x: 44, y: by - 2, "font-size": 12, "font-weight": 700, fill: INK,
    "font-family": "'Archivo', system-ui, sans-serif",
    "letter-spacing": "0.04em"
  }, g);
  title.textContent = (opts.title || "").toUpperCase();
  var sub = el("text", {
    x: 44, y: by + 12, "font-size": 9, fill: "#54514b",
    "font-family": "'IBM Plex Mono', ui-monospace, monospace"
  }, g);
  sub.textContent = opts.scale || "";
  return g;
}

/* A chequered scale bar, so the drawing survives being screenshotted. */
function scaleBar(svg, view, length, px, py, unit) {
  var g = el("g", null, svg);
  var divisions = 4;
  var step = length / divisions;
  var wpx = view.s * step;
  for (var i = 0; i < divisions; i++) {
    el("rect", { x: px + i * wpx, y: py, width: wpx, height: 5,
                 fill: i % 2 ? INK : "#ffffff", stroke: INK,
                 "stroke-width": 0.6 }, g);
  }
  for (i = 0; i <= divisions; i++) {
    var t = el("text", {
      x: px + i * wpx, y: py - 4, "text-anchor": "middle", "font-size": 8,
      "font-family": "'IBM Plex Mono', ui-monospace, monospace", fill: INK
    }, g);
    t.textContent = String(Math.round(i * step * 10) / 10);
  }
  var u = el("text", {
    x: px + divisions * wpx + 6, y: py + 5, "font-size": 8, fill: INK,
    "font-family": "'IBM Plex Mono', ui-monospace, monospace"
  }, g);
  u.textContent = unit || "m";
}

function legend(svg, entries, x, y) {
  var g = el("g", null, svg);
  var seen = {};
  var rows = [];
  entries.forEach(function (e) {
    if (!e || seen[e.label]) return;
    seen[e.label] = true;
    rows.push(e);
  });
  var pad = 6, rowH = 15;
  var longest = 0;
  rows.forEach(function (e) { longest = Math.max(longest, e.label.length); });
  var boxW = Math.max(150, 34 + longest * 5.6);
  var box = el("rect", {
    x: x, y: y, width: boxW, height: rows.length * rowH + 2 * pad,
    fill: "#ffffff", opacity: 0.94, stroke: INK, "stroke-width": 0.6
  }, g);
  rows.forEach(function (e, i) {
    var spec = MATERIALS[e.material];
    var ry = y + pad + i * rowH;
    el("rect", { x: x + pad, y: ry + 2, width: 16, height: 9,
                 fill: spec.fill, stroke: spec.stroke, "stroke-width": 0.6 }, g);
    if (spec.pattern) {
      el("rect", { x: x + pad, y: ry + 2, width: 16, height: 9,
                   fill: "url(#hx-" + spec.pattern + ")" }, g);
    }
    var t = el("text", {
      x: x + pad + 22, y: ry + 10, "font-size": 9, fill: INK,
      "font-family": "'IBM Plex Mono', ui-monospace, monospace"
    }, g);
    t.textContent = e.label;
  });
  return g;
}

function newSheet(host, w, h) {
  host.innerHTML = "";
  var svg = el("svg", {
    viewBox: "0 0 " + w + " " + h,
    width: w, height: h,
    preserveAspectRatio: "xMidYMid meet",
    role: "img"
  }, host);
  definePatterns(svg);
  el("rect", { x: 0, y: 0, width: w, height: h, fill: "#ffffff" }, svg);
  return svg;
}

/* ------------------------------------------------------------------ */
/* Seawall                                                             */
/* ------------------------------------------------------------------ */

function drawSeawall(host, d, w, h) {
  var svg = newSheet(host, w, h);
  var seaExtent = Math.max(20, 2.2 * d.water_depth);
  /* Room on the landward side for the pressure diagram as well as the fill. */
  var landExtent = Math.max(12, 1.0 * d.base_width);
  var x0 = -seaExtent, x1 = d.base_width + landExtent;
  var bed = d.seabed_level, swl = d.still_water_level;
  var found = d.founding_level, baseTop = found + d.base_thickness;
  var z0 = Math.min(found - 2.5, bed - d.scour_depth - 1.5);
  var z1 = d.crest_level + 3.5;

  var body = el("g", null, svg);
  var view = new View({ x: 54, y: 16, w: w - 74, h: h - 66 }, [x0, x1], [z0, z1]);
  clipTo(svg, body, view.box);
  var keys = [];

  keys.push(view.poly(body, [[x0, z0 - 5], [x1, z0 - 5], [x1, bed], [x0, bed]],
                      "subgrade"));
  keys.push(view.poly(body, [[x0, bed], [0, bed], [0, swl], [x0, swl]], "water"));

  var bermFace = 1.5 * d.toe_berm_thickness;
  keys.push(view.poly(body, [
    [-d.toe_berm_width - bermFace, bed],
    [-d.toe_berm_width, bed + d.toe_berm_thickness],
    [0, bed + d.toe_berm_thickness], [0, bed]
  ], "toe", "Toe rock, Dn50 = " + d.toe_Dn50.toFixed(2) + " m"));

  keys.push(view.poly(body, [[0, found - 0.15], [d.base_width, found - 0.15],
                             [d.base_width, found], [0, found]], "blinding"));
  keys.push(view.poly(body, [[d.stem_thickness, baseTop], [x1, baseTop],
                             [x1, d.promenade_level], [d.stem_thickness, d.promenade_level]],
                      "granular"));
  keys.push(view.poly(body, [[0, found], [d.base_width, found],
                             [d.base_width, baseTop], [0, baseTop]], "reinforced",
                      "Reinforced concrete"));
  view.poly(body, [[0, baseTop], [d.stem_thickness, baseTop],
                   [d.stem_thickness, d.crest_level], [0, d.crest_level]], "reinforced");

  /* The balance, drawn. Goda on the seaward face, soil and pore water on
     the virtual back face. Both to the same pressure scale, so the picture
     answers the question the numbers answer: which side is winning. */
  var pressureScale = 0;
  var maxBack = 0;
  if (d.earth_driving && d.earth_driving.diagram) {
    var diag = d.earth_driving.diagram;
    for (var pi = 0; pi < diag.total.length; pi++) {
      if (diag.total[pi] > maxBack) maxBack = diag.total[pi];
    }
  }
  var maxFront = d.pressures ? d.pressures.p1 : 0;
  var maxPressure = Math.max(maxBack, maxFront, 1);
  pressureScale = (0.30 * landExtent) / maxPressure;   /* metres per kPa */

  if (d.pressures) {
    var hc = d.pressures.hc_star;
    var wave = [
      [0, swl + hc],
      [-d.pressures.p4 * pressureScale, swl + hc],
      [-d.pressures.p1 * pressureScale, swl],
      [-d.pressures.p3 * pressureScale, bed],
      [0, bed]
    ];
    var wavePath = wave.map(function (q, i) {
      return (i ? "L" : "M") + view.X(q[0]).toFixed(1) + "," + view.Y(q[1]).toFixed(1);
    }).join(" ") + " Z";
    el("path", { d: wavePath, fill: "#1b6fa0", "fill-opacity": 0.28,
                 stroke: "#0b3554", "stroke-width": 1.1 }, body);
    view.pad(body, view.X(-d.pressures.p1 * pressureScale) - 6, view.Y(swl) - 6,
             "wave " + d.pressures.F.toFixed(0) + " kN/m", "end");
  }

  if (d.earth_driving && d.earth_driving.diagram) {
    var dg = d.earth_driving.diagram;
    var top = d.promenade_level;
    var backTotal = [[d.base_width, top]];
    var backPore = [[d.base_width, top]];
    for (var j = 0; j < dg.depth.length; j++) {
      var zj = top - dg.depth[j];
      backTotal.push([d.base_width + dg.total[j] * pressureScale, zj]);
      backPore.push([d.base_width + dg.pore[j] * pressureScale, zj]);
    }
    backTotal.push([d.base_width, top - dg.depth[dg.depth.length - 1]]);
    backPore.push([d.base_width, top - dg.depth[dg.depth.length - 1]]);

    function pressurePath(points) {
      return points.map(function (q, i) {
        return (i ? "L" : "M") + view.X(q[0]).toFixed(1) + "," +
               view.Y(q[1]).toFixed(1);
      }).join(" ") + " Z";
    }
    el("path", { d: pressurePath(backTotal), fill: "#c47f1a",
                 "fill-opacity": 0.30, stroke: "#8a5a12",
                 "stroke-width": 1.1 }, body);
    el("path", { d: pressurePath(backPore), fill: "#1b6fa0",
                 "fill-opacity": 0.38, stroke: "#0b3554",
                 "stroke-width": 0.9 }, body);
    view.pad(body,
             view.X(d.base_width + maxBack * pressureScale) + 8,
             view.Y(top - 0.72 * d.retained_height),
             "soil + water " + d.earth_driving.total.toFixed(0) + " kN/m");
    view.pad(body,
             view.X(d.base_width + maxBack * pressureScale * 0.30) + 4,
             view.Y(top - 0.42 * d.retained_height),
             "pore " + d.earth_driving.water.toFixed(0) + " kN/m");
  }

  if (d.scour_depth > 0) {
    var L = d.pressures.wavelength;
    var half = Math.min(Math.max(2 * d.scour_depth, 0.1 * L), 0.22 * seaExtent);
    var centre = Math.max(-0.25 * L, -0.55 * seaExtent + half);
    var pts = [];
    for (var i = 0; i <= 60; i++) {
      var xs = centre - half + 2 * half * i / 60;
      var c = Math.cos(0.5 * Math.PI * (xs - centre) / half);
      pts.push([xs, bed - d.scour_depth * c * c]);
    }
    view.line(body, pts, { stroke: "#8a2f24", width: 1.2, dash: "6 3" });
    view.pad(body, view.X(centre), view.Y(bed - d.scour_depth) + 14,
             "scour " + d.scour_depth.toFixed(2) + " m", "middle");
  }

  view.level(body, x0 + 1.5, swl, "SWL " + fmt(swl) + " m CD", "water");
  view.level(body, d.stem_thickness, d.crest_level, "Crest " + fmt(d.crest_level));
  view.level(body, -d.toe_berm_width - bermFace, bed, "Seabed " + fmt(bed));
  view.level(body, d.base_width, found, "Founding " + fmt(found));

  view.dimH(body, 0, d.base_width, d.crest_level + 1.5,
            "B = " + d.base_width.toFixed(2),
            [d.crest_level, d.promenade_level]);
  view.dimV(body, swl, d.crest_level, x1 - 0.22 * landExtent,
            "Rc = " + d.crest_freeboard.toFixed(2),
            [d.base_width, d.stem_thickness]);
  view.dimV(body, found, bed, x0 + 3.0, d.embedment.toFixed(2), [0, 0]);

  legend(svg, keys, 62, 24);
  scaleBar(svg, view, 10 * view.s > 60 ? 10 : 20, w - 230, h - 26);
  sheetFrame(svg, w, h, {
    bubble: "A", title: "Seawall typical section",
    scale: "1:" + Math.round(view.scaleDenominator / 5) * 5 + " on screen" +
           (d.governing_case ? "   governed by the " + d.governing_case : "")
  });
  return svg;
}

/* ------------------------------------------------------------------ */
/* Breakwater                                                          */
/* ------------------------------------------------------------------ */

function moundProfile(xSea, xLand, crest, cotSea, cotLand) {
  return {
    xSea: xSea, xLand: xLand, crest: crest, cotSea: cotSea, cotLand: cotLand,
    points: function (bed) {
      var rise = crest - bed;
      return [[xSea - cotSea * rise, bed], [xSea, crest], [xLand, crest],
              [xLand + cotLand * rise, bed]];
    },
    offset: function (t) {
      return moundProfile(
        xSea + t * (Math.hypot(1, cotSea) - cotSea),
        xLand - t * (Math.hypot(1, cotLand) - cotLand),
        crest - t, cotSea, cotLand);
    }
  };
}

function drawBreakwater(host, d, swl, bed, w, h) {
  var svg = newSheet(host, w, h);
  var crest = swl + d.crest_freeboard;
  var cotSea = d.cot_alpha;
  var cotLand = Math.max(cotSea - 0.5, 1.5);
  var tArmour = d.layer.thickness;
  var DnUnder = d.Dn50 / Math.pow(10, 1 / 3);
  var crestWidth = Math.max(3 * d.Dn50, 4);

  var outer = moundProfile(-0.5 * crestWidth, 0.5 * crestWidth, crest, cotSea, cotLand);
  var under = outer.offset(tArmour);
  var core = under.offset(2 * DnUnder);

  var toeX = outer.points(bed)[0][0];
  var margin = 12;
  var x0 = toeX - margin;
  var x1 = outer.points(bed)[3][0] + margin;
  var z0 = bed - 3, z1 = crest + 4;

  var body = el("g", null, svg);
  var view = new View({ x: 44, y: 16, w: w - 64, h: h - 66 }, [x0, x1], [z0, z1]);
  clipTo(svg, body, view.box);
  var keys = [];

  keys.push(view.poly(body, [[x0, z0 - 5], [x1, z0 - 5], [x1, bed], [x0, bed]], "subgrade"));
  keys.push(view.poly(body, [[x0, bed], [x1, bed], [x1, swl], [x0, swl]], "water"));
  keys.push(view.poly(body, core.points(bed), "core", "Quarry run core"));
  keys.push(view.poly(body, under.points(bed).concat(core.points(bed).slice().reverse()),
                      "underlayer", "Underlayer, Dn50 = " + DnUnder.toFixed(2) + " m"));
  keys.push(view.poly(body, outer.points(bed).concat(under.points(bed).slice().reverse()),
                      "armour", "Armour, Dn50 = " + d.Dn50.toFixed(2) + " m ("
                        + (d.M50 / 1000).toFixed(1) + " t)"));

  var toeW = Math.max(3 * d.Dn50, 3), toeT = 2 * d.Dn50;
  keys.push(view.poly(body, [[toeX - toeW - 1.5 * toeT, bed], [toeX - toeW, bed + toeT],
                             [toeX + 0.5, bed + toeT], [toeX + 0.5, bed]], "toe", "Toe berm"));

  // Individual stones on the armour face, at the computed Dn50. This is the
  // detail that makes a mound read as rubble rather than as a shaded wedge.
  stoneTexture(body, view, outer, under, bed, d.Dn50);

  view.level(body, x0 + 2, swl, "SWL " + fmt(swl) + " m CD", "water");
  view.level(body, 0, crest, "Crest " + fmt(crest) + " m CD");
  view.dimH(body, outer.xSea, outer.xLand, crest + 1.6, crestWidth.toFixed(1),
            [crest, crest]);
  view.dimV(body, swl, crest, x1 - 0.30 * margin,
            "Rc = " + d.crest_freeboard.toFixed(2),
            [outer.xLand, x1 - 0.30 * margin]);
  var mid = 0.5 * (swl + crest);
  view.slope(body, outer.xSea - cotSea * (crest - mid), mid, cotSea,
             0.22 * (crest - bed), "left", "1 : " + cotSea);
  view.slope(body, outer.xLand + cotLand * (crest - mid), mid, cotLand,
             0.22 * (crest - bed), "right", "1 : " + cotLand);

  legend(svg, keys, 52, 24);
  scaleBar(svg, view, 20, w - 190, h - 24);
  sheetFrame(svg, w, h, {
    bubble: "A", title: "Breakwater typical section",
    scale: "1:" + Math.round(view.scaleDenominator / 5) * 5 + " on screen"
  });
  return svg;
}

function stoneTexture(g, view, outer, inner, bed, Dn) {
  var band = el("g", { opacity: 0.55 }, g);
  var seed = 7;
  function rnd() { seed = (seed * 1103515245 + 12345) & 0x7fffffff; return seed / 0x7fffffff; }
  var steps = Math.min(48, Math.max(6, Math.round((outer.crest - bed) / Dn)));
  for (var face = 0; face < 2; face++) {
    for (var i = 0; i <= steps; i++) {
      var z = bed + (outer.crest - bed) * i / steps;
      var cot = face ? outer.cotLand : outer.cotSea;
      var sign = face ? 1 : -1;
      var xOuter = (face ? outer.xLand : outer.xSea) + sign * cot * (outer.crest - z);
      var xInner = (face ? inner.xLand : inner.xSea) + sign * cot * (inner.crest - z);
      if (z > inner.crest) continue;
      var n = Math.max(1, Math.round(Math.abs(xOuter - xInner) / Dn));
      for (var j = 0; j < n; j++) {
        var t = (j + 0.5) / n;
        var x = xOuter + (xInner - xOuter) * t;
        var r = 0.5 * Dn * (0.7 + 0.4 * rnd());
        el("circle", {
          cx: view.X(x).toFixed(1), cy: view.Y(z).toFixed(1),
          r: (r * view.s).toFixed(1), fill: "none", stroke: "#2f2d2a",
          "stroke-width": 0.5
        }, band);
      }
    }
  }
}

/* ------------------------------------------------------------------ */
/* Channel                                                             */
/* ------------------------------------------------------------------ */

function drawChannel(host, d, w, h, exaggeration) {
  var svg = newSheet(host, w, h);
  var wl = d.design_water_level;
  var bed = d.existing_bed === null ? d.dredge_level + 2 : d.existing_bed;
  var half = 0.5 * d.width;
  var rise = Math.max(bed - d.dredge_level, 0);
  var toe = half + d.side_slope * rise;
  var extent = toe + 70;
  var z0 = d.dredge_level - 6, z1 = wl + 0.5 * d.vessel.beam;

  var body = el("g", null, svg);
  var view = new View({ x: 30, y: 16, w: w - 50, h: h - 66 },
                      [-extent, extent], [z0, z1], exaggeration || 8);
  clipTo(svg, body, view.box);
  var keys = [];

  keys.push(view.poly(body, [
    [-extent, z0 - 10], [extent, z0 - 10], [extent, bed], [toe, bed],
    [half, d.dredge_level], [-half, d.dredge_level], [-toe, bed], [-extent, bed]
  ], "subgrade", "In-situ material"));
  keys.push(view.poly(body, [
    [-extent, wl], [extent, wl], [extent, bed], [toe, bed],
    [half, d.dredge_level], [-half, d.dredge_level], [-toe, bed], [-extent, bed]
  ], "water"));

  view.line(body, [[-toe, bed], [-half, d.dredge_level], [half, d.dredge_level],
                   [toe, bed]], { width: 2 });

  var lanes = d.width_result.lanes;
  var offsets = lanes === 1 ? [0] : [-0.25 * d.width, 0.25 * d.width];
  offsets.forEach(function (centre, i) {
    var hull = hullSection(d.vessel.beam, d.vessel.draught, 0.2 * d.vessel.beam, centre);
    hull = hull.map(function (p) { return [p[0], p[1] + wl]; });
    var k = view.poly(body, hull, "pavement", i ? null : "Design vessel");
    if (!i) keys.push(k);
  });

  view.level(body, -extent * 0.9, wl, "DWL " + fmt(wl) + " m CD", "water");
  view.level(body, 0, d.dredge_level, "Dredge " + fmt(d.dredge_level) + " m CD");
  if (d.existing_bed !== null) {
    view.level(body, -extent * 0.62, bed, "Bed " + fmt(bed) + " m CD");
  }
  view.dimH(body, -half, half, d.dredge_level - 2.0,
            "bed width " + Math.round(d.width) + " m",
            [d.dredge_level, d.dredge_level]);

  legend(svg, keys, 40, 24);
  scaleBar(svg, view, 100, w - 200, h - 24);
  sheetFrame(svg, w, h, {
    bubble: "A", title: "Navigation channel section",
    scale: "vertical exaggeration " + (exaggeration || 8) + " : 1"
  });
  return svg;
}

function hullSection(beam, draught, freeboard, centre) {
  var r = 0.18 * beam, half = 0.5 * beam;
  return [
    [centre - half - 0.03 * beam, freeboard], [centre - half, 0],
    [centre - half, -draught + r], [centre - half + r, -draught],
    [centre + half - r, -draught], [centre + half, -draught + r],
    [centre + half, 0], [centre + half + 0.03 * beam, freeboard]
  ];
}

/* ------------------------------------------------------------------ */
/* Charts, for the modules whose answer is a curve not a section       */
/* ------------------------------------------------------------------ */

function chartFrame(svg, box, xlabel, ylabel) {
  var g = el("g", null, svg);
  el("rect", { x: box.x, y: box.y, width: box.w, height: box.h,
               fill: "#ffffff", stroke: "#c9c7c0", "stroke-width": 1 }, g);
  var xt = el("text", {
    x: box.x + box.w / 2, y: box.y + box.h + 30, "text-anchor": "middle",
    "font-size": 10, fill: "#54514b",
    "font-family": "'IBM Plex Sans', system-ui, sans-serif"
  }, g);
  xt.textContent = xlabel;
  var yt = el("text", {
    x: box.x - 36, y: box.y + box.h / 2, "text-anchor": "middle",
    "font-size": 10, fill: "#54514b",
    "font-family": "'IBM Plex Sans', system-ui, sans-serif",
    transform: "rotate(-90 " + (box.x - 36) + " " + (box.y + box.h / 2) + ")"
  }, g);
  yt.textContent = ylabel;
  return g;
}

/* Negative zero reads as "-0" on an axis, which looks like a typo. */
function tickText(value, fmtFn) {
  var text = fmtFn ? fmtFn(value) : value.toFixed(0);
  return text === "-0" ? "0" : text;
}

function axis(g, box, lo, hi, horizontal, fmtFn) {
  var ticks = 5;
  for (var i = 0; i <= ticks; i++) {
    var f = i / ticks;
    var value = lo + (hi - lo) * f;
    if (horizontal) {
      var px = box.x + box.w * f;
      el("path", { d: "M" + px + "," + box.y + " V" + (box.y + box.h),
                   stroke: "#e6e4de", "stroke-width": 1 }, g);
      var t = el("text", { x: px, y: box.y + box.h + 14, "text-anchor": "middle",
                           "font-size": 9, fill: "#54514b",
                           "font-family": "'IBM Plex Mono', monospace" }, g);
      t.textContent = tickText(value, fmtFn);
    } else {
      var py = box.y + box.h * (1 - f);
      el("path", { d: "M" + box.x + "," + py + " H" + (box.x + box.w),
                   stroke: "#e6e4de", "stroke-width": 1 }, g);
      var u = el("text", { x: box.x - 6, y: py + 3, "text-anchor": "end",
                           "font-size": 9, fill: "#54514b",
                           "font-family": "'IBM Plex Mono', monospace" }, g);
      u.textContent = tickText(value, fmtFn);
    }
  }
}

function polyline(g, box, xs, ys, xlim, ylim, opts) {
  opts = opts || {};
  var d = "";
  for (var i = 0; i < xs.length; i++) {
    var px = box.x + box.w * (xs[i] - xlim[0]) / (xlim[1] - xlim[0]);
    var py = box.y + box.h * (1 - (ys[i] - ylim[0]) / (ylim[1] - ylim[0]));
    d += (i ? "L" : "M") + px.toFixed(1) + "," + py.toFixed(1);
  }
  el("path", { d: d, fill: "none", stroke: opts.stroke || "#0b3554",
               "stroke-width": opts.width || 1.8,
               "stroke-dasharray": opts.dash || null }, g);
  return d;
}

function fmt(v) { return (v >= 0 ? "+" : "") + v.toFixed(2); }

function roundScale(v) { return v; }

var DRAW = {
  drawSeawall: drawSeawall,
  drawBreakwater: drawBreakwater,
  drawChannel: drawChannel,
  newSheet: newSheet,
  chartFrame: chartFrame,
  axis: axis,
  polyline: polyline,
  el: el,
  sheetFrame: sheetFrame,
  MATERIALS: MATERIALS
};
if (typeof globalThis !== "undefined") globalThis.DRAW = DRAW;
