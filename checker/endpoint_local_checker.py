#!/usr/bin/env python3
"""Fail-closed skeleton for the endpoint-local independent checker.

This checker does not import or execute producer code. Until every TODO
obligation is implemented, verify_record raises VerificationIncomplete after
running schema-independent controls and exact coverage checks.
"""

from fractions import Fraction

from checker.endpoint_local_controls import run_exact_controls


SQRT2 = "sqrt2"


class VerificationError(RuntimeError):
    pass


class VerificationIncomplete(VerificationError):
    pass


def _rational(text):
    if not isinstance(text, str) or "/" not in text:
        raise VerificationError(f"invalid rational endpoint: {text!r}")
    numerator, denominator = text.split("/", 1)
    value = Fraction(int(numerator), int(denominator))
    if str(value.numerator) + "/" + str(value.denominator) != text:
        raise VerificationError(f"noncanonical rational endpoint: {text!r}")
    return value


def _endpoint_key(text):
    if text == SQRT2:
        return (1, None)
    value = _rational(text)
    if value < 0 or value * value > 2:
        raise VerificationError(f"s endpoint outside [0,sqrt2]: {text}")
    return (0, value)


def verify_exact_cell_cover(cells):
    """Require one gap-free partition with the unique seam at exact s=1."""
    if not isinstance(cells, list) or len(cells) < 2:
        raise VerificationError("at least two cells required")

    expected_left = "0/1"
    seam_count = 0
    for ordinal, cell in enumerate(cells):
        if cell.get("ordinal") != ordinal:
            raise VerificationError("cell ordinals must be contiguous from zero")
        interval = cell.get("s_interval")
        if not isinstance(interval, list) or len(interval) != 2:
            raise VerificationError("each cell needs two s endpoints")
        left, right = interval
        if left != expected_left:
            raise VerificationError("cell gap, overlap, or reordered endpoint")
        left_key = _endpoint_key(left)
        right_key = _endpoint_key(right)
        if right_key[0] == 0:
            if left_key[0] != 0 or not left_key[1] < right_key[1]:
                raise VerificationError("cell endpoints must strictly increase")
        elif left == SQRT2:
            raise VerificationError("cell cannot start at terminal sqrt2")

        chart = cell.get("chart")
        if right_key[0] == 0 and right_key[1] <= 1:
            if chart != "gamma_lower":
                raise VerificationError("lower cell has wrong chart")
        elif left_key[0] == 0 and left_key[1] >= 1:
            if chart != "u_upper":
                raise VerificationError("upper cell has wrong chart")
        else:
            raise VerificationError("a cell may not cross the exact seam s=1")

        if right == "1/1":
            seam_count += 1
        expected_left = right

    if expected_left != SQRT2:
        raise VerificationError("cell cover must terminate at exact sqrt2 label")
    if seam_count != 1:
        raise VerificationError("cell cover must contain exactly one s=1 seam")


def verification_layers():
    """Machine-readable trust-boundary wording for the final report."""
    return {
        "controls_check": (
            "six checker-owned exact algebra families; the seventh "
            "quadrature-bookkeeping family requires an implementation-produced "
            "candidate and an independent exact expectation"
        ),
        "controls_do_not_check": (
            "geometric derivation of the kernel, analytic two-chart lemma, "
            "or differentiation-under-the-integral proof"
        ),
        "checker_reconstructs": (
            "coverage, series remainder bounds, cell range enclosures, "
            "weighted cell integrals, totals, and sign relations"
        ),
        "checker_does_not_reuse": (
            "producer adaptive integration path, producer PASS labels, "
            "or producer final sums"
        ),
    }


def verify_record(record):
    """Run implemented independent checks, then fail until arithmetic is complete."""
    controls = run_exact_controls()
    evaluations = record.get("evaluations")
    if not isinstance(evaluations, list):
        raise VerificationError("missing evaluations")
    for evaluation in evaluations:
        verify_exact_cell_cover(evaluation.get("cells"))
    if record["precision"]["checker_bits"] < record["precision"]["producer_bits"]:
        raise VerificationError("checker precision below producer precision")

    # Deliberately fail closed. Future units must independently reconstruct
    # series remainders, cell range enclosures, integrals, totals, and signs.
    raise VerificationIncomplete(
        "interval arithmetic reconstruction is not implemented; "
        f"exact controls passed: {sorted(controls)}"
    )
