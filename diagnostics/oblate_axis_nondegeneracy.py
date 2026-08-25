#!/usr/bin/env python3
"""Non-binding axial nondegeneracy diagnostic for the oblate spheroid.

Evidence class: DIAGNOSTIC_ONLY / NOT_BINDING.
Derivation class: HIGH_PRECISION.

This script estimates A_ob'(lambda_axis_ob) and the cubic coefficient C_ob in

    g_axis_ob(t, lambda_axis_ob) = A_ob*t + C_ob*t^3 + O(t^5).

It uses centered differences and Richardson extrapolation.  It does not
produce a certified enclosure or a uniqueness result.
"""

import mpmath as mp

from checker.oblate_axis_prototype import g_axis_ob


LAMBDA_AXIS_OB = mp.mpf("0.4079588603009463642491058701855256993")
DPS = 50


def centered_slope(lam, h):
    return (g_axis_ob(h, lam, dps=DPS) - g_axis_ob(-h, lam, dps=DPS)) / (2 * h)


def richardson(values):
    rows = []
    for k, value in enumerate(values):
        row = [value]
        for j in range(1, k + 1):
            factor = mp.mpf(4) ** j
            row.append(row[j - 1] + (row[j - 1] - rows[k - 1][j - 1]) / (factor - 1))
        rows.append(row)
    return rows


def a_ob(lam, h0=mp.mpf("0.03"), levels=4):
    slopes = [centered_slope(lam, h0 / 2**k) for k in range(levels)]
    return richardson(slopes)[-1][-1]


def transverse_lambda_sequence():
    h0 = mp.mpf("0.004")
    estimates = []
    for k in range(4):
        h = h0 / 2**k
        estimate = (a_ob(LAMBDA_AXIS_OB + h) - a_ob(LAMBDA_AXIS_OB - h)) / (2 * h)
        estimates.append(estimate)
    return estimates, richardson(estimates)[-1][-1]


def cubic_sequence():
    h0 = mp.mpf("0.04")
    slopes = [centered_slope(LAMBDA_AXIS_OB, h0 / 2**k) for k in range(6)]
    estimates = []
    for k in range(5):
        h = h0 / 2**k
        estimates.append(4 * (slopes[k] - slopes[k + 1]) / (3 * h * h))
    return estimates, richardson(estimates)[-1][-1]


def main():
    with mp.workdps(DPS):
        a_axis = a_ob(LAMBDA_AXIS_OB, levels=5)
        aprime_values, aprime = transverse_lambda_sequence()
        cubic_values, cubic = cubic_sequence()
        branch_ratio = -aprime / cubic

        print("EVIDENCE_CLASS DIAGNOSTIC_ONLY / NOT_BINDING")
        print("DERIVATION_CLASS HIGH_PRECISION")
        print("DPS", DPS)
        print("lambda_axis_ob", mp.nstr(LAMBDA_AXIS_OB, 45))
        print("A_ob_at_axis", mp.nstr(a_axis, 30))
        for k, value in enumerate(aprime_values):
            print("A_ob_prime_raw", k, mp.nstr(value, 30))
        print("A_ob_prime_richardson", mp.nstr(aprime, 40))
        for k, value in enumerate(cubic_values):
            print("C_ob_raw", k, mp.nstr(value, 30))
        print("C_ob_richardson", mp.nstr(cubic, 40))
        print("minus_Aprime_over_C", mp.nstr(branch_ratio, 40))


if __name__ == "__main__":
    main()
