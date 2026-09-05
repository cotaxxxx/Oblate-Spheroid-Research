# Global axial cover C0 — machine receipt

Status: `CHAT_RAW_AUDIT_PASS / MACHINE_GATING_PASS / EXTERNAL_JUDGE_PENDING / NOT_BINDING`

## Scoped claim

This receipt supports only the two C0 gates

```text
C0a: partial_t^3 g_axis_ob(t,lambda) < 0
     for every (t,lambda) in [0,1/2] x [2/5,83/200].

C0b: g_axis_ob(1/2,lambda)/(1/2) < 0
     for every lambda in [2/5,83/200].
```

In the contract notation `Phi(tau,lambda)=g_axis_ob(t,lambda)/t` with `tau=t^2`, C0b is `Phi(1/4,lambda)<0`; the producer log labels the same edge quotient as `Phi(t=1/2)<0`.

Together with already closed contracts A and B, these gates give the quantitative center-pitchfork box on `|t|<=1/2`, `lambda in [2/5,83/200]`. They do not certify the middle axial region above `t=1/2` or any off-axis statement.

## Contract pin

```text
analysis/GLOBAL_AXIAL_COVER_C0_QUANTITATIVE_PITCHFORK_CONTRACT.md
blob 95ee0472526cacc721c2544ff6fab8f983a11cf5
fixed box: t in [0,1/2], tau in [0,1/4], lambda in [2/5,83/200]
T_EDGE = 1/2
```

The historical old-edge run `33446730602` is `HISTORICAL_UNRESOLVED_CONTROL / NOT_EVIDENCE` and is not used here.

## Evidence commit and cleanup pin

Authoritative evidence head:

```text
commit b8a25658a67cec2d750eef7c5b5ce037dfc6cadf
message Clean C0 receipt producer diagnostics
parent e5b5d4d3736d6c74e623803815a9539e5d1dc714
```

This commit removes only receipt-noise diagnostics from the V2 producer and the now-dead K3 infinity diagnostic path:

```text
removed producer output/helpers:
  PT_TEST
  BOX_TEST_*
  BOX_CANDIDATE_*
  HULL_TEST_*
  CTX_PREC

removed report-only path:
  C0A_K3_INF_DIAGNOSTIC
```

The C0 stage schedule, gate logic, K0 factorization, K1/K2 recurrence, K3 formula, checker, and workflow are otherwise unchanged. The previously withdrawn independent workflow step `Run corrected lower-edge 256-box refinement` had already been removed in parent-lineage commit `e5b5d4d3736d6c74e623803815a9539e5d1dc714`.

## Machine source pins

Workflow:

```text
.github/workflows/oblate-global-axial-c0.yml
blob 3f9ebc5d1b9167283b402dce46d538e0efe62dfd
```

Producer wrapper:

```text
producer/global_axial_c0_producer_v2.py
blob cdbdf51f8656c1fcae97666cc1846461b250a591
```

Producer base:

```text
producer/global_axial_c0_producer.py
blob c4c8d6b59d3829e1843d149b7857eda5800287aa
Arb precision 160 bits
Psi degree 50
USTAR 3/5
```

Producer four-group kernel:

```text
producer/c0a_four_group_v2.py
blob 2bb556ab4f0c0cfd9ce6afa65d762551dd3791f4
K0 exact factorized Horner numerator
positive-q endpoint powers for q^4,q^5,q^6,q^(9/2),q^(11/2)
```

Checker wrapper:

```text
checker/global_axial_c0_checker_v2.py
blob fbec890588d2d390ea67bc90116b80bb37ebf9cc
```

Checker base:

```text
checker/global_axial_c0_checker.py
blob 85978625e029b01c8ae40fa8234566f10eea251c
Arb precision 192 bits
Psi degree 50
USTAR 3/5
```

Checker four-group kernel:

```text
checker/c0a_four_group_v2.py
blob 18e66b6450cd2a379bbb869a99e4e5ce6999f6e5
```

Checker independence must be interpreted exactly as the runtime declaration:

```text
CHECKER_KERNEL=TRANSCRIBED_COPY_NOT_INDEPENDENT_DERIVATION
INDEPENDENCE_SCOPE=PRECISION/PARTITION/GATING
```

The V2 C0a kernel is separately transcribed in the checker, but this receipt does not upgrade the checker to an independently derived mathematical proof. Derivational support is the exact raw audit plus the audited C0 contract.

## Dependency and runner pins

Requirements:

```text
requirements-prototype.txt
blob e01c11e4c67774875b280ccc7603ffb29aa427f4
mpmath==1.4.1
sha256 dc4f0ea2304480d4a9a48a94c1020571558ade522b44a6912efac63a586e140f

requirements-interval.txt
blob 399cb56905e5cf6e71a2d59771fee1ea7c2834e0
python-flint==0.9.0
sha256 376b88cacd30612479e839ffdba887599d3f9c8c0e214852bf80bb2b194e4d76
```

Actions run environment recorded by the successful job:

```text
Ubuntu 24.04.4 LTS
runner image ubuntu-24.04 version 20260823.283.1
CPython 3.12.14
actions/checkout@v4 resolved SHA 11d5960a326750d5838078e36cf38b85af677262
actions/setup-python@v5 resolved SHA a26af69be951a213d495a4c3e4e4022e16d87065
```

## Raw audit pin and result

```text
analysis/c0a_four_group_raw_audit.py
blob 26002379307379c9a1cb05a7644fa638e7a0fa9a
```

Run output:

```text
PASS exact_fraction_cases 16
PASS eight_term_equals_four_group
PASS K0_K1_K2_K3_common_denominators
PASS K0_factorized_numerator_exact_fraction_cases 64
PASS K0_factorized_constant_coefficient 4*e^2*mu^2
STATUS TRANSCRIPTION_AUDIT_PASS / NOT_FORMAL_SYMBOLIC_PROOF / NOT_BINDING
```

## Successful Actions evidence

```text
workflow Oblate global axial C0 quantitative pitchfork
run 33576831323
run number 38
job global-axial-c0-evidence
job id 100082541189
head b8a25658a67cec2d750eef7c5b5ce037dfc6cadf
conclusion SUCCESS
```

The job directly checked out the evidence head and printed the same SHA through `git rev-parse HEAD`.

## Predeclared first-passing schedules

```text
C0a:
A0  t_boxes=8   lambda_boxes=8   s_panels=512
A1  t_boxes=16  lambda_boxes=16  s_panels=1024
A2  t_boxes=32  lambda_boxes=32  s_panels=2048

C0b:
B0  lambda_boxes=16  s_panels=512
B1  lambda_boxes=32  s_panels=1024
B2  lambda_boxes=64  s_panels=2048

PREDECLARED_MAX_S_PANEL_EVALS = 5128192
```

First passing is authoritative; later stages are not consulted.

## Producer gating result — 160 bits

C0a A0 is retained only as the declared failed precursor:

```text
A0 unresolved 64
chart counts: series 36569, direct 9831, moving-u0 789, chart_unresolved 0
K0..K3 max radii, series:
  33.8903566002845764
  119.9144618511199951
  15.0010633021593094
  4.44718775898218155
K0..K3 max radii, direct:
  22.6620067059993744
  32.3742190599441528
  24.9280542731285095
  17.8751325905323029
worst box:
  t=[7/16,1/2], lambda=[661/1600,83/200], enclosure [+/- 6.54]
```

Authoritative C0a stage:

```text
C0A_FIRST_PASS A1
A1: t_boxes 16, lambda_boxes 16, s_panels 1024, unresolved 0
chart counts: series 300407, direct 70537, moving-u0 3148, chart_unresolved 0
K0..K3 max radii, series:
  17.5357675850391388
  32.8023241162300110
  4.12094284594058990
  1.50809102505445480
K0..K3 max radii, direct:
  10.1810398399829865
  10.2112966179847717
  5.51455381512641907
  4.25285977125167847
worst box:
  t=[15/32,1/2], lambda=[2/5,1283/3200], enclosure [+/- 3.38]
```

The K0 factorization reduces the A0 series K0 width from the earlier diagnostic scale about `1759.4` to `33.8903566003` (about 1/52). K1 is now the largest A0 series group. At A1, K0 series is `17.5357675850` and all 256 C0a boxes resolve.

C0b:

```text
B0: lambda_boxes 16, s_panels 512, unresolved 10
chart counts: series 7001, direct 4599, moving-u0 75, chart_unresolved 0
worst lambda box [53/128,83/200], enclosure [+/- 0.122]

C0B_FIRST_PASS B1
B1: lambda_boxes 32, s_panels 1024, unresolved 0
chart counts: series 28179, direct 18189, moving-u0 151, chart_unresolved 0
worst lambda box [2653/6400,83/200], enclosure [+/- 0.0855]
```

Final producer line:

```text
LOGICAL_FINAL_C0 PASS C0a_stage A1 C0b_stage B1
claim: g_ttt<0 on box and Phi(t=1/2)<0 on lambda interval
```

No `PT_TEST`, `BOX_TEST`, `BOX_CANDIDATE`, `HULL_TEST`, `CTX_PREC`, or `C0A_K3_INF_DIAGNOSTIC` line is emitted by the receipt run.

## Checker reproduction — 192 bits

The checker independently reconstructs its partition and reproduces the authoritative stages and worst boxes:

```text
C0A_FIRST_PASS A1
A1 unresolved 0
chart counts: series 300407, direct 70537, moving-u0 3148, chart_unresolved 0
worst box t=[15/32,1/2], lambda=[2/5,1283/3200], enclosure [+/- 3.38]

C0B_FIRST_PASS B1
B1 unresolved 0
chart counts: series 28179, direct 18189, moving-u0 151, chart_unresolved 0
worst lambda box [2653/6400,83/200], enclosure [+/- 0.0855]

LOGICAL_FINAL_C0 PASS C0a_stage A1 C0b_stage B1
```

Its A1 K0..K3 max radii are the same at the displayed decision scale. The higher precision changes only harmless low-order tail digits in some K2/K3 radii; for example series K2 is `4.1209428384900093` rather than producer `4.1209428459405899`. The stage decisions, chart counts, worst boxes, and printed worst enclosures are identical.

Checker A1 max radii:

```text
series:
  K0 17.5357675850391388
  K1 32.8023241162300110
  K2 4.12094283849000931
  K3 1.50809102877974510

direct:
  K0 10.1810398399829865
  K1 10.2112966179847717
  K2 5.51455380022525787
  K3 4.25285977125167847
```

## Logical consequence requested from Judge

Please verify only that the pinned contract, exact raw audit, and successful producer/checker cover establish C0a and C0b on the fixed box. Then, using already closed A and B, verify the contract consequence:

```text
lambda < lambda_c^ob:
  no nonzero axial root with 0<|t|<=1/2;

lambda = lambda_c^ob:
  t=0 is the only axial root in |t|<=1/2;

lambda > lambda_c^ob:
  exactly one positive root t*(lambda) in (0,1/2)
  and its odd-symmetry negative partner.
```

This is the quantitative center-pitchfork box only.

## Explicit exclusions

This receipt does not certify:

- any axial statement for lambda outside `[2/5,83/200]`;
- continuation or root exclusion for `1/2<t<31/32`;
- connection to the boundary-entry branch;
- any off-axis stationary-orbit exclusion;
- any global stationary-point census.

No `CERTIFIED` label is authorized for C0 until an external `JUDGE_PASS` is recorded.
