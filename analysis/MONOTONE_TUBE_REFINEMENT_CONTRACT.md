# Monotone tube refinement contract — oblate axial boundary branch

Status: `FIXED_BEFORE_REFINEMENT_RUN / NOT_BINDING`

This refinement does not replace or rewrite the failed initial contract. It is a separately declared run motivated by the non-gating width diagnostics.

## Claim scope

```text
quantity      = partial_t g_axis_ob(t,lambda)
t domain      = [63/64, 1]
lambda domain = [5/8, 33/50]
required sign = NEG
gating        = every rigorous (t,lambda)-box enclosure has upper endpoint < 0
```

The parameter partition is unchanged from the initial run:

- 8 exact t boxes, width 1/512;
- 8 exact lambda boxes, width 7/1600;
- inherited 1024-panel exact s partition;
- Arb precision 160 bits;
- Psi / Psi_prime degree 50.

No parameter or s refinement is authorized in this run.

## Diagnostic basis fixed before refinement

The term-by-chart diagnostic identified T2 in the old gamma_lower chart as the dominant dependency loss. On the prior maximum-radius parameter box, the old total radius was about 705.59 and the T2 radius about 705.45, while the u_upper contribution to T2 was negligible.

A threshold diagnostic compared u* in {1/4, 1/2, 3/5} on the first parameter box and the prior maximum-radius box. The best of the declared candidates was u*=3/5:

```text
first box:     total radius ~0.09554, T2 radius ~0.01088
prior max box: total radius ~0.09934, T2 radius ~0.01165
```

These are `DIAGNOSTIC_ONLY / NOT_BINDING` and are not gating expectations.

## Exact A tightening

For every ordinary box, use both exact forms

```text
A = 1 - t*mu,
A = (1-t) + t*s^2,
```

and replace the raw interval for A by their intersection before forming gamma or A/sqrt(q). The second form is a positive sum on the present tube and removes an avoidable interval cancellation. This is an exact algebraic intersection, not a numerical approximation.

## Chart policy fixed before refinement

Let u = 1-gamma^2, with the same rigorous intersection of the factorized u enclosure and the gamma-derived enclosure used by the prototype.

Set exactly

```text
u_star = 3/5.
```

For each ordinary s-cell:

1. if `u.upper() <= 3/5`, use `u_upper`:
   - R = Psi(u),
   - R_gamma = -2 gamma Psi_prime(u),
   - degree 50 with the inherited rigorous geometric remainder;
2. if `u.lower() >= 3/5`, use `gamma_lower`:
   - R = acos(gamma)/sqrt(u),
   - R_gamma = (gamma R - 1)/u;
3. if `u.lower() < 3/5 < u.upper()`, evaluate T1, T2, T3 independently in both valid charts and intersect the two rigorous enclosures **term by term**.

The crossing-cell intersection is valid because each chart enclosure independently contains the same exact term. No correlation between R and R_gamma across charts is assumed.

If only one chart is mathematically admissible on a crossing cell (`u.upper()<1` for the series chart, `u.lower()>0` for the quotient chart), use only the admissible chart and record the chart label. If neither chart is admissible, the refinement run is `UNRESOLVED`; no silent s subdivision is allowed.

## Density representation

For ordinary boxes with q.lower()>0, retain the current scaled three-term identity

```text
rho  = s/sqrt(q),
phi  = d/sqrt(q),
Ahat = A/sqrt(q),

T1 = -4 mu R lambda rho^3 H / w,
T2 = -2 R_gamma lambda^2 H^2 Ahat rho^5 / w^2,
T3 = -2 R lambda^3 Ahat rho^3 [3 phi H - (2-s^2)sqrt(q)] / w.
```

The diagnostics show that the dominant loss was the gamma_lower evaluation of R_gamma, not T1/T3 or the scaled identity itself.

## Corner chart

The north-pole corner policy is unchanged:

- no division by a q interval containing zero;
- rho, phi, Ahat from the a-priori corner hull;
- R in [1,pi/2];
- R_gamma in [-1,-1/3];
- sqrt(q) used only as the nonnegative hull [0,sqrt(q_upper)].

## Evidence handling

- All threshold-comparison numbers are `DIAGNOSTIC_ONLY / NOT_BINDING`.
- The sole gating predicate is `upper_endpoint < 0` for all 64 exact parameter boxes.
- The producer and checker must be separate implementations.
- Failure of any box leaves this refinement `UNRESOLVED`.
- No `CERTIFIED` status may be assigned from this refinement run alone.
