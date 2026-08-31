# Center-axis lambda derivative — symbolic audit target

Status: `CHAT_DERIVATION / NOT_AUDITED / NOT_BINDING`

This note is the human-audit target for Claim A3 in `CENTER_AXIS_COEFFICIENT_CONTRACT.md`. It must be independently rederived before machine implementation is treated as audited.

## 1. Start from the already audited general t-second derivative

```text
G_t = s [ 4 mu R gamma_t
          - 2 A (R_gamma gamma_t^2 + R gamma_tt) ].
```

At `t=0`, `A=1` and `A_lambda=0`, so

```text
G_t|_0 = s [ 4 mu R gamma_t
             - 2 (R_gamma gamma_t^2 + R gamma_tt) ].
```

No new t-limit argument is used.

## 2. t=0 geometry

Let

```text
e = s^2,
mu = 1-e,
gap = 2-e = 1+mu.
```

Then

```text
q = 1-mu^2 + lambda^2 mu^2,
w^2 = mu^2 + lambda^2(1-mu^2),
H = mu(1+mu) - lambda^2(1+mu^2),
K = -3 mu H - gap q,

gamma = lambda/(w sqrt(q)),
gamma_t = -lambda e H/(w q^(3/2)),
gamma_tt = lambda^3 e K/(w q^(5/2)).
```

Checks:

```text
q_lambda = 2 lambda mu^2,
(w^2)_lambda = 2 lambda(1-mu^2),
w_lambda/w = lambda(1-mu^2)/w^2,
H_lambda = -2 lambda(1+mu^2),
K_lambda = -3 mu H_lambda - gap q_lambda.
```

## 3. gamma_lambda

From

```text
gamma = lambda w^(-1) q^(-1/2),
```

logarithmic differentiation gives

```text
gamma_lambda
 = gamma [ 1/lambda
           - lambda(1-mu^2)/w^2
           - lambda mu^2/q ].
```

## 4. (gamma_t)_lambda

Define

```text
P = lambda/(w q^(3/2)).
```

Then

```text
gamma_t = -e P H
```

and

```text
P_lambda
 = P [ 1/lambda
       - lambda(1-mu^2)/w^2
       - 3 lambda mu^2/q ].
```

Therefore

```text
(gamma_t)_lambda
 = -e (P_lambda H + P H_lambda).
```

This product form is preferred over division by `H`; it remains valid where `H=0`.

## 5. (gamma_tt)_lambda

Define

```text
Q = lambda^3/(w q^(5/2)).
```

Then

```text
gamma_tt = e Q K
```

and

```text
Q_lambda
 = Q [ 3/lambda
       - lambda(1-mu^2)/w^2
       - 5 lambda mu^2/q ].
```

Thus

```text
(gamma_tt)_lambda
 = e (Q_lambda K + Q K_lambda).
```

Again this avoids division by `K`.

## 6. R derivatives

Set

```text
u = 1-gamma^2,
R = acos(gamma)/sqrt(u).
```

The already used first derivative is

```text
R_gamma = (gamma R - 1)/u.
```

Differentiate once more. With `n=gamma R-1`, `n_gamma=R+gamma R_gamma`, and `u_gamma=-2gamma`,

```text
R_gammagamma
 = [ (R + gamma R_gamma) u
     + 2 gamma (gamma R - 1) ] / u^2.
```

Hence

```text
R_lambda = R_gamma gamma_lambda,
(R_gamma)_lambda = R_gammagamma gamma_lambda.
```

At fixed surface endpoints where `u=0`, these expressions are interpreted by the removable analytic continuation used by the implementation chart; literal division by zero is forbidden.

## 7. Final lambda derivative

Differentiate

```text
G_t|_0 = s [4 mu R gamma_t
            -2(R_gamma gamma_t^2 + R gamma_tt)].
```

Since `s,mu` are lambda-independent,

```text
partial_lambda G_t|_0
 = s [
       4 mu (R_lambda gamma_t + R (gamma_t)_lambda)
       -2 (
            (R_gamma)_lambda gamma_t^2
            + 2 R_gamma gamma_t (gamma_t)_lambda
            + R_lambda gamma_tt
            + R (gamma_tt)_lambda
          )
     ].
```

Substituting the preceding formulas gives the implementation target for

```text
partial_lambda H_axis_ob(lambda)
 = integral_0^sqrt(2) partial_lambda G_t(s,0,lambda) ds.
```

## 8. Mandatory audit checks

An independent auditor should check, in order:

1. `H = mu(1+mu)-lambda^2(1+mu^2)` from the general `H` at `t=0`.
2. the signs and powers `q^(-3/2)` and `q^(-5/2)` in `gamma_t`, `gamma_tt`.
3. the `-3 lambda mu^2/q` coefficient in `P_lambda`.
4. the `-5 lambda mu^2/q` coefficient in `Q_lambda`.
5. `K_lambda = -3 mu H_lambda-gap q_lambda`.
6. the **plus** sign in `+2 gamma(gamma R-1)` in `R_gammagamma`.
7. the coefficient `2 R_gamma gamma_t (gamma_t)_lambda`.
8. absence of any `A_lambda` term because `A=1` after specialization to `t=0`.

## 9. Independent controls

`REPORTED_NOT_GATING`:

```text
H_axis_ob(0.3) ~ -0.24350
H_axis_ob(0.4) ~ -0.01973
H_axis_ob(0.5) ~ +0.23697
H_axis_ob(0.6) ~ +0.49623
H_axis_ob(0.8) ~ +0.96387
lambda_c^ob ~ 0.4079588603...
```

Exact sphere control:

```text
H_axis_ob(1)=4/3.
```

The exact sphere value follows independently from the known unit-ball center Hessian `D^2 E_B(0)=(4/3) I_3`; it is not generated from the oblate production evaluator.
