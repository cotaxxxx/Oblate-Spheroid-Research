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


def run_v2():
    """Run unchanged audited gates under the V2 redeclaration.

    The wrapper mirrors base.run() only so the machine-facing claim string
    reflects T_EDGE=1/2. Numerical kernels and gate routines remain in base.
    """
    base.ctx.prec = base.BITS
    print("GLOBAL_AXIAL_C0_PRODUCER_V2 — PROTOTYPE / NOT_BINDING")
    print("BITS", base.BITS, "DEG", base.DEG, "USTAR", "3/5")
    print("T_HI", base.T_HI, "T_EDGE", base.T_EDGE)
    print("C0A_STAGES", base.C0A_STAGES)
    print("C0B_STAGES", base.C0B_STAGES)
    print("PREDECLARED_MAX_S_PANEL_EVALS", base.MAX_S_PANEL_EVALS)
    aok, astage, _ = base._run_c0a()
    bok, bstage, _ = base._run_c0b()
    ok = aok and bok
    print(
        "LOGICAL_FINAL_C0",
        "PASS" if ok else "UNRESOLVED",
        "C0a_stage",
        astage,
        "C0b_stage",
        bstage,
        "claim: g_ttt<0 on box and Phi(t=1/2)<0 on lambda interval",
    )
    if not ok:
        raise SystemExit("UNRESOLVED")


if __name__ == "__main__":
    run_v2()
