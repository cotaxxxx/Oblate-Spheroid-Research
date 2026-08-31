# Meridian axis-row diagnostic result

Status: `DIAGNOSTIC_ONLY / NOT_BINDING`

This is the theta=0 row of the same meridian evaluator used by the six-point off-axis scan.  The surface quadrature is the refined diagnostic resolution `N_mu=240`, `N_phi=512`.  At theta=0 the integrand is phi-independent after symmetry, so the reported values are exactly the same tensor rule with the periodic phi sum collapsed analytically to its factor `2 pi`.

Sampling:

- `t in [1e-5,1]`
- 4001 equally spaced samples
- sign-change brackets refined by binary64 bisection
- center root `t=0` excluded from the nonzero-root count

No statement below is a proof of absence of further roots between samples.

| lambda | sample min | sample max | all samples negative | all samples positive | nonzero roots detected |
|---:|---:|---:|:---:|:---:|---:|
| 0.30 | -0.39832357123011813 | -2.4350138756595863e-06 | YES | NO | 0 |
| 0.50 | -0.16923412829498385 | 0.07206036179052414 | NO | NO | 1 |
| 0.60 | -0.04916809081291251 | 0.18825112569987776 | NO | NO | 1 |
| 0.65 | 6.211837375175167e-06 | 0.24860082543513878 | NO | YES | 0 |
| 0.80 | 9.638658728022831e-06 | 0.4206604297954833 | NO | YES | 0 |
| 0.95 | 1.2503382876258988e-05 | 0.569178275883542 | NO | YES | 0 |

Detected nonzero positive-axis roots:

```text
lambda=0.50: t = 0.7802783958430173, g ~= -2.08e-17
lambda=0.60: t = 0.9599010241384347, g ~= +1.39e-17
```

The lambda=0.60 root agrees with the earlier axial census value `t ~= 0.959901002...` to the expected binary64/quadrature diagnostic accuracy.

Direct three-phase diagnostic picture:

```text
lambda=0.30 (< lambda_c candidate):
    g(t,lambda) < 0 at every sampled t in (0,1]; no positive interval was seen.

lambda=0.50, 0.60 (between lambda_c and lambda_partial candidates):
    g starts positive near the center and has exactly one detected nonzero positive-axis zero.

lambda=0.65, 0.80, 0.95 (> lambda_partial candidate):
    g(t,lambda) > 0 at every sampled t in (0,1]; no nonzero positive-axis zero was seen.
```

By z -> -z symmetry, each detected positive-axis root represents the pair `+/- t*` in the full axis.

Interpretation restriction: this diagnostic supports the proposed pitchfork-to-boundary-entry picture, but it does not certify uniqueness or root exclusion between sample points.  Those are obligations for the later center-coefficient and global axial-cover contracts.
