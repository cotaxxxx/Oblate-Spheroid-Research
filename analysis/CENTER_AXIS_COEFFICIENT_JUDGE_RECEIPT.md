# Center-axis coefficient Judge receipt

Status: `JUDGE_PASS / CERTIFIED_WITHIN_SCOPE`

## Scoped claim

For

```text
H_axis_ob(lambda) := partial_t g_axis_ob(0,lambda),
```

on `lambda in [1/4,1]`, there exists exactly one

```text
lambda_c^ob in (2/5,83/200)
```

such that

```text
H_axis_ob(lambda) < 0 for lambda < lambda_c^ob,
H_axis_ob(lambda) > 0 for lambda > lambda_c^ob.
```

Equivalently, the approved machine decomposition is

```text
partial_lambda H_axis_ob(lambda) > 0 on [1/4,1],
H_axis_ob(2/5) < 0,
H_axis_ob(83/200) > 0.
```

## Judge outcome

The external human reviewer approved the Judge request at commit

```text
06eae461deed6a343774d3f67c83f7921bc79bba
```

with the explicit judgment that the scoped request is approved after checking the receipt declaration that:

```text
CHECKER_KERNEL=TRANSCRIBED_COPY_NOT_INDEPENDENT_DERIVATION
INDEPENDENCE_SCOPE=PRECISION/PARTITION/GATING
```

The normalized certification outcome is:

```text
JUDGE_PASS
```

## Evidence basis acknowledged by Judge

Mathematical correctness is supported by the reviewer's independent symbolic derivation and finite-difference cross-checks. Machine evidence is supplied by both producer and checker passing the global derivative gate, the two point-sign gates, and both exact sphere containment controls.

Pinned machine receipt:

```text
analysis/CENTER_AXIS_COEFFICIENT_MACHINE_RECEIPT.md
commit d2321a12033b5ad3ad14e2282603aefcb2ebfdaa
```

Pinned audited source:

```text
commit 79234b601e4cd05d66e4dfa926184dd527e08588
producer blob 0b604f1dc17c8aba2825f25659b5d06a77c20c16
checker blob 3af01fbc62a77061ab6131ca442ff39f3e25a722
```

Focused machine run:

```text
run 33387236630
job center-axis-evidence
job id 99472510996
```

## Scope boundary

This receipt certifies only the sign structure and unique center axial degeneracy parameter on `[1/4,1]`. It does not certify:

- the cubic pitchfork coefficient;
- local nonzero branches;
- global axial census away from the center;
- connection to the boundary-entry bifurcation;
- off-axis exclusion;
- any statement for `lambda<1/4`;
- the non-gating decimal approximation of `lambda_c^ob`.

Those remain separate contracts.
