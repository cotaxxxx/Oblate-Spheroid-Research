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

## Diagnostic predictions — not certified

The following values are targets for independent computation, not results:

```text
lambda_entry_ob  ~ 0.64430
lambda_axis_ob   ~ 0.4079
entry slope C    ~ 0.6965
```

Expected signs:

```text
b_ob(0.60) < 0
b_ob(0.70) > 0
b_ob(1) = pi^2/32 > 0
```

Failure to reproduce these targets requires investigation; agreement does not
constitute certification.

## Open obligations

- implement the endpoint-regular axial evaluator;
- certify existence, uniqueness, and transversality of `lambda_entry_ob`;
- certify `b_ob_prime > 0` and `gt_boundary_ob < 0`;
- certify the center-axis degeneracy and nondegenerate pitchfork coefficients;
- exclude interior folds and additional meridian stationary points;
- keep the `lambda -> 0` uniform tail outside the present finite-window claim.
