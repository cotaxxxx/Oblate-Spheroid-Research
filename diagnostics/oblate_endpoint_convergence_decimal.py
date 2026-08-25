"""Independent endpoint convergence diagnostic.

Evidence class: DIAGNOSTIC_ONLY / NOT_BINDING.
Derivation class: HIGH_PRECISION.

This implementation uses Python Decimal and a standalone tanh-sinh rule.  It
does not import or call the mpmath prototype under checker/.
"""

from decimal import Decimal, localcontext


def constants(prec):
    with localcontext() as c:
        c.prec = prec + 15
        one = Decimal(1)
        two = Decimal(2)
        a = one
        b = (one / two).sqrt()
        t = Decimal("0.25")
        p = one
        for _ in range(20):
            an = (a + b) / two
            bn = (a * b).sqrt()
            t -= p * (a - an) ** 2
            a, b, p = an, bn, two * p
            if abs(a - b) < Decimal(10) ** (-(prec + 5)):
                break
        pi = (a + b) ** 2 / (Decimal(4) * t)
        return +pi


def exp(x):
    return x.exp()


def sinh(x):
    ex = exp(x)
    em = Decimal(1) / ex
    return (ex - em) / Decimal(2)


def cosh(x):
    ex = exp(x)
    em = Decimal(1) / ex
    return (ex + em) / Decimal(2)


def tanh(x):
    ex2 = exp(Decimal(2) * x)
    return (ex2 - 1) / (ex2 + 1)


def atan_series(z, eps):
    z2 = z * z
    term = z
    total = z
    n = 1
    while True:
        term *= -z2
        add = term / Decimal(2 * n + 1)
        total += add
        if abs(add) < eps:
            return total
        n += 1


def atan_nonnegative(x, pi, eps):
    if x == 0:
        return Decimal(0)
    if x > 1:
        return pi / 2 - atan_nonnegative(1 / x, pi, eps)
    # Reduce [sqrt(2)-1,1] around pi/4 for rapid convergence.
    if x > Decimal("0.4"):
        return pi / 4 + atan_series((x - 1) / (x + 1), eps)
    return atan_series(x, eps)


def alpha_and_ratio(gamma, pi, eps):
    if gamma < 0 or gamma > 1:
        tiny = Decimal(100) * eps
        if gamma > 1 and gamma - 1 < tiny:
            gamma = Decimal(1)
        else:
            raise ArithmeticError(("gamma", gamma))
    y2 = 1 - gamma * gamma
    if y2 <= 0:
        return Decimal(0), Decimal(1)
    y = y2.sqrt()
    if gamma == 0:
        alpha = pi / 2
    else:
        alpha = atan_nonnegative(y / gamma, pi, eps)
    return alpha, alpha / y


def b_density(s, lam, pi, eps):
    if s == 0:
        return Decimal(0)
    mu = 1 - s * s
    w = (lam * lam * (1 - mu * mu) + mu * mu).sqrt()
    qhat = 2 + (lam * lam - 1) * s * s
    gamma = lam * s / (w * qhat.sqrt())
    alpha, ratio = alpha_and_ratio(gamma, pi, eps)
    bracket = (1 - s * s) * (2 - s * s) + lam * lam * (2 * s * s - s ** 4)
    a_gamma_t = -lam * s * bracket / (w * qhat * qhat.sqrt())
    return s * (-mu * alpha * alpha - 2 * ratio * a_gamma_t)


def tanh_sinh(f, a, b, pi, h, tmax=Decimal(6)):
    mid = (a + b) / 2
    half = (b - a) / 2
    kmax = int(tmax / h)
    total = Decimal(0)
    for k in range(-kmax, kmax + 1):
        t = Decimal(k) * h
        sh = sinh(t)
        ch = cosh(t)
        u = (pi / 2) * sh
        th = tanh(u)
        cu = cosh(u)
        x = mid + half * th
        weight = half * (pi / 2) * ch / (cu * cu)
        total += f(x) * weight
    return h * total


def b_value(lam, prec, split, h):
    with localcontext() as c:
        c.prec = prec + 15
        pi = constants(prec + 10)
        eps = Decimal(10) ** (-(prec + 8))
        upper = Decimal(2).sqrt()
        fn = lambda s: b_density(s, lam, pi, eps)
        if split:
            value = tanh_sinh(fn, Decimal(0), Decimal(1), pi, h)
            value += tanh_sinh(fn, Decimal(1), upper, pi, h)
        else:
            value = tanh_sinh(fn, Decimal(0), upper, pi, h)
        c.prec = prec
        return +value, +pi


def root_value(prec, split, h):
    with localcontext() as c:
        c.prec = prec + 10
        x0, x1 = Decimal("0.63"), Decimal("0.65")
        f0, _ = b_value(x0, prec, split, h)
        f1, _ = b_value(x1, prec, split, h)
        target = Decimal(10) ** (-(prec - 8))
        for _ in range(30):
            x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
            if abs(x2 - x1) < target:
                return +x2
            x0, f0 = x1, f1
            x1 = x2
            f1, _ = b_value(x1, prec, split, h)
        raise ArithmeticError("secant root did not converge")


def run(prec, h):
    with localcontext() as c:
        c.prec = prec
        one = Decimal(1)
        bu, pi = b_value(one, prec, False, h)
        bs, _ = b_value(one, prec, True, h)
        expected = pi * pi / 32
        ru = root_value(prec, False, h)
        rs = root_value(prec, True, h)
        print("PREC", prec, "h", h)
        print("b unsplit", bu)
        print("b split  ", bs)
        print("b exact  ", expected)
        print("b split-unsplit", bs - bu)
        print("b unsplit-exact", bu - expected)
        print("root unsplit", ru)
        print("root split  ", rs)
        print("root split-unsplit", rs - ru)


if __name__ == "__main__":
    run(50, Decimal("0.04"))
    run(80, Decimal("0.025"))
