# Global axial C1a machine receipt

Status: `MACHINE_PASS / C1A_CLOSED / NOT_EXTERNAL_JUDGE_BINDING`

This receipt records the C1a crossing-bridge machine run after the pre-run bisection amendment. It does not certify C1b or any off-axis statement.

## Pins

```text
implementation commit: 04cc7975b294e39a4444cc6dc7c9e4d539307302
parent C1 contract blob: 77210a5402c1299499b59426d18bdd00e1cc6122
C1a pre-run amendment blob: 0f6c3134342fbf1a4ae4cfa4527af5cf4970e0dd
producer blob: 9081996afc82b38f960aa6ebdebbd82bef019e46
checker blob: 6efe7a9150c3ff947194ba82c43b404c8f472020
workflow blob: 1846376fce059b98a523b68ec5f7c8f0229cc128
crossing lambda-derivative symbolic-audit blob: db3539c14d9f398111243e5823e8d22eb8a11a5a
C0a four-group raw-audit blob: 26002379307379c9a1cb05a7644fa638e7a0fa9a
requirements-prototype.txt blob: e01c11e4c67774875b280ccc7603ffb29aa427f4
requirements-interval.txt blob: 399cb56905e5cf6e71a2d59771fee1ea7c2834e0
Actions run id: 33603133689
Actions job id: 100161077293
Python: 3.12.14
mpmath: 1.4.1
python-flint: 0.9.0
producer precision: 160 bits
checker precision: 192 bits
DEG: 50
USTAR: 3/5
```

The workflow recorded the checked-out implementation HEAD and the amendment blob before numerical work. The run completed `success`; both producer and checker steps completed `success`.

## Logical C1a gate

Under the pinned pre-run amendment,

```text
LOGICAL_FINAL_C1A = PASS
```

is gated only by

```text
A: partial_t^3 g < 0 on [0,1/2] x [83/200,9/20]
D: partial_lambda F_x > 0 on [83/200,9/20]
L: F_x(83/200) < 0
R: F_x(9/20) > 0
```

Exact-rational bisection is report-only and does not gate existence or uniqueness.

## Producer result

```text
C1A_G3_FIRST_PASS A1
A1 unresolved = 0
A1 worst box:
  t = [15/32,1/2]
  lambda = [83/200,267/640]
  enclosure = [+/- 3.77] with certified upper endpoint < 0

C1A_D_FIRST_PASS D0
D0 unresolved = 0
D0 weakest lambda box = [83/200,267/640]
D0 enclosure = [2e+0 +/- 0.409] with certified lower endpoint > 0

C1A_FX_LEFT PASS 83/200 [-0.05 +/- 5.11e-3]
C1A_FX_RIGHT PASS 9/20 [0.03 +/- 6.43e-3]

LOGICAL_FINAL_C1A PASS
g3_stage A1
derivative_stage D0
gates A_AND_D_AND_ENDPOINT_SIGNS
```

Therefore `F_x` is strictly increasing on `[83/200,9/20]`, changes sign across the endpoints, and has exactly one zero

```text
lambda_x in (83/200,9/20).
```

In particular,

```text
lambda_x < 9/20.
```

This is the C1a crossing bridge required to start C1b.

## Reported certified crossing bracket

Predeclared midpoint panel ladder:

```text
1024, 4096, 16384, 65536
```

Producer first-passing sequence:

```text
step 1: 173/400  NEG at 4096 panels
step 2: 353/800  POS at 16384 panels
step 3: 699/1600 NEG at 65536 panels
step 4: 281/640  POS at 16384 panels
step 5: 2803/6400 unresolved through 65536 panels -> STOP
```

Final report-only certified bracket:

```text
C1A_REPORTED_CERTIFIED_BRACKET PASS
depth = 4
lo = 699/1600 = 0.436875
hi = 281/640 = 0.4390625
width = 7/3200 = 0.0021875
F_lo = [-0.002 +/- 5.46e-4]
F_hi = [+/- 5.02e-3] with certified lower endpoint > 0
stop_reason = POINT_UNRESOLVED
```

The decimal landmark

```text
lambda_x ~= 0.43775487...
```

remains `REPORTED_EXPECTATION / NON_GATING`.

## Checker reproduction

The 192-bit checker reproduced:

```text
C1A_G3_FIRST_PASS A1
C1A_D_FIRST_PASS D0
C1A_FX_LEFT PASS
C1A_FX_RIGHT PASS
same first-passing panel counts at bisection steps 1-4
same unresolved step 5 at 65536 panels
same exact bracket [699/1600,281/640]
same width 7/3200
same stop_reason POINT_UNRESOLVED
LOGICAL_FINAL_C1A PASS
```

Checker declaration remains:

```text
CHECKER_KERNEL TRANSCRIBED_COPY_NOT_INDEPENDENT_DERIVATION
INDEPENDENCE_SCOPE PRECISION/PARTITION/GATING
```

Thus this receipt records independent precision/partition/gating reproduction, not an independent mathematical derivation.

## Work ledger

Authoritative stages stop at first pass.

```text
A0 + A1:
  8*8*512 + 16*16*1024 = 294,912 panels
D0:
  16*1024 = 16,384 panels
endpoint signs:
  2*8192 = 16,384 panels
reported bisection attempts:
  step 1 = 1024+4096 = 5,120
  step 2 = 1024+4096+16384 = 21,504
  step 3 = 1024+4096+16384+65536 = 86,016
  step 4 = 1024+4096+16384 = 21,504
  step 5 = 1024+4096+16384+65536 = 86,016
  bisection total = 220,160 panels

TOTAL PER PRODUCER/CHECKER = 547,840 panel evaluations
PREDECLARED C1A CEILING = 4,128,768
```

The executed work is below the predeclared ceiling.

## C1a closure

```text
C1A MACHINE PASS
unique lambda_x exists in (83/200,9/20)
certified reported bracket = [699/1600,281/640]
lambda_x < 9/20
C1b start condition satisfied
```

C1a is closed at the machine-evidence level recorded here. C1b remains a separate obligation under the parent C1 contract.
