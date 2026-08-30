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
formula has now received an independent implementation-level audit, but the
analytic interchange/regularity lemma remains a separate manuscript
obligation.

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

## Candidate numerical evidence — not certified

The following values are candidate evidence, not certified enclosures:

```text
lambda_entry_ob = 0.6435457703666799690435  [HIGH_PRECISION; mpmath dps=40; tanh-sinh]
lambda_axis_ob  = 0.40795886030094636425    [HIGH_PRECISION; mpmath dps=40; tanh-sinh]
b_ob_prime      = +1.10246                  [HIGH_PRECISION; centered difference h=1e-12]
gt_boundary_ob  = -1.45623                  [HIGH_PRECISION; one-sided Richardson difference]
entry_slope_ob  = 0.757064                  [HIGH_PRECISION; ratio b_ob_prime/(-gt_boundary_ob)]
b_ob(1)         = pi^2/32                   [EXACT]
```

These computations are candidate evidence under the two-layer certification
rule. `lambda_axis_ob` independently agrees with an earlier floating-point
search near `0.40796`; `lambda_entry_ob` remains a high-precision candidate
location and must not be substituted for the certified bracket.

Expected signs:

```text
b_ob(0.60) < 0
b_ob(0.70) > 0
b_ob(1) = pi^2/32 > 0
```

Measured diagnostic values for the first two signs were approximately
`-0.04917` and `+0.06016`. Their derivation class remains diagnostic. Failure
to reproduce the signs requires investigation; agreement does not constitute
certification.

## Open obligations

- preserve the independent PROTOTYPE audit record for `axial_endpoint_ob.py`;
- reconnect any future production work explicitly to the pinned certified
  lineage rather than duplicating the two-chart Arb kernel without provenance;
- discharge the endpoint analytic and one-sided-limit interchange lemma;
- establish the census-branch identification needed to interpret the certified
  endpoint zero as the boundary passage of the stationary branch;
- certify `gt_boundary_ob < 0` at the boundary-entry zero and the associated
  entry slope under the same fixed proof chain;
- certify the center-axis degeneracy and nondegenerate pitchfork coefficients;
- exclude interior folds and additional meridian stationary points;
- keep the `lambda -> 0` uniform tail outside the present finite-window claim.
