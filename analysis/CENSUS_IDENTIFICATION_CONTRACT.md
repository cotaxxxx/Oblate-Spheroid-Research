# Census identification contract — oblate boundary tube

Status: `FIXED_BEFORE_RUN / NOT_BINDING`

## Machine target

Certify only

```text
quantity      = g_axis_ob(63/64, lambda)
lambda domain = [5/8, 33/50]
required sign = POS
sole gate     = full-domain enclosure lower endpoint > 0
```

Use one exact lambda box for the full interval, the inherited exact 1024-panel s partition, Arb 160 bits, and degree-50 Psi/Phi series. No lambda subdivision is authorized in the initial run.

At t=63/64, delta=1/64>0 and q=s^2(2-s^2)+lambda^2(s^2-delta)^2 is strictly positive, so no north-pole corner chart is needed.

Use the exact first-derivative density

```text
F_t = -s*mu*alpha^2 + 2*lambda*R*Ahat*rho^3*H/w,
rho  = s/sqrt(q),
Ahat = A/sqrt(q),
R = alpha/sin(alpha).
```

Tighten A by intersecting `A=1-t*mu` with `A=(1-t)+t*s^2`.

Use `u_star=3/5`:
- u.upper() <= 3/5: `u_upper`, alpha^2=Phi(u), R=Psi(u);
- u.lower() >= 3/5: `gamma_lower`, alpha=acos(gamma), alpha^2 direct, R=alpha/sqrt(u);
- crossing: evaluate the full density in both valid charts and intersect the two rigorous enclosures;
- if only one chart is admissible, use it;
- if neither is admissible, abort as UNRESOLVED.

## Logical role

Combined later with a binding monotone-tube result `partial_t g_axis_ob<0` and the separately certified endpoint sign structure of `b_ob(lambda)=g_axis_ob(1,lambda)`, this lower-edge positivity would imply:

- below the unique boundary-entry parameter: exactly one root in the tube `[63/64,1]`;
- above it: no root in that tube.

This run alone does not identify `lambda_entry_ob`, certify endpoint signs, exclude roots below 63/64, or prove a global census.
