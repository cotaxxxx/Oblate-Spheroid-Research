# Exact Expectations

The expectations in this directory were fixed independently of the evaluator.

## Sphere positive expectation

```text
b_ob(1) = pi^2/32
        = 0.3084251375340424...
```

## Sphere symbolic identity

For `lambda = 1`, the numerator bracket in `gamma_t` must simplify to

```text
-mu*q - (1 - t*mu)*(t - mu) = -t*(1 - mu^2).
```

The expected value must never be generated or overwritten by the evaluator it
constrains.

## Prototype implementation control

`test_sphere_expectations.py` now calls the `PROTOTYPE` implementation
`axial_endpoint_ob.b_ob` at `lambda = 1` and compares it with the independently
fixed exact value `pi^2/32`.

This is an implementation-connected control for the prototype only. It does
not make the evaluator audited, production, or certified. A future interval
production evaluator must still produce an enclosure containing the exact value
through the clean-room proof path.
