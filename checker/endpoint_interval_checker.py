#!/usr/bin/env python3
"""Independent Arb checker for endpoint-local producer records.

This module imports neither the producer nor the mpmath prototype evaluator.
It reconstructs every cell range, series tail, integral, total, and sign.
"""

from __future__ import annotations

from fractions import Fraction
import hashlib
import json
from math import comb
from pathlib import Path
import subprocess

from flint import arb, ctx

from checker.endpoint_local_checker import (
    VerificationError,
    verify_exact_cell_cover,
)
from checker.endpoint_local_controls import run_exact_controls


ROOT = Path(__file__).resolve().parents[1]
WHEEL_SHA256 = "376b88cacd30612479e839ffdba887599d3f9c8c0e214852bf80bb2b194e4d76"
TOP_KEYS = {
    "schema", "status", "provenance", "precision", "contract", "controls",
    "evaluations",
}
PROVENANCE_KEYS = {
    "source_commit", "producer_sha256", "checker_sha256", "prototype_sha256",
    "controls_sha256", "contract_sha256", "workflow_sha256",
    "requirements_sha256", "wheel_filename", "wheel_sha256",
}


def _fraction(text):
    if text == "sqrt2":
        return None
    return Fraction(text)


def _point(value):
    if isinstance(value, Fraction):
        return arb(value.numerator) / value.denominator
    return arb(value)


def _box(left, right):
    return arb((left + right) / 2, (right - left) / 2)


def _zero_to_upper(value):
    upper = max(arb(0), value.upper())
    half = upper / 2
    return arb(half, half)


def _clamp_nonnegative(value):
    lower = max(arb(0), value.lower())
    upper = max(arb(0), value.upper())
    return _box(lower, upper)


def _power(value, exponent):
    result = arb(1)
    for _ in range(exponent):
        result *= value
    return result


def _record_ball(record):
    try:
        midpoint = arb(record["midpoint"])
        radius = arb(record["radius"])
    except (KeyError, TypeError, ValueError) as exc:
        raise VerificationError("invalid Arb ball record") from exc
    if radius < 0:
        raise VerificationError("negative Arb radius")
    return arb(midpoint, radius)


def _require_contains(record, independently_computed, label):
    supplied = _record_ball(record)
    if not supplied.contains(independently_computed):
        raise VerificationError(f"{label} does not contain checker enclosure")


def _series(u, name, degree):
    if name == "Phi":
        partial = arb(0)
        for n in range(1, degree + 1):
            partial += _point(
                Fraction(4**n, 2 * n * n * comb(2 * n, n))
            ) * _power(u, n)
        n = degree + 1
        next_term = _point(
            Fraction(4**n, 2 * n * n * comb(2 * n, n))
        ) * _power(u, n)
    elif name == "Psi":
        partial = arb(0)
        for n in range(degree + 1):
            partial += _point(
                Fraction(comb(2 * n, n), 4**n * (2 * n + 1))
            ) * _power(u, n)
        n = degree + 1
        next_term = _point(
            Fraction(comb(2 * n, n), 4**n * (2 * n + 1))
        ) * _power(u, n)
    elif name == "Psi_prime":
        partial = arb(0)
        for n in range(1, degree + 1):
            partial += _point(
                Fraction(n * comb(2 * n, n), 4**n * (2 * n + 1))
            ) * _power(u, n - 1)
        n = degree + 1
        next_term = _point(
            Fraction(n * comb(2 * n, n), 4**n * (2 * n + 1))
        ) * _power(u, n - 1)
    else:
        raise VerificationError(f"unsupported series {name}")
    remainder = _zero_to_upper(next_term / (1 - u))
    return partial + remainder, partial, remainder


def _kernel_box(s, lam, chart, derivative, series_records):
    e = s * s
    lam2 = lam * lam
    a = 1 - lam2
    h = 1 - a * e
    w2 = 1 - 2 * a * e + a * e * e
    qhat = 2 - a * e
    gap = 2 - e
    if chart == "u_upper":
        gap = _clamp_nonnegative(gap)
    gamma = lam * s / (w2.sqrt() * qhat.sqrt())
    gamma2 = lam2 * e / (w2 * qhat)
    qhat_3_2 = qhat * qhat.sqrt()
    p = 2 * lam * e * gap * h / (w2.sqrt() * qhat_3_2)
    r = -gap * h * ((1 + lam2) * e - 1) / (lam * w2 * qhat)
    j = (
        h + 2 * lam2 * e
        - lam2 * h * e * gap / w2
        - 3 * lam2 * h * e / qhat
    )
    p_lam = 2 * e * gap * j / (w2.sqrt() * qhat_3_2)

    if chart == "gamma_lower":
        expected_name = "Psi" if derivative else "Phi"
        if len(series_records) != 1 or series_records[0].get("function") != expected_name:
            raise VerificationError("lower-chart record inventory mismatch")
        u = 1 - gamma * gamma
        sqrt_u = u.sqrt()
        alpha = gamma.acos()
        psi = alpha / sqrt_u
        if not derivative:
            return -s * (1 - e) * alpha * alpha + p * psi
        psi_lam = gamma * r * (gamma * psi - 1) / u
        return (
            2 * s * (1 - e) * alpha * gamma * r / sqrt_u
            + p_lam * psi + p * psi_lam
        )

    u = gap * h * h / (w2 * qhat)
    by_name = {}
    for record in series_records:
        name = record["function"]
        degree = record["degree"]
        value, partial, remainder = _series(u, name, degree)
        _require_contains(record["partial_sum"], partial, f"{name} partial sum")
        _require_contains(
            record["remainder_bound"], remainder, f"{name} remainder"
        )
        by_name[name] = value
    required = {"Phi", "Psi"} | ({"Psi_prime"} if derivative else set())
    if set(by_name) != required:
        raise VerificationError("series inventory mismatch")
    value = -s * (1 - e) * by_name["Phi"] + p * by_name["Psi"]
    if derivative:
        value = (
            2 * s * (1 - e) * gamma * r * by_name["Psi"]
            + p_lam * by_name["Psi"]
            - 2 * p * gamma2 * r * by_name["Psi_prime"]
        )
    return value


def _endpoint(text):
    return arb(2).sqrt() if text == "sqrt2" else _point(Fraction(text))


def _check_quadrature_bookkeeping(cells):
    total = arb(0)
    for cell in cells:
        left, right = map(_endpoint, cell["s_interval"])
        s = _box(left, right)
        total += s**3 * (right - left)
    if not total.contains(arb(1)):
        raise VerificationError("checker quadrature bookkeeping misses 1")
    if total.rad() > arb("0.01"):
        raise VerificationError("checker quadrature bookkeeping too wide")


def _verify_evaluation(evaluation):
    cells = evaluation["cells"]
    verify_exact_cell_cover(cells)
    derivative = evaluation["purpose"] == "B_ob_prime"
    checker_total = arb(0)
    for cell in cells:
        left, right = map(_endpoint, cell["s_interval"])
        lam_left, lam_right = map(
            lambda text: _point(Fraction(text)),
            cell["lambda_interval"],
        )
        if cell["lambda_interval"] != evaluation["lambda_interval"]:
            raise VerificationError("cell/evaluation lambda interval mismatch")
        expected_construction = (
            "not_used" if cell["chart"] == "gamma_lower"
            else "factorized_complement"
        )
        if cell["u_construction"] != expected_construction:
            raise VerificationError("chart construction mismatch")
        s = _box(left, right)
        lam = _box(lam_left, lam_right)
        kernel = _kernel_box(
            s, lam, cell["chart"], derivative, cell["series"]
        )
        integral = kernel * (right - left)
        if derivative:
            _require_contains(
                cell["lambda_derivative_enclosure"],
                kernel,
                "derivative kernel",
            )
            _require_contains(
                cell["weighted_derivative_integral_enclosure"],
                integral,
                "derivative integral",
            )
        else:
            _require_contains(cell["kernel_enclosure"], kernel, "kernel")
            _require_contains(
                cell["weighted_integral_enclosure"], integral, "integral"
            )
        checker_total += integral
    _require_contains(evaluation["reported_sum"], checker_total, "reported sum")
    return checker_total


def _sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_interval_record(record):
    if not isinstance(record, dict) or set(record) != TOP_KEYS:
        raise VerificationError("top-level record shape mismatch")
    if record["schema"] != "bg-oblate-spheroid.endpoint-local-producer-record.v1":
        raise VerificationError("schema identifier mismatch")
    if record["status"] != {
        "evidence_class": "NOT_BINDING",
        "derivation_class": "PROTOTYPE",
        "is_certificate": False,
    }:
        raise VerificationError("record status mismatch")
    if record["contract"] != {
        "lambda_lower": "5/8",
        "lambda_upper": "33/50",
    }:
        raise VerificationError("contract mismatch")
    if set(record["provenance"]) != PROVENANCE_KEYS:
        raise VerificationError("provenance shape mismatch")
    if not isinstance(record["evaluations"], list) or len(record["evaluations"]) != 3:
        raise VerificationError("exactly three evaluations required")
    bits = record["precision"]["checker_bits"]
    if bits < record["precision"]["producer_bits"]:
        raise VerificationError("checker precision below producer precision")
    ctx.prec = bits
    if record["controls"] != {
        **run_exact_controls(),
        "quadrature_bookkeeping": "PASS",
    }:
        raise VerificationError("control ledger mismatch")
    expected_hashes = {
        "producer_sha256": ROOT / "producer/endpoint_interval_producer.py",
        "checker_sha256": ROOT / "checker/endpoint_interval_checker.py",
        "prototype_sha256": ROOT / "checker/oblate_axis_prototype.py",
        "controls_sha256": ROOT / "checker/endpoint_local_controls.py",
        "contract_sha256": ROOT / "spec/endpoint_local_interval_contract_v1.json",
        "workflow_sha256": ROOT / ".github/workflows/oblate-endpoint-prototype.yml",
        "requirements_sha256": ROOT / "requirements-interval.txt",
    }
    for key, path in expected_hashes.items():
        if record["provenance"][key] != _sha256(path):
            raise VerificationError(f"provenance mismatch: {key}")
    current_commit = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()
    if record["provenance"]["source_commit"] != current_commit:
        raise VerificationError("source commit mismatch")
    if record["provenance"]["wheel_sha256"] != WHEEL_SHA256:
        raise VerificationError("wheel hash mismatch")

    labels = {item["label"]: item for item in record["evaluations"]}
    if set(labels) != {"left_endpoint", "right_endpoint", "derivative_domain"}:
        raise VerificationError("evaluation label inventory mismatch")
    expected_roles = {
        "left_endpoint": ("B_ob", ["5/8", "5/8"]),
        "right_endpoint": ("B_ob", ["33/50", "33/50"]),
        "derivative_domain": ("B_ob_prime", ["5/8", "33/50"]),
    }
    for label, (purpose, interval) in expected_roles.items():
        if labels[label].get("purpose") != purpose:
            raise VerificationError("label/purpose mismatch")
        if labels[label].get("lambda_interval") != interval:
            raise VerificationError("binding lambda interval mismatch")
    _check_quadrature_bookkeeping(labels["left_endpoint"]["cells"])
    totals = {label: _verify_evaluation(item) for label, item in labels.items()}
    if not totals["left_endpoint"].upper() < 0:
        raise VerificationError("left endpoint is not strictly negative")
    if not totals["right_endpoint"].lower() > 0:
        raise VerificationError("right endpoint is not strictly positive")
    if not totals["derivative_domain"].lower() > 0:
        raise VerificationError("derivative is not strictly positive")
    return {
        "status": "PASS",
        "conclusion": "B_ob has exactly one zero in [5/8,33/50].",
        "checker_totals": {
            key: {"lower": value.lower().str(50), "upper": value.upper().str(50)}
            for key, value in totals.items()
        },
    }


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("record", type=Path)
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    record = json.loads(args.record.read_text(encoding="utf-8"))
    receipt = verify_interval_record(record)
    output = json.dumps(receipt, sort_keys=True, separators=(",", ":")) + "\n"
    if args.receipt:
        args.receipt.write_text(output, encoding="utf-8")
    else:
        print(output, end="")


if __name__ == "__main__":
    main()
