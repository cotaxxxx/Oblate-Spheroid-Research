# Global axial cover C0 — quantitative center pitchfork box

Status: `PROTOTYPE / SYMBOLIC_READY / MACHINE_PENDING / NOT_BINDING`

## Purpose

This is the first obligation in global axial cover C. It converts the qualitative odd-analytic pitchfork near the certified center parameter into an explicit box that can be joined to the later sign-definite cover / branch tube.

Dependencies:

```text
A: H_axis_ob(lambda)=partial_t g_axis_ob(0,lambda)
   has exactly one lambda_c^ob in (2/5,83/200),
   H<0 below lambda_c^ob and H>0 above.

B: c3_ob(lambda)=(1/6)partial_t^3 g_axis_ob(0,lambda)<0
   on [2/5,83/200].
```

C0 does not alter either A or B.

## Candidate explicit box

Use

```text
t in [0,5/16],
lambda in [2/5,83/200],
tau=t^2 in [0,25/256].
```

The endpoint `5/16` is provisional until machine gating closes. It is chosen with ample diagnostic margin above the largest local root in the A bracket.

## Reduced even function

Because `g_axis_ob(t,lambda)` is odd in `t`, define the analytic even quotient

```text
Phi(tau,lambda) := g_axis_ob(t,lambda)/t,
tau=t^2,
```

with analytic continuation

```text
Phi(0,lambda)=H_axis_ob(lambda).
```

For stable evaluation at `tau=0`, do not divide by `t`. Use

```text
Phi(tau,lambda)
 = integral_0^1 partial_t g_axis_ob(u t,lambda) du.
```

Differentiating in `tau` gives the nonsingular identities

```text
partial_tau Phi(tau,lambda)
 = (1/2) integral_0^1 integral_0^1
     u^2 partial_t^3 g_axis_ob(v u t,lambda) dv du
```

and equivalently

```text
partial_tau Phi(tau,lambda)
 = (1/4) integral_0^1
     (1-x^2) partial_t^3 g_axis_ob(x t,lambda) dx.
```

At `t=0`, this gives exactly

```text
partial_tau Phi(0,lambda)
 = (1/6) partial_t^3 g_axis_ob(0,lambda)
 = c3_ob(lambda).
```

## Simplified machine strategy

A separate proof of `partial_lambda Phi>0` is not required for the C0 existence/uniqueness theorem.

A already gives the sign of

```text
Phi(0,lambda)=H_axis_ob(lambda)
```

on either side of `lambda_c^ob`. Therefore it is enough to certify the stronger two-dimensional claim

```text
C0a: partial_t^3 g_axis_ob(t,lambda) < 0
     on [0,5/16] x [2/5,83/200],
```

which implies

```text
partial_tau Phi(tau,lambda) < 0
```

on the full C0 box by the positive-weight integral identity, together with

```text
C0b: Phi(25/256,lambda) < 0
     for every lambda in [2/5,83/200].
```

For C0b, since `t=5/16` is bounded away from zero, either direct `g/t` evaluation or the integral representation of `Phi` is acceptable. The implementation should prefer whichever gives the narrower Arb enclosure.

## General-t geometry

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

On the candidate box, `t<=5/16<1`, so the north-corner singularity `s=0,t=1` is absent and `q>0` uniformly.

The exact stable complement is

```text
u = 1-gamma^2
  = e [mu(1-lambda^2)+lambda^2 t]^2/(w^2 q) >= 0.
```

Unlike B at `t=0`, the interior removable `u=0` locus moves with `(t,lambda)`. This is harmless only if the implementation uses the analytic `Psi(u)` chart whenever the interval may meet `u=0`; literal division by `u`, `u^2`, or `u^3` is forbidden there.

## General-t gamma derivative recurrence

Keep the pre-limit derivatives factorized. Define

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
gamma_t
 = lambda N/(w q^(3/2)),

gamma_tt
 = lambda M/(w q^(5/2)),

gamma_ttt
 = lambda P/(w q^(7/2)),

gamma_tttt
 = lambda (P1 q - 7 P L2 d)/(w q^(9/2)).
```

These identities reduce at `t=0` to the four formulas already audited in B.

## General-t third derivative density

Retain the B organization

```text
R = acos(gamma)/sqrt(1-gamma^2),
C = R gamma_t.
```

With

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
   + R gamma_tttt,
```

we have for all pre-limit `t`

```text
partial_t^3 F_t
 = s [8 mu C_tt - 2 A C_ttt].
```

Hence

```text
partial_t^3 g_axis_ob(t,lambda)
 = integral_0^sqrt(2)
     s [8 mu C_tt - 2 A C_ttt] ds.
```

This is the canonical C0a machine density.

Use the same `R_gamma`, `R_gammagamma`, `R_gammagammagamma` two-chart formulas and `Psi'''` tail already audited in B.

## Logical consequence of C0a + C0b + A

If C0a and C0b are certified, then for each fixed lambda in `[2/5,83/200]`, `Phi(tau,lambda)` is strictly decreasing in `tau` on `[0,25/256]`.

Therefore:

```text
lambda < lambda_c^ob:
  Phi(0,lambda)<0, hence no nonzero axial root in 0<t<=5/16.

lambda = lambda_c^ob:
  Phi(0,lambda)=0 and Phi(tau,lambda)<0 for every tau>0,
  hence only the center root occurs in the box.

lambda > lambda_c^ob:
  Phi(0,lambda)>0 while Phi(25/256,lambda)<0,
  hence exactly one tau*(lambda) in (0,25/256),
  equivalently exactly one positive root t*(lambda) in (0,5/16),
  together with its symmetric negative partner.
```

This is the quantitative C0 pitchfork box needed by global cover C.

## REPORTED_NOT_GATING diagnostics

High-precision direct evaluation before machine implementation gives approximately

```text
partial_lambda Phi > 2.35  on sampled points of the candidate box,
partial_tau Phi   < -0.25 on sampled points,

Phi(t=5/16, lambda=2/5)   ~ -0.04444,
Phi(t=5/16, lambda_c)     ~ -0.02564,
Phi(t=5/16, lambda=83/200)~ -0.008864.
```

Also sampled `partial_t^3 g_axis_ob` remains negative with values roughly from `-1.51` to `-1.70` across the candidate box. These are expectations only and are not gates.

## Machine architecture proposal

Start with:

```text
producer bits: 160
checker bits: 192
lambda boxes: 64
t boxes: 64
s panels: 4096
Psi degree: 50
u threshold: 3/5
checker kernel: TRANSCRIBED_COPY_NOT_INDEPENDENT_DERIVATION
independence scope: PRECISION/PARTITION/GATING
```

If direct 64x64 boxes are too wide, refine `t` first; do not silently change the declared partition after a gating run.

## Explicit exclusions

C0 does not certify:

- any axial statement for lambda outside `[2/5,83/200]`;
- continuation of the nonzero branch beyond `t=5/16`;
- connection to the certified boundary band `[31/32,1]`;
- absence of additional roots in the middle axial region;
- any off-axis stationary-orbit statement.

Those remain later obligations in C and D.
