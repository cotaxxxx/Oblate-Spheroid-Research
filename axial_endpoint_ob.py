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

    mu = 1 - s * s
    lam2 = lam * lam
    d = 2 + (lam2 - 1) * s * s
    w = mp.sqrt(lam2 * (1 - mu * mu) + mu * mu)

    gamma = lam * s / (w * mp.sqrt(d))
    angle = mp.acos(gamma)
    h = angle * angle
    h_prime = -2 * angle / mp.sqrt(1 - gamma * gamma)

    gamma_t = -lam * (mu * d + lam2 * s * s) / (w * s * d ** mp.mpf("1.5"))
    derivative_density = -mu * h + s * s * h_prime * gamma_t
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
