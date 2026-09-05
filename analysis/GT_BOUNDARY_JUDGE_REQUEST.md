# External Judge request — oblate boundary t-derivative

Status: `SUBMITTED_FOR_JUDGE / NOT_BINDING`

This file is a request for an external Judge decision. It does not itself
promote the claim or replace an independent Judge receipt.

## Claim under review

```text
quantity      = partial_t g_axis_ob(1,lambda)
lambda domain = [5/8,33/50]
required sign = NEG
gating rule   = full-domain independent checker enclosure upper endpoint < 0
```

## Pinned audited source

- source branch: `implementation/gt-boundary-two-chart`
- audited source commit: `23cd08741ba797597c1d6ba9c74da41bdb66b1c4`
- producer path: `producer/gt_boundary_interval_producer.py`
- producer blob SHA: `00e3986b728f6b21ddc42131c132585da568b830`
- checker path: `checker/gt_boundary_interval_checker.py`
- checker blob SHA: `ae2b06659c657a1584c79e88c532ea2862726538`
- symbolic audit path: `analysis/GT_BOUNDARY_SYMBOLIC_AUDIT.md`
- symbolic audit blob SHA at audited source: `ceae80b6a301b3aa05583606a56354d074c9d03e`

Any change to the mathematical producer or checker after these pins requires a
new Judge request. Changes only to this request file do not alter the pinned
source object above.

## Owner symbolic audit

Content-level verdict supplied by the project owner: `PASS`.

The owner independently checked the three regularized terms:

```text
s*4 mu R gamma_t
  -> -4(1-e) lambda R C/(w qhat^(3/2))

s*(-2s^2) R_gamma gamma_t^2
  -> -2 s lambda^2 R_gamma C^2/(w^2 qhat^3)

s*(-2s^2) R gamma_tt
  -> -2 e lambda^3 R D/(w qhat^(5/2))
```

and the upper-chart substitution

```text
R_gamma = -2 gamma Psi_prime(u)
gamma   = lambda s/(w sqrt(qhat))

=> +4 e lambda^3 Psi_prime(u) C^2/(w^3 qhat^(7/2)).
```

The lower-chart denominator was also checked to stay separated from zero on
`s in [0,1]`, since the internal `u=0` point has `s0>1` throughout the lambda
bracket. Producer and checker independently reconstruct the kernel and the
checker enforces `u.upper() < 1` for the series chart.

## Clean-room Actions receipt

- workflow: `Oblate boundary t-derivative prototype`
- workflow id: `346289126`
- run id: `33354706446`
- run number: `11`
- source commit: `23cd08741ba797597c1d6ba9c74da41bdb66b1c4`
- conclusion: `success`
- job id: `99374531157`
- inherited exact endpoint controls: `success`
- producer + independent checker step: `success`

The log reports:

```text
REPORTED checker enclosure: [-1e+0 +/- 0.740]
GATING criterion: upper endpoint < 0
Ran 1 test ... OK
```

The displayed Arb ball has a strictly negative upper endpoint, so the fixed
gating predicate passed on the complete lambda interval in this run.

## REPORTED_NOT_GATING expectations

These values are comparison-only and are not part of the acceptance predicate:

```text
5/8   = -1.4120900996030582330984866619528326407579821748752
13/20 = -1.4717090003859539426113646310237584846969543547289
33/50 = -1.4958034682340728485822766948219344845501715771395
```

The final value corrects an earlier non-gating transcription error.

## Requested Judge decision

Please independently verify:

1. the pinned source hashes and Actions receipt;
2. symbolic correspondence between the endpoint derivative and both charts;
3. independence of producer and checker mathematical reconstruction;
4. inherited `Psi` / `Psi_prime` series and rigorous remainder handling;
5. complete `[5/8,33/50]` lambda coverage and complete `[0,sqrt(2)]` s-cell cover;
6. that point expectations are non-gating;
7. that the sole gating predicate is the full-domain checker upper endpoint `<0`.

Return a separate Judge receipt with `PASS` or `FAIL`, the pinned identifiers
above, and any exceptions. No certification promotion is authorized by this
request alone.
