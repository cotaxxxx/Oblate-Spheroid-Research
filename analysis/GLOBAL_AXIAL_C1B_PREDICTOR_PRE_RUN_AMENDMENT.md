# C1b predictor pre-run amendment

Status: `PREDECLARED_AMENDMENT / MACHINE_NOT_RUN / NOT_BINDING`

This amendment fixes the deterministic predictor-selection rule before the first full C1b branch-tube machine run. It does not alter any mathematical gate, tube width, refinement depth, precision, or work ceiling in the parent C1 contract or the right-clamp amendment.

## 1. Scope

The predictor is candidate-generation only. No predictor point evaluation is theorem evidence. Every accepted candidate must still pass the binding tube monotonicity, wall signs, certified root localization, and

```text
sup |t_c - T_*| <= 1/64
```

gate from the parent contract.

## 2. Three-step predictor rule

For each attempted lambda slab `Lambda=[lambda_L,lambda_R]`, use the following deterministic order.

### P0 — continuation

For the first coarse slab beginning at `lambda=9/20`, set

```text
t_cont = 9/16.
```

For every later attempted slab whose immediate left neighbour has an accepted certified root enclosure

```text
T_prev=[a,b],
```

set

```text
t_cont = (a+b)/2.
```

This is an exact rational continuation candidate.

### P1 — bracket scan

Independently scan the slab midpoint

```text
lambda_mid = (lambda_L+lambda_R)/2
```

on the fixed exact rational t grid

```text
t_k = 1/2 + k/1024,  k=0,...,512.
```

The scan uses ordinary high-precision point evaluation only to choose a candidate; it is explicitly non-gating. Find the first adjacent grid pair `[t_k,t_{k+1}]` with the expected post-crossing orientation

```text
g(t_k,lambda_mid) > 0,
g(t_{k+1},lambda_mid) < 0.
```

If no such pair is found, the predictor is unresolved and the permitted lambda-refinement rule is invoked.

### P2 — relocated candidate

Let `[p,q]` be the P1 sign-change pair and define

```text
t_scan = (p+q)/2.
```

If `|t_cont-t_scan| <= 1/64`, use

```text
t_c = t_cont,
predictor_mode = continuation.
```

Otherwise use

```text
t_c = t_scan,
predictor_mode = relocated.
```

Thus the scan can relocate a stale continuation predictor before the expensive binding tube test. The numerical P1 signs themselves do not discharge any C1b sign obligation.

## 3. Raw logging

Every attempted slab must print at least

```text
coarse_index / refinement_depth / exact lambda endpoints
P0 continuation candidate
P1 exact scan bracket, or NONE
P2 final rational t_c and predictor_mode
```

Every accepted slab additionally prints the certified root enclosure and the binding `sup|t_c-T_*|` value.

## 4. No weakening

The predictor rule cannot convert a failed binding gate into PASS. Failure at T2, wall failure, localization failure, predictor acceptance failure after permitted lambda refinement, or exterior failure remains `UNRESOLVED` under the existing contracts.
