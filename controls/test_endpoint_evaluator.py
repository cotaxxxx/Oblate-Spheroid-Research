#!/usr/bin/env python3
"""Implementation-calling checks against pre-existing sphere expectations."""

from fractions import Fraction
import unittest
from unittest.mock import patch

import mpmath as mp

from checker.endpoint_local_controls import run_quadrature_bookkeeping_control
from checker.endpoint_local_controls import ControlFailure
import checker.oblate_axis_prototype as prototype
from checker.oblate_axis_prototype import (
    b_ob,
    boundary_energy_ob,
    g_axis_ob,
    quadrature_bookkeeping_ob,
)


class EndpointEvaluatorSphereControl(unittest.TestCase):
    DPs = 50

    def test_quadrature_bookkeeping_calls_transformed_integration_path(self):
        def implementation_candidate():
            actual = quadrature_bookkeeping_ob(dps=self.DPs)
            return Fraction(mp.nstr(actual, n=self.DPs))

        result = run_quadrature_bookkeeping_control(
            implementation_candidate,
            Fraction(1, 10**40),
        )
        self.assertEqual(result, {"quadrature_bookkeeping": "PASS"})

    def test_shared_weight_mutation_is_detected(self):
        with patch.object(
            prototype,
            "_transformed_cone_jacobian_weight",
            side_effect=lambda s: s**2,
        ):
            with self.assertRaises(ControlFailure):
                run_quadrature_bookkeeping_control(
                    lambda: Fraction(
                        mp.nstr(
                            prototype.quadrature_bookkeeping_ob(dps=self.DPs),
                            n=self.DPs,
                        )
                    ),
                    Fraction(1, 10**40),
                )

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

    def test_g_axis_ob_is_stable_at_previously_failing_precisions(self):
        values = {}
        for dps in (30, 50, 80):
            with self.subTest(dps=dps):
                value = g_axis_ob("0.99", "0.63", dps=dps)
                self.assertTrue(mp.isfinite(value))
                values[dps] = value
        with mp.workdps(80):
            self.assertLess(abs(values[30] - values[80]), mp.mpf("1e-25"))
            self.assertLess(abs(values[50] - values[80]), mp.mpf("1e-45"))

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
