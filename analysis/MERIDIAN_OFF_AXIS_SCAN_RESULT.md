# Meridian off-axis six-point scan — result

Status: `DIAGNOSTIC_ONLY / NOT_BINDING / PRE_THEOREM_SCAN`

Source evaluator:

- `analysis/meridian_off_axis_scan.py`
- baseline quadrature: `N_mu=160`, `N_phi=256`
- refined candidate validation: `N_mu=240`, `N_phi=512`
- lambda set fixed before scan: `{0.30,0.50,0.60,0.65,0.80,0.95}`
- Actions run: `33380520435`, step `Run six-point meridian off-axis diagnostic` SUCCESS
- axis consistency control: PASS at all four pinned points

## Raw scan summary and corrected interpretation

The raw script labels every converged point with `q>0` as off-axis. At lambda 0.30 and 0.50, permissive near-center seeds converge numerically to extremely small q rather than to a finite-radius stationary orbit. These are therefore interpreted as `CENTER_COLLAPSE_ARTIFACT`, not as genuine off-axis stationary orbits.

| lambda | raw candidates | finite-q off-axis candidates | equatorial candidates | q>0.95 off-axis candidates | minimum off-axis grid norm |
|---:|---:|---:|---:|---:|---:|
| 0.30 | 33 | 0 | 0 | 0 | 2.393102198720456e-4 |
| 0.50 | 4 | 0 | 0 | 0 | 4.765423587214939e-3 |
| 0.60 | 0 | 0 | 0 | 0 | 9.943851676856817e-3 |
| 0.65 | 0 | 0 | 0 | 0 | 1.243939254612293e-2 |
| 0.80 | 0 | 0 | 0 | 0 | 1.928262905537969e-2 |
| 0.95 | 0 | 0 | 0 | 0 | 2.500255832081703e-2 |

For lambda 0.30, all 33 refined points satisfy approximately

```text
q <= 1.14e-5,
theta approximately 0.3912 rad,
```

and collapse toward the center. An independent local rerun from `(q,theta)=(0.02,pi/8)` and `(0.08,pi/8)` converged to `q approximately 9.8e-6`, confirming the center-collapse interpretation.

For lambda 0.50, all four raw off-axis labels also collapse to the center, with q of order `1e-10`. The other coarse seeds are on the symmetry axis near the known axial root and are excluded from off-axis classification.

No equatorial orbit was detected at any sampled lambda. No finite-q off-axis candidate with `q>0.95` was detected, so the `NEAR_BOUNDARY_UNRELIABLE` validation branch was not triggered by a genuine off-axis candidate in this scan.

## Center Hessian diagnostic

Axial center coefficient estimates `g_axis_ob(eps,lambda)/eps` were stable across `eps in {1e-4,3e-4,1e-3}`:

| lambda | axial coefficient sign | representative value |
|---:|:---:|---:|
| 0.30 | NEG | -0.2435014 |
| 0.50 | POS | +0.2369730 |
| 0.60 | POS | +0.4962309 |
| 0.65 | POS | +0.6211837 |
| 0.80 | POS | +0.9638659 |
| 0.95 | POS | +1.2503383 |

A high-precision diagnostic bisection using the independent axial kernel gives the candidate center axial degeneracy

```text
lambda_c^ob approximately 0.40795886135.
```

The transverse/radial center coefficient, independently estimated from `E_r(eps,0)/eps` with the refined meridian evaluator, remains positive at all six sampled lambdas and at the candidate lambda_c. Representative refined values are:

```text
lambda=0.30:          H_perp approximately +1.4313616
lambda=lambda_c^ob:  H_perp approximately +1.5524020
lambda=0.50:          H_perp approximately +1.5887418
lambda=0.60:          H_perp approximately +1.5818388
lambda=0.65:          H_perp approximately +1.5655013
lambda=0.80:          H_perp approximately +1.4832683
lambda=0.95:          H_perp approximately +1.3729616
```

Thus the diagnostic picture is: below `lambda_c^ob`, the center is a saddle with two positive transverse directions and one negative axial direction; above `lambda_c^ob`, the center is a local minimum. At `lambda_c^ob`, only the axial eigenvalue is indicated to vanish.

## Pre-theorem implication only

The six-point scan supports, but does not prove, the following theorem shape:

1. a center axial degeneracy value `lambda_c^ob` near `0.40795886135`;
2. an axial nonzero stationary branch for an intermediate lambda range, to be certified globally on-axis;
3. no off-axis stationary latitude circles detected on the sampled lambdas;
4. no sampled evidence for an off-axis boundary-entry event.

The absence of off-axis points remains `DIAGNOSTIC_ONLY`. A later meridian exclusion contract is still required before theorem item (v) can state nonexistence.
