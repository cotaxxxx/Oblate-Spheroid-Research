#!/usr/bin/env python3
"""DIAGNOSTIC_ONLY term-by-chart width audit for the fixed monotone-tube run.

This does not change the fixed contract and is not gating.  It reconstructs
exactly the current producer representation, accumulates T1/T2/T3 separately
by chart for each of the 64 fixed parameter boxes, and reports the first box
and the box with the largest total radius.
"""
from __future__ import annotations

from collections import defaultdict
from fractions import Fraction

from flint import arb, ctx

from producer.endpoint_interval_producer import SQRT2, _box, _partition, _point, _series
from producer.monotone_tube_interval_producer import (
    BITS,
    L_LEFT,
    L_RIGHT,
    L_SPLITS,
    SERIES_DEGREE,
    S_PANELS,
    T_LEFT,
    T_RIGHT,
    T_SPLITS,
    _arb_interval,
    _contains_zero,
    _nonnegative_sqrt_hull,
    _pow,
    _quantities,
    _split,
    _square,
    _unit_hull,
)

STATUS = "DIAGNOSTIC_ONLY / NOT_BINDING"


def _terms(s, t, lam, degree, corner=False):
    e, gap, mu, d, lam2, A, q, w2, w, ht, H = _quantities(s, t, lam)
    lam3 = lam2 * lam

    if corner:
        rho = _box(arb(0), 1 / gap.lower().sqrt())
        inv_lam_hi = (1 / lam).upper()
        phi = _box(-inv_lam_hi, inv_lam_hi)
        Ahat = gap * s * rho - mu * phi
        R = _box(arb(1), arb.pi() / 2)
        Rg = _box(-arb(1), -arb(1) / 3)
        sqrtq = _nonnegative_sqrt_hull(q)
        chart = "corner_hull"
    else:
        if not q.lower() > 0:
            raise ValueError("ordinary diagnostic requires q>0")
        sqrtq = q.sqrt()
        gamma = _unit_hull(lam * A / (w * sqrtq))
        u0 = _unit_hull(e * gap * _square(ht) / (w2 * q))
        glo = max(arb(0), gamma.lower())
        ghi = min(arb(1), gamma.upper())
        ulo = max(u0.lower(), arb(1) - ghi * ghi)
        uhi = min(u0.upper(), arb(1) - glo * glo)
        if uhi < ulo:
            raise ValueError("inconsistent gamma/u enclosures")
        u = _box(ulo, uhi)
        gc_lo = max(arb(0), arb(1) - u.upper()).sqrt()
        gc_hi = max(arb(0), arb(1) - u.lower()).sqrt()
        g2lo = max(gamma.lower(), gc_lo)
        g2hi = min(gamma.upper(), gc_hi)
        gamma = _box(g2lo, g2hi)

        use_u = _contains_zero(ht) or not u.lower() > 0
        if use_u:
            R, _ = _series(u, "Psi", degree, clamped_nonnegative=True)
            Psip, _ = _series(u, "Psi_prime", degree, clamped_nonnegative=True)
            Rg = -2 * gamma * Psip
            chart = "u_upper"
        else:
            R = gamma.acos() / u.sqrt()
            Rg = (gamma * R - 1) / u
            chart = "gamma_lower"

        # Current producer representation, deliberately unchanged for diagnosis.
        rho = s / sqrtq
        phi = d / sqrtq
        Ahat = A / sqrtq

    T1 = -4 * mu * R * lam * _pow(rho, 3) * H / w
    T2 = -2 * Rg * lam2 * H * H * Ahat * _pow(rho, 5) / w2
    T3 = -2 * R * lam3 * Ahat * _pow(rho, 3) * (3 * phi * H - gap * sqrtq) / w
    return chart, (T1, T2, T3)


def _fmt(x):
    return {
        "mid": x.mid().str(18),
        "rad": x.rad().str(18),
        "lo": x.lower().str(18),
        "hi": x.upper().str(18),
    }


def box_record(ti, li, tbox, lbox, sends, sqrt2, degree):
    tl, tr = tbox
    ll, lr = lbox
    t = _arb_interval(tl, tr)
    lam = _arb_interval(ll, lr)
    by_chart = defaultdict(lambda: [arb(0), arb(0), arb(0)])
    total_terms = [arb(0), arb(0), arb(0)]
    total = arb(0)
    counts = defaultdict(int)

    for si, (sl, sr) in enumerate(zip(sends, sends[1:])):
        left = sqrt2 if sl == SQRT2 else _point(sl)
        right = sqrt2 if sr == SQRT2 else _point(sr)
        s = _box(left, right)
        chart, terms = _terms(s, t, lam, degree, corner=(ti == T_SPLITS - 1 and si == 0))
        width = right - left
        counts[chart] += 1
        for j, term in enumerate(terms):
            contrib = term * width
            by_chart[chart][j] += contrib
            total_terms[j] += contrib
            total += contrib

    return {
        "ti": ti,
        "li": li,
        "t_box": [str(tl), str(tr)],
        "lambda_box": [str(ll), str(lr)],
        "counts": dict(counts),
        "total": total,
        "total_terms": total_terms,
        "by_chart": dict(by_chart),
    }


def print_record(label, rec):
    print(f"\n=== {label} ===")
    print("status:", STATUS)
    print("t_box:", rec["t_box"], "lambda_box:", rec["lambda_box"])
    print("chart_counts:", rec["counts"])
    print("TOTAL:", _fmt(rec["total"]))
    print("TOTAL TERMS:")
    for name, val in zip(("T1", "T2", "T3"), rec["total_terms"]):
        print(f"  {name}: {_fmt(val)}")
    print("BY CHART:")
    for chart in ("gamma_lower", "u_upper", "corner_hull"):
        if chart not in rec["by_chart"]:
            continue
        print(f"  [{chart}]")
        for name, val in zip(("T1", "T2", "T3"), rec["by_chart"][chart]):
            print(f"    {name}: {_fmt(val)}")


def main():
    ctx.prec = BITS
    sends, sqrt2 = _partition(S_PANELS)
    tboxes = _split(T_LEFT, T_RIGHT, T_SPLITS)
    lboxes = _split(L_LEFT, L_RIGHT, L_SPLITS)

    records = []
    for ti, tbox in enumerate(tboxes):
        for li, lbox in enumerate(lboxes):
            records.append(box_record(ti, li, tbox, lbox, sends, sqrt2, SERIES_DEGREE))

    first = records[0]
    widest = max(records, key=lambda r: r["total"].rad())
    print("MONOTONE_TUBE WIDTH DIAGNOSTIC")
    print("fixed contract unchanged; diagnostic only")
    print_record("FIRST BOX", first)
    print_record("MAX TOTAL-RADIUS BOX", widest)


if __name__ == "__main__":
    main()
