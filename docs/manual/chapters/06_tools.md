# Part III. Engineering tools {.part .unnumbered}

# Standalone formulae: `pyCoastal.tools` {#sec:tools}

`pyCoastal.tools` collects standalone coastal engineering formulae. Every
function takes its parameters explicitly, with no hidden hard-coded values,
so defaults can be set or overridden from a case file. These are the first
checks an engineer runs; the design applications of Part IV build full
design chains on top of the same relations, with validity checks and
reporting. Where a tool and an application overlap, prefer the
application for design.

## Waves: `tools.wave` {#sec:tools-wave}

### Linear dispersion and derived numbers

Under linear (small-amplitude) theory, frequency, wavenumber, and depth are
linked by the dispersion relation, which sets the phase and group speeds and
underpins most coastal scalings:

$$ \omega^2 = g k\tanh(kh),\qquad c = \frac{\omega}{k},\qquad c_g = \frac{c}{2}\left(1 + \frac{2kh}{\sinh 2kh}\right). $$ {#eq:dispersion}

`dispersion(T, h, g=9.81, tol=1e-12)` solves it for the wavelength $L$ by
Newton iteration and raises on a non-positive period or depth;
`wave_number(T, h)` returns $k = 2\pi/L$. The deep-water wavelength is
$L_0 = gT^2/(2\pi)$.

Two nondimensional numbers classify the waves:

- **Iribarren (surf similarity)**, $\xi_0 = \tan\beta/\sqrt{H_0/L_0}$:
  `surf_similarity(alpha, H, T)` returns it and `breaker_type(alpha, H, T)`
  names the breaker, spilling for $\xi < 0.4$, plunging for
  $0.4 \le \xi \le 2$, and collapsing or surging above 2.
- **Ursell**, $U = HL^2/h^3$: `ursell_number(H, T, h)` returns the value and
  an interpretation, linear theory for $U < 32$ and a nonlinear theory
  (Stokes, Boussinesq) above.

`wave_setup(Hb, gamma=0.8)` gives the shoreline setup
$\bar\eta = \tfrac{5}{16}\gamma H_b$.

### Spectral synthesis

A wave spectrum describes how the energy of a sea state is distributed over
frequency. To drive a numerical flume with irregular seas, a surface
elevation record is synthesized by random-phase superposition consistent
with a target spectrum:

$$ \eta(t) = \sum_{i=1}^{N}\sqrt{2S(f_i)\,\Delta f}\,\cos(2\pi f_i t + \varphi_i),\qquad \varphi_i \sim U[0, 2\pi]. $$ {#eq:synthesis}

The spectral moments $m_n = \int_0^\infty f^n S(f)\,\mathrm{d}f$ give
$H_s \approx 4\sqrt{m_0}$ and $T_z \approx \sqrt{m_0/m_2}$.
`generate_irregular_wave(Hs, Tp, duration, dt, spectrum="pm", gamma=3.3)`
returns `(t, eta)` for a Pierson-Moskowitz (fully developed) or JONSWAP
(fetch-limited, peak enhancement `gamma`) spectrum scaled to the requested
$H_s$.

## Sediment transport: `tools.sediment_transport`

The Shields parameter gauges bed mobility under a bed shear stress
$\tau_b = \rho u_*^2$:

$$ \theta = \frac{\tau_b}{(\rho_s - \rho)\,g\,d}, $$ {#eq:shields}

with a critical value $\theta_c \approx$ 0.03 to 0.06 for sand (the design
modules compute it from the grain size, @sec:sediment). The transport
formulae in @tbl:transport convert mobility into rates.

: Transport relations in `pyCoastal.tools.sediment_transport`. {#tbl:transport}

| Function | Relation |
|----------|----------|
| `shields_parameter(tau_b, rho_s, rho, d)` | @eq:shields |
| `van_rijn_bedload(Ue, h, d50, rho_s, rho)` | $q_b = 0.015\rho_s U_e h (d_{50}/h)^{1.2} M_e^{1.5}$, $M_e = (U_e - U_{cr})/\sqrt{(s-1)g d_{50}}$ (Van Rijn 1984) |
| `van_rijn_suspended(Ue, h, d50, rho_s, rho)` | $q_s = 0.008\rho_s U_e d_{50} M_e^{2.4} D_*^{-0.6}$ |
| `bijker_bedload(tau_wave, tau_current, rho_s, rho, d50)` | $\propto\sqrt{\tau_\mathrm{total}}$, waves and current combined (Bijker 1971) |
| `cerc_transport(Eb, angle, K=0.39)` | $Q = K\,E_b/(\rho g)\,\sin\varphi_b\cos\varphi_b$ (CERC) |
| `bagnold_sediment(H, c, rho_s)` | $(\rho_s/\rho)\,H^2 c$, energetics estimate |
| `izbash_current(rho_s, rho, d)` | $u_c = 1.7\sqrt{\Delta g d}$, stone stability in current |
| `einstein_bedload(tau_star, d, s)` | $q_b = 8\sqrt{g(s-1)d^3}\,\tau_*^{1.5}$ |

The critical velocity in the Van Rijn functions is
$U_{cr} = 0.19\,d_{50}^{0.1}\log(12h/3d_{50})$ and $s = \rho_s/\rho$.

## Structures and runup: `tools.structural`

- `hudson_dn50(Hs, Delta, theta, Kd=3.0)`:
  $H_s/(\Delta D_{n50}) = (K_D\cot\theta)^{1/3}/1.27$ (SPM 1984).
- `vandermeer_dn50(Hs, Delta, P, N, alpha, xi_m, damage=2.0, safety=1.0)`:
  Van der Meer (1988), plunging and surging branches (@eq:vdm-plunging and
  @eq:vdm-surging in @sec:structures), with the wave count saturating at
  7500. The surf similarity must be supplied, because it depends on the
  period.
- `hunt_runup(beta, H, L)`: $R \approx H\tan\beta/\sqrt{H/L}$ (Hunt 1959).
- `stockdon_runup(H, L, beta)`: the Stockdon et al. (2006) 2% runup.
- `goda_wave_force(H, T, h, beta)`: a screening estimate of the Goda
  horizontal force on a vertical face, in N/m, taking
  $H_\mathrm{design} = 1.8H$. The full Goda distribution with uplift and
  stability checks is `applications.seawall.goda_pressures` (@sec:seawall).
- `iribarren_stability(H, alpha, rho_s, rho_w, mu, N)`: the Iribarren stone
  weight, $W \ge N\rho_s g H^3/[\Delta^3(\mu\cos\alpha - \sin\alpha)^3]$.

## One-line shoreline model: `tools.shoreline` {#sec:tools-oneline}

The one-line model treats the shoreline position $y(x, t)$ as the only
morphological variable and conserves sediment alongshore:

$$ \frac{\partial y}{\partial t} = -\frac{1}{(1-p)D}\frac{\partial Q_{ls}}{\partial x},\qquad
Q_{ls} = K_\mathrm{cerc}H_b^{5/2}\sin(2\alpha_b),\qquad \alpha_b = \alpha_0 - \frac{\partial y}{\partial x}, $$ {#eq:oneline}

with $H_b = K_d K_t H_\mathrm{free}$, where $K_d$ is a diffraction shadow
factor and $K_t$ a transmission factor. The explicit scheme is stable for

$$ \Delta t \le 0.45\,\frac{\Delta x^2}{\max G},\qquad G = \frac{2K_\mathrm{cerc}H_b^{5/2}}{(1-p)D}. $$ {#eq:oneline-dt}

`OneLineParams(D=8, p=0.4, Kcerc=0.4, Hfree=1.0, alpha0=10 deg, Kt=1.0,
beta0=-30 deg, morfac=1.0)` holds the parameters; any of `Hfree`,
`alpha0`, `Kt` can be arrays over $x$. The building blocks are
`make_grid(Lx, dx)`, `breakwaters_geometry(x, tips, y_tip, crest_freeboard)`
for any number of detached breakwaters, `kd_diffraction_field(x, geom,
beta0)` for a simple shadow factor
$K_d = \tfrac12(1 + \cos\theta)$ from each tip, `compute_flux_Qls`,
`rhs_y_t`, `suggest_dt`, and `apply_bcs(y, bc="fixed_ends" | "zero_slope")`.
`run_one_line_model()` runs a default two-breakwater case. The nourishment
application (@sec:nourishment) drives this solver with a fill planform.

## Morphodynamics helpers: `tools.morphodynamics` {#sec:tools-morpho}

- `bruuns_rule(S, beta, L=None, h=None, B=None)`: shoreline retreat under
  sea-level rise $S$, $R = SL/(h + B)$ when the profile length, closure
  depth, and berm height are given, and $R = S/\tan\beta$ otherwise.
- `exner_change(qs_dx, porosity=0.64)`: bed change rate from the transport
  divergence, $\partial\eta/\partial t = -q_{s,x}/(1-n)$.
- `linear_slope(grid, north_level, south_level)`: a plane beach on a grid.
- `circle_through_points`, `two_point_arc`, and `build_tombolo_arcs(Lshore,
  Gb, Lb1, Lb2, yb, ...)`: the three-arc equilibrium planform behind a pair
  of detached breakwaters used by `examples/equilibrium_shoreline.py`, with
  retreat $Y_e = 1.204Y_i - 0.07G_b$ below the breakwater line;
  `accretion_metrics(x_eq, y_eq, geom)` returns the retreat and the
  accretion percentage.
