# Census lower-edge refinement contract — corrected v2

Status: `FIXED_BEFORE_REFINEMENT_RUN / NOT_BINDING`

The corrected one-box v2 run is retained as `UNRESOLVED`. This is a separately declared lambda refinement; it does not rewrite that failed contract.

## Claim scope

```text
quantity      = g_axis_ob(63/64,lambda)
lambda domain = [5/8,33/50]
required sign = POS
gating        = every exact lambda-box enclosure has lower endpoint > 0
```

## Fixed partition

```text
lambda boxes  = 256 exact equal boxes
box width     = 7/51200
s panels      = 1024 inherited exact partition
series degree = 50
producer bits = 160
checker bits  = 192
u_star        = 3/5
```

No adaptive subdivision is authorized in this run. If any one box fails, the refinement is `UNRESOLVED`.

The choice 256 is fixed before the run. It is motivated only by the independently reported left-end value `g(63/64,5/8) ~ +4.37e-4`; this value is `REPORTED_NOT_GATING` and is not used by the checker.

## Corrected first-t density

For

```text
rho=s/sqrt(q),
gamma_t=-lambda s^2 H/(w q^(3/2)),
```

use

```text
F_t = -s mu alpha^2 + 2 lambda A R rho^3 H/w.
```

The factor is `A`, not `Ahat=A/sqrt(q)`. The superseded v1 receipt used `Ahat` and is invalid.

## Chart policy

Use the same rigorous policy as the monotone-tube refinement:

```text
u_hi <= 3/5 -> u_upper
u_lo >= 3/5 -> gamma_lower
crossing     -> evaluate both admissible charts and intersect the density enclosures
```

with exact tightening

```text
A = intersection(1-t*mu, (1-t)+t*s^2),
u = intersection(factorized complement, 1-gamma^2),
gamma = intersection(raw gamma, sqrt(1-u)).
```

At `t=63/64`, q is uniformly positive, so no corner hull is needed.

## Evidence handling

- The sole gate is positivity of every checker-recomputed lambda-box lower endpoint.
- The minimum lower endpoint and its lambda box must be printed in the workflow log.
- Producer and checker remain on separate lineages.
- No Judge request may be issued unless all 256 boxes pass.
- No `CERTIFIED` status follows from this machine run alone.
