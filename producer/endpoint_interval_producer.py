#!/usr/bin/env python3
"""Arb producer for the local oblate boundary-entry certificate candidate.

Evidence class: NOT_BINDING.
Derivation class: PROTOTYPE built from the separately pinned AUDITED_SOURCE.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from math import comb, isqrt
from pathlib import Path
import subprocess

from flint import arb, ctx
import mpmath as mp

from checker.endpoint_local_controls import (
    CONTROL_NAMES,
    run_exact_controls,
    run_quadrature_bookkeeping_control,
)
from checker.oblate_axis_prototype import quadrature_bookkeeping_ob


ROOT = Path(__file__).resolve().parents[1]
SQRT2 = "sqrt2"
WHEEL_FILENAME = (
    "python_flint-0.9.0-cp310-abi3-manylinux2014_x86_64."
    "manylinux_2_17_x86_64.whl"
)
WHEEL_SHA256 = "376b88cacd30612479e839ffdba887599d3f9c8c0e214852bf80bb2b194e4d76"


def _point(value):
    if isinstance(value, Fraction):
        return arb(value.numerator) / value.denominator
    return arb(value)


def _box(left, right):
    midpoint = (left + right) / 2
    radius = (right - left) / 2
    return arb(midpoint, radius)


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


def _ball_record(value):
    return {
        "midpoint": value.mid().str(80),
        "radius": value.rad().str(80),
    }


def _series(u, name, degree):
    if name == "Phi":
        partial = arb(0)
        for n in range(1, degree + 1):
            coefficient = Fraction(4**n, 2 * n * n * comb(2 * n, n))
            partial += _point(coefficient) * _power(u, n)
        n = degree + 1
        next_term = _point(
            Fraction(4**n, 2 * n * n * comb(2 * n, n))
        ) * _power(u, n)
    elif name == "Psi":
        partial = arb(0)
        for n in range(degree + 1):
            coefficient = Fraction(comb(2 * n, n), 4**n * (2 * n + 1))
            partial += _point(coefficient) * _power(u, n)
        n = degree + 1
        next_term = _point(
            Fraction(comb(2 * n, n), 4**n * (2 * n + 1))
        ) * _power(u, n)
    elif name == "Psi_prime":
        partial = arb(0)
        for n in range(1, degree + 1):
            coefficient = Fraction(
                n * comb(2 * n, n),
                4**n * (2 * n + 1),
            )
            partial += _point(coefficient) * _power(u, n - 1)
        n = degree + 1
        next_term = _point(
            Fraction(n * comb(2 * n, n), 4**n * (2 * n + 1))
        ) * _power(u, n - 1)
    else:
        raise ValueError(f"unknown series {name}")

    remainder = next_term / (1 - u)
    remainder_ball = _zero_to_upper(remainder)
    return partial + remainder_ball, {
        "function": name,
        "degree": degree,
        "partial_sum": _ball_record(partial),
        "remainder_bound": _ball_record(remainder_ball),
    }


def _kernel_box(s, lam, chart, derivative, degree):
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
        h
        + 2 * lam2 * e
        - lam2 * h * e * gap / w2
        - 3 * lam2 * h * e / qhat
    )
    p_lam = 2 * e * gap * j / (w2.sqrt() * qhat_3_2)

    records = []
    if chart == "gamma_lower":
        u = 1 - gamma * gamma
        sqrt_u = u.sqrt()
        alpha = gamma.acos()
        psi = alpha / sqrt_u
        value = -s * (1 - e) * alpha * alpha + p * psi
        if derivative:
            psi_lam = gamma * r * (gamma * psi - 1) / u
            value = (
                2 * s * (1 - e) * alpha * gamma * r / sqrt_u
                + p_lam * psi
                + p * psi_lam
            )
        records.append({
            "function": "Phi" if not derivative else "Psi",
            "degree": 0,
            "partial_sum": _ball_record(alpha * alpha if not derivative else psi),
            "remainder_bound": _ball_record(arb(0)),
        })
    else:
        u = gap * h * h / (w2 * qhat)
        phi, phi_record = _series(u, "Phi", degree)
        psi, psi_record = _series(u, "Psi", degree)
        records.extend([phi_record, psi_record])
        value = -s * (1 - e) * phi + p * psi
        if derivative:
            psi_prime, prime_record = _series(u, "Psi_prime", degree)
            records.append(prime_record)
            value = (
                2 * s * (1 - e) * gamma * r * psi
                + p_lam * psi
                - 2 * p * gamma2 * r * psi_prime
            )
    return value, records


def _endpoint_label(value):
    if value == SQRT2:
        return value
    return f"{value.numerator}/{value.denominator}"


def _partition(panels_per_unit):
    root = arb(2).sqrt()
    rational_end = isqrt(2 * panels_per_unit * panels_per_unit)
    values = [Fraction(i, panels_per_unit) for i in range(panels_per_unit + 1)]
    values.extend(
        Fraction(i, panels_per_unit)
        for i in range(panels_per_unit + 1, rational_end + 1)
    )
    return values + [SQRT2], root


def _evaluation(label, lam_left, lam_right, derivative, panels, degree):
    endpoints, root = _partition(panels)
    lam = _box(_point(lam_left), _point(lam_right))
    total = arb(0)
    cells = []
    for ordinal, (left, right) in enumerate(zip(endpoints, endpoints[1:])):
        left_arb = root if left == SQRT2 else _point(left)
        right_arb = root if right == SQRT2 else _point(right)
        chart = "gamma_lower" if right != SQRT2 and right <= 1 else "u_upper"
        s = _box(left_arb, right_arb)
        kernel, series = _kernel_box(s, lam, chart, derivative, degree)
        integral = kernel * (right_arb - left_arb)
        total += integral
        zero = arb(0)
        cells.append({
            "ordinal": ordinal,
            "s_interval": [_endpoint_label(left), _endpoint_label(right)],
            "lambda_interval": [
                _endpoint_label(lam_left),
                _endpoint_label(lam_right),
            ],
            "chart": chart,
            "u_construction": (
                "not_used" if chart == "gamma_lower"
                else "factorized_complement"
            ),
            "series": series,
            "kernel_enclosure": _ball_record(kernel if not derivative else zero),
            "lambda_derivative_enclosure": _ball_record(
                kernel if derivative else zero
            ),
            "weighted_integral_enclosure": _ball_record(
                integral if not derivative else zero
            ),
            "weighted_derivative_integral_enclosure": _ball_record(
                integral if derivative else zero
            ),
        })
    return {
        "label": label,
        "lambda_interval": [
            _endpoint_label(lam_left),
            _endpoint_label(lam_right),
        ],
        "purpose": "B_ob_prime" if derivative else "B_ob",
        "cells": cells,
        "reported_sum": _ball_record(total),
    }


def _sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def produce_record(bits=160, panels=1024, degree=50):
    ctx.prec = bits
    exact = run_exact_controls()
    quadrature = run_quadrature_bookkeeping_control(
        lambda: Fraction(
            mp.nstr(
                quadrature_bookkeeping_ob(dps=max(50, bits // 3)),
                n=max(50, bits // 3),
            )
        ),
        Fraction(1, 10**30),
    )
    controls = exact | quadrature
    if set(controls) != set(CONTROL_NAMES):
        raise RuntimeError("control ledger mismatch")

    source_commit = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()
    paths = {
        "producer_sha256": ROOT / "producer/endpoint_interval_producer.py",
        "checker_sha256": ROOT / "checker/endpoint_interval_checker.py",
        "prototype_sha256": ROOT / "checker/oblate_axis_prototype.py",
        "controls_sha256": ROOT / "checker/endpoint_local_controls.py",
        "contract_sha256": ROOT / "spec/endpoint_local_interval_contract_v1.json",
        "workflow_sha256": ROOT / ".github/workflows/oblate-endpoint-prototype.yml",
        "requirements_sha256": ROOT / "requirements-interval.txt",
    }
    return {
        "schema": "bg-oblate-spheroid.endpoint-local-producer-record.v1",
        "status": {
            "evidence_class": "NOT_BINDING",
            "derivation_class": "PROTOTYPE",
            "is_certificate": False,
        },
        "provenance": {
            "source_commit": source_commit,
            **{key: _sha256(path) for key, path in paths.items()},
            "wheel_filename": WHEEL_FILENAME,
            "wheel_sha256": WHEEL_SHA256,
        },
        "precision": {"producer_bits": bits, "checker_bits": bits},
        "contract": {"lambda_lower": "5/8", "lambda_upper": "33/50"},
        "controls": controls,
        "evaluations": [
            _evaluation("left_endpoint", Fraction(5, 8), Fraction(5, 8), False, panels, degree),
            _evaluation("right_endpoint", Fraction(33, 50), Fraction(33, 50), False, panels, degree),
            _evaluation("derivative_domain", Fraction(5, 8), Fraction(33, 50), True, panels, degree),
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--bits", type=int, default=160)
    parser.add_argument("--panels", type=int, default=1024)
    parser.add_argument("--degree", type=int, default=50)
    args = parser.parse_args()
    record = produce_record(args.bits, args.panels, args.degree)
    args.output.write_text(
        json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
