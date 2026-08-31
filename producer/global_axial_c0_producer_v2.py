#!/usr/bin/env python3
"""C0 producer wrapper: stabilize only C0b alpha^2 evaluation.

The raw-audited C0a implementation in global_axial_c0_producer.py is left
unchanged.  This wrapper replaces only _g_density using the exact identity

    alpha^2 = u * R^2,

where R = asin(sqrt(u))/sqrt(u) is already evaluated by the audited two-chart
continuation.  This removes Arb indeterminacy from interval asin at u=1.

Evidence class: PROTOTYPE / NOT_BINDING.
"""
from producer import global_axial_c0_producer as base


def _g_density_stable(s, t, lam, stats):
    mu, A, gamma, u, gt, _, _, _ = base._geometry(s, t, lam)
    R, _, _, _ = base._R_bundle(u, gamma, stats)
    alpha2 = u * R * R
    return s * (-mu * alpha2 - 2 * A * R * gt)


base._g_density = _g_density_stable

if __name__ == "__main__":
    base.run()
