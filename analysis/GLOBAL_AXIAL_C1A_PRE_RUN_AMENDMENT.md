# C1a pre-run amendment — logical gate and reported crossing bracket

Status: `PREDECLARED_AMENDMENT / MACHINE_NOT_RUN / NOT_BINDING`

This amendment is made before the next C1a gating run. It supersedes only the bisection-gating language in Section C1a.3 of `analysis/GLOBAL_AXIAL_C1_CROSSING_TUBE_CONTRACT.md`. All C1a mathematical sign gates, A/D stages, arithmetic, chart architecture, precisions, and C1b rules remain unchanged.

## 1. Logical C1a gate

`LOGICAL_FINAL_C1A = PASS` iff all of the following machine gates pass:

```text
A: partial_t^3 g(t,lambda) < 0 on [0,1/2] x [83/200,9/20]
D: partial_lambda F_x(lambda) > 0 on [83/200,9/20]
L: F_x(83/200) < 0
R: F_x(9/20) > 0
```

These four strict sign statements imply that `F_x` is strictly increasing and has exactly one zero

```text
lambda_x in (83/200,9/20).
```

Therefore exact-rational bisection is a localization/reporting operation only. Its achieved depth is not a logical gate for existence, uniqueness, or `lambda_x < 9/20`.

## 2. Reported certified bracket policy

After L/R pass, start from

```text
[lo,hi] = [83/200,9/20]
```

with certified opposite endpoint signs. At each exact-rational midpoint, try the following predeclared point-panel ladder in order:

```text
1024, 4096, 16384, 65536
```

The first panel count producing a strict sign is authoritative for that midpoint. Update the corresponding endpoint and continue. If all four panel counts leave the midpoint enclosure containing zero, stop bisection without failing C1a.

Maximum attempted bisection depth remains

```text
16
```

but depth is a reported attribute, not a gate.

The producer and checker must always print the last opposite-sign exact-rational interval as

```text
C1A_REPORTED_CERTIFIED_BRACKET
```

including depth, exact endpoints, endpoint enclosures, width, and whether the stop reason was `MAX_DEPTH` or `POINT_UNRESOLVED`.

The decimal landmark

```text
lambda_x ~= 0.43775487...
```

is expectation/report-only and never gates.

## 3. Work ceiling amendment

Endpoint signs retain `8192` panels each.

Worst-case bisection work is now

```text
16 * (1024 + 4096 + 16384 + 65536)
= 1,376,256 panel evaluations.
```

Thus the amended C1a ceiling is

```text
A stages                2,392,064
D stages                  344,064
endpoint signs              16,384
bisection ladder          1,376,256
----------------------------------
TOTAL                     4,128,768
```

No run exceeding this ceiling is C1a evidence under this amendment.

## 4. Receipt rule

A C1a receipt must separately record:

```text
LOGICAL_FINAL_C1A gate result
A first-pass stage and worst enclosure
D first-pass stage and weakest enclosure
F_x endpoint enclosures
C1A_REPORTED_CERTIFIED_BRACKET and achieved depth
bisection stop reason
actual/predeclared point-panel ladder
producer/checker agreement
```

A reported bracket may be coarser than the 16-step target and still be certified, provided its two exact endpoints retain opposite certified signs. This does not weaken the C1a theorem because bisection is not used to prove existence or uniqueness.
