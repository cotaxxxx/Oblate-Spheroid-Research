#!/usr/bin/env python3
"""Arb producer candidate for gt_boundary_ob = partial_t g_axis_ob(1, lambda).

Evidence class: NOT_BINDING.
Derivation class: PROTOTYPE derived from the retained certified two-chart
endpoint lineage on receipt-binding-e5ab171.

The only gating claim is an Arb enclosure with upper endpoint < 0 on
lambda in [5/8, 33/50]. Point expectations are REPORTED_NOT_GATING.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
from math import isqrt
from pathlib import Path

from flint import arb, ctx

from producer.endpoint_interval_producer import (
    SQRT2,
    _ball_record,
    _box,
    _clamp_nonnegative,
    _endpoint_label,
    _partition,
    _point,
    _series,
)


EXPECTATIONS = {
    "5/8": "-1.4120900996030582330984866619528326407579821748752",
    "13/20": "-1.4717090003859539426113646310237584846969543547289",
    "33/50": "-1.4958034682340728485822766948219344845501715771395",
}


def _gt_kernel_box(s, lam, chart, degree):
    """Endpoint-regular density for partial_t g_axis_ob at t=1.

    Starting from
        G = s[4 mu R gamma_t - 2 s^2(R_gamma gamma_t^2 + R gamma_tt)],
    all explicit 1/s factors are cancelled analytically before interval
    evaluation.
    """
    e = s * s
    lam2 = lam * lam
    lam3 = lam2 * lam
    a = 1 - lam2
    h = 1 - a * e
    w2 = 1 - 2 * a * e + a * e * e
    w = w2.sqrt()
    qhat = 2 - a * e
    qhat_sqrt = qhat.sqrt()
    qhat_3_2 = qhat * qhat_sqrt
    qhat_5_2 = qhat * qhat_3_2
    gap = 2 - e
    if chart == "u_upper":
        gap = _clamp_nonnegative(gap)

    c = gap * h
    d = gap * (1 - 2 * a * e)
    gamma = lam * s / (w * qhat_sqrt)

    records = []
    if chart == "gamma_lower":
        u = 1 - gamma * gamma
        alpha = gamma.acos()
        r = alpha / u.sqrt()
        r_gamma = (gamma * r - 1) / u
        value = (
            -4 * (1 - e) * lam * r * c / (w * qhat_3_2)
            -2 * s * lam2 * r_gamma * c * c / (w2 * qhat * qhat * qhat)
            -2 * e * lam3 * r * d / (w * qhat_5_2)
        )
        return value, records

    # Upper chart: u = 1-gamma^2 is factorized to cross the internal gamma=1
    # point without a 0/0 quotient.  R=Psi(u), R_gamma=-2 gamma Psi'(u).
    u = _clamp_nonnegative(gap * h * h / (w2 * qhat))
    psi, psi_record = _series(u, "Psi", degree, clamped_nonnegative=True)
    psi_prime, prime_record = _series(
        u, "Psi_prime", degree, clamped_nonnegative=True
    )
    records.extend([psi_record, prime_record])

    # Substitute gamma into the R_gamma term as well, eliminating its
    # denominator and preserving the certified Psi_prime series lineage.
    value = (
        -4 * (1 - e) * lam * psi * c / (w * qhat_3_2)
        +4 * e * lam3 * psi_prime * c * c
        / (w * w2 * qhat * qhat * qhat_3_2)
        -2 * e * lam3 * psi * d / (w * qhat_5_2)
    )
    return value, records


def _evaluation(lam_left, lam_right, panels, degree):
    endpoints, root = _partition(panels)
    lam = _box(_point(lam_left), _point(lam_right))
    total = arb(0)
    cells = []
    for ordinal, (left, right) in enumerate(zip(endpoints, endpoints[1:])):
        left_arb = root if left == SQRT2 else _point(left)
        right_arb = root if right == SQRT2 else _point(right)
        chart = "gamma_lower" if right != SQRT2 and right <= 1 else "u_upper"
        s = _box(left_arb, right_arb)
        kernel, series = _gt_kernel_box(s, lam, chart, degree)
        weighted = kernel * (right_arb - left_arb)
        total += weighted
        cells.append({
            "ordinal": ordinal,
            "s_interval": [_endpoint_label(left), _endpoint_label(right)],
            "lambda_interval": [
                _endpoint_label(lam_left), _endpoint_label(lam_right)
            ],
            "chart": chart,
            "series": series,
            "kernel_enclosure": _ball_record(kernel),
            "weighted_integral_enclosure": _ball_record(weighted),
        })
    return {
        "purpose": "gt_boundary_ob",
        "lambda_interval": [
            _endpoint_label(lam_left), _endpoint_label(lam_right)
        ],
        "cells": cells,
        "reported_sum": _ball_record(total),
        "gating": {
            "required_sign": "NEG",
            "criterion": "upper_endpoint < 0",
            "pass": bool(total.upper() < 0),
        },
    }


def produce_record(bits=160, panels=1024, degree=50):
    ctx.prec = bits
    evaluation = _evaluation(Fraction(5, 8), Fraction(33, 50), panels, degree)
    return {
        "schema": "bg-oblate-spheroid.gt-boundary-producer-record.v1",
        "status": {
            "evidence_class": "NOT_BINDING",
            "derivation_class": "PROTOTYPE",
            "is_certificate": False,
        },
        "contract": {
            "quantity": "partial_t g_axis_ob(1,lambda)",
            "lambda_domain": ["5/8", "33/50"],
            "required_sign": "NEG",
            "gating_rule": "reported_sum.upper_endpoint < 0",
        },
        "expectations": {
            "status": "REPORTED_NOT_GATING",
            "values": EXPECTATIONS,
        },
        "precision": {"producer_bits": bits},
        "evaluation": evaluation,
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
    if not record["evaluation"]["gating"]["pass"]:
        raise SystemExit("UNRESOLVED: gt_boundary_ob upper endpoint is not < 0")


if __name__ == "__main__":
    main()
