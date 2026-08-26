#!/usr/bin/env python3
"""End-to-end interval producer/checker tests and fail-closed mutations."""

import copy
import hashlib
import json
import unittest

from flint import arb

from checker.endpoint_interval_checker import _series as checker_series
from checker.endpoint_interval_checker import verify_interval_record
from checker.endpoint_interval_checker import verify_interval_record_bytes
from checker.endpoint_interval_checker import verify_receipt_binding
from checker.endpoint_local_checker import VerificationError
from producer.endpoint_interval_producer import produce_record
from producer.endpoint_interval_producer import _series as producer_series


class EndpointIntervalCertificateCandidate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record = produce_record(bits=160, panels=1024, degree=50)

    @staticmethod
    def canonical_bytes(record):
        return (
            json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n"
        ).encode("utf-8")

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
        record_bytes = self.canonical_bytes(self.record)
        self.assertEqual(
            receipt["record_sha256"], hashlib.sha256(record_bytes).hexdigest()
        )
        self.assertEqual(
            receipt["source_commit"],
            self.record["provenance"]["source_commit"],
        )
        self.assertTrue(verify_receipt_binding(receipt, record_bytes))

    def test_noncanonical_record_bytes_are_rejected(self):
        with self.assertRaisesRegex(VerificationError, "not canonical"):
            verify_interval_record_bytes(self.canonical_bytes(self.record) + b"\n")

    def test_receipt_cannot_be_reused_for_another_record(self):
        record_bytes = self.canonical_bytes(self.record)
        receipt = verify_interval_record_bytes(record_bytes)
        other = copy.deepcopy(self.record)
        other["precision"]["producer_bits"] += 1
        with self.assertRaisesRegex(VerificationError, "SHA-256 mismatch"):
            verify_receipt_binding(receipt, self.canonical_bytes(other))

    def test_receipt_source_commit_is_independently_bound(self):
        record_bytes = self.canonical_bytes(self.record)
        receipt = verify_interval_record_bytes(record_bytes)
        receipt["source_commit"] = "0" * 40
        with self.assertRaisesRegex(VerificationError, "source commit mismatch"):
            verify_receipt_binding(receipt, record_bytes)

    def test_series_domain_is_fail_closed_at_and_above_one(self):
        for invalid_u in (arb(1), arb("1.2")):
            with self.subTest(u=invalid_u):
                with self.assertRaisesRegex(ValueError, "requires u < 1"):
                    producer_series(invalid_u, "Psi", 10)
                with self.assertRaisesRegex(VerificationError, "requires u < 1"):
                    checker_series(invalid_u, "Psi", 10)

    def test_series_domain_rejects_intervals_crossing_below_zero(self):
        invalid_u = arb("-0.1", "0.2")
        with self.assertRaisesRegex(ValueError, "requires u >= 0"):
            producer_series(invalid_u, "Psi", 10)
        with self.assertRaisesRegex(VerificationError, "requires u >= 0"):
            checker_series(invalid_u, "Psi", 10)

    def test_derivative_upper_chart_records_only_used_series(self):
        derivative = next(
            item for item in self.record["evaluations"]
            if item["label"] == "derivative_domain"
        )
        for cell in derivative["cells"]:
            if cell["chart"] == "u_upper":
                self.assertEqual(
                    {item["function"] for item in cell["series"]},
                    {"Psi", "Psi_prime"},
                )

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
