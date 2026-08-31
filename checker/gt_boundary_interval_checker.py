#!/usr/bin/env python3
"""Independent checker for gt_boundary_ob producer records.

Imports neither gt_boundary_interval_producer nor its kernel. Reconstructs the
two-chart endpoint-regular density and requires the full-domain enclosure to
have upper endpoint < 0. Reported point expectations are explicitly non-gating.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
from math import comb
from pathlib import Path

from flint import arb, ctx


class VerificationError(RuntimeError):
    pass


def _point(x):
    if isinstance(x, Fraction):
        return arb(x.numerator) / x.denominator
    return arb(x)


def _box(left, right):
    return arb((left + right) / 2, (right - left) / 2)


def _clamp_nonnegative(x):
    lo = max(arb(0), x.lower())
    hi = max(arb(0), x.upper())
    return _box(lo, hi)


def _power(x, n):
    out = arb(1)
    for _ in range(n):
        out *= x
    return out


def _zero_to_upper(x):
    hi = max(arb(0), x.upper())
    return arb(hi / 2, hi / 2)


def _series(u, name, degree):
    if not u.upper() < 1:
        raise VerificationError(f"{name} requires u<1")
    if name == "Psi":
        partial = arb(0)
        for n in range(degree + 1):
            c = Fraction(comb(2*n, n), 4**n * (2*n + 1))
            partial += _point(c) * _power(u, n)
        n = degree + 1
        c = Fraction(comb(2*n, n), 4**n * (2*n + 1))
        nxt = _point(c) * _power(u, n)
    elif name == "Psi_prime":
        partial = arb(0)
        for n in range(1, degree + 1):
            c = Fraction(n * comb(2*n, n), 4**n * (2*n + 1))
            partial += _point(c) * _power(u, n-1)
        n = degree + 1
        c = Fraction(n * comb(2*n, n), 4**n * (2*n + 1))
        nxt = _point(c) * _power(u, n-1)
    else:
        raise VerificationError("unsupported series")
    return partial + _zero_to_upper(nxt / (1-u))


def _kernel(s, lam, chart, degree):
    e = s*s
    lam2 = lam*lam
    lam3 = lam2*lam
    a = 1-lam2
    h = 1-a*e
    w2 = 1-2*a*e+a*e*e
    w = w2.sqrt()
    qh = 2-a*e
    qhs = qh.sqrt()
    qh32 = qh*qhs
    qh52 = qh*qh32
    gap = 2-e
    if chart == "u_upper":
        gap = _clamp_nonnegative(gap)
    c = gap*h
    d = gap*(1-2*a*e)
    gamma = lam*s/(w*qhs)

    if chart == "gamma_lower":
        u = 1-gamma*gamma
        alpha = gamma.acos()
        r = alpha/u.sqrt()
        rg = (gamma*r-1)/u
        return (
            -4*(1-e)*lam*r*c/(w*qh32)
            -2*s*lam2*rg*c*c/(w2*qh*qh*qh)
            -2*e*lam3*r*d/(w*qh52)
        )

    u = _clamp_nonnegative(gap*h*h/(w2*qh))
    psi = _series(u, "Psi", degree)
    psip = _series(u, "Psi_prime", degree)
    return (
        -4*(1-e)*lam*psi*c/(w*qh32)
        +4*e*lam3*psip*c*c/(w*w2*qh*qh*qh32)
        -2*e*lam3*psi*d/(w*qh52)
    )


def _parse_endpoint(text):
    if text == "sqrt2":
        return arb(2).sqrt()
    return _point(Fraction(text))


def verify(record):
    if record.get("schema") != "bg-oblate-spheroid.gt-boundary-producer-record.v1":
        raise VerificationError("schema mismatch")
    contract = record.get("contract", {})
    if contract.get("lambda_domain") != ["5/8", "33/50"]:
        raise VerificationError("lambda domain mismatch")
    if contract.get("required_sign") != "NEG":
        raise VerificationError("required sign mismatch")
    if record.get("expectations", {}).get("status") != "REPORTED_NOT_GATING":
        raise VerificationError("expectations must be non-gating")

    evaluation = record["evaluation"]
    cells = evaluation["cells"]
    bits = int(record["precision"]["producer_bits"])
    ctx.prec = max(bits, 192)
    lam = _box(_point(Fraction(5,8)), _point(Fraction(33,50)))
    total = arb(0)
    previous_right = None
    for ordinal, cell in enumerate(cells):
        if cell["ordinal"] != ordinal:
            raise VerificationError("cell ordinal mismatch")
        left_text, right_text = cell["s_interval"]
        if previous_right is not None and left_text != previous_right:
            raise VerificationError("s-cell cover has gap/overlap ordering error")
        previous_right = right_text
        left = _parse_endpoint(left_text)
        right = _parse_endpoint(right_text)
        chart = cell["chart"]
        expected_chart = "gamma_lower" if right_text != "sqrt2" and right <= 1 else "u_upper"
        if chart != expected_chart:
            raise VerificationError("chart mismatch")
        s = _box(left, right)
        value = _kernel(s, lam, chart, 50)
        total += value * (right-left)

    if cells[0]["s_interval"][0] != "0/1" or previous_right != "sqrt2":
        raise VerificationError("s-domain cover mismatch")
    if not total.upper() < 0:
        raise VerificationError("GATING FAIL: full-domain upper endpoint is not < 0")
    return total


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("record", type=Path)
    args = parser.parse_args()
    record = json.loads(args.record.read_text(encoding="utf-8"))
    total = verify(record)
    print("PASS")
    print("checker enclosure:", total)


if __name__ == "__main__":
    main()
