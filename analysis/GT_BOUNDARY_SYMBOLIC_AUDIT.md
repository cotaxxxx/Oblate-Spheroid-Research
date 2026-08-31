# Boundary t-derivative symbolic audit — receipt template

Status: `PENDING / NOT_AUDITED / NOT_BINDING`

This receipt covers the correspondence between the independently derived
endpoint density for

`gt_boundary_ob(lambda) = partial_t g_axis_ob(1,lambda)`

and its two-chart Arb implementation. It does not certify a sign enclosure.

## Target claim fixed before computation

```text
quantity      = partial_t g_axis_ob(1,lambda)
lambda domain = [5/8,33/50]
required sign = NEG
gating rule   = full-domain Arb enclosure upper endpoint < 0
```

The orientation basis is the independently reproduced census: the positive
axial root exists for lambda below the boundary value, satisfies t_star -> 1
as lambda increases to the boundary value, and is absent above it. Together
with the retained certified `B_ob'(lambda)>0`, the IFT relation

`dt_star/dlambda = -B_ob'(lambda)/partial_t g_axis_ob`

requires `partial_t g_axis_ob < 0`.

## Pinned derivation

Starting from the pre-limit density

`F_t = s[-mu alpha^2 - 2 A R gamma_t]`,

with `R = alpha/sin(alpha)`, the independently checked derivative is

`G = s[4 mu R gamma_t - 2 A(R_gamma gamma_t^2 + R gamma_tt)]`.

At `t=1`, write

```text
e      = s^2
a      = 1-lambda^2
h      = 1-a e
qhat   = 2-a e
w^2    = 1-2 a e+a e^2
gap    = 2-e
C      = gap h
D      = gap(1-2 a e)
gamma  = lambda s/(w sqrt(qhat))
```

and cancel all explicit `1/s` factors before interval evaluation. The regular
endpoint density is

```text
G_boundary =
  -4(1-e) lambda R C/(w qhat^(3/2))
  -2 s lambda^2 R_gamma C^2/(w^2 qhat^3)
  -2 e lambda^3 R D/(w qhat^(5/2)).
```

### Lower gamma chart

For `s in [0,1]`, use

```text
u       = 1-gamma^2
R       = acos(gamma)/sqrt(u)
R_gamma = (gamma R - 1)/u.
```

The chart bound keeps `u` away from zero.

### Upper u chart

For `s in [1,sqrt(2)]`, use the inherited factorized complement

`u = gap h^2/(w^2 qhat)`

and the certified-lineage series

```text
R       = Psi(u)
R_gamma = -2 gamma Psi_prime(u).
```

After substituting gamma, the second term becomes

```text
+4 e lambda^3 Psi_prime(u) C^2/(w^3 qhat^(7/2)),
```

so no quotient by `u` or `s` remains. The implementation must reuse the
retained `Psi` and `Psi_prime` coefficient formulae and rigorous geometric
remainder enclosure.

## REPORTED_NOT_GATING expectations

These values are comparison targets only and must never gate acceptance:

```text
lambda = 5/8   : -1.4120900996030582330984866619528326407579821749232
lambda = 13/20 : -1.4717090003859539426113646310237584846969543547625
lambda = 33/50 : -1.4958034682340728485822766948219344846969543547625
```

## Human audit checklist

1. Verify the pre-limit differentiation from `F_t` to `G` term by term.
2. Verify `N_t=-lambda^2(1-mu^2)` and the displayed endpoint `gamma_tt`.
3. Verify analytic cancellation of all explicit `1/s` factors.
4. Verify the lower-chart `R_gamma` identity and that its denominator is
   separated from zero on the lower chart.
5. Verify `R=Psi(u)` and `R_gamma=-2 gamma Psi_prime(u)` on the upper chart.
6. Verify the algebra giving the upper-chart `Psi_prime` term with denominator
   `w^3 qhat^(7/2)`.
7. Verify producer and checker implement the same mathematical density without
   importing one another's kernel implementation.
8. Verify the inherited series coefficients/remainder rule are unchanged.
9. Verify the three numerical expectations are labelled
   `REPORTED_NOT_GATING` and do not enter the pass criterion.
10. Verify the sole gating condition is `upper_endpoint < 0` for the complete
    lambda interval `[5/8,33/50]`.

No `PASS` may be written into this file by the implementation actor. An
external audit/judge record must identify the audited commit and file hashes.
