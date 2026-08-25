#!/usr/bin/env python3
"""Direct non-interval fold scan for the positive oblate axial branch.

Evidence class: DIAGNOSTIC_ONLY / NOT_BINDING.
Derivation class: NUMERICAL_DIAGNOSTIC.

This standard-library implementation uses composite Simpson quadrature and does
not import the mpmath prototype. It excludes the symmetry-forced root t=0 and
counts sign-changing roots on 0<t<1. A certified no-fold statement still
requires interval bounds for g and partial_t g.

Near t=1 this binary64 path records roots and g(1), but deliberately does not
estimate partial_t g: a centered stencil would leave the documented domain and
the endpoint derivative needs the endpoint-regular high-precision path.
"""

import math


def density(s, t, lam):
    if s == 0.0:
        return 0.0
    mu = 1.0 - s * s
    a = 1.0 - t * mu
    q = 1.0 - mu * mu + lam * lam * (mu - t) ** 2
    w = math.sqrt(lam * lam * (1.0 - mu * mu) + mu * mu)
    gamma = lam * a / (w * math.sqrt(q))
    gamma = max(-1.0, min(1.0, gamma))
    alpha = math.acos(gamma)
    ratio = 1.0 if alpha == 0.0 else alpha / math.sin(alpha)
    numerator = -mu * q - a * lam * lam * (t - mu)
    gamma_t = lam * numerator / (w * q ** 1.5)
    return s * (-mu * alpha * alpha - 2.0 * a * ratio * gamma_t)


def g_value(t, lam, panels=1200):
    if not (0.0 < t <= 1.0):
        raise ValueError("fold scan requires 0 < t <= 1")
    if panels % 2:
        raise ValueError("Simpson panel count must be even")
    lo, hi = 0.0, math.sqrt(2.0)
    h = (hi - lo) / panels
    total = density(lo, t, lam) + density(hi, t, lam)
    total += 4.0 * sum(density(lo + i * h, t, lam) for i in range(1, panels, 2))
    total += 2.0 * sum(density(lo + i * h, t, lam) for i in range(2, panels, 2))
    return total * h / 3.0


def bisect_root(lam, lo, hi):
    flo = g_value(lo, lam)
    for _ in range(45):
        mid = (lo + hi) / 2.0
        fmid = g_value(mid, lam)
        if flo * fmid <= 0.0:
            hi = mid
        else:
            lo, flo = mid, fmid
    return (lo + hi) / 2.0


def safe_centered_slope(root, lam, h=1.0e-5):
    """Return a centered diagnostic only when the stencil stays in-domain."""
    if root - h <= 0.0 or root + h > 1.0:
        return None
    return (g_value(root + h, lam) - g_value(root - h, lam)) / (2.0 * h)


def roots_at(lam, lo=0.0001, hi=1.0, samples=200):
    nodes = [lo + i * (hi - lo) / samples for i in range(samples + 1)]
    values = [g_value(t, lam) for t in nodes]
    roots = []
    for a, b, fa, fb in zip(nodes, nodes[1:], values, values[1:]):
        if fa * fb < 0.0:
            root = bisect_root(lam, a, b)
            roots.append((root, safe_centered_slope(root, lam)))
    return roots


def main():
    print("full axial branch window")
    full_window = [0.408] + [k / 100.0 for k in range(41, 65)]
    for lam in full_window:
        print(f"{lam:.3f}", roots_at(lam))
    print("fine endpoint window")
    for lam in (
        0.6430, 0.6432, 0.6434, 0.6435, 0.64354, 0.643545,
        0.6435457, 0.64354577, 0.643546, 0.64355, 0.6436,
        0.6438, 0.6440,
    ):
        print(f"{lam:.8f}", roots_at(lam, lo=0.98), "g(1)=", g_value(1.0, lam))


if __name__ == "__main__":
    main()
