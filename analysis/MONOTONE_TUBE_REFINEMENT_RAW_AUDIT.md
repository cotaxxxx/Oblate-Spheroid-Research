# Monotone tube refinement — raw audit receipt

Status: `OWNER_RAW_AUDIT_PASS / CHAT_RAW_AUDIT_PASS / EXTERNAL_JUDGE_PENDING / NOT_BINDING`

This receipt audits the separately declared monotone-tube refinement. It does not promote the result to CERTIFIED and does not replace the failed initial run.

## Attribution chronology

The repository-side implementation actor may record only `OWNER_RAW_AUDIT_PASS` before an independent chat-side raw read has occurred. `CHAT_RAW_AUDIT_PASS` is added only after that separate read.

For this receipt the chronology is:

1. repository/owner-side raw correspondence review: `OWNER_RAW_AUDIT_PASS`;
2. subsequent independent chat-side raw read of the refinement producer/checker: `CHAT_RAW_AUDIT_PASS`;
3. external Judge remains pending.

The earlier version of this receipt prematurely used the chat attribution before the chat-side raw read. That attribution-order error is corrected here; it did not affect the mathematical content or machine gating result.

## Pinned source

- refinement contract blob: `5808e84572b1428c58a9b4136b56c4b6f54339cb`
- refinement producer blob: `c2fee40053ab055ce352e93e1c6d1fc43e46310a`
- refinement checker blob: `fd778d6d3a2dc52ae38be87bf4eb800bfbdea6d3`
- machine run: Actions #87, run id `33362970980`
- machine result: refinement step SUCCESS, `MONOTONE_TUBE_REFINEMENT unresolved producer boxes: 0`
- scope: `partial_t g_axis_ob(t,lambda) < 0` only on `[63/64,1] x [5/8,33/50]`

## Raw correspondence audit

### 1. Contract and partition

Producer and checker both enforce:

```text
t domain      = [63/64, 1]
lambda domain = [5/8, 33/50]
t boxes       = 8 exact boxes
lambda boxes  = 8 exact boxes
s panels      = 1024 inherited exact partition
series degree = 50
producer bits = 160
checker bits  = 192
u_star        = 3/5
required sign = NEG
sole gate     = every parameter-box total.upper() < 0
```

Checker reconstructs the 64 exact `(t,lambda)` boxes, checks labels and chart inventories, and independently recomputes each enclosure before applying the sign gate.

### 2. Ordinary algebra

Both implementations form the same exact quantities `e,gap,mu,d,lambda^2,A,q,w^2,w,h_t,H` using separate producer/checker helper lineages.

For ordinary boxes both require `q.lower() > 0` and tighten

```text
A = 1 - t*mu
A = (1-t) + t*s^2
```

by interval intersection before forming `gamma` and `Ahat=A/sqrt(q)`.

Both then intersect the factorized `u` enclosure with the gamma-derived enclosure and reciprocally tighten gamma from `u`.

### 3. Three-term density

Producer and checker match term-by-term:

```text
rho  = s/sqrt(q)
phi  = d/sqrt(q)
Ahat = A/sqrt(q)

T1 = -4 mu R lambda rho^3 H / w
T2 = -2 R_gamma lambda^2 H^2 Ahat rho^5 / w^2
T3 = -2 R lambda^3 Ahat rho^3 [3 phi H - gap sqrt(q)] / w
```

No standalone `q^(-5/2)` expression is used.

### 4. Chart policy

Both implementations use exactly `u_star=3/5`:

- `u.upper() <= 3/5` -> `u_upper`;
- `u.lower() >= 3/5` -> `gamma_lower`;
- threshold crossing -> evaluate both valid charts and intersect `T1,T2,T3` term by term;
- only one admissible chart -> use that chart and record a distinct crossing label;
- no admissible chart -> abort/unresolved.

Upper chart:

```text
R       = Psi(u)
R_gamma = -2 gamma Psi_prime(u)
```

with degree 50 and rigorous remainder.

Lower chart:

```text
R       = acos(gamma)/sqrt(u)
R_gamma = (gamma R - 1)/u
```

with the explicit precondition `u.lower() > 0`.

### 5. Corner chart

The last t-box / first s-cell only is sent to `corner_hull` on both sides.

Both use:

```text
rho in [0, 1/sqrt(gap.lower())]
phi in [-1/lambda, 1/lambda]
Ahat = gap*s*rho - mu*phi
R in [1, pi/2]
R_gamma in [-1, -1/3]
sqrt(q) in [0, sqrt(q_upper)]
```

and the same three-term density. No division by a q interval containing zero occurs in the corner chart.

### 6. Producer/checker separation

The refinement checker does **not** import the refinement producer. It reuses the pre-existing independent checker lineage (`checker.monotone_tube_interval_checker`) for low-level Arb helpers, series, quantities, corner handling and exact partitions. The refinement producer analogously reuses the producer lineage. Thus the producer/checker separation remains across the two lineages.

### 7. Gating

No diagnostic expectation is gating. The only machine predicate is

```text
total.upper() < 0
```

for all 64 exact parameter boxes. Actions #87 reports zero unresolved refinement boxes and the independent checker step passed.

## Audit conclusion

Content-level raw correspondence: `PASS`.

Evidence status remains:

```text
MACHINE_GATING_PASS
OWNER_RAW_AUDIT_PASS
CHAT_RAW_AUDIT_PASS
EXTERNAL_JUDGE_PENDING
NOT_BINDING
```

No `CERTIFIED` claim is authorized by this receipt. The analytic C2-like differentiation/interchange obligation remains separate and open.
