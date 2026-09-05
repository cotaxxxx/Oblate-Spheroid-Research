#!/usr/bin/env python3
"""Transcribed-copy checker for C1a crossing-bridge gates.

CHECKER_KERNEL=TRANSCRIBED_COPY_NOT_INDEPENDENT_DERIVATION
INDEPENDENCE_SCOPE=PRECISION/PARTITION/GATING
Bisection is report-only under the pinned C1a pre-run amendment.
Evidence class: PROTOTYPE / NOT_BINDING.
"""
from fractions import Fraction
from flint import arb, ctx

from checker import global_axial_c0_checker as base
from checker import c0a_four_group_v2 as grouped

BITS = 192
T_LO, T_HI = Fraction(0), Fraction(1, 2)
L_LO, L_HI = Fraction(83, 200), Fraction(9, 20)
T_EDGE = Fraction(1, 2)
A_STAGES = (("A0", 8, 8, 512), ("A1", 16, 16, 1024), ("A2", 32, 32, 2048))
D_STAGES = (("D0", 16, 1024), ("D1", 32, 2048), ("D2", 64, 4096))
ENDPOINT_PANELS = 8192
BISECTION_PANEL_LADDER = (1024, 4096, 16384, 65536)
BISECTION_STEPS = 16
C1A_PANEL_CEILING = 4128768


def _stats():
    return {"series": 0, "direct": 0, "series_hits_moving_u0": 0, "chart_unresolved": 0}


def _g_density_stable(s, t, L, stats):
    s, x, mu, eps, A, delta, delta_sq, gam, u, L2, q, rootq, W, W2, n, m, p, big_q = grouped._primitives(s, t, L)
    R, _, _, _ = base._R(u, gam, stats)
    gt = L * n / (W * q * rootq)
    alpha2 = u * R * R
    return s * (-mu * alpha2 - 2 * A * R * gt)


def _fx_lambda_density(s, t, Lm, stats):
    s, x, mu, eps, A, delta, delta_sq, gam, u, L2, q, rootq, W, W2, n, m, p, big_q = grouped._primitives(s, t, Lm)
    R, Rg, _, _ = base._R(u, gam, stats)
    wlog = Lm * eps / W2
    glam = gam * (1 / Lm - wlog - Lm * delta_sq / q)
    pref = Lm / (W * q * rootq)
    nlam = -2 * Lm * (mu * delta_sq + A * delta)
    preflam = pref * (1 / Lm - wlog - 3 * Lm * delta_sq / q)
    gt = pref * n
    gtlam = preflam * n + pref * nlam
    return 2 * s * (2 * mu * R * glam - 2 * A * (Rg * glam * gt + R * gtlam))


def _integrate(tl, tr, ll, lr, panels, mode, stats):
    grid, root = base._partition(panels)
    t = base._box(base._point(tl), base._point(tr))
    Lm = base._box(base._point(ll), base._point(lr))
    total = arb(0)
    for a, b in zip(grid, grid[1:]):
        aa = root if a == base.SQRT2 else base._point(a)
        bb = root if b == base.SQRT2 else base._point(b)
        s = base._box(aa, bb)
        if mode == "g3":
            y = grouped.density(s, t, Lm, stats)
        elif mode == "fx_lam":
            y = _fx_lambda_density(s, t, Lm, stats)
        elif mode == "g":
            y = _g_density_stable(s, t, Lm, stats)
        else:
            raise ValueError(mode)
        total += y * (bb - aa)
    return total


def _split(a, b, n):
    h = (b - a) / n
    return [(a + i * h, a + (i + 1) * h) for i in range(n)]


def _gate_a():
    for label, nt, nl, panels in A_STAGES:
        st = _stats(); unresolved = 0; worst = None
        for tl, tr in _split(T_LO, T_HI, nt):
            for ll, lr in _split(L_LO, L_HI, nl):
                try:
                    v = _integrate(tl, tr, ll, lr, panels, "g3", st)
                    good = v.upper() < 0
                except (ValueError, ZeroDivisionError):
                    v = None; good = False
                if not good:
                    unresolved += 1
                if v is not None and (worst is None or v.upper() > worst[0]):
                    worst = (v.upper(), tl, tr, ll, lr, v)
        print("C1A_G3_STAGE", label, "t_boxes", nt, "lambda_boxes", nl, "s_panels", panels,
              "unresolved", unresolved, "chart_stats", st,
              "worst", None if worst is None else worst[1:])
        if unresolved == 0:
            print("C1A_G3_FIRST_PASS", label)
            return True, label, worst
    return False, None, worst


def _gate_d():
    for label, nl, panels in D_STAGES:
        st = _stats(); unresolved = 0; weakest = None
        for ll, lr in _split(L_LO, L_HI, nl):
            try:
                v = _integrate(T_EDGE, T_EDGE, ll, lr, panels, "fx_lam", st)
                good = v.lower() > 0
            except (ValueError, ZeroDivisionError):
                v = None; good = False
            if not good:
                unresolved += 1
            if v is not None and (weakest is None or v.lower() < weakest[0]):
                weakest = (v.lower(), ll, lr, v)
        print("C1A_D_STAGE", label, "lambda_boxes", nl, "s_panels", panels,
              "unresolved", unresolved, "chart_stats", st,
              "weakest", None if weakest is None else weakest[1:])
        if unresolved == 0:
            print("C1A_D_FIRST_PASS", label)
            return True, label, weakest
    return False, None, weakest


def _fx_point(lam, panels):
    st = _stats()
    g = _integrate(T_EDGE, T_EDGE, lam, lam, panels, "g", st)
    return 2 * g, st


def _endpoint_signs():
    left, lst = _fx_point(L_LO, ENDPOINT_PANELS)
    right, rst = _fx_point(L_HI, ENDPOINT_PANELS)
    left_ok = left.upper() < 0
    right_ok = right.lower() > 0
    print("C1A_FX_LEFT", "PASS" if left_ok else "UNRESOLVED", L_LO, left, "panels", ENDPOINT_PANELS, "chart_stats", lst)
    print("C1A_FX_RIGHT", "PASS" if right_ok else "UNRESOLVED", L_HI, right, "panels", ENDPOINT_PANELS, "chart_stats", rst)
    return left_ok and right_ok, left, right


def _reported_bisection(left, right):
    lo, hi = L_LO, L_HI
    vlo, vhi = left, right
    depth = 0
    stop_reason = "MAX_DEPTH"
    for k in range(1, BISECTION_STEPS + 1):
        mid = (lo + hi) / 2
        resolved = False
        for panels in BISECTION_PANEL_LADDER:
            v, st = _fx_point(mid, panels)
            if v.upper() < 0:
                lo, vlo = mid, v; sign = "NEG"; resolved = True
            elif v.lower() > 0:
                hi, vhi = mid, v; sign = "POS"; resolved = True
            else:
                print("C1A_BISECTION_TRY", k, "UNRESOLVED", "mid", mid, "panels", panels,
                      "enclosure", v, "chart_stats", st)
                continue
            depth = k
            print("C1A_BISECTION", k, sign, "mid", mid, "panels", panels, "enclosure", v,
                  "FIRST_PASS")
            break
        if not resolved:
            stop_reason = "POINT_UNRESOLVED"
            print("C1A_BISECTION_STOP", "depth", depth, "next_step", k, "mid", mid,
                  "reason", stop_reason)
            break
    ok = vlo.upper() < 0 and vhi.lower() > 0
    print("C1A_REPORTED_CERTIFIED_BRACKET", "PASS" if ok else "UNRESOLVED",
          "depth", depth, "lo", lo, "hi", hi, "F_lo", vlo, "F_hi", vhi,
          "width", hi - lo, "stop_reason", stop_reason)
    return lo, hi, vlo, vhi, depth, stop_reason


def verify():
    ctx.prec = BITS
    base.ctx.prec = BITS
    print("GLOBAL_AXIAL_C1A_CHECKER — PROTOTYPE / NOT_BINDING")
    print("C1A_AMENDMENT analysis/GLOBAL_AXIAL_C1A_PRE_RUN_AMENDMENT.md")
    print("CHECKER_KERNEL TRANSCRIBED_COPY_NOT_INDEPENDENT_DERIVATION")
    print("INDEPENDENCE_SCOPE PRECISION/PARTITION/GATING")
    print("SYMBOLIC_AUDIT USER_SYMBOLIC_AUDIT_PASS")
    print("BITS", BITS, "DEG", base.DEG, "USTAR", "3/5")
    print("A_STAGES", A_STAGES)
    print("D_STAGES", D_STAGES)
    print("ENDPOINT_PANELS", ENDPOINT_PANELS)
    print("BISECTION_PANEL_LADDER", BISECTION_PANEL_LADDER, "BISECTION_STEPS", BISECTION_STEPS,
          "BISECTION_IS_GATING", False)
    print("PREDECLARED_C1A_PANEL_CEILING", C1A_PANEL_CEILING)

    aok, astage, _ = _gate_a()
    dok, dstage, _ = _gate_d()
    eok, left, right = _endpoint_signs()
    if eok:
        _reported_bisection(left, right)
    else:
        print("C1A_REPORTED_CERTIFIED_BRACKET", "UNAVAILABLE", "reason", "ENDPOINT_GATE_UNRESOLVED")

    ok = aok and dok and eok
    print("LOGICAL_FINAL_C1A", "PASS" if ok else "UNRESOLVED",
          "g3_stage", astage, "derivative_stage", dstage,
          "gates", "A_AND_D_AND_ENDPOINT_SIGNS")
    if not ok:
        raise SystemExit("UNRESOLVED")


if __name__ == "__main__":
    verify()
