# `pyCoastal.config`

Source: [`pyCoastal/config.py`](../../pyCoastal/config.py)

Configuration loader for pyCoastal.
Supports YAML, JSON, and INI-style files.

## `load_config`

```python
def load_config(path: str) -> dict
```

```text
Load a configuration file and return a dictionary.

Supported formats:
  - .yaml, .yml  (requires PyYAML)
  - .json
  - .ini, .cfg

Parameters
----------
path : str
    Path to the config file.

Returns
-------
dict
    Parsed configuration.
```

