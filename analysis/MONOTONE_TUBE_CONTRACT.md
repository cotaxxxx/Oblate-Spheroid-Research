# Monotone tube contract — oblate axial boundary branch

Status: `FIXED_BEFORE_IMPLEMENTATION / NOT_BINDING`

## Claim scope

This stage proves only local uniqueness in a near-boundary tube. It does not claim existence of a root for every lambda in the tube projection.

```text
quantity      = partial_t g_axis_ob(t,lambda)
t domain      = [63/64, 1]
lambda domain = [5/8, 33/50]
required sign = NEG
gating        = every rigorous (t,lambda)-box enclosure has upper endpoint < 0
```

Consequent use, only after certification: for each fixed lambda there is at most one positive-axis stationary root inside `t in [63/64,1]`.

## Exact parameter partition fixed before run

- `delta = 1/64`.
- Split `t in [63/64,1]` into 8 equal exact rational boxes of width `1/512`.
- Split `lambda in [5/8,33/50]` into 8 equal exact rational boxes. Since the total width is `7/200`, each lambda box has width `7/1600`.
- For each of the 64 parameter boxes, split `s in [0,sqrt(2)]` using the inherited 1024-panel exact partition and chart seam at `s=1`.
- Initial Arb precision: 160 bits.
- Upper-series degree: 50, using the retained `Psi` and `Psi_prime` coefficient formulae and rigorous geometric remainder rule.

No box may be dropped because a census root is absent there. The tube claim is a uniform derivative-sign claim on the complete Cartesian product.

## General-t identities fixed before implementation

With

```text
mu = 1-s^2
e = s^2
d = t-mu = e-(1-t)
A = 1-t*mu
q = 1-mu^2 + lambda^2 d^2
w^2 = lambda^2(1-mu^2)+mu^2
```

use the exact identities

```text
w^2 q - lambda^2 A^2
  = (1-mu^2) (mu + lambda^2(t-mu))^2,

1-gamma^2
  = e(2-e) h_t^2/(w^2 q),

h_t = mu + lambda^2 d,

N = -mu q - A lambda^2 d = -e H,

N_t = -lambda^2(1-mu^2) = -lambda^2 e(2-e).
```

The moving internal `gamma=1` locus is `h_t=0`; in delta notation its positive solution satisfies

```text
s0(t)^2 = (1-lambda^2(1-t))/(1-lambda^2).
```

Boxes crossing this locus must use the `u` series chart rather than the scalar quotient form for `R_gamma`.

## Corner-hull chart fixed before implementation

The only zero of `q` in the present tube/cell geometry is the north-pole corner `(s,delta)=(0,0)`, where `delta=1-t`. The density is bounded there; the singularity is an interval-dependency artifact. On any `s`-cell / `t`-box containing that corner, direct construction of `s/sqrt(q)` or `d/sqrt(q)` is forbidden.

Define formally

```text
rho  = s/sqrt(q)
phi  = d/sqrt(q)
Ahat = A/sqrt(q)
```

and use the exact relation

```text
rho^2 (2-s^2) + lambda^2 phi^2 = 1.
```

Hence the corner box may use the a-priori hulls

```text
0 <= rho <= 1/sqrt(2-s^2),
-1/lambda <= phi <= 1/lambda.
```

Also use the exact identity

```text
A = s^2(2-s^2) - d(1-s^2),
```

which gives

```text
Ahat = (2-s^2) s rho - (1-s^2) phi.
```

Thus `Ahat` is formed from bounded hull quantities, not by dividing an `A` interval by a `sqrt(q)` interval containing zero.

Starting from

```text
G_t = s[4 mu R gamma_t - 2 A(R_gamma gamma_t^2 + R gamma_tt)],
N = -s^2 H,
gamma_tt = lambda^3 s^2[3 d H-(2-s^2)q]/(w q^(5/2)),
```

the three terms become exactly

```text
T1 = -4 mu R lambda rho^3 H / w,

T2 = -2 R_gamma lambda^2 H^2 Ahat rho^5 / w^2,

T3 = -2 R lambda^3 Ahat rho^3
     [3 phi H - (2-s^2) sqrt(q)] / w.
```

These are the required symbolic correspondences for the `corner_hull` chart. The corner implementation must compute neither `rho` nor `phi` as interval quotients. `sqrt(q)` itself may be used only multiplicatively in `T3`, where an upper enclosure is harmless.

### Corner angle bounds

The corner does **not** have a single limiting gamma value. Since

```text
gamma = lambda Ahat / w,
```

one has `gamma=1` along `s=0, delta>0`, while along `delta=0, s->0` one has `gamma->0`. Hence a corner box can span the full geometric range `0<=gamma<=1`. The corner chart must therefore not use either the lower quotient `R_gamma=(gamma R-1)/(1-gamma^2)` or the upper `Psi_prime` series as a pointwise chart across the whole corner box.

Instead use the exact global analytic hulls valid for `0<=gamma<=1`:

```text
1 <= R = acos(gamma)/sqrt(1-gamma^2) <= pi/2,
-1 <= R_gamma <= 0.
```

For the second bound, write `gamma=cos(alpha)`, `0<=alpha<=pi/2`. Then `gamma R = alpha cot(alpha) <= 1`, so `R_gamma<=0`; and `R>=gamma` gives `gamma R >= gamma^2`, hence `R_gamma>=-1`. These global bounds remove both endpoint quotient problems and are intentionally coarse; the corner cell contribution is controlled by its small `s` width and the bounded `rho`, `phi`, `Ahat` factors.

The corner chart is used only for boxes whose Cartesian product contains `(s,t)=(0,1)`. All other boxes use the ordinary general-t quotient formulas, with the moving `gamma=1` locus handled by the factorized upper `u` chart.

## Chart policy

The rigorous cover therefore has three chart labels:

1. `gamma_lower`: ordinary general-t boxes with `u=1-gamma^2` rigorously separated from zero;
2. `u_upper`: boxes that can meet the moving `h_t=0` locus, with `R=Psi(u)` and `R_gamma=-2 gamma Psi_prime(u)`;
3. `corner_hull`: only the north-pole corner box(es), using bounded `rho`, `phi`, `Ahat` together with the global angle hulls `R in [1,pi/2]`, `R_gamma in [-1,0]`.

No direct interval division by a `q` box containing zero is permitted in any chart.

## Evidence handling

- Any mpmath point values are `REPORTED_NOT_GATING` only.
- The only gating predicate is `upper_endpoint < 0` for every one of the 64 exact parameter boxes.
- Failure of any single box leaves the tube `UNRESOLVED`; refinement must be declared separately rather than silently changing this fixed run.
