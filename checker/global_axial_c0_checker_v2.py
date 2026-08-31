#!/usr/bin/env python3
"""C0 checker wrapper: stabilize only C0b alpha^2 evaluation.

CHECKER_KERNEL=TRANSCRIBED_COPY_NOT_INDEPENDENT_DERIVATION
INDEPENDENCE_SCOPE=PRECISION/PARTITION/GATING
Evidence class: PROTOTYPE / NOT_BINDING.
"""
from checker import global_axial_c0_checker as base


def _g_density_stable(s, t, L, stats):
    mu, A, gam, u, g1, _, _, _ = base._geom(s, t, L)
    R, _, _, _ = base._R(u, gam, stats)
    a2 = u * R * R
    return s * (-mu * a2 - 2 * A * R * g1)


base._g_density = _g_density_stable

if __name__ == "__main__":
    base.verify()
