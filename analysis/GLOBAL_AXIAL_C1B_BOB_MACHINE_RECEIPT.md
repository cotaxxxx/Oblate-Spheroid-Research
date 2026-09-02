# C1b B_ob bridge machine receipt

Status: `MACHINE_PASS / C1B_SUBGATE_ONLY / FULL_C1B_NOT_YET_CLOSED`

This receipt records the first accepted machine run of the predeclared one-dimensional endpoint bridge gate required by the C1b right-clamp amendment.

## Provenance

```text
repository = cotaxxxx/bg-oblate-spheroid
branch = implementation/gt-boundary-two-chart
checked-out head = 25efb59b851eb9d7a3d5ce30309eb8903d976930
Actions run id = 33606498924
job id = 100171586740
job conclusion = success
```

Pinned blobs at the accepted head:

```text
C1b pre-run amendment
analysis/GLOBAL_AXIAL_C1B_PRE_RUN_AMENDMENT.md
blob = 8e04e2efaf816bab9d9d1f3fd0a9d753538b31ad

B_ob bridge contract
analysis/GLOBAL_AXIAL_C1B_BOB_BRIDGE_CONTRACT.md
blob = 215193e2fc2a1abcf2aee2527c4c2e6f3176ea6c

producer
producer/global_axial_c1b_bob_producer.py
blob = 1a54875e1b93281c32f030081cdccd415827dcea

checker
checker/global_axial_c1b_bob_checker.py
blob = 1cded03e6c769adf26ead8b79f31e90dfbf7ce9d

workflow
.github/workflows/oblate-global-axial-c1b-bob.yml
blob = 556e749dc42bcc71a5219e49ecd11f2a0858374d
```

The workflow recorded the same checked-out head and the two contract/amendment hashes before numerical execution.

## Fixed machine policy

```text
lambda domain = [9/20,5/8]
required sign = B_ob(lambda) < 0
producer precision = 160 bits
checker precision = 192 bits
DEG = 50
B0 = 16 lambda boxes, 1024 s panels
B1 = 32 lambda boxes, 2048 s panels
B2 = 64 lambda boxes, 4096 s panels
first zero-unresolved stage authoritative
predeclared maximum panel evaluations per producer/checker = 344064
```

The checker is a separately transcribed interval computation with

```text
CHECKER_KERNEL = TRANSCRIBED_COPY_NOT_INDEPENDENT_DERIVATION
INDEPENDENCE_SCOPE = PRECISION/PARTITION/GATING
```

and imports no producer implementation.

## Producer result

```text
B0:
  lambda_boxes = 16
  s_panels = 1024
  unresolved = 2
  worst lambda box = [393/640,5/8]
  worst enclosure = [+/- 0.0636]

B1:
  lambda_boxes = 32
  s_panels = 2048
  unresolved = 0
  worst lambda box = [793/1280,5/8]
  worst enclosure = [+/- 0.0421]

C1B_BOB_FIRST_PASS B1
LOGICAL_FINAL_C1B_BOB PASS
```

## Checker result

At 192 bits, the checker independently reproduced the same stage ledger:

```text
B0: unresolved = 2
B1: unresolved = 0
C1B_BOB_FIRST_PASS B1
worst lambda box = [793/1280,5/8]
worst enclosure = [+/- 0.0421]
LOGICAL_FINAL_C1B_BOB PASS
```

The producer and checker therefore agree on the first-passing stage, unresolved counts, worst exact lambda box, and strict negative sign enclosure.

## Certified subgate consequence

The accepted run certifies the stronger full-interval statement

```text
B_ob(lambda) < 0 for every lambda in [9/20,5/8].
```

Therefore, for every later accepted C1b slab whose right wall is clamped to `t_plus=1`, the required endpoint wall sign

```text
g(1,lambda) = B_ob(lambda) < 0
```

is already supplied on that slab, independently of the eventual derived value of `lambda_B`.

This closes only the right-clamped endpoint subgate. It does not by itself certify C1b tube monotonicity, predictor acceptance, root localization, exterior cover, exact slab union, or the full C1b theorem.