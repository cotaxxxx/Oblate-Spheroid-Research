# Exact Controls

The controls in this directory are fixed independently of the future
production evaluator.

## Sphere positive control

```text
b_ob(1) = pi^2/32
        = 0.3084251375340424...
```

## Sphere symbolic identity

For `lambda = 1`, the numerator bracket in `gamma_t` must simplify to

```text
-mu*q - (1 - t*mu)*(t - mu) = -t*(1 - mu^2).
```

A future production evaluator must reproduce the exact control and an interval
enclosure containing the exact value. The expected value must never be
generated or overwritten by that evaluator.
