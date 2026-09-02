"""Raw-audited four-group C0a Arb kernel (producer transcription)."""
from producer import global_axial_c0_producer as base


def _nonnegative(x):
    """Intersect an Arb enclosure with the mathematically known half-line x>=0."""
    lo = max(base.arb(0), x.lower())
    hi = x.upper()
    if hi < lo:
        raise ValueError("empty exact nonnegative intersection")
    return base._box(lo, hi)


def _positive_q_powers(q):
    """Monotone endpoint enclosures for q^4,q^5,q^6,q^(9/2),q^(11/2)."""
    qlo = q.lower()
    qhi = q.upper()
    if qlo <= 0:
        raise ValueError("C0a positive-q power construction requires q.lower() > 0")

    qlo2 = qlo * qlo
    qlo4 = qlo2 * qlo2
    qlo5 = qlo4 * qlo
    qlo6 = qlo5 * qlo
    qhilo2 = qhi * qhi
    qhilo4 = qhilo2 * qhilo2
    qhilo5 = qhilo4 * qhi
    qhilo6 = qhilo5 * qhi

    qlo_sqrt = qlo.sqrt()
    qhi_sqrt = qhi.sqrt()
    return (
        base._box(qlo4, qhilo4),
        base._box(qlo5, qhilo5),
        base._box(qlo6, qhilo6),
        base._box(qlo4 * qlo_sqrt, qhilo4 * qhi_sqrt),
        base._box(qlo5 * qlo_sqrt, qhilo5 * qhi_sqrt),
    )


def _even_fourth_power(x):
    """Endpoint enclosure of x^4 using the known nonnegativity of an even power."""
    lo = x.lower()
    hi = x.upper()
    mag = max(abs(lo), abs(hi))
    mag2 = mag * mag
    mag4 = mag2 * mag2
    return base._box(base.arb(0), mag4)


def _geometry(s, t, lam):
    # Preserve exact nonnegative structure near s=0.  In particular, avoid
    # e = 1-mu^2, whose interval subtraction loses the cancellation mu~1.
    s = _nonnegative(s)
    x = _nonnegative(s * s)
    mu = 1 - x
    e = _nonnegative(x * (2 - x))
    l2 = _nonnegative(lam * lam)
    l4 = l2 * l2
    A = 1 - t * mu
    d = t - mu
    d2 = _nonnegative(d * d)
    q = e + l2 * d2
    w2 = mu * mu + l2 * e
    w = w2.sqrt()
    sq = q.sqrt()
    gamma = lam * A / (w * sq)
    h = mu * (1 - l2) + l2 * t
    u = _nonnegative(base._unit_nonnegative(e * h * h / (w2 * q)))
    N = -mu * q - A * l2 * d
    M = (-l2 * e) * q - 3 * N * l2 * d
    M1 = l4 * e * d - 3 * l2 * N
    P = M1 * q - 5 * M * l2 * d
    P1 = (4 * l4 * e) * q - 3 * l2 * d * M1 - 5 * l2 * M
    Q = P1 * q - 7 * P * l2 * d
    return s, x, mu, e, A, d, d2, gamma, u, l2, q, sq, w, w2, N, M, P, Q


def _factorized_k0(x, mu, e, A, d2, t, lam, l2, w, q9h):
    """Exact factorization 8*mu*P*q-2*A*Q = 6*l2*e*G, with G Horner-evaluated."""
    # W = -t^2(x-1)^2 + t(8x^3-24x^2+14x+2)
    #     + 3x^4-12x^3+20x^2-16x-1.
    xm1 = x - 1
    wx0 = (((3 * x - 12) * x + 20) * x - 16) * x - 1
    wx1 = ((8 * x - 24) * x + 14) * x + 2
    Wpoly = wx0 + t * wx1 - (t * t) * _nonnegative(xm1 * xm1)

    # S = 9*t*(x-1) + 8*x^2 - 16*x + 9.
    S = (8 * x - 16) * x + 9 + 9 * t * xm1

    d4 = _nonnegative(d2 * d2)
    e2 = _nonnegative(e * e)
    mu2 = _nonnegative(mu * mu)
    c3 = -8 * e * d4
    c2 = -4 * d2 * Wpoly
    c1 = -3 * e * A * S
    c0 = 4 * e2 * mu2
    G = ((c3 * l2 + c2) * l2 + c1) * l2 + c0
    l3 = l2 * lam
    return 6 * l3 * e * G / (w * q9h)


def _record(stats, chart, groups):
    rec = stats.setdefault("four_group_width_max", {"series": [None]*4, "direct": [None]*4})
    for i, value in enumerate(groups):
        r = value.rad()
        old = rec[chart][i]
        if old is None or r.upper() > old.upper():
            rec[chart][i] = r


def density(s, t, lam, stats):
    s, x, mu, e, A, d, d2, gamma, u, l2, q, sq, w, w2, N, M, P, Q = _geometry(s, t, lam)
    chart = "series" if u.upper() <= base.USTAR else "direct"
    R, Rg, Rgg, Rggg = base._R_bundle(u, gamma, stats)

    # q is strictly positive on C0a.  Construct its powers from endpoint
    # monotonicity instead of repeated ball multiplication, which can make the
    # relative radius exceed 100% on coarse boxes.
    q4, q5, q6, q9h, q11h = _positive_q_powers(q)
    l3 = l2 * lam
    l4 = l2 * l2
    w3 = w2 * w
    w4 = w2 * w2
    N2 = _nonnegative(N * N)
    N3 = N2 * N
    N4 = _even_fourth_power(N)

    # K0 uses the exact polynomial factorization; K1/K2 retain the audited
    # recursive numerators until their own factorizations are separately checked.
    num1 = 24 * mu * N * M * q - 6 * A * M * M - 8 * A * N * P
    num2 = 8 * mu * N3 * q - 12 * A * N2 * M
    K0 = _factorized_k0(x, mu, e, A, d2, t, lam, l2, w, q9h)
    K1 = l2 * num1 / (w2 * q5)
    K2 = l3 * num2 / (w3 * q11h)
    K3 = (-2 * A * l4 * N4) / (w4 * q6)

    groups = (R*K0, Rg*K1, Rgg*K2, Rggg*K3)
    _record(stats, chart, groups)
    return s * (groups[0] + groups[1] + groups[2] + groups[3])
