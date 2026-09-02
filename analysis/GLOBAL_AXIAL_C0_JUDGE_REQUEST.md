# Global axial cover C0 — external Judge request

Status: `EXTERNAL_JUDGE_PENDING / NOT_BINDING`

## Requested scoped judgment

Please independently review only the quantitative center-pitchfork C0 claim

```text
C0a: partial_t^3 g_axis_ob(t,lambda) < 0
     on [0,1/2] x [2/5,83/200].

C0b: g_axis_ob(1/2,lambda)/(1/2) < 0
     on lambda in [2/5,83/200].
```

Equivalently, with the contract variable `tau=t^2` and
`Phi(tau,lambda)=g_axis_ob(t,lambda)/t`, C0b is `Phi(1/4,lambda)<0`. The machine output calls this edge quotient `Phi(t=1/2)<0`.

Do not expand the judgment beyond this fixed box.

## Pinned materials

Machine receipt:

```text
analysis/GLOBAL_AXIAL_C0_MACHINE_RECEIPT.md
blob 605c11c6ed8c8dcd720e1dd72c91580fe36b7320
```

C0 contract:

```text
analysis/GLOBAL_AXIAL_COVER_C0_QUANTITATIVE_PITCHFORK_CONTRACT.md
blob 95ee0472526cacc721c2544ff6fab8f983a11cf5
```

Raw audit:

```text
analysis/c0a_four_group_raw_audit.py
blob 26002379307379c9a1cb05a7644fa638e7a0fa9a
result:
  PASS exact_fraction_cases 16
  PASS eight_term_equals_four_group
  PASS K0_K1_K2_K3_common_denominators
  PASS K0_factorized_numerator_exact_fraction_cases 64
  PASS K0_factorized_constant_coefficient 4*e^2*mu^2
```

Authoritative evidence head:

```text
b8a25658a67cec2d750eef7c5b5ce037dfc6cadf
```

Producer pins:

```text
producer/global_axial_c0_producer_v2.py
blob cdbdf51f8656c1fcae97666cc1846461b250a591

producer/global_axial_c0_producer.py
blob c4c8d6b59d3829e1843d149b7857eda5800287aa
precision 160 bits

producer/c0a_four_group_v2.py
blob 2bb556ab4f0c0cfd9ce6afa65d762551dd3791f4
```

Checker pins:

```text
checker/global_axial_c0_checker_v2.py
blob fbec890588d2d390ea67bc90116b80bb37ebf9cc

checker/global_axial_c0_checker.py
blob 85978625e029b01c8ae40fa8234566f10eea251c
precision 192 bits

checker/c0a_four_group_v2.py
blob 18e66b6450cd2a379bbb869a99e4e5ce6999f6e5
```

Successful Actions evidence:

```text
workflow Oblate global axial C0 quantitative pitchfork
run 33576831323
run number 38
job global-axial-c0-evidence
job id 100082541189
head b8a25658a67cec2d750eef7c5b5ce037dfc6cadf
conclusion SUCCESS
```

## Machine facts to verify

The first-passing schedule was predeclared. Producer and checker both give

```text
C0A_FIRST_PASS A1
A1: 16 x 16 (t,lambda) boxes, s_panels 1024, unresolved 0
worst: t=[15/32,1/2], lambda=[2/5,1283/3200], enclosure [+/- 3.38]
chart counts: series 300407, direct 70537,
              moving-u0 3148, chart_unresolved 0

C0B_FIRST_PASS B1
B1: 32 lambda boxes, s_panels 1024, unresolved 0
worst: lambda=[2653/6400,83/200], enclosure [+/- 0.0855]
chart counts: series 28179, direct 18189,
              moving-u0 151, chart_unresolved 0

LOGICAL_FINAL_C0 PASS C0a_stage A1 C0b_stage B1
```

The producer A1 four-group width maxima are

```text
series K0..K3:
17.5357675850391388
32.8023241162300110
4.12094284594058990
1.50809102505445480

direct K0..K3:
10.1810398399829865
10.2112966179847717
5.51455381512641907
4.25285977125167847
```

The 192-bit checker reproduces the same stage decisions, chart counts, worst boxes, and printed worst enclosures. Its low-order K2/K3 width digits differ slightly because of precision, as explicitly recorded in the machine receipt; no gate decision differs.

A0 remains a declared unresolved precursor, not a failure of the schedule:

```text
A0 unresolved 64
A0 series K0 width 33.8903566002845764
A0 series K1 width 119.9144618511199951
worst [+/- 6.54]
```

The factorized K0 has reduced the former diagnostic K0 series width from about `1759.4` to `33.89`; no K1/K2 factorization or A3 stage was needed. K3 no longer produces an infinite width after the positive-q `q^6` endpoint construction.

## Cleanup separation

The evidence head removes only obsolete receipt diagnostics:

```text
PT_TEST / BOX_TEST / BOX_CANDIDATE / HULL_TEST / CTX_PREC
C0A_K3_INF_DIAGNOSTIC
```

The successful receipt run emits none of them. The withdrawn lower-edge 256-box refinement workflow step was already removed in commit `e5b5d4d3736d6c74e623803815a9539e5d1dc714` and is not evidence for C0.

## Checker independence scope

Interpret the checker exactly as

```text
CHECKER_KERNEL=TRANSCRIBED_COPY_NOT_INDEPENDENT_DERIVATION
INDEPENDENCE_SCOPE=PRECISION/PARTITION/GATING
```

The V2 four-group implementation is separately transcribed on the checker side, but Judge should not treat that fact as an independent mathematical derivation. The raw-audit identity and the contract supply the derivational audit layer.

## Requested checks

Please check:

1. that the four-group exact-Fraction audit supports the implemented regrouping, including the factorized K0 constant coefficient `4*e^2*mu^2`;
2. that the positive-q endpoint powers, including `q^6`, are valid on the fixed C0a box;
3. that A1's 16 x 16 exact boxes cover all of `[0,1/2] x [2/5,83/200]` and every integrated upper endpoint is strictly negative;
4. that B1's 32 exact lambda boxes cover `[2/5,83/200]` and every edge-quotient upper endpoint is strictly negative;
5. that first-pass logic makes A1 and B1 authoritative and does not require A2/B2 or any undeclared refinement;
6. that the 192-bit checker reproduction is consistent with the stated independence scope;
7. that C0a implies strict decrease of `Phi` in `tau` by the contract identity, and C0b supplies the negative outer edge;
8. using the already closed A and B results, that these facts give the quantitative center pitchfork within `|t|<=1/2`.

## Consequence requested with A and B

Please verify the contract consequence only inside the C0 box:

```text
lambda < lambda_c^ob:
  no nonzero axial root in 0<|t|<=1/2;

lambda = lambda_c^ob:
  t=0 is the only axial root in |t|<=1/2;

lambda > lambda_c^ob:
  exactly one positive axial root in (0,1/2)
  and exactly one symmetric negative root.
```

## Explicit exclusions

Do not judge or certify from this request:

- `lambda` outside `[2/5,83/200]`;
- the middle region `1/2<t<31/32`;
- connection to the boundary-entry branch;
- off-axis exclusion;
- the global axial or stationary-point census.

## Requested outcome vocabulary

If approved, please return an explicit

```text
JUDGE_PASS
```

for C0 only. Until then C0 remains `NOT_BINDING`.
