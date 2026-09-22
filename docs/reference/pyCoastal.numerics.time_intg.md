# `pyCoastal.numerics.time_intg`

Source: [`pyCoastal/numerics/time_intg.py`](../../pyCoastal/numerics/time_intg.py)

## `euler_step`

```python
def euler_step(u, t, dt, rhs)
```

```text
Forward Euler scheme (1st-order). u_{n+1} = u_n + dt * rhs(u_n, t)
Parameters:
    u   : 2D numpy array, current solution field
    t   : float, current time
    dt  : float, time step size
    rhs : function(u, t) -> 2D array of same shape as u, computes time derivative
Returns:
    u_new : 2D array, solution at t + dt
```

## `rk2_step`

```python
def rk2_step(u, t, dt, rhs)
```

```text
Heun's method / explicit midpoint (2nd-order Runge-Kutta).
k1 = rhs(u, t)
k2 = rhs(u + dt * k1, t + dt)
u_{n+1} = u_n + (dt/2) * (k1 + k2)
```

## `rk4_step`

```python
def rk4_step(u, t, dt, rhs)
```

```text
Classic 4th-order Runge-Kutta.
k1 = rhs(u, t)
k2 = rhs(u + dt/2 * k1, t + dt/2)
k3 = rhs(u + dt/2 * k2, t + dt/2)
k4 = rhs(u + dt * k3, t + dt)
u_{n+1} = u_n + dt/6 * (k1 + 2*k2 + 2*k3 + k4)
```

## `ab2_step`

```python
def ab2_step(u, u_prev, t, dt, rhs)
```

```text
Second-order Adams-Bashforth.
Requires solution at two previous times: u_n and u_{n-1}.
u_{n+1} = u_n + dt * (3/2 * rhs(u_n,t) - 1/2 * rhs(u_{n-1}, t-dt))
```

## `rk3_ssp_step`

```python
def rk3_ssp_step(u, t, dt, rhs)
```

```text
Strong Stability-Preserving 3rd-order Runge-Kutta (SSP RK3).
Stage 1: u1 = u + dt * rhs(u, t)
Stage 2: u2 = 0.75 u + 0.25 (u1 + dt * rhs(u1, t+dt))
Stage 3: u_{n+1} = (1/3) u + (2/3) (u2 + dt * rhs(u2, t+0.5*dt))
```

