#!/usr/bin/env python3
"""Independent sphere controls fixed before the production evaluator exists."""

import math
import unittest


class SphereControls(unittest.TestCase):
    def test_b_ob_exact_decimal_control(self):
        expected_prefix = "0.3084251375340424"
        value = math.pi**2 / 32.0
        self.assertTrue(format(value, ".16f").startswith(expected_prefix))

    def test_gamma_t_numerator_identity(self):
        # Deterministic algebraic samples for
        # q = 1-mu^2+(mu-t)^2 at lambda=1.
        for mu, t in [(-0.8, 0.2), (-0.1, 0.7), (0.3, 0.4), (0.9, 1.0)]:
            q = 1.0 - mu * mu + (mu - t) ** 2
            lhs = -mu * q - (1.0 - t * mu) * (t - mu)
            rhs = -t * (1.0 - mu * mu)
            self.assertAlmostEqual(lhs, rhs, places=14)


if __name__ == "__main__":
    unittest.main()
