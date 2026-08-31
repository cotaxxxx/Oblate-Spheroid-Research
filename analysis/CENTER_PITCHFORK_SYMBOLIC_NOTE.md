# Center pitchfork symbolic note B

Status: `SYMBOLIC_DERIVATION_READY_FOR_RAW_AUDIT / NOT_BINDING`

## Scope

This note is the symbolic/raw-audit target for contract B. It concerns only

```text
c3_ob(lambda) := (1/6) partial_t^3 g_axis_ob(0,lambda)
```

on

```text
lambda in [2/5,83/200].
```

By z -> -z symmetry,

```text
g_axis_ob(-t,lambda) = -g_axis_ob(t,lambda),
```

so near `t=0`

```text
g_axis_ob(t,lambda)
 = H_axis_ob(lambda) t
   + c3_ob(lambda) t^3
   + O(t^5).
```

The fixed machine target after raw audit is

```text
c3_ob(lambda) < 0
for lambda in [2/5,83/200].
```

No implementation is certified by this note.

## 1. Pre-limit notation

Use

```text
mu = 1-s^2,
A = 1-t mu,
q = 1-mu^2 + lambda^2(mu-t)^2,
w^2 = mu^2 + lambda^2(1-mu^2),
gamma = lambda A/(w sqrt(q)),
R = acos(gamma)/sqrt(1-gamma^2),
C = R gamma_t.
```

The axial gradient density is

```text
F_t = s[-mu alpha^2 - 2 A C],
```

with `alpha=acos(gamma)` and

```text
g_axis_ob(t,lambda) = integral_0^sqrt(2) F_t ds.
```

Since

```text
partial_t(-mu alpha^2) = 2 mu C,
A_t = -mu,
```

successive t derivatives are

```text
partial_t F_t
 = s[4 mu C - 2 A C_t],

partial_t^2 F_t
 = s[6 mu C_t - 2 A C_tt],

partial_t^3 F_t
 = s[8 mu C_tt - 2 A C_ttt].
```

Because the A-chain notation uses

```text
G_t := partial_t F_t,
```

we have

```text
partial_t^2 G_t = partial_t^3 F_t,
```

and therefore

```text
c3_ob(lambda)
 = (1/6) integral_0^sqrt(2)
     [partial_t^2 G_t]_{t=0} ds
 = (1/6) integral_0^sqrt(2)
     s[8 mu C_tt - 2 A C_ttt]_{t=0} ds.
```

At `t=0`, `A=1`.

## 2. C derivatives

For

```text
C = R(gamma) gamma_t,
```

we have

```text
C_t
 = R_gamma gamma_t^2 + R gamma_tt,
```

```text
C_tt
 = R_gammagamma gamma_t^3
   + 3 R_gamma gamma_t gamma_tt
   + R gamma_ttt,
```

and

```text
C_ttt
 = R_gammagammagamma gamma_t^4
   + 6 R_gammagamma gamma_t^2 gamma_tt
   + 3 R_gamma gamma_tt^2
   + 4 R_gamma gamma_t gamma_ttt
   + R gamma_tttt.
```

The coefficients `3` and `6,3,4` are part of the raw-audit target.

## 3. t=0 geometry

Set

```text
e = 1-mu^2,
q = 1-mu^2 + lambda^2 mu^2,
w^2 = mu^2 + lambda^2(1-mu^2).
```

Then `q>=lambda^2>0` and `w>=lambda>0` on the B interval.

The independently cross-checked t derivatives of

```text
gamma = lambda(1-t mu)/(w sqrt(1-mu^2 + lambda^2(mu-t)^2))
```

at `t=0` are:

```text
gamma_t
 = -lambda mu(1-mu^2)(1-lambda^2)
   /(w q^(3/2)),
```

```text
gamma_tt
 = lambda^3(1-mu^2)
   (2 lambda^2 mu^2 - 2 mu^2 - 1)
   /(w q^(5/2)),
```

```text
gamma_ttt
 = 3 lambda^3 mu(1-mu^2)
   (2 lambda^4 mu^2
    - lambda^2 mu^2
    - 3 lambda^2
    - mu^2
    + 1)
   /(w q^(7/2)),
```

```text
gamma_tttt
 = 3 lambda^5(1-mu^2)
   (8 lambda^4 mu^4
    + 4 lambda^2 mu^4
    - 24 lambda^2 mu^2
    - 12 mu^4
    + 9 mu^2
    + 3)
   /(w q^(9/2)).
```

These formulas were independently derived on both sides before this note.

## 4. R derivatives: gamma chart

Let

```text
u = 1-gamma^2.
```

Then

```text
R_gamma = (gamma R - 1)/u,
```

```text
R_gammagamma
 = [ (R + gamma R_gamma)u
     + 2 gamma(gamma R - 1) ]/u^2,
```

and the third derivative simplifies to

```text
R_gammagammagamma
 = [3 gamma(2 gamma^2 + 3)R
    - (11 gamma^2 + 4)]/u^3.
```

Literal evaluation at `u=0` is forbidden; use the analytic continuation / u-series chart below.

## 5. R derivatives: u/Psi chart

Define

```text
Psi(u) = asin(sqrt(u))/sqrt(u),
R = Psi(u).
```

Then

```text
R_gamma
 = -2 gamma Psi'(u),
```

```text
R_gammagamma
 = 4 gamma^2 Psi''(u) - 2 Psi'(u),
```

```text
R_gammagammagamma
 = -8 gamma^3 Psi'''(u) + 12 gamma Psi''(u).
```

The exact stable complement at `t=0` inherited from A is

```text
u = (1-mu^2) mu^2 (1-lambda^2)^2/(w^2 q) >= 0.
```

Thus the removable `u=0` loci are fixed. There is no moving corner singularity.

## 6. Psi series and Psi''' tail

Use the same positive-coefficient series as A,

```text
Psi(u) = sum_{n>=0} c_n u^n,
c_0 = 1,
c_{n+1} = c_n (2n+1)^2/[2(n+1)(2n+3)].
```

A already audits the tails for `Psi`, `Psi'`, `Psi''`. For `Psi'''`, if degree `N` is retained and `0<=u<=U`, the first omitted differentiated term is

```text
(N+1)N(N-1)c_{N+1} U^(N-2).
```

For the differentiated tail terms

```text
T_n = n(n-1)(n-2)c_n U^(n-3),
```

we have

```text
T_{n+1}/T_n
 = [(n+1)/(n-2)] [c_{n+1}/c_n] U
 < [(n+1)/(n-2)] U.
```

Hence a valid positive tail bound is

```text
Tail_Psi3
 <= (N+1)N(N-1)c_{N+1} U^(N-2)
    / [1 - U (N+2)/(N-1)].
```

For the intended A-compatible values

```text
N = 50,
U <= 3/5,
```

the denominator obeys

```text
1 - (3/5)(52/49)
 = 89/245
 > 0.
```

This exact denominator is a raw-audit control.

## 7. Factorized c3 density for implementation

Do not algebraically expand the full integrand. At `t=0`, evaluate in the factorized order

```text
C_tt
 = R_gammagamma gamma_t^3
   + 3 R_gamma gamma_t gamma_tt
   + R gamma_ttt,
```

```text
C_ttt
 = R_gammagammagamma gamma_t^4
   + 6 R_gammagamma gamma_t^2 gamma_tt
   + 3 R_gamma gamma_tt^2
   + 4 R_gamma gamma_t gamma_ttt
   + R gamma_tttt,
```

then

```text
D3_density
 = (s/6) [8 mu C_tt - 2 C_ttt],
```

and

```text
c3_ob(lambda)
 = integral_0^sqrt(2) D3_density(s,lambda) ds.
```

This factorized form is the canonical implementation target.

## 8. Machine target and evidence boundary

After raw audit, the only theorem gate for B is

```text
c3_ob(lambda) < 0
for every lambda in [2/5,83/200].
```

Equivalently, each covering Arb box must have strictly negative upper endpoint.

The following are `REPORTED_NOT_GATING` expectations only:

```text
c3_ob(2/5)        ~ -0.25187,
c3_ob(lambda_c^ob) ~ -0.26140,
c3_ob(83/200)     ~ -0.26989.
```

The additional diagnostic value

```text
c3_ob(0.5) ~ -0.376
```

may be retained for comparison but is outside the B gating interval.

## 9. Exact sphere control

For the unit sphere,

```text
alpha(t,mu)
 = atan( t sqrt(1-mu^2)/(1-t mu) ).
```

The exact center expansion is

```text
E_1(t)
 = E_1(0) + (2/3)t^2 - (2/9)t^4 + O(t^6),
```

so

```text
g_axis_ob(t,1)
 = (4/3)t - (8/9)t^3 + O(t^5).
```

Therefore

```text
c3_ob(1) = -8/9.
```

This is the fixed sphere containment control for B implementation. It is a control of evaluator normalization/continuation, not an assumption in the proof that `c3_ob<0` on `[2/5,83/200]`.

## 10. Raw-audit checklist

Before implementation, verify:

1. parity: `g_axis_ob` is odd in `t`;
2. derivative chain from `F_t` to `partial_t^3 F_t` has coefficients `4,6,8` as stated;
3. `C_tt` coefficients are `1,3,1`;
4. `C_ttt` coefficients are `1,6,3,4,1`;
5. all four `gamma` derivatives agree with independent derivation;
6. `R_gammagammagamma` agrees in gamma and Psi charts;
7. `Psi'''` tail bound and denominator `89/245` are correct;
8. fixed `u=0` removable loci are covered without literal singular division;
9. sphere control `c3_ob(1)=-8/9` is independently reproduced;
10. only the interval sign `upper(c3_ob)<0` is theorem-gating.

## 11. Consequence after B certification

Contract A already certifies

```text
H_axis_ob(lambda_c^ob)=0,
partial_lambda H_axis_ob(lambda_c^ob)>0.
```

If B certifies

```text
c3_ob(lambda_c^ob)<0,
```

then the odd analytic normal form gives a supercritical pitchfork with increasing `lambda`: for `lambda>lambda_c^ob` sufficiently close there is exactly one local nonzero pair `+/-t*(lambda)`, while for `lambda<lambda_c^ob` sufficiently close there is no local nonzero pair, and

```text
t*(lambda)^2
 ~ H_axis_ob(lambda)/|c3_ob(lambda_c^ob)|
 ~ [partial_lambda H_axis_ob(lambda_c^ob)/|c3_ob(lambda_c^ob)|]
    (lambda-lambda_c^ob).
```

Any explicit quantitative local box required by global axial cover C is a separate obligation.

## Explicit exclusions

This note does not certify:

- B machine implementation or any Arb enclosure;
- a quantitative epsilon/t0 local box;
- the global nonzero axial branch;
- connection to the boundary-entry branch;
- off-axis exclusion;
- any global stationary-point census.
