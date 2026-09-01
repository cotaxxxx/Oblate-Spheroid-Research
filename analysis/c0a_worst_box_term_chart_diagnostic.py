#!/usr/bin/env python3
"""C0a worst-box term-by-chart diagnostic.

REPORT_ONLY / NOT_GATING / PROTOTYPE / NOT_BINDING.

This diagnostic does not modify the C0 kernel, chart policy, USTAR, or any
certification stage.  It reuses the V2 C0 geometry/R-bundle on the three
upper-right A0/A1/A2 boxes and decomposes the g_ttt density into

    8 s mu (T1+T2+T3) - 2 s A (U1+...+U5)

with per-chart accumulated enclosures.  Its purpose is to identify whether
residual interval width is concentrated in the direct-chart U1 term near the
moving removable locus u=0.
"""
from fractions import Fraction

from flint import arb, ctx

# Importing V2 applies only the declared t<=1/2 redeclaration and stabilized
# g density.  The g3 kernel and fixed two-chart policy remain the audited base.
from producer import global_axial_c0_producer_v2 as v2  # noqa: F401
from producer import global_axial_c0_producer as base
from producer.endpoint_interval_producer import _point, _box, SQRT2


ctx.prec = base.BITS

BOXES = (
    ("A0", Fraction(7, 16), Fraction(1, 2), Fraction(661, 1600), Fraction(83, 200), 512),
    ("A1", Fraction(15, 32), Fraction(1, 2), Fraction(53, 128), Fraction(83, 200), 1024),
    ("A2", Fraction(31, 64), Fraction(1, 2), Fraction(2653, 6400), Fraction(83, 200), 2048),
)
TERMS = ("T1", "T2", "T3", "U1", "U2", "U3", "U4", "U5")
CHARTS = ("series", "direct")


def width(x):
    return x.upper() - x.lower()


def classify_chart(u):
    if u.upper() <= base.USTAR:
        return "series"
    if u.lower() > 0:
        return "direct"
    return "unresolved"


def term_densities(s, t, lam, stats):
    mu, A, gamma, u, gt, gtt, gttt, gtttt = base._geometry(s, t, lam)
    chart = classify_chart(u)
    if chart == "unresolved":
        return chart, u, None
    R, Rg, Rgg, Rggg = base._R_bundle(u, gamma, stats)

    T1 = Rgg * gt**3
    T2 = 3 * Rg * gt * gtt
    T3 = R * gttt
    U1 = Rggg * gt**4
    U2 = 6 * Rgg * gt * gt * gtt
    U3 = 3 * Rg * gtt * gtt
    U4 = 4 * Rg * gt * gttt
    U5 = R * gtttt

    vals = (
        8 * s * mu * T1,
        8 * s * mu * T2,
        8 * s * mu * T3,
        -2 * s * A * U1,
        -2 * s * A * U2,
        -2 * s * A * U3,
        -2 * s * A * U4,
        -2 * s * A * U5,
    )
    return chart, u, vals


def moving_corner_data(t, lam):
    # h = mu(1-lambda^2)+lambda^2 t; h=0 gives the removable locus.
    mu0 = -(lam * lam * t) / (1 - lam * lam)
    s02 = 1 - mu0
    return mu0, s02


def run_box(label, tl, tr, ll, lr, panels):
    print("C0A_TERM_CHART_DIAGNOSTIC", label)
    print("BOX", "t", (tl, tr), "lambda", (ll, lr), "s_panels_per_unit", panels)
    t = _box(_point(tl), _point(tr))
    lam = _box(_point(ll), _point(lr))
    grid, root = base._partition(panels)

    sums = {chart: {name: arb(0) for name in TERMS} for chart in CHARTS}
    counts = {"series": 0, "direct": 0, "unresolved": 0}
    stats = {"series": 0, "direct": 0, "series_hits_moving_u0": 0, "chart_unresolved": 0}
    direct_min_u_lower = None
    direct_max = None
    unresolved_panels = []

    # Locate the exact moving-locus point at the upper-right corner, which is
    # where all three logged worst boxes are anchored.
    mu0, s02 = moving_corner_data(tr, lr)
    s0 = _point(s02).sqrt()
    moving_index = None
    moving_interval = None

    for idx, (a, b) in enumerate(zip(grid, grid[1:])):
        aa = root if a == SQRT2 else _point(a)
        bb = root if b == SQRT2 else _point(b)
        s = _box(aa, bb)

        if moving_index is None and aa <= s0 <= bb:
            moving_index = idx
            moving_interval = (a, b)

        chart, u, vals = term_densities(s, t, lam, stats)
        counts[chart] += 1
        if chart == "unresolved":
            unresolved_panels.append((idx, a, b, u))
            continue

        ds = bb - aa
        panel_total = arb(0)
        for name, val in zip(TERMS, vals):
            contrib = val * ds
            sums[chart][name] += contrib
            panel_total += contrib

        if chart == "direct":
            ulo = u.lower()
            if direct_min_u_lower is None or ulo < direct_min_u_lower:
                direct_min_u_lower = ulo
            rec = (width(panel_total), idx, a, b, u, panel_total)
            if direct_max is None or rec[0] > direct_max[0]:
                direct_max = rec

    print("series_panels", counts["series"])
    print("direct_panels", counts["direct"])
    print("series_hits_moving_u0", stats["series_hits_moving_u0"])
    print("unresolved_panels", counts["unresolved"])
    print("direct_min_u_lower", direct_min_u_lower)
    print("moving_corner_mu0", mu0)
    print("moving_corner_s0", s0)
    print("moving_u0_panel_index", moving_index)
    print("moving_u0_panel_s_interval", moving_interval)

    if direct_max is None:
        print("direct_max_width_panel", None)
    else:
        w, idx, a, b, u, total = direct_max
        print("direct_max_width_panel", idx, "s_interval", (a, b), "width", w,
              "u", u, "panel_total", total)

    for chart in CHARTS:
        print("CHART", chart)
        for name in TERMS:
            v = sums[chart][name]
            print("TERM", name, "enclosure", v, "width", width(v))
        total = sum(sums[chart].values(), arb(0))
        print("CHART_TOTAL", chart, "enclosure", total, "width", width(total))

    grand = arb(0)
    for chart in CHARTS:
        for name in TERMS:
            grand += sums[chart][name]
    print("DIAGNOSTIC_TOTAL", grand, "width", width(grand))

    if unresolved_panels:
        print("UNRESOLVED_PANEL_DETAILS")
        for rec in unresolved_panels:
            print("UNRESOLVED_PANEL", *rec)
    print("END_C0A_TERM_CHART_DIAGNOSTIC", label)


def main():
    print("C0A WORST-BOX TERM-BY-CHART DIAGNOSTIC — REPORT_ONLY / NOT_GATING")
    print("EVIDENCE_CLASS PROTOTYPE / NOT_BINDING")
    print("BITS", base.BITS, "DEG", base.DEG, "USTAR", "3/5")
    print("CHART_POLICY upper(u)<=3/5 -> series; lower(u)>0 -> direct; otherwise unresolved")
    for args in BOXES:
        run_box(*args)


if __name__ == "__main__":
    main()
