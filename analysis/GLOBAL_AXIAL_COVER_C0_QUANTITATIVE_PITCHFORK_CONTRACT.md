# Global axial cover C0 — quantitative center pitchfork box

Status: `CHAT_RAW_AUDIT_PASS / IMPLEMENTED_PROTOTYPE / MACHINE_PENDING / NOT_BINDING`

## Purpose

This is the first obligation in global axial cover C. It converts the qualitative odd-analytic center pitchfork into an explicit certified candidate box that can later be joined to the middle axial branch tube / sign-definite cover.

Dependencies are the already closed center contracts:

```text
A: H_axis_ob(lambda)=partial_t g_axis_ob(0,lambda)
   has exactly one lambda_c^ob in (2/5,83/200),
   H<0 below lambda_c^ob and H>0 above.

B: c3_ob(lambda)=(1/6)partial_t^3 g_axis_ob(0,lambda)<0
   on [2/5,83/200].
```

C0 does not alter A or B.

## Fixed redeclaration

The C0 candidate box is now fixed as

```text
t in [0,1/2],
lambda in [2/5,83/200],
tau=t^2 in [0,1/4],
T_EDGE = 1/2.
```

The previous `t<=5/16`, `tau<=25/256`, `T_EDGE=5/16` attempt is superseded for evidence purposes. In particular, run `33446730602` is retained only as a `HISTORICAL_UNRESOLVED_CONTROL`; it is not admissible as C0 evidence.

## Reduced even function

Because `g_axis_ob(t,lambda)` is odd in `t`, define

```text
Phi(tau,lambda) := g_axis_ob(t,lambda)/t,
tau=t^2,
Phi(0,lambda)=H_axis_ob(lambda).
```

The nonsingular identity

```text
partial_tau Phi(tau,lambda)
 = (1/4) integral_0^1
     (1-x^2) partial_t^3 g_axis_ob(x t,lambda) dx
```

is exact. Therefore strict negativity of `partial_t^3 g_axis_ob` on the full C0 box implies strict decrease of `Phi` in `tau`.

At `t=0`,

```text
partial_tau Phi(0,lambda)
 = (1/6) partial_t^3 g_axis_ob(0,lambda)
 = c3_ob(lambda).
```

## Machine gates

The machine obligations are exactly:

```text
C0a: partial_t^3 g_axis_ob(t,lambda) < 0
     on [0,1/2] x [2/5,83/200].

C0b: Phi(1/4,lambda)
     = g_axis_ob(1/2,lambda)/(1/2) < 0
     for every lambda in [2/5,83/200].
```

The predeclared first-passing stage schedules remain unchanged:

```text
C0a:
A0  t_boxes=8   lambda_boxes=8   s_panels=512
A1  t_boxes=16  lambda_boxes=16  s_panels=1024
A2  t_boxes=32  lambda_boxes=32  s_panels=2048

C0b:
B0  lambda_boxes=16  s_panels=512
B1  lambda_boxes=32  s_panels=1024
B2  lambda_boxes=64  s_panels=2048
```

The first stage with `unresolved=0` is authoritative; later stages are not consulted. No undeclared refinement is permitted.

Producer precision remains 160 bits; checker precision remains 192 bits; `Psi` degree 50 and `USTAR=3/5` remain unchanged. The checker remains

```text
CHECKER_KERNEL=TRANSCRIBED_COPY_NOT_INDEPENDENT_DERIVATION
INDEPENDENCE_SCOPE=PRECISION/PARTITION/GATING
```

## General-t geometry and stable chart policy

Use

```text
mu = 1-s^2,
e = 1-mu^2,
A = 1-t mu,
d = t-mu,
q = e + lambda^2 d^2,
w^2 = mu^2 + lambda^2 e,
gamma = lambda A/(w sqrt(q)).
```

The exact complement identity is

```text
u = 1-gamma^2
  = e [mu(1-lambda^2)+lambda^2 t]^2/(w^2 q) >= 0.
```

Because the removable `u=0` locus moves with `(t,lambda)`, chart handling is fixed:

```text
intersect u only with exact 0<=u<=1;
if upper(u)<=3/5: use the Psi series chart;
elif lower(u)>0: use the direct chart;
else: UNRESOLVED.
```

Literal division by `u`, `u^2`, or `u^3` across an interval meeting zero is forbidden.

For C0b, use the stable exact identity

```text
alpha^2 = u R^2,
R = asin(sqrt(u))/sqrt(u),
```

through the same two-chart continuation.

## General-t derivative recurrence

Define

```text
L2 = lambda^2,
N  = -mu q - A L2 d,
N1 = -L2 e,
M  = N1 q - 3 N L2 d,
M1 = lambda^4 e d - 3 L2 N,
P  = M1 q - 5 M L2 d,
M2 = 4 lambda^4 e,
P1 = M2 q - 3 L2 d M1 - 5 L2 M.
```

Then exactly

```text
gamma_t    = lambda N/(w q^(3/2)),
gamma_tt   = lambda M/(w q^(5/2)),
gamma_ttt  = lambda P/(w q^(7/2)),
gamma_tttt = lambda(P1 q - 7 P L2 d)/(w q^(9/2)).
```

With `C=R gamma_t`,

```text
C_tt
 = R_gammagamma gamma_t^3
   + 3 R_gamma gamma_t gamma_tt
   + R gamma_ttt,

C_ttt
 = R_gammagammagamma gamma_t^4
   + 6 R_gammagamma gamma_t^2 gamma_tt
   + 3 R_gamma gamma_tt^2
   + 4 R_gamma gamma_t gamma_ttt
   + R gamma_tttt.
```

Hence the canonical C0a density is

```text
partial_t^3 F_t = s [8 mu C_tt - 2 A C_ttt],
```

and

```text
partial_t^3 g_axis_ob(t,lambda)
 = integral_0^sqrt(2) partial_t^3 F_t ds.
```

## Logical consequence of C0a + C0b + A

If C0a and C0b pass, then `Phi(tau,lambda)` is strictly decreasing in `tau` on `[0,1/4]`. Using the certified sign structure of `H_axis_ob=Phi(0,lambda)` from A:

```text
lambda < lambda_c^ob:
  no nonzero axial root in 0<t<=1/2.

lambda = lambda_c^ob:
  t=0 is the only axial root in the C0 box.

lambda > lambda_c^ob:
  exactly one positive root t*(lambda) with 0<t*(lambda)<1/2,
  together with its symmetric negative partner.
```

The observed branch value near `lambda=83/200` is approximately `t*~0.25`, safely inside the redeclared box; this is diagnostic only.

## REPORTED_NOT_GATING expectations

Before the rerun, direct high-precision diagnostics suggest approximately

```text
Phi(1/4, 2/5)      ~ -0.13,
Phi(1/4, 83/200)   ~ -0.0507,
```

and `partial_t^3 g_axis_ob` is expected to retain a margin of roughly `-1.5` or better over the enlarged `t` interval. These are expectations only and are not gates.

## Historical unresolved control

```text
run 33446730602
old box: t<=5/16, tau<=25/256, T_EDGE=5/16
classification: HISTORICAL_UNRESOLVED_CONTROL / NOT_EVIDENCE
```

Its C0b failure is retained as a control showing that the old edge did not have enough enclosure margin. It must not be cited in a positive C0 machine receipt.

## Explicit exclusions

C0 does not certify:

- any axial statement for lambda outside `[2/5,83/200]`;
- continuation of the nonzero branch beyond `t=1/2`;
- connection from `t=1/2` to the certified boundary band `[31/32,1]`;
- absence of additional roots in that middle region;
- any off-axis stationary-orbit statement.

After C0 closes, the next axial obligation is C1: cover the middle region between `t=1/2` and `[31/32,1]` for the relevant lambda range by a branch tube plus sign-definite boxes.
