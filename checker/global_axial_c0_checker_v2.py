#!/usr/bin/env python3
"""C0 V2 checker: separately transcribed four-group C0a and stable C0b.

CHECKER_KERNEL=SEPARATE_FOUR_GROUP_TRANSCRIPTION
INDEPENDENCE_SCOPE=TRANSCRIPTION/PRECISION/PARTITION/GATING
Evidence class: PROTOTYPE / NOT_BINDING.
"""
from fractions import Fraction
from checker import global_axial_c0_checker as base
from checker import c0a_four_group_v2 as grouped

base.T_HI = Fraction(1, 2)
base.T_EDGE = Fraction(1, 2)


def _g_density_stable(s, t, L, stats):
    mu, A, gam, u, g1, _, _, _ = base._geom(s, t, L)
    R, _, _, _ = base._R(u, gam, stats)
    a2 = u * R * R
    return s * (-mu * a2 - 2 * A * R * g1)


base._g3_density = grouped.density
base._g_density = _g_density_stable

if __name__ == "__main__":
    print("C0A_KERNEL FOUR_GROUP_COMMON_DENOMINATOR / SEPARATE_CHECKER_TRANSCRIPTION")
    print("C0A_WIDTH_DIAGNOSTIC four_group_width_max = K0..K3 density radii by chart")
    base.verify()
