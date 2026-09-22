# `pyCoastal.plotting`

Source: [`pyCoastal/plotting.py`](../../pyCoastal/plotting.py)

Plot helpers shared by the examples.

Importing this module needs matplotlib, which is not a runtime dependency of
the package. Install it with the ``plots`` extra::

    pip install pyCoastal[plots]

The colour maps here are built to look like water rather than to be
perceptually uniform. For quantitative fields such as a disturbance
coefficient use ``agitation_colormap`` or a standard scientific map; keep
``water_colormap`` for the instantaneous surface, where the point is to read
the wave pattern at a glance.

## `LAND_COLOR`

```python
LAND_COLOR = '#6b6f73'
```

## `water_colormap`

```python
def water_colormap(name: str='pyCoastal_water') -> LinearSegmentedColormap
```

```text
Diverging map for instantaneous surface elevation.

Troughs run to deep navy, still water sits at a mid ocean blue, and
crests lift through turquoise to a pale foam white. Reading it as a
photograph of the sea surface: dark water in the hollows, light broken
water on the crests.
```

## `agitation_colormap`

```python
def agitation_colormap(name: str='pyCoastal_agitation') -> LinearSegmentedColormap
```

```text
Sequential map for wave height or disturbance coefficient.

Calm water is dark and quiet; agitation brightens through green to a hot
yellow, so the berths in trouble stand out.
```

## `surface_norm`

```python
def surface_norm(snapshots: np.ndarray, percentile: float=99.5) -> TwoSlopeNorm
```

```text
Symmetric colour scale centred on still water.

The limit comes from a high percentile rather than the maximum, so a
single sharp spike near a structure does not flatten the whole field.
```

## `land_overlay`

```python
def land_overlay(land: np.ndarray) -> np.ndarray
```

```text
Float array that is 1.0 on structures and NaN on water.

Draw it over a field with a solid colour map so breakwaters read as
material rather than as an extreme value of the field.
```

## `panel_labels`

```python
def panel_labels(axes, labels=None, loc: str='upper left', fontsize: float=10.0, offset: float=0.02)
```

```text
Label each panel of a multi-panel figure with (a), (b), (c), ...

The figures in ``examples/`` carry no titles. Panel letters identify the
panels, and the caption of the figure states what each one shows.

Parameters
----------
axes : sequence of matplotlib Axes
    Panels in reading order. A 2D array from ``plt.subplots`` is
    flattened.
labels : sequence of str, optional
    Replacement labels. Defaults to "(a)", "(b)", ...
loc : {"upper left", "upper right", "lower left", "lower right"}
    Corner of the panel, in axes coordinates.
offset : float
    Inset from the corner, as a fraction of the panel.

Returns
-------
list
    The created text artists.
```

