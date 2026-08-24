# Research Status

Updated: 2026-08-25

## Global status

`NOT_BINDING / DIAGNOSTIC_ONLY`

This repository currently contains no certified theorem, certified numerical
value, approved production kernel, or Actions-produced clean-room certificate.

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

- implement the endpoint-regular axial evaluator;
- certify existence, uniqueness, and transversality of `lambda_entry_ob`;
- certify `b_ob_prime > 0` and `gt_boundary_ob < 0`;
- certify the center-axis degeneracy and nondegenerate pitchfork coefficients;
- exclude interior folds and additional meridian stationary points;
- keep the `lambda -> 0` uniform tail outside the present finite-window claim.
