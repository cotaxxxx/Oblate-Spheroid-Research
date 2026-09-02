#!/usr/bin/env python3
"""C1b B_ob<0 bridge producer on [9/20,5/8].

Uses the pinned endpoint-regular two-chart B_ob kernel.
Evidence class: PROTOTYPE / NOT_BINDING until a pinned machine receipt exists.
"""
from fractions import Fraction
from flint import arb, ctx

from producer.endpoint_interval_producer import SQRT2, _box, _kernel_box, _partition, _point

BITS = 160
DEG = 50
L_LO = Fraction(9, 20)
L_HI = Fraction(5, 8)
STAGES = (("B0", 16, 1024), ("B1", 32, 2048), ("B2", 64, 4096))
PANEL_CEILING = 344064


def _split(a, b, n):
    h = (b - a) / n
    return [(a + i*h, a + (i+1)*h) for i in range(n)]


def _integrate(ll, lr, panels):
    endpoints, root = _partition(panels)
    lam = _box(_point(ll), _point(lr))
    total = arb(0)
    charts = {"gamma_lower": 0, "u_upper": 0}
    for left, right in zip(endpoints, endpoints[1:]):
        la = root if left == SQRT2 else _point(left)
        ra = root if right == SQRT2 else _point(right)
        chart = "gamma_lower" if right != SQRT2 and right <= 1 else "u_upper"
        s = _box(la, ra)
        kernel, _ = _kernel_box(s, lam, chart, False, DEG)
        total += kernel * (ra - la)
        charts[chart] += 1
    return total, charts


def run():
    ctx.prec = BITS
    print("C1B_BOB_PRODUCER — PROTOTYPE / NOT_BINDING")
    print("CONTRACT analysis/GLOBAL_AXIAL_C1B_BOB_BRIDGE_CONTRACT.md")
    print("LAMBDA_DOMAIN", L_LO, L_HI)
    print("BITS", BITS, "DEG", DEG, "STAGES", STAGES)
    print("PREDECLARED_PANEL_CEILING", PANEL_CEILING)
    first = None
    final_worst = None
    for label, nlam, panels in STAGES:
        unresolved = 0
        worst = None
        for ll, lr in _split(L_LO, L_HI, nlam):
            try:
                value, charts = _integrate(ll, lr, panels)
                good = value.upper() < 0
            except (ValueError, ZeroDivisionError):
                value = None
                charts = None
                good = False
            if not good:
                unresolved += 1
            if value is not None and (worst is None or value.upper() > worst[0]):
                worst = (value.upper(), ll, lr, value, charts)
        final_worst = worst
        print("C1B_BOB_STAGE", label, "lambda_boxes", nlam, "s_panels", panels,
              "unresolved", unresolved,
              "worst", None if worst is None else worst[1:])
        if unresolved == 0:
            first = label
            print("C1B_BOB_FIRST_PASS", label)
            break
    ok = first is not None
    print("LOGICAL_FINAL_C1B_BOB", "PASS" if ok else "UNRESOLVED",
          "first_pass", first,
          "worst", None if final_worst is None else final_worst[1:4])
    if not ok:
        raise SystemExit("UNRESOLVED")


if __name__ == "__main__":
    run()
