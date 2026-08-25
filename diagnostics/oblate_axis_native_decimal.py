"""Native center-axis degeneracy diagnostic.

Evidence class: DIAGNOSTIC_ONLY / NOT_BINDING.
Derivation class: HIGH_PRECISION.

The calculation evaluates the native axial stationary equation g_axis_ob at
positive and negative t, forms its centered slope at t=0, Richardson-
extrapolates that slope, and solves for its zero in lambda.
"""

from decimal import Decimal, localcontext

from oblate_convergence_decimal import (
    alpha_and_ratio,
    constants,
    tanh_sinh,
)


def g_density(s, t, lam, pi, eps):
    if s == 0:
        return Decimal(0)
    mu = 1 - s * s
    a = 1 - t * mu
    q = 1 - mu * mu + lam * lam * (mu - t) ** 2
    w = (lam * lam * (1 - mu * mu) + mu * mu).sqrt()
    gamma = lam * a / (w * q.sqrt())
    alpha, ratio = alpha_and_ratio(gamma, pi, eps)
    numerator = -mu * q - a * lam * lam * (t - mu)
    gamma_t = lam * numerator / (w * q * q.sqrt())
    return s * (-mu * alpha * alpha - 2 * a * ratio * gamma_t)


def g_value(t, lam, prec, step, split=True):
    with localcontext() as c:
        c.prec = prec + 18
        pi = constants(prec + 12)
        eps = Decimal(10) ** (-(prec + 10))
        upper = Decimal(2).sqrt()
        fn = lambda s: g_density(s, t, lam, pi, eps)
        if split:
            value = tanh_sinh(fn, Decimal(0), Decimal(1), pi, step)
            value += tanh_sinh(fn, Decimal(1), upper, pi, step)
        else:
            value = tanh_sinh(fn, Decimal(0), upper, pi, step)
        c.prec = prec
        return +value


def center_slope(lam, prec, step, h0, levels):
    """Richardson limit of [g(h)-g(-h)]/(2h) as h -> 0."""
    with localcontext() as c:
        c.prec = prec + 12
        rows = []
        h = h0
        for k in range(levels):
            gp = g_value(h, lam, prec, step)
            gm = g_value(-h, lam, prec, step)
            row = [(gp - gm) / (2 * h)]
            for j in range(1, k + 1):
                factor = Decimal(4) ** j
                refined = row[j - 1] + (row[j - 1] - rows[k - 1][j - 1]) / (
                    factor - 1
                )
                row.append(refined)
            rows.append(row)
            h /= 2
        c.prec = prec
        return +rows[-1][-1]


def axis_root(prec, step, h0, levels):
    with localcontext() as c:
        c.prec = prec + 10
        x0 = Decimal("0.40")
        x1 = Decimal("0.42")
        f0 = center_slope(x0, prec, step, h0, levels)
        f1 = center_slope(x1, prec, step, h0, levels)
        target = Decimal(10) ** (-(prec - 12))
        for _ in range(24):
            x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
            if abs(x2 - x1) < target:
                return +x2, center_slope(x2, prec, step, h0, levels)
            x0, f0 = x1, f1
            x1 = x2
            f1 = center_slope(x1, prec, step, h0, levels)
        raise ArithmeticError("native axis root did not converge")


def run(prec, step, h0, levels):
    root, residual = axis_root(prec, step, h0, levels)
    print("PREC", prec, "step", step, "h0", h0, "levels", levels)
    print("lambda_axis_ob", root)
    print("slope residual", residual)


if __name__ == "__main__":
    run(50, Decimal("0.04"), Decimal("0.02"), 7)
    run(80, Decimal("0.025"), Decimal("0.02"), 9)
