# pycoastal/physics/shallow_water.py

import numpy as np

class ShallowWater2D:
    """
    2D nonlinear shallow water equations:
      ∂h/∂t + ∂(h u)/∂x + ∂(h v)/∂y = 0
      ∂(h u)/∂t + ∂(h u^2 + ½ g h^2)/∂x + ∂(h u v)/∂y = Sx
      ∂(h v)/∂t + ∂(h u v)/∂x + ∂(h v^2 + ½ g h^2)/∂y = Sy
    """
    def __init__(self, g: float = 9.81):
        self.g = g

    def fluxes(self, h: np.ndarray, hu: np.ndarray, hv: np.ndarray):
        """
        Compute the three flux‐pairs (in x and y) for the SWEs.
        Returns (Fh, Gh), (Fhu, Ghu), (Fhv, Ghv)
        """
        u = hu / h
        v = hv / h

        Fh  = hu
        Gh  = hv

        Fhu = hu * u + 0.5 * self.g * h**2
        Ghu = hu * v

        Fhv = hv * u
        Ghv = hv * v + 0.5 * self.g * h**2

        return (Fh, Gh), (Fhu, Ghu), (Fhv, Ghv)

    def source_bed_slope(self, h: np.ndarray, zb: np.ndarray, grid=None):
        """
        Return bed‐slope source terms Sx, Sy for momentum:
          Sx = - g h ∂zb/∂x,  Sy = - g h ∂zb/∂y

        x is axis 0 and y is axis 1. Pass ``grid`` (a UniformGrid) so the
        derivatives use the real cell spacing; without it the spacing is
        taken as unity, which is only correct on a unit mesh.
        """
        dx, dy = grid.spacing if grid is not None else (1.0, 1.0)
        dzdx = np.gradient(zb, dx, axis=0)
        dzdy = np.gradient(zb, dy, axis=1)
        Sx = - self.g * h * dzdx
        Sy = - self.g * h * dzdy
        return Sx, Sy

    # you can add friction, coriolis, rainfall, etc.

