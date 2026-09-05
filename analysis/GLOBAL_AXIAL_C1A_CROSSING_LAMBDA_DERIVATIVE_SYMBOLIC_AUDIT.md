# Global axial C1a crossing lambda derivative — symbolic audit target

Status: `USER_SYMBOLIC_AUDIT_PASS / NOT_IMPLEMENTED / NOT_BINDING`

This note is the pre-implementation human-audit target for the C1a gate

```text
partial_lambda F_x(lambda) > 0,
F_x(lambda) := Phi(1/4,lambda) = 2 g_axis_ob(1/2,lambda),
lambda in [83/200,9/20].
```

The new lambda-derivative assembly below has now received an independent user symbolic/numerical audit.  This document remains an algebra audit only; no machine enclosure is promoted by this note.

## 1. Start from the already used first-t density

For the oblate axial gradient,

```text
g(t,lambda) = integral_0^sqrt(2) F_t(s,t,lambda) ds,
```

with

```text
F_t = s [ -mu alpha^2 - 2 A R gamma_t ],
alpha = acos(gamma),
R = acos(gamma)/sqrt(1-gamma^2).
```

The geometry variables used by the existing C0 producer are

```text
s2 = s^2,
mu = 1-s2,
e = 1-mu^2,
A = 1-t mu,
d = t-mu,
q = e + lambda^2 d^2,
w^2 = mu^2 + lambda^2 e,
gamma = lambda A/(w sqrt(q)),
N = -mu q - A lambda^2 d,
gamma_t = lambda N/(w q^(3/2)).
```

For C1a.2, `t=1/2` is fixed throughout. Thus `mu,e,A,d` are independent of lambda.

## 2. Basic lambda derivatives at fixed t

```text
q_lambda = 2 lambda d^2,
(w^2)_lambda = 2 lambda e,
w_lambda/w = lambda e/w^2.
```

Therefore

```text
gamma_lambda
 = gamma [ 1/lambda
           - lambda e/w^2
           - lambda d^2/q ].
```

## 3. Lambda derivative of gamma_t

Write

```text
L = lambda/(w q^(3/2)),
gamma_t = L N.
```

Since

```text
N = -mu q - A lambda^2 d,
```

we have

```text
N_lambda
 = -mu q_lambda - 2 A lambda d
 = -2 lambda (mu d^2 + A d).
```

Also

```text
L_lambda
 = L [ 1/lambda
       - lambda e/w^2
       - 3 lambda d^2/q ].
```

Hence

```text
(gamma_t)_lambda
 = L_lambda N + L N_lambda.
```

No `gamma_tt` or `(gamma_tt)_lambda` term enters C1a.2.

## 4. R and alpha-square derivatives

Set

```text
u = 1-gamma^2,
R = acos(gamma)/sqrt(u),
R_gamma = (gamma R - 1)/u.
```

Then

```text
R_lambda = R_gamma gamma_lambda.
```

Also

```text
partial_lambda(alpha^2)
 = -2 R gamma_lambda.
```

The removable `u=0` loci must use the same analytic continuation / positive-series chart as the C0/A kernels; literal division by zero is forbidden.

## 5. Final lambda derivative of the first-t density

Starting from

```text
F_t = s [ -mu alpha^2 - 2 A R gamma_t ],
```

the product rule gives

```text
partial_lambda F_t
 = s [
       2 mu R gamma_lambda
       - 2 A (
           R_gamma gamma_lambda gamma_t
           + R (gamma_t)_lambda
         )
     ].
```

Therefore at `t=1/2`,

```text
partial_lambda F_x(lambda)
 = 2 integral_0^sqrt(2) partial_lambda F_t(s,1/2,lambda) ds.
```

The outer factor `2` is part of the C1a crossing quantity.

## 6. Relation to the already audited A derivative

Reusable audited components from the center-axis lambda-derivative work are only

```text
q_lambda,
w_lambda/w,
gamma_lambda pattern,
R_lambda = R_gamma gamma_lambda,
series/direct removable-locus handling.
```

C1a.2 is not the A density `partial_lambda G_t|_{t=0}` and does not reuse its final product-rule assembly.

## 7. Reported numerical expectations — NOT GATING

Corrected independent controls:

```text
F_x(83/200) ~ -0.0507,
F_x(9/20)   ~ +0.0276,

partial_lambda F_x(83/200) ~ 2.2042426481,
partial_lambda F_x(9/20)   ~ 2.2642011538,

partial_lambda g(1/2,lambda) ~ 1.10 to 1.13
through lambda in [83/200,9/20].
```

The earlier `F_x(83/200) ~ -0.0089` control was from the superseded `t=5/16` edge and was not a `t=1/2` value.  The earlier derivative expectations `partial_lambda g ~ 0.52` and `partial_lambda F_x ~ 1.0` inherited the same stale-edge mixup.  None of these reported decimals is gating.

## 8. Independent audit result

`USER_SYMBOLIC_AUDIT_PASS`.

The independent implementation checked:

```text
1. gamma_lambda logarithmic derivative — PASS;
2. N_lambda = -2 lambda(mu d^2 + A d) — PASS;
3. L_lambda q-power coefficient -3 — PASS;
4. (gamma_t)_lambda = L_lambda N + L N_lambda — PASS;
5. partial_lambda(alpha^2) = -2 R gamma_lambda — PASS;
6. final partial_lambda F_t product rule — PASS;
7. outer factor 2 from F_x=2g(1/2,lambda) — PASS.
```

Independent formula evaluation and finite differences agreed to 12 digits.  Reported derivative values were

```text
partial_lambda F_x(83/200) = 2.2042426481...
partial_lambda F_x(9/20)   = 2.2642011538...
```

## 9. Evidence boundary

This document records a successful independent symbolic/numerical audit of the algebra only. It does not establish `partial_lambda F_x>0` by interval arithmetic, does not certify `lambda_x`, and does not alter any closed A/B/C0 result.
