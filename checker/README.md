# Oblate axial checker prototype

Status: **PROTOTYPE / NOT_AUDITED**

`oblate_axis_prototype.py` implements the analytically derived axial energy
derivative.  Its canonical endpoint path substitutes `mu = 1 - s^2` and
factors the product `(1-t*mu)*gamma_t` before evaluation at `t=1`.
Consequently, `b_ob(lambda)` is evaluated directly and is not obtained by
extrapolating interior values as `t -> 1`.

The implementation uses `mpmath` multiprecision tanh-sinh quadrature.  It is
not interval arithmetic and produces candidate evidence only.

Run the implementation-calling sphere checks from the repository root:

```bash
python -m unittest controls/test_endpoint_evaluator.py
```

The independent expectations remain in `controls/CONTROL_EXPECT.json` and
`controls/test_sphere_expectations.py`.  The implementation-calling test is a
separate file so the provenance distinction remains visible.
