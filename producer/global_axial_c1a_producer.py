#!/usr/bin/env python3
"""C1a crossing-bridge Arb producer.

Implements only the predeclared C1a gates:
  A: g_ttt < 0 on [0,1/2] x [83/200,9/20]
  D: d_lambda F_x > 0 on [83/200,9/20]
  endpoint signs and exact-rational bisection for lambda_x.

Evidence class: PROTOTYPE / NOT_BINDING until a pinned machine receipt exists.
"""
from fractions import Fraction
from flint import arb, ctx

from producer import global_axial_c0_producer as base
from producer import c0a_four_group_v2 as grouped

BITS = 160
T_LO, T_HI = Fraction(0), Fraction(1, 2)
L_LO, L_HI = Fraction(83, 200), Fraction(9, 20)
T_EDGE = Fraction(1, 2)
A_STAGES = (("A0", 8, 8, 512), ("A1", 16, 16, 1024), ("A2", 32, 32, 2048))
D_STAGES = (("D0", 16, 1024), ("D1", 32, 2048), ("D2", 64, 4096))
POINT_PANELS = 8192
BISECTION_STEPS = 16
C1A_PANEL_CEILING = 2883584


def _stats():
    return {"series": 0, "direct": 0, "series_hits_moving_u0": 0, "chart_unresolved": 0}


def _g_density_stable(s, t, lam, stats):
    s, x, mu, e, A, d, d2, gamma, u, l2, q, sq, w, w2, N, M, P, Q = grouped._geometry(s, t, lam)
    R, _, _, _ = base._R_bundle(u, gamma, stats)
    gt = lam * N / (w * q * sq)
    alpha2 = u * R * R
    return s * (-mu * alpha2 - 2 * A * R * gt)


def _fx_lambda_density(s, t, lam, stats):
    s, x, mu, e, A, d, d2, gamma, u, l2, q, sq, w, w2, N, M, P, Q = grouped._geometry(s, t, lam)
    R, Rg, _, _ = base._R_bundle(u, gamma, stats)

    wl_over_w = lam * e / w2
    gamma_lam = gamma * (1 / lam - wl_over_w - lam * d2 / q)

    L = lam / (w * q * sq)
    N_lam = -2 * lam * (mu * d2 + A * d)
    L_lam = L * (1 / lam - wl_over_w - 3 * lam * d2 / q)
    gt = L * N
    gt_lam = L_lam * N + L * N_lam

    # This is already the F_x derivative density: outer factor 2 from F_x=2g(1/2,lambda).
    return 2 * s * (2 * mu * R * gamma_lam - 2 * A * (Rg * gamma_lam * gt + R * gt_lam))


def _integrate(tl, tr, ll, lr, panels, mode, stats):
    grid, root = base._partition(panels)
    t = base._box(base._point(tl), base._point(tr))
    lam = base._box(base._point(ll), base._point(lr))
    z = arb(0)
    for a, b in zip(grid, grid[1:]):
        aa = root if a == base.SQRT2 else base._point(a)
        bb = root if b == base.SQRT2 else base._point(b)
        s = base._box(aa, bb)
        if mode == "g3":
            y = grouped.density(s, t, lam, stats)
        elif mode == "fx_lam":
            y = _fx_lambda_density(s, t, lam, stats)
        elif mode == "g":
            y = _g_density_stable(s, t, lam, stats)
        else:
            raise ValueError(mode)
        z += y * (bb - aa)
    return z


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
        st = _stats(); unresolved = 0; worst = None
        for ll, lr in _split(L_LO, L_HI, nl):
            try:
                v = _integrate(T_EDGE, T_EDGE, ll, lr, panels, "fx_lam", st)
                good = v.lower() > 0
            except (ValueError, ZeroDivisionError):
                v = None; good = False
            if not good:
                unresolved += 1
            if v is not None and (worst is None or v.lower() < worst[0]):
                worst = (v.lower(), ll, lr, v)
        print("C1A_D_STAGE", label, "lambda_boxes", nl, "s_panels", panels,
              "unresolved", unresolved, "chart_stats", st,
              "weakest", None if worst is None else worst[1:])
        if unresolved == 0:
            print("C1A_D_FIRST_PASS", label)
            return True, label, worst
    return False, None, worst


def _fx_point(lam):
    st = _stats()
    g = _integrate(T_EDGE, T_EDGE, lam, lam, POINT_PANELS, "g", st)
    return 2 * g, st


def _endpoint_and_bisection():
    left, lst = _fx_point(L_LO)
    right, rst = _fx_point(L_HI)
    left_ok = left.upper() < 0
    right_ok = right.lower() > 0
    print("C1A_FX_LEFT", "PASS" if left_ok else "UNRESOLVED", L_LO, left, "chart_stats", lst)
    print("C1A_FX_RIGHT", "PASS" if right_ok else "UNRESOLVED", L_HI, right, "chart_stats", rst)
    if not (left_ok and right_ok):
        return False, None

    lo, hi = L_LO, L_HI
    for k in range(1, BISECTION_STEPS + 1):
        mid = (lo + hi) / 2
        v, st = _fx_point(mid)
        if v.upper() < 0:
            lo = mid; sign = "NEG"
        elif v.lower() > 0:
            hi = mid; sign = "POS"
        else:
            print("C1A_BISECTION", k, "UNRESOLVED", "mid", mid, "enclosure", v, "chart_stats", st)
            return False, None
        print("C1A_BISECTION", k, sign, "mid", mid, "enclosure", v)
    vlo, _ = _fx_point(lo); vhi, _ = _fx_point(hi)
    ok = vlo.upper() < 0 and vhi.lower() > 0
    print("C1A_LAMBDA_X_BRACKET", "PASS" if ok else "UNRESOLVED", "lo", lo, "hi", hi,
          "F_lo", vlo, "F_hi", vhi, "width", hi - lo)
    return ok, (lo, hi, vlo, vhi)


def run():
    ctx.prec = BITS
    base.ctx.prec = BITS
    print("GLOBAL_AXIAL_C1A_PRODUCER — PROTOTYPE / NOT_BINDING")
    print("SYMBOLIC_AUDIT USER_SYMBOLIC_AUDIT_PASS")
    print("CHECKED_SCOPE", "t", (T_LO, T_HI), "lambda", (L_LO, L_HI), "T_EDGE", T_EDGE)
    print("BITS", BITS, "DEG", base.DEG, "USTAR", "3/5")
    print("A_STAGES", A_STAGES)
    print("D_STAGES", D_STAGES)
    print("POINT_PANELS", POINT_PANELS, "BISECTION_STEPS", BISECTION_STEPS)
    print("PREDECLARED_C1A_PANEL_CEILING", C1A_PANEL_CEILING)

    aok, astage, _ = _gate_a()
    dok, dstage, _ = _gate_d()
    xok, bracket = _endpoint_and_bisection()
    ok = aok and dok and xok
    print("LOGICAL_FINAL_C1A", "PASS" if ok else "UNRESOLVED",
          "g3_stage", astage, "derivative_stage", dstage,
          "claim: g_ttt<0, F_x strictly increasing, unique crossing lambda_x")
    if not ok:
        raise SystemExit("UNRESOLVED")


if __name__ == "__main__":
    run()
