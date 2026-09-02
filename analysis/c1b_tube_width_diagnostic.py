#!/usr/bin/env python3
"""Non-binding C1b left-edge tube-width diagnostic.

This script is deliberately diagnostic only. It does not participate in any
C1 gate, contract, first-pass schedule, or theorem evidence.

A coarse whole-tube Arb box is known to suffer strong dependency inflation.
This diagnostic therefore subdivides the representative tube in t and lambda,
then reports the worst certified upper bound for g_t and the worst wall-sign
bounds across the small boxes.

Status: DIAGNOSTIC_ONLY / NOT_GATING / NOT_BINDING.
"""
from fractions import Fraction

from flint import arb, ctx

from producer import global_axial_c0_producer as base
from producer.global_axial_c0_producer_v2 import _g_density_stable

BITS = 192
PANELS = 4096
T_BOXES = 8
LAMBDA_BOXES = 4

LAMBDA_J = Fraction(9, 20)
LAMBDA_LO = Fraction(719, 1600)
LAMBDA_HI = Fraction(721, 1600)
T_C = Fraction(9, 16)  # diagnostic stand-in for census predictor ~= 0.56
WIDTHS = (Fraction(1, 32), Fraction(3, 64), Fraction(1, 16))
T_DOMAIN_LO = Fraction(1, 2)


def _split(a, b, n):
    h = (b - a) / n
    return [(a + i * h, a + (i + 1) * h) for i in range(n)]


def _stats():
    return {"series": 0, "direct": 0, "series_hits_moving_u0": 0, "chart_unresolved": 0}


def _merge_stats(dst, src):
    for k in dst:
        dst[k] += src[k]


def _gt_density(s, t, lam, stats):
    mu, A, gamma, u, gamma_t, gamma_tt, _, _ = base._geometry(s, t, lam)
    R, Rg, _, _ = base._R_bundle(u, gamma, stats)
    return s * (4 * mu * R * gamma_t - 2 * A * (Rg * gamma_t * gamma_t + R * gamma_tt))


def _integrate(tl, tr, ll, lr, mode):
    stats = _stats()
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


def _tube_gt_worst(t_minus, t_plus):
    worst = None
    total = _stats()
    for tl, tr in _split(t_minus, t_plus, T_BOXES):
        for ll, lr in _split(LAMBDA_LO, LAMBDA_HI, LAMBDA_BOXES):
            v, st = _integrate(tl, tr, ll, lr, "gt")
            _merge_stats(total, st)
            item = (v.upper(), tl, tr, ll, lr, v)
            if worst is None or item[0] > worst[0]:
                worst = item
    return worst, total


def _wall_extreme(t, want):
    extreme = None
    total = _stats()
    for ll, lr in _split(LAMBDA_LO, LAMBDA_HI, LAMBDA_BOXES):
        v, st = _integrate(t, t, ll, lr, "g")
        _merge_stats(total, st)
        key = v.lower() if want == "min_lower" else v.upper()
        item = (key, ll, lr, v)
        if extreme is None:
            extreme = item
        elif want == "min_lower" and key < extreme[0]:
            extreme = item
        elif want == "max_upper" and key > extreme[0]:
            extreme = item
    return extreme, total


def main():
    ctx.prec = BITS
    base.ctx.prec = BITS
    print("C1B_TUBE_WIDTH_DIAGNOSTIC — DIAGNOSTIC_ONLY / NOT_GATING / NOT_BINDING")
    print("BITS", BITS, "PANELS", PANELS, "T_BOXES", T_BOXES, "LAMBDA_BOXES", LAMBDA_BOXES)
    print("LAMBDA_J", LAMBDA_J, "LAMBDA_SLAB", (LAMBDA_LO, LAMBDA_HI))
    print("T_C_DIAGNOSTIC", T_C, "LEFT_CLAMP", T_DOMAIN_LO)
    print("WIDTHS", WIDTHS)

    for w in WIDTHS:
        t_minus = max(T_DOMAIN_LO, T_C - w)
        t_plus = T_C + w
        gt_worst, gt_stats = _tube_gt_worst(t_minus, t_plus)
        left_worst, left_stats = _wall_extreme(t_minus, "min_lower")
        right_worst, right_stats = _wall_extreme(t_plus, "max_upper")
        print(
            "WIDTH_RESULT",
            "w", w,
            "tube", (t_minus, t_plus),
            "gt_worst", gt_worst[1:],
            "gt_sup_upper", gt_worst[0],
            "left_g_worst", left_worst[1:],
            "left_g_inf_lower", left_worst[0],
            "right_g_worst", right_worst[1:],
            "right_g_sup_upper", right_worst[0],
        )
        print("WIDTH_CHART_STATS", "w", w, "gt", gt_stats, "left_g", left_stats, "right_g", right_stats)

    print("DIAGNOSTIC_COMPLETE / NOT_GATING / NOT_BINDING")


if __name__ == "__main__":
    main()
