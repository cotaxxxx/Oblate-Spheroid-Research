#!/usr/bin/env python3
"""REPORT_ONLY / NOT_GATING: print exact Arb midpoint/radius for center-axis evidence."""
from fractions import Fraction
from flint import ctx
import producer.center_axis_coefficient_producer as P
import checker.center_axis_coefficient_checker as C


def ball(v):
    return f"mid={v.mid().str(80)} rad={v.rad().str(80)}"


def report_producer():
    ctx.prec=P.BITS
    worst=None
    for ll,rr in P.split(Fraction(1,4),Fraction(1),P.MONO_N):
        x=P.integrate(ll,rr,True,P.REG_PANELS)
        if worst is None or x.lower()<worst[0]: worst=(x.lower(),ll,rr,x)
    vals={
        'GLOBAL_DERIV_POS_WEAKEST': worst[3],
        'POINT_2_5': P.integrate(Fraction(2,5),Fraction(2,5),False,P.POINT_PANELS),
        'POINT_83_200': P.integrate(Fraction(83,200),Fraction(83,200),False,P.POINT_PANELS),
        'SPHERE_H': P.integrate(Fraction(1),Fraction(1),False,P.POINT_PANELS),
        'SPHERE_HLAMBDA': P.integrate(Fraction(1),Fraction(1),True,P.POINT_PANELS),
    }
    print('PRODUCER_WEAKEST_BOX',worst[1],worst[2])
    for k,v in vals.items(): print('PRODUCER',k,ball(v))


def report_checker():
    ctx.prec=C.BITS
    worst=None
    for ll,rr in C._boxes(Fraction(1,4),Fraction(1),C.MONO_N):
        x=C._int(ll,rr,True,C.REG_PANELS)
        if worst is None or x.lower()<worst[0]: worst=(x.lower(),ll,rr,x)
    vals={
        'GLOBAL_DERIV_POS_WEAKEST': worst[3],
        'POINT_2_5': C._int(Fraction(2,5),Fraction(2,5),False,C.POINT_PANELS),
        'POINT_83_200': C._int(Fraction(83,200),Fraction(83,200),False,C.POINT_PANELS),
        'SPHERE_H': C._int(Fraction(1),Fraction(1),False,C.POINT_PANELS),
        'SPHERE_HLAMBDA': C._int(Fraction(1),Fraction(1),True,C.POINT_PANELS),
    }
    print('CHECKER_WEAKEST_BOX',worst[1],worst[2])
    for k,v in vals.items(): print('CHECKER',k,ball(v))

if __name__=='__main__':
    report_producer(); report_checker()
