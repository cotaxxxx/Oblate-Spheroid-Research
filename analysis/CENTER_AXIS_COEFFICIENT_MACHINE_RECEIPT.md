# Center-axis coefficient machine receipt

Status: `MACHINE_GATING_PASS / USER_AUDIT_PASS / EXTERNAL_JUDGE_PENDING / NOT_BINDING`

## Scope

This receipt concerns only

```text
H_axis_ob(lambda) := partial_t g_axis_ob(0,lambda)
```

on `lambda in [1/4,1]`, its strict lambda-monotonicity, endpoint signs at `2/5` and `83/200`, and the resulting unique zero `lambda_c^ob in (2/5,83/200)`.

It does not certify the center pitchfork normal form, the global nonzero axial branch, off-axis exclusion, or any theorem outside `[1/4,1]`.

## Audited source pin

Audited source commit:

```text
79234b601e4cd05d66e4dfa926184dd527e08588
```

Producer:

```text
producer/center_axis_coefficient_producer.py
blob 0b604f1dc17c8aba2825f25659b5d06a77c20c16
precision 160 bits
```

Checker:

```text
checker/center_axis_coefficient_checker.py
blob 3af01fbc62a77061ab6131ca442ff39f3e25a722
precision 192 bits
```

Contract:

```text
analysis/CENTER_AXIS_COEFFICIENT_CONTRACT.md
blob 342b2dc964f0e549836bc1100e8b628252aecf24
```

Symbolic audit note:

```text
analysis/CENTER_AXIS_LAMBDA_DERIVATIVE_SYMBOLIC_AUDIT.md
blob 3d047b2ff24af46765795323c2f7a921bb437c3b
status USER_SYMBOLIC_AUDIT_PASS / NOT_BINDING
```

## Checker independence declaration

```text
CHECKER_KERNEL=TRANSCRIBED_COPY_NOT_INDEPENDENT_DERIVATION
INDEPENDENCE_SCOPE=PRECISION/PARTITION/GATING
```

The checker does not import the producer kernel, series, tail, or partition. It reconstructs the partition and evaluates the same transcribed formulas at higher precision. The mathematical derivation was independently audited by the user, including finite-difference checks of the lambda derivative.

## Human raw audit

User raw audit of the pinned producer/checker source: `PASS`.

Audited items include:

- Taylor coefficient recurrence for `Psi(u)=asin(sqrt(u))/sqrt(u)`;
- positive geometric tail bounds for `Psi`, `Psi'`, and `Psi''` at `u<=3/5`, degree 50;
- corrected `H=mu(1+mu)(1-lambda^2)` and `K=-3 mu H-(1+mu)q`;
- factorized complement `u=(1-mu^2) mu^2 (1-lambda^2)^2/(w^2 q)`;
- removable continuation at fixed `u=0` loci;
- `R_gamma=-2 gamma Psi'`, `R_gammagamma=4 gamma^2 Psi''-2 Psi'`;
- all lambda derivative terms, including the `-3`, `-5`, and cross term `2 R_gamma gamma_t (gamma_t)_lambda`;
- checker precision, independent partition reconstruction, and gating logic.

## Machine run pin

Focused evidence run:

```text
GitHub Actions run 33387236630
job center-axis-evidence
job id 99472510996
head commit b491874f70fd0ad742870b26b68eaa7f4e5cbedf
```

The head differs from the audited source commit only by report-only reconstruction/workflow additions. The audited producer/checker blobs above are unchanged.

All focused steps completed with `SUCCESS`:

```text
Run center-axis producer
Run independent center-axis checker
Report exact center-axis enclosures
```

## Gating claims

The proof decomposition is the stronger lemma

```text
A0: partial_lambda H_axis_ob(lambda) > 0 on [1/4,1],
```

together with

```text
H_axis_ob(2/5) < 0,
H_axis_ob(83/200) > 0.
```

Then the original contract claims A1 and A2 follow by monotonicity, and A3 is the restriction of A0 to `[2/5,83/200]`.

### Producer exact enclosures

Weakest derivative box:

```text
lambda box = [1/4,67/256]
mid = 1.4988001248326236703234720440936328285486077810985013851870345479423775084375209
rad = 1.2168929856270551681518554687500000000000000000000000000000000000000000000000000
```

Hence its lower endpoint is strictly positive.

Point `lambda=2/5`:

```text
mid = -0.019726495260655184251735597119334994526999779061645221099858195973322968783068065
rad = 0.0059856576481251977384090423583984375000000000000000000000000000000000000000000000
```

Point `lambda=83/200`:

```text
mid = 0.017615553230052575633518844783125104081572592146623653459444521721879080986614579
rad = 0.0058854636154137551784515380859375000000000000000000000000000000000000000000000000
```

Sphere `H_axis_ob(1)` control:

```text
mid = 1.3333379266542818150987798042301569253348381138821381384613664267724743851725684
rad = 0.0029582415700133424252271652221679687500000000000000000000000000000000000000000000
contains 4/3
```

Sphere `partial_lambda H_axis_ob(1)` control:

```text
mid = 1.5999971246164512257408688386171391189870363623832167525592700451315926300023571
rad = 0.014687572256661951541900634765625000000000000000000000000000000000000000000000000
contains 8/5
```

### Checker exact enclosures

Weakest derivative box:

```text
lambda box = [1/4,67/256]
mid = 1.4988001248310325453916085183659700060394422880555594256078481284872151789608333
rad = 1.2168929837644100189208984375000000000000000000000000000000000000000000000000000
```

Point `lambda=2/5`:

```text
mid = -0.019726495261167165837576222241868520315520362658455028696839471294443402585583732
rad = 0.0059856576626771129667758941650390625000000000000000000000000000000000000000000000
```

Point `lambda=83/200`:

```text
mid = 0.017615553230543683664969302437987278968025362419086576617314195174810037647038707
rad = 0.0058854636154137551784515380859375000000000000000000000000000000000000000000000000
```

Sphere `H_axis_ob(1)` control:

```text
mid = 1.3333379266542818150987798042301569253348381138835065939926150125610718493883442
rad = 0.0029582415700133424252271652221679687500000000000000000000000000000000000000000000
contains 4/3
```

Sphere `partial_lambda H_axis_ob(1)` control:

```text
mid = 1.5999971246164512257408688386171391189870363638144535421431126375718817506379683
rad = 0.014687572227558121085166931152343750000000000000000000000000000000000000000000000
contains 8/5
```

## Logical consequence

The machine gates and audited algebra establish the candidate implication

```text
partial_lambda H_axis_ob(lambda) > 0 for all lambda in [1/4,1],
H_axis_ob(2/5) < 0,
H_axis_ob(83/200) > 0.
```

Therefore there is exactly one

```text
lambda_c^ob in (2/5,83/200)
```

with

```text
H_axis_ob(lambda) < 0 for lambda < lambda_c^ob,
H_axis_ob(lambda) > 0 for lambda > lambda_c^ob,
```

throughout the contract domain `[1/4,1]`.

This receipt remains `NOT_BINDING` until external Judge approval. No `CERTIFIED` label is asserted here.
