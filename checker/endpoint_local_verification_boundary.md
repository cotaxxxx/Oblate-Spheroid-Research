# Endpoint local producer/checker boundary

Status: **PROTOTYPE / NOT_AUDITED** and **NOT_BINDING**.

This document fixes the verification boundary before either the producer or
checker exists. It does not certify an enclosure.

## Chosen architecture

The checker does **not** call the producer and does not rerun the producer's
adaptive integration path. The producer emits cell records conforming to
`spec/endpoint_local_producer_record_v1.schema.json`. The checker consumes
only that record, its pinned sources, and the fixed analytic/contract files.

A record contains three evaluations:

- (B_{\rm ob}(5/8));
- (B_{\rm ob}(33/50));
- (B'_{\rm ob}([5/8,33/50])).

Each evaluation is a rational partition in (s). Every cell records its
rational (s)-interval and (lambda)-interval, chart, series degrees,
partial-sum and rigorous-remainder balls, kernel and
(partial_lambda)-kernel balls, and the corresponding weighted integral
balls.

## Checker obligations

The checker fails closed unless all of the following hold.

1. The JSON has exactly the allowed schema keys and labels.
2. Every SHA-256, source commit, wheel filename, dependency version, and
   workflow hash matches the pinned inputs.
3. `checker_bits >= producer_bits` is enforced in code.
4. Cells are ordered, nonoverlapping, gap-free, and cover exactly
   ([0,1]cup[1,sqrt2]) using the prescribed chart on each side. The
   algebraic upper endpoint is represented by its fixed endpoint label rather
   than an unverified decimal approximation.
5. Series partial sums and remainder bounds are reconstructed independently
   from their recorded rational domains and degrees. Producer-supplied
   `PASS` labels or final sums are never trusted.
6. Kernel and derivative enclosures are checked from the recorded elementary
   factor enclosures and the independently reconstructed series bounds. A
   cell enclosure that is merely self-reported is rejected.
7. Cell integral balls are recomputed from the checked cell range and exact
   cell width. The checker independently sums them and requires containment
   in, but not equality with, the producer's reported sum.
8. At (s=1), the checker evaluates the exact rational targets
   [
   gamma^2=\frac1{1+lambda^2},qquad
   u=\frac{lambda^2}{1+lambda^2}
   ]
   and verifies overlap of the lower and upper chart enclosures.
9. The six exact control families are executed by checker-owned code:
   endpoint values, global complement identity, internal double zero, seam
   rational targets, and the (Agamma_t) factorization. A producer-supplied
   control status is informational only.
10. The independently reconstructed totals satisfy
    [
    sup B_{\rm ob}(5/8)<0,qquad
    inf B_{\rm ob}(33/50)>0,qquad
    inf B'_{\rm ob}([5/8,33/50])>0.
    ]

Only these three inequalities imply the contract conclusion: exactly one zero
of (B_{\rm ob}) in ([5/8,33/50]), conditional on the separately audited
analytic lemma.

## Newton gate

Interval Newton is a second-stage consumer. It may run only after the checker
has accepted all three broad-bracket inequalities. It must reuse an accepted
derivative enclosure and cannot replace or weaken the broad-bracket proof.
The interval ([16/25,13/20]) remains a non-binding diagnostic waypoint.

## Artifact and receipt chain

The clean-room workflow follows the existing B-TUBE pattern:

- install only hash-pinned binary wheels with
  `--require-hashes --only-binary=:all:`;
- record source commit plus producer, checker, contract, requirements, wheel,
  and workflow SHA-256 values;
- emit a canonical payload manifest;
- have the final receipt verifier recompute all file hashes and reject any
  source, workflow, configuration, precision, or artifact mismatch.

No output is `CERTIFIED` until a separate auditor fixes an audited source
hash and the clean-room receipt chain passes.
