# Center pitchfork coefficient B — machine receipt

Status: `AUDITED_SOURCE / CHAT_RAW_AUDIT_PASS / MACHINE_GATING_PASS / EXTERNAL_JUDGE_PENDING / NOT_BINDING`

## Scoped claim

This receipt supports only

```text
c3_ob(lambda) := (1/6) partial_t^3 g_axis_ob(0,lambda) < 0
for every lambda in [2/5,83/200].
```

Together with certified contract A, this is the cubic nondegeneracy/sign input for the local supercritical center pitchfork. This receipt does not by itself certify a quantitative `(epsilon,t0)` neighborhood or any global axial census.

## Symbolic/raw audit pin

Canonical symbolic note:

```text
analysis/CENTER_PITCHFORK_SYMBOLIC_NOTE.md
commit 943aebe575785e8433e3ea39ea0c6e23e9f7f512
blob efabc9d6c07d2176a62d1d985cba7f8ea01cc629
status CHAT_RAW_AUDIT_PASS / SYMBOLIC_DERIVATION_AUDITED / NOT_BINDING
```

The independent raw audit checked all ten checklist items: parity; derivative-chain coefficients `4,6,8`; `C_tt` coefficients `1,3,1`; `C_ttt` coefficients `1,6,3,4,1`; all four `gamma` t-derivatives; both charts for `R_gammagammagamma`; the `Psi'''` tail and exact denominator `89/245`; the fixed removable `u=0` loci; exact sphere control `c3_ob(1)=-8/9`; and the fact that only the interval upper-sign gate is theorem-gating.

## Contract pin

```text
analysis/CENTER_PITCHFORK_CONTRACT.md
blob 0c98759fd4c1026e70d4ec49f6487223e026e6cf
```

## Machine source pins

Producer:

```text
producer/center_pitchfork_producer.py
blob 468ab9a3dd318998eb22b8bfbc09c3848cfb45d4
Arb precision 160 bits
s panels 4096
lambda boxes 64 exact boxes on [2/5,83/200]
Psi degree 50
u threshold 3/5
```

Checker:

```text
checker/center_pitchfork_checker.py
blob 46d05b1aaef31a2e24beceed43d29113af351842
Arb precision 192 bits
s panels 4096
lambda boxes 64 exact boxes on [2/5,83/200]
Psi degree 50
u threshold 3/5
```

The A-certified producer/checker files were not modified; B uses separate source files.

Checker independence declaration:

```text
CHECKER_KERNEL=TRANSCRIBED_COPY_NOT_INDEPENDENT_DERIVATION
INDEPENDENCE_SCOPE=PRECISION/PARTITION/GATING
```

The checker independently reconstructs its rational/sqrt(2) partition and runs at higher precision, but its mathematical B kernel is a transcribed copy of the producer formulation. Derivational independence is supplied by the separately audited symbolic derivation and the user's independent SymPy/finite-value checks, not by checker lineage alone.

## Successful Actions evidence

Initial focused gating run:

```text
run 33437813853
job center-pitchfork-evidence
job id 99638430514
head 07c01d4b5e38f64ecf610ca2d9d5b8390034d720
conclusion SUCCESS
```

Exact-report focused run:

```text
run 33438258204
job center-pitchfork-evidence
job id 99639876658
head cbaa72fa2e55f5b5e0a698a763a680be35e1a7ae
conclusion SUCCESS
```

The second run repeats both gating producer/checker and then executes a `REPORT_ONLY / NOT_GATING` exact-enclosure reporter. The report-only additions do not alter the pinned producer/checker blobs.

## Gating result

Both producer and checker report

```text
C3_NEG_ALL PASS
weakest_box [2/5,5123/12800]
SPHERE_C3_NEG_8_9 PASS
LOGICAL_FINAL_CLAIM PASS
```

Thus every one of the 64 exact lambda boxes covering `[2/5,83/200]` has strictly negative `upper(c3_ob)` in both evaluators.

## Exact Arb enclosures — report-only reconstruction

The reporter prints midpoint/radius with 80 digits. The following are pinned verbatim from run `33438258204`, job `99639876658`.

### Producer

Weakest box `[2/5,5123/12800]`:

```text
mid = -0.25200435805273807940443221986802789258472610665641142982367936522688096932891324
rad = 0.011056052855565212666988372802734375000000000000000000000000000000000000000000000
```

`c3_ob(2/5)` (`REPORTED_NOT_GATING` point enclosure):

```text
mid = -0.25186554449442014946552235091577374577545428448892809014438724463906809095038132
rad = 0.0089171896979678422212600708007812500000000000000000000000000000000000000000000000
```

`c3_ob(0.4079588603)` (`REPORTED_NOT_GATING` point enclosure):

```text
mid = -0.26138846616846582642611930017748498530154299199024097234095492539867753290676577
rad = 0.0089188132405979558825492858886718750000000000000000000000000000000000000000000000
```

`c3_ob(83/200)` (`REPORTED_NOT_GATING` point enclosure):

```text
mid = -0.26988560177604200126450431560186547075150083409289777838487796107617735962751245
rad = 0.0089228837023256346583366394042968750000000000000000000000000000000000000000000000
```

Sphere control:

```text
mid = -0.88887275639247288629952554173125248535472520314067962966578351274291276173886575
rad = 0.015766709693707525730133056640625000000000000000000000000000000000000000000000000
contains -8/9
```

### Checker

Weakest box `[2/5,5123/12800]`:

```text
mid = -0.25200435805262419867803132360427527568050224092122718245008790617993586076104520
rad = 0.011056052841013297438621520996093750000000000000000000000000000000000000000000000
```

`c3_ob(2/5)` (`REPORTED_NOT_GATING` point enclosure):

```text
mid = -0.25186554449478878630144573918526398023570893903615505386254302040648712611571900
rad = 0.0089171896834159269928932189941406250000000000000000000000000000000000000000000000
```

`c3_ob(0.4079588603)` (`REPORTED_NOT_GATING` point enclosure):

```text
mid = -0.26138846616829221041871114274043742656907102449253760010421583788242222980504852
rad = 0.0089188132260460406541824340820312500000000000000000000000000000000000000000000000
```

`c3_ob(83/200)` (`REPORTED_NOT_GATING` point enclosure):

```text
mid = -0.26988560177557305654806641928752862980420736418025875759055846056856077579293020
rad = 0.0089228836877737194299697875976562500000000000000000000000000000000000000000000000
```

Sphere control:

```text
mid = -0.88887275639247288629952554173125248535472520351320393282524983257736457348811788
rad = 0.015766709693707525730133056640625000000000000000000000000000000000000000000000000
contains -8/9
```

The expectation points are explicitly non-gating. The theorem gate is the 64-box interval cover; the sphere value is a gating evaluator control.

## Logical consequence requested from Judge

Please verify that the audited symbolic representation plus the successful 64-box Arb cover imply

```text
c3_ob(lambda) < 0 on [2/5,83/200].
```

Since certified contract A gives a unique `lambda_c^ob in (2/5,83/200)` with

```text
H_axis_ob(lambda_c^ob)=0,
partial_lambda H_axis_ob(lambda_c^ob)>0,
```

B then gives in particular

```text
c3_ob(lambda_c^ob)<0.
```

By the odd real-analytic local normal form, this fixes the orientation as supercritical for increasing lambda. A quantitative local box for use in global cover C remains a separate obligation.

## Explicit exclusions

This receipt does not certify:

- any numerical refinement of `lambda_c^ob`;
- a quantitative `(epsilon,t0)` pitchfork box;
- the nonzero axial branch outside the local center neighborhood;
- connection to the boundary-entry branch;
- absence of additional axial roots globally;
- off-axis stationary-orbit exclusion;
- any global stationary-point census.

No `CERTIFIED` label is authorized for B until an external `JUDGE_PASS` is recorded.
