# Oblate Spheroid Research

Research on stationary base points of the cone-volume-weighted radial–normal
angle functional on oblate spheroids.

> **Repository status: `NOT_BINDING / DIAGNOSTIC_ONLY`**
>
> This repository currently contains no certified theorem, approved production
> kernel, or Actions-produced clean-room certificate.

## Geometric setting

For

[
K_\lambda
=
\left\{
(x,y,z):
x^2+y^2+\frac{z^2}{\lambda^2}\le 1
\right\},
\qquad 0<\lambda<1,
]

the equatorial semiaxes are (1,1), while the polar semiaxis is (lambda).
Thus the rotation axis is the shortest semiaxis direction.

The functional is

[
E_{K}(p)
=
\int_{\partial K}
\alpha_{K,p}(x)^2,d\mu_{K,p}(x),
]

where

[
\alpha_{K,p}(x)
=
\arccos
\frac{(x-p)\cdot\nu_K(x)}{|x-p|},
\qquad
d\mu_{K,p}(x)
=
\frac{(x-p)\cdot\nu_K(x)}
{3\operatorname{Vol}(K)},dA.
]

The principal problem is to determine whether two stationary base points enter
transversely from the poles, move along the shortest axis, and are eventually
absorbed into the center.

## Axial reduction

Write an axial base point as

[
p=(0,0,\lambda t),
\qquad -1<t<1,
]

and put (mu=cos\theta). Define

[
q=1-\mu^2+\lambda^2(\mu-t)^2,
\qquad
w^2=\lambda^2(1-\mu^2)+\mu^2,
]

[
\gamma
=
\frac{\lambda(1-t\mu)}
{w\sqrt q},
\qquad
h(c)=\arccos(c)^2.
]

Then

[
E_\lambda(t)
=
\frac12
\int_{-1}^{1}
(1-t\mu)h(\gamma),d\mu.
]

The canonical axial stationary kernel is

[
g_{\mathrm{axis,ob}}(t,\lambda)
=
\partial_tE_\lambda(t),
]

and its pole endpoint value is

[
b_{\mathrm{ob}}(\lambda)
=
g_{\mathrm{axis,ob}}(1,\lambda).
]

With (mu=1-s^2), the transformed endpoint density is regular. This gives the
analytic route for evaluating (b_{\mathrm{ob}}),
(b_{\mathrm{ob}}'), and
(partial_tg_{\mathrm{axis,ob}}(1,\lambda)) without extrapolating
(t\uparrow1).

## Boundary-entry problem

The proposed boundary-entry parameter is defined by the one-variable equation

[
b_{\mathrm{ob}}
(\lambda_{\mathrm{entry,ob}})=0.
]

The desired transverse-entry conditions are

[
b_{\mathrm{ob}}'
(\lambda_{\mathrm{entry,ob}})>0,
\qquad
\partial_tg_{\mathrm{axis,ob}}
(1,\lambda_{\mathrm{entry,ob}})<0.
]

If certified, these inequalities imply that the entering stationary points are
axial maxima of the restricted profile, have Morse index (1) in the full
three-dimensional problem once transverse positivity is established, and move
into the interior with

[
1-t(\lambda)
=
C_{\mathrm{ob}}
(\lambda_{\mathrm{entry,ob}}-\lambda)
+
O\!\left(
(\lambda_{\mathrm{entry,ob}}-\lambda)^2
\right),
]

where

[
C_{\mathrm{ob}}
=
\frac{
b_{\mathrm{ob}}'
(\lambda_{\mathrm{entry,ob}})
}{
-\partial_tg_{\mathrm{axis,ob}}
(1,\lambda_{\mathrm{entry,ob}})
}.
]

## Exact sphere controls

At (lambda=1), the axial derivative geometry satisfies

[
-\mu q-(1-t\mu)(t-\mu)
=
-t(1-\mu^2).
]

The exact positive control is

[
\boxed{
b_{\mathrm{ob}}(1)
=
\frac{\pi^2}{32}
=
0.3084251375340424\ldots
}
]

and the boundary energy is

[
E_1(1)
=
\frac{3\pi^2}{32}-\frac12.
]

These expectations were fixed before implementation and must never be
regenerated from the production evaluator.

## Diagnostic predictions — not certified

Current exploratory calculations suggest

[
\lambda_{\mathrm{entry,ob}}
\approx 0.64430,
\qquad
\lambda_{\mathrm{axis,ob}}
\approx 0.4079,
\qquad
C_{\mathrm{ob}}
\approx 0.6965.
]

Expected boundary signs are

[
b_{\mathrm{ob}}(0.60)<0,
\qquad
b_{\mathrm{ob}}(0.70)>0,
\qquad
b_{\mathrm{ob}}(1)=\frac{\pi^2}{32}>0.
]

These values are diagnostic targets only. Agreement does not constitute
certification, and numerical searches that detect no additional stationary
points are not nonexistence proofs.

## Certification roadmap

1. Implement the endpoint-regular axial evaluator.
2. Reproduce the exact sphere controls independently.
3. Certify existence, uniqueness, and transversality of
   (lambda_{\mathrm{entry,ob}}).
4. Certify the center-axis degeneracy
   (lambda_{\mathrm{axis,ob}}) and its nondegenerate pitchfork
   coefficients.
5. Exclude interior folds and additional stationary points in the meridian
   domain.
6. Treat the singular limit (lambda\to0) as a separate analytic tail
   obligation.

A result may be labelled `CERTIFIED` only after its formulas, interval
implementation, configuration, workflow run, machine-readable certificate,
and independent audit have all been fixed and reviewed.

## Repository documents

- [Research status](STATUS.md)
- [Naming conventions](NAMING_CONVENTIONS.md)
- [Exact controls](controls/README.md)
- [Diagnostic-artifact rules](diagnostics/README.md)
