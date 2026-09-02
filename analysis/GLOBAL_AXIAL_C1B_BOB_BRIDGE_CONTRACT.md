# C1b B_ob bridge gate contract

Status: `PREDECLARED_SUBGATE / MACHINE_NOT_RUN / NOT_BINDING`

This file predeclares the one-dimensional endpoint gate required by `analysis/GLOBAL_AXIAL_C1B_PRE_RUN_AMENDMENT.md` before its first machine run.

## Scope

The machine will certify the stronger statement

```text
B_ob(lambda) < 0 on [9/20,5/8].
```

This strictly contains every possible derived clamp interval `[lambda_B,5/8]`, so a passing result discharges the right-clamped wall gate for every C1b slab without making `lambda_B` part of this subgate's arithmetic.

The analytic kernel is the endpoint-regular two-chart `B_ob` kernel already used by `producer/endpoint_interval_producer.py` and independently reconstructed in the checker lineage. No finite-t surrogate is permitted.

## First-passing stages

Exact lambda partitions and s-panel counts are fixed as

```text
B0: lambda_boxes=16, s_panels=1024
B1: lambda_boxes=32, s_panels=2048
B2: lambda_boxes=64, s_panels=4096
```

The first stage for which every exact lambda box has `total.upper() < 0` is authoritative. If B2 has any unresolved/nonnegative box, this subgate is `UNRESOLVED` and C1b may not use a right-clamped wall as certified evidence.

Arithmetic:

```text
producer precision = 160 bits
checker precision  = 192 bits
series degree      = 50
arithmetic         = Arb
required sign      = NEG
```

The checker is a separately transcribed interval computation and is not an independent mathematical derivation.

## Work ceiling

If all stages run, the maximum number of s-panel evaluations per producer/checker is

```text
16*1024 + 32*2048 + 64*4096 = 344,064.
```

No additional hidden refinement is permitted in the same gating run.

## Mandatory output

Producer and checker must print, for every stage:

```text
stage label
lambda_boxes
s_panels
unresolved count
worst exact lambda box
worst Arb enclosure / upper endpoint
```

and finally

```text
C1B_BOB_FIRST_PASS <stage>
LOGICAL_FINAL_C1B_BOB PASS|UNRESOLVED
```

A later C1b receipt must pin this contract blob, producer/checker blobs, workflow/run identity, first-pass stage, worst strict-negative upper bound, and checker agreement.