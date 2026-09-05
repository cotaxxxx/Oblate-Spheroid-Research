#!/usr/bin/env python3
"""REPORT_ONLY / NOT_GATING exact enclosure printout for B center pitchfork evidence."""
from fractions import Fraction
from flint import ctx
import producer.center_pitchfork_producer as P
import checker.center_pitchfork_checker as C

WLO = Fraction(2, 5)
WHI = Fraction(5123, 12800)
MID = Fraction(4079588603, 10_000_000_000)
POINTS = [
    ('WEAKEST', WLO, WHI),
    ('C3_2_5', Fraction(2,5), Fraction(2,5)),
    ('C3_LAMBDA_C_APPROX', MID, MID),
    ('C3_83_200', Fraction(83,200), Fraction(83,200)),
    ('SPHERE_C3', Fraction(1), Fraction(1)),
]


def emit(prefix, name, v):
    print(prefix, name, 'mid=' + v.mid().str(80), 'rad=' + v.rad().str(80))


def main():
    print('CENTER_PITCHFORK_EXACT_ENCLOSURE_REPORT — REPORT_ONLY / NOT_GATING')
    ctx.prec = P.BITS
    for name, a, b in POINTS:
        emit('PRODUCER', name, P.integrate(a, b))
    ctx.prec = C.BITS
    for name, a, b in POINTS:
        emit('CHECKER', name, C._int(a, b))


if __name__ == '__main__':
    main()
