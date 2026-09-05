# Global axial C1c machine receipt

Status: `MACHINE_GATING_PASS / ASSEMBLY_PENDING_C1B / NOT_BINDING`

## 1. Evidence identity

```text
receipt run id = 33652374082
receipt run number = 3
receipt run URL = https://github.com/cotaxxxx/bg-oblate-spheroid/actions/runs/33652374082
receipt run HEAD = 3dec57ae76aa6d1e3254592f03eda7fef2eb736c
job id = 100322341007
conclusion = success
started = 2026-09-02T16:02:04Z
updated = 2026-09-02T16:28:31Z
```

Run-time blobs:

```text
analysis/GLOBAL_AXIAL_C1C_PRE_RUN_AMENDMENT.md f7568ac381884e35386de221277776765baf5c57
producer/global_axial_c1c_producer.py          fbffaccc6dfcfd1b7b9be5b362d8cb80d867aa62
checker/global_axial_c1c_checker.py            3ecbda1b3e9acd8134fdd94505721b1780e14edc
.github/workflows/oblate-global-axial-c1c.yml   b9de12fae75ce0268fc1b4d87257a057896e752c
requirements-prototype.txt                     e01c11e4c67774875b280ccc7603ffb29aa427f4
requirements-interval.txt                      399cb56905e5cf6e71a2d59771fee1ea7c2834e0
```

## 2. Historical lineage

```text
33630228893 HISTORICAL_MACHINE_PASS_DISPLAY_INCOMPLETE
33650157537 MACHINE_NUMERIC_PASS_AGREEMENT_PARSE_FAIL / NOT_RECEIPT
33652374082 RECEIPT_RUN / MACHINE_GATING_PASS
```

Run 33630228893 remains historical numerical evidence but its worst display was incomplete for audit. Run 33650157537 emitted corrected fields and both numerical lineages passed, but its agreement parser attempted `float()` on python-flint's certified point-interval rendering; it is not the receipt run.

## 3. Receipt-layer-only source change

```text
git diff e66dab917d9dba0b06298ba480d197cb6bc6e944..fbffaccc6dfcfd1b7b9be5b362d8cb80d867aa62 --stat
 producer/global_axial_c1c_producer.py | 23 +++++++++++++++++++----
 1 file changed, 19 insertions(+), 4 deletions(-)
```

Checker receipt-layer stat:

```text
git diff 5b4c8c1068f7452e8f25f0b8ebcc13d0bb54ae3b..3ecbda1b3e9acd8134fdd94505721b1780e14edc --stat
 checker/global_axial_c1c_checker.py | 23 +++++++++++++++++++----
 1 file changed, 19 insertions(+), 4 deletions(-)
```

Workflow receipt/agreement stat:

```text
git diff e9c3bfb7a88ba94323bc934e6168875c878b3d3d..b9de12fae75ce0268fc1b4d87257a057896e752c --stat
 .github/workflows/oblate-global-axial-c1c.yml | 69 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++---------
 1 file changed, 60 insertions(+), 9 deletions(-)
```

Those 23 changed lines only retain `arb.upper()`, `mid()`, and `rad()` for output, count per-stage panel evaluations, and split stage/chart/worst receipt records. Density, chart selection, recurrence, series, tail, partitions, strict-sign predicate, stages, precision, and ceiling are unchanged. The checker has the same receipt-layer change in its separate lineage.

```text
3fbdbc2c C1c receipt-layer print/agreement only, kernel unchanged
3dec57ae C1c receipt parser accepts certified arb.upper rendering, kernel unchanged
```

## 4. Exact stage ledger

```text
stage  t_boxes lambda_boxes s_panels unresolved panel_evaluations
A0     8       8            512      64         32768
A1     16      16           1024     59         262144
A2     32      32           2048     0          2097152
total                                             2392064
```

Producer and checker agreed on each stage's unresolved count, worst-box coordinates, and actual panel evaluations. The first passing stage is A2 in both lineages. The total equals the predeclared ceiling. `four_group_width_max` is excluded from agreement because it is derived from `mag_t`.

## 5. A2 worst certified enclosure

Common exact box:

```text
t_lo=31/64 t_hi=1/2 lambda_lo=9/20 lambda_hi=583/1280
```

Producer, 160 bits:

```text
mid = [-2.2249909149075616224375296732110637256501131414 +/- 3.99e-47]
rad = 1.3444432076066732406616210937500000000000000000
upper = [-0.88054770730088838177590857946106372565011314144 +/- 1.80e-49]
```

Checker, 192 bits:

```text
mid = [-2.22499091492090030914696293814714230512678984081503399246 +/- 9.37e-58]
rad = 1.34444320760667324066162109375000000000000000000000000000
upper = [-0.880547707314227068485341844397142305126789840815033992461 +/- 6.42e-59]
```

Both gating upper bounds are strictly negative; numerical equality is not required across precisions. The margin is approximately `0.8805` below zero, thicker than expected, so no near-zero qualification is required.

## 6. Conclusions

```text
LOGICAL_FINAL_C1C_MACHINE PASS
C1C_PRODUCER_CHECKER_AGREEMENT PASS first_stage A2
LOGICAL_FINAL_C1C_ASSEMBLY PENDING_C1B_ANCHOR_AND_EXACT_COVER
```

This certifies `partial_t^3 g<0` on the exact C1c rectangle. Global promotion still requires a pinned successful C1b receipt with exact lambda union `[9/20,5/8]` and a positive `g(1/2,lambda)` anchor on every accepted slab.
