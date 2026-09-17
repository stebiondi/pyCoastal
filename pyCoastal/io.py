# pycoastal/io.py

import os, json, yaml
from configparser import ConfigParser

def read_data(path: "str | os.PathLike") -> dict:
    """
    Read a YAML, JSON or INI file and return a python dict.

    Accepts a Path as well as a string, so a caller can resolve the file
    relative to its own location rather than to the shell's directory.
    """
    ext = os.path.splitext(path)[1].lower()
    with open(path, 'r') as f:
        if ext in ('.yaml','.yml'):
            return yaml.safe_load(f)
        elif ext == '.json':
            return json.load(f)
        elif ext == '.ini':
            cfg = ConfigParser()
            cfg.read_file(f)
            return {s: dict(cfg[s]) for s in cfg.sections()}
    raise ValueError(f"Unknown file extension: {ext}")

def write_vtk(grid, filename: str):
    """
    Write a vtkUnstructuredGrid (or similar) to a .vtk file.
    """
    try:
        import vtk
    except ImportError:
        raise ImportError("VTK bindings not installed")
    writer = vtk.vtkUnstructuredGridWriter()
    writer.SetFileName(filename)
    writer.SetInputData(grid)
    writer.Write()
