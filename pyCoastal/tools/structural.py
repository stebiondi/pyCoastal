# structural.py
import numpy as np
import math
from .wave import surf_similarity

def hudson_dn50(Hs: float, Delta: float, theta: float, Kd: float = 3.0) -> float:
    """
    Calculate nominal diameter Dn50 for armor stone using Hudson's formula.
    Hs/(Δ Dn50) = (Kd cotθ)^(1/3) / 1.27
    """
    return Hs / (Delta * ((Kd * 1/math.tan(theta))**(1/3)) / 1.27)

def vandermeer_dn50(
    Hs: float,
    Delta: float,
    P: float,
    N: int,
    alpha: float,
    xi_m: float,
    damage: float = 2.0,
    safety: float = 1.0,
) -> float:
    """
    Nominal armour diameter Dn50 from Van der Meer (1988).

    plunging (xi_m < xi_cr)
        Hs / (Delta Dn50) = 6.2 P^0.18 (S / sqrt(N))^0.2 xi_m^-0.5
    surging (xi_m >= xi_cr)
        Hs / (Delta Dn50) = 1.0 P^-0.13 (S / sqrt(N))^0.2 sqrt(cot a) xi_m^P

    Args:
        Hs: significant wave height at the toe (m)
        Delta: relative buoyant density, rho_s/rho_w - 1
        P: notional permeability (0.1 impermeable to 0.6 very permeable)
        N: number of waves in the design storm, saturating near 7500
        alpha: slope angle (rad)
        xi_m: surf similarity parameter. Required: it depends on the wave
            period, which this function has no other way to know.
        damage: damage level S = A_e / Dn50^2. 2 is start of damage.
        safety: divides the stability coefficients, so >1 gives larger stone.

    Returns:
        float: nominal diameter Dn50 (m)

    Note:
        For a full design, including the crest level and overtopping checks,
        use ``pyCoastal.applications.structures``.
    """
    if damage <= 0:
        raise ValueError(f"Damage level S must be positive, got {damage}")
    if N <= 0:
        raise ValueError(f"Wave count must be positive, got {N}")

    cp, cs = 6.2 / safety, 1.0 / safety
    xi_cr = ((cp / cs) * (P**0.31) * math.sqrt(math.tan(alpha))) ** (1 / (P + 0.5))
    damage_term = (damage / math.sqrt(min(N, 7500))) ** 0.2

    if xi_m < xi_cr:
        denom = cp * (P**0.18) * damage_term * (xi_m**-0.5)
    else:
        denom = (
            cs * (P**-0.13) * damage_term
            * math.sqrt(1 / math.tan(alpha)) * (xi_m**P)
        )
    return Hs / (Delta * denom)
    
def hunt_runup(beta: float, H: float, L: float) -> float:
    """
    Hunt (1959) empirical run-up:
    R ≈ H * (tan beta) / sqrt(H / L)
    """
    return H * np.tan(beta) / np.sqrt(H / L)

def stockdon_runup(H: float, L: float, beta: float) -> float:
    """
    Stockdon et al. (2006) 2%-exceedance run-up:
    R2 = 1.1*(0.35 H xi) + 0.55*(0.75 H xi)
    where xi = tan beta / sqrt(H/L)
    """
    xi = np.tan(beta) / np.sqrt(H / L)
    eta_u = 0.35 * H * xi
    S_w = 0.75 * H * xi
    return 1.1 * (eta_u + 0.5 * np.sqrt(S_w**2 + (0.06*np.sqrt(H*L))**2))
    
def goda_wave_force(H: float, T: float, h: float, beta: float, rho: float = 1025) -> float:
    """
    Estimate the Goda–Takahashi equivalent-static horizontal wave force per unit width (kN/m)
    acting on a vertical breakwater face using Goda's method.

    Args:
        H (float): Significant wave height at wall (m)
        T (float): Wave period (s)
        h (float): Water depth at face (m)
        beta (float): Wave incidence angle (radians)
        rho (float): Water density (kg/m³) [default: 1025 for seawater]

    Returns:
        float: Estimated wave force per unit width (N/m)
    """
    # Design wave height H_design ≈ 1.8 × H (common assumption per Goda)
    H_design = 1.8 * H

    # Pressure distribution height limit ~0.75 H_design above SWL
    p_max = 0.5 * rho * 9.81 * H_design * (1 + math.cos(beta))

    # Linear pressure decrease to z = ±0.75 H_design
    z_limit = 0.75 * H_design

    # Equivalent static force per unit width (area of triangle): F = p_max * z_limit
    F = p_max * z_limit  # N/m

    return F
    
def iribarren_stability(H: float, alpha: float, rho_s: float, rho_w: float, mu: float, N: float) -> float:
    """
    Stone weight W needed for armor stability per Iribarren:
      W ≥ [N ρ_s g H^3] / [Δ^3 (μ cosα − sinα)^3]
    where Δ = (ρ_s/ρ_w − 1), N is safety coefficient,
    μ is friction coefficient, α is slope angle (rad).
    """
    Delta = rho_s/rho_w - 1
    numerator = N * rho_s * 9.81 * H**3
    denom = (Delta**3) * (mu * math.cos(alpha) - math.sin(alpha))**3
    return numerator / denom
