#!/usr/bin/env python3
"""Structural checks for the pre-implementation endpoint interval contract.

This is a contract lint, not a mathematical control and not a certificate.
"""

from fractions import Fraction
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "spec" / "endpoint_local_interval_contract_v1.json"
PRODUCER_SCHEMA = (
    ROOT / "spec" / "endpoint_local_producer_record_v1.schema.json"
)


def rational(pair):
    return Fraction(pair["numerator"], pair["denominator"])


class EndpointLocalIntervalContractLint(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = json.loads(CONTRACT.read_text(encoding="utf-8"))
        cls.producer_schema = json.loads(
            PRODUCER_SCHEMA.read_text(encoding="utf-8")
        )

    def test_file_cannot_be_mistaken_for_a_certificate(self):
        status = self.document["status"]
        self.assertEqual(status["evidence_class"], "NOT_BINDING")
        self.assertEqual(status["derivation_class"], "PROTOTYPE")
        self.assertIs(status["is_certificate"], False)

    def test_broad_bracket_is_exact_and_ordered(self):
        parameter = self.document["parameter"]
        domain = parameter["certification_domain"]
        lower = rational(domain["lower"])
        upper = rational(domain["upper"])
        self.assertEqual(lower, Fraction(5, 8))
        self.assertEqual(upper, Fraction(33, 50))
        self.assertLess(lower, upper)

        waypoint = parameter["diagnostic_newton_waypoint"]
        self.assertEqual(rational(waypoint["lower"]), Fraction(16, 25))
        self.assertEqual(rational(waypoint["upper"]), Fraction(13, 20))
        self.assertIs(waypoint["binding"], False)
        self.assertLess(lower, rational(waypoint["lower"]))
        self.assertLess(rational(waypoint["upper"]), upper)

    def test_required_relations_fix_exist_unique_scope(self):
        relations = {
            item["quantity"]: item["required_relation"]
            for item in self.document["required_enclosures"]
        }
        self.assertEqual(relations["B_ob(5/8)"], "upper_bound < 0")
        self.assertEqual(relations["B_ob(33/50)"], "lower_bound > 0")
        self.assertEqual(
            relations["B_ob_prime([5/8,33/50])"],
            "lower_bound > 0",
        )
        self.assertEqual(
            self.document["conclusion_if_all_checks_pass"],
            "B_ob has exactly one zero in [5/8,33/50].",
        )

    def test_newton_cannot_replace_broad_bracket(self):
        policy = self.document["refinement_policy"]
        self.assertEqual(policy["method"], "interval_newton")
        self.assertIs(policy["starts_only_after_broad_bracket_passes"], True)
        self.assertIs(policy["reuses_certified_derivative_enclosure"], True)


    def test_producer_schema_fixes_independent_checker_inputs(self):
        schema = self.producer_schema
        self.assertFalse(schema["additionalProperties"])
        required = set(schema["required"])
        self.assertEqual(
            required,
            {
                "schema",
                "status",
                "provenance",
                "precision",
                "contract",
                "controls",
                "evaluations",
            },
        )
        control_required = set(
            schema["properties"]["controls"]["required"]
        )
        self.assertEqual(
            control_required,
            {
                "endpoint_values",
                "global_complement",
                "internal_double_zero",
                "seam_rational_targets",
                "A_gamma_t_factorization",
                "gamma_lambda_factorization",
                "quadrature_bookkeeping",
            },
        )
        provenance_required = set(
            schema["properties"]["provenance"]["required"]
        )
        self.assertTrue(
            {
                "source_commit",
                "producer_sha256",
                "checker_sha256",
                "contract_sha256",
                "workflow_sha256",
                "requirements_sha256",
                "wheel_filename",
                "wheel_sha256",
            }.issubset(provenance_required)
        )
        cell_required = set(schema["$defs"]["cell"]["required"])
        self.assertTrue(
            {
                "s_interval",
                "lambda_interval",
                "chart",
                "u_construction",
                "series",
                "kernel_enclosure",
                "lambda_derivative_enclosure",
                "weighted_integral_enclosure",
                "weighted_derivative_integral_enclosure",
            }.issubset(cell_required)
        )
        cell_schema = schema["$defs"]["cell"]
        upper_rule = cell_schema["allOf"][1]
        self.assertEqual(
            upper_rule["then"]["properties"]["u_construction"]["const"],
            "factorized_complement",
        )
        series_schema = cell_schema["properties"]["series"]
        self.assertEqual(series_schema["minItems"], 1)
        self.assertIn(
            "Psi_prime",
            schema["$defs"]["series"]["properties"]["function"]["enum"],
        )
        evaluations_schema = schema["properties"]["evaluations"]
        self.assertEqual(evaluations_schema["minItems"], 3)
        self.assertEqual(evaluations_schema["maxItems"], 3)
        required_labels = {
            rule["contains"]["properties"]["label"]["const"]
            for rule in evaluations_schema["allOf"]
        }
        self.assertEqual(
            required_labels,
            {"left_endpoint", "right_endpoint", "derivative_domain"},
        )
        self.assertTrue(
            all(
                rule["minContains"] == rule["maxContains"] == 1
                for rule in evaluations_schema["allOf"]
            )
        )
        derivative_rule = schema["$defs"]["evaluation"]["allOf"][1]
        self.assertEqual(
            derivative_rule["then"]["properties"]["purpose"]["const"],
            "B_ob_prime",
        )
        upper_series = (
            derivative_rule["then"]["properties"]["cells"]["items"]["then"]
            ["properties"]["series"]
        )
        self.assertEqual(
            upper_series["contains"]["properties"]["function"]["const"],
            "Psi_prime",
        )
        self.assertEqual(upper_series["minContains"], 1)
        self.assertNotIn(
            "one_minus_gamma_squared",
            cell_schema["properties"]["u_construction"]["enum"],
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
