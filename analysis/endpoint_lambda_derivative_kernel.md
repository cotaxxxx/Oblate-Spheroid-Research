# Lambda derivative of the endpoint-regular oblate kernel

## Status

- Evidence class: `DIAGNOSTIC_ONLY / NOT_BINDING`.
- Derivation class: `PROTOTYPE / NOT_AUDITED`.
- This note derives the candidate kernel for (B'_{\rm ob}). It is not an
  interval enclosure or an audited analytic proof.

Use
[
 e=s^2,qquad a=1-\lambda^2,qquad
 H=1-ae,
]
[
 W=w^2=1-2ae+ae^2=1+ae(e-2),qquad
 Q=\widehat q=2-ae,
]
and
[
 \gamma=\frac{\lambda s}{\sqrt W\sqrt Q},qquad
 u=1-\gamma^2=\frac{(2-e)H^2}{WQ}.
]
On the fixed broad bracket (5/8\leq\lambda\leq33/50), both (W) and
(Q) have the positive uniform lower bounds recorded in the endpoint lemma.

Define
[
 \Phi(u)=(\arcsin\sqrt u)^2,qquad
 \Psi(u)=\frac{\arcsin\sqrt u}{\sqrt u},
]
by their analytic series at (u=0), and write
[
 P(s,\lambda)
 =\frac{2\lambda e(2-e)H}{\sqrt W,Q^{3/2}}.
]
Then
[
 F_{\rm ob}(s,\lambda)
 =-s(1-e)\Phi(u)+P\Psi(u).
]

## Derivatives without singular quotients

The elementary derivatives are
[
 W_\lambda=2\lambda e(2-e),qquad
 Q_\lambda=2\lambda e,qquad
 H_\lambda=2\lambda e.
]
Set
[
 R:=\frac1\lambda
 -\frac{\lambda e(2-e)}{W}
 -\frac{\lambda e}{Q}.
]
Direct logarithmic differentiation of the strictly positive (gamma) gives
[
 \gamma_\lambda=\gamma R,qquad
 u_\lambda=-2\gamma^2R=-2(1-u)R.
]
The identity
[
 \Phi'(u)=\frac{\Psi(u)}{\gamma}
]
is never evaluated as a quotient. Multiplication by (u_\lambda) is
performed symbolically first:
[
 \Phi'(u)u_\lambda=-2\gamma R\Psi(u).
]
Thus neither (1/\gamma) nor a removable (0/0) enters the evaluator.

For (P_\lambda), logarithmic differentiation of (H) is forbidden because
(H=0) at the internal angle-zero point. Differentiate the product instead:
[
 P_\lambda
 =\frac{2e(2-e)}{\sqrt W,Q^{3/2}},J,
]
where
[
 J=
 H+2\lambda^2e
 -\frac{\lambda^2He(2-e)}{W}
 -\frac{3\lambda^2He}{Q}.
]
This expression contains no division by (H).

Finally,
[
 \boxed{
 \partial_\lambda F_{\rm ob}
 =
 2s(1-e)\gamma R\Psi(u)
 +P_\lambda\Psi(u)
 -2P\gamma^2R\Psi'(u)
 }.
]
This is the form imposed on the future producer.

## The new analytic series

No quotient formula for (Psi') is permitted. Use
[
 \Psi(u)=\sum_{n=0}^{\infty}c_nu^n,qquad
 c_n=\frac{\binom{2n}{n}}{4^n(2n+1)},
]
and therefore
[
 \Psi'(u)=\sum_{n=1}^{\infty}n c_nu^{n-1}.
]
All coefficients are positive and
[
 \Psi'(0)=c_1=\frac16.
]
The interval implementation must evaluate a truncated positive series with an
explicit rigorous tail bound. It must never form (1/u), (1/\sqrt u), or
a difference quotient at (u=0).

## Internal double zero: termwise orders

For the oblate bracket,
[
 e_0=\frac1a\in(1,2),qquad H(e_0,\lambda)=0,qquad
 u(e_0,\lambda)=0.
]
This is not a moving integration boundary, so differentiating the integral
produces no term involving (partial_\lambda s_0).

At fixed (s), near (e=e_0):

- (u=O(H^2));
- from the exact formula for (u_\lambda), (R=O(H));
- hence (gamma_\lambda=\gamma R=O(H));
- (P=O(H));
- (P_\lambda=O(1)), with
  [
  P_\lambda(e_0,\lambda)
  =\frac{4\lambda^2e_0^2(2-e_0)}
         {\sqrt{W(e_0)}Q(e_0)^{3/2}};
  ]
- (Psi(u)=1+O(H^2)) and
  (Psi'(u)=1/6+O(H^2)).

Consequently the three boxed terms have respective orders
[
 O(H),qquad O(1),qquad O(H^2).
]
They are individually finite. No cancellation between separately unbounded
terms is needed at (s_0).

The assertion (R=O(H)) also has an exact point control:
[
 R(e_0,\lambda)=0.
]

## Endpoint orders

At (s=0), (e=s^2), and
[
 \gamma R=O(s),qquad P_\lambda=O(s^2),qquad
 P\gamma^2R=O(s^4).
]
The three derivative-kernel terms are therefore
[
 O(s^2),qquad O(s^2),qquad O(s^4).
]

At (s=\sqrt2), put (d=2-e). Because
(H(2,\lambda)=2\lambda^2-1\neq0) on the broad bracket,
[
 R=O(d),qquad P=O(d),qquad P_\lambda=O(d).
]
The three terms are
[
 O(d),qquad O(d),qquad O(d^2).
]
Thus the differentiated kernel extends termwise and finitely at both
integration endpoints and at the internal double zero.

## Trust boundary and controls

Exact controls must precede implementation and check:

1. the formulas for (W_\lambda,Q_\lambda,H_\lambda);
2. (gamma_\lambda=\gamma R) through the squared identity
   [
   (\gamma^2)_\lambda=2\gamma^2R;
   ]
3. (u_\lambda=-2\gamma^2R), independently differentiated from the
   rational expression for (u);
4. the product-rule formula for (P_\lambda), without division by (H);
5. (R(e_0,\lambda)=0);
6. (Psi'(0)=1/6).

These controls verify algebraic transformations. They do not verify the
geometric derivation of (F_{\rm ob}), the analytic two-chart lemma,
differentiation under the integral, or any interval enclosure.
