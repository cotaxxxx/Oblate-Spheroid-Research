# Judge request — lower slab and 31/32 lower edge

Status: `EXTERNAL_JUDGE_REQUESTED / NOT_BINDING`

Judge only the following two claims:

```text
(A) partial_t g_axis_ob(t,lambda) < 0
    on [31/32,63/64] x [5/8,33/50].

(B) g_axis_ob(31/32,lambda) > 0
    on [5/8,33/50].
```

Do not judge or promote any global axial census, roots below 31/32, or off-axis claims.

Pinned evidence:
- contract blob: `61068734b05d5179924d29c555dee7ec3e3dde01`
- lower-slab producer: `e927cda5a18983de94a59903e643e421d2699357`
- lower-slab checker: `3d38a16efd93abf15f169c785e494b1c7c00d559`
- 31/32-edge producer: `8b3cb9ab249182360cb144ecea6f05bef6cc5813`
- 31/32-edge checker: `b11617f30ac804b7668be5e370429d8d6fbfff02`
- source commit: `efb6b5bacf13e9d0bf98e40d04904e1d5a66953a`
- Actions run #147, run id `33371387643`, combined step SUCCESS
- machine receipt: `analysis/LOWER_SLAB_31_32_MACHINE_RECEIPT.md`

For claim A, audit the same ordinary-cell second-derivative algebra and chart policy already used in the `[63/64,1]` refinement. There is no corner cell because `t<=63/64<1`, so `q>0` uniformly at `s=0`.

For claim B, audit the corrected first-derivative density carefully:

```text
F_t = -s*mu*alpha^2 + 2*lambda*A*R*rho^3*H/w,
rho=s/sqrt(q).
```

The second term contains `A`, not `Ahat=A/sqrt(q)`. This distinction is mandatory and is the reason the superseded `t=63/64` v1 receipt is invalid.

Numerical margins from the independent checker:
- claim A worst upper endpoint: approximately `-1.130849882824852566...`
- claim B weakest box `[5/8,1007/1600]`, lower endpoint approximately `+0.004810798130505721...`

Requested Judge output:

```text
PASS
FAIL: <specific defect>
UNRESOLVED: <specific missing obligation>
```

A PASS must identify the audited blobs/run and remain limited to claims A and B.
