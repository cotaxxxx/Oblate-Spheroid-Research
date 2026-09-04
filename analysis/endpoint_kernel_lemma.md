# Endpoint-regular oblate axis kernel

## Status and scope

- Evidence class: `DIAGNOSTIC_ONLY / NOT_BINDING`.
- Derivation class: `PROTOTYPE / NOT_AUDITED`.
- This note records an analytic reduction and the obligations imposed on a
  future interval evaluator. It is not a certificate and does not promote any
  numerical value.

The parameter interval below is a compact rational interval
(I=[\lambda_-,\lambda_+]\Subset(0,1/\sqrt2)) containing the candidate
boundary-entry parameter.

## Geometry and normalization

Parametrize the oblate spheroid by
[
 x=(\sqrt{1-\mu^2}\cos\varphi,
    \sqrt{1-\mu^2}\sin\varphi,\lambda\mu),
 \qquad -1\leq\mu\leq1,
]
and put the axial base point at (p=(0,0,\lambda t)), with (t<1). Define
[
 A=1-t\mu,qquad
 q=1-\mu^2+\lambda^2(\mu-t)^2,qquad
 w^2=\lambda^2(1-\mu^2)+\mu^2.
]
The cosine of the angle between (x-p) and the outward normal is
[
 \gamma=\frac{\lambda A}{w\sqrt q}.
]
After the azimuthal integral, the normalized cone measure is
[
 \frac12(1-t\mu),d\mu.
]
Consequently, with (alpha=\arccos\gamma),
[
 E_\lambda(t)=\frac12\int_{-1}^{1}A\alpha^2,d\mu.
]
Differentiating for (t<1) gives
[
 \partial_tE_\lambda(t)
 =\frac12\int_{-1}^{1}
 \left[-\mu\alpha^2
 -2A\frac{\alpha}{\sin\alpha}\gamma_t\right]d\mu,
]
where
[
 \gamma_t=
 \frac{\lambda\{-\mu q-A\lambda^2(t-\mu)\}}
      {wq^{3/2}}.
]

The boundary functional is defined by the one-sided limit
[
 B_{\rm ob}(\lambda)
 :=\lim_{t\uparrow1}\partial_tE_\lambda(t),
]
not by silently substituting (t=1) into a singular formula. The reduction
below proves the direct endpoint integral that a verifier may evaluate.

## Exact endpoint reduction

Set
[
 \mu=1-s^2,quad 0\leq s\leq\sqrt2,quad
 a=1-\lambda^2,quad
 \widehat q=2-as^2,
]
so that
[
 w^2=1-2as^2+as^4,qquad q|_{t=1}=s^2\widehat q.
]
The derivative numerator factors exactly:
[
 -\mu\widehat q-\lambda^2s^2
 =-(2-s^2)(1-as^2),
]
and hence
[
 (A\gamma_t)|_{t=1}
 =-\frac{\lambda s(2-s^2)(1-as^2)}
          {w\widehat q^{3/2}}.
]

Choose the positive square-root branch
[
 \gamma(s,\lambda)
 =\frac{\lambda s}{w\sqrt{\widehat q}}.
]
The lower bounds
[
 w^2\geq\lambda_-^2,qquad
 \widehat q\geq2\lambda_-^2
]
hold uniformly on ([0,\sqrt2]\times I). Thus this expression is
real analytic, is positive for (s>0), and fixes the endpoint branch
(gamma\to+1), rather than the nonanalytic (gamma\to-1) branch.

The exact complement identity is
[
 w^2\widehat q-\lambda^2s^2
 =(2-s^2)(1-as^2)^2.
]
Therefore
[
 \gamma^2=\frac{\lambda^2s^2}{w^2\widehat q},
 \qquad
 u:=1-\gamma^2
 =\frac{(2-s^2)(1-as^2)^2}{w^2\widehat q}.
]
In particular, (gamma(0,\lambda)=0) and
(gamma(\sqrt2,\lambda)=1).

Define the analytic angle functions
[
 \Phi(u)=(\arcsin\sqrt u)^2,qquad
 \Psi(u)=\frac{\arcsin\sqrt u}{\sqrt u},
]
using their power-series continuations at (u=0). Because the positive branch
gives (alpha=\arcsin\sqrt u\in[0,\pi/2]), no further branch split is
hidden in these definitions.

The endpoint density is
[
 F_{\rm ob}(s,\lambda)
 =-s(1-s^2)\Phi(u)
 +\frac{2\lambda s^2(2-s^2)(1-as^2)}
 {w\widehat q^{3/2}}\Psi(u),
]
and the reduced endpoint functional is
[
 B_{\rm ob}(\lambda)=\int_0^{\sqrt2}F_{\rm ob}(s,\lambda),ds.
]

At (s=0), the two displayed terms are respectively (O(s)) and (O(s^2)).
At (s=\sqrt2), both have a factor (2-s^2). Thus the cone weight,
Jacobian, and angle factors are all included in the endpoint regularization.

## Two-chart analytic lemma

The complement (u) has an internal double zero
[
 s_0^2=\frac1{1-\lambda^2}\in(1,2),qquad
 u(s_0,\lambda)=0,qquad\gamma(s_0,\lambda)=1.
]
Accordingly, a direct (arccos\gamma) implementation cannot be used on one
interval crossing (s_0). The kernel is represented by two overlapping
analytic charts:

1. On (0\leq s\leq1), use the (gamma)-chart. Here
   [
   \gamma^2\leq\frac1{1+\lambda_-^2}<1.
   ]
2. On (1\leq s\leq\sqrt2), use the (u)-chart. The intentionally weak
   uniform bound
   [
   0\leq u\leq1-\frac{\lambda_-^2}{2}<1
   ]
   follows from (w^2\leq1), (widehat q\leq2), and (s^2\geq1).
   A tighter bound may be used for conditioning but is not part of this lemma.

At the fixed seam (s=1),
[
 \gamma^2(1,\lambda)=\frac1{1+\lambda^2},qquad
 u(1,\lambda)=\frac{\lambda^2}{1+\lambda^2},
]
so the charts have an exact rational overlap target for rational (lambda).

These bounds and the analytic power-series extensions of (Phi) and (Psi)
show that the two representations glue to a real-analytic endpoint density on
the closed rectangle, chart by chart. In particular, (F_{\rm ob}) and
(partial_\lambda F_{\rm ob}) are bounded there. Dominated
differentiation yields
[
 B'_{\rm ob}(\lambda)
 =\int_0^{\sqrt2}\partial_\lambda
 F_{\rm ob}(s,\lambda),ds.
]

For interval implementation, every truncated series for (Phi) or (Psi)
must carry a rigorous remainder enclosure. Equality of the two chart
enclosures at the seam is a certificate condition.

## Independent algebra controls

Before an interval evaluator is trusted, exact rational tests must check:

- endpoint values (gamma^2(0,\lambda)=0) and
  (gamma^2(\sqrt2,\lambda)=1);
- the global complement identity and (gamma^2+u=1);
- the internal double zero (s_0^2=1/(1-\lambda^2));
- the seam targets at (s=1);
- the factorization used for (A\gamma_t).

These controls live in `controls/test_endpoint_algebra.py`, use only exact
`Fraction` arithmetic, and do not call the prototype evaluator or an
integrator.

## Later certification target

The first interval certificate is deliberately local:

1. enclose (B_{\rm ob}(\lambda_-)) below zero and
   (B_{\rm ob}(\lambda_+)) above zero with comfortable margins;
2. prove (B'_{\rm ob}>0) throughout that rational bracket;
3. reuse the same derivative enclosure in interval Newton refinement.

This proves exactly one zero in the stated bracket. It does not prove global
uniqueness on ((\lambda_{\rm axis},1)); that obligation belongs to the
later two-dimensional axial coverage.

The fixed parameter space for static bifurcation statements is (P=B^3), with
(p=L_\lambda u) and (L_\lambda=\operatorname{diag}(1,1,\lambda)).
This normalization preserves orbit type, Hessian index, and nullity by
equivariance and congruence. It is only a static identification: it neither
chooses a metric nor asserts conjugacy of gradient flows.
