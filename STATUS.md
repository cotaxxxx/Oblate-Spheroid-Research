# Research Status

Updated: 2026-08-31

## Global status

`NOT_BINDING / DIAGNOSTIC_ONLY`

This repository currently contains no certified theorem, certified numerical
value, approved production kernel, or Actions-produced clean-room certificate.

## Provenance

This repository continues the oblate-spheroid work previously kept under
`Oblate-Spheroid-Research`. Existing certified artifacts from that lineage,
including the `CERTIFIED_ENCLOSURE` for `lambda_entry_ob` in `[5/8, 33/50]`
and its Arb producer/checker and pinned judge record, are historical upstream
artifacts and are not regenerated or promoted by the present prototype branch.
Their exact source hashes and certificate references must be preserved when the
interval proof path is reconnected here.

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
density and supports a one-sided `C^1` extension to `t = 1`. This analytic
statement still requires a formal manuscript proof and independent audit.

## Endpoint evaluator prototype

`axial_endpoint_ob.py` implements a direct `PROTOTYPE` evaluator for `b_ob`
using `mu = 1 - s^2`; it does not extrapolate from interior `t` values.

An independent prototype audit has checked the implemented endpoint density
term-by-term against the recorded `B_ob` kernel and independently reproduced
the values at `lambda = 0.60`, `0.70`, and `1`, as well as the earlier
binary64 diagnostics at `5/8` and `33/50`. The prototype audit verdict is
`PASS`. This does not change the evidence class: the implementation remains
`PROTOTYPE / NOT_BINDING` and is not an interval production kernel.

The pre-existing exact sphere expectation

```text
b_ob(1) = pi^2/32
```

is now exercised by an implementation-connected test in
`controls/test_sphere_expectations.py`. This is a prototype control only and
must not be described as production or certified.

The same test file checks the previously recorded diagnostic sign targets
`b_ob(0.60) < 0` and `b_ob(0.70) > 0`. These remain diagnostic evidence.

## Interval implementation constraint

The pointwise prototype treatment of

```text
h_prime = -2*alpha/sin(alpha)
```

at the endpoint where `alpha -> 0` is not suitable for interval boxes that
contain the limiting point, because numerator and denominator simultaneously
contain zero. The interval evaluator must therefore use separate charts:

- on `s in [0,1]`, the algebraic `atan2` representation may be used;
- on `s in [1,sqrt(2)]`, `Phi` and `Psi` must be evaluated by their series
  representations with a rigorous remainder bound (for example, a geometric
  tail controlled by an explicit term-ratio bound strictly below one).

The scalar branch `sin_num == 0 -> -2` is a point-evaluation convenience only
and must not be copied into the interval production evaluator.

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

These computations were supplied through chat and are candidate evidence under
the two-layer certification rule. `lambda_axis_ob` independently agrees with
an earlier floating-point search near `0.40796`; `lambda_entry_ob` currently
has one computational source. Independent agreement does not promote either
value to `CERTIFIED_ENCLOSURE`.

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

- preserve the independent prototype-audit record and fixed source hash;
- reconnect the historical `[5/8,33/50]` certificate lineage with exact hashes
  and judge reference;
- implement the two-chart interval evaluator, using rigorous `Phi`/`Psi` series
  bounds on `s in [1,sqrt(2)]`;
- certify existence, uniqueness, and transversality of `lambda_entry_ob`;
- certify `b_ob_prime > 0` and `gt_boundary_ob < 0`;
- certify the center-axis degeneracy and nondegenerate pitchfork coefficients;
- exclude interior folds and additional meridian stationary points;
- keep the `lambda -> 0` uniform tail outside the present finite-window claim.
