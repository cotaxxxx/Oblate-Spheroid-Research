# Research Status

Updated: 2026-08-31

## Global status

`NOT_BINDING / DIAGNOSTIC_ONLY`

This repository currently contains no certified theorem, certified numerical
value, approved production kernel, or Actions-produced clean-room certificate
on `main`.

## Analytically derived kernel

For the oblate spheroid

```text
x^2 + y^2 + z^2/lambda^2 = 1,   0 < lambda < 1,
```

write an axial base point as `p = (0, 0, lambda*t)` and set

```text
q = 1 - mu^2 + lambda^2*(mu - t)^2
w^2 = lambda^2*(1 - mu^2) + mu^2
gamma = lambda*(1 - t*mu)/(w*sqrt(q))
h(c) = acos(c)^2
```

Then

```text
E_lambda(t) = (1/2) integral[-1,1] (1 - t*mu)*h(gamma) dmu
g_axis_ob(t,lambda) = partial_t E_lambda(t)
b_ob(lambda) = g_axis_ob(1,lambda)
```

The substitution `mu = 1 - s^2` regularizes the transformed endpoint
density and supports a one-sided `C^1` extension to `t = 1`. The prototype
formula has received an independent implementation-level audit, while the
analytic interchange/regularity statement is pinned separately for human audit.

## Endpoint C1 analytic source

The retained analytic branch

```text
analytic-endpoint-limit-78c178f
```

contains `analysis/endpoint_kernel_lemma.md`, blob SHA

```text
aa6a1a1710d1a4af560e5ddf0c504870f50c535c
```

which gives the pre-limit factorization, a `t`- and `lambda`-independent
integrable majorant near `s=0`, compact domination on `[1,sqrt(2)]`, dominated
convergence to the endpoint density, the exact endpoint reduction, and the
two-chart analyticity needed for differentiation under the lambda integral.
This source is not yet promoted by the present branch; its human audit receipt
is `analysis/ENDPOINT_C1_AUDIT_RECEIPT.md` and remains `PENDING` until an
external judge record is attached.

## Endpoint evaluator prototype

`axial_endpoint_ob.py` implements a direct `PROTOTYPE` evaluator for `b_ob`
using `mu = 1 - s^2`; it does not extrapolate from interior `t` values.

The pre-existing exact sphere expectation

```text
b_ob(1) = pi^2/32
```

is exercised by an implementation-connected test in
`controls/test_sphere_expectations.py`. The prototype audit also independently
reproduced the recorded values at `lambda = 0.60`, `0.70`, `5/8`, and `33/50`
using the equivalent `arcsin(sqrt(u))` representation. This is a prototype
control/audit result only and does not promote the file to a production or
certified implementation.

### Interval-chart obligation

The scalar `atan2` representation is suitable for the lower chart
`s in [0,1]`. It must not be naively intervalized across the opposite pole:
there `alpha -> 0` and `alpha/sin(alpha)` becomes a `0/0` interval quotient.
The rigorous upper chart `s in [1,sqrt(2)]` therefore uses the existing
`Phi`, `Psi`, and `Psi_prime` power-series representation with a geometric
remainder enclosure. The scalar branch `sin_num == 0 -> -2` is not an interval
proof device.

For the boundary `t`-derivative density, write `R = Psi(u)` on the upper chart.
Then

```text
R_gamma = Psi_prime(u) * du/dgamma = -2*gamma*Psi_prime(u)
```

so

```text
R_gamma * gamma_t^2 = -2*gamma*Psi_prime(u)*gamma_t^2.
```

This reuses the retained certified-lineage `Psi_prime` series and its rigorous
remainder enclosure. On the lower `gamma_lower` chart one may retain

```text
R_gamma = (gamma*R - 1)/(1 - gamma^2),
```

because that chart keeps the denominator uniformly away from zero.

## Certified-lineage record

The repository was renamed from `Oblate-Spheroid-Research` to
`bg-oblate-spheroid`; the historical certification branches are retained in
the same repository rather than being a separate replacement project.

The retained branch `receipt-binding-e5ab171` has head commit

```text
2d4bf4d51d2724b5693d3db292da3bccec940bc4
```

and contains the historical Arb producer/checker, controls, workflow material,
and `AUDIT_PIN.md`. That pin records the accepted endpoint enclosure checkpoint

```text
evidence class   = CERTIFIED_ENCLOSURE
source commit    = 7bdcbdcba3dab51c8ddbe72dac02c6307e1b5064
audit result     = PASS
tests reproduced = 52
claim domain     = [5/8, 33/50]
```

It also records the earlier audited-source pin

```text
derivation class = AUDITED_SOURCE
source commit    = 3406baad993701758a74ca9b42976412ca27b781
archive SHA-256  = b48b1c9dfbe4596834ddb669f79cd9ce85b92d07c7f274f2467e012784c44a8e
workflow run     = #182, success
```

The certified endpoint claim is conditional on the endpoint analytic and
one-sided-limit interchange lemma and on identification of the endpoint zero
with the boundary passage of the census branch. It certifies the two endpoint
signs and a positive derivative enclosure on `[5/8,33/50]` under those stated
conditions; it does not certify the full axial branch or the census
identification.

The historical two-chart Arb producer already implements the required split:
`gamma_lower` below `s=1` and `u_upper` above it, with factorized complement
and `Phi`/`Psi`/`Psi_prime` series plus rigorous remainder bounds. New interval
work must therefore reuse or explicitly derive from this pinned lineage rather
than silently reimplementing an equivalent kernel under a new provenance.

## Census re-derivation and orientation

The pinned pre-limit kernel and the historical census script now agree on the
branch orientation. The historical script uses `lambda` directly as the oblate
axis ratio; it does not replace it by `a = 1-lambda^2` or by `1/lambda`.

The reproduced positive-axis roots include

```text
lambda = 0.600   t_star = 0.959901001842...
lambda = 0.625   t_star = 0.9847113707...   [REPORTED]
lambda = 0.640   t_star = 0.997267672733...
lambda = 0.643   t_star = 0.999585461678...
lambda = 0.644   no positive-axis root observed
lambda = 0.650   no positive-axis root observed
```

The earlier working-note claims of roots near `t=0.9905` at `lambda=0.65`,
`t=0.9865` at `lambda=0.66`, and `t=0.9377` at `lambda=0.70` are superseded and
must not be used.

The consistent orientation is therefore

```text
lambda < lambda_boundary : one observed interior positive-axis stationary root
lambda -> lambda_boundary from below : t_star -> 1
lambda > lambda_boundary : no observed positive-axis stationary root
```

Together with the certified `B_ob'(lambda) > 0`, the implicit-function identity

```text
dt_star/dlambda = -partial_lambda g / partial_t g
```

requires `partial_t g < 0` at the boundary passage in order to have
`dt_star/dlambda > 0`.

## Boundary-branch identification sequence

The remaining boundary-entry proof chain is fixed in the following order.

1. **Endpoint C1 lemma audit.** Audit the pinned analytic source and attach an
   external judge receipt. This discharges the equality between the one-sided
   limit of `g_axis_ob(t,lambda)` and the direct endpoint integral.
2. **Boundary t-derivative sign.** Certify, with `t` as the axial coordinate,

   ```text
   gt_boundary_ob = partial_t g_axis_ob(1,lambda) < 0
   ```

   on the lambda bracket `[5/8,33/50]`. Equivalently, for `tau = 1-t`, certify
   `partial_tau g_axis_ob > 0`.

   The only gating numerical claim is the rigorous interval statement

   ```text
   hi(partial_t g_axis_ob(1,[5/8,33/50])) < 0.
   ```

   Independent point expectations at `lambda = 5/8`, `0.65`, and `33/50` are
   recorded only as `REPORTED_NOT_GATING` values:

   ```text
   lambda = 5/8    partial_t g(1,lambda) ~ -1.41209
   lambda = 0.65   partial_t g(1,lambda) ~ -1.47171
   lambda = 33/50  partial_t g(1,lambda) ~ -1.49580
   ```

   Agreement with those values is a diagnostic cross-check only. Failure to
   obtain `hi < 0` is a gating failure regardless of pointwise agreement.
3. **Monotone tube.** Certify a strip `t in [1-delta,1]` on which
   `partial_t g_axis_ob < 0`. This proves at most one axial stationary root per
   lambda inside the strip; Krawczyk is not required if the monotonicity
   enclosure closes.
4. **Census identification.** Reproduce the positive-axis census roots under a
   fixed configuration and place selected subcritical-lambda roots inside the
   certified monotone tube. Tube uniqueness then identifies those roots with
   the local IFT branch terminating at the certified boundary zero.

Only after all four steps are fixed may the endpoint zero be stated as the
boundary passage of the census branch.

## Symbolic-audit rule for the boundary t derivative

The pre-limit second-derivative density `G_t = partial_t F_t` has received a
chat-side symbolic derivation and term-by-term audit. The Arb implementation
must be audited again against that analytic density before any gating run is
accepted. In particular, the lower-chart and upper-chart formulas must be
checked symbolically against the same `G_t`; the upper chart must use the
`Psi_prime` identity above rather than a direct interval quotient through the
`gamma -> 1` point.

This audit is independent of the numerical sign run. A numerically negative
result from code that has not passed the symbolic correspondence audit is not a
certificate.

## Candidate numerical evidence — not certified

The following values are candidate evidence, not certified enclosures:

```text
lambda_entry_ob = 0.6435457703666799690435  [HIGH_PRECISION; mpmath dps=40; tanh-sinh]
lambda_axis_ob  = 0.40795886030094636425    [HIGH_PRECISION; mpmath dps=40; tanh-sinh]
b_ob_prime      = +1.10246                  [HIGH_PRECISION; centered difference h=1e-12]
gt_boundary_ob  = -1.45623019               [HIGH_PRECISION; one-sided dps=50 diagnostic]
b_ob(1)         = pi^2/32                   [EXACT]
```

The `gt_boundary_ob` value above is restored only as a high-precision diagnostic
candidate after the census orientation was independently re-derived from the
pinned kernel and historical raw script. It is not a certified enclosure and
is not a gating target.

Expected signs:

```text
b_ob(0.60) < 0
b_ob(0.70) > 0
b_ob(1) = pi^2/32 > 0
partial_t g_axis_ob(1,lambda) < 0 on [5/8,33/50]  [TARGET; NOT YET CERTIFIED]
```

Measured diagnostic values for the first two signs were approximately
`-0.04917` and `+0.06016`. Their derivation class remains diagnostic. Failure
to reproduce the signs requires investigation; agreement does not constitute
certification.

## Open obligations

- obtain the external human-audit/Judge receipt for the pinned endpoint C1
  analytic source;
- implement the boundary `t`-derivative density on the retained two-chart Arb
  lineage and pass an independent symbolic correspondence audit;
- run the certified interval enclosure on `[5/8,33/50]` with the sole gating
  condition `hi < 0`; treat point expectations as `REPORTED_NOT_GATING`;
- certify a monotone near-boundary tube with `partial_t g_axis_ob < 0`;
- reproduce the census roots under fixed configuration and identify them with
  the IFT branch by tube uniqueness;
- preserve the independent PROTOTYPE audit record for `axial_endpoint_ob.py`;
- reconnect any future production work explicitly to the pinned certified
  lineage rather than duplicating the two-chart Arb kernel without provenance;
- certify the center-axis degeneracy and nondegenerate pitchfork coefficients;
- exclude interior folds and additional meridian stationary points;
- keep the `lambda -> 0` uniform tail outside the present finite-window claim.
