"""PyCoaTools interface translations: every string the app shows has one."""

import importlib.util
import json
import re
from pathlib import Path

import pytest

WEBAPP = Path(__file__).resolve().parents[1] / "webapp"

pytest.importorskip("quickjs")


def _load(name):
    spec = importlib.util.spec_from_file_location(name, WEBAPP / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_every_interface_string_is_translated():
    check = _load("i18n_check")
    keys, context = check.collect(samples=5)
    assert len(keys) > 400
    for lang in check.LANGS:
        missing = [k for k in keys
                   if not context.eval(f"I18N.covered('{lang}', {json.dumps(k)})")]
        assert not missing, f"{lang}: {missing[:10]}"


def test_translations_keep_their_number_slots():
    text = (WEBAPP / "lang" / "strings.txt").read_text(encoding="utf-8")
    blocks = [b.splitlines() for b in re.split(r"\n\s*\n", text)]
    blocks = [[l for l in b if not l.startswith("#")] for b in blocks]
    blocks = [b for b in blocks if b]
    for block in blocks:
        assert len(block) == 3, block
        slots = sorted(re.findall(r"\{\d+\}", block[0]))
        for line in block[1:]:
            assert sorted(re.findall(r"\{\d+\}", line)) == slots, block


def test_numbers_pass_through_unchanged():
    import quickjs

    context = quickjs.Context()
    context.eval("var globalThis = this;")
    for name in ("i18n.js", "lang/es.js", "lang/zh.js"):
        context.eval((WEBAPP / name).read_text(encoding="utf-8"))
    context.eval("I18N.lang = 'zh';")
    out = context.eval('I18N.t("Toe berm, Dn50 = 0.78 m (1.2 t), both toes")')
    assert "0.78" in out and "1.2" in out and "Dn50" in out
    context.eval("I18N.lang = 'es';")
    assert context.eval('I18N.t("  friction angle")') == "  ángulo de rozamiento"
    assert context.eval('I18N.t("12.3 t")') == "12.3 t"
