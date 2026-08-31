# Center-axis lambda derivative — symbolic audit target

Status: `USER_SYMBOLIC_AUDIT_PASS / NOT_BINDING`

This note is the human-audit target for Claim A3 in `CENTER_AXIS_COEFFICIENT_CONTRACT.md`. The independent audit identified and corrected one transcription error in the `t=0` specialization of `H`; the lambda-differentiation structure itself passed.

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

## 2. t=0 geometry — corrected specialization

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
H = mu(1+mu)(1-lambda^2),
K = -3 mu H - gap q,

gamma = lambda/(w sqrt(q)),
gamma_t = -lambda e H/(w q^(3/2)),
gamma_tt = lambda^3 e K/(w q^(5/2)).
```

The corrected `H` follows either directly from the general formula at `delta=1`,

```text
(1-s^2)(2-s^2) + lambda^2(3s^2-2-s^4)
 = mu(1+mu) - lambda^2(mu+mu^2)
 = mu(1+mu)(1-lambda^2),
```

or from `N=-s^2 H` and

```text
N = mu(lambda^2-q)
  = -mu(1-mu^2)(1-lambda^2).
```

Checks:

```text
q_lambda = 2 lambda mu^2,
(w^2)_lambda = 2 lambda(1-mu^2),
w_lambda/w = lambda(1-mu^2)/w^2,
H_lambda = -2 lambda mu(1+mu),
K_lambda = -3 mu H_lambda - gap q_lambda.
```

## 3. gamma_lambda

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

## 6. R derivatives

Set

```text
u = 1-gamma^2,
R = acos(gamma)/sqrt(u),
R_gamma = (gamma R - 1)/u.
```

Then

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

At the fixed surface endpoints where `u=0`, use the removable analytic continuation; literal division by zero is forbidden.

## 7. Final lambda derivative

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

Therefore

```text
partial_lambda H_axis_ob(lambda)
 = integral_0^sqrt(2) partial_lambda G_t(s,0,lambda) ds.
```

## 8. Independent audit result

The independent audit checked the corrected formulas and found:

- `P_lambda` and `Q_lambda` powers/coefficient structure correct;
- `R_gammagamma` correct, including the `+2 gamma(gamma R-1)` term;
- final product-rule assembly correct, including `2 R_gamma gamma_t (gamma_t)_lambda`;
- finite-difference agreement for `partial_lambda H_axis_ob` to about 15 digits at tested lambdas.

Reported derivative expectations from that independent calculation:

```text
partial_lambda H_axis_ob(0.4) ~ 2.467472463656
partial_lambda H_axis_ob(0.5) ~ 2.617190122360
```

## 9. Independent controls

`REPORTED_NOT_GATING`:

```text
H_axis_ob(0.3) ~ -0.24350
H_axis_ob(0.4) ~ -0.019734
H_axis_ob(0.5) ~ +0.236973
partial_lambda H_axis_ob(0.4) ~ 2.4675
partial_lambda H_axis_ob(0.5) ~ 2.6172
lambda_c^ob ~ 0.4079588603...
```

Exact sphere controls:

```text
H_axis_ob(1) = 4/3,
partial_lambda H_axis_ob(1) = 8/5.
```

The first follows from the unit-ball center Hessian `D^2 E_B(0)=(4/3) I_3`. The second is an independent sphere-limit control for the lambda derivative. Neither is generated from the production evaluator.

## 10. Evidence boundary

This document records a successful independent symbolic audit of the corrected algebra only. It does not promote any machine enclosure or theorem claim to `CERTIFIED` by itself.
