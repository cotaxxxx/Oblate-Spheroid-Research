#!/usr/bin/env python3
"""PROTOTYPE / NOT_BINDING Arb producer for center pitchfork cubic coefficient c3_ob."""
from fractions import Fraction
from flint import arb, ctx
from producer.endpoint_interval_producer import _point, _box, _partition, SQRT2

BITS = 160
PANELS = 4096
LAM_N = 64
DEG = 50
USTAR = arb(3) / 5


def _coeffs():
    out = [Fraction(1)]
    c = Fraction(1)
    for k in range(DEG + 2):
        c *= Fraction((2 * k + 1) ** 2, 2 * (k + 1) * (2 * k + 3))
        out.append(c)
    return out


COEFFS = _coeffs()


def _psi_bundle(u, gamma):
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


def _density(s, lam):
    s2 = s * s
    mu = 1 - s2
    mu2 = mu * mu
    e = 1 - mu2
    l2 = lam * lam
    l3 = lam * l2
    l4 = l2 * l2
    l5 = lam * l4
    q = e + l2 * mu2
    w2 = mu2 + l2 * e
    w = w2.sqrt()
    gamma = lam / (w * q.sqrt())
    u = e * mu2 * (1 - l2) * (1 - l2) / (w2 * q)

    gt = -lam * mu * e * (1 - l2) / (w * q * q.sqrt())
    gtt = l3 * e * (2 * l2 * mu2 - 2 * mu2 - 1) / (w * q * q * q.sqrt())
    gttt = 3 * l3 * mu * e * (2 * l4 * mu2 - l2 * mu2 - 3 * l2 - mu2 + 1) / (w * q * q * q * q.sqrt())
    poly4 = 8 * l4 * mu2 * mu2 + 4 * l2 * mu2 * mu2 - 24 * l2 * mu2 - 12 * mu2 * mu2 + 9 * mu2 + 3
    gtttt = 3 * l5 * e * poly4 / (w * q * q * q * q * q.sqrt())

    if u.upper() <= USTAR:
        R, Rg, Rgg, Rggg = _psi_bundle(u, gamma)
    else:
        R = u.sqrt().asin() / u.sqrt()
        Rg = (gamma * R - 1) / u
        Rgg = ((R + gamma * Rg) * u + 2 * gamma * (gamma * R - 1)) / (u * u)
        Rggg = (3 * gamma * (2 * gamma * gamma + 3) * R - (11 * gamma * gamma + 4)) / (u * u * u)

    Ctt = Rgg * gt * gt * gt + 3 * Rg * gt * gtt + R * gttt
    Cttt = Rggg * gt * gt * gt * gt + 6 * Rgg * gt * gt * gtt + 3 * Rg * gtt * gtt + 4 * Rg * gt * gttt + R * gtttt
    return (s / 6) * (8 * mu * Ctt - 2 * Cttt)


def integrate(ll, rr, panels=PANELS):
    grid, root = _partition(panels)
    lam = _box(_point(ll), _point(rr))
    total = arb(0)
    for a, b in zip(grid, grid[1:]):
        aa = root if a == SQRT2 else _point(a)
        bb = root if b == SQRT2 else _point(b)
        total += _density(_box(aa, bb), lam) * (bb - aa)
    return total


def split(a, b, n):
    d = (b - a) / n
    return [(a + i * d, a + (i + 1) * d) for i in range(n)]


def run():
    ctx.prec = BITS
    worst = None
    gate_ok = True
    for ll, rr in split(Fraction(2, 5), Fraction(83, 200), LAM_N):
        x = integrate(ll, rr)
        good = x.upper() < 0
        gate_ok &= bool(good)
        if worst is None or x.upper() > worst[0]:
            worst = (x.upper(), ll, rr, x)

    sphere = integrate(Fraction(1), Fraction(1))
    exact_sphere = _point(Fraction(-8, 9))
    sphere_ok = bool(sphere.contains(exact_sphere))

    rep_left = integrate(Fraction(2, 5), Fraction(2, 5))
    rep_right = integrate(Fraction(83, 200), Fraction(83, 200))
    rep_mid = integrate(Fraction(4079588603, 10_000_000_000), Fraction(4079588603, 10_000_000_000))

    print('CENTER_PITCHFORK_PRODUCER — PROTOTYPE / NOT_BINDING')
    print('C3_NEG_ALL', 'PASS' if gate_ok else 'UNRESOLVED', 'weakest_box', worst[1], worst[2], 'enclosure', worst[3])
    print('SPHERE_C3_NEG_8_9', 'PASS' if sphere_ok else 'FAIL', 'enclosure', sphere)
    print('REPORTED_NOT_GATING C3_2_5', rep_left)
    print('REPORTED_NOT_GATING C3_LAMBDA_C_APPROX', rep_mid)
    print('REPORTED_NOT_GATING C3_83_200', rep_right)
    final_ok = gate_ok and sphere_ok
    print('LOGICAL_FINAL_CLAIM', 'PASS' if final_ok else 'UNRESOLVED', 'c3_ob(lambda)<0 on [2/5,83/200]; sphere containment control gating')
    if not final_ok:
        raise SystemExit('UNRESOLVED')


if __name__ == '__main__':
    run()
