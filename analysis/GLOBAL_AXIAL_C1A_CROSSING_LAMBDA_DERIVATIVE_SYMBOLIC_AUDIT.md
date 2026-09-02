# Global axial C1a crossing lambda derivative — symbolic audit target

Status: `AWAITING_USER_SYMBOLIC_AUDIT / NOT_IMPLEMENTED / NOT_BINDING`

This note is the pre-implementation human-audit target for the C1a gate

```text
partial_lambda F_x(lambda) > 0,
F_x(lambda) := Phi(1/4,lambda) = 2 g_axis_ob(1/2,lambda),
lambda in [83/200,9/20].
```

No machine implementation of this new lambda-derivative density is to be used as C1 evidence before this symbolic target is independently checked.

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

For C1a.2, `t=1/2` is fixed throughout.  Thus `mu,e,A,d` are independent of lambda.

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

This is the general-fixed-t analogue of the `t=0` formula already audited for Claim A.

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

and `mu,A,d` are lambda-independent at fixed t,

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

No `gamma_tt` or `(gamma_tt)_lambda` term enters C1a.2; those belonged to the center-axis second-density derivative used in Claim A.

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

For the first term of `F_t`, differentiate `alpha^2 = acos(gamma)^2` directly:

```text
partial_lambda(alpha^2)
 = -2 R gamma_lambda.
```

The removable `u=0` loci must be handled by the same analytic continuation / positive-series chart already used by the C0/A kernels; literal division by zero is forbidden.

## 5. Final lambda derivative of the first-t density

Starting from

```text
F_t = s [ -mu alpha^2 - 2 A R gamma_t ],
```

with `mu_lambda=A_lambda=0` at fixed `t`, the product rule gives

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

Equivalently, using `R_lambda=R_gamma gamma_lambda`,

```text
partial_lambda F_t
 = s [
       2 mu R gamma_lambda
       - 2 A (R_lambda gamma_t + R (gamma_t)_lambda)
     ].
```

Therefore at `t=1/2`,

```text
partial_lambda g(1/2,lambda)
 = integral_0^sqrt(2) partial_lambda F_t(s,1/2,lambda) ds,
```

and because

```text
F_x(lambda) = 2 g(1/2,lambda),
```

we have

```text
partial_lambda F_x(lambda)
 = 2 integral_0^sqrt(2) partial_lambda F_t(s,1/2,lambda) ds.
```

The outer factor `2` is part of the C1a crossing quantity and must not be omitted in the producer/checker reporting.

## 6. Relation to the already audited A derivative

Reusable audited components from the center-axis lambda-derivative work are only the analytic architecture and common identities:

```text
q_lambda,
w_lambda/w,
gamma_lambda pattern,
R_lambda = R_gamma gamma_lambda,
series/direct removable-locus handling.
```

C1a.2 is NOT the A density `partial_lambda G_t|_{t=0}`.  In particular C1a.2 does not reuse the A final product-rule assembly and does not require `R_gammagamma`, `gamma_tt`, or `(gamma_tt)_lambda`.

The new algebra requiring independent audit here is specifically:

```text
N_lambda = -2 lambda (mu d^2 + A d),
L_lambda = L[1/lambda - lambda e/w^2 - 3 lambda d^2/q],
(gamma_t)_lambda = L_lambda N + L N_lambda,
partial_lambda(alpha^2) = -2 R gamma_lambda,
partial_lambda F_t
 = s[2 mu R gamma_lambda
     -2A(R_gamma gamma_lambda gamma_t + R(gamma_t)_lambda)].
```

## 7. Reported numerical expectations — NOT GATING

The following are independent point-evaluation expectations supplied before implementation.  They are controls only and cannot certify C1a:

```text
partial_lambda g(1/2,lambda) ~ +0.52
through lambda in [83/200,9/20], approximately,

partial_lambda F_x(lambda) ~ +1.0,

F_x(83/200) ~ -0.0089,
F_x(9/20)   ~ +0.0276.
```

The eventual Arb producer should report these endpoint quantities and derivative margins, but containment of these decimal expectations is not itself a gate.

## 8. Required independent audit before implementation

Please check independently:

```text
1. gamma_lambda logarithmic derivative;
2. N_lambda at fixed t;
3. L_lambda q-power coefficient 3;
4. (gamma_t)_lambda product rule;
5. partial_lambda(alpha^2) sign and factor 2;
6. final partial_lambda F_t assembly;
7. outer factor 2 from F_x=2g(1/2,lambda).
```

Only after this note receives an explicit independent symbolic pass should the new C1a derivative density be implemented in producer/checker code.

## 9. Evidence boundary

This document is a symbolic audit target only.  It contains no machine certification, does not establish `partial_lambda F_x>0`, does not certify `lambda_x`, and does not alter any closed A/B/C0 result.
