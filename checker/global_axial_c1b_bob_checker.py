#!/usr/bin/env python3
"""C1b B_ob<0 bridge checker on [9/20,5/8].

Separately transcribed interval computation. No producer import.
CHECKER_KERNEL=TRANSCRIBED_COPY_NOT_INDEPENDENT_DERIVATION
INDEPENDENCE_SCOPE=PRECISION/PARTITION/GATING
"""
from fractions import Fraction
from math import isqrt
from flint import arb, ctx

from checker.endpoint_interval_checker import _box, _clamp_nonnegative, _point, _series

BITS = 192
DEG = 50
SQRT2 = "sqrt2"
L_LO = Fraction(9, 20)
L_HI = Fraction(5, 8)
STAGES = (("B0", 16, 1024), ("B1", 32, 2048), ("B2", 64, 4096))
PANEL_CEILING = 344064


def _partition(panels):
    root = arb(2).sqrt()
    rational_end = isqrt(2 * panels * panels)
    values = [Fraction(i, panels) for i in range(panels + 1)]
    values.extend(Fraction(i, panels) for i in range(panels + 1, rational_end + 1))
    return values + [SQRT2], root


def _split(a, b, n):
    h = (b-a)/n
    return [(a+i*h, a+(i+1)*h) for i in range(n)]


def _kernel(s, lam, chart):
    e = s*s
    lam2 = lam*lam
    a = 1-lam2
    h = 1-a*e
    w2 = 1-2*a*e+a*e*e
    qhat = 2-a*e
    gap = 2-e
    if chart == "u_upper":
        gap = _clamp_nonnegative(gap)
    gamma = lam*s/(w2.sqrt()*qhat.sqrt())
    qhat_3_2 = qhat*qhat.sqrt()
    p = 2*lam*e*gap*h/(w2.sqrt()*qhat_3_2)
    if chart == "gamma_lower":
        u = 1-gamma*gamma
        alpha = gamma.acos()
        psi = alpha/u.sqrt()
        return -s*(1-e)*alpha*alpha + p*psi
    u = _clamp_nonnegative(gap*h*h/(w2*qhat))
    phi, _, _ = _series(u, "Phi", DEG, clamped_nonnegative=True)
    psi, _, _ = _series(u, "Psi", DEG, clamped_nonnegative=True)
    return -s*(1-e)*phi + p*psi


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
        total += _kernel(s, lam, chart)*(ra-la)
        charts[chart] += 1
    return total, charts


def verify():
    ctx.prec = BITS
    print("C1B_BOB_CHECKER — PROTOTYPE / NOT_BINDING")
    print("CHECKER_KERNEL TRANSCRIBED_COPY_NOT_INDEPENDENT_DERIVATION")
    print("INDEPENDENCE_SCOPE PRECISION/PARTITION/GATING")
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
    verify()
