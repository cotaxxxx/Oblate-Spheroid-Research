# Axial census rederivation from the pinned pre-limit kernel

Status: `DIAGNOSTIC_ONLY / NOT_BINDING`

This note records a clean re-scan of the positive oblate axial branch using the pinned pre-limit density

```text
F_t(s,t,lambda)
 = s[-mu*alpha^2 - 2*A*(alpha/sin(alpha))*gamma_t],
A = 1 - t*mu,
d = t - mu,
q = 1 - mu^2 + lambda^2*d^2,
N = -mu*q - A*lambda^2*d,
gamma_t = lambda*N/(w*q^(3/2)),
g(t,lambda) = integral_0^sqrt(2) F_t ds.
```

The historical census script `diagnostics/oblate_fold_scan.py` uses `lam` directly as the spheroid polar semiaxis ratio in the formulas above. It does **not** replace it by `a = 1-lambda^2`, `1/lambda`, or another transformed parameter.

## Re-scan configuration

- arithmetic: `mpmath`, 40 decimal digits
- lambda grid: `0.60, 0.625, 0.65, 0.66, 0.70`
- t grid: `1, 0.99, 0.97, 0.95, 0.9, 0.8, 0.7, 0.5, 0.3, 0.1`
- integration splits: `0, 0.5, 1, s0, sqrt(2)` when `s0 = 1/sqrt(1-lambda^2)` lies in `(1,sqrt(2))`
- roots: bisection on observed sign-changing grid intervals
- point values below are `REPORTED / DIAGNOSTIC_ONLY`; they are not gating controls

## Grid values g(t,lambda)

| lambda | t=1 | 0.99 | 0.97 | 0.95 | 0.9 | 0.8 | 0.7 | 0.5 | 0.3 | 0.1 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.60 | -0.0491681187153 | -0.0360257121496 | -0.0115617952399 | 0.0108657021266 | 0.0593627766777 | 0.129438586631 | 0.170210119296 | 0.184527357209 | 0.135248291998 | 0.0491204998628 |
| 0.625 | -0.0206610795789 | -0.00696190240705 | 0.0184827229704 | 0.0417462061962 | 0.0918081575532 | 0.163196031238 | 0.203351676075 | 0.212129446390 | 0.153321879544 | 0.0553922070947 |
| 0.65 | 0.00708903796296 | 0.0213540998209 | 0.0477951536105 | 0.0719082123883 | 0.123563469273 | 0.196310087175 | 0.235896158484 | 0.239253209391 | 0.171082917531 | 0.0615550120399 |
| 0.66 | 0.0179668082666 | 0.0324604996162 | 0.0593040068302 | 0.0837602240333 | 0.136059749771 | 0.209361634746 | 0.248732444076 | 0.249956021828 | 0.178091116319 | 0.0639865627682 |
| 0.70 | 0.0601563093685 | 0.0755756222019 | 0.104047543001 | 0.129892106709 | 0.184801300427 | 0.260381984797 | 0.298959800093 | 0.291855840493 | 0.205523813174 | 0.0735030913462 |

At `t=1`, these values reproduce the endpoint functional `b_ob(lambda)`; in particular the already recorded values at `0.60`, `0.625=5/8`, `0.66=33/50`, and `0.70` agree.

## Sign changes and roots

| lambda | sign-changing interval on fixed grid | rederived root t* | historical census correspondence |
|---:|---|---:|---|
| 0.60 | `(0.95,0.97)` | 0.959901 | historical `0.9599010018420894` |
| 0.625 | `(0.97,0.99)` | 0.984711 | not sampled exactly; historical neighbors: `0.620 -> 0.980157068710`, `0.630 -> 0.989077541575` |
| 0.65 | none; all sampled g>0 | none observed | historical `0.650 -> null` |
| 0.66 | none; all sampled g>0 | none observed | outside historical full-window sampling |
| 0.70 | none; all sampled g>0 | none observed | outside historical full-window sampling |

The fixed-grid scan does not by itself exclude an unresolved root pair between sampled t values. However, the observed orientation agrees with the historical fold scan and its refined endpoint window: the positive-axis root exists for lambda below the boundary value, moves upward in t as lambda increases, reaches `t=1` at the endpoint zero, and is absent immediately above it.

The historical result records, for example,

```text
lambda=0.640  t*=0.997267672733
lambda=0.643  t*=0.999585461678
lambda=0.644  no positive root
lambda=0.650  no positive root
```

and gives negative branch slopes `partial_t g` through the approach to the endpoint.

## Consequence for the expected boundary orientation

The earlier working-note locations claiming roots at `lambda=0.65,0.66,0.70` do not correspond to this pinned `g(t,lambda)` and should not be used as census evidence.

For the pinned kernel, the observed branch is on the `lambda < lambda_boundary` side. Since the certified endpoint lineage gives `B_ob'(lambda)>0`, the local branch orientation is

```text
dt_star/dlambda = -B_ob'(lambda_boundary) / partial_t g(1,lambda_boundary) > 0,
```

which requires the expected `t`-derivative sign

```text
partial_t g_axis_ob(1,lambda_boundary) < 0.
```

Equivalently, with `tau=1-t`, the expected sign is `partial_tau g > 0`.

This sign is an expectation fixed from branch orientation before the new interval run. Numerical point values for `partial_t g` remain `REPORTED_NOT_GATING`; only the rigorous sign enclosure should gate the future certificate.
