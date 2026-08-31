# Center-axis coefficient certification contract

Status: `PROTOTYPE / NOT_AUDITED / NOT_BINDING`

## Target

For the oblate spheroid axial gradient `g_axis_ob(t,lambda)`, define

```text
H_axis_ob(lambda) := partial_t g_axis_ob(0,lambda).
```

The target parameter domain for this contract is

```text
lambda in [1/4,1].
```

This contract concerns only the center axial Hessian coefficient and its unique zero. It does not certify the pitchfork normal-form coefficient, the global nonzero axial branch, or off-axis exclusion.

## Existing density specialization

No new t->0 limiting density is introduced. Use the already derived and symbolically audited general second t-derivative density

```text
G_t(s,t,lambda)
 = s [ 4 mu R gamma_t
       - 2 A ( R_gamma gamma_t^2 + R gamma_tt ) ].
```

Set `t=0` directly. With

```text
e   = s^2,
mu  = 1-e,
gap = 2-e = 1+mu,
A   = 1,
d   = -mu,
q   = 1-mu^2 + lambda^2 mu^2,
w^2 = mu^2 + lambda^2(1-mu^2),
H   = mu(1+mu) - lambda^2(1+mu^2),
gamma = lambda/(w sqrt(q)),
```

we have

```text
gamma_t  = -lambda e H/(w q^(3/2)),
gamma_tt = lambda^3 e K/(w q^(5/2)),
K        = -3 mu H - gap q.
```

Hence

```text
H_axis_ob(lambda) = integral_0^sqrt(2) G_t(s,0,lambda) ds.
```

For `lambda>=1/4`, `q>=lambda^2>0` and `w>=lambda>0`. There is no moving north-corner singularity. `gamma=1` occurs only at the fixed surface endpoints `mu=+/-1`; the `R` and derivative combinations are understood by their removable endpoint limits. The machine implementation must use a representation valid at these fixed endpoints and must not divide naively by `1-gamma^2` there.

## Fixed sign claims

The machine gates are declared before implementation.

### Claim A1 — lower sign cover

```text
H_axis_ob(lambda) < 0  for lambda in [1/4,2/5].
```

### Claim A2 — upper sign cover

```text
H_axis_ob(lambda) > 0  for lambda in [83/200,1].
```

### Claim A3 — central transversality

```text
partial_lambda H_axis_ob(lambda) > 0
for lambda in [2/5,83/200].
```

Together with the endpoint signs at `lambda=2/5` and `lambda=83/200`, A3 implies exactly one zero

```text
lambda_c^ob in (2/5,83/200).
```

A later bisection/refinement may certify a narrower enclosure, but it must not change the claims above.

## Lambda derivative density

Differentiate the t=0 specialization, not the unspecialized full expression. Define

```text
q_lam  = 2 lambda mu^2,
w_lam  = lambda(1-mu^2)/w,
H_lam  = -2 lambda(1+mu^2),

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

gamma_t_lam = -e (P_lam H + P H_lam).
```

For the second t derivative set

```text
K = -3 mu H - gap q,
K_lam = -3 mu H_lam - gap q_lam,
Q = lambda^3/(w q^(5/2)),
Q_lam = Q [ 3/lambda
            - lambda(1-mu^2)/w^2
            - 5 lambda mu^2/q ],

gamma_tt_lam = e (Q_lam K + Q K_lam).
```

Use

```text
u = 1-gamma^2,
R = acos(gamma)/sqrt(u),
R_gamma = (gamma R - 1)/u,
R_gammagamma
 = [ (R + gamma R_gamma) u
     + 2 gamma (gamma R - 1) ] / u^2,

R_lam = R_gamma gamma_lam,
R_gamma_lam = R_gammagamma gamma_lam,
```

with removable endpoint continuation rather than literal division when `u=0`.

Then the declared lambda derivative density is

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

The symbolic audit must independently rederive this formula before any machine result is promoted.

## Machine architecture

Producer/checker separation is mandatory.

Suggested first declaration:

```text
arithmetic: Arb
producer bits: 160
checker bits: >=192
s panels: 1024 exact panels with fixed endpoint handling
lambda cover A1: exact rational boxes covering [1/4,2/5]
lambda cover A2: exact rational boxes covering [83/200,1]
lambda cover A3: exact rational boxes covering [2/5,83/200]
required signs: NEG / POS / POS respectively
```

Subdivision counts may be chosen after a non-gating width diagnostic, but must then be frozen in a separate implementation contract before the gating run.

## Independent expectations — REPORTED_NOT_GATING

These values are controls only and never machine gates:

```text
H_axis_ob(0.3) ~ -0.24350
H_axis_ob(0.4) ~ -0.01973
H_axis_ob(0.5) ~ +0.23697
H_axis_ob(0.6) ~ +0.49623
H_axis_ob(0.8) ~ +0.96387
lambda_c^ob    ~ 0.4079588603...
```

Exact sphere control:

```text
H_axis_ob(1) = 4/3.
```

The sphere identity is an exact algebraic control analogous to `b_ob(1)=pi^2/32` and must be checked independently of the production evaluator.

## Logical consequence after certification

If A1--A3 and the required symbolic/audit chain are certified, then there exists exactly one

```text
lambda_c^ob in (2/5,83/200)
```

such that

```text
H_axis_ob(lambda) < 0 for lambda < lambda_c^ob,
H_axis_ob(lambda) = 0 for lambda = lambda_c^ob,
H_axis_ob(lambda) > 0 for lambda > lambda_c^ob,
```

throughout `[1/4,1]`.

This establishes only the change of the axial center eigenvalue. The pitchfork statement requires a separate nonzero cubic/normal-form coefficient contract.