# C0a four-group symbolic regrouping note

Status: SYMBOLIC NOTE / PRE-AUDIT / NOT GATING / NOT BINDING

Source kernel pinned for derivation: `5716bccfe66ac92ef73b84100ba1c3f37a406964`.

This note does not alter `USTAR`, the A0--A2/B0--B2 stage schedule, the two-chart continuation, or any producer/checker gate. It only rewrites the existing C0a density algebraically so cancellation occurs before interval evaluation.

The current density is

\[
\frac{g_{ttt}}{s}=8\mu C_{tt}-2A C_{ttt},
\]

with

\[
C_{tt}=R_{\gamma\gamma}\gamma_t^3+3R_\gamma\gamma_t\gamma_{tt}+R\gamma_{ttt},
\]

\[
C_{ttt}=R_{\gamma\gamma\gamma}\gamma_t^4+6R_{\gamma\gamma}\gamma_t^2\gamma_{tt}+3R_\gamma\gamma_{tt}^2+4R_\gamma\gamma_t\gamma_{ttt}+R\gamma_{tttt}.
\]

Collecting by the common factors `R`, `R_gamma`, `R_gammagamma`, `R_gammagammagamma` gives exactly

\[
\frac{g_{ttt}}{s}=R K_0+R_\gamma K_1+R_{\gamma\gamma}K_2+R_{\gamma\gamma\gamma}K_3,
\]

where

\[
K_0=8\mu\gamma_{ttt}-2A\gamma_{tttt},
\]

\[
K_1=24\mu\gamma_t\gamma_{tt}-2A\left(3\gamma_{tt}^2+4\gamma_t\gamma_{ttt}\right),
\]

\[
K_2=8\mu\gamma_t^3-12A\gamma_t^2\gamma_{tt},
\]

\[
K_3=-2A\gamma_t^4.
\]

Use the existing kernel abbreviations

\[
\gamma_t=\frac{\lambda N}{wq^{3/2}},\qquad
\gamma_{tt}=\frac{\lambda M}{wq^{5/2}},\qquad
\gamma_{ttt}=\frac{\lambda P}{wq^{7/2}},
\]

\[
\gamma_{tttt}=\frac{\lambda Q}{wq^{9/2}},\qquad
Q=P_1q-7P\lambda^2d.
\]

Then each group coefficient is evaluated as one common-denominator rational expression:

\[
K_0=\frac{\lambda\left(8\mu Pq-2AQ\right)}{wq^{9/2}},
\]

\[
K_1=\frac{\lambda^2\left(24\mu NMq-6AM^2-8ANP\right)}{w^2q^5},
\]

\[
K_2=\frac{\lambda^3\left(8\mu N^3q-12AN^2M\right)}{w^3q^{11/2}},
\]

\[
K_3=-\frac{2A\lambda^4N^4}{w^4q^6}.
\]

The proposed grouped density is therefore

\[
 g_{ttt}=s\left(RK_0+R_\gamma K_1+R_{\gamma\gamma}K_2+R_{\gamma\gamma\gamma}K_3\right).
\]

No chart formula changes are implied. `R`, `R_gamma`, `R_gammagamma`, `R_gammagammagamma` are still supplied by the existing audited two-chart continuation with `USTAR=3/5`.

## Audit obligations before implementation

1. Expand `R K0 + R_gamma K1 + R_gammagamma K2 + R_gammagammagamma K3` back to the existing eight-term density and verify exact coefficient identity.
2. Independently verify the substitutions for `gamma_t`, `gamma_tt`, `gamma_ttt`, `gamma_tttt` and the powers of `w` and `q` in `K0`--`K3`.
3. Check the grouped and legacy formulas on exact rational point inputs at both ordinary and near-threshold `u` values using the same `R` bundle only as a numerical transcription check; this is supplementary, not the symbolic proof.
4. Only after the symbolic audit passes may producer/checker implementations be changed, in separate transcriptions.

The expected benefit is cancellation inside `K0` in particular, before interval multiplication by `R`, rather than summing wide enclosures of `8 mu R gamma_ttt` and `-2 A R gamma_tttt` separately.
