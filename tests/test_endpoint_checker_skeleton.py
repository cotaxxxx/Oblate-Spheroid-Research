#!/usr/bin/env python3
"""Tests for checker-owned controls and exact cell-cover validation."""

import copy
import subprocess
import sys
from fractions import Fraction
import unittest

from checker.endpoint_local_checker import (
    VerificationError,
    VerificationIncomplete,
    verification_layers,
    verify_exact_cell_cover,
    verify_record,
)
from checker.endpoint_local_controls import (
    CONTROL_NAMES,
    ControlFailure,
    run_exact_controls,
    verify_gamma_lambda_factorization,
    verify_quadrature_bookkeeping,
)


def valid_cells():
    return [
        {
            "ordinal": 0,
            "s_interval": ["0/1", "1/2"],
            "chart": "gamma_lower",
        },
        {
            "ordinal": 1,
            "s_interval": ["1/2", "1/1"],
            "chart": "gamma_lower",
        },
        {
            "ordinal": 2,
            "s_interval": ["1/1", "5/4"],
            "chart": "u_upper",
        },
        {
            "ordinal": 3,
            "s_interval": ["5/4", "sqrt2"],
            "chart": "u_upper",
        },
    ]


class CheckerOwnedEndpointControls(unittest.TestCase):
    def test_all_seven_exact_control_families_pass(self):
        self.assertEqual(
            run_exact_controls(),
            {name: "PASS" for name in CONTROL_NAMES},
        )

    def test_sign_reversed_gamma_lambda_factorization_is_rejected(self):
        lam = Fraction(5, 8)
        eps = Fraction(1, 2)
        lam2 = lam * lam
        a = 1 - lam2
        w2 = 1 - 2 * a * eps + a * eps * eps
        qhat = 2 - a * eps
        sign_reversed = (
            (2 - eps)
            * (1 - a * eps)
            * ((1 + lam2) * eps - 1)
            / (lam * w2 * qhat)
        )
        with self.assertRaisesRegex(
            ControlFailure,
            "gamma_lambda factorization failed",
        ):
            verify_gamma_lambda_factorization(lam, eps, sign_reversed)

    def test_wrong_quadrature_bookkeeping_is_rejected(self):
        with self.assertRaisesRegex(
            ControlFailure,
            "quadrature bookkeeping failed",
        ):
            verify_quadrature_bookkeeping(Fraction(3, 4))

    def test_package_import_does_not_load_prototype_or_mpmath(self):
        code = (
            "import checker, sys; "
            "assert 'mpmath' not in sys.modules; "
            "assert 'checker.oblate_axis_prototype' not in sys.modules"
        )
        subprocess.run([sys.executable, "-c", code], check=True)

    def test_exact_cover_accepts_unique_seam_and_sqrt2_terminal(self):
        verify_exact_cell_cover(valid_cells())

    def test_exact_cover_rejects_gap(self):
        cells = valid_cells()
        cells[1]["s_interval"][0] = "3/5"
        with self.assertRaisesRegex(VerificationError, "gap, overlap"):
            verify_exact_cell_cover(cells)

    def test_exact_cover_rejects_overlap(self):
        cells = valid_cells()
        cells[2]["s_interval"][0] = "3/4"
        with self.assertRaisesRegex(VerificationError, "gap, overlap"):
            verify_exact_cell_cover(cells)

    def test_exact_cover_rejects_missing_seam(self):
        cells = valid_cells()
        cells[1]["s_interval"][1] = "5/4"
        cells.pop(2)
        cells[2]["ordinal"] = 2
        with self.assertRaises(VerificationError):
            verify_exact_cell_cover(cells)

    def test_exact_cover_rejects_decimal_endpoint(self):
        cells = valid_cells()
        cells[-1]["s_interval"][1] = "1.41421356237"
        with self.assertRaisesRegex(VerificationError, "invalid rational"):
            verify_exact_cell_cover(cells)

    def test_exact_cover_rejects_wrong_chart(self):
        cells = valid_cells()
        cells[2]["chart"] = "gamma_lower"
        with self.assertRaisesRegex(VerificationError, "wrong chart"):
            verify_exact_cell_cover(cells)

    def test_checker_is_deliberately_fail_closed(self):
        record = {
            "precision": {"producer_bits": 128, "checker_bits": 192},
            "evaluations": [{"cells": copy.deepcopy(valid_cells())}],
        }
        with self.assertRaisesRegex(
            VerificationIncomplete,
            "interval arithmetic reconstruction is not implemented",
        ):
            verify_record(record)

    def test_trust_report_names_checked_and_unchecked_layers(self):
        layers = verification_layers()
        self.assertIn("controls_check", layers)
        self.assertIn("controls_do_not_check", layers)
        self.assertIn("checker_reconstructs", layers)
        self.assertIn("checker_does_not_reuse", layers)


if __name__ == "__main__":
    unittest.main()
