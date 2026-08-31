# Meridian evaluator axis consistency control

Status: `DIAGNOSTIC_ONLY / NOT_BINDING / PRE_SCAN_CONTROL_PASS`

Implementation under test:

- `analysis/meridian_off_axis_scan.py`
- implementation commit: `a028b91d5e7390a45494e1b1317b925cd130f32f`

Control requirement from `analysis/MERIDIAN_OFF_AXIS_DIAGNOSTIC_SPEC.md`:

```text
theta = 0 => G_q(q,0;lambda) = lambda E_z = g_axis_ob(t,lambda), t=q.
```

Binary64 meridian quadrature for this control used the refined resolution `N_mu=240`, `N_phi=512`. The independent axial reference was evaluated from the transformed one-dimensional axial kernel with mpmath high precision. Declared meridian-vs-axial absolute tolerance: `5e-6`.

Results:

```text
lambda=5/8, t=63/64
meridian G_q = 0.00043890080576085283
axial reference = 0.00043680804819001693
absolute difference = 2.0927575708359035e-6
sign = POS / POS
PASS

lambda=5/8, t=31/32
meridian G_q = 0.01999736641583677
axial reference = 0.019997234152361168
absolute difference = 1.3226347560235663e-7
sign = POS / POS
PASS

lambda=0.60, t=1
meridian G_q = -0.049168090812912534
axial reference = -0.04916811871525341
absolute difference = 2.7902340875296527e-8
sign = NEG / NEG
PASS

lambda=1, t=1
meridian G_q = 0.3084251840386295
axial reference = 0.30842513753404244
exact expectation pi^2/32 = 0.30842513753404244...
absolute meridian-reference difference = 4.650458707011751e-8
sign = POS / POS
PASS
```

Overall:

```text
AXIS_CONSISTENCY_CONTROL: PASS
```

This result validates the diagnostic evaluator's orientation and normalization sufficiently to permit the non-binding meridian scan. It is not a certification of any stationary-point claim.
