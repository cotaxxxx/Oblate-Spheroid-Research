# Global axial C0 — C0b evaluator stabilization note

Status: `IMPLEMENTED_FIX / MACHINE_PENDING / NOT_BINDING`

## Scope

This note records one numerical-evaluation correction for C0b only.  It does
not change the C0 theorem, the C0a density, the predeclared stage schedule, or
the first-passing discipline.

## Superseded run

The initial focused C0 run

```text
run 33445617927
job 99663932621
```

proved C0a at first-passing stage `A2`, but C0b returned Arb `nan` values in
all predeclared B stages.  The chart ledger had `chart_unresolved=0`; the
failure came from direct interval evaluation of

```text
alpha2 = asin(sqrt(u))^2
```

when an Arb interval touched the endpoint `u=1`.

Therefore run `33445617927` is classified for C0b as

```text
SUPERSEDED_EVALUATOR_DIAGNOSTIC / NOT_EVIDENCE_FOR_C0B
```

It must not be cited as a successful C0 machine gate.  Its C0a output remains
a useful diagnostic/reconstruction check, but the final C0 receipt must pin a
clean successful run using the stabilized evaluator for both producer and
checker.

## Exact stabilization

The already audited continuation is

```text
R(u) = asin(sqrt(u))/sqrt(u).
```

Hence identically, including by analytic continuation at `u=0`,

```text
alpha^2 = asin(sqrt(u))^2 = u R(u)^2.
```

The stabilized C0b density therefore evaluates

```text
alpha2 = u * R * R
F_t = s * (-mu * alpha2 - 2 * A * R * gamma_t).
```

No mathematical formula or sign target changes.  The same two-chart `R`
evaluator that already handles the moving removable `u=0` locus is reused.

## Source isolation

The raw-audited base C0 producer/checker are left unchanged.  The C0b-only
stabilization is isolated in wrappers:

```text
producer/global_axial_c0_producer_v2.py
checker/global_axial_c0_checker_v2.py
```

The wrappers replace only `_g_density`; C0a `_g3_density`, geometry,
`N -> M -> P -> P1`, chart policy, stage schedule, budgets, and first-passing
logic are inherited unchanged.

Checker declaration remains

```text
CHECKER_KERNEL=TRANSCRIBED_COPY_NOT_INDEPENDENT_DERIVATION
INDEPENDENCE_SCOPE=PRECISION/PARTITION/GATING
```

## Machine obligations after the fix

A successful final C0 machine lineage must show, for producer and checker:

1. C0a: `unresolved=0` at its first-passing predeclared stage;
2. C0b: `unresolved=0` at its first-passing predeclared stage;
3. `chart_unresolved=0`;
4. moving-`u=0` cells are actually routed through the series chart;
5. worst C0a upper bound is strictly negative;
6. worst C0b upper bound is strictly negative;
7. later stages are not consulted after first pass.

Until those outputs exist, C0 remains

```text
MACHINE_PENDING / NOT_BINDING.
```
