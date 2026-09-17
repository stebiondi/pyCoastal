"""Shared test setup."""

import pytest


@pytest.fixture(autouse=True)
def close_figures():
    """Close every matplotlib figure a test leaves behind.

    The drawing tests build a figure each, and pyplot keeps them alive until
    closed. Without this the suite trips matplotlib's open-figure warning and
    slowly eats memory.
    """
    yield
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return
    plt.close("all")
