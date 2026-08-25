#!/usr/bin/env python3
"""Non-binding transverse-Hessian diagnostic along the oblate axial branch.

Evidence class: DIAGNOSTIC_ONLY / NOT_BINDING.
Derivation class: HIGH_PRECISION.

For p=(r,0,lambda*t), this script differentiates the normalized surface
integrand twice at r=0, analytically averages cos(phi)^2=1/2, and evaluates the
remaining one-dimensional integral.  It does not provide an interval
enclosure or exclude additional stationary points.
"""

import mpmath as mp

from checker.oblate_axis_prototype import (
    _alpha_over_sin_alpha,
    _transformed_s2,
    g_axis_ob,
)


DPS = 40
LAMBDA_SAMPLES = ("0.42", "0.45", "0.50", "0.55", "0.60", "0.63", "0.6435")


def h_second(gamma, alpha):
    """Stable second gamma derivative of acos(gamma)^2."""
    if alpha == 0:
        return mp.mpf(2) / 3
    if abs(alpha) < mp.root(mp.eps, 4):
        # h'' = 2/3 + O(alpha^2); this branch is used only when the omitted
        # term is below the working-precision target of this diagnostic.
        return mp.mpf(2) / 3
    sine = mp.sin(alpha)
    return 2 * (sine - alpha * gamma) / sine**3


def transverse_hessian_ob(t, lam):
    """Return the candidate transverse eigenvalue E_rr at an axial point."""
    one = mp.mpf(1)
    two = mp.mpf(2)
    zero = mp.mpf(0)
    upper = mp.sqrt(two)

    def density(s):
        s2 = _transformed_s2(s)
        mu = one - s2
        radial = s2 * (two - s2)
        radius = mp.sqrt(max(zero, radial))
        a = one - t * mu
        q = radial + lam * lam * (mu - t) ** 2
        w2 = lam * lam * radial + mu * mu
        w = mp.sqrt(w2)
        prefactor = lam / w

        complement_factor = (one - lam * lam) * mu + lam * lam * t
        one_minus_gamma2 = (
            radial * complement_factor * complement_factor / (w2 * q)
        )
        gamma2 = min(one, max(zero, one - one_minus_gamma2))
        gamma = mp.sqrt(gamma2)
        alpha, ratio = _alpha_over_sin_alpha(gamma)
        hp = -2 * ratio
        hpp = h_second(gamma, alpha)

        # gamma_r = gamma_r_coefficient*cos(phi) at r=0.
        gamma_r_coefficient = (
            prefactor * radius / mp.sqrt(q) * (-one + a / q)
        )

        # Azimuthal average of gamma_rr, using <cos(phi)^2>=1/2.
        gamma_rr_average = prefactor * (
            -radial * q ** mp.mpf("-1.5")
            + a
            * (
                mp.mpf("1.5") * radial * q ** mp.mpf("-2.5")
                - q ** mp.mpf("-1.5")
            )
        )

        # For F=A*h(gamma), A_r=-radius*cos(phi), A_rr=0.
        f_rr_average = (
            -radius * hp * gamma_r_coefficient
            + a
            * (
                mp.mpf("0.5") * hpp * gamma_r_coefficient**2
                + hp * gamma_rr_average
            )
        )

        # E_rr=(1/2)int[-1,1]<F_rr> dmu and dmu=2s ds.
        return s * f_rr_average

    return +mp.quad(density, [zero, upper], method="tanh-sinh")


def positive_axis_root(lam):
    """Bisect the noncentral positive root; diagnostic, not a proof."""
    lo = mp.mpf("1e-6")
    hi = mp.mpf(1)
    flo = g_axis_ob(lo, lam, dps=DPS)
    fhi = g_axis_ob(hi, lam, dps=DPS)
    if not (flo > 0 and fhi < 0):
        raise ArithmeticError(
            f"expected branch bracket absent at lambda={lam}: {flo}, {fhi}"
        )
    for _ in range(70):
        mid = (lo + hi) / 2
        fm = g_axis_ob(mid, lam, dps=DPS)
        if fm > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def main():
    with mp.workdps(DPS):
        print("EVIDENCE_CLASS DIAGNOSTIC_ONLY / NOT_BINDING")
        print("DERIVATION_CLASS HIGH_PRECISION")
        print("DPS", DPS)
        for lam_text in LAMBDA_SAMPLES:
            lam = mp.mpf(lam_text)
            t = positive_axis_root(lam)
            z = lam * t
            q_perp = transverse_hessian_ob(t, lam)
            print(
                "BRANCH",
                lam_text,
                "t",
                mp.nstr(t, 24),
                "z",
                mp.nstr(z, 24),
                "Q_perp_ob",
                mp.nstr(q_perp, 30),
            )


if __name__ == "__main__":
    main()
