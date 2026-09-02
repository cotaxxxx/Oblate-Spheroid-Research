#!/usr/bin/env python3
"""Non-binding C1b left-edge tube-width diagnostic.

This script is deliberately diagnostic only.  It does not participate in any
C1 gate, contract, first-pass schedule, or theorem evidence.

At a fixed rational candidate near lambda_J = 9/20, compare three nominal
tube half-widths.  The left wall is clamped at t=1/2.  For each width report
an Arb enclosure for g_t over the whole representative tube box and Arb
enclosures for g on the left and right walls.

Status: DIAGNOSTIC_ONLY / NOT_GATING / NOT_BINDING.
"""
from fractions import Fraction

from flint import arb, ctx

from producer import global_axial_c0_producer as base
from producer.global_axial_c0_producer_v2 import _g_density_stable

BITS = 192
PANELS = 2048

LAMBDA_J = Fraction(9, 20)
# Narrow representative slab around lambda_J; diagnostic geometry only.
LAMBDA_LO = Fraction(719, 1600)
LAMBDA_HI = Fraction(721, 1600)
# Rational stand-in for the census candidate t_c ~= 0.56.  This is not pinned
# as theorem data and may be replaced by the future predictor policy.
T_C = Fraction(9, 16)
WIDTHS = (Fraction(1, 32), Fraction(3, 64), Fraction(1, 16))
T_DOMAIN_LO = Fraction(1, 2)


def _gt_density(s, t, lam, stats):
    mu, A, gamma, u, gamma_t, gamma_tt, _, _ = base._geometry(s, t, lam)
    R, Rg, _, _ = base._R_bundle(u, gamma, stats)
    return s * (4 * mu * R * gamma_t - 2 * A * (Rg * gamma_t * gamma_t + R * gamma_tt))


def _integrate(tl, tr, ll, lr, mode):
    stats = {"series": 0, "direct": 0, "series_hits_moving_u0": 0, "chart_unresolved": 0}
    grid, root = base._partition(PANELS)
    t = base._box(base._point(tl), base._point(tr))
    lam = base._box(base._point(ll), base._point(lr))
    z = arb(0)
    for a, b in zip(grid, grid[1:]):
        aa = root if a == base.SQRT2 else base._point(a)
        bb = root if b == base.SQRT2 else base._point(b)
        s = base._box(aa, bb)
        if mode == "gt":
            y = _gt_density(s, t, lam, stats)
        elif mode == "g":
            y = _g_density_stable(s, t, lam, stats)
        else:
            raise ValueError(mode)
        z += y * (bb - aa)
    return z, stats


def main():
    ctx.prec = BITS
    base.ctx.prec = BITS
    print("C1B_TUBE_WIDTH_DIAGNOSTIC — DIAGNOSTIC_ONLY / NOT_GATING / NOT_BINDING")
    print("BITS", BITS, "PANELS", PANELS)
    print("LAMBDA_J", LAMBDA_J, "LAMBDA_SLAB", (LAMBDA_LO, LAMBDA_HI))
    print("T_C_DIAGNOSTIC", T_C, "LEFT_CLAMP", T_DOMAIN_LO)
    print("WIDTHS", WIDTHS)

    for w in WIDTHS:
        t_minus = max(T_DOMAIN_LO, T_C - w)
        t_plus = T_C + w
        gt_box, gt_stats = _integrate(t_minus, t_plus, LAMBDA_LO, LAMBDA_HI, "gt")
        g_left, left_stats = _integrate(t_minus, t_minus, LAMBDA_LO, LAMBDA_HI, "g")
        g_right, right_stats = _integrate(t_plus, t_plus, LAMBDA_LO, LAMBDA_HI, "g")
        print(
            "WIDTH_RESULT",
            "w", w,
            "tube", (t_minus, t_plus),
            "gt", gt_box,
            "gt_upper", gt_box.upper(),
            "left_g", g_left,
            "right_g", g_right,
        )
        print("WIDTH_CHART_STATS", "w", w, "gt", gt_stats, "left_g", left_stats, "right_g", right_stats)

    print("DIAGNOSTIC_COMPLETE / NOT_GATING / NOT_BINDING")


if __name__ == "__main__":
    main()
