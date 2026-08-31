#!/usr/bin/env python3
from fractions import Fraction
from flint import arb,ctx
from producer.endpoint_interval_producer import SQRT2,_box,_partition,_point,_series
from producer.monotone_tube_interval_producer import _square,_pow,_unit_hull,_quantities
T=Fraction(63,64); L0=Fraction(5,8); L1=Fraction(33,50); PANELS=1024; DEG=50; BITS=160; USTAR=Fraction(3,5)

def _inter(x,y):
    lo=max(x.lower(),y.lower()); hi=min(x.upper(),y.upper())
    if hi<lo: raise ValueError("empty intersection")
    return _box(lo,hi)

def _density(s,t,lam):
    e,gap,mu,d,lam2,A,q,w2,w,ht,H=_quantities(s,t,lam)
    A=_inter(A,(1-t)+t*e)
    if not q.lower()>0: raise ValueError("q not positive")
    sq=q.sqrt(); gamma=_unit_hull(lam*A/(w*sq)); u0=_unit_hull(e*gap*_square(ht)/(w2*q))
    glo=max(arb(0),gamma.lower()); ghi=min(arb(1),gamma.upper()); ulo=max(u0.lower(),arb(1)-ghi*ghi); uhi=min(u0.upper(),arb(1)-glo*glo)
    if uhi<ulo: raise ValueError("bad gamma/u")
    u=_box(ulo,uhi); gamma=_inter(gamma,_box(max(arb(0),arb(1)-u.upper()).sqrt(),max(arb(0),arb(1)-u.lower()).sqrt()))
    rho=s/sq
    def upper():
        if not u.upper()<1: raise ValueError("upper invalid")
        Phi,_=_series(u,"Phi",DEG,clamped_nonnegative=True); R,_=_series(u,"Psi",DEG,clamped_nonnegative=True)
        return -s*mu*Phi + 2*lam*R*A*_pow(rho,3)*H/w
    def lower():
        if not u.lower()>0: raise ValueError("lower invalid")
        alpha=gamma.acos(); R=alpha/u.sqrt()
        return -s*mu*alpha*alpha + 2*lam*R*A*_pow(rho,3)*H/w
    th=_point(USTAR)
    if u.upper()<=th: return upper(),"u_upper"
    if u.lower()>=th: return lower(),"gamma_lower"
    uok=bool(u.upper()<1); gok=bool(u.lower()>0)
    if uok and gok: return _inter(upper(),lower()),"intersection"
    if uok: return upper(),"u_upper_cross_only"
    if gok: return lower(),"gamma_lower_cross_only"
    raise ValueError("no chart")

def produce_record():
    ctx.prec=BITS; sends,sqrt2=_partition(PANELS); t=_point(T); lam=_box(_point(L0),_point(L1)); total=arb(0); counts={}
    for sl,sr in zip(sends,sends[1:]):
        left=sqrt2 if sl==SQRT2 else _point(sl); right=sqrt2 if sr==SQRT2 else _point(sr); s=_box(left,right)
        val,chart=_density(s,t,lam); counts[chart]=counts.get(chart,0)+1; total+=val*(right-left)
    return {"schema":"bg-oblate-spheroid.census-lower-edge.v2","status":"PROTOTYPE_NOT_AUDITED_NOT_BINDING","contract":{"t":"63/64","lambda_domain":["5/8","33/50"],"lambda_boxes":1,"s_panels":1024,"series_degree":50,"bits":160,"u_star":"3/5","required_sign":"POS","sole_gate":"full-domain lower endpoint > 0"},"chart_counts":counts,"total_mid":total.mid().str(50),"total_rad":total.rad().str(50),"gating_pass":bool(total.lower()>0)}
