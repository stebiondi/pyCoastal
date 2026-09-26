"""
List every interface string the pages show, and the ones without a translation.

The strings are collected by running the page scripts in QuickJS behind the
stub DOM of ``verify_app.py``: every design module is run through its
defaults, the ends of each slider, every option of each list and a set of
random combinations, so the warnings that only appear at the edges of the
input range are reached too. The static markup (``data-i18n`` in
``index.html``) and literal ``T("...")`` calls are added
from the source.

    python webapp/i18n_check.py            # counts, and missing keys per language
    python webapp/i18n_check.py --dump     # write lang/keys.json, all keys

Exit status 1 when a language misses a key, so the tests can call it.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from verify_app import DOM_STUB  # noqa: E402

LANGS = ("es", "zh")
SCRIPTS = ("i18n.js", "lang/es.js", "lang/zh.js", "engine.js", "draw.js", "app.js")

EXTRA = [
    "Depth is only {0} times the draught. Squat and manoeuvrability both "
    "degrade sharply below about {1}.",
]

SWEEP = """
// The stub DOM of verify_app.py, extended with what the checks table and
// the drawing guard in run() need.
var __make = makeNode;
makeNode = function (tag) {
  var n = __make(tag);
  n.firstChild = {};
  n.hasAttribute = function () { return false; };
  n.createTHead = function () { return makeNode("thead"); };
  n.createTBody = function () { return makeNode("tbody"); };
  n.insertRow = function () { return makeNode("tr"); };
  n.insertCell = function () { return makeNode("td"); };
  return n;
};
function lcg(seed) {
  return function () { seed = (seed * 1103515245 + 12345) % 2147483648; return seed / 2147483648; };
}

function sweep(knowledgeJson, samples) {
  I18N.record();
  var rand = lcg(7);
  var names = Object.keys(MODULES);
  names.forEach(function (name) {
    selectModule(name);
    var inputs = MODULES[name].inputs;
    var defaults = inputs.map(function (i) { return i.value; });
    function reset() { inputs.forEach(function (inp, k) { inp.value = defaults[k]; }); }
    // One input at a time: ends of each slider, every option, both toggles.
    inputs.forEach(function (inp) {
      var trial = inp.type === "select" ? inp.options
        : inp.type === "toggle" ? [true, false] : [inp.min, inp.max];
      trial.forEach(function (value) { reset(); inp.value = value; run(); });
    });
    // Random combinations.
    for (var s = 0; s < samples; s++) {
      inputs.forEach(function (inp) {
        if (inp.type === "select") inp.value = inp.options[Math.floor(rand() * inp.options.length)];
        else if (inp.type === "toggle") inp.value = rand() < 0.5;
        else inp.value = Math.round((inp.min + rand() * (inp.max - inp.min)) / inp.step) * inp.step;
      });
      run();
    }
    reset();
    run();
  });
  renderInputs();
  STATE.verified = { failed: 0, total: 642 };
  renderVerification();
  STATE.verified = { failed: 3, total: 642, first: null };
  renderVerification();
  if (knowledgeJson) {
    STATE.knowledge = JSON.parse(knowledgeJson);
    showCorpusStat();
    names.forEach(function (name) {
      STATE.module = name;
      var key = MODULE_TO_KEY[name];
      (STATE.knowledge.modules[key] || { topics: [] }).topics.forEach(function (tid) {
        if (!STATE.knowledge.topics[tid]) return;
        STATE.topic = tid;
        renderKnowledge();
      });
    });
  }
  return JSON.stringify(I18N.recorded());
}
"""


def static_keys(context) -> set[str]:
    """data-i18n markup and literal T("...") calls, keyed as I18N keys them."""
    raw: set[str] = set()
    for page in ("index.html",):
        html = (HERE / page).read_text(encoding="utf-8")
        for m in re.finditer(r"<[^>]*\sdata-i18n(?:\s[^>]*)?>(.*?)</", html, re.S):
            raw.add(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(1))).strip()
                    .replace("&hellip;", "…").replace("&amp;", "&"))
        for attr in ("title", "aria", "placeholder"):
            raw.update(re.findall(rf'data-i18n-{attr}="([^"]+)"', html))
    for name in ("app.js", "draw.js"):
        src = (HERE / name).read_text(encoding="utf-8")
        for lit in re.findall(r'\bT\("((?:[^"\\]|\\.)*)"\)', src):
            raw.add(json.loads(f'"{lit}"'))
    keys = set()
    for text in raw:
        if text:
            context.eval("I18N.record()")
            context.eval(f"I18N.t({json.dumps(text)})")
            keys.update(json.loads(context.eval("JSON.stringify(I18N.recorded())")))
    return keys


def collect(samples: int = 40) -> tuple[list[str], object]:
    import quickjs

    context = quickjs.Context()
    context.eval("var globalThis = this;")
    context.eval(DOM_STUB)
    context.eval("var history = {}; var location = { hash: '', search: '' };")
    for name in SCRIPTS:
        path = HERE / name
        if path.exists():
            context.eval(path.read_text(encoding="utf-8"))
    context.eval(SWEEP)
    knowledge = HERE / "knowledge.json"
    kjson = knowledge.read_text(encoding="utf-8") if knowledge.exists() else ""
    keys = set(json.loads(context.get("sweep")(kjson, samples)))
    keys |= static_keys(context)
    # Warnings the sweep does not reach, keyed by hand.
    keys |= set(EXTRA)
    return sorted(keys), context


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--dump", action="store_true", help="write lang/keys.json")
    parser.add_argument("--samples", type=int, default=40)
    args = parser.parse_args()
    try:
        keys, context = collect(args.samples)
    except ImportError:
        print("quickjs is not installed. pip install quickjs")
        return 2
    print(f"{len(keys)} interface strings")
    if args.dump:
        (HERE / "lang" / "keys.json").write_text(
            json.dumps(keys, ensure_ascii=False, indent=1), encoding="utf-8")
    bad = 0
    for lang in LANGS:
        missing = [k for k in keys
                   if not context.eval(f"I18N.covered('{lang}', {json.dumps(k)})")]
        print(f"  {lang}: {len(keys) - len(missing)}/{len(keys)} translated")
        for k in missing[:40]:
            print(f"     missing: {k}")
        if len(missing) > 40:
            print(f"     ... and {len(missing) - 40} more")
        bad += bool(missing)
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
