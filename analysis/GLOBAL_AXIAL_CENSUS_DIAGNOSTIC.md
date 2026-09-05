# Global axial census — diagnostic declaration

Status: `DIAGNOSTIC_ONLY / NOT_BINDING`

Goal: exclude positive-axis zeros outside the already treated local-entry tube.

Because axial symmetry gives `g_axis_ob(0,lambda)=0`, and because the local branch requires `g>0` below the boundary root, a global claim `partial_t g<0` is impossible. The correct target is

```text
g_axis_ob(t,lambda) > 0
for 0 < t <= 31/32, lambda in [5/8,33/50].
```

Together with odd symmetry this would exclude any additional axial roots outside the local-entry tube.

## Diagnostic split

First inspect the ordinary integral representation on

```text
t in [1/32,31/32]
lambda in [5/8,33/50]
```

using exact 16 x 8 parameter boxes, 1024 inherited s-panels, Arb 160 bits, and the corrected first-derivative density

```text
F_t = -s*mu*alpha^2 + 2*lambda*A*R*rho^3*H/w.
```

This diagnostic is sign-only and non-gating. It records the minimum lower endpoint and all unresolved boxes.

The center strip `t in [0,1/32]` is deliberately excluded from this first diagnostic because `g(0,lambda)=0`; it will require a separate regularized quantity, preferably `g_axis_ob(t,lambda)/t`, or an equivalent center Taylor/Hessian argument fixed before certification.

No global theorem is claimed by this file.