#!/usr/bin/env python3
"""Binary64 margin reconnaissance for the broad endpoint bracket.

Evidence class: DIAGNOSTIC_ONLY / NOT_BINDING.
Derivation class: FLOAT.

This script is not imported by the interval producer or checker. It estimates
endpoint sign margins and finite-difference lambda slopes using the independent
standard-library Simpson evaluator from oblate_fold_scan.
"""

from diagnostics.oblate_fold_scan import g_value


LOWER = 5.0 / 8.0
UPPER = 33.0 / 50.0


def b_float(lam, panels):
    return g_value(1.0, lam, panels=panels)


def centered_lambda_slope(lam, panels, h=1.0e-4):
    return (
        b_float(lam + h, panels) - b_float(lam - h, panels)
    ) / (2.0 * h)


def main():
    print("status=DIAGNOSTIC_ONLY/NOT_BINDING derivation=FLOAT")
    for lam in (LOWER, 0.64, 0.65, UPPER):
        coarse = b_float(lam, 1200)
        fine = b_float(lam, 2400)
        slope = centered_lambda_slope(lam, 2400)
        print(
            f"lambda={lam:.17g} "
            f"B_1200={coarse:.17g} "
            f"B_2400={fine:.17g} "
            f"panel_delta={fine-coarse:.3e} "
            f"Bprime_centered={slope:.17g}"
        )

    slopes = []
    for index in range(15):
        lam = LOWER + (UPPER - LOWER) * index / 14.0
        slopes.append((lam, centered_lambda_slope(lam, 1200)))
    lam_min, slope_min = min(slopes, key=lambda item: item[1])
    print(
        f"sampled_Bprime_min={slope_min:.17g} "
        f"at_lambda={lam_min:.17g} samples={len(slopes)}"
    )


if __name__ == "__main__":
    main()
