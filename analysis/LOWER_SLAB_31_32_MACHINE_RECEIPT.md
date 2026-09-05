# Lower slab + 31/32 lower edge — machine receipt

Status: `MACHINE_GATING_PASS / NOT_AUDITED / NOT_BINDING`

Pinned source commit: `efb6b5bacf13e9d0bf98e40d04904e1d5a66953a`

Pinned contract blob: `61068734b05d5179924d29c555dee7ec3e3dde01`

Lower slab:
- producer blob: `e927cda5a18983de94a59903e643e421d2699357`
- checker blob: `3d38a16efd93abf15f169c785e494b1c7c00d559`
- scope: `partial_t g_axis_ob(t,lambda) < 0` on `[31/32,63/64] x [5/8,33/50]`
- 8 x 8 exact parameter boxes, 1024 s panels, u_star=3/5
- sole gate: every box `total.upper() < 0`
- run #147, run id `33371387643`, combined lower-slab/edge step SUCCESS
- worst independent-checker upper endpoint:
  `-1.1308498828248525660337054178626663178257717367189470334498530159296817291473396`

31/32 lower edge:
- producer blob: `8b3cb9ab249182360cb144ecea6f05bef6cc5813`
- checker blob: `b11617f30ac804b7668be5e370429d8d6fbfff02`
- scope: `g_axis_ob(31/32,lambda) > 0` on `[5/8,33/50]`
- 8 exact lambda boxes, 1024 s panels, u_star=3/5
- sole gate: every lambda box `total.lower() > 0`
- weakest independent-checker box: `[5/8,1007/1600]`
- weakest mid:
  `0.022669317582198421397107506739812946752620192211651285918321683508610227641239959`
- weakest radius:
  `0.01785851945169270038604736328125`
- weakest lower endpoint:
  `0.0048107981305057210110601434585629467526201922116512859183216835086102276412399589`
- weakest upper endpoint:
  `0.040527837033891121783154870021062946752620192211651285918326661920832516554605674`

The later failure in run #147 is the preserved, superseded `t=63/64` corrected 256-lambda-box attempt. It is not part of this receipt.

No binding or CERTIFIED promotion is authorized by this machine receipt. Raw audit and external Judge remain required.
