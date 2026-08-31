#!/usr/bin/env python3
"""DIAGNOSTIC_ONLY threshold comparison for oblate monotone-tube charts.

The fixed initial contract and producer are unchanged. This compares
u* in {1/4,1/2,3/5}. Ordinary cells use:
  u_hi <= u*       -> u_upper
  u_lo >= u*       -> gamma_lower
  u_lo < u* < u_hi -> termwise intersection of both rigorous charts
when both charts are valid. T1/T2/T3 are intersected separately so no
cross-chart correlation assumption is made.

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


def _intersection(x,y):
    lo=max(x.lower(),y.lower()); hi=min(x.upper(),y.upper())
    if hi < lo: raise ValueError("empty rigorous intersection")
    return _box(lo,hi)


def _angle_data(s,t,lam,degree):
    e,gap,mu,d,lam2,A,q,w2,w,ht,H=_quantities(s,t,lam)
    if not q.lower()>0: raise ValueError("ordinary diagnostic requires q>0")
    # Exact positive-sum form; intersect with the original algebraic form.
    Apos=(1-t)+t*e
    A=_intersection(A,Apos)
    sq=q.sqrt(); gamma=_unit_hull(lam*A/(w*sq)); u0=_unit_hull(e*gap*_square(ht)/(w2*q))
    glo=max(arb(0),gamma.lower()); ghi=min(arb(1),gamma.upper())
    ulo=max(u0.lower(),arb(1)-ghi*ghi); uhi=min(u0.upper(),arb(1)-glo*glo)
    if uhi<ulo: raise ValueError("inconsistent gamma/u enclosures")
    u=_box(ulo,uhi)
    gc_lo=max(arb(0),arb(1)-u.upper()).sqrt(); gc_hi=max(arb(0),arb(1)-u.lower()).sqrt()
    g2lo=max(gamma.lower(),gc_lo); g2hi=min(gamma.upper(),gc_hi)
    if g2hi<g2lo: raise ValueError("empty reciprocal gamma/u intersection")
    gamma=_box(g2lo,g2hi)
    return (e,gap,mu,d,lam2,A,q,w2,w,ht,H,sq,gamma,u)


def _terms_from_angle(data,lam,R,Rg):
    e,gap,mu,d,lam2,A,q,w2,w,ht,H,sq,gamma,u=data
    lam3=lam2*lam; rho=s_current/sq; phi=d/sq; Ahat=A/sq
    T1=-4*mu*R*lam*_pow(rho,3)*H/w
    T2=-2*Rg*lam2*H*H*Ahat*_pow(rho,5)/w2
    T3=-2*R*lam3*Ahat*_pow(rho,3)*(3*phi*H-gap*sq)/w
    return T1,T2,T3


def _ordinary_terms(s,t,lam,degree,threshold):
    global s_current
    s_current=s
    data=_angle_data(s,t,lam,degree)
    *_,gamma,u=data
    th=_point(threshold)

    def u_terms():
        if not u.upper()<1: raise ValueError("u chart requires u<1")
        R,_=_series(u,"Psi",degree,clamped_nonnegative=True)
        Psip,_=_series(u,"Psi_prime",degree,clamped_nonnegative=True)
        return _terms_from_angle(data,lam,R,-2*gamma*Psip)

    def g_terms():
        if not u.lower()>0: raise ValueError("gamma chart requires u>0")
        R=gamma.acos()/u.sqrt(); Rg=(gamma*R-1)/u
        return _terms_from_angle(data,lam,R,Rg)

    if u.upper() <= th:
        return "u_upper",u_terms()
    if u.lower() >= th:
        return "gamma_lower",g_terms()
    # Crossing: use both when both are valid, otherwise the one valid chart.
    u_ok=bool(u.upper()<1)
    g_ok=bool(u.lower()>0)
    if u_ok and g_ok:
        ut=u_terms(); gt=g_terms()
        return "intersection",tuple(_intersection(a,b) for a,b in zip(ut,gt))
    if u_ok:
        return "u_upper_cross_only",u_terms()
    if g_ok:
        return "gamma_lower_cross_only",g_terms()
    raise ValueError(f"crossing cell has neither valid chart: u={u}")


def _corner_terms(s,t,lam):
    e,gap,mu,d,lam2,A,q,w2,w,ht,H=_quantities(s,t,lam); lam3=lam2*lam
    rho=_box(arb(0),1/gap.lower().sqrt()); inv=(1/lam).upper(); phi=_box(-inv,inv)
    Ahat=gap*s*rho-mu*phi; R=_box(arb(1),arb.pi()/2); Rg=_box(-arb(1),-arb(1)/3)
    sq=_nonnegative_sqrt_hull(q)
    return "corner_hull",(
        -4*mu*R*lam*_pow(rho,3)*H/w,
        -2*Rg*lam2*H*H*Ahat*_pow(rho,5)/w2,
        -2*R*lam3*Ahat*_pow(rho,3)*(3*phi*H-gap*sq)/w,
    )


def run_threshold(threshold):
    sends,sqrt2=_partition(S_PANELS); tboxes=_split(T_LEFT,T_RIGHT,T_SPLITS); lboxes=_split(L_LEFT,L_RIGHT,L_SPLITS)
    records=[]
    for ti,(tl,tr) in enumerate(tboxes):
        t=_arb_interval(tl,tr)
        for li,(ll,lr) in enumerate(lboxes):
            lam=_arb_interval(ll,lr); total=arb(0); T=[arb(0),arb(0),arb(0)]; by=defaultdict(lambda:[arb(0),arb(0),arb(0)]); counts=defaultdict(int)
            for si,(sl,sr) in enumerate(zip(sends,sends[1:])):
                left=sqrt2 if sl==SQRT2 else _point(sl); right=sqrt2 if sr==SQRT2 else _point(sr); s=_box(left,right); width=right-left
                chart,terms=_corner_terms(s,t,lam) if (ti==T_SPLITS-1 and si==0) else _ordinary_terms(s,t,lam,SERIES_DEGREE,threshold)
                counts[chart]+=1
                for j,x in enumerate(terms):
                    c=x*width; T[j]+=c; by[chart][j]+=c; total+=c
            records.append({"ti":ti,"li":li,"t_box":[str(tl),str(tr)],"lambda_box":[str(ll),str(lr)],"total":total,"terms":T,"by":dict(by),"counts":dict(counts)})
    return records


def f(x): return f"mid={x.mid().str(14)} rad={x.rad().str(14)}"

def main():
    ctx.prec=BITS
    print("MONOTONE_TUBE U-THRESHOLD DIAGNOSTIC")
    print("fixed initial contract unchanged; diagnostic only")
    for th in THRESHOLDS:
        recs=run_threshold(th); first=recs[0]; widest=max(recs,key=lambda r:r["total"].rad()); max_t2=max(recs,key=lambda r:r["terms"][1].rad())
        print(f"\n=== u*={th} ===")
        print("FIRST",first["t_box"],first["lambda_box"],"counts",first["counts"])
        print(" total",f(first["total"]),"T2",f(first["terms"][1]))
        print("WIDEST",widest["t_box"],widest["lambda_box"],"counts",widest["counts"])
        print(" total",f(widest["total"]),"T2",f(widest["terms"][1]))
        print("MAX_T2",max_t2["t_box"],max_t2["lambda_box"],f(max_t2["terms"][1]))
        for chart in ("gamma_lower","u_upper","intersection","u_upper_cross_only","gamma_lower_cross_only","corner_hull"):
            if chart in widest["by"]:
                print(f" widest[{chart}] T2",f(widest["by"][chart][1]))

if __name__=="__main__": main()
