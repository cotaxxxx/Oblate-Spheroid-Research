# C1c pre-run amendment — lower-half post-crossing exclusion

Status: `PREDECLARED_AMENDMENT / MACHINE_GATING_PASS / ASSEMBLY_PENDING_C1B / NOT_BINDING`

This amendment is made before the first C1c gating run. It adds the missing lower-half obligation to the global C1 assembly without changing any C0, C1a, C1b, boundary-band, tube, predictor, clamp, corner-hull, exterior, precision, or budget rule.

## 1. Missing domain and claim

C1c covers exactly

```text
(t,lambda) in [0,1/2] x [9/20,5/8].
```

Its strict machine gate is

```text
partial_t^3 g(t,lambda) < 0
```

on that full exact rectangle. The implementation must reuse the raw-audited C0a/C1a four-group Arb kernel with only the lambda box changed. No formula, chart, degree, denominator refactor, or finite-difference substitute is permitted.

## 2. Logical assembly

Write

```text
Phi(tau,lambda) = g(sqrt(tau),lambda)/sqrt(tau),  tau=t^2.
```

The same lower-half lemma used by C1a converts the strict C1c third-t-derivative gate into

```text
partial_tau Phi(tau,lambda) < 0
```

on `tau in [0,1/4]`.

C1c does not independently recertify the endpoint anchor. The assembly must obtain, for every lambda in `[9/20,5/8]`,

```text
Phi(1/4,lambda) = 2 g(1/2,lambda) > 0
```

from the accepted C1b exact slab ledger: either the left tube wall when `t_minus=1/2`, or the certified left exterior cover connecting `1/2` to the tube wall. The accepted C1b lambda slabs must have exact union `[9/20,5/8]`.

Consequently `Phi(tau,lambda)>0` on `[0,1/4]`, and hence `g(t,lambda)>0` for `t in (0,1/2]`. Thus there is no lower-half nonzero axial root on the C1c domain.

`LOGICAL_FINAL_C1C_ASSEMBLY=PASS` is forbidden unless both the C1c machine gate and the pinned C1b anchor/cover receipt pass.

## 3. Predeclared stages and ceiling

```text
A0: t_boxes=8,  lambda_boxes=8,  s_panels=512
A1: t_boxes=16, lambda_boxes=16, s_panels=1024
A2: t_boxes=32, lambda_boxes=32, s_panels=2048
```

The first stage with zero unresolved boxes is authoritative. If A2 has any unresolved box, C1c is `UNRESOLVED / NOT_BINDING` and no ad hoc stage may be added inside the same run.

The absolute panel-evaluation ceiling is

```text
8*8*512 + 16*16*1024 + 32*32*2048 = 2,392,064.
```

## 4. Arithmetic and independence

```text
producer precision = 160 bits
checker precision  = 192 bits
Psi series degree  = 50
u-series threshold = 3/5
arithmetic          = Arb
```

The producer and checker use their respective C0a four-group lineages. The checker must not import the producer. A transcribed checker is not an independent mathematical derivation; its independence scope is precision, partition execution, gating, and receipt comparison.

## 5. Mandatory receipt fields

A C1c machine receipt must record:

```text
amendment blob and commit
producer/checker/workflow blobs
checked-out head
dependency pins
exact t and lambda domains
precision, degree, threshold, stage declarations, and ceiling
first-passing stage
unresolved count at every attempted stage
worst upper enclosure and exact box
chart statistics
producer/checker first-stage agreement
LOGICAL_FINAL_C1C_MACHINE
```

The later assembly receipt must additionally pin the C1b receipt, its exact lambda union, its `t=1/2` positive-anchor supply for every accepted slab, and must distinguish tube uniqueness on the full `[t_minus,t_plus]` from the bookkeeping cut at `31/32`.

## 6. Abort rule

Any unresolved A2 box, ceiling excess, source/dependency pin mismatch, producer/checker disagreement, missing C1b exact cover, or missing positive `t=1/2` anchor leaves the corresponding machine or assembly claim `UNRESOLVED / NOT_BINDING`.

## 7. Pinned machine-gating result

```text
run id = 33652374082
run number = 3
run URL = https://github.com/cotaxxxx/bg-oblate-spheroid/actions/runs/33652374082
run HEAD = 3dec57ae76aa6d1e3254592f03eda7fef2eb736c
run status = success
run started = 2026-09-02T16:02:04Z
run updated = 2026-09-02T16:28:31Z
```

Run-time blob pins:

```text
amendment = f7568ac381884e35386de221277776765baf5c57
producer = fbffaccc6dfcfd1b7b9be5b362d8cb80d867aa62
checker = 3ecbda1b3e9acd8134fdd94505721b1780e14edc
workflow = b9de12fae75ce0268fc1b4d87257a057896e752c
requirements-prototype = e01c11e4c67774875b280ccc7603ffb29aa427f4
requirements-interval = 399cb56905e5cf6e71a2d59771fee1ea7c2834e0
```

The machine gate passed at A2 in both lineages. The global assembly remains pending until the pinned C1b receipt supplies the exact `[9/20,5/8]` lambda union and the positive `g(1/2,lambda)` anchor on every accepted slab.
