# Global axial C1 crossing / branch-tube contract

Status: `PREDECLARED_CONTRACT / MACHINE_NOT_RUN / NOT_BINDING`

This file fixes the C1 machine policy before any C1 gating run is used as evidence.

Pre-run amendment: the C1a crossing lambda-derivative density must pass an independent symbolic audit before implementation, and C1b may be executed on a pinned external workstation under the acceptance rules in Section 7.1.  No stage, sign, refinement, width, or budget rule is changed by this amendment.

## 1. Scope

C1 is the axial middle-cover bridge immediately to the right of the closed C0 box.  Its fixed parameter interval is

```text
lambda in [83/200, 9/20].
lambda_J = 9/20.
```

The fixed axial middle domain is

```text
t in [1/2, 31/32].
```

C1 does not reopen C0 and does not alter any previously certified A/B/C0 statement.

C1 is split into two logically separate obligations.

```text
C1a = crossing bridge at t = 1/2.
C1b = unique nonzero axial branch tube plus sign-definite exterior cover.
```

C1 does not certify off-axis exclusion, the boundary band `[31/32,1]`, or any statement outside the displayed lambda interval.

## 2. Fixed notation

Let

```text
g(t,lambda) := g_axis_ob(t,lambda),
Phi(tau,lambda) := g(t,lambda)/t,  tau=t^2,
F_x(lambda) := Phi(1/4,lambda) = g(1/2,lambda)/(1/2).
```

The crossing parameter `lambda_x` is the unique zero sought for `F_x` on

```text
[83/200, 9/20].
```

The right-hand census anchor is

```text
lambda_J = 9/20.
```

For C1b, a predictor supplies a rational center `t_c` on each lambda slab.  The nominal tube half-width is fixed before the run as

```text
w0 = 1/16.
```

The tube walls are

```text
t_minus = max(1/2, t_c - w0),
t_plus  = t_c + w0.
```

No automatic narrowing of `w0` is permitted in a gating run.  A failed wall-separation test is not repaired by shrinking the tube.

## 3. C1a — crossing bridge

### C1a.1 Reused third-t derivative gate

Reuse the raw-audited C0a four-group Arb kernel with only the lambda box changed to

```text
t in [0,1/2],
lambda in [83/200,9/20].
```

The required sign is

```text
partial_t^3 g(t,lambda) < 0.
```

No formula change, chart change, degree change, or denominator refactor is allowed merely for C1a.

Predeclared stages:

```text
A0: t_boxes=8,  lambda_boxes=8,  s_panels=512
A1: t_boxes=16, lambda_boxes=16, s_panels=1024
A2: t_boxes=32, lambda_boxes=32, s_panels=2048
```

The first stage with zero unresolved boxes is authoritative.  If A2 has any unresolved box, C1a aborts and this contract must be revised before further gating work.

Maximum C1a.1 panel evaluations if all stages run:

```text
8*8*512 + 16*16*1024 + 32*32*2048 = 2,392,064.
```

### C1a.2 Crossing function and lambda monotonicity

Certify

```text
F_x(83/200) < 0,
F_x(9/20) > 0,
partial_lambda F_x(lambda) > 0 on [83/200,9/20].
```

The `partial_lambda F_x` certification is a new first-density lambda derivative at fixed `t=1/2`; it is not the center-axis second-density derivative used for Claim A.  Before producer/checker implementation, the algebra in

```text
analysis/GLOBAL_AXIAL_C1A_CROSSING_LAMBDA_DERIVATIVE_SYMBOLIC_AUDIT.md
```

must receive an explicit independent symbolic pass.  Until then C1a.2 remains `NOT_IMPLEMENTED / NOT_BINDING`.

After that audit, implementation must use Arb, the same stable `R/R_gamma` series/direct architecture used by the certified A/C0 kernels, and a separately transcribed checker.  A finite-difference derivative is diagnostic only and cannot gate C1a.

Reported independent controls, explicitly non-gating:

```text
F_x(83/200) ~ -0.0089,
F_x(9/20)   ~ +0.0276,
partial_lambda g(1/2,lambda) ~ +0.52,
partial_lambda F_x(lambda)   ~ +1.0.
```

Predeclared derivative stages:

```text
D0: lambda_boxes=16, s_panels=1024
D1: lambda_boxes=32, s_panels=2048
D2: lambda_boxes=64, s_panels=4096
```

First zero-unresolved stage is authoritative.  Endpoint signs use point boxes with

```text
s_panels=8192.
```

Maximum derivative-stage panel evaluations:

```text
16*1024 + 32*2048 + 64*4096 = 344,064.
```

Endpoint-sign allowance:

```text
2*8192 = 16,384 panel evaluations.
```

### C1a.3 Certified enclosure of lambda_x

After the two endpoint signs and `partial_lambda F_x>0` are certified, isolate the unique zero by exact rational bisection.

Predeclared policy:

```text
initial bracket = [83/200,9/20]
maximum bisection steps = 16
point-sign s_panels = 8192
target: opposite certified signs at the final exact-rational bracket endpoints
```

No decimal root value participates in gating.

Maximum bisection allowance:

```text
16*8192 = 131,072 panel evaluations.
```

Thus the predeclared C1a total ceiling is

```text
2,392,064 + 344,064 + 16,384 + 131,072 = 2,883,584 panel evaluations.
```

## 4. C1b — branch tube

### C1b.1 Initial geometry

The non-binding diagnostic established that `w0=1/16` is the first tested width with comfortable wall separation near `lambda_J`; `w=3/64` was thinner and `w=1/32` failed the right-wall sign enclosure.  These observations motivate `w0`; they are not C1b evidence.

The diagnostic stand-in `t_c=9/16` is not automatically accepted as the binding predictor.  The binding candidate must pass the acceptance rule below.

### C1b.2 Lambda slab policy

March from `lambda_J` leftward toward the certified C1a crossing bracket using exact rational slabs.

Predeclared initial slab width and refinement limits:

```text
initial Delta_lambda = 1/800
maximum accepted slabs = 64
maximum lambda-refinement depth per attempted slab = 3
refinement = exact bisection in lambda only
```

Slabs must form an exact contiguous cover with no gaps or overlaps except shared endpoints.  The final leftmost slab may be clipped to the certified `lambda_x` bracket / crossing bridge interface.

If 64 accepted slabs are insufficient, or depth 3 is exhausted with an unresolved candidate, C1b aborts; the cap may not be silently increased.

### C1b.3 Tube monotonicity and wall separation

For every accepted slab `Lambda`, certify simultaneously

```text
sup_{(t,lambda) in T(Lambda)} partial_t g(t,lambda) < 0,
inf_{lambda in Lambda} g(t_minus,lambda) > 0,
sup_{lambda in Lambda} g(t_plus,lambda) < 0,
```

where

```text
T(Lambda) = [t_minus,t_plus] x Lambda,
```

with the left clamp `t_minus=max(1/2,t_c-w0)`.

Predeclared tube stages per attempted slab:

```text
T0: t_boxes=8,  lambda_boxes=4,  s_panels=4096
T1: t_boxes=16, lambda_boxes=8,  s_panels=4096
T2: t_boxes=32, lambda_boxes=16, s_panels=8192
```

Wall evaluations use the same lambda partition as the corresponding T-stage and the same `s_panels` value.

The first stage at which all tube boxes and both walls are resolved with the required strict signs is authoritative.

Maximum tube-density panel allowance per attempted slab:

```text
8*4*4096 + 16*8*4096 + 32*16*8192 = 4,849,664.
```

Maximum two-wall allowance per attempted slab:

```text
2*(4*4096 + 8*4096 + 16*8192) = 360,448.
```

### C1b.4 Predictor acceptance

Wall separation alone is not sufficient to accept a census predictor.  Once strict tube monotonicity and wall signs give a unique root `t_*(lambda)` in the tube, produce a certified root enclosure `T_*` over the slab by exact t-bisection / interval sign evaluation.

Predeclared root-localization policy:

```text
maximum t-bisection steps = 12
maximum lambda boxes used in the localization = 16
s_panels = 8192
target enclosure width <= w0/8
```

The predictor is accepted only if the certified enclosure verifies

```text
sup |t_c - T_*| <= w0/4 = 1/64.
```

Here `sup |t_c-T_*|` means the maximum distance from the rational predictor `t_c` to either endpoint of the certified root enclosure over the slab.

This rule is deliberately stricter than mere root containment.  In particular, a predictor displaced too far to the left must be recentered or the lambda slab refined; the right wall may not be allowed to become thin merely because the root still lies inside the nominal tube.

Maximum localization allowance per attempted slab:

```text
12*16*8192 = 1,572,864 panel evaluations.
```

If the predictor-acceptance inequality fails, the permitted repair order is:

```text
1. refine the lambda slab by exact bisection;
2. recompute/recenter the predictor by the predeclared predictor rule;
3. rerun the same fixed-width w0 tube tests.
```

Shrinking `w0`, changing the acceptance constant `1/4`, or increasing the refinement cap is forbidden inside the same gating run.

## 5. C1b exterior cover

For each accepted branch slab, remove the certified root tube and prove that every remaining middle-domain box is sign definite:

```text
left exterior:  g(t,lambda) > 0,
right exterior: g(t,lambda) < 0.
```

The exterior domain is the exact remainder of

```text
[1/2,31/32] x Lambda
```

after removing the interior of the accepted tube.  Shared tube-wall boundaries are already certified by the wall gates.

Predeclared exterior policy per slab:

```text
E0: initial t_boxes=24, lambda_boxes=8, s_panels=1024
E1: bisect unresolved boxes once, s_panels=2048
E2: bisect unresolved boxes once again, s_panels=4096
maximum live/terminal exterior boxes over E0-E2 = 4096
```

Refinement is local: resolved boxes are never recomputed solely because another box is unresolved.

Absolute exterior panel-evaluation ceiling per attempted slab:

```text
4096 terminal/live boxes * 4096 s_panels = 16,777,216.
```

This ceiling is intentionally conservative; the machine receipt must report actual box counts and panel evaluations by stage.

Any exterior box still unresolved after E2 aborts C1b.  No ad hoc fourth stage is allowed.

## 6. Global C1b resource ceiling

Per attempted slab, the declared worst-case allowance is

```text
tube density   4,849,664
walls            360,448
root location  1,572,864
exterior      16,777,216
-----------------------
total         23,560,192 panel evaluations.
```

With the hard cap of 64 accepted slabs, the accepted-slab ceiling is

```text
64 * 23,560,192 = 1,507,852,288 panel evaluations.
```

Refined failed attempts must also be reported separately in the receipt.  The workflow must enforce a separate global attempted-slab cap of

```text
MAX_ATTEMPTED_SLABS = 128.
```

Therefore the absolute C1b machine-work ceiling, including failed refined attempts, is

```text
128 * 23,560,192 = 3,015,704,576 panel evaluations.
```

This is a safety ceiling, not a target workload.  Because this ceiling is not assumed to fit inside hosted Actions wall-time, C1b is permitted to run on an external workstation under Section 7.1 without changing any mathematical gate or budget.

## 7. Arithmetic / checker architecture

Unless a later pre-run amendment explicitly tightens these values, C1 uses

```text
producer precision = 160 bits
checker precision  = 192 bits
Psi series degree  = 50
u-series threshold = 3/5
arithmetic          = Arb
```

The checker must reproduce exact coverage, first-pass stage choice, strict signs, candidate acceptance, and resource counts with an independently transcribed kernel where one already exists.  As in A/C0, a transcribed checker is not to be described as an independent mathematical derivation.

### 7.1 External-workstation execution acceptance

C1b may be run outside GitHub Actions, including on the designated external high-performance workstation, provided the run starts from a fully pinned repository state and emits a receipt sufficient to reproduce the environment.

Mandatory pre-run acceptance conditions:

```text
1. exact git HEAD is recorded before execution;
2. git status --short is empty before execution;
3. branch/ref name is recorded;
4. contract blob and contract commit are recorded;
5. producer/checker blobs are recorded;
6. requirements-prototype.txt and requirements-interval.txt blobs are recorded;
7. installed Python version is recorded;
8. installed mpmath and python-flint versions are recorded;
9. package hashes / the same hash-pinned requirement files are used;
10. producer/checker precision, DEG, USTAR, all stage declarations, w0, slab caps, and work ceilings are echoed before numerical work;
11. host CPU/OS metadata and start/end timestamps are recorded;
12. no source file, requirement file, contract, or executable parameter is modified during the accepted run.
```

The authoritative source identity is the recorded Git commit plus blob pins, not the machine name.  A local run from a dirty tree, an unrecorded HEAD, an unpinned dependency environment, or altered stage/budget parameters is `NOT_EVIDENCE` even if all numerical signs appear to pass.

For a long C1b execution, periodic checkpoint files are permitted only as resumability artifacts.  Acceptance after resume requires the checkpoint to pin the same HEAD, contract blob, producer/checker blobs, dependency pins, precision, stage declarations, exact slab ledger, accumulated resource ledger, and next unresolved slab.  A resume that changes any gating parameter is a new run and requires a pre-run contract amendment.

Hosted Actions may still be used for C1a and for focused C1b smoke/diagnostic runs.  Such focused runs do not replace the full external C1b evidence unless they themselves satisfy the complete declared cover and receipt requirements.

## 8. Mandatory machine receipt fields

A C1 machine receipt must pin at least:

```text
contract blob and commit
producer/checker blobs
workflow blob, or external-run launcher/script blob when Actions is not used
requirements blobs and package hashes
run id / job id when Actions is used; external run label / host metadata otherwise
checked-out head and clean-tree precondition
precision and all stage declarations
C1a first-pass stages and unresolved counts
C1a worst boxes and sign margins
certified exact-rational lambda_x bracket
C1b exact slab list and exact union/coverage check
predictor t_c for every slab
certified T_* enclosure for every accepted slab
sup |t_c-T_*| and acceptance result
w0 and left-clamp events
tube worst partial_t g upper bound
left-wall worst g lower bound
right-wall worst g upper bound
exterior box counts / unresolved counts / worst margins
actual panel-evaluation totals
checkpoint/resume lineage if any
checker agreement and stated independence scope
```

## 9. Abort conditions

The run is `UNRESOLVED / NOT_BINDING` if any of the following occurs:

```text
C1a symbolic lambda-derivative audit has not passed before implementation/evidence use;
C1a A2 unresolved;
C1a D2 unresolved;
endpoint signs do not bracket a crossing;
partial_lambda F_x is not strictly positive;
lambda_x bisection cannot maintain certified opposite signs;
C1b tube monotonicity fails at T2;
either tube wall lacks its strict sign at T2;
predictor error exceeds w0/4 after lambda-refinement depth 3;
root localization width exceeds w0/8;
any exterior box remains unresolved after E2;
exact slab union/coverage check fails;
accepted slab count exceeds 64;
attempted slab count exceeds 128;
any declared work ceiling is exceeded;
external execution begins from a dirty tree or unrecorded HEAD;
external dependency/source/stage pins do not match the declared run identity.
```

A failed condition may not be converted to PASS by an unannounced partition, width, precision, formula, or budget change.

## 10. Existing evidence used only as inputs

C1 may rely on already closed upstream results, including the certified center-axis coefficient contract and the closed C0 result, but must pin their exact receipts/commits in the eventual machine receipt.

The non-binding C1b width diagnostic near `lambda_J` is design evidence only.  It selected `w0=1/16`; it is not part of the logical C1 proof.

## 11. Intended logical output

If C1a and C1b both pass, the requested C1 logical conclusion is limited to:

```text
- a unique simple crossing lambda_x of F_x at t=1/2 on [83/200,9/20];
- a unique axial nonzero root inside every accepted post-crossing tube slab;
- certified predictor proximity sup |t_c-T_*| <= 1/64;
- no additional axial roots in the middle-domain exterior [1/2,31/32] on the exactly covered C1b slabs;
- exact connection of the post-crossing branch cover to the lambda_J anchor.
```

It does not, by itself, certify the boundary band, off-axis uniqueness, or a global stationary-point census.
