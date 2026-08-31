#!/usr/bin/env python3
"""C0 checker wrapper: stabilized C0b and redeclared quantitative box.

CHECKER_KERNEL=TRANSCRIBED_COPY_NOT_INDEPENDENT_DERIVATION
INDEPENDENCE_SCOPE=PRECISION/PARTITION/GATING
Evidence class: PROTOTYPE / NOT_BINDING.
"""
from fractions import Fraction
from checker import global_axial_c0_checker as base

# Fixed redeclaration for the quantitative C0 box.
base.T_HI = Fraction(1, 2)
base.T_EDGE = Fraction(1, 2)


def _g_density_stable(s, t, L, stats):
    mu, A, gam, u, g1, _, _, _ = base._geom(s, t, L)
    R, _, _, _ = base._R(u, gam, stats)
    a2 = u * R * R
    return s * (-mu * a2 - 2 * A * R * g1)


base._g_density = _g_density_stable

if __name__ == "__main__":
    base.verify()
