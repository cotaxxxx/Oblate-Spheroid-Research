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

## Chart policy

- Lower gamma chart may be used only on boxes where the checker proves `u=1-gamma^2` is separated from zero.
- Any box that can meet the moving `h_t=0` locus must use the factorized `u` chart with `R=Psi(u)` and `R_gamma=-2 gamma Psi_prime(u)`.
- The north-pole corner `(s,t)=(0,1)` is an explicit analytic/implementation obligation: no direct interval division by a `q` box containing zero is permitted. The implementation must use an algebraically regularized corner representation or a separately proved corner bound.

## Evidence handling

- Any mpmath point values are `REPORTED_NOT_GATING` only.
- The only gating predicate is `upper_endpoint < 0` for every one of the 64 exact parameter boxes.
- Failure of any single box leaves the tube `UNRESOLVED`; refinement must be declared separately rather than silently changing this fixed run.
