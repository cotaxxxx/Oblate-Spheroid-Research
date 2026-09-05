# Center-axis coefficient certification contract

Status: `CERTIFIED_WITHIN_SCOPE / JUDGE_PASS`

## Target

For the oblate spheroid axial gradient `g_axis_ob(t,lambda)`, define

```text
H_axis_ob(lambda) := partial_t g_axis_ob(0,lambda).
```

Target parameter domain:

```text
lambda in [1/4,1].
```

This contract certifies only the center axial Hessian coefficient sign structure and its unique zero. It does not certify the pitchfork normal-form coefficient, the global nonzero axial branch, or off-axis exclusion.

## Certified claim

There exists exactly one

```text
lambda_c^ob in (2/5,83/200)
```

such that throughout `[1/4,1]`

```text
H_axis_ob(lambda) < 0 for lambda < lambda_c^ob,
H_axis_ob(lambda) > 0 for lambda > lambda_c^ob.
```

The certified stronger decomposition is

```text
partial_lambda H_axis_ob(lambda) > 0 on [1/4,1],
H_axis_ob(2/5) < 0,
H_axis_ob(83/200) > 0.
```

Hence the zero is simple in the lambda direction.

## t=0 specialization

With

```text
e = s^2,
mu = 1-e,
gap = 2-e = 1+mu,
A = 1,
d = -mu,
q = 1-mu^2 + lambda^2 mu^2,
w^2 = mu^2 + lambda^2(1-mu^2),
H = mu(1+mu)(1-lambda^2),
K = -3 mu H - gap q,
gamma = lambda/(w sqrt(q)),
```

we have

```text
gamma_t  = -lambda e H/(w q^(3/2)),
gamma_tt = lambda^3 e K/(w q^(5/2)),
H_axis_ob(lambda) = integral_0^sqrt(2) G_t(s,0,lambda) ds,
```

where

```text
G_t = s [ 4 mu R gamma_t
          - 2 A (R_gamma gamma_t^2 + R gamma_tt) ].
```

For `lambda>=1/4`, `q>=lambda^2>0` and `w>=lambda>0`. The removable loci `gamma=1` are fixed (`s=0,1,sqrt(2)` at t=0) and are handled by analytic continuation.

The exact complement used for stable evaluation is

```text
u = 1-gamma^2
  = e (1+mu) mu^2 (1-lambda^2)^2 / (w^2 q) >= 0.
```

## Lambda derivative density

Define

```text
q_lam = 2 lambda mu^2,
w_lam/w = lambda(1-mu^2)/w^2,
H_lam = -2 lambda mu(1+mu),
K_lam = -3 mu H_lam - gap q_lam,

gamma_lam
 = gamma [ 1/lambda
           - lambda(1-mu^2)/w^2
           - lambda mu^2/q ],

P = lambda/(w q^(3/2)),
P_lam = P [ 1/lambda
            - lambda(1-mu^2)/w^2
            - 3 lambda mu^2/q ],
gamma_t_lam = -e (P_lam H + P H_lam),

Q = lambda^3/(w q^(5/2)),
Q_lam = Q [ 3/lambda
            - lambda(1-mu^2)/w^2
            - 5 lambda mu^2/q ],
gamma_tt_lam = e (Q_lam K + Q K_lam).
```

Use

```text
R_gamma = (gamma R - 1)/(1-gamma^2),
R_gammagamma
 = [ (R + gamma R_gamma)(1-gamma^2)
     + 2 gamma(gamma R - 1) ]/(1-gamma^2)^2,
R_lam = R_gamma gamma_lam,
R_gamma_lam = R_gammagamma gamma_lam.
```

Then

```text
partial_lambda G_t
 = s [
       4 mu (R_lam gamma_t + R gamma_t_lam)
       - 2 (
           R_gamma_lam gamma_t^2
           + 2 R_gamma gamma_t gamma_t_lam
           + R_lam gamma_tt
           + R gamma_tt_lam
         )
     ].
```

## Machine architecture

```text
arithmetic: Arb
producer bits: 160
checker bits: 192
regular derivative s panels: 1024
point-sign s panels: 4096
Psi series degree: 50
u-series threshold: 3/5
CHECKER_KERNEL=TRANSCRIBED_COPY_NOT_INDEPENDENT_DERIVATION
INDEPENDENCE_SCOPE=PRECISION/PARTITION/GATING
```

At `u<=3/5`, evaluate

```text
R = Psi(u),
R_gamma = -2 gamma Psi'(u),
R_gammagamma = 4 gamma^2 Psi''(u) - 2 Psi'(u)
```

using positive-coefficient series with rigorous tails. For larger `u`, use the factorized positive complement and direct regular formulas.

Mathematical derivation independence is supplied by the external human reviewer's independent symbolic derivation and finite-difference checks, not by the checker kernel.

## Pinned evidence

```text
Audited source commit:
79234b601e4cd05d66e4dfa926184dd527e08588

Producer blob:
0b604f1dc17c8aba2825f25659b5d06a77c20c16

Checker blob:
3af01fbc62a77061ab6131ca442ff39f3e25a722

Machine receipt:
analysis/CENTER_AXIS_COEFFICIENT_MACHINE_RECEIPT.md
commit d2321a12033b5ad3ad14e2282603aefcb2ebfdaa

Judge request:
analysis/CENTER_AXIS_COEFFICIENT_JUDGE_REQUEST.md
commit 06eae461deed6a343774d3f67c83f7921bc79bba

Judge receipt:
analysis/CENTER_AXIS_COEFFICIENT_JUDGE_RECEIPT.md
commit e56b751fe3864eb6e9ba3e2249608ae05217d11f

Focused machine run:
33387236630
job 99472510996
```

Exact sphere controls, machine-gated by containment:

```text
H_axis_ob(1) = 4/3,
partial_lambda H_axis_ob(1) = 8/5.
```

## Scope exclusions

Not certified by A:

- the pitchfork cubic coefficient `c3`;
- existence/uniqueness of local nonzero branches;
- global axial census away from the center;
- connection to the boundary-entry parameter;
- off-axis exclusion;
- any statement for `lambda<1/4`;
- the non-gating decimal approximation `lambda_c^ob ~ 0.4079588603...`.

Those remain separate contracts.
