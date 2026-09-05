# Census lower-edge machine receipt — superseded v1

Status: `SUPERSEDED_INVALID / NOT_BINDING`

The earlier v1 machine PASS for

```text
g_axis_ob(63/64, lambda) > 0
lambda in [5/8, 33/50]
```

is withdrawn.

## Defect

The v1 first-t density used

```text
2 lambda R Ahat rho^3 H / w,
Ahat=A/sqrt(q),
rho=s/sqrt(q),
```

for the second term. This introduces one extra factor `q^(-1/2)`.

From

```text
F_t=s[-mu alpha^2 - 2 A R gamma_t],
gamma_t=-lambda s^2 H/(w q^(3/2)),
```

the correct regularized first-t density is

```text
F_t = -s mu alpha^2 + 2 lambda A R rho^3 H/w,
```

with `A`, not `Ahat`.

This defect was exposed by printing the full Arb margin: the invalid v1 checker enclosure was approximately

```text
[0.0414298359373783, 0.204878853734044],
```

which cannot contain the independent high-precision value near `lambda=5/8`, approximately `+4.37e-4`.

## Superseded evidence

The following are retained only for provenance and are **not valid evidence**:

- v1 producer blob: `243124b76726de8a81ab42ba5edf19c000c3a963`
- v1 checker blob: `0245d6c680c54e91eb6123d6fd40c9f210e60a40`
- Actions #101 / run id `33368313307`
- Actions #107 / run id `33369692803`

The producer/checker were corrected independently and schema was advanced to `bg-oblate-spheroid.census-lower-edge.v2`.

No lower-edge Judge request may cite the v1 receipt. A new machine receipt must be created only after the corrected v2 run is evaluated.
