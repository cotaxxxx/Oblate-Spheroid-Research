# Census lower-edge machine receipt

Status: `MACHINE_GATING_PASS / NOT_AUDITED / NOT_BINDING`

Pinned claim scope:

```text
g_axis_ob(63/64, lambda) > 0
lambda in [5/8, 33/50]
```

Sole gate: the full-domain one-box Arb enclosure has strictly positive lower endpoint.

Pinned sources:

- contract commit: `53e2886f89e1b8c45bd65fa1c0adabbeb6eef731`
- producer blob: `243124b76726de8a81ab42ba5edf19c000c3a963`
- checker blob: `0245d6c680c54e91eb6123d6fd40c9f210e60a40`
- workflow source commit: `dbe215cfa7e4cbb549dc909382bc83a3e7019fad`
- Actions run: #101, run id `33368313307`
- lower-edge step: SUCCESS
- log: `CENSUS_LOWER_EDGE producer pass: True`
- independent checker: SUCCESS

The same run also reconfirmed the monotone-tube refinement step with zero unresolved boxes. The workflow's overall failure is intentionally caused by the final preserved initial-contract test, which remains 64/64 UNRESOLVED and is not part of this lower-edge gate.

Logical consequence is conditional on separately binding prior ingredients: if `partial_t g_axis_ob<0` holds throughout `[63/64,1] x [5/8,33/50]`, then for each fixed lambda the axial function is strictly decreasing on the tube. Combining that with this lower-edge positivity and the separately certified endpoint sign structure of `b_ob(lambda)=g_axis_ob(1,lambda)` yields exactly one tube root when `b_ob(lambda)<0`, and zero tube roots when `b_ob(lambda)>0`.

This receipt does not certify `lambda_entry_ob`, endpoint sign structure, roots below `63/64`, a global axial census, or any off-axis exclusion.
