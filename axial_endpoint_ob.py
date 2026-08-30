#!/usr/bin/env python3
"""PROTOTYPE endpoint-regular evaluator for the oblate axial boundary kernel.

NOT_AUDITED / NOT_BINDING. Evaluates b_ob(lambda)=g_axis_ob(1,lambda)
without extrapolating t -> 1, using mu=1-s^2.
"""

from __future__ import annotations

import mpmath as mp

EVIDENCE_CLASS = "PROTOTYPE"


def _b_ob_integrand_s(s: mp.mpf, lam: mp.mpf) -> mp.mpf:
    """Return the transformed endpoint density, including its Jacobian."""
    if s == 0:
        return mp.mpf("0")

    u = s * s
    mu = 1 - u
    lam2 = lam * lam
    d = 2 + (lam2 - 1) * u
    w = mp.sqrt(lam2 * (1 - mu * mu) + mu * mu)
    denom = w * mp.sqrt(d)

    # At t=1,
    #   cos(alpha) = lam*s/denom,
    #   sin(alpha) = sqrt(2-u)*abs(1+(lam^2-1)u)/denom.
    # The latter follows from
    #   w^2*d - lam^2*u = (2-u)*(1+(lam^2-1)u)^2.
    # Using atan2 avoids loss of domain at points where cos(alpha) -> 1.
    cos_num = lam * s
    sin_num = mp.sqrt(max(mp.mpf("0"), 2 - u)) * abs(1 + (lam2 - 1) * u)
    angle = mp.atan2(sin_num, cos_num)
    h = angle * angle

    if sin_num == 0:
        # lim_{alpha->0} -2*alpha/sin(alpha) = -2.
        h_prime = mp.mpf("-2")
    else:
        sin_angle = sin_num / denom
        h_prime = -2 * angle / sin_angle

    gamma_t = -lam * (mu * d + lam2 * u) / (w * s * d ** mp.mpf("1.5"))
    derivative_density = -mu * h + u * h_prime * gamma_t
    return s * derivative_density


def b_ob(lam, *, dps: int = 50) -> mp.mpf:
    """Directly evaluate b_ob(lambda) for 0 < lambda <= 1."""
    with mp.workdps(dps):
        lam = mp.mpf(lam)
        if not (0 < lam <= 1):
            raise ValueError("b_ob requires 0 < lambda <= 1")
        root2 = mp.sqrt(2)
        return +mp.quad(lambda s: _b_ob_integrand_s(s, lam), [0, 1, root2])


if __name__ == "__main__":
    with mp.workdps(50):
        for lam in (mp.mpf("0.60"), mp.mpf("0.70"), mp.mpf("1")):
            print(lam, mp.nstr(b_ob(lam, dps=50), 40))
