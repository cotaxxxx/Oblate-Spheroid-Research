# Monotone tube refinement machine receipt

Status: `MACHINE_GATING_PASS / NOT_AUDITED / NOT_BINDING`

This receipt records only the separately declared refinement run. It does not certify the theorem and it does not erase the failed initial contract.

## Pinned source

```text
source commit:
2f1186386a329a61a51d125245b5bc8971b6610e

refinement contract blob:
5808e84572b1428c58a9b4136b56c4b6f54339cb

producer blob:
c2fee40053ab055ce352e93e1c6d1fc43e46310a

independent checker blob:
fd778d6d3a2dc52ae38be87bf4eb800bfbdea6d3
```

## Pinned Actions receipt

```text
workflow run id: 33362970980
run number: 87
job id: 99397822892
step: Run separately declared monotone tube refinement
step conclusion: success
```

The step log records:

```text
Ran 1 test in 56.072s
OK
MONOTONE_TUBE_REFINEMENT unresolved producer boxes: 0
```

The same test constructs the producer record and then runs the independent checker over all 64 exact parameter boxes. The test succeeds only if the checker verifies every box with `total.upper() < 0` and the producer record reports `gating_pass = true`.

## Claim scope of this receipt

```text
quantity      = partial_t g_axis_ob(t,lambda)
t domain      = [63/64,1]
lambda domain = [5/8,33/50]
partition     = 8 exact t boxes x 8 exact lambda boxes
s partition   = inherited 1024-panel exact partition
precision     = producer 160 bits; checker 192 bits
u_star        = 3/5
required sign = NEG
sole gate     = every parameter-box total.upper() < 0
```

This supports the machine statement that the refinement implementation encloses the full Cartesian tube with negative upper endpoints on all 64 parameter boxes.

## Important workflow distinction

The overall workflow run concludes `failure` only because the subsequent step intentionally reruns the original fixed initial monotone-tube contract, which remains `UNRESOLVED` on all 64 boxes. That later failure does not negate the successful separately declared refinement step. Both records are retained.

## Remaining obligations

- external/raw audit of the refinement producer and independent checker;
- audit of the exact `A=(1-t)+t*s^2` intersection and the `u_star=3/5` chart policy;
- audit of termwise intersection on threshold-crossing cells;
- analytic C2-like justification for differentiating to `partial_t g` and passing the `t -> 1-` limit where required;
- census identification after the monotone-tube claim is accepted.

No `CERTIFIED` label may be assigned from this receipt alone.
