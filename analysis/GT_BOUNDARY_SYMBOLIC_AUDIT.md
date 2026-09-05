# Boundary t-derivative symbolic audit — receipt template

Status: `OWNER_SYMBOLIC_AUDIT_PASS / EXTERNAL_JUDGE_PENDING / NOT_BINDING`

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

## Owner symbolic correspondence audit

The project-owner independent audit checked the implementation term by term.
The content-level verdict is `PASS`; external Judge sign-off remains separate.

| Derived term | Arb implementation correspondence | Result |
| --- | --- | --- |
| `s*4 mu R gamma_t` | `-4(1-e) lambda R C/(w qhat^(3/2))` | PASS |
| `s*(-2s^2) R_gamma gamma_t^2` | `-2 s lambda^2 R_gamma C^2/(w^2 qhat^3)` | PASS |
| `s*(-2s^2) R gamma_tt` | `-2 e lambda^3 R D/(w qhat^(5/2))` | PASS |
| upper chart `R_gamma=-2 gamma Psi_prime(u)` | after substituting `gamma=lambda s/(w sqrt(qhat))`: `+4 e lambda^3 Psi_prime(u) C^2/(w^3 qhat^(7/2))` | PASS |

Here `C=(2-s^2)(1-a s^2)` and `D=(2-s^2)(1-2 a s^2)`.

### Lower gamma chart

For `s in [0,1]`, use

```text
u       = 1-gamma^2
R       = acos(gamma)/sqrt(u)
R_gamma = (gamma R - 1)/u.
```

For `lambda in [5/8,33/50]`, the internal zero satisfies
`s0=1/sqrt(a)>1`, numerically in the range about `[1.28,1.33]`, so the lower
chart stays separated from `u=0`. The owner audit marked this denominator
handling `PASS`.

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

so no quotient by `u` or `s` remains. The implementation reuses the retained
`Psi` and `Psi_prime` coefficient formulae and rigorous geometric remainder
enclosure. The checker independently reconstructs the kernel and series and
requires `u.upper() < 1` before using the series.

## REPORTED_NOT_GATING expectations

These values are comparison targets only and must never gate acceptance:

```text
lambda = 5/8   : -1.4120900996030582330984866619528326407579821748752
lambda = 13/20 : -1.4717090003859539426113646310237584846969543547289
lambda = 33/50 : -1.4958034682340728485822766948219344845501715771395
```

The `33/50` value corrects a prior non-gating transcription/copy error.

## Audit checklist status

1. Pre-limit differentiation from `F_t` to `G`: owner audit PASS.
2. `N_t=-lambda^2(1-mu^2)` and endpoint `gamma_tt`: owner audit PASS.
3. Analytic cancellation of explicit `1/s`: owner audit PASS.
4. Lower-chart `R_gamma` identity and denominator separation: owner audit PASS.
5. Upper-chart `R=Psi(u)` and `R_gamma=-2 gamma Psi_prime(u)`: owner audit PASS.
6. Upper-chart `Psi_prime` denominator `w^3 qhat^(7/2)`: owner audit PASS.
7. Producer/checker independent kernel reconstruction: owner audit PASS.
8. Inherited series coefficients/remainder rule: owner audit PASS.
9. Numerical expectations are `REPORTED_NOT_GATING`: owner audit PASS.
10. Sole gating condition is complete-domain `upper_endpoint < 0`: owner audit PASS.

## External Judge requirement

The owner audit above does not promote this branch to `CERTIFIED`. The external
Judge record must pin the final audited commit, producer blob SHA, checker blob
SHA, workflow run id/number/conclusion, and the complete-domain checker
enclosure. Any source change after those pins requires a new Judge receipt.
