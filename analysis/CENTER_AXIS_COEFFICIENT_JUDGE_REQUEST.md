# Center-axis coefficient external Judge request

Status: `EXTERNAL_JUDGE_PENDING / NOT_BINDING`

## Request

Please independently review the center-axis coefficient certification chain for

```text
H_axis_ob(lambda) := partial_t g_axis_ob(0,lambda)
```

on

```text
lambda in [1/4,1].
```

The requested judgment is limited to the following theorem-level claim:

```text
There exists exactly one lambda_c^ob in (2/5,83/200)
such that
H_axis_ob(lambda) < 0 for lambda < lambda_c^ob,
H_axis_ob(lambda) > 0 for lambda > lambda_c^ob,
throughout [1/4,1].
```

Equivalently, Judge may approve the stronger machine decomposition

```text
partial_lambda H_axis_ob(lambda) > 0 on [1/4,1],
H_axis_ob(2/5) < 0,
H_axis_ob(83/200) > 0.
```

## Pinned materials

Machine receipt:

```text
analysis/CENTER_AXIS_COEFFICIENT_MACHINE_RECEIPT.md
commit d2321a12033b5ad3ad14e2282603aefcb2ebfdaa
```

Audited source commit:

```text
79234b601e4cd05d66e4dfa926184dd527e08588
```

Producer:

```text
producer/center_axis_coefficient_producer.py
blob 0b604f1dc17c8aba2825f25659b5d06a77c20c16
160-bit Arb
```

Checker:

```text
checker/center_axis_coefficient_checker.py
blob 3af01fbc62a77061ab6131ca442ff39f3e25a722
192-bit Arb
```

Contract:

```text
analysis/CENTER_AXIS_COEFFICIENT_CONTRACT.md
blob 342b2dc964f0e549836bc1100e8b628252aecf24
```

Symbolic audit:

```text
analysis/CENTER_AXIS_LAMBDA_DERIVATIVE_SYMBOLIC_AUDIT.md
blob 3d047b2ff24af46765795323c2f7a921bb437c3b
status USER_SYMBOLIC_AUDIT_PASS / NOT_BINDING
```

Focused successful Actions evidence:

```text
run 33387236630
job center-axis-evidence
job id 99472510996
head b491874f70fd0ad742870b26b68eaa7f4e5cbedf
```

The run head adds report-only reconstruction/workflow code; the audited producer/checker blobs are unchanged.

## Human audit status

The user performed an independent content-level audit and reported `PASS` for:

- the corrected t=0 specialization;
- the lambda derivative algebra;
- `Psi`, `Psi'`, `Psi''` coefficient/tail bounds;
- factorized `u=1-gamma^2` and removable endpoint handling;
- sphere controls;
- gating logic.

The checker independence scope is intentionally limited:

```text
CHECKER_KERNEL=TRANSCRIBED_COPY_NOT_INDEPENDENT_DERIVATION
INDEPENDENCE_SCOPE=PRECISION/PARTITION/GATING
```

The checker kernel is a transcribed copy, not an independent mathematical derivation. Mathematical derivation independence is supplied by the user's independent symbolic derivation and finite-difference checks. Judge should not interpret checker lineage alone as derivational independence.

## Exact machine facts to verify

Both producer and checker report the same weakest lambda box for the global derivative gate:

```text
[1/4,67/256]
```

with strictly positive lower endpoints. Exact midpoint/radius values for producer and checker are pinned in the machine receipt.

Both independently pass:

```text
H_axis_ob(2/5) < 0,
H_axis_ob(83/200) > 0,
H_axis_ob(1) enclosure contains 4/3,
partial_lambda H_axis_ob(1) enclosure contains 8/5.
```

The last two are gating sphere controls for evaluator normalization.

## Requested Judge checks

Please check only:

1. the pinned algebra/series representation and its removable continuation are mathematically valid on `[1/4,1]`;
2. the Arb partition/tail enclosures and sign tests imply `partial_lambda H_axis_ob>0` on the full interval and the two point signs;
3. the monotonicity + two point signs logically imply existence and uniqueness of `lambda_c^ob in (2/5,83/200)` and the global sign split on `[1/4,1]`;
4. the independence declaration accurately describes the producer/checker relationship.

## Explicit exclusions

Do not judge or certify from this request:

- the pitchfork normal-form coefficient at `lambda_c^ob`;
- existence or uniqueness of nonzero axial stationary roots away from the center;
- connection of that branch to the boundary-entry parameter;
- off-axis stationary-orbit exclusion;
- any statement for `lambda<1/4`;
- any numerical refinement `lambda_c^ob ~ 0.4079588603...` beyond its non-gating expectation status.

## Requested outcome vocabulary

If approved, please return an explicit

```text
JUDGE_PASS
```

for the scoped center-axis coefficient claim. Until such approval is recorded, all claims remain `NOT_BINDING` and no `CERTIFIED` label is to be used.
