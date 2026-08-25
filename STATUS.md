# Research Status

Updated: 2026-08-25

## Global status

`NOT_BINDING / DIAGNOSTIC_ONLY`

This repository currently contains no certified theorem, certified numerical
value, approved production kernel, or Actions-produced clean-room certificate.

## Analytically derived kernel

For the oblate spheroid

```text
x^2 + y^2 + z^2/lambda^2 = 1,   0 < lambda < 1,
```

write an axial base point as `p = (0, 0, lambda*t)` and set

```text
q = 1 - mu^2 + lambda^2*(mu - t)^2
w^2 = lambda^2*(1 - mu^2) + mu^2
gamma = lambda*(1 - t*mu)/(w*sqrt(q))
h(c) = acos(c)^2
```

Then

```text
E_lambda(t) = (1/2) integral[-1,1] (1 - t*mu)*h(gamma) dmu
g_axis_ob(t,lambda) = partial_t E_lambda(t)
b_ob(lambda) = g_axis_ob(1,lambda)
```

The substitution `mu = 1 - s^2` regularizes the transformed endpoint
density and supports a one-sided `C^1` extension to `t = 1`. This analytic
statement still requires a formal manuscript proof and independent audit.

## Candidate numerical evidence — not certified

The following values are candidate evidence, not certified enclosures:

```text
lambda_entry_ob = 0.6435457703666799690435  [HIGH_PRECISION; mpmath dps=40; tanh-sinh]
lambda_axis_ob  = 0.4079588603009463642491058701855256993  [HIGH_PRECISION; two-source agreement]
b_ob_prime      = +1.10246                  [HIGH_PRECISION; two-source agreement]
gt_boundary_ob  = -1.45623019               [HIGH_PRECISION; mpmath dps=50; one-sided differences]
entry_slope_ob  = 0.757064                  [HIGH_PRECISION; ratio b_ob_prime/(-gt_boundary_ob)]
b_ob(1)         = pi^2/32                   [EXACT]
```

The original values were supplied through chat and remain candidate evidence
under the two-layer certification rule. `lambda_axis_ob` now has two direct
computational sources: the original `mpmath` evaluation (`dps=40`,
tanh-sinh) and a native axial-equation calculation of
`partial_t g_axis_ob(0,lambda)=0` using Python `Decimal`, split standalone
tanh-sinh quadrature, centered slopes, and Richardson extrapolation at 50 and
80 decimal digits. The two native precision settings agree through the stable
prefix printed above, and the result agrees with the original recorded value
through all 20 of its decimal places. `lambda_entry_ob` also has an
independent Decimal/tanh-sinh reproduction of the endpoint equation.

The `b_ob_prime` candidate now has a second numerical source: the binary64
Simpson fold diagnostic reproduces local difference ratios approximately
`1.10247` to `1.10250` across the boundary sign change, consistent with
the prior high-precision value `1.10246`. The endpoint derivative candidate
uses the independently audited one-sided sequence
`-1.45550032, -1.45622003, -1.45623006, -1.45623019, -1.45623019` for
steps `1e-4, 1e-6, 1e-8, 1e-10, 1e-12`. None of these agreements promotes
a value to `CERTIFIED_ENCLOSURE`.

Expected signs:

```text
b_ob(0.60) < 0
b_ob(0.70) > 0
b_ob(1) = pi^2/32 > 0
```

Measured diagnostic values for the first two signs were approximately
`-0.04917` and `+0.06016`. Their derivation class remains diagnostic. Failure
to reproduce the signs requires investigation; agreement does not constitute
certification.

## Finite-window fold diagnostic

A direct scan on `lambda in [0.630,0.650]` observed one positive-axis root
through `lambda=0.643`, no root from `lambda=0.644` onward, and a branch
approaching `t=1` at `lambda_entry_ob`. No interior fold signature was
observed in this window. This is not a global no-fold result: the scan does not
cover lambda outside this window and is not interval arithmetic.

## Precision-robustness correction

A precision-dependent endpoint failure was reproduced in the prototype
`b_ob` evaluator. The former `64*mp.eps` post-division slack admitted or
rejected a rounded value of `gamma` non-monotonically as the requested
precision changed. Failures were observed at dps 30, 35, 60, and 80.

The regression test was committed before the implementation correction. The
endpoint geometry now evaluates the exact factorization

```text
1 - gamma^2
  = (2 - s^2)*(1 - (1 - lambda^2)*s^2)^2/(w^2*qhat).
```

This exposes the endpoint factor `2-s^2` and avoids forming a quotient that
can round above one. A tanh-sinh node whose rounded `s^2` exceeds 2 only by
at most `sqrt(eps)` is projected to the exact endpoint; a larger excursion
fails closed.

Correction checkpoint:

```text
branch head = 5cc212d47145704d39cb486df28eefc2e3938d79
workflow run = #43, success
status       = PROTOTYPE / NOT_AUDITED
```

The project owner independently checked the factorization and reran the
corrected evaluator at ten precision settings from dps 20 through 120. All
previously failing settings completed, and the observed error decreased from
approximately `1e-22` to `1e-122` with increasing precision. Values at
`lambda=0.408` and the reported root agreed across dps 30, 50, and 80.
This verifies the robustness correction but does not promote the evaluator or
any numerical value to `AUDITED_SOURCE`, `CERTIFIED_ENCLOSURE`, or
`CERTIFIED`.

The earlier split-versus-unsplit quadrature comparison is now optional
diagnostic work rather than a blocking obligation, because the unsplit
quadrature displays precision-proportional convergence over the tested range.

A second occurrence of the same robustness defect was subsequently found in
the interior `g_axis_ob` path for `t<1`. The case
`g_axis_ob(0.99,0.63)` reproduced the former dps-dependent failure pattern.
The general identity

```text
1 - gamma^2
  = (1 - mu^2)*((1 - lambda^2)*mu + lambda^2*t)^2/(w^2*q)
```

now replaces the direct quotient on that path. It reduces exactly to the
endpoint factorization when `t=1`. A dps 30, 50, and 80 regression was
committed before the implementation change. GitHub Actions run #61 succeeded,
and the previously recorded center-axis nondegeneracy sequence was unchanged
at all printed digits. The correction checkpoint is
`c9fb76ebdb94fd16bdbe9414107693952874cc9f`. Evidence status remains
`PROTOTYPE / NOT_AUDITED`.

## Candidate center-axis nondegeneracy

A 50-dps centered-difference and Richardson diagnostic at
`lambda_axis_ob` produced

```text
A_ob(lambda_axis_ob)       = -5.55e-25
A_ob_prime(lambda_axis_ob) = +2.491132481221525520635103855...
C_ob                       = -0.261396885193674917352806250...
-A_ob_prime/C_ob           = +9.530077144476257310077726938...
```

Here `A_ob(lambda)=partial_t g_axis_ob(0,lambda)` and `C_ob` is the
coefficient of `t^3` in the odd expansion of `g_axis_ob` at the center.
The raw sequences converge with stable positive sign for `A_ob_prime` and
stable negative sign for `C_ob`. The candidate normal form is therefore

```text
t^2 approximately 9.5300771445*(lambda-lambda_axis_ob),
```

so the candidate noncentral axial branch lies on the
`lambda > lambda_axis_ob` side, consistent with absorption into the center as
lambda decreases. The full diagnostic record is
[diagnostics/oblate_axis_nondegeneracy_result.json](diagnostics/oblate_axis_nondegeneracy_result.json).

Evidence status remains `DIAGNOSTIC_ONLY / NOT_BINDING`; derivation class is
`HIGH_PRECISION`. GitHub Actions run #53 succeeded. These calculations do not
prove nondegeneracy or supply certified coefficient enclosures.

## Candidate transverse index on the axial branch

For a transverse displacement `p=(r,0,lambda*t)`, the second derivative
`Q_perp_ob=E_rr(0,t,lambda)` was reduced analytically to a one-dimensional
azimuthally averaged integral and evaluated at seven positive-axis branch
points.

```text
lambda    t                     z=lambda*t            Q_perp_ob
0.42      0.3299485239648909    0.1385783800652542    +1.5188410161701126
0.45      0.5793708519677305    0.2607168833854787    +1.4279175760127804
0.50      0.7802783958430172    0.3901391979215086    +1.2639635299552409
0.55      0.8909899971394450    0.4900444984266947    +1.0968377348233276
0.60      0.9599010020396870    0.5759406012238122    +0.9346164228385508
0.63      0.9890775444970755    0.6231188530331576    +0.8414580737026062
0.6435    0.9999653387083598    0.6434776954588295    +0.8007594212804716
```

All sampled transverse eigenvalues are positive and remain separated from
zero. Together with the negative axial second variation, this supports Morse
index 1 for the sampled noncentral stationary points. The machine-readable
record is
[diagnostics/oblate_transverse_index_result.json](diagnostics/oblate_transverse_index_result.json).

Evidence status is `DIAGNOSTIC_ONLY / NOT_BINDING`; derivation class is
`HIGH_PRECISION`. GitHub Actions run #67 succeeded. Finite sampling does not
prove positivity on the entire branch and does not exclude additional
stationary points.

## Open obligations

- independently audit and intervalize the endpoint-regular axial prototype;
- certify existence, uniqueness, and transversality of `lambda_entry_ob`;
- certify `b_ob_prime > 0` and `gt_boundary_ob < 0`;
- certify the center-axis degeneracy and nondegenerate pitchfork coefficients;
- exclude interior folds and additional meridian stationary points globally;
- keep the `lambda -> 0` uniform tail outside the present finite-window claim.
