/*
 * Interface language.
 *
 * Every piece of text the pages show passes through I18N.t(). The English
 * string is the key, so the code stays readable and a missing translation
 * falls back to English rather than to a blank.
 *
 * Most text is built from numbers: "Toe rock, Dn50 = 1.24 m". Before the
 * lookup, each free-standing number is replaced by a numbered slot, so the
 * key is "Toe rock, Dn50 = {0} m" and one entry covers every value. Digits
 * that belong to a symbol (Hm0, Dn50, M50, C35) stay part of the key. The
 * translation may move the slots; the numbers are put back unchanged,
 * with a decimal point in every language, as on a drawing.
 *
 * The dictionaries are lang/es.js and lang/zh.js. webapp/i18n_check.py runs
 * the whole app through its inputs and lists any key without a
 * translation. The literature itself (PyCoaPedia claims, synthesis and
 * paper titles) is not translated: it is quoted from English sources.
 */

(function () {
  var NAMES = { en: "English", es: "Español", zh: "中文" };
  var DICT = { en: {} };
  var listeners = [];
  var recorded = null;

  var NUM = /(^|[^A-Za-z0-9_.])([-+−]?\d+(?:\.\d+)?(?:e[-+]?\d+)?)/g;

  function template(text) {
    var nums = [];
    var key = text.replace(NUM, function (all, lead, num) {
      nums.push(num);
      return lead + "{" + (nums.length - 1) + "}";
    });
    return { key: key, nums: nums };
  }

  /* Text with no word in it (a bare value, a unit after a value) is the
     same in every language and is not looked up. */
  function wordy(key) {
    var words = key.replace(/\{\d+\}/g, " ").match(/[A-Za-z]{2,}/g) || [];
    var units = /^(m|s|kn|kPa|kN|kNm|MNm|deg|yr|CD|kg|t|mm|Pa|FoS|Kr|Ucw|KC|KD|Hs|Hm|Tp|Rc|Cd|Cm|Dn|D|L|H|h|B|e|m3|m2|l|Ed|M_Ed|V_Ed|phi|Um|pu|pb|Fh|Ru|nan|Infinity)$/;
    return words.some(function (w) { return !units.test(w); });
  }

  function lookup(dict, text) {
    if (dict.hasOwnProperty(text)) return dict[text];
    var tp = template(text);
    if (dict.hasOwnProperty(tp.key)) return fill(dict[tp.key], tp.nums);
    return null;
  }

  function fill(pattern, nums) {
    return pattern.replace(/\{(\d+)\}/g, function (all, i) {
      return nums[+i] !== undefined ? nums[+i] : all;
    });
  }

  function initial() {
    var wanted = null;
    try {
      var m = /[?&]lang=([a-z]{2})/.exec(location.search);
      if (m) wanted = m[1];
    } catch (e) { /* no location */ }
    if (!wanted) {
      try { wanted = localStorage.getItem("pycoastal-lang"); } catch (e) { /* storage blocked */ }
    }
    if (!wanted) {
      try { wanted = (navigator.language || "en").slice(0, 2).toLowerCase(); } catch (e) { /* none */ }
    }
    return NAMES[wanted] ? wanted : "en";
  }

  var I18N = {
    names: NAMES,
    lang: "en",

    add: function (lang, dict) {
      DICT[lang] = DICT[lang] || {};
      for (var k in dict) if (dict.hasOwnProperty(k)) DICT[lang][k] = dict[k];
    },

    t: function (text) {
      if (text === null || text === undefined || text === "") return text;
      text = String(text);
      // Report rows indent their sub-items; the indent is kept, not looked up.
      var indent = /^\s*/.exec(text)[0];
      if (indent) return indent + I18N.t(text.slice(indent.length));
      var tp = template(text);
      if (!wordy(tp.key)) return text;
      if (recorded) recorded[tp.key] = true;
      var dict = DICT[I18N.lang];
      if (!dict || I18N.lang === "en") return text;
      var whole = lookup(dict, text);
      if (whole !== null) return whole;
      // A list joined with "; " (the out-of-range parameters of a relation)
      // is translated part by part, when every part has an entry.
      if (text.indexOf("; ") > 0) {
        var parts = text.split("; ").map(function (p) { return lookup(dict, p); });
        if (parts.every(function (p) { return p !== null; })) {
          return parts.join(dict["; "] || "; ");
        }
      }
      return text;
    },

    /* Whether a recorded key has a translation, whole or part by part. */
    covered: function (lang, key) {
      var dict = DICT[lang] || {};
      if (dict.hasOwnProperty(key)) return true;
      if (key.indexOf("; ") < 0) return false;
      return key.split("; ").every(function (p) {
        var n = 0;
        return dict.hasOwnProperty(p.replace(/\{\d+\}/g, function () { return "{" + (n++) + "}"; }));
      });
    },

    /* Static markup: data-i18n translates the text, data-i18n-title,
       data-i18n-aria and data-i18n-placeholder the attributes. The English
       is kept on the element, so switching back and forth is lossless. */
    apply: function (root) {
      root = root || document;
      var nodes = root.querySelectorAll("[data-i18n], [data-i18n-title], " +
                                        "[data-i18n-aria], [data-i18n-placeholder]");
      Array.prototype.forEach.call(nodes, function (n) {
        if (n.hasAttribute("data-i18n")) {
          if (!n.dataset.en) n.dataset.en = n.textContent.replace(/\s+/g, " ").trim();
          n.textContent = I18N.t(n.dataset.en);
        }
        [["data-i18n-title", "title"], ["data-i18n-aria", "aria-label"],
         ["data-i18n-placeholder", "placeholder"]].forEach(function (pair) {
          if (n.hasAttribute(pair[0])) {
            n.setAttribute(pair[1], I18N.t(n.getAttribute(pair[0])));
          }
        });
      });
      document.documentElement.setAttribute("lang", I18N.lang === "zh" ? "zh-Hans" : I18N.lang);
    },

    set: function (lang) {
      if (!NAMES[lang]) lang = "en";
      I18N.lang = lang;
      try { localStorage.setItem("pycoastal-lang", lang); } catch (e) { /* storage blocked */ }
      if (typeof document !== "undefined" && document.querySelectorAll) I18N.apply();
      listeners.forEach(function (fn) { fn(lang); });
    },

    onChange: function (fn) { listeners.push(fn); },

    /* A <select> that switches the language, for the page header. */
    picker: function (host) {
      var sel = document.createElement("select");
      sel.className = "lang-picker";
      sel.setAttribute("aria-label", "Language");
      Object.keys(NAMES).forEach(function (code) {
        var o = document.createElement("option");
        o.value = code;
        o.textContent = NAMES[code];
        if (code === I18N.lang) o.selected = true;
        sel.appendChild(o);
      });
      sel.addEventListener("change", function () { I18N.set(sel.value); });
      host.appendChild(sel);
      return sel;
    },

    /* Harvest support for i18n_check.py. */
    record: function () { recorded = {}; },
    recorded: function () { return Object.keys(recorded || {}).sort(); },
    missing: function (lang) {
      var dict = DICT[lang] || {};
      return I18N.recorded().filter(function (k) { return !I18N.covered(lang, k); });
    },
    dictionary: function (lang) { return DICT[lang] || {}; },
    keyOf: function (text) { return template(String(text)).key; }
  };

  I18N.lang = initial();
  globalThis.I18N = I18N;
  globalThis.T = function (text) { return I18N.t(text); };
})();
