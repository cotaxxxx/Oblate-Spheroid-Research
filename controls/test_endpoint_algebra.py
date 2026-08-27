#!/usr/bin/env python3
"""Exact algebra controls for the endpoint-regular oblate kernel.

These controls use only fractions and polynomial identities. They do not call
an integrator or the prototype evaluator, and therefore precede the interval
implementation they will constrain.
"""

from fractions import Fraction
import unittest


LAMBDAS = (Fraction(1, 2), Fraction(3, 5), Fraction(16, 25))
DELTAS = (Fraction(0), Fraction(1, 16), Fraction(1, 4), Fraction(1, 2))


def quantities(lam, eps):
    lam2 = lam * lam
    a = 1 - lam2
    w2 = 1 - 2 * a * eps + a * eps * eps
    qhat = 2 - a * eps
    denominator = w2 * qhat
    gamma2 = lam2 * eps / denominator
    u = (2 - eps) * (1 - a * eps) ** 2 / denominator
    return a, w2, qhat, gamma2, u


class EndpointKernelExactAlgebra(unittest.TestCase):
    def test_endpoint_values(self):
        for lam in LAMBDAS:
            with self.subTest(lam=lam):
                _, _, _, gamma2_lo, _ = quantities(lam, Fraction(0))
                _, _, _, gamma2_hi, _ = quantities(lam, Fraction(2))
                self.assertEqual(gamma2_lo, 0)
                self.assertEqual(gamma2_hi, 1)

    def test_global_complement_identity(self):
        eps_samples = (
            Fraction(0),
            Fraction(1, 4),
            Fraction(1),
            Fraction(5, 4),
            Fraction(3, 2),
            Fraction(2),
        )
        for lam in LAMBDAS:
            for eps in eps_samples:
                with self.subTest(lam=lam, eps=eps):
                    lam2 = lam * lam
                    a, w2, qhat, gamma2, u = quantities(lam, eps)
                    self.assertEqual(
                        w2 * qhat - lam2 * eps,
                        (2 - eps) * (1 - a * eps) ** 2,
                    )
                    self.assertEqual(gamma2 + u, 1)
                    self.assertEqual(gamma2 * w2 * qhat, lam2 * eps)

    def test_prelimit_complement_reduces_to_endpoint_identity(self):
        eps_samples = (
            Fraction(0),
            Fraction(1, 4),
            Fraction(1),
            Fraction(5, 4),
            Fraction(3, 2),
            Fraction(2),
        )
        for lam in LAMBDAS:
            for eps in eps_samples:
                with self.subTest(lam=lam, eps=eps):
                    lam2 = lam * lam
                    a, w2, qhat, _, _ = quantities(lam, eps)
                    mu = 1 - eps
                    t = Fraction(1)
                    A = 1 - t * mu
                    q = 1 - mu * mu + lam2 * (mu - t) ** 2
                    general_complement = w2 * q - lam2 * A * A
                    general_factored = (
                        (1 - mu * mu) * ((1 - lam2) * mu + lam2 * t) ** 2
                    )
                    endpoint_factored_with_common_s2 = (
                        eps * (2 - eps) * (1 - a * eps) ** 2
                    )
                    self.assertEqual(q, eps * qhat)
                    self.assertEqual(general_complement, general_factored)
                    self.assertEqual(
                        general_factored,
                        endpoint_factored_with_common_s2,
                    )
                    self.assertEqual(
                        eps * (w2 * qhat - lam2 * eps),
                        endpoint_factored_with_common_s2,
                    )

    def test_internal_double_zero(self):
        for lam in LAMBDAS:
            with self.subTest(lam=lam):
                lam2 = lam * lam
                a = 1 - lam2
                eps0 = 1 / a
                self.assertGreater(eps0, 1)
                self.assertLess(eps0, 2)
                _, _, _, gamma2, u = quantities(lam, eps0)
                self.assertEqual(1 - a * eps0, 0)
                self.assertEqual(u, 0)
                self.assertEqual(gamma2, 1)

    def test_chart_seam(self):
        for lam in LAMBDAS:
            with self.subTest(lam=lam):
                lam2 = lam * lam
                _, _, _, gamma2, u = quantities(lam, Fraction(1))
                self.assertEqual(gamma2, 1 / (1 + lam2))
                self.assertEqual(u, lam2 / (1 + lam2))
                self.assertEqual(gamma2 + u, 1)

    def test_A_gamma_t_factorization(self):
        eps_samples = (
            Fraction(0),
            Fraction(1, 4),
            Fraction(1),
            Fraction(3, 2),
            Fraction(2),
        )
        for lam in LAMBDAS:
            for eps in eps_samples:
                with self.subTest(lam=lam, eps=eps):
                    lam2 = lam * lam
                    a = 1 - lam2
                    mu = 1 - eps
                    qhat = 2 - a * eps
                    bracket_from_derivative = mu * qhat + lam2 * eps
                    bracket_factored = (2 - eps) * (1 - a * eps)
                    self.assertEqual(bracket_from_derivative, bracket_factored)

    def test_prelimit_numerator_factorization(self):
        """Regress the exact identities used by the limit-exchange proof."""
        eps_samples = (
            Fraction(0),
            Fraction(1, 4),
            Fraction(1),
            Fraction(3, 2),
            Fraction(2),
        )
        for lam in LAMBDAS:
            for delta in DELTAS:
                for eps in eps_samples:
                    with self.subTest(lam=lam, delta=delta, eps=eps):
                        lam2 = lam * lam
                        mu = 1 - eps
                        t = 1 - delta
                        A = 1 - t * mu
                        q = 1 - mu * mu + lam2 * (mu - t) ** 2
                        d = eps - delta
                        H = (
                            (1 - eps) * (2 - eps)
                            + lam2
                            * (2 * eps - 2 * delta - eps * eps + delta * eps)
                        )
                        N = -mu * q - A * lam2 * (t - mu)
                        self.assertEqual(A, delta + (1 - delta) * eps)
                        self.assertEqual(q, eps * (2 - eps) + lam2 * d * d)
                        self.assertEqual(N, -eps * H)


if __name__ == "__main__":
    unittest.main()
