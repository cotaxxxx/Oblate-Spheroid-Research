#!/usr/bin/env python3
"""Endpoint-regular axial evaluator for the oblate spheroid.

Evidence class: PROTOTYPE / NOT_AUDITED.

This module performs multiprecision candidate evaluation only.  It is not an
interval implementation and cannot produce CERTIFIED_ENCLOSURE results.

The pole endpoint uses mu = 1 - s**2 and analytically factored expressions, so
no extrapolation t -> 1 is used.
"""

from __future__ import annotations

from contextlib import contextmanager

import mpmath as mp


@contextmanager
def _workdps(dps: int):
    if dps < 20:
        raise ValueError("dps must be at least 20")
    with mp.workdps(dps):
        yield


def _validate_lambda(lam: mp.mpf) -> None:
    if not (mp.mpf("0") < lam <= mp.mpf("1")):
        raise ValueError("oblate axis ratio lambda must satisfy 0 < lambda <= 1")


def _unit_interval_value(value: mp.mpf) -> mp.mpf:
    """Remove only roundoff-sized excursions from the acos domain."""
    one = mp.mpf("1")
    slack = 64 * mp.eps
    if value > one and value - one <= slack:
        return one
    if value < -one and -one - value <= slack:
        return -one
    if not (-one <= value <= one):
        raise ArithmeticError(f"gamma outside [-1,1]: {value}")
    return value


def _alpha_over_sin_alpha(gamma: mp.mpf) -> tuple[mp.mpf, mp.mpf]:
    gamma = _unit_interval_value(gamma)
    alpha = mp.acos(gamma)
    if alpha == 0:
        return alpha, mp.mpf("1")
    return alpha, alpha / mp.sin(alpha)


def _transformed_geometry(s: mp.mpf, lam: mp.mpf) -> tuple[mp.mpf, ...]:
    """Geometry at t=1 after mu=1-s^2, with q=s^2*qhat."""
    mu = 1 - s * s
    w2 = lam * lam * (1 - mu * mu) + mu * mu
    qhat = 2 + (lam * lam - 1) * s * s
    w = mp.sqrt(w2)
    gamma = lam * s / (w * mp.sqrt(qhat))
    return mu, w, qhat, _unit_interval_value(gamma)


def boundary_energy_ob(lam, *, dps: int = 50):
    """Return E_lambda(1) by endpoint-regular tanh-sinh quadrature."""
    with _workdps(dps):
        lam = mp.mpf(lam)
        _validate_lambda(lam)
        upper = mp.sqrt(2)

        def density(s):
            if s == 0:
                return mp.mpf("0")
            _, _, _, gamma = _transformed_geometry(s, lam)
            alpha = mp.acos(gamma)
            # (1/2)dmu becomes s ds, and 1-mu=s^2 at t=1.
            return s**3 * alpha**2

        return +mp.quad(density, [0, upper], method="tanh-sinh")


def b_ob(lam, *, dps: int = 50):
    """Return b_ob(lambda)=g_axis_ob(1,lambda), without t extrapolation."""
    with _workdps(dps):
        lam = mp.mpf(lam)
        _validate_lambda(lam)
        upper = mp.sqrt(2)

        def density(s):
            if s == 0:
                return mp.mpf("0")
            mu, w, qhat, gamma = _transformed_geometry(s, lam)
            alpha, ratio = _alpha_over_sin_alpha(gamma)

            # At t=1, N=-mu*q-(1-t*mu)*lambda^2*(t-mu)
            # factors as -s^2*bracket.  Multiplying gamma_t by
            # A=(1-t*mu)=s^2 before evaluation removes the 1/s term.
            bracket = (1 - s * s) * (2 - s * s) + lam * lam * (
                2 * s * s - s**4
            )
            a_gamma_t = -lam * s * bracket / (w * qhat ** mp.mpf("1.5"))

            # g=(1/2)int[-mu*h + A*h'(gamma)*gamma_t]dmu,
            # h'= -2*alpha/sin(alpha); dmu=2s ds.
            return s * (-mu * alpha**2 - 2 * ratio * a_gamma_t)

        return +mp.quad(density, [0, upper], method="tanh-sinh")


def g_axis_ob(t, lam, *, dps: int = 50):
    """Return partial_t E_lambda(t) for -1<t<1.

    The same s substitution is used.  The exact endpoint t=1 is delegated to
    b_ob, whose factored formula is the canonical endpoint path.
    """
    with _workdps(dps):
        t = mp.mpf(t)
        lam = mp.mpf(lam)
        _validate_lambda(lam)
        if t == 1:
            return b_ob(lam, dps=dps)
        if not (-1 < t < 1):
            raise ValueError("t must satisfy -1 < t <= 1")
        upper = mp.sqrt(2)

        def density(s):
            if s == 0:
                return mp.mpf("0")
            mu = 1 - s * s
            a = 1 - t * mu
            q = 1 - mu * mu + lam * lam * (mu - t) ** 2
            w = mp.sqrt(lam * lam * (1 - mu * mu) + mu * mu)
            gamma = _unit_interval_value(lam * a / (w * mp.sqrt(q)))
            alpha, ratio = _alpha_over_sin_alpha(gamma)
            numerator = -mu * q - a * lam * lam * (t - mu)
            gamma_t = lam * numerator / (w * q ** mp.mpf("1.5"))
            return s * (-mu * alpha**2 - 2 * a * ratio * gamma_t)

        return +mp.quad(density, [0, upper], method="tanh-sinh")
