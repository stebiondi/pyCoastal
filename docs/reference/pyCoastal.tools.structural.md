# `pyCoastal.tools.structural`

Source: [`pyCoastal/tools/structural.py`](../../pyCoastal/tools/structural.py)

## `hudson_dn50`

```python
def hudson_dn50(Hs: float, Delta: float, theta: float, Kd: float=3.0) -> float
```

```text
Calculate nominal diameter Dn50 for armor stone using Hudson's formula.
Hs/(Δ Dn50) = (Kd cotθ)^(1/3) / 1.27
```

## `vandermeer_dn50`

```python
def vandermeer_dn50(Hs: float, Delta: float, P: float, N: int, alpha: float, xi_m: float, damage: float=2.0, safety: float=1.0) -> float
```

```text
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
```

## `hunt_runup`

```python
def hunt_runup(beta: float, H: float, L: float) -> float
```

```text
Hunt (1959) empirical run-up:
R ≈ H * (tan beta) / sqrt(H / L)
```

## `stockdon_runup`

```python
def stockdon_runup(H: float, L: float, beta: float) -> float
```

```text
Stockdon et al. (2006) 2%-exceedance run-up:
R2 = 1.1*(0.35 H xi) + 0.55*(0.75 H xi)
where xi = tan beta / sqrt(H/L)
```

## `goda_wave_force`

```python
def goda_wave_force(H: float, T: float, h: float, beta: float, rho: float=1025) -> float
```

```text
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
```

## `iribarren_stability`

```python
def iribarren_stability(H: float, alpha: float, rho_s: float, rho_w: float, mu: float, N: float) -> float
```

```text
Stone weight W needed for armor stability per Iribarren:
  W ≥ [N ρ_s g H^3] / [Δ^3 (μ cosα − sinα)^3]
where Δ = (ρ_s/ρ_w − 1), N is safety coefficient,
μ is friction coefficient, α is slope angle (rad).
```

