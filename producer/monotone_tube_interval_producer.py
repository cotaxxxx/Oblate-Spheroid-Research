#!/usr/bin/env python3
"""Arb producer candidate for the oblate near-boundary monotone tube.

Status: PROTOTYPE / NOT_AUDITED / NOT_BINDING.
Fixed claim: partial_t g_axis_ob(t,lambda) < 0 on
[63/64,1] x [5/8,33/50].  The sole gate is upper_endpoint < 0 on every
one of the 8 x 8 exact parameter boxes fixed before implementation.
"""

from __future__ import annotations

from fractions import Fraction
from flint import arb, ctx

from producer.endpoint_interval_producer import (
    SQRT2, _box, _clamp_nonnegative, _partition, _point, _series,
)

T_LEFT = Fraction(63, 64)
T_RIGHT = Fraction(1, 1)
L_LEFT = Fraction(5, 8)
L_RIGHT = Fraction(33, 50)
T_SPLITS = 8
L_SPLITS = 8
S_PANELS = 1024
SERIES_DEGREE = 50
BITS = 160


def _arb_interval(lo, hi):
    return _box(_point(lo), _point(hi))


def _unit_hull(x):
    lo = max(arb(0), x.lower())
    hi = min(arb(1), x.upper())
    if hi < lo:
        raise ValueError("empty [0,1] intersection")
    return _box(lo, hi)


def _square(x):
    lo = x.lower(); hi = x.upper()
    if lo <= 0 <= hi:
        upper = max((-lo) * (-lo), hi * hi)
        return _box(arb(0), upper)
    a = lo * lo; b = hi * hi
    return _box(min(a, b), max(a, b))


def _pow(x, n):
    out = arb(1)
    for _ in range(n): out *= x
    return out


def _contains_zero(x):
    return x.lower() <= 0 <= x.upper()


def _general_quantities(s, t, lam):
    e = _square(s); gap = 2 - e; mu = 1 - e
    delta = 1 - t; d = e - delta; lam2 = _square(lam)
    A = 1 - t * mu
    q = _clamp_nonnegative(e * gap + lam2 * _square(d))
    w2 = lam2 * e * gap + _square(mu); w = w2.sqrt()
    h_t = mu + lam2 * d
    H = (1 - e) * gap + lam2 * (2 * e - 2 * delta - e * e + delta * e)
    return e, gap, mu, delta, d, lam2, A, q, w2, w, h_t, H


def _corner_kernel(s, t, lam):
    e, gap, mu, delta, d, lam2, A, q, w2, w, h_t, H = _general_quantities(s, t, lam)
    lam3 = lam2 * lam
    rho = _box(arb(0), 1 / gap.lower().sqrt())
    phi = arb(0, (1 / lam).upper())
    Ahat = gap * s * rho - mu * phi
    sqrtq = q.sqrt()
    R = _box(arb(1), arb.pi() / 2)
    Rg = _box(-arb(1), -arb(1) / 3)
    T1 = -4 * mu * R * lam * _pow(rho, 3) * H / w
    T2 = -2 * Rg * lam2 * H * H * Ahat * _pow(rho, 5) / w2
    T3 = -2 * R * lam3 * Ahat * _pow(rho, 3) * (3 * phi * H - gap * sqrtq) / w
    return T1 + T2 + T3, "corner_hull"


def _ordinary_kernel(s, t, lam, degree):
    e, gap, mu, delta, d, lam2, A, q, w2, w, h_t, H = _general_quantities(s, t, lam)
    if not q.lower() > 0:
        raise ValueError("ordinary chart requires q>0")
    sqrtq = q.sqrt(); q32 = q * sqrtq; q52 = q * q32; lam3 = lam2 * lam
    gamma = _unit_hull(lam * A / (w * sqrtq))
    u = _unit_hull(_clamp_nonnegative(e * gap * _square(h_t) / (w2 * q)))
    gt = -lam * e * H / (w * q32)
    gtt = lam3 * e * (3 * d * H - gap * q) / (w * q52)

    # The series chart is mandatory whenever u can touch zero, whether through
    # the moving h_t=0 locus or through s=0 with t<1 (where gamma=1 exactly).
    use_u = _contains_zero(h_t) or not u.lower() > 0
    if use_u:
        if not u.upper() < 1:
            raise ValueError("u_upper requires u<1")
        R, _ = _series(u, "Psi", degree, clamped_nonnegative=True)
        Psip, _ = _series(u, "Psi_prime", degree, clamped_nonnegative=True)
        Rg = -2 * gamma * Psip
        chart = "u_upper"
    else:
        R = gamma.acos() / u.sqrt()
        Rg = (gamma * R - 1) / u
        chart = "gamma_lower"

    G = s * (4 * mu * R * gt - 2 * A * (Rg * gt * gt + R * gtt))
    return G, chart


def _split(a, b, n):
    width = (b - a) / n
    return [(a + i * width, a + (i + 1) * width) for i in range(n)]


def produce_record(bits=BITS, panels=S_PANELS, degree=SERIES_DEGREE):
    ctx.prec = bits
    s_endpoints, sqrt2 = _partition(panels)
    t_boxes = _split(T_LEFT, T_RIGHT, T_SPLITS)
    l_boxes = _split(L_LEFT, L_RIGHT, L_SPLITS)
    records = []; all_pass = True
    for ti, (tl, tr) in enumerate(t_boxes):
        t = _arb_interval(tl, tr)
        for li, (ll, lr) in enumerate(l_boxes):
            lam = _arb_interval(ll, lr); total = arb(0)
            chart_counts = {"gamma_lower": 0, "u_upper": 0, "corner_hull": 0}
            for si, (sl, sr) in enumerate(zip(s_endpoints, s_endpoints[1:])):
                sleft = sqrt2 if sl == SQRT2 else _point(sl)
                sright = sqrt2 if sr == SQRT2 else _point(sr)
                s = _box(sleft, sright)
                if ti == T_SPLITS - 1 and si == 0:
                    kernel, chart = _corner_kernel(s, t, lam)
                else:
                    kernel, chart = _ordinary_kernel(s, t, lam, degree)
                chart_counts[chart] += 1
                total += kernel * (sright - sleft)
            passed = bool(total.upper() < 0); all_pass = all_pass and passed
            records.append({"t_box": [str(tl), str(tr)], "lambda_box": [str(ll), str(lr)],
                "chart_counts": chart_counts, "total_mid": total.mid().str(50),
                "total_rad": total.rad().str(50), "upper_negative": passed})
    return {"schema": "bg-oblate-spheroid.monotone-tube.v1",
        "status": "PROTOTYPE_NOT_AUDITED_NOT_BINDING",
        "contract": {"t_domain": ["63/64", "1"], "lambda_domain": ["5/8", "33/50"],
            "t_boxes": 8, "lambda_boxes": 8, "s_panels": panels,
            "series_degree": degree, "bits": bits, "required_sign": "NEG",
            "sole_gate": "every parameter-box total.upper() < 0"},
        "parameter_boxes": records, "gating_pass": all_pass}
