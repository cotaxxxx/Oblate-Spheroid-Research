# Meridian off-axis stationary-point diagnostic — specification

Status: `DIAGNOSTIC_ONLY / NOT_BINDING / PRE_THEOREM_SCAN`

Purpose: determine the qualitative stationary-point structure before fixing the global oblate theorem. This scan is not a certification and must not be cited as proof.

## Geometry and coordinates

Oblate spheroid

```text
K_lambda = { x^2 + y^2 + z^2/lambda^2 <= 1 },  0 < lambda <= 1.
```

By O(2) rotation symmetry and z -> -z reflection, every off-axis orbit has a representative in the half meridian y=0, x=r>0, z>=0.

Use interior-adapted search coordinates

```text
p(q,theta) = (q sin(theta), 0, lambda q cos(theta)),
0 < q < 1,
0 <= theta <= pi/2.
```

Thus q is the normalized ellipsoidal radius. The axis is theta=0; the equatorial plane is theta=pi/2. Off-axis means q>0 and theta>0.

## Surface parameterization

Let mu in [-1,1], phi in [0,2pi), a = sqrt(1-mu^2), and

```text
x(mu,phi) = (a cos(phi), a sin(phi), lambda mu).
```

Use the oriented area vector

```text
N(mu,phi) = (lambda a cos(phi), lambda a sin(phi), mu),
w = |N| = sqrt(lambda^2(1-mu^2)+mu^2).
```

For p=(r,0,z), define

```text
d = x-p,
D = |d|,
h = d.N = lambda(1-r a cos(phi)) - z mu,
c = h/(D w),
alpha = acos(c),
Ralpha = alpha/sin(alpha).
```

Since 3 Vol(K_lambda)=4 pi lambda,

```text
E_lambda(r,z) = (1/(4 pi lambda)) int_{-1}^1 int_0^{2pi} h alpha^2 dphi dmu.
```

## Exact first-gradient densities

For j in {r,z}, with

```text
N_r = lambda a cos(phi),   d_r = a cos(phi)-r,
N_z = mu,                  d_z = lambda mu-z,
```

we have

```text
partial_j c = -N_j/(D w) + h d_j/(D^3 w),
partial_j alpha = -partial_j c / sin(alpha),
```

and hence

```text
partial_j E_lambda
 = (1/(4 pi lambda)) int int G_j dphi dmu,

G_j = -N_j alpha^2 - 2 h Ralpha partial_j c.
```

These analytic densities, not finite differences of E, are the primary binary64 gradient evaluator.

For search coordinates (q,theta), obtain the two components by the chain rule:

```text
G_q     = sin(theta) * E_r + lambda cos(theta) * E_z,
G_theta = q cos(theta) * E_r - lambda q sin(theta) * E_z.
```

A meridian stationary point away from q=0 is a simultaneous zero of (G_q,G_theta). For numerical conditioning near q=0, also report E_r and E_z separately; do not use G_theta/q as a root criterion unless explicitly labelled diagnostic.

## Lambda values — fixed before scan

```text
lambda in {0.30, 0.50, 0.60, 0.65, 0.80, 0.95}.
```

No interpolation in lambda is part of this first scan.

## Binary64 quadrature

Primary evaluator:

- tensor Gauss-Legendre quadrature in mu and periodic trapezoidal quadrature in phi;
- baseline: N_mu=160, N_phi=256;
- validation rerun: N_mu=240, N_phi=512;
- all arithmetic IEEE binary64;
- clamp c only for final roundoff protection to [-1,1]; record the maximum unclamped violation if any;
- use a stable evaluation of Ralpha=alpha/sin(alpha) near alpha=0, e.g. a short even Taylor expansion below a declared threshold.

A candidate is retained only if the refined quadrature changes both gradient components by less than `1e-8` in absolute value at the candidate and the refined residual norm is below `1e-8`. These thresholds are diagnostic only.

## Search grid

Coarse seed grid in (q,theta):

```text
q_i     = 0.02, 0.04, ..., 0.98,
theta_j = j*pi/96,  j=0,...,48.
```

The theta=0 axis row is included only as a control and must not be reported as an off-axis root. The theta=pi/2 row is included because an equatorial stationary circle may occur.

For every grid cell, record the four corner values of (G_q,G_theta). Create a root seed when either:

1. both components have zero in their corner min/max ranges; or
2. the minimum corner gradient norm is below `5e-3`; or
3. a local minimum of the grid gradient norm is below `2e-2`.

These permissive rules are intended to avoid missing tangential roots that do not produce independent sign changes.

## Root refinement

For each seed, refine in (q,theta) by a safeguarded two-dimensional Newton method:

- numerical 2x2 Jacobian of the analytic gradient using centered binary64 differences;
- initial difference step `1e-5` in each search coordinate, adaptively reduced to stay inside the domain;
- damp Newton steps to remain in `0<q<1`, `0<=theta<=pi/2`;
- if the Jacobian is ill-conditioned, switch to a trust-region / least-squares step;
- convergence target: refined gradient norm < `1e-10` before quadrature validation;
- merge candidates whose `(q,theta)` separation is < `1e-6`.

No root count obtained here is binding.

## Axis and center controls

For each lambda also report:

1. `g_axis_ob(t,lambda)` for t in `{0, 1e-4, 1e-3, 1e-2, 0.05, 0.10}` using the independent axial evaluator if available;
2. a symmetric estimate of the center axial Hessian coefficient

```text
H_axis(lambda) ~= g_axis_ob(eps,lambda)/eps
```

at eps in `{1e-4, 3e-4, 1e-3}`;
3. the sign stability of that estimate under precision/quadrature refinement.

This is only to locate a possible center index-change value lambda_c^ob for later certification.

## Required output table

For each lambda print:

```text
lambda
number_of_off_axis_candidates
candidate_id
q
theta
r=q sin(theta)
z=lambda q cos(theta)
E_r
E_z
G_q
G_theta
grad_norm
quadrature_coarse_residual
quadrature_refined_residual
classification_hint: AXIS_CONTROL / EQUATORIAL_ORBIT / GENERIC_OFF_AXIS_ORBIT
Jacobian eigenvalues or singular values at the candidate
```

Also print a lambda-level summary:

```text
OFF_AXIS_FOUND: YES/NO
EQUATORIAL_FOUND: YES/NO
MIN_OFF_AXIS_GRAD_NORM_ON_GRID
CENTER_AXIS_HESSIAN_SIGN_HINT: POS/NEG/UNRESOLVED
```

## Mandatory interpretation rules

- `OFF_AXIS_FOUND: NO` means only "none detected by this scan"; it is not an exclusion theorem.
- Any detected off-axis candidate must be independently rerun at higher quadrature resolution before it is used to shape the theorem statement.
- The scan must not choose `lambda_min` by convenience. It may only suggest candidate breakpoints / topology changes for later exact contracts.
- No `CERTIFIED`, `AUDITED`, or theorem language is permitted in the diagnostic output.
- The global theorem statement remains unfixed until this table has been reviewed.
