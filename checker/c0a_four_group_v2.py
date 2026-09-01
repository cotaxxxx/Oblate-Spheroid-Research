"""Raw-audited four-group C0a Arb kernel (checker transcription)."""
from checker import global_axial_c0_checker as base


def _known_nonnegative(x):
    """Intersect an Arb enclosure with the mathematically known half-line x>=0."""
    lower = max(base.arb(0), x.lower())
    upper = x.upper()
    if upper < lower:
        raise ValueError("empty exact nonnegative intersection")
    return base._box(lower, upper)


def _positive_q_powers(q):
    """Independent monotone endpoint construction for positive q powers."""
    lower = q.lower()
    upper = q.upper()
    if lower <= 0:
        raise ValueError("C0a checker requires q.lower() > 0 for positive powers")

    lower2 = lower * lower
    lower4 = lower2 * lower2
    lower5 = lower4 * lower
    lower6 = lower5 * lower
    upper2 = upper * upper
    upper4 = upper2 * upper2
    upper5 = upper4 * upper
    upper6 = upper5 * upper
    return (
        base._box(lower4, upper4),
        base._box(lower5, upper5),
        base._box(lower6, upper6),
        base._box(lower4 * lower.sqrt(), upper4 * upper.sqrt()),
        base._box(lower5 * lower.sqrt(), upper5 * upper.sqrt()),
    )


def _fourth_even_enclosure(x):
    """Independent endpoint enclosure for the mathematically nonnegative x^4."""
    lower = x.lower()
    upper = x.upper()
    bound = max(abs(lower), abs(upper))
    bound2 = bound * bound
    bound4 = bound2 * bound2
    return base._box(base.arb(0), bound4)


def _primitives(s, t, L):
    # Independent transcription of the factorized nonnegative q geometry.
    s = _known_nonnegative(s)
    x = _known_nonnegative(s * s)
    mu = 1 - x
    eps = _known_nonnegative(x * (2 - x))
    L2 = _known_nonnegative(L * L)
    L4 = L2 * L2
    delta = t - mu
    delta_sq = _known_nonnegative(delta * delta)
    A = 1 - t * mu
    q = eps + L2 * delta_sq
    W2 = mu * mu + L2 * eps
    W = W2.sqrt()
    rootq = q.sqrt()
    gam = L * A / (W * rootq)
    h = mu * (1 - L2) + L2 * t
    u = _known_nonnegative(base._unit_nonnegative(eps * h * h / (W2 * q)))

    n = -mu * q - A * L2 * delta
    m = (-L2 * eps) * q - 3 * n * L2 * delta
    m_first = L4 * eps * delta - 3 * L2 * n
    p = m_first * q - 5 * m * L2 * delta
    p_first = (4 * L4 * eps) * q - 3 * L2 * delta * m_first - 5 * L2 * m
    big_q = p_first * q - 7 * p * L2 * delta
    return s, x, mu, eps, A, delta, delta_sq, gam, u, L2, q, rootq, W, W2, n, m, p, big_q


def _k0_factored(x, mu, eps, A, delta_sq, t, L, L2, W, q9h):
    """Independent transcription of the exact factored K0 polynomial."""
    xm1 = x - 1

    # Polynomial W from the symbolic factorization, evaluated by x-Horner blocks.
    base_poly = (((3 * x - 12) * x + 20) * x - 16) * x - 1
    t_poly = ((8 * x - 24) * x + 14) * x + 2
    xm1_sq = _known_nonnegative(xm1 * xm1)
    Wcoef = base_poly + t * t_poly - t * t * xm1_sq

    # S = 8*x^2 - 16*x + 9 + 9*t*(x-1).
    Scoef = (8 * x - 16) * x + 9 + 9 * t * xm1

    delta4 = _known_nonnegative(delta_sq * delta_sq)
    eps2 = _known_nonnegative(eps * eps)
    mu2 = _known_nonnegative(mu * mu)

    b3 = -8 * eps * delta4
    b2 = -4 * delta_sq * Wcoef
    b1 = -3 * eps * A * Scoef
    b0 = 4 * eps2 * mu2
    G = ((b3 * L2 + b2) * L2 + b1) * L2 + b0

    L3 = L2 * L
    return 6 * L3 * eps * G / (W * q9h)


def _note_width(stats, chart, values):
    table = stats.setdefault("four_group_width_max", {"series": [None]*4, "direct": [None]*4})
    row = table[chart]
    for j, value in enumerate(values):
        radius = value.rad()
        if row[j] is None or radius.upper() > row[j].upper():
            row[j] = radius


def density(s, t, L, stats):
    s, x, mu, eps, A, delta, delta_sq, gam, u, L2, q, rootq, W, W2, n, m, p, big_q = _primitives(s, t, L)
    chart = "series" if u.upper() <= base.USTAR else "direct"
    r0, r1, r2, r3 = base._R(u, gam, stats)

    # q is positive on C0a; use endpoint monotonicity rather than repeated
    # ball multiplication for all denominator powers.
    q4, q5, q6, q9h, q11h = _positive_q_powers(q)
    L3 = L2 * L
    L4 = L2 * L2
    W3 = W2 * W
    W4 = W2 * W2
    n2 = _known_nonnegative(n * n)
    n3 = n2 * n
    n4 = _fourth_even_enclosure(n)

    # K0 is independently evaluated from the exact factored polynomial.
    # K1/K2 stay on the audited recursive transcription for this experiment.
    a1 = 24 * mu * n * m * q - 6 * A * m * m - 8 * A * n * p
    a2 = 8 * mu * n3 * q - 12 * A * n2 * m
    k0 = _k0_factored(x, mu, eps, A, delta_sq, t, L, L2, W, q9h)
    k1 = L2 * a1 / (W2 * q5)
    k2 = L3 * a2 / (W3 * q11h)
    k3 = -2 * A * L4 * n4 / (W4 * q6)

    pieces = (r0*k0, r1*k1, r2*k2, r3*k3)
    _note_width(stats, chart, pieces)
    return s * (pieces[0] + pieces[1] + pieces[2] + pieces[3])
