# Center pitchfork coefficient B — external Judge request

Status: `EXTERNAL_JUDGE_PENDING / NOT_BINDING`

## Requested scoped judgment

Please independently review contract B for the single theorem-level claim

```text
c3_ob(lambda) := (1/6) partial_t^3 g_axis_ob(0,lambda) < 0
for every lambda in [2/5,83/200].
```

Together with already certified contract A, approval of this claim supplies the cubic sign/nondegeneracy at the unique center critical parameter `lambda_c^ob` and fixes the local pitchfork orientation as supercritical for increasing `lambda`.

## Pinned materials

Machine receipt:

```text
analysis/CENTER_PITCHFORK_MACHINE_RECEIPT.md
commit 0af9d6e11117c9183951eaf60506682b1de6f608
```

Symbolic/raw-audit note:

```text
analysis/CENTER_PITCHFORK_SYMBOLIC_NOTE.md
commit 943aebe575785e8433e3ea39ea0c6e23e9f7f512
blob efabc9d6c07d2176a62d1d985cba7f8ea01cc629
status CHAT_RAW_AUDIT_PASS / SYMBOLIC_DERIVATION_AUDITED
```

Contract:

```text
analysis/CENTER_PITCHFORK_CONTRACT.md
blob 0c98759fd4c1026e70d4ec49f6487223e026e6cf
```

Producer:

```text
producer/center_pitchfork_producer.py
blob 468ab9a3dd318998eb22b8bfbc09c3848cfb45d4
160-bit Arb
4096 s panels
64 exact lambda boxes
```

Checker:

```text
checker/center_pitchfork_checker.py
blob 46d05b1aaef31a2e24beceed43d29113af351842
192-bit Arb
4096 s panels
64 exact lambda boxes
```

Successful focused Actions evidence:

```text
run 33438258204
job center-pitchfork-evidence
job id 99639876658
head cbaa72fa2e55f5b5e0a698a763a680be35e1a7ae
conclusion SUCCESS
```

The same producer/checker also passed in initial run `33437813853`, job `99638430514`.

## Human/raw audit status

The user independently checked and approved all symbolic items, including:

- odd parity of `g_axis_ob`;
- derivative chain coefficients `4,6,8`;
- `C_tt` coefficients `1,3,1`;
- `C_ttt` coefficients `1,6,3,4,1`;
- all four `gamma` t-derivatives against an independent symbolic derivation;
- both gamma/u charts for `R_gammagammagamma`;
- the `Psi'''` tail with exact denominator `89/245`;
- fixed removable `u=0` loci and absence of moving singularities at `t=0`;
- exact sphere control `c3_ob(1)=-8/9`;
- gating logic.

Raw audit result:

```text
CHAT_RAW_AUDIT_PASS
```

## Checker independence scope

Judge must interpret the checker relationship exactly as

```text
CHECKER_KERNEL=TRANSCRIBED_COPY_NOT_INDEPENDENT_DERIVATION
INDEPENDENCE_SCOPE=PRECISION/PARTITION/GATING
```

The checker is not an independent derivation of the B kernel. Mathematical derivational independence comes from the separate symbolic/raw audit. The checker contributes higher precision, independently reconstructed partition glue, and independent execution of the interval gates.

## Machine facts to verify

Both producer and checker cover `[2/5,83/200]` by 64 exact lambda boxes and return strictly negative upper endpoints in every box.

Both identify the weakest box as

```text
[2/5,5123/12800]
```

with exact report-only enclosures pinned in the machine receipt. In particular, both weakest-box intervals remain strictly negative.

Both also pass the exact sphere containment control

```text
c3_ob(1) = -8/9.
```

The three point expectations near `2/5`, `lambda_c^ob`, and `83/200` are `REPORTED_NOT_GATING` only.

## Requested checks

Please check only:

1. the factorized symbolic identity
   `c3_ob=(1/6) integral partial_t^2 G_t|_{t=0}` and the `C_tt/C_ttt` assembly;
2. the four specialized `gamma` derivatives and the gamma/u charts for `R_gammagammagamma`;
3. the positive-coefficient `Psi'''` tail bound and removable continuation;
4. that the 64 exact boxes cover all of `[2/5,83/200]` and that the recorded Arb upper endpoints imply `c3_ob<0` throughout;
5. that the sphere containment control is consistent with the exact value `-8/9`;
6. that the checker independence declaration is accurate;
7. that, when combined with certified contract A, `H_lambda(lambda_c^ob)>0` and `c3_ob(lambda_c^ob)<0` give the supercritical local orientation for increasing lambda.

## Explicit exclusions

Do not judge or certify from this request:

- a quantitative `epsilon,t0` pitchfork neighborhood;
- any root-count statement outside the local center theorem;
- the entire nonzero axial branch;
- connection to the boundary-entry branch;
- off-axis exclusion;
- the global stationary-point census;
- any refinement of `lambda_c^ob` beyond the certified interval from A.

## Requested outcome vocabulary

If approved, please return an explicit

```text
JUDGE_PASS
```

for the scoped B claim. Until that approval is recorded, B remains `NOT_BINDING` and must not be labeled `CERTIFIED`.
