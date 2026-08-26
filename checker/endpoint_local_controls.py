#!/usr/bin/env python3
"""Checker-owned exact controls for the endpoint-local verification path.

Evidence class: NOT_BINDING.
Derivation class: PROTOTYPE / NOT_AUDITED.

This module uses exact Fraction arithmetic only. It does not import the
producer, prototype evaluator, quadrature code, or python-flint.
"""

from fractions import Fraction


CONTROL_NAMES = (
    "endpoint_values",
    "global_complement",
    "internal_double_zero",
    "seam_rational_targets",
    "A_gamma_t_factorization",
    "gamma_lambda_factorization",
)

CONTROL_LAMBDAS = (
    Fraction(1, 2),
    Fraction(3, 5),
    Fraction(5, 8),
    Fraction(16, 25),
    Fraction(13, 20),
)


class ControlFailure(ArithmeticError):
    pass


def _quantities(lam: Fraction, eps: Fraction):
    lam2 = lam * lam
    a = 1 - lam2
    w2 = 1 - 2 * a * eps + a * eps * eps
    qhat = 2 - a * eps
    denominator = w2 * qhat
    if denominator <= 0:
        raise ControlFailure("nonpositive exact denominator")
    gamma2 = lam2 * eps / denominator
    u = (2 - eps) * (1 - a * eps) ** 2 / denominator
    return a, w2, qhat, gamma2, u


def run_exact_controls():
    result = {name: "PASS" for name in CONTROL_NAMES}
    eps_samples = (
        Fraction(0),
        Fraction(1, 4),
        Fraction(1),
        Fraction(5, 4),
        Fraction(3, 2),
        Fraction(2),
    )

    for lam in CONTROL_LAMBDAS:
        lam2 = lam * lam
        a = 1 - lam2

        *_, gamma2_lo, _ = _quantities(lam, Fraction(0))
        *_, gamma2_hi, _ = _quantities(lam, Fraction(2))
        if gamma2_lo != 0 or gamma2_hi != 1:
            raise ControlFailure("endpoint-value identity failed")

        for eps in eps_samples:
            _, w2, qhat, gamma2, u = _quantities(lam, eps)
            complement = (2 - eps) * (1 - a * eps) ** 2
            if w2 * qhat - lam2 * eps != complement:
                raise ControlFailure("global complement identity failed")
            if gamma2 + u != 1:
                raise ControlFailure("gamma2 + u identity failed")

            mu = 1 - eps
            derivative_bracket = mu * qhat + lam2 * eps
            factored_bracket = (2 - eps) * (1 - a * eps)
            if derivative_bracket != factored_bracket:
                raise ControlFailure("A*gamma_t factorization failed")

            r_log = (
                1 / lam
                - lam * eps * (2 - eps) / w2
                - lam * eps / qhat
            )
            r_factored = -(
                (2 - eps)
                * (1 - a * eps)
                * ((1 + lam2) * eps - 1)
                / (lam * w2 * qhat)
            )
            if r_log != r_factored:
                raise ControlFailure("gamma_lambda factorization failed")

        eps0 = 1 / a
        if not (1 < eps0 < 2):
            raise ControlFailure("internal-zero location outside upper chart")
        *_, gamma2_zero, u_zero = _quantities(lam, eps0)
        if u_zero != 0 or gamma2_zero != 1:
            raise ControlFailure("internal double-zero identity failed")

        *_, gamma2_seam, u_seam = _quantities(lam, Fraction(1))
        if gamma2_seam != 1 / (1 + lam2):
            raise ControlFailure("gamma2 seam target failed")
        if u_seam != lam2 / (1 + lam2):
            raise ControlFailure("u seam target failed")

    return result
