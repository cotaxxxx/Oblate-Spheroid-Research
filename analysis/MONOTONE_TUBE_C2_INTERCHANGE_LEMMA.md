# Monotone-tube C2 interchange lemma — analytic obligation

Status: `CHAT_ANALYTIC_DERIVATION_PASS / EXTERNAL_AUDIT_PENDING / NOT_BINDING`

This note supplies the analytic differentiation/interchange step needed to interpret the machine enclosure for the regularized second-t density as the one-sided quantity

```text
gt_boundary_ob(lambda) = partial_t g_axis_ob(1-,lambda)
```

and, more generally, to justify `partial_t g_axis_ob(t,lambda)` on the closed near-boundary tube

```text
t in [63/64,1], lambda in [5/8,33/50].
```

It is an analytic lemma only. It does not certify the Arb implementation and does not promote any machine result.

## 1. Pre-limit kernel and first derivative

Set

```text
mu    = 1-s^2,
delta = 1-t,
d     = t-mu = s^2-delta,
A     = 1-t*mu = delta + (1-delta)s^2,
q     = s^2(2-s^2) + lambda^2 d^2,
w^2   = lambda^2 s^2(2-s^2) + mu^2,
gamma = lambda A/(w sqrt(q)),
alpha = acos(gamma),
R     = alpha/sin(alpha).
```

For `t<1`, `q>0` for every `s in [0,sqrt(2)]`. The first-t derivative density is

```text
F_t = s[-mu alpha^2 - 2 A R gamma_t],
```

with

```text
N       = -mu q - A lambda^2 d = -s^2 H,
gamma_t = lambda N/(w q^(3/2)),
H       = (1-s^2)(2-s^2)
          + lambda^2(2s^2-2delta-s^4+delta s^2).
```

Thus `g_axis_ob(t,lambda)=integral F_t ds` for interior `t` by the already established C1-level differentiation argument.

## 2. Formal second-t derivative

For interior `t<1`, direct differentiation gives

```text
R_gamma = (gamma R - 1)/(1-gamma^2),
N_t     = -lambda^2 s^2(2-s^2),

gamma_tt
 = lambda^3 s^2[3 d H-(2-s^2)q]/(w q^(5/2)),

G_t := partial_t F_t
 = s[4 mu R gamma_t
     -2 A(R_gamma gamma_t^2 + R gamma_tt)].
```

The coefficient `4 mu` is the sum of the two identical `2 mu R gamma_t` contributions from differentiating `-mu alpha^2` and `-2 A R gamma_t`.

## 3. Corner-scaled identity

Define for `q>0`

```text
rho  = s/sqrt(q),
phi  = d/sqrt(q),
Ahat = A/sqrt(q).
```

Then exactly

```text
rho^2(2-s^2) + lambda^2 phi^2 = 1,
Ahat = (2-s^2)s rho - (1-s^2)phi.
```

Substitution into `G_t` removes every explicit negative power of `q`:

```text
T1 = -4(1-s^2) R lambda rho^3 H / w,

T2 = -2 R_gamma lambda^2 H^2 Ahat rho^5 / w^2,

T3 = -2 R lambda^3 Ahat rho^3
     [3 phi H-(2-s^2)sqrt(q)] / w,

G_t = T1+T2+T3.
```

These are algebraic identities for every `q>0`; the corner hull used by the machine code is an enclosure device for this same identity.

## 4. Uniform majorant on the north half `s in [0,1]`

Let

```text
lambda_- = 5/8,
lambda_+ = 33/50,
t in [63/64,1).
```

On `s in [0,1]`, `gap=2-s^2 in [1,2]`. The scaled identity implies

```text
0 <= rho <= 1,
|phi| <= 1/lambda_-,
|Ahat| <= 2 + 1/lambda_-.
```

Also

```text
w^2 = lambda^2(1-mu^2)+mu^2 >= lambda_-^2,
```

so `w>=lambda_-` uniformly.

The previously established elementary bound for this larger parameter rectangle applies:

```text
|H| <= 4.
```

Furthermore `0<=gamma<=1`, `alpha in [0,pi/2]`, hence

```text
1 <= R <= pi/2.
```

For the derivative quotient it is enough here to use the coarse global bound

```text
-1 <= R_gamma <= 0.
```

(The sharper `[-1,-1/3]` used by the corner machine hull is not needed for the analytic majorant.)

Finally, on this compact north rectangle,

```text
q = s^2(2-s^2)+lambda^2 d^2 <= 2,
```

so `sqrt(q)<=sqrt(2)` is a harmless uniform bound.

Consequently each of `T1,T2,T3` is bounded in absolute value by a constant depending only on `lambda_-` and `lambda_+`, not on `s,t,lambda`. For example one may take the explicit coarse bounds

```text
|T1| <= 4*(pi/2)*lambda_+*4/lambda_-,

|T2| <= 2*lambda_+^2*16*(2+1/lambda_-)/lambda_-^2,

|T3| <= 2*(pi/2)*lambda_+^3*(2+1/lambda_-)
        *[12/lambda_- + 2*sqrt(2)]/lambda_-.
```

Their sum is a finite constant `M_N`. Therefore

```text
|G_t(s,t,lambda)| <= M_N
```

uniformly on `s in [0,1]`, `t in [63/64,1)`, `lambda in [5/8,33/50]`.

This is an integrable majorant. The apparent corner singularity of the unscaled formula is therefore purely representational.

## 5. South half `s in [1,sqrt(2)]`

For `s>=1` and `delta<=1/64`,

```text
d = s^2-delta >= 63/64.
```

Hence

```text
q >= lambda_-^2(63/64)^2 > 0.
```

All quantities in the unscaled or scaled second derivative are therefore continuous on the compact set

```text
s in [1,sqrt(2)],
t in [63/64,1],
lambda in [5/8,33/50],
```

including the internal `gamma=1` locus when `R` and `R_gamma` are understood by their continuous `Psi/Psi_prime` extensions. Thus `|G_t|` has a finite compact-set bound `M_S` on the south half.

## 6. Differentiation under the integral and endpoint extension

For every interior `t<1`, the pre-limit density is smooth in `t`, and Sections 4–5 provide an integrable majorant for its second-t derivative that is uniform as `t` approaches `1`.

Therefore the standard dominated differentiation theorem gives

```text
partial_t g_axis_ob(t,lambda)
 = integral_0^sqrt(2) G_t(s,t,lambda) ds
```

for `t in [63/64,1)`.

For every fixed `s>0`, the regularized expression has a pointwise limit as `t->1-`. The uniform majorant `max(M_N,M_S)` permits dominated convergence, so

```text
lim_{t->1-} partial_t g_axis_ob(t,lambda)
 = integral_0^sqrt(2) G_boundary(s,lambda) ds.
```

The C1 endpoint lemma already supplies continuity of `g_axis_ob(t,lambda)` at `t=1`. Since the interior derivative has the finite limit above, the fundamental theorem of calculus on `[t,1)` gives

```text
[g_axis_ob(1,lambda)-g_axis_ob(t,lambda)]/(1-t)
 -> integral_0^sqrt(2) G_boundary(s,lambda) ds.
```

Thus the one-sided derivative exists and equals the endpoint integral:

```text
gt_boundary_ob(lambda)
 = partial_t g_axis_ob(1-,lambda)
 = integral_0^sqrt(2) G_boundary(s,lambda) ds.
```

The same majorant justifies the closed-tube interpretation of the machine quantity `partial_t g_axis_ob(t,lambda)` with the endpoint understood one-sidedly.

## 7. Scope and remaining audit

This lemma establishes the analytic bridge only. It does not assert the sign of the integral.

Required external checks before binding use:

1. line-by-line verification of the formal second-t derivative;
2. verification of the scaled identities for `T1,T2,T3`;
3. verification of the global bounds on `R` and the coarse bound `R_gamma in [-1,0]`;
4. confirmation that the existing C1 endpoint lemma supplies the continuity premise used in Section 6;
5. confirmation that the machine producer/checker enclose the same `G_t` density.

Until that audit is recorded, status remains `NOT_BINDING`.
