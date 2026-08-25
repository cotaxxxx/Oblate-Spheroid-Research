#!/usr/bin/env python3
"""Structural checks for the pre-implementation endpoint interval contract.

This is a contract lint, not a mathematical control and not a certificate.
"""

from fractions import Fraction
import json
from pathlib import Path
import unittest


CONTRACT = (
    Path(__file__).resolve().parents[1]
    / "spec"
    / "endpoint_local_interval_contract_v1.json"
)


class EndpointLocalIntervalContractLint(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = json.loads(CONTRACT.read_text(encoding="utf-8"))

    def test_file_cannot_be_mistaken_for_a_certificate(self):
        status = self.document["status"]
        self.assertEqual(status["evidence_class"], "NOT_BINDING")
        self.assertEqual(status["derivation_class"], "PROTOTYPE")
        self.assertIs(status["is_certificate"], False)

    def test_bracket_is_exact_and_ordered(self):
        domain = self.document["parameter"]["domain"]
        lower = Fraction(domain["lower"]["numerator"], domain["lower"]["denominator"])
        upper = Fraction(domain["upper"]["numerator"], domain["upper"]["denominator"])
        self.assertEqual(lower, Fraction(16, 25))
        self.assertEqual(upper, Fraction(13, 20))
        self.assertLess(lower, upper)

    def test_required_relations_fix_exist_unique_scope(self):
        relations = {
            item["quantity"]: item["required_relation"]
            for item in self.document["required_enclosures"]
        }
        self.assertEqual(relations["B_ob(16/25)"], "upper_bound < 0")
        self.assertEqual(relations["B_ob(13/20)"], "lower_bound > 0")
        self.assertEqual(
            relations["B_ob_prime([16/25,13/20])"],
            "lower_bound > 0",
        )
        self.assertEqual(
            self.document["conclusion_if_all_checks_pass"],
            "B_ob has exactly one zero in [16/25,13/20].",
        )

    def test_precision_and_clean_room_obligations_are_explicit(self):
        separation = self.document["producer_checker_separation"]
        self.assertIs(separation["producer_output_required"], True)
        self.assertIs(separation["checker_reconstructs_enclosures"], True)
        self.assertIs(
            separation["checker_precision_not_less_than_producer"],
            True,
        )
        self.assertIs(separation["clean_room_run_required_for_certified_status"], True)


if __name__ == "__main__":
    unittest.main()
