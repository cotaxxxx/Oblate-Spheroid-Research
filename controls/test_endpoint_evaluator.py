#!/usr/bin/env python3
"""Implementation-calling checks against pre-existing sphere expectations."""

import unittest

import mpmath as mp

from checker.oblate_axis_prototype import b_ob, boundary_energy_ob


class EndpointEvaluatorSphereControl(unittest.TestCase):
    DPs = 50

    def test_b_ob_calls_implementation_and_matches_exact_expectation(self):
        with mp.workdps(self.DPs):
            expected = mp.pi**2 / 32
            actual = b_ob(1, dps=self.DPs)
            self.assertLess(abs(actual - expected), mp.mpf("1e-40"))

    def test_boundary_energy_calls_implementation(self):
        with mp.workdps(self.DPs):
            expected = 3 * mp.pi**2 / 32 - mp.mpf("0.5")
            actual = boundary_energy_ob(1, dps=self.DPs)
            self.assertLess(abs(actual - expected), mp.mpf("1e-40"))


if __name__ == "__main__":
    unittest.main()
