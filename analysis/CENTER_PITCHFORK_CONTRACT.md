# Center pitchfork certification contract B

Status: `AUDIT_COMPLETE / MACHINE_GATING_PASS / EXTERNAL_JUDGE_PENDING / NOT_BINDING`

## Purpose

This contract concerns the local center pitchfork at the certified parameter

```text
lambda_c^ob in (2/5,83/200)
```

from certified contract A.

By `z -> -z` symmetry,

```text
g_axis_ob(-t,lambda) = -g_axis_ob(t,lambda),
```

so near `t=0`

```text
g_axis_ob(t,lambda)
 = H_axis_ob(lambda) t
   + c3_ob(lambda) t^3
   + O(t^5),
```

with

```text
c3_ob(lambda) := (1/6) partial_t^3 g_axis_ob(0,lambda).
```

## Fixed theorem target B1

```text
c3_ob(lambda) < 0
for every lambda in [2/5,83/200].
```

This is the sole machine theorem gate for B.

## Correct density order

The canonical notation is

```text
g_axis_ob(t,lambda) = integral_0^sqrt(2) F_t(s,t,lambda) ds,
G_t = partial_t F_t,
partial_t g_axis_ob = integral_0^sqrt(2) G_t ds.
```

Therefore

```text
c3_ob(lambda)
 = (1/6) integral_0^sqrt(2)
     [partial_t^2 G_t(s,t,lambda)]_{t=0} ds
 = (1/6) integral_0^sqrt(2)
     [partial_t^3 F_t(s,t,lambda)]_{t=0} ds.
```

Write `C=R gamma_t`. Since `A=1-t mu`,

```text
partial_t^3 F_t
 = s[8 mu C_tt - 2 A C_ttt],
```

where

```text
C_tt
 = R_gammagamma gamma_t^3
   + 3 R_gamma gamma_t gamma_tt
   + R gamma_ttt,
```

and

```text
C_ttt
 = R_gammagammagamma gamma_t^4
   + 6 R_gammagamma gamma_t^2 gamma_tt
   + 3 R_gamma gamma_tt^2
   + 4 R_gamma gamma_t gamma_ttt
   + R gamma_tttt.
```

At `t=0`, `A=1`, so the canonical implementation density is

```text
D3_density
 = (s/6)[8 mu C_tt - 2 C_ttt].
```

## Symbolic/raw audit

Canonical note:

```text
analysis/CENTER_PITCHFORK_SYMBOLIC_NOTE.md
commit 943aebe575785e8433e3ea39ea0c6e23e9f7f512
blob efabc9d6c07d2176a62d1d985cba7f8ea01cc629
status CHAT_RAW_AUDIT_PASS / SYMBOLIC_DERIVATION_AUDITED
```

The raw audit independently checked parity, the `4,6,8` derivative chain, the `1,3,1` and `1,6,3,4,1` product-rule coefficients, all four specialized gamma derivatives, both charts for `R_gammagammagamma`, the `Psi'''` tail with exact denominator `89/245`, the fixed removable loci, the exact sphere control, and gating logic.

## Geometry / regularity

On the B interval at `t=0`,

```text
q = 1-mu^2 + lambda^2 mu^2 >= lambda^2 > 0,
w^2 = mu^2 + lambda^2(1-mu^2) >= lambda^2 > 0.
```

There is no moving corner singularity. The exact complement

```text
u = (1-mu^2) mu^2 (1-lambda^2)^2/(w^2 q)
```

has fixed removable zero loci only, handled by the audited `Psi` series chart.

## Exact sphere control

The unit-sphere expansion gives

```text
E_1(t) = E_1(0) + (2/3)t^2 - (2/9)t^4 + O(t^6),
```

hence

```text
g_axis_ob(t,1) = (4/3)t - (8/9)t^3 + O(t^5),
c3_ob(1) = -8/9.
```

The machine evaluator must contain `-8/9`; this is a gating normalization/continuation control, not an assumption in the interval-sign proof.

## Machine architecture and pins

Producer:

```text
producer/center_pitchfork_producer.py
blob 468ab9a3dd318998eb22b8bfbc09c3848cfb45d4
160-bit Arb
4096 s panels
64 exact lambda boxes
Psi degree 50
u threshold 3/5
```

Checker:

```text
checker/center_pitchfork_checker.py
blob 46d05b1aaef31a2e24beceed43d29113af351842
192-bit Arb
4096 s panels
64 exact lambda boxes
Psi degree 50
u threshold 3/5
```

Independence declaration:

```text
CHECKER_KERNEL=TRANSCRIBED_COPY_NOT_INDEPENDENT_DERIVATION
INDEPENDENCE_SCOPE=PRECISION/PARTITION/GATING
```

The A-certified source blobs are unchanged; B uses separate files.

## Machine evidence

Focused successful run with exact report:

```text
run 33438258204
job center-pitchfork-evidence
job id 99639876658
head cbaa72fa2e55f5b5e0a698a763a680be35e1a7ae
conclusion SUCCESS
```

Both producer and checker return

```text
C3_NEG_ALL PASS
weakest_box [2/5,5123/12800]
SPHERE_C3_NEG_8_9 PASS
LOGICAL_FINAL_CLAIM PASS
```

Machine receipt:

```text
analysis/CENTER_PITCHFORK_MACHINE_RECEIPT.md
commit 0af9d6e11117c9183951eaf60506682b1de6f608
```

Judge request:

```text
analysis/CENTER_PITCHFORK_JUDGE_REQUEST.md
commit a30f640d7f6441ba1a424d6e6c0825d9f730dcd9
```

## Independent expectations — REPORTED_NOT_GATING

```text
c3_ob(2/5)          ~ -0.25187,
c3_ob(lambda_c^ob)  ~ -0.26140,
c3_ob(83/200)       ~ -0.26989,
c3_ob(0.5)          ~ -0.376.
```

These are diagnostic/consistency values only.

## Consequence after external Judge approval

Certified contract A gives

```text
H_axis_ob(lambda_c^ob)=0,
partial_lambda H_axis_ob(lambda_c^ob)>0.
```

If external Judge approves B1, then

```text
c3_ob(lambda_c^ob)<0.
```

The odd real-analytic normal form therefore has supercritical orientation for increasing `lambda`: sufficiently near `lambda_c^ob`, one nonzero pair `+/-t*(lambda)` exists for `lambda>lambda_c^ob`, none exists for `lambda<lambda_c^ob`, and

```text
t*(lambda)^2
 ~ H_axis_ob(lambda)/|c3_ob(lambda_c^ob)|
 ~ [partial_lambda H_axis_ob(lambda_c^ob)/|c3_ob(lambda_c^ob)|]
    (lambda-lambda_c^ob).
```

A quantitative local `(epsilon,t0)` box for global cover C is a separate obligation.

## Explicit exclusions

B does not certify by itself:

- a quantitative pitchfork neighborhood;
- the entire nonzero axial branch;
- absence of additional axial roots globally;
- connection to the boundary-entry branch;
- off-axis exclusion;
- the global stationary-point census.

B is internally complete through machine receipt and Judge request, but remains `NOT_BINDING` until an external `JUDGE_PASS` is recorded.
