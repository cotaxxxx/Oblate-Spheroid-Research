# Endpoint C1 analytic audit receipt — template

Status: `PENDING / NOT_AUDITED / NOT_BINDING`

This receipt is for the human audit of the one-sided endpoint regularity and differentiation-under-the-integral lemma for the oblate axial kernel. It does not certify any numerical enclosure.

## Pinned analytic source

- branch: `analytic-endpoint-limit-78c178f`
- file: `analysis/endpoint_kernel_lemma.md`
- blob SHA: `aa6a1a1710d1a4af560e5ddf0c504870f50c535c`

The audit must be performed against the pinned source above. Any source modification requires a new receipt and new pin.

## Claim under audit

For a compact rational interval `I` containing the certified endpoint-zero bracket `[5/8,33/50]`, the axial derivative

`g_axis_ob(t,lambda) = partial_t E_lambda(t)`

has a one-sided continuous extension to `t=1`, and

`b_ob(lambda) = lim_{t->1-} g_axis_ob(t,lambda)`

is equal to the integral of the endpoint density `F_ob(s,lambda)` obtained after `mu = 1-s^2`. The same analytic setup also justifies differentiation of `B_ob(lambda)` under the integral sign on `I`.

## Human audit checklist

1. **Fixed compact domains** — verify the angular domain is fixed and independent of `t` and `lambda`, and that `I` is compactly contained in the stated admissible lambda range.
2. **Denominator positivity** — verify all lower bounds used for `w`, `q`, and `qhat`; in particular no denominator vanishes on the closed parameter sets used in the proof.
3. **Apparent singularity at gamma=1** — verify the exact complement identity and that `h(c)=acos(c)^2` / the equivalent `Phi`,`Psi` representation extends analytically through the apparent `0/0` angle-ratio point.
4. **Exact pre-limit factorization** — verify `A`, `q`, `N=-s^2 H`, the bound on `H`, and the cancellation structure used near `s=0`.
5. **Uniform majorant on s in [0,1]** — verify the displayed `t`- and `lambda`-independent integrable majorant for the transformed derivative density.
6. **Compact majorant on s in [1,sqrt(2)]** — verify the lower bound away from the north-pole singular layer and continuity on the compact set.
7. **Dominated convergence** — verify pointwise convergence for every `s>0`, integrable domination, and the conclusion that the one-sided limit commutes with the integral.
8. **Endpoint density formula** — verify the exact `t=1` factorization and the final formula for `F_ob` including Jacobian and cone-weight factors.
9. **Two-chart analyticity** — verify the lower `gamma` chart, upper `u` chart, internal double zero, seam values at `s=1`, and analytic gluing.
10. **Lambda differentiation** — verify the open-neighborhood argument `I compactly contained in J`, boundedness of `F_ob` and `partial_lambda F_ob`, and differentiation under the integral sign including the endpoints of `I`.
11. **Scope** — confirm that this lemma does not by itself identify the certified endpoint zero with the census branch and does not certify `partial_t F_ob(1,lambda)`.

## Required external judge record

The judge signature/result must be stored outside this source file and must contain at minimum:

- analytic source branch and blob SHA;
- audit date;
- auditor identity or external judge identifier;
- checklist result for items 1–11;
- final verdict: `PASS` or `FAIL`;
- any exceptions or unresolved obligations.

No `PASS` text may be inserted here by the implementation actor.
