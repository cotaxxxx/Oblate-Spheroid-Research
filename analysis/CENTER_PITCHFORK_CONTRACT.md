# Center pitchfork certification contract B

Status: `PROTOTYPE / SYMBOLIC_DERIVATION_PENDING / NOT_BINDING`

## Purpose

This contract concerns the local center pitchfork at the certified parameter

```text
lambda_c^ob in (2/5,83/200)
```

from contract A.

By z -> -z symmetry,

```text
g_axis_ob(-t,lambda) = -g_axis_ob(t,lambda),
```

so near `t=0`

```text
g_axis_ob(t,lambda)
 = H_axis_ob(lambda) t
   + c3_ob(lambda) t^3
   + O(t^5),
```

with

```text
c3_ob(lambda) := (1/6) partial_t^3 g_axis_ob(0,lambda).
```

## Fixed machine target B1

Certify

```text
c3_ob(lambda) < 0
for lambda in [2/5,83/200].
```

This is a one-parameter interval claim on the same lambda interval used to isolate `lambda_c^ob` in A.

## Correct density order

The canonical notation is

```text
g_axis_ob(t,lambda) = integral_0^sqrt(2) F_t(s,t,lambda) ds,
G_t = partial_t F_t,
partial_t g_axis_ob = integral_0^sqrt(2) G_t ds.
```

Therefore the cubic coefficient is

```text
c3_ob(lambda)
 = (1/6) integral_0^sqrt(2)
     [partial_t^2 G_t(s,t,lambda)]_{t=0} ds
 = (1/6) integral_0^sqrt(2)
     [partial_t^3 F_t(s,t,lambda)]_{t=0} ds.
```

A single derivative `partial_t G_t` would correspond to `partial_t^2 g` and vanishes at `t=0` by oddness; it is not the cubic coefficient.

## Useful pre-limit organization

Write

```text
x = gamma,
x1 = gamma_t,
x2 = gamma_tt,
x3 = gamma_ttt,
x4 = gamma_tttt,
R1 = R_gamma,
R2 = R_gammagamma,
R3 = R_gammagammagamma,
C = R x1.
```

Since

```text
A = 1-t mu,
A_t = -mu,
A_tt = 0,
```

and

```text
G_t/s = 4 mu C - 2 A C_t,
```

two further t derivatives simplify to

```text
(partial_t^2 G_t)/s
 = 8 mu C_tt - 2 A C_ttt.
```

At `t=0`, `A=1`, with

```text
C_tt
 = R2 x1^3
   + 3 R1 x1 x2
   + R x3,

C_ttt
 = R3 x1^4
   + 6 R2 x1^2 x2
   + 3 R1 x2^2
   + 4 R1 x1 x3
   + R x4.
```

Hence the symbolic B density target is

```text
6 c3_ob(lambda)
 = integral_0^sqrt(2) s [
     8 mu (
       R2 gamma_t^3
       + 3 R1 gamma_t gamma_tt
       + R gamma_ttt
     )
     - 2 (
       R3 gamma_t^4
       + 6 R2 gamma_t^2 gamma_tt
       + 3 R1 gamma_tt^2
       + 4 R1 gamma_t gamma_ttt
       + R gamma_tttt
     )
   ]_{t=0} ds.
```

Thus B requires `gamma_tttt` in addition to `gamma_ttt`, and `R_gammagammagamma`; no fourth gamma-derivative of R is needed in this organization.

The symbolic derivation must start from the pre-limit geometry, derive `gamma_ttt` and `gamma_tttt`, and only then specialize to `t=0`. No machine implementation is authorized until this density is independently audited.

## Geometry / regularity inherited from A

On

```text
lambda in [2/5,83/200],
```

at `t=0`, retain

```text
q = 1-mu^2 + lambda^2 mu^2 >= lambda^2 > 0,
w^2 = mu^2 + lambda^2(1-mu^2) >= lambda^2 > 0.
```

There is no moving corner singularity. Fixed removable `u=1-gamma^2=0` loci are handled with the same analytic continuation / series chart philosophy as A. Endpoint and center removable loci must be covered explicitly by the symbolic and machine audit.

## Independent expectations — REPORTED_NOT_GATING

The following are expectations only and must not be used as proof gates:

```text
c3_ob(0.4)   ~ -0.252
c3_ob(lambda_c^ob) ~ -0.2614
c3_ob(0.415) ~ -0.270
c3_ob(0.5)   ~ -0.376
```

The observed nonzero axial root at `lambda=0.5`,

```text
t* ~ 0.7803,
```

is qualitatively consistent with the cubic approximation

```text
t*^2 ~ H_axis_ob(lambda)/|c3_ob(lambda)|.
```

This census comparison is diagnostic only.

## Direction / normal form consequence after B certification

Contract A certifies

```text
H_axis_ob(lambda_c^ob)=0,
partial_lambda H_axis_ob(lambda_c^ob)>0.
```

If B certifies

```text
c3_ob(lambda_c^ob)<0,
```

then the local reduced equation

```text
0 = t [ H_axis_ob(lambda)
        + c3_ob(lambda_c^ob) t^2
        + higher order terms ]
```

has the supercritical orientation with respect to increasing `lambda`: for `lambda>lambda_c^ob` sufficiently close to the critical parameter there is one local nonzero pair `+/- t*(lambda)`, while for `lambda<lambda_c^ob` sufficiently close there is no local nonzero pair.

The leading scaling is

```text
t*(lambda)^2
 ~ H_axis_ob(lambda)/|c3_ob(lambda_c^ob)|
 ~ [partial_lambda H_axis_ob(lambda_c^ob)/|c3_ob(lambda_c^ob)|]
    (lambda-lambda_c^ob).
```

The local theorem must be stated on an explicit neighborhood

```text
lambda in (lambda_c^ob-epsilon, lambda_c^ob+epsilon),
|t| < t0,
```

with exact uniqueness of the nonzero pair inside that neighborhood. The existence of such an `epsilon,t0` follows analytically from the odd real-analytic normal form once A transversality and B cubic nondegeneracy are established; any quantitative box used later by global cover C is a separate machine obligation.

## Sphere control

If an independent closed form for

```text
c3_ob(1)
```

is derived, it should be added as a gating containment control before B certification. Until independently derived and audited, no sphere `c3` value is assumed.

## Audit sequence

1. derive `gamma_ttt`, `gamma_tttt` and `partial_t^2 G_t|_{t=0}` from pre-limit formulas;
2. independently audit `R_gammagammagamma`, all product-rule coefficients, parity, and removable limits;
3. compare high-precision values against `REPORTED_NOT_GATING` expectations;
4. only then implement Arb producer/checker;
5. freeze partitions/precision before gating run;
6. record machine receipt;
7. external Judge review;
8. promote B only after `JUDGE_PASS`.

## Explicit exclusions

B does not by itself certify:

- the entire nonzero axial branch up to boundary entry;
- absence of additional roots outside the local center box;
- off-axis exclusion;
- global stationary-point census.

Those belong to C and D.
