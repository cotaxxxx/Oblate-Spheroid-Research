#!/usr/bin/env python3
"""Independent sphere expectations and implementation-connected controls."""

import math
from pathlib import Path
import sys
import unittest

import mpmath as mp

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from axial_endpoint_ob import b_ob


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


class SphereImplementationControl(unittest.TestCase):
    def test_b_ob_sphere_control_calls_implementation(self):
        with mp.workdps(60):
            expected = mp.pi**2 / 32
            actual = b_ob(mp.mpf("1"), dps=60)
            self.assertLess(abs(actual - expected), mp.mpf("1e-50"))


class BoundarySignDiagnostics(unittest.TestCase):
    def test_expected_boundary_signs(self):
        # Diagnostic targets only; these are not certification claims.
        self.assertLess(b_ob(mp.mpf("0.60"), dps=50), 0)
        self.assertGreater(b_ob(mp.mpf("0.70"), dps=50), 0)


if __name__ == "__main__":
    unittest.main()
