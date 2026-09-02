#!/usr/bin/env python3
"""C1c lower-half post-crossing exclusion producer.

Evidence class: PROTOTYPE / NOT_BINDING until pinned machine receipt.
"""
from fractions import Fraction
from flint import arb, ctx

from producer import global_axial_c0_producer as base
from producer import c0a_four_group_v2 as grouped

BITS = 160
T_LO, T_HI = Fraction(0), Fraction(1, 2)
L_LO, L_HI = Fraction(9, 20), Fraction(5, 8)
A_STAGES = (("A0", 8, 8, 512), ("A1", 16, 16, 1024), ("A2", 32, 32, 2048))
C1C_PANEL_CEILING = 2392064


def _stats():
    return {"series": 0, "direct": 0, "series_hits_moving_u0": 0, "chart_unresolved": 0}


def _integrate(tl, tr, ll, lr, panels, stats):
    grid, root = base._partition(panels)
    t = base._box(base._point(tl), base._point(tr))
    lam = base._box(base._point(ll), base._point(lr))
    total = arb(0)
    for a, b in zip(grid, grid[1:]):
        aa = root if a == base.SQRT2 else base._point(a)
        bb = root if b == base.SQRT2 else base._point(b)
        s = base._box(aa, bb)
        total += grouped.density(s, t, lam, stats) * (bb - aa)
    return total


def _split(a, b, n):
    h = (b - a) / n
    return [(a + i * h, a + (i + 1) * h) for i in range(n)]


def _gate():
    actual = 0
    worst = None
    for label, nt, nl, panels in A_STAGES:
        stats = _stats()
        unresolved = 0
        stage_worst = None
        for tl, tr in _split(T_LO, T_HI, nt):
            for ll, lr in _split(L_LO, L_HI, nl):
                actual += panels
                try:
                    value = _integrate(tl, tr, ll, lr, panels, stats)
                    good = value.upper() < 0
                except (ValueError, ZeroDivisionError):
                    value = None
                    good = False
                if not good:
                    unresolved += 1
                if value is not None and (stage_worst is None or value.upper() > stage_worst[0]):
                    stage_worst = (value.upper(), tl, tr, ll, lr, value)
        worst = stage_worst
        print("C1C_G3_STAGE", label, "t_boxes", nt, "lambda_boxes", nl,
              "s_panels", panels, "unresolved", unresolved, "chart_stats", stats,
              "worst", None if worst is None else worst[1:])
        if actual > C1C_PANEL_CEILING:
            raise SystemExit("C1C_PANEL_CEILING_EXCEEDED")
        if unresolved == 0:
            print("C1C_G3_FIRST_PASS", label)
            return True, label, actual, worst
    return False, None, actual, worst


def run():
    ctx.prec = BITS
    base.ctx.prec = BITS
    print("GLOBAL_AXIAL_C1C_PRODUCER — PROTOTYPE / NOT_BINDING")
    print("C1C_AMENDMENT analysis/GLOBAL_AXIAL_C1C_PRE_RUN_AMENDMENT.md")
    print("CHECKED_SCOPE", "t", (T_LO, T_HI), "lambda", (L_LO, L_HI))
    print("BITS", BITS, "DEG", base.DEG, "USTAR", "3/5")
    print("A_STAGES", A_STAGES)
    print("PREDECLARED_C1C_PANEL_CEILING", C1C_PANEL_CEILING)
    ok, stage, actual, _ = _gate()
    print("C1C_ACTUAL_PANEL_EVALUATIONS", actual)
    print("LOGICAL_FINAL_C1C_MACHINE", "PASS" if ok else "UNRESOLVED",
          "g3_stage", stage, "claim", "g_ttt<0 on exact C1c rectangle")
    print("LOGICAL_FINAL_C1C_ASSEMBLY", "PENDING_C1B_ANCHOR_AND_EXACT_COVER")
    if not ok:
        raise SystemExit("UNRESOLVED")


if __name__ == "__main__":
    run()
