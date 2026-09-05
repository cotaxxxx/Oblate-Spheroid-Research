#!/usr/bin/env python3
"""DIAGNOSTIC_ONLY / NOT_BINDING: separate lambda-box width from s-panel width."""
from fractions import Fraction
from flint import ctx
from producer.center_axis_coefficient_producer import integrate

ctx.prec=160
for lam in [Fraction(2,5), Fraction(83,200)]:
    h=integrate(lam,lam,False)
    hp=integrate(lam,lam,True)
    print('lambda',lam,'H_POINT',h,'H_LAMBDA_POINT',hp)
