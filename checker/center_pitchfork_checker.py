#!/usr/bin/env python3
"""PROTOTYPE / NOT_BINDING Arb checker for center pitchfork cubic coefficient c3_ob."""
from fractions import Fraction
from math import isqrt
from flint import arb, ctx
from checker.endpoint_interval_checker import _point, _box

BITS = 192
PANELS = 4096
LAM_N = 64
DEG = 50
USTAR = arb(3) / 5
SQRT2 = 'sqrt2'


def _partition(panels):
    root = arb(2).sqrt()
    rational_end = isqrt(2 * panels * panels)
    vals = [Fraction(i, panels) for i in range(panels + 1)]
    vals.extend(Fraction(i, panels) for i in range(panels + 1, rational_end + 1))
    return vals + [SQRT2], root


def _coeffs():
    out = [Fraction(1)]
    c = Fraction(1)
    for k in range(DEG + 2):
        c *= Fraction((2 * k + 1) ** 2, 2 * (k + 1) * (2 * k + 3))
        out.append(c)
    return out


COEFFS = _coeffs()


def _series(u, gamma):
    R = arb(0)
    Rp = arb(0)
    Rpp = arb(0)
    Rppp = arb(0)
    powers = [arb(1)]
    for _ in range(DEG + 1):
        powers.append(powers[-1] * u)
    for n, c in enumerate(COEFFS[: DEG + 1]):
        a = arb(c.numerator) / c.denominator
        R += a * powers[n]
        if n:
            Rp += n * a * powers[n - 1]
        if n > 1:
            Rpp += n * (n - 1) * a * powers[n - 2]
        if n > 2:
            Rppp += n * (n - 1) * (n - 2) * a * powers[n - 3]
    U = u.upper()
    c = COEFFS[DEG + 1]
    cn = arb(c.numerator) / c.denominator
    R += _box(arb(0), cn * powers[DEG + 1].upper() / (1 - U))
    Rp += _box(arb(0), (DEG + 1) * cn * powers[DEG].upper() / (1 - U * arb(DEG + 2) / (DEG + 1)))
    Rpp += _box(arb(0), (DEG + 1) * DEG * cn * powers[DEG - 1].upper() / (1 - U * arb(DEG + 2) / DEG))
    Rppp += _box(arb(0), (DEG + 1) * DEG * (DEG - 1) * cn * powers[DEG - 2].upper() / (1 - U * arb(DEG + 2) / (DEG - 1)))
    Rg = -2 * gamma * Rp
    Rgg = 4 * gamma * gamma * Rpp - 2 * Rp
    Rggg = -8 * gamma * gamma * gamma * Rppp + 12 * gamma * Rpp
    return R, Rg, Rgg, Rggg


def _density(s, L):
    s2 = s * s
    mu = 1 - s2
    mu2 = mu * mu
    e = 1 - mu2
    L2 = L * L
    L3 = L * L2
    L4 = L2 * L2
    L5 = L * L4
    q = e + L2 * mu2
    w2 = mu2 + L2 * e
    w = w2.sqrt()
    gam = L / (w * q.sqrt())
    u = e * mu2 * (1 - L2) * (1 - L2) / (w2 * q)

    gt = -L * mu * e * (1 - L2) / (w * q * q.sqrt())
    gtt = L3 * e * (2 * L2 * mu2 - 2 * mu2 - 1) / (w * q * q * q.sqrt())
    gttt = 3 * L3 * mu * e * (2 * L4 * mu2 - L2 * mu2 - 3 * L2 - mu2 + 1) / (w * q * q * q * q.sqrt())
    p4 = 8 * L4 * mu2 * mu2 + 4 * L2 * mu2 * mu2 - 24 * L2 * mu2 - 12 * mu2 * mu2 + 9 * mu2 + 3
    gtttt = 3 * L5 * e * p4 / (w * q * q * q * q * q.sqrt())

    if u.upper() <= USTAR:
        R, Rg, Rgg, Rggg = _series(u, gam)
    else:
        R = u.sqrt().asin() / u.sqrt()
        Rg = (gam * R - 1) / u
        Rgg = ((R + gam * Rg) * u + 2 * gam * (gam * R - 1)) / (u * u)
        Rggg = (3 * gam * (2 * gam * gam + 3) * R - (11 * gam * gam + 4)) / (u * u * u)

    Ctt = Rgg * gt * gt * gt + 3 * Rg * gt * gtt + R * gttt
    Cttt = Rggg * gt * gt * gt * gt + 6 * Rgg * gt * gt * gtt + 3 * Rg * gtt * gtt + 4 * Rg * gt * gttt + R * gtttt
    return (s / 6) * (8 * mu * Ctt - 2 * Cttt)


def _int(a, b, panels=PANELS):
    grid, root = _partition(panels)
    L = _box(_point(a), _point(b))
    total = arb(0)
    for x, y in zip(grid, grid[1:]):
        xx = root if x == SQRT2 else _point(x)
        yy = root if y == SQRT2 else _point(y)
        total += _density(_box(xx, yy), L) * (yy - xx)
    return total


def _boxes(a, b, n):
    d = (b - a) / n
    return [(a + i * d, a + (i + 1) * d) for i in range(n)]


def verify():
    ctx.prec = BITS
    worst = None
    gate = True
    for l, r in _boxes(Fraction(2, 5), Fraction(83, 200), LAM_N):
        v = _int(l, r)
        good = v.upper() < 0
        gate &= bool(good)
        if worst is None or v.upper() > worst[0]:
            worst = (v.upper(), l, r, v)

    sphere = _int(Fraction(1), Fraction(1))
    sphere_ok = bool(sphere.contains(_point(Fraction(-8, 9))))

    left = _int(Fraction(2, 5), Fraction(2, 5))
    midq = Fraction(4079588603, 10_000_000_000)
    mid = _int(midq, midq)
    right = _int(Fraction(83, 200), Fraction(83, 200))

    print('CENTER_PITCHFORK_CHECKER — PROTOTYPE / NOT_BINDING')
    print('C3_NEG_ALL', 'PASS' if gate else 'UNRESOLVED', 'weakest_box', worst[1], worst[2], 'enclosure', worst[3])
    print('SPHERE_C3_NEG_8_9', 'PASS' if sphere_ok else 'FAIL', 'enclosure', sphere)
    print('REPORTED_NOT_GATING C3_2_5', left)
    print('REPORTED_NOT_GATING C3_LAMBDA_C_APPROX', mid)
    print('REPORTED_NOT_GATING C3_83_200', right)
    final_ok = gate and sphere_ok
    print('LOGICAL_FINAL_CLAIM', 'PASS' if final_ok else 'UNRESOLVED', 'c3_ob(lambda)<0 on [2/5,83/200]; sphere containment control gating')
    if not final_ok:
        raise SystemExit('UNRESOLVED')


if __name__ == '__main__':
    verify()
