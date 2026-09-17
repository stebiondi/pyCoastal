import os
import sys
from datetime import datetime

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(".."))

project = "pyCoastal"
author = "Stefano Biondi"
copyright = f"{datetime.now().year}"
# Single source of truth is pyproject.toml, read through the installed
# package metadata so the docs cannot drift from the release.
try:
    from importlib.metadata import version as _version

    release = _version("pyCoastal")
except Exception:                      # not installed, e.g. a bare checkout
    release = "0.0.0"


extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosummary",
    "sphinx.ext.viewcode",
    "sphinx.ext.mathjax",
    "myst_parser"
]

autosummary_generate = True
autodoc_member_order = "bysource"

templates_path = ["_templates"]
exclude_patterns = []

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

myst_enable_extensions = [
    "dollarmath",
    "amsmath"
]
