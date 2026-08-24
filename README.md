# Oblate Spheroid Research

This project studies stationary base points of the cone-volume-weighted
radial–normal angle functional on oblate spheroids.

The principal problem is to determine whether two stationary points enter
transversely from the poles, move along the shortest axis, and are eventually
absorbed into the center.

## Certification status

**All results currently stored in this repository are `NOT_BINDING` and
`DIAGNOSTIC_ONLY`.**

No numerical result in this repository belongs to an approved,
Actions-produced clean-room certification path. Numerical searches that detect
no additional stationary points are not nonexistence proofs.

A result may be labelled `CERTIFIED` only after its formulas, interval
implementation, configuration, workflow run, machine-readable certificate,
and independent audit have all been fixed and reviewed.

## Current research targets

1. Construct the canonical axial kernel
   `g_axis_ob(t, lambda)`.
2. Extend it analytically to the pole:
   `b_ob(lambda) = g_axis_ob(1, lambda)`.
3. Determine and certify the boundary-entry parameter
   `lambda_entry_ob`.
4. Determine the center-axis degeneracy parameter
   `lambda_axis_ob` and its nondegenerate pitchfork coefficients.
5. Exclude additional stationary points in the meridian domain.
6. Keep the singular tail `lambda -> 0` as a separate analytic obligation.

## Exact positive control

At the sphere, `lambda = 1`,

```text
b_ob(1) = pi^2 / 32
        = 0.3084251375340424...
```

The axial derivative geometry also satisfies the exact identity

```text
-mu*q - (1 - t*mu)*(t - mu) = -t*(1 - mu^2)
```

when `lambda = 1`. These expectations are fixed before implementation and
must not be regenerated from the production evaluator.

See [STATUS.md](STATUS.md), [NAMING_CONVENTIONS.md](NAMING_CONVENTIONS.md),
and [controls/README.md](controls/README.md).
