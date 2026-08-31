# Judge receipt template — oblate local boundary entry

Status: `EXTERNAL_JUDGE_PENDING / NOT_BINDING`

This receipt is intentionally limited to the local axial boundary-entry theorem on

```text
t in [31/32,1], lambda in [5/8,33/50].
```

It does not certify any claim outside that tube or parameter interval.

## Claims to judge

### Claim 1 — upper tube monotonicity

```text
partial_t g_axis_ob(t,lambda) < 0
on [63/64,1] x [5/8,33/50],
with t=1 interpreted one-sidedly.
```

Pinned machine lineage:

- Actions run #101: `33368313307` (upper-tube refinement step SUCCESS)
- refinement contract blob: `5808e84572b1428c58a9b4136b56c4b6f54339cb`
- producer blob: `c2fee40053ab055ce352e93e1c6d1fc43e46310a`
- checker blob: `fd778d6d3a2dc52ae38be87bf4eb800bfbdea6d3`
- corrected raw-audit receipt blob: `c3b3666d485a02a5acf4eb856e9c399118a53a9c`

### Claim 2 — lower slab monotonicity

```text
partial_t g_axis_ob(t,lambda) < 0
on [31/32,63/64] x [5/8,33/50].
```

Pinned machine lineage:

- Actions run #147: `33371387643` (lower-slab step SUCCESS)
- contract blob: `61068734b05d5179924d29c555dee7ec3e3dde01`
- producer blob: `e927cda5a18983de94a59903e643e421d2699357`
- checker blob: `3d38a16efd93abf15f169c785e494b1c7c00d559`
- reported worst independent-checker upper endpoint:
  `-1.1308498828248525660337054178626663... < 0`

### Claim 3 — positive lower edge

```text
g_axis_ob(31/32,lambda) > 0
for lambda in [5/8,33/50].
```

Pinned machine lineage:

- Actions run #147: `33371387643` (31/32 lower-edge step SUCCESS)
- contract blob: `61068734b05d5179924d29c555dee7ec3e3dde01`
- producer blob: `8b3cb9ab249182360cb144ecea6f05bef6cc5813`
- checker blob: `b11617f30ac804b7668be5e370429d8d6fbfff02`
- weakest lambda box: `[5/8,1007/1600]`
- weakest independent-checker lower endpoint:
  `0.0048107981305057210110601434585629... > 0`

## Analytic lemmas to audit and pin

### C1 endpoint lemma

Pinned from branch `analytic-endpoint-limit-78c178f`:

- `analysis/endpoint_kernel_lemma.md`
- blob: `aa6a1a1710d1a4af560e5ddf0c504870f50c535c`

This is the analytic endpoint-limit / one-sided C1 identification needed to interpret `g_axis_ob(1,lambda)=b_ob(lambda)` and to connect the pre-limit integral with the endpoint kernel.

### C2 differentiation/interchange lemma

Pinned on the implementation branch:

- `analysis/MONOTONE_TUBE_C2_INTERCHANGE_LEMMA.md`
- blob: `7cb9b8091596510203d74e09387bc1e8188b8b47`

This supplies the dominated differentiation / endpoint-continuity obligation needed to identify the machine-enclosed second-t density with `partial_t g_axis_ob` up to `t=1`.

## Endpoint sign structure used as an external certified input

The logical consequence below also assumes the separately certified endpoint statement:

```text
b_ob(lambda) has exactly one zero lambda_partial^ob in [5/8,33/50],
b_ob(lambda) < 0 for lambda < lambda_partial^ob,
b_ob(lambda) > 0 for lambda > lambda_partial^ob,
and B_ob'(lambda) > 0 on the certified endpoint domain.
```

The Judge must identify the exact certified endpoint receipt/source used for this input. This local-entry receipt must not silently re-certify that earlier theorem.

## Logical consequence — only after PASS of Claims 1–3 and analytic pins

Because Claims 1 and 2 overlap at `t=63/64`, their union gives

```text
partial_t g_axis_ob(t,lambda) < 0
on [31/32,1] x [5/8,33/50].
```

Hence for every fixed lambda in the certified interval, `t -> g_axis_ob(t,lambda)` is strictly decreasing on `[31/32,1]`.

Combining strict decrease with Claim 3 and `g_axis_ob(1,lambda)=b_ob(lambda)` gives:

```text
lambda < lambda_partial^ob:
    exactly one root t*(lambda) in (31/32,1);

lambda = lambda_partial^ob:
    the unique root in [31/32,1] is t=1;

lambda > lambda_partial^ob:
    no root in [31/32,1].
```

Since `partial_t g_axis_ob != 0` throughout the tube, the implicit-function theorem gives a local C1 root branch wherever an interior root exists. Its derivative is

```text
dt*/dlambda = - partial_lambda g_axis_ob / partial_t g_axis_ob.
```

**Important:** the stronger sign conclusion `dt*/dlambda > 0` requires an independently audited sign input `partial_lambda g_axis_ob(t*(lambda),lambda) > 0` (or an equivalent rigorous argument). `B_ob' > 0` at the endpoint alone does not by itself establish the sign of `partial_lambda g` along the full interior root branch. Unless that additional input is pinned, the Judge receipt must state only C1 regularity and continuity of the unique branch, not global positive branch slope.

From uniqueness plus the endpoint sign transition and continuity, the local axial boundary-entry parameter is identified with the endpoint zero:

```text
lambda_entry,ob = lambda_partial^ob
```

**within the stated local tube meaning**: this identifies the parameter at which the unique axial root in `[31/32,1]` meets/leaves the boundary. It is not a global no-extra-root theorem.

## Explicit exclusions

This receipt does **not** claim:

- absence or uniqueness of roots with `t < 31/32`;
- absence or classification of off-axis stationary points;
- any statement for `lambda` outside `[5/8,33/50]`;
- a global no-fold theorem outside the local tube;
- `dt*/dlambda > 0` unless a separate rigorous `partial_lambda g` sign input is pinned;
- any promotion of the historical `t=63/64` lower-edge failed/unresolved controls.

## Required Judge output

Record exactly one of:

```text
PASS
FAIL: <specific mathematical or provenance defect>
UNRESOLVED: <specific missing obligation>
```

A PASS must list the exact blobs/runs actually audited and explicitly confirm the scope exclusions above.
