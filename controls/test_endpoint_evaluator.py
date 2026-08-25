#!/usr/bin/env python3
"""Implementation-calling checks against pre-existing sphere expectations."""

import unittest

import mpmath as mp

from checker.oblate_axis_prototype import b_ob, boundary_energy_ob, g_axis_ob


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

    def test_g_axis_ob_accepts_t_equal_one_and_delegates_to_b_ob(self):
        with mp.workdps(self.DPs):
            actual = g_axis_ob(1, 1, dps=self.DPs)
            expected = b_ob(1, dps=self.DPs)
            self.assertLess(abs(actual - expected), mp.mpf("1e-40"))

    def test_g_axis_ob_rejects_inputs_outside_documented_domain(self):
        for invalid_t in (-1, mp.mpf("1.000001")):
            with self.subTest(t=invalid_t):
                with self.assertRaisesRegex(
                    ValueError, r"t must satisfy -1 < t <= 1"
                ):
                    g_axis_ob(invalid_t, 1, dps=self.DPs)

    def test_b_ob_is_stable_at_previously_failing_precisions(self):
        values = {}
        for dps in (30, 50, 80):
            with self.subTest(dps=dps):
                value = b_ob("0.9", dps=dps)
                self.assertTrue(mp.isfinite(value))
                values[dps] = value
        with mp.workdps(80):
            self.assertLess(abs(values[30] - values[80]), mp.mpf("1e-25"))
            self.assertLess(abs(values[50] - values[80]), mp.mpf("1e-45"))


if __name__ == "__main__":
    unittest.main()
