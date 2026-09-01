"""Raw-audited four-group C0a Arb kernel (checker transcription)."""
from checker import global_axial_c0_checker as base


def _primitives(s, t, L):
    mu = 1 - s * s
    eps = 1 - mu * mu
    L2 = L * L
    L4 = L2 * L2
    delta = t - mu
    A = 1 - t * mu
    q = eps + L2 * delta * delta
    W2 = mu * mu + L2 * eps
    W = W2.sqrt()
    rootq = q.sqrt()
    gam = L * A / (W * rootq)
    h = mu * (1 - L2) + L2 * t
    u = base._unit_nonnegative(eps * h * h / (W2 * q))

    n = -mu * q - A * L2 * delta
    m = (-L2 * eps) * q - 3 * n * L2 * delta
    m_first = L4 * eps * delta - 3 * L2 * n
    p = m_first * q - 5 * m * L2 * delta
    p_first = (4 * L4 * eps) * q - 3 * L2 * delta * m_first - 5 * L2 * m
    big_q = p_first * q - 7 * p * L2 * delta
    return mu, A, gam, u, L2, q, rootq, W, W2, n, m, p, big_q


def _note_width(stats, chart, values):
    table = stats.setdefault("four_group_width_max", {"series": [None]*4, "direct": [None]*4})
    row = table[chart]
    for j, value in enumerate(values):
        radius = value.rad()
        if row[j] is None or radius.upper() > row[j].upper():
            row[j] = radius


def density(s, t, L, stats):
    mu, A, gam, u, L2, q, rootq, W, W2, n, m, p, big_q = _primitives(s, t, L)
    chart = "series" if u.upper() <= base.USTAR else "direct"
    r0, r1, r2, r3 = base._R(u, gam, stats)

    # Independent transcription of q products and the four common denominators.
    qq = q * q
    q4 = qq * qq
    q5 = q4 * q
    q6 = q5 * q
    L3 = L2 * L
    L4 = L2 * L2
    W3 = W2 * W
    W4 = W2 * W2
    n2 = n * n
    n3 = n2 * n
    n4 = n2 * n2

    a0 = 8 * mu * p * q - 2 * A * big_q
    a1 = 24 * mu * n * m * q - 6 * A * m * m - 8 * A * n * p
    a2 = 8 * mu * n3 * q - 12 * A * n2 * m
    k0 = L * a0 / (W * q4 * rootq)
    k1 = L2 * a1 / (W2 * q5)
    k2 = L3 * a2 / (W3 * q5 * rootq)
    k3 = -2 * A * L4 * n4 / (W4 * q6)

    pieces = (r0*k0, r1*k1, r2*k2, r3*k3)
    _note_width(stats, chart, pieces)
    return s * (pieces[0] + pieces[1] + pieces[2] + pieces[3])
