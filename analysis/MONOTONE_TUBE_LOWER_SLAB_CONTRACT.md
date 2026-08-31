# Lower monotone slab and 31/32 edge — fixed contract

Status: `PROTOTYPE / NOT_AUDITED / NOT_BINDING`

This is a separate declaration. It does not modify or replace the existing `[63/64,1]` monotone-tube refinement.

## Claim A — lower slab monotonicity

```text
quantity: partial_t g_axis_ob(t,lambda)
t domain: [31/32,63/64]
lambda domain: [5/8,33/50]
t boxes: 8 exact equal boxes
lambda boxes: 8 exact equal boxes
s panels: 1024
series degree: 50
producer bits: 160
checker bits: 192
u_star: 3/5
required sign: NEG
sole gate: every one of 64 parameter boxes has total.upper() < 0
```

Since `t<=63/64<1`, q is uniformly positive at s=0; no corner chart is permitted or needed. Ordinary cells use exactly the audited refinement policy: A intersection, factorized-u / 1-gamma^2 mutual tightening, gamma tightening from u, `u_star=3/5`, and termwise intersection on threshold-crossing cells.

## Claim B — new lower edge

```text
quantity: g_axis_ob(31/32,lambda)
lambda domain: [5/8,33/50]
initial lambda boxes: 8 exact equal boxes
s panels: 1024
series degree: 50
producer bits: 160
checker bits: 192
u_star: 3/5
required sign: POS
sole gate: every lambda box has total.lower() > 0
```

The corrected first-derivative density is

```text
F_t = -s*mu*alpha^2 + 2*lambda*A*R*rho^3*H/w,
rho=s/sqrt(q).
```

`Ahat=A/sqrt(q)` is forbidden in this first-derivative density. If Claim B is unresolved, refinement must be separately declared; changing T requires a new contract.
