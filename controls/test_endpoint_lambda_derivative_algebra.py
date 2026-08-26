#!/usr/bin/env python3
"""Exact algebra controls for the lambda derivative endpoint kernel.

These controls precede and do not import the future interval implementation.
All calculations use Fraction arithmetic.
"""

from fractions import Fraction
from math import comb
import unittest


LAMBDAS = (
    Fraction(1, 2),
    Fraction(3, 5),
    Fraction(5, 8),
    Fraction(16, 25),
    Fraction(13, 20),
)

EPSILONS = (
    Fraction(1, 4),
    Fraction(1),
    Fraction(5, 4),
    Fraction(3, 2),
    Fraction(7, 4),
)


def algebra(lam, eps):
    lam2 = lam * lam
    a = 1 - lam2
    h = 1 - a * eps
    w = 1 - 2 * a * eps + a * eps * eps
    q = 2 - a * eps
    w_lam = 2 * lam * eps * (2 - eps)
    q_lam = 2 * lam * eps
    h_lam = 2 * lam * eps
    denominator = w * q
    gamma2 = lam2 * eps / denominator
    u = (2 - eps) * h * h / denominator
    denominator_lam = w_lam * q + w * q_lam
    gamma2_lam = (
        2 * lam * eps * denominator
        - lam2 * eps * denominator_lam
    ) / (denominator * denominator)
    numerator_lam = 2 * (2 - eps) * h * h_lam
    u_lam = (
        numerator_lam * denominator
        - (2 - eps) * h * h * denominator_lam
    ) / (denominator * denominator)
    r = (
        1 / lam
        - lam * eps * (2 - eps) / w
        - lam * eps / q
    )
    j_product = (
        h
        + lam * h_lam
        - lam * h * w_lam / (2 * w)
        - 3 * lam * h * q_lam / (2 * q)
    )
    j_factored = (
        h
        + 2 * lam2 * eps
        - lam2 * h * eps * (2 - eps) / w
        - 3 * lam2 * h * eps / q
    )
    return {
        "a": a,
        "h": h,
        "w": w,
        "q": q,
        "gamma2": gamma2,
        "u": u,
        "gamma2_lam": gamma2_lam,
        "u_lam": u_lam,
        "r": r,
        "j_product": j_product,
        "j_factored": j_factored,
    }


class EndpointLambdaDerivativeExactAlgebra(unittest.TestCase):
    def test_gamma_squared_and_u_derivatives_use_same_R(self):
        for lam in LAMBDAS:
            for eps in EPSILONS:
                with self.subTest(lam=lam, eps=eps):
                    data = algebra(lam, eps)
                    self.assertEqual(
                        data["gamma2_lam"],
                        2 * data["gamma2"] * data["r"],
                    )
                    self.assertEqual(
                        data["u_lam"],
                        -2 * data["gamma2"] * data["r"],
                    )
                    self.assertEqual(
                        data["gamma2_lam"] + data["u_lam"],
                        0,
                    )

    def test_P_lambda_product_rule_has_no_division_by_H(self):
        for lam in LAMBDAS:
            for eps in EPSILONS:
                with self.subTest(lam=lam, eps=eps):
                    data = algebra(lam, eps)
                    self.assertEqual(data["j_product"], data["j_factored"])

    def test_internal_double_zero_is_termwise_regular(self):
        for lam in LAMBDAS:
            eps0 = 1 / (1 - lam * lam)
            with self.subTest(lam=lam, eps0=eps0):
                data = algebra(lam, eps0)
                self.assertEqual(data["h"], 0)
                self.assertEqual(data["u"], 0)
                self.assertEqual(data["gamma2"], 1)
                self.assertEqual(data["r"], 0)
                self.assertEqual(data["u_lam"], 0)
                self.assertEqual(
                    data["j_factored"],
                    2 * lam * lam * eps0,
                )

    def test_upper_endpoint_R_vanishes_exactly(self):
        for lam in LAMBDAS:
            with self.subTest(lam=lam):
                data = algebra(lam, Fraction(2))
                self.assertEqual(data["gamma2"], 1)
                self.assertEqual(data["r"], 0)
                self.assertEqual(data["gamma2_lam"], 0)
                self.assertEqual(data["u_lam"], 0)

    def test_Psi_prime_at_zero_is_one_sixth(self):
        n = 1
        c1 = Fraction(comb(2 * n, n), 4**n * (2 * n + 1))
        self.assertEqual(n * c1, Fraction(1, 6))


if __name__ == "__main__":
    unittest.main()
