#!/usr/bin/env python3
"""Arb producer for the separately declared oblate monotone-tube refinement."""
from __future__ import annotations
from collections import defaultdict
from fractions import Fraction
from flint import arb,ctx
from producer.endpoint_interval_producer import SQRT2,_box,_partition,_point,_series
from producer.monotone_tube_interval_producer import (
    BITS,L_LEFT,L_RIGHT,L_SPLITS,SERIES_DEGREE,S_PANELS,T_LEFT,T_RIGHT,T_SPLITS,
    _arb_interval,_nonnegative_sqrt_hull,_pow,_quantities,_split,_square,_unit_hull,
)
U_STAR=Fraction(3,5)

def _inter(x,y):
    lo=max(x.lower(),y.lower()); hi=min(x.upper(),y.upper())
    if hi<lo: raise ValueError("empty interval intersection")
    return _box(lo,hi)

def _ordinary(s,t,lam):
    e,gap,mu,d,lam2,A,q,w2,w,ht,H=_quantities(s,t,lam)
    if not q.lower()>0: raise ValueError("ordinary q not positive")
    A=_inter(A,(1-t)+t*e); sq=q.sqrt(); gamma=_unit_hull(lam*A/(w*sq)); u0=_unit_hull(e*gap*_square(ht)/(w2*q))
    glo=max(arb(0),gamma.lower()); ghi=min(arb(1),gamma.upper()); ulo=max(u0.lower(),arb(1)-ghi*ghi); uhi=min(u0.upper(),arb(1)-glo*glo)
    if uhi<ulo: raise ValueError("inconsistent gamma/u")
    u=_box(ulo,uhi); gc_lo=max(arb(0),arb(1)-u.upper()).sqrt(); gc_hi=max(arb(0),arb(1)-u.lower()).sqrt(); gamma=_inter(gamma,_box(gc_lo,gc_hi))
    lam3=lam2*lam; rho=s/sq; phi=d/sq; Ahat=A/sq
    def terms(R,Rg):
        return (-4*mu*R*lam*_pow(rho,3)*H/w,-2*Rg*lam2*H*H*Ahat*_pow(rho,5)/w2,-2*R*lam3*Ahat*_pow(rho,3)*(3*phi*H-gap*sq)/w)
    def ut():
        if not u.upper()<1: raise ValueError("u chart invalid")
        R,_=_series(u,"Psi",SERIES_DEGREE,clamped_nonnegative=True); P,_=_series(u,"Psi_prime",SERIES_DEGREE,clamped_nonnegative=True)
        return terms(R,-2*gamma*P)
    def gt():
        if not u.lower()>0: raise ValueError("gamma chart invalid")
        R=gamma.acos()/u.sqrt(); return terms(R,(gamma*R-1)/u)
    th=_point(U_STAR)
    if u.upper()<=th: return "u_upper",ut()
    if u.lower()>=th: return "gamma_lower",gt()
    uok=bool(u.upper()<1); gok=bool(u.lower()>0)
    if uok and gok:
        a,b=ut(),gt(); return "intersection",tuple(_inter(x,y) for x,y in zip(a,b))
    if uok: return "u_upper_cross_only",ut()
    if gok: return "gamma_lower_cross_only",gt()
    raise ValueError("crossing cell has no valid chart")

def _corner(s,t,lam):
    e,gap,mu,d,lam2,A,q,w2,w,ht,H=_quantities(s,t,lam); lam3=lam2*lam
    rho=_box(arb(0),1/gap.lower().sqrt()); inv=(1/lam).upper(); phi=_box(-inv,inv); Ahat=gap*s*rho-mu*phi
    R=_box(arb(1),arb.pi()/2); Rg=_box(-arb(1),-arb(1)/3); sq=_nonnegative_sqrt_hull(q)
    return "corner_hull",(-4*mu*R*lam*_pow(rho,3)*H/w,-2*Rg*lam2*H*H*Ahat*_pow(rho,5)/w2,-2*R*lam3*Ahat*_pow(rho,3)*(3*phi*H-gap*sq)/w)

def produce_record():
    ctx.prec=BITS; sends,sqrt2=_partition(S_PANELS); tboxes=_split(T_LEFT,T_RIGHT,T_SPLITS); lboxes=_split(L_LEFT,L_RIGHT,L_SPLITS); out=[]; ok=True
    for ti,(tl,tr) in enumerate(tboxes):
        t=_arb_interval(tl,tr)
        for li,(ll,lr) in enumerate(lboxes):
            lam=_arb_interval(ll,lr); total=arb(0); counts=defaultdict(int)
            for si,(sl,sr) in enumerate(zip(sends,sends[1:])):
                left=sqrt2 if sl==SQRT2 else _point(sl); right=sqrt2 if sr==SQRT2 else _point(sr); s=_box(left,right)
                chart,terms=_corner(s,t,lam) if (ti==7 and si==0) else _ordinary(s,t,lam); counts[chart]+=1
                total+=(terms[0]+terms[1]+terms[2])*(right-left)
            passed=bool(total.upper()<0); ok=ok and passed
            out.append({"t_box":[str(tl),str(tr)],"lambda_box":[str(ll),str(lr)],"chart_counts":dict(counts),"total_mid":total.mid().str(50),"total_rad":total.rad().str(50),"upper_negative":passed})
    return {"schema":"bg-oblate-spheroid.monotone-tube-refinement.v1","status":"PROTOTYPE_NOT_AUDITED_NOT_BINDING","contract":{"t_domain":["63/64","1"],"lambda_domain":["5/8","33/50"],"t_boxes":8,"lambda_boxes":8,"s_panels":1024,"series_degree":50,"bits":160,"u_star":"3/5","required_sign":"NEG","sole_gate":"every parameter-box total.upper() < 0"},"parameter_boxes":out,"gating_pass":ok}
