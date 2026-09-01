#!/usr/bin/env python3
"""Exact-rational transcription audit for the C0a four-group regrouping.

RAW_AUDIT_TRANSCRIPTION_CHECK / REPORT_ONLY / NOT_GATING / NOT_BINDING.

This is not a formal symbolic proof.  It is a deterministic exact-Fraction
check designed to catch transcription/sign/power mistakes before any Arb
producer/checker implementation is changed.
"""
from fractions import Fraction as F


def legacy_density(mu, A, R, Rg, Rgg, Rggg, gt, gtt, gttt, gtttt):
    Ctt = Rgg * gt**3 + 3 * Rg * gt * gtt + R * gttt
    Cttt = (
        Rggg * gt**4
        + 6 * Rgg * gt**2 * gtt
        + 3 * Rg * gtt**2
        + 4 * Rg * gt * gttt
        + R * gtttt
    )
    return 8 * mu * Ctt - 2 * A * Cttt


def grouped_density(mu, A, R, Rg, Rgg, Rggg, gt, gtt, gttt, gtttt):
    K0 = 8 * mu * gttt - 2 * A * gtttt
    K1 = 24 * mu * gt * gtt - 2 * A * (3 * gtt**2 + 4 * gt * gttt)
    K2 = 8 * mu * gt**3 - 12 * A * gt**2 * gtt
    K3 = -2 * A * gt**4
    return R * K0 + Rg * K1 + Rgg * K2 + Rggg * K3


def derivative_bundle(lam, w, q, N, M, P, Q):
    # Represent q^(1/2) by an independent exact rational r with q=r^2 in the
    # test generator, so all powers remain exact Fractions.
    r = sqrt_fraction(q)
    gt = lam * N / (w * q * r)
    gtt = lam * M / (w * q**2 * r)
    gttt = lam * P / (w * q**3 * r)
    gtttt = lam * Q / (w * q**4 * r)
    return gt, gtt, gttt, gtttt


def common_denominator_K(mu, A, lam, w, q, N, M, P, Q):
    r = sqrt_fraction(q)
    K0 = lam * (8 * mu * P * q - 2 * A * Q) / (w * q**4 * r)
    K1 = lam**2 * (24 * mu * N * M * q - 6 * A * M**2 - 8 * A * N * P) / (w**2 * q**5)
    K2 = lam**3 * (8 * mu * N**3 * q - 12 * A * N**2 * M) / (w**3 * q**5 * r)
    K3 = -2 * A * lam**4 * N**4 / (w**4 * q**6)
    return K0, K1, K2, K3


def direct_K(mu, A, gt, gtt, gttt, gtttt):
    return (
        8 * mu * gttt - 2 * A * gtttt,
        24 * mu * gt * gtt - 2 * A * (3 * gtt**2 + 4 * gt * gttt),
        8 * mu * gt**3 - 12 * A * gt**2 * gtt,
        -2 * A * gt**4,
    )


def sqrt_fraction(x):
    import math

    n = x.numerator
    d = x.denominator
    rn = math.isqrt(n)
    rd = math.isqrt(d)
    if rn * rn != n or rd * rd != d:
        raise ValueError("audit generator requires q to be a rational square")
    return F(rn, rd)


def deterministic_cases():
    # q values are rational squares so the derivative formulas are checked
    # without floating point or algebraic-number dependencies.
    qs = [F(1, 4), F(4, 9), F(9, 16), F(25, 36)]
    vals = [F(1, 7), F(2, 5), F(3, 8), F(5, 9), F(7, 11)]
    signed = [F(-5, 7), F(-2, 9), F(1, 6), F(4, 7)]
    idx = 0
    for q in qs:
        for mu in signed:
            A = vals[idx % len(vals)]
            lam = vals[(idx + 1) % len(vals)]
            w = vals[(idx + 2) % len(vals)] + 1
            N = signed[(idx + 1) % len(signed)]
            M = signed[(idx + 2) % len(signed)]
            P = signed[(idx + 3) % len(signed)]
            Q = signed[idx % len(signed)] + F(1, 13)
            R = vals[(idx + 3) % len(vals)]
            Rg = signed[idx % len(signed)]
            Rgg = signed[(idx + 1) % len(signed)]
            Rggg = signed[(idx + 2) % len(signed)]
            yield (mu, A, lam, w, q, N, M, P, Q, R, Rg, Rgg, Rggg)
            idx += 1


def main():
    print("C0A FOUR-GROUP RAW AUDIT — EXACT FRACTION / REPORT_ONLY / NOT_GATING")
    count = 0
    for case in deterministic_cases():
        mu, A, lam, w, q, N, M, P, Q, R, Rg, Rgg, Rggg = case
        gt, gtt, gttt, gtttt = derivative_bundle(lam, w, q, N, M, P, Q)

        old = legacy_density(mu, A, R, Rg, Rgg, Rggg, gt, gtt, gttt, gtttt)
        new = grouped_density(mu, A, R, Rg, Rgg, Rggg, gt, gtt, gttt, gtttt)
        if old != new:
            raise SystemExit(f"FAIL eight-term/grouped identity at case {count}: {old-new}")

        kd = direct_K(mu, A, gt, gtt, gttt, gtttt)
        kc = common_denominator_K(mu, A, lam, w, q, N, M, P, Q)
        if kd != kc:
            raise SystemExit(f"FAIL common-denominator K identity at case {count}: {tuple(a-b for a,b in zip(kd,kc))}")

        count += 1

    print("PASS exact_fraction_cases", count)
    print("PASS eight_term_equals_four_group")
    print("PASS K0_K1_K2_K3_common_denominators")
    print("STATUS TRANSCRIPTION_AUDIT_PASS / NOT_FORMAL_SYMBOLIC_PROOF / NOT_BINDING")


if __name__ == "__main__":
    main()
