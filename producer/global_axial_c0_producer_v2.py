#!/usr/bin/env python3
"""C0 V2 producer: four-group C0a and stabilized C0b.

The legacy base kernel remains unchanged as the raw-audit reference.  V2 uses
the separately implemented common-denominator four-group C0a evaluator while
keeping the declared box t in [0,1/2], tau<=1/4 and T_EDGE=1/2.

Evidence class: PROTOTYPE / NOT_BINDING.
"""
from fractions import Fraction
from producer import global_axial_c0_producer as base
from producer import c0a_four_group_v2 as grouped

base.T_HI = Fraction(1, 2)
base.T_EDGE = Fraction(1, 2)


def _g_density_stable(s, t, lam, stats):
    mu, A, gamma, u, gt, _, _, _ = base._geometry(s, t, lam)
    R, _, _, _ = base._R_bundle(u, gamma, stats)
    alpha2 = u * R * R
    return s * (-mu * alpha2 - 2 * A * R * gt)


base._g3_density = grouped.density
base._g_density = _g_density_stable


def run_v2():
    base.ctx.prec = base.BITS
    print("GLOBAL_AXIAL_C0_PRODUCER_V2 — PROTOTYPE / NOT_BINDING")
    print("C0A_KERNEL FOUR_GROUP_COMMON_DENOMINATOR / RAW_AUDITED")
    print("C0A_WIDTH_DIAGNOSTIC four_group_width_max = K0..K3 density radii by chart")
    print("BITS", base.BITS, "DEG", base.DEG, "USTAR", "3/5")
    print("T_HI", base.T_HI, "T_EDGE", base.T_EDGE)
    print("C0A_STAGES", base.C0A_STAGES)
    print("C0B_STAGES", base.C0B_STAGES)
    print("PREDECLARED_MAX_S_PANEL_EVALS", base.MAX_S_PANEL_EVALS)
    print(
        "PT_TEST",
        base._point(Fraction(2, 5)),
        base._point(Fraction(1, 2)),
        base._point(Fraction(1, 512)),
    )
    print(
        "BOX_TEST_01",
        base._box(base._point(Fraction(0)), base._point(Fraction(1))),
    )
    print(
        "BOX_TEST_T",
        base._box(base._point(Fraction(7, 16)), base._point(Fraction(1, 2))),
    )
    print("CTX_PREC", base.ctx.prec)
    aok, astage, _ = base._run_c0a()
    bok, bstage, _ = base._run_c0b()
    ok = aok and bok
    print(
        "LOGICAL_FINAL_C0",
        "PASS" if ok else "UNRESOLVED",
        "C0a_stage", astage,
        "C0b_stage", bstage,
        "claim: g_ttt<0 on box and Phi(t=1/2)<0 on lambda interval",
    )
    if not ok:
        raise SystemExit("UNRESOLVED")


if __name__ == "__main__":
    run_v2()
