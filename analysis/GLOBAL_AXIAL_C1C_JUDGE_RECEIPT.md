# Global axial C1c Judge receipt

Status: `MACHINE_GATING_PASS / JUDGE_PASS / ASSEMBLY_PENDING_C1B / NOT_BINDING`

## 1. Judge scope

The Judge approves only

```text
partial_t^3 g(t,lambda) < 0 on [0,1/2] x [9/20,5/8].
```

This approval excludes `Phi(1/4,lambda)>0`, the deduction `Phi>0` on `[0,1/4]`, and nonzero-root exclusion on `(0,1/2]`. Those consequences remain pending until a pinned successful C1b receipt supplies the positive `g(1/2,lambda)` anchor and exact lambda union `[9/20,5/8]`.

## 2. Evidence pins

```text
receipt run = 33652374082
run HEAD = 3dec57ae76aa6d1e3254592f03eda7fef2eb736c
producer = fbffaccc6dfcfd1b7b9be5b362d8cb80d867aa62
checker = 3ecbda1b3e9acd8134fdd94505721b1780e14edc
workflow = b9de12fae75ce0268fc1b4d87257a057896e752c
run-time amendment = f7568ac381884e35386de221277776765baf5c57
receipt-state amendment = 80b431d10dbd029a7368721676b8abe67d659f81
receipt commit = 45669d4a7a5712ce6c496250e19771846c0fb481
diff-stat completion = c19bf9f5ee282f84168d1f70bf23b607f14f02d5
```

The `80b431d1...` amendment is pinned on the receipt commit. The separate run-time amendment pin preserves the executed identity.

## 3. Receipt-layer diff statistics

```text
checker 5b4c8c1068f7452e8f25f0b8ebcc13d0bb54ae3b
     -> 3ecbda1b3e9acd8134fdd94505721b1780e14edc
1 file changed, 19 insertions(+), 4 deletions(-)

workflow e9c3bfb7a88ba94323bc934e6168875c878b3d3d
      -> b9de12fae75ce0268fc1b4d87257a057896e752c
1 file changed, 60 insertions(+), 9 deletions(-)
```

These are receipt/display/agreement changes only. Kernel, partition, and gating are unchanged.

## 4. Policy inherited by later contracts

```text
worst = exact worst box plus separate mid/rad/upper
stage agreement = unresolved + worst-box coordinates + actual panel evaluations
upper agreement = strict sign only; values need not match across precisions
four_group_width_max = excluded because it is mag_t-derived
```

## 5. C1a non-retroactivity

C1a remains `CLOSED`; its historical `worst +/- 3.77` display is not reopened. The same display limitation remains noted, but no C1a claim or receipt is changed.

## 6. Decision

```text
JUDGE_FINAL_C1C_MACHINE PASS
JUDGE_SCOPE g_ttt<0 on [0,1/2] x [9/20,5/8]
C1C_ASSEMBLY_STATUS PENDING_C1B_ANCHOR_AND_EXACT_COVER
```
