#!/usr/bin/env python3
"""End-to-end interval producer/checker tests and fail-closed mutations."""

import copy
import unittest

from flint import arb

from checker.endpoint_interval_checker import _series as checker_series
from checker.endpoint_interval_checker import verify_interval_record
from checker.endpoint_local_checker import VerificationError
from producer.endpoint_interval_producer import produce_record
from producer.endpoint_interval_producer import _series as producer_series


class EndpointIntervalCertificateCandidate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record = produce_record(bits=160, panels=1024, degree=50)

    def test_three_binding_signs_are_independently_reconstructed(self):
        receipt = verify_interval_record(copy.deepcopy(self.record))
        self.assertEqual(receipt["status"], "PASS")
        self.assertEqual(
            receipt["conclusion"],
            (
                "Conditional on the endpoint analytic and one-sided-limit "
                "identification lemmas, B_ob has exactly one zero "
                "in [5/8,33/50]."
            ),
        )
        self.assertEqual(len(receipt["conditional_on"]), 2)

    def test_series_domain_is_fail_closed_at_and_above_one(self):
        for invalid_u in (arb(1), arb("1.2")):
            with self.subTest(u=invalid_u):
                with self.assertRaisesRegex(ValueError, "requires u < 1"):
                    producer_series(invalid_u, "Psi", 10)
                with self.assertRaisesRegex(VerificationError, "requires u < 1"):
                    checker_series(invalid_u, "Psi", 10)

    def test_producer_reported_sum_is_not_trusted(self):
        record = copy.deepcopy(self.record)
        record["evaluations"][0]["reported_sum"] = {
            "midpoint": "0",
            "radius": "0",
        }
        with self.assertRaisesRegex(VerificationError, "reported sum"):
            verify_interval_record(record)

    def test_producer_cell_kernel_is_not_trusted(self):
        record = copy.deepcopy(self.record)
        record["evaluations"][1]["cells"][10]["kernel_enclosure"] = {
            "midpoint": "0",
            "radius": "0",
        }
        with self.assertRaisesRegex(VerificationError, "kernel"):
            verify_interval_record(record)

    def test_missing_derivative_series_is_rejected(self):
        record = copy.deepcopy(self.record)
        derivative = next(
            item for item in record["evaluations"]
            if item["label"] == "derivative_domain"
        )
        upper = next(cell for cell in derivative["cells"] if cell["chart"] == "u_upper")
        upper["series"] = [
            item for item in upper["series"]
            if item["function"] != "Psi_prime"
        ]
        with self.assertRaisesRegex(VerificationError, "series inventory"):
            verify_interval_record(record)

    def test_unused_enclosure_field_is_rejected(self):
        record = copy.deepcopy(self.record)
        record["evaluations"][0]["cells"][0][
            "lambda_derivative_enclosure"
        ] = {"midpoint": "0", "radius": "0"}
        with self.assertRaisesRegex(VerificationError, "field inventory"):
            verify_interval_record(record)

    def test_duplicate_evaluation_label_is_rejected(self):
        record = copy.deepcopy(self.record)
        record["evaluations"][2]["label"] = "left_endpoint"
        with self.assertRaisesRegex(VerificationError, "label inventory"):
            verify_interval_record(record)

    def test_label_purpose_mismatch_is_rejected(self):
        record = copy.deepcopy(self.record)
        record["evaluations"][2]["purpose"] = "B_ob"
        with self.assertRaisesRegex(VerificationError, "label/purpose"):
            verify_interval_record(record)

    def test_extra_top_level_key_is_rejected(self):
        record = copy.deepcopy(self.record)
        record["producer_pass"] = True
        with self.assertRaisesRegex(VerificationError, "top-level"):
            verify_interval_record(record)

    def test_control_pass_label_alone_is_insufficient(self):
        record = copy.deepcopy(self.record)
        first = record["evaluations"][0]["cells"][0]
        first["s_interval"][1] = "1/2048"
        with self.assertRaises(VerificationError):
            verify_interval_record(record)


if __name__ == "__main__":
    unittest.main()
