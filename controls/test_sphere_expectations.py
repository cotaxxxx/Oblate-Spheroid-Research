#!/usr/bin/env python3
"""Independent sphere expectations fixed before an evaluator exists."""

import math
import unittest


class SphereExpectations(unittest.TestCase):
    def test_b_ob_exact_decimal_expectation(self):
        expected_prefix = "0.3084251375340424"
        value = math.pi**2 / 32.0
        self.assertTrue(format(value, ".16f").startswith(expected_prefix))

    def test_gamma_t_numerator_expectation(self):
        # This checks a fixed identity only. It does not call an implementation
        # and is therefore an expectation test, not a control test.
        for mu, t in [(-0.8, 0.2), (-0.1, 0.7), (0.3, 0.4), (0.9, 1.0)]:
            q = 1.0 - mu * mu + (mu - t) ** 2
            lhs = -mu * q - (1.0 - t * mu) * (t - mu)
            rhs = -t * (1.0 - mu * mu)
            self.assertAlmostEqual(lhs, rhs, places=14)


if __name__ == "__main__":
    unittest.main()
