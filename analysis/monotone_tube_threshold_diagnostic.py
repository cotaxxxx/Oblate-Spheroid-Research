#!/usr/bin/env python3
"""DIAGNOSTIC_ONLY threshold comparison for two fixed monotone-tube boxes.

The fixed initial contract and producer are unchanged. This compares
u* in {1/4,1/2,3/5} on exactly two previously identified boxes:
  (ti,li)=(0,0) first box,
  (ti,li)=(0,7) prior maximum-radius box.

Ordinary cells use:
  u_hi <= u*       -> u_upper
  u_lo >= u*       -> gamma_lower
  u_lo < u* < u_hi -> termwise intersection of both rigorous charts
when both are valid. T1/T2/T3 are intersected separately.

For this diagnostic only, A is tightened by the exact positive-sum identity
A = 1-t*mu = (1-t)+t*s^2 before forming gamma and A/sqrt(q). This does not
modify the fixed initial producer or its contract.
"""
from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from flint import arb, ctx

from producer.endpoint_interval_producer import SQRT2, _box, _partition, _point, _series
from producer.monotone_tube_interval_producer import (
    BITS,L_LEFT,L_RIGHT,L_SPLITS,SERIES_DEGREE,S_PANELS,
    T_LEFT,T_RIGHT,T_SPLITS,_arb_interval,_nonnegative_sqrt_hull,
    _pow,_quantities,_split,_square,_unit_hull,
)

STATUS="DIAGNOSTIC_ONLY / NOT_BINDING"
THRESHOLDS=(Fraction(1,4),Fraction(1,2),Fraction(3,5))
TARGETS=((0,0,"FIRST"),(0,7,"PRIOR_MAX"))


def _intersection(x,y):
    lo=max(x.lower(),y.lower()); hi=min(x.upper(),y.upper())
    if hi < lo: raise ValueError("empty rigorous intersection")
    return _box(lo,hi)


def _angle_data(s,t,lam):
    e,gap,mu,d,lam2,A,q,w2,w,ht,H=_quantities(s,t,lam)
    if not q.lower()>0: raise ValueError("ordinary diagnostic requires q>0")
    A=_intersection(A,(1-t)+t*e)
    sq=q.sqrt(); gamma=_unit_hull(lam*A/(w*sq)); u0=_unit_hull(e*gap*_square(ht)/(w2*q))
    glo=max(arb(0),gamma.lower()); ghi=min(arb(1),gamma.upper())
    ulo=max(u0.lower(),arb(1)-ghi*ghi); uhi=min(u0.upper(),arb(1)-glo*glo)
    if uhi<ulo: raise ValueError("inconsistent gamma/u enclosures")
    u=_box(ulo,uhi)
    gc_lo=max(arb(0),arb(1)-u.upper()).sqrt(); gc_hi=max(arb(0),arb(1)-u.lower()).sqrt()
    g2lo=max(gamma.lower(),gc_lo); g2hi=min(gamma.upper(),gc_hi)
    if g2hi<g2lo: raise ValueError("empty reciprocal gamma/u intersection")
    gamma=_box(g2lo,g2hi)
    return e,gap,mu,d,lam2,A,q,w2,w,ht,H,sq,gamma,u


def _terms(data,s,lam,R,Rg):
    e,gap,mu,d,lam2,A,q,w2,w,ht,H,sq,gamma,u=data
    lam3=lam2*lam; rho=s/sq; phi=d/sq; Ahat=A/sq
    return (
        -4*mu*R*lam*_pow(rho,3)*H/w,
        -2*Rg*lam2*H*H*Ahat*_pow(rho,5)/w2,
        -2*R*lam3*Ahat*_pow(rho,3)*(3*phi*H-gap*sq)/w,
    )


def _ordinary_terms(s,t,lam,threshold):
    data=_angle_data(s,t,lam); *_,gamma,u=data; th=_point(threshold)
    def u_terms():
        if not u.upper()<1: raise ValueError("u chart requires u<1")
        R,_=_series(u,"Psi",SERIES_DEGREE,clamped_nonnegative=True)
        Psip,_=_series(u,"Psi_prime",SERIES_DEGREE,clamped_nonnegative=True)
        return _terms(data,s,lam,R,-2*gamma*Psip)
    def g_terms():
        if not u.lower()>0: raise ValueError("gamma chart requires u>0")
        R=gamma.acos()/u.sqrt(); Rg=(gamma*R-1)/u
        return _terms(data,s,lam,R,Rg)
    if u.upper()<=th: return "u_upper",u_terms()
    if u.lower()>=th: return "gamma_lower",g_terms()
    u_ok=bool(u.upper()<1); g_ok=bool(u.lower()>0)
    if u_ok and g_ok:
        ut=u_terms(); gt=g_terms()
        return "intersection",tuple(_intersection(a,b) for a,b in zip(ut,gt))
    if u_ok: return "u_upper_cross_only",u_terms()
    if g_ok: return "gamma_lower_cross_only",g_terms()
    raise ValueError(f"crossing cell has neither valid chart: u={u}")


def box_record(ti,li,threshold,sends,sqrt2,tboxes,lboxes):
    tl,tr=tboxes[ti]; ll,lr=lboxes[li]; t=_arb_interval(tl,tr); lam=_arb_interval(ll,lr)
    total=arb(0); T=[arb(0),arb(0),arb(0)]; by=defaultdict(lambda:[arb(0),arb(0),arb(0)]); counts=defaultdict(int)
    for sl,sr in zip(sends,sends[1:]):
        left=sqrt2 if sl==SQRT2 else _point(sl); right=sqrt2 if sr==SQRT2 else _point(sr); s=_box(left,right); width=right-left
        chart,terms=_ordinary_terms(s,t,lam,threshold)
        counts[chart]+=1
        for j,x in enumerate(terms):
            c=x*width; T[j]+=c; by[chart][j]+=c; total+=c
    return {"t_box":[str(tl),str(tr)],"lambda_box":[str(ll),str(lr)],"total":total,"terms":T,"by":dict(by),"counts":dict(counts)}


def f(x): return f"mid={x.mid().str(14)} rad={x.rad().str(14)}"


def main():
    ctx.prec=BITS; sends,sqrt2=_partition(S_PANELS); tboxes=_split(T_LEFT,T_RIGHT,T_SPLITS); lboxes=_split(L_LEFT,L_RIGHT,L_SPLITS)
    print("MONOTONE_TUBE U-THRESHOLD DIAGNOSTIC")
    print("fixed initial contract unchanged; diagnostic only; two target boxes")
    for th in THRESHOLDS:
        print(f"\n=== u*={th} ===")
        for ti,li,label in TARGETS:
            r=box_record(ti,li,th,sends,sqrt2,tboxes,lboxes)
            print(label,r["t_box"],r["lambda_box"],"counts",r["counts"])
            print(" total",f(r["total"]),"T2",f(r["terms"][1]))
            for chart in ("gamma_lower","u_upper","intersection","u_upper_cross_only","gamma_lower_cross_only"):
                if chart in r["by"]: print(f"  {chart} T2",f(r["by"][chart][1]))

if __name__=="__main__": main()
