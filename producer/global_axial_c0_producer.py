#!/usr/bin/env python3
"""C0 quantitative pitchfork Arb producer.

Evidence class: PROTOTYPE / NOT_BINDING.
The stage schedule is predeclared and first-passing: later stages are not
consulted after the first stage that proves the requested gate.
"""
from fractions import Fraction
from flint import arb, ctx
from producer.endpoint_interval_producer import _point, _box, _partition, SQRT2

BITS = 160
DEG = 50
USTAR = arb(3) / 5
T_LO, T_HI = Fraction(0), Fraction(5, 16)
L_LO, L_HI = Fraction(2, 5), Fraction(83, 200)
T_EDGE = Fraction(5, 16)

# (label, t_boxes, lambda_boxes, s_panels_per_unit)
C0A_STAGES = (
    ("A0", 8, 8, 512),
    ("A1", 16, 16, 1024),
    ("A2", 32, 32, 2048),
)
# (label, lambda_boxes, s_panels_per_unit)
C0B_STAGES = (
    ("B0", 16, 512),
    ("B1", 32, 1024),
    ("B2", 64, 2048),
)
# Safe predeclared cap: each _partition has < 2*panels cells.
MAX_S_PANEL_EVALS = (
    sum(2 * p * nt * nl for _, nt, nl, p in C0A_STAGES)
    + sum(2 * p * nl for _, nl, p in C0B_STAGES)
)


def _coeffs():
    out = [Fraction(1)]
    c = Fraction(1)
    for k in range(DEG + 2):
        c *= Fraction((2 * k + 1) ** 2, 2 * (k + 1) * (2 * k + 3))
        out.append(c)
    return out


COEFFS = _coeffs()


def _unit_nonnegative(x):
    lo = max(arb(0), x.lower())
    hi = min(arb(1), x.upper())
    if hi < lo:
        raise ValueError("empty exact 0<=u<=1 intersection")
    return _box(lo, hi)


def _psi_bundle(u, gamma):
    R = arb(0); Rp = arb(0); Rpp = arb(0); Rppp = arb(0)
    powers = [arb(1)]
    for _ in range(DEG + 1):
        powers.append(powers[-1] * u)
    for n, c in enumerate(COEFFS[: DEG + 1]):
        a = arb(c.numerator) / c.denominator
        R += a * powers[n]
        if n:
            Rp += n * a * powers[n - 1]
        if n > 1:
            Rpp += n * (n - 1) * a * powers[n - 2]
        if n > 2:
            Rppp += n * (n - 1) * (n - 2) * a * powers[n - 3]
    U = u.upper()
    c = COEFFS[DEG + 1]
    cn = arb(c.numerator) / c.denominator
    R += _box(arb(0), cn * powers[DEG + 1].upper() / (1 - U))
    Rp += _box(arb(0), (DEG + 1) * cn * powers[DEG].upper() /
               (1 - U * arb(DEG + 2) / (DEG + 1)))
    Rpp += _box(arb(0), (DEG + 1) * DEG * cn * powers[DEG - 1].upper() /
                (1 - U * arb(DEG + 2) / DEG))
    Rppp += _box(arb(0), (DEG + 1) * DEG * (DEG - 1) * cn * powers[DEG - 2].upper() /
                 (1 - U * arb(DEG + 2) / (DEG - 1)))
    return (
        R,
        -2 * gamma * Rp,
        4 * gamma * gamma * Rpp - 2 * Rp,
        -8 * gamma * gamma * gamma * Rppp + 12 * gamma * Rpp,
    )


def _geometry(s, t, lam):
    s2 = s * s
    mu = 1 - s2
    e = 1 - mu * mu
    l2 = lam * lam
    l4 = l2 * l2
    A = 1 - t * mu
    d = t - mu
    q = e + l2 * d * d
    w2 = mu * mu + l2 * e
    w = w2.sqrt()
    gamma = lam * A / (w * q.sqrt())
    # Exact factorized complement; clamp only by the exact identity 0<=u<=1.
    h = mu * (1 - l2) + l2 * t
    u = _unit_nonnegative(e * h * h / (w2 * q))

    N = -mu * q - A * l2 * d
    N1 = -l2 * e
    M = N1 * q - 3 * N * l2 * d
    M1 = l4 * e * d - 3 * l2 * N
    P = M1 * q - 5 * M * l2 * d
    M2 = 4 * l4 * e
    P1 = M2 * q - 3 * l2 * d * M1 - 5 * l2 * M

    sq = q.sqrt()
    gt = lam * N / (w * q * sq)
    gtt = lam * M / (w * q * q * sq)
    gttt = lam * P / (w * q * q * q * sq)
    gtttt = lam * (P1 * q - 7 * P * l2 * d) / (w * q * q * q * q * sq)
    return mu, A, gamma, u, gt, gtt, gttt, gtttt


def _R_bundle(u, gamma, stats):
    if u.upper() <= USTAR:
        stats["series"] += 1
        if u.lower() <= 0:
            stats["series_hits_moving_u0"] += 1
        return _psi_bundle(u, gamma)
    if u.lower() <= 0:
        stats["chart_unresolved"] += 1
        raise ValueError("u interval meets 0 but exceeds series chart threshold")
    stats["direct"] += 1
    sq = u.sqrt()
    R = sq.asin() / sq
    Rg = (gamma * R - 1) / u
    Rgg = ((R + gamma * Rg) * u + 2 * gamma * (gamma * R - 1)) / (u * u)
    Rggg = (3 * gamma * (2 * gamma * gamma + 3) * R - (11 * gamma * gamma + 4)) / (u * u * u)
    return R, Rg, Rgg, Rggg


def _g3_density(s, t, lam, stats):
    mu, A, gamma, u, gt, gtt, gttt, gtttt = _geometry(s, t, lam)
    R, Rg, Rgg, Rggg = _R_bundle(u, gamma, stats)
    Ctt = Rgg * gt**3 + 3 * Rg * gt * gtt + R * gttt
    Cttt = (Rggg * gt**4 + 6 * Rgg * gt * gt * gtt + 3 * Rg * gtt * gtt
             + 4 * Rg * gt * gttt + R * gtttt)
    return s * (8 * mu * Ctt - 2 * A * Cttt)


def _g_density(s, t, lam, stats):
    mu, A, gamma, u, gt, _, _, _ = _geometry(s, t, lam)
    R, _, _, _ = _R_bundle(u, gamma, stats)
    alpha2 = u.sqrt().asin() ** 2
    return s * (-mu * alpha2 - 2 * A * R * gt)


def _integrate_box(tl, tr, ll, lr, panels, mode, stats):
    grid, root = _partition(panels)
    t = _box(_point(tl), _point(tr))
    lam = _box(_point(ll), _point(lr))
    z = arb(0)
    for a, b in zip(grid, grid[1:]):
        aa = root if a == SQRT2 else _point(a)
        bb = root if b == SQRT2 else _point(b)
        s = _box(aa, bb)
        if mode == "g3":
            y = _g3_density(s, t, lam, stats)
        else:
            y = _g_density(s, t, lam, stats)
        z += y * (bb - aa)
    return z


def _split(a, b, n):
    h = (b - a) / n
    return [(a + i * h, a + (i + 1) * h) for i in range(n)]


def _run_c0a():
    for label, nt, nl, panels in C0A_STAGES:
        stats = {"series": 0, "direct": 0, "series_hits_moving_u0": 0, "chart_unresolved": 0}
        unresolved = 0; worst = None
        for tl, tr in _split(T_LO, T_HI, nt):
            for ll, lr in _split(L_LO, L_HI, nl):
                try:
                    v = _integrate_box(tl, tr, ll, lr, panels, "g3", stats)
                    good = v.upper() < 0
                except (ValueError, ZeroDivisionError):
                    v = None; good = False
                if not good:
                    unresolved += 1
                if v is not None and (worst is None or v.upper() > worst[0]):
                    worst = (v.upper(), tl, tr, ll, lr, v)
        print("C0A_STAGE", label, "t_boxes", nt, "lambda_boxes", nl, "s_panels", panels,
              "unresolved", unresolved, "chart_stats", stats,
              "worst", None if worst is None else worst[1:])
        if unresolved == 0:
            print("C0A_FIRST_PASS", label)
            return True, label, worst
    return False, None, worst


def _run_c0b():
    for label, nl, panels in C0B_STAGES:
        stats = {"series": 0, "direct": 0, "series_hits_moving_u0": 0, "chart_unresolved": 0}
        unresolved = 0; worst = None
        for ll, lr in _split(L_LO, L_HI, nl):
            try:
                g = _integrate_box(T_EDGE, T_EDGE, ll, lr, panels, "g", stats)
                v = g / _point(T_EDGE)
                good = v.upper() < 0
            except (ValueError, ZeroDivisionError):
                v = None; good = False
            if not good:
                unresolved += 1
            if v is not None and (worst is None or v.upper() > worst[0]):
                worst = (v.upper(), ll, lr, v)
        print("C0B_STAGE", label, "lambda_boxes", nl, "s_panels", panels,
              "unresolved", unresolved, "chart_stats", stats,
              "worst", None if worst is None else worst[1:])
        if unresolved == 0:
            print("C0B_FIRST_PASS", label)
            return True, label, worst
    return False, None, worst


def run():
    ctx.prec = BITS
    print("GLOBAL_AXIAL_C0_PRODUCER — PROTOTYPE / NOT_BINDING")
    print("BITS", BITS, "DEG", DEG, "USTAR", "3/5")
    print("C0A_STAGES", C0A_STAGES)
    print("C0B_STAGES", C0B_STAGES)
    print("PREDECLARED_MAX_S_PANEL_EVALS", MAX_S_PANEL_EVALS)
    aok, astage, aworst = _run_c0a()
    bok, bstage, bworst = _run_c0b()
    ok = aok and bok
    print("LOGICAL_FINAL_C0", "PASS" if ok else "UNRESOLVED",
          "C0a_stage", astage, "C0b_stage", bstage,
          "claim: g_ttt<0 on box and Phi(t=5/16)<0 on lambda interval")
    if not ok:
        raise SystemExit("UNRESOLVED")


if __name__ == "__main__":
    run()
