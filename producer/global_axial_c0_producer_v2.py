#!/usr/bin/env python3
"""C0 producer wrapper: stabilized C0b and redeclared quantitative box.

The raw-audited C0 kernel in global_axial_c0_producer.py is left unchanged.
This wrapper makes only the declared C0 box/edge change

    t in [0, 1/2],  tau=t^2 in [0, 1/4],  T_EDGE=1/2,

while preserving the predeclared A0--A2 and B0--B2 stage schedules.
For C0b it also keeps the exact stable identity

    alpha^2 = u * R^2,

where R = asin(sqrt(u))/sqrt(u) is evaluated by the audited two-chart
continuation.

Evidence class: PROTOTYPE / NOT_BINDING.
"""
from fractions import Fraction
from producer import global_axial_c0_producer as base

# Fixed redeclaration for the quantitative C0 box.
base.T_HI = Fraction(1, 2)
base.T_EDGE = Fraction(1, 2)


def _g_density_stable(s, t, lam, stats):
    mu, A, gamma, u, gt, _, _, _ = base._geometry(s, t, lam)
    R, _, _, _ = base._R_bundle(u, gamma, stats)
    alpha2 = u * R * R
    return s * (-mu * alpha2 - 2 * A * R * gt)


base._g_density = _g_density_stable

if __name__ == "__main__":
    base.run()
