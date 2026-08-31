# Center-axis coefficient certification contract

Status: `AUDIT_COMPLETE / MACHINE_GATING_PASS / EXTERNAL_JUDGE_PENDING / NOT_BINDING`

## Target

For the oblate spheroid axial gradient `g_axis_ob(t,lambda)`, define

```text
H_axis_ob(lambda) := partial_t g_axis_ob(0,lambda).
```

Target parameter domain:

```text
lambda in [1/4,1].
```

This contract concerns only the center axial Hessian coefficient and its unique zero. It does not certify the pitchfork normal-form coefficient, the global nonzero axial branch, or off-axis exclusion.

## Existing density specialization

No new t->0 limiting density is introduced. Use the already derived general second-t density

```text
G_t = s [ 4 mu R gamma_t
          - 2 A (R_gamma gamma_t^2 + R gamma_tt) ].
```

Set `t=0` directly. With

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
H_axis_ob(lambda) = integral_0^sqrt(2) G_t(s,0,lambda) ds.
```

For `lambda>=1/4`, `q>=lambda^2>0` and `w>=lambda>0`. There is no moving north-corner singularity. The removable loci `gamma=1` are fixed (`s=0,1,sqrt(2)` at t=0); machine evaluation must use an analytic continuation representation there.

The exact complement used for stable evaluation is

```text
u = 1-gamma^2
  = e (1+mu) mu^2 (1-lambda^2)^2 / (w^2 q) >= 0.
```

## Fixed final claims

### Claim A1 — lower sign

```text
H_axis_ob(lambda) < 0  for lambda in [1/4,2/5].
```

### Claim A2 — upper sign

```text
H_axis_ob(lambda) > 0  for lambda in [83/200,1].
```

### Claim A3 — central transversality

```text
partial_lambda H_axis_ob(lambda) > 0
for lambda in [2/5,83/200].
```

Together these imply exactly one zero `lambda_c^ob in (2/5,83/200)`.

## Stable proof decomposition after width diagnostic

The final claims A1--A3 are unchanged. A direct two-parameter sign cover for A1/A2 was found to be unnecessarily weak near `lambda=2/5` and `83/200`; even point-lambda 1024-panel enclosures for H were wider than the true endpoint margins. Therefore the machine proof establishes the stronger monotonicity lemma

```text
A0: partial_lambda H_axis_ob(lambda) > 0 on [1/4,1],
```

together with high-resolution point enclosures

```text
H_axis_ob(2/5) < 0,
H_axis_ob(83/200) > 0.
```

Then A1 and A2 follow immediately from A0, and A3 is a restriction of A0. This is a proof decomposition only; it does not change the theorem claim, parameter domain, or zero enclosure target.

The machine receipt is pinned at

```text
analysis/CENTER_AXIS_COEFFICIENT_MACHINE_RECEIPT.md
commit d2321a12033b5ad3ad14e2282603aefcb2ebfdaa
```

and the Judge request at

```text
analysis/CENTER_AXIS_COEFFICIENT_JUDGE_REQUEST.md
commit 06eae461deed6a343774d3f67c83f7921bc79bba
```

## Lambda derivative density

Differentiate the corrected t=0 specialization. Define

```text
q_lam = 2 lambda mu^2,
w_lam/w = lambda(1-mu^2)/w^2,
H_lam = -2 lambda mu(1+mu),
K_lam = -3 mu H_lam - gap q_lam,

gamma_lam
 = gamma [ 1/lambda
           - lambda(1-mu^2)/w^2
           - lambda mu^2/q ].
```

Let

```text
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

The corrected symbolic audit is recorded separately and has user audit status `PASS / NOT_BINDING`.

## Machine architecture

Producer/checker separation is mandatory. Final A implementation declaration:

```text
arithmetic: Arb
producer bits: 160
checker bits: 192
regular derivative s panels: 1024
point-sign s panels: 4096
Psi series degree: 50
u-series threshold: 3/5
checker kernel: TRANSCRIBED_COPY_NOT_INDEPENDENT_DERIVATION
independence scope: PRECISION/PARTITION/GATING
```

At `u<=3/5`, evaluate

```text
R = Psi(u),
R_gamma = -2 gamma Psi'(u),
R_gammagamma = 4 gamma^2 Psi''(u) - 2 Psi'(u)
```

using positive-coefficient series with a rigorous tail. For larger u use the factorized positive complement and direct regular formulas.

The user completed a raw content audit of producer/checker algebra, tail bounds, removable continuation, lambda derivatives, sphere controls, and gating logic with result `PASS`.

## Independent expectations — REPORTED_NOT_GATING

```text
H_axis_ob(0.3) ~ -0.24350
H_axis_ob(0.4) ~ -0.019734
H_axis_ob(0.5) ~ +0.236973
H_axis_ob(0.6) ~ +0.49623
H_axis_ob(0.8) ~ +0.96387
partial_lambda H_axis_ob(0.4) ~ 2.4675
partial_lambda H_axis_ob(0.5) ~ 2.6172
lambda_c^ob ~ 0.4079588603...
```

Exact sphere controls, independent of production evaluation and machine-gated by containment:

```text
H_axis_ob(1) = 4/3,
partial_lambda H_axis_ob(1) = 8/5.
```

## Current logical consequence

The audited machine chain establishes, pending external Judge approval, exactly one

```text
lambda_c^ob in (2/5,83/200)
```

such that H is negative below it and positive above it throughout `[1/4,1]`.

A is internally closed at `AUDIT_COMPLETE / MACHINE_GATING_PASS`; only external Judge approval remains before any `CERTIFIED` promotion. The pitchfork normal-form coefficient is a separate contract B.
