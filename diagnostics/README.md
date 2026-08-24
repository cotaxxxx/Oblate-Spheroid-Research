# Diagnostics

Everything in this directory is `DIAGNOSTIC_ONLY` and `NOT_BINDING`.

Parameter scans, floating-point roots, finite differences, plots, and
exploratory branch continuations belong here. In particular, a scan reporting
that no additional stationary point was detected is not a proof of
nonexistence.

Every diagnostic artifact must record:

- code revision;
- parameter domain;
- mesh or subdivision;
- arithmetic and precision;
- stopping criteria;
- unresolved or failed cells;
- creation date.

Diagnostic files must not be consumed as certification dependencies.
