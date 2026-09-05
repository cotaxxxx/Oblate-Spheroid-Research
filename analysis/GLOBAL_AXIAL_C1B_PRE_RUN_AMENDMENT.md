# C1b pre-run amendment — right clamp and boundary connection

Status: `PREDECLARED_AMENDMENT / MACHINE_NOT_RUN / NOT_BINDING`

This amendment is made before any binding C1b machine run. It supersedes only the C1b lambda-direction, tube-wall, boundary-connection, slab-cap, and corresponding resource-ceiling language in `analysis/GLOBAL_AXIAL_C1_CROSSING_TUBE_CONTRACT.md`. C1a is closed separately by its pinned machine receipt and is not reopened.

## 1. C1b parameter direction and target interval

C1a already covers the crossing bridge through `lambda_J = 9/20`. C1b therefore marches in the increasing-lambda direction from

```text
lambda = 9/20
```

to the certified boundary-band interface

```text
lambda = 5/8.
```

The C1b lambda domain is exactly

```text
lambda in [9/20,5/8].
```

The previous wording "march leftward toward the C1a crossing bracket" is superseded.

The initial exact slab width remains

```text
Delta_lambda = 1/800.
```

Since

```text
5/8 - 9/20 = 7/40 = 140/800,
```

the unrefined cover consists of exactly 140 coarse slabs.

## 2. Symmetric tube clamps

The nominal half-width remains fixed at

```text
w0 = 1/16.
```

For a rational predictor `t_c`, the binding tube walls are now

```text
t_minus = max(1/2, t_c - w0),
t_plus  = min(1,   t_c + w0).
```

Neither clamp changes `w0`; it only intersects the nominal tube with the physical axial interval `[1/2,1]`.

For every accepted slab `Lambda`, certify

```text
sup_{(t,lambda) in [t_minus,t_plus] x Lambda} partial_t g(t,lambda) < 0,
inf_{lambda in Lambda} g(t_minus,lambda) > 0,
```

and the right-wall gate according to the following exhaustive cases.

### 2.1 Unclamped right wall

If `t_c + w0 < 1`, require

```text
sup_{lambda in Lambda} g(t_plus,lambda) < 0.
```

### 2.2 Clamped right wall

If `t_c + w0 >= 1`, then `t_plus=1` and the right-wall condition is the one-sided endpoint value

```text
g(1,lambda) = B_ob(lambda) < 0.
```

The endpoint-regular two-chart `B_ob` kernel already used by the pinned boundary endpoint implementation is the required analytic representation. A finite-`t` surrogate for `t=1` may not replace this gate.

Let `lambda_B` be the smallest exact left endpoint among accepted C1b slabs whose right wall is clamped. If no slab is right-clamped, the `B_ob` extension gate is vacuous. Otherwise the machine run must certify

```text
B_ob(lambda) < 0 on [lambda_B,5/8].
```

The exact value of `lambda_B` is therefore a derived ledger value, not a decimal pre-run predictor. The `B_ob` certification must use exact rational lambda boxes whose union is exactly `[lambda_B,5/8]`.

No claim `g(31/32,lambda)>0` is extended below `lambda=5/8`.

## 3. Corner-hull requirement at t=1

Any tube-monotonicity box touching `t=1` also contains the singular-looking `t->1, s->0` corner in the raw variables. Such a box must use the already implemented endpoint-safe corner-hull treatment from the boundary monotone-tube refinement architecture on the first `s` panel at the upper `t` edge.

In particular, the binding C1b implementation must preserve the same analytic hull ingredients used there:

```text
chart label: corner_hull
R in [1,pi/2]
R_gamma in [-1,-1/3]
```

with the corresponding nonnegative square-root and rational hull constructions. The ordinary chart is not allowed to be forced through the corner merely to avoid a clamp-specific branch.

Producer and checker must each implement/transcribe this rule independently within their stated independence scope.

## 4. Connection to the certified boundary band

The C1b cover terminates at the exact interface

```text
lambda = 5/8.
```

At that lambda, the C1b root tube may extend into `[31/32,1]`; the already certified boundary band begins on

```text
(t,lambda) in [31/32,1] x [5/8,33/50].
```

Thus the two certificates overlap at `lambda=5/8` rather than requiring an invalid extension of the lower-edge sign gate to smaller lambda.

The C1b machine receipt must explicitly report this exact interface and verify that its final accepted slab ends at `5/8` with no lambda gap.

## 5. Slab caps after interval enlargement

The original `maximum accepted slabs = 64` cannot cover `[9/20,5/8]` at initial width `1/800`; it is superseded.

The lambda-refinement depth remains

```text
maximum lambda-refinement depth per coarse slab = 3,
refinement = exact bisection in lambda only.
```

There are exactly 140 coarse slabs. At depth 3, one coarse slab can have at most 8 accepted leaf slabs and at most 15 attempted nodes in its complete binary refinement tree. Therefore the amended absolute caps are

```text
MAX_COARSE_SLABS    = 140
MAX_ACCEPTED_SLABS  = 140 * 8  = 1120
MAX_ATTEMPTED_SLABS = 140 * 15 = 2100
```

These are safety ceilings, not target counts. A run exceeding any cap is `NOT_EVIDENCE`.

## 6. Resource ceiling

The pre-existing per-attempted-slab ceiling remains

```text
23,560,192 panel evaluations.
```

Accordingly the amended absolute C1b machine-work safety ceiling is

```text
2100 * 23,560,192 = 49,476,403,200 panel evaluations,
```

plus the separately reported `B_ob` extension-gate work. The `B_ob` work must have its own predeclared stage/box/panel ceiling before its first gating run; it may not be absorbed silently into the slab budget.

The accepted-leaf safety ceiling corresponding to 1120 accepted slabs is

```text
1120 * 23,560,192 = 26,387,415,040 panel evaluations.
```

External-workstation acceptance rules from the parent contract remain unchanged.

## 7. Receipt additions

In addition to the parent C1 receipt fields, a binding C1b receipt must record

```text
direction = increasing lambda
exact C1b lambda union = [9/20,5/8]
140-coarse-slab exact cover check
left-clamp events
right-clamp events
lambda_B, or NONE if no right clamp occurs
B_ob extension exact lambda cover and strict-negative worst upper bound
corner_hull counts for all t=1-touching tube boxes
final exact interface lambda = 5/8
MAX_COARSE_SLABS / MAX_ACCEPTED_SLABS / MAX_ATTEMPTED_SLABS
actual attempted and accepted slab counts
actual panel totals including B_ob extension work
```

## 8. No other weakening

This amendment does not alter

```text
T0/T1/T2 stage definitions,
w0 = 1/16,
predictor acceptance sup|t_c-T_*| <= 1/64,
root-localization limits,
E0/E1/E2 exterior policy,
producer precision 160 bits,
checker precision 192 bits,
Psi degree 50,
u-series threshold 3/5,
Arb arithmetic,
strict-sign requirements.
```

A later change to any of those rules requires another pre-run amendment.