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

## Arb interval candidate

The new producer and checker are deliberately separate modules:

- `producer/endpoint_interval_producer.py` emits cellwise Arb enclosures;
- `checker/endpoint_interval_checker.py` imports no producer code and
  reconstructs the series tails, kernel ranges, cell integrals, totals, and
  signs.

Generate and check a candidate record from the repository root:

~~~bash
python -m producer.endpoint_interval_producer --output endpoint-record.json
python -m checker.endpoint_interval_checker endpoint-record.json \
  --receipt endpoint-receipt.json
~~~

The default grid uses 1024 panels per unit in the transformed coordinate and
160-bit Arb arithmetic. A PASS receipt is an interval-certificate candidate,
not a promotion by itself. The new producer/checker source requires its own
audit and clean-room receipt before any result is labelled CERTIFIED.
The receipt includes the SHA-256 of the exact canonical record bytes and the
record's source commit; the checker rejects noncanonical bytes and verifies
both bindings before writing the receipt.
