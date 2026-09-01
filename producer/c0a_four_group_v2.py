"""Raw-audited four-group C0a Arb kernel (producer transcription)."""
from producer import global_axial_c0_producer as base


def _geometry(s, t, lam):
    s2 = s * s
    mu = 1 - s2
    e = 1 - mu * mu
    l2 = lam * lam
    l4 = l2 * l2
    A = 1 - t * mu
    d = t - mu
    q = e + l2 * d * d
    w2 = mu * mu + l2 * e
    w = w2.sqrt()
    sq = q.sqrt()
    gamma = lam * A / (w * sq)
    h = mu * (1 - l2) + l2 * t
    u = base._unit_nonnegative(e * h * h / (w2 * q))
    N = -mu * q - A * l2 * d
    M = (-l2 * e) * q - 3 * N * l2 * d
    M1 = l4 * e * d - 3 * l2 * N
    P = M1 * q - 5 * M * l2 * d
    P1 = (4 * l4 * e) * q - 3 * l2 * d * M1 - 5 * l2 * M
    Q = P1 * q - 7 * P * l2 * d
    return mu, A, gamma, u, l2, q, sq, w, w2, N, M, P, Q


def _record(stats, chart, groups):
    rec = stats.setdefault("four_group_width_max", {"series": [None]*4, "direct": [None]*4})
    for i, value in enumerate(groups):
        r = value.rad()
        old = rec[chart][i]
        if old is None or r.upper() > old.upper():
            rec[chart][i] = r


def density(s, t, lam, stats):
    mu, A, gamma, u, l2, q, sq, w, w2, N, M, P, Q = _geometry(s, t, lam)
    chart = "series" if u.upper() <= base.USTAR else "direct"
    R, Rg, Rgg, Rggg = base._R_bundle(u, gamma, stats)

    # Deliberately use products, not interval powers. q^(9/2)=q4*sqrt(q).
    q2 = q * q
    q4 = q2 * q2
    q5 = q4 * q
    q6 = q5 * q
    l3 = l2 * lam
    l4 = l2 * l2
    w3 = w2 * w
    w4 = w2 * w2
    N2 = N * N
    N3 = N2 * N
    N4 = N2 * N2

    # Build each cancelling numerator before its single common-denominator division.
    num0 = 8 * mu * P * q - 2 * A * Q
    num1 = 24 * mu * N * M * q - 6 * A * M * M - 8 * A * N * P
    num2 = 8 * mu * N3 * q - 12 * A * N2 * M
    K0 = lam * num0 / (w * q4 * sq)
    K1 = l2 * num1 / (w2 * q5)
    K2 = l3 * num2 / (w3 * q5 * sq)
    K3 = -2 * A * l4 * N4 / (w4 * q6)

    groups = (R*K0, Rg*K1, Rgg*K2, Rggg*K3)
    _record(stats, chart, groups)
    return s * (groups[0] + groups[1] + groups[2] + groups[3])
