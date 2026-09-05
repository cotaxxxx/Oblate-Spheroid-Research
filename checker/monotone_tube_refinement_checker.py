#!/usr/bin/env python3
"""Independent checker for the separately declared monotone-tube refinement."""
from __future__ import annotations
from fractions import Fraction
from flint import arb,ctx
from checker.monotone_tube_interval_checker import (
    VerificationError,_point,_box,_square,_pow,_series,_quantities,_corner,_split,_s_partition
)
U_STAR=Fraction(3,5)

def _inter(x,y):
    lo=max(x.lower(),y.lower()); hi=min(x.upper(),y.upper())
    if hi<lo: raise VerificationError("empty interval intersection")
    return _box(lo,hi)

def _unit(x):
    lo=max(arb(0),x.lower()); hi=min(arb(1),x.upper())
    if hi<lo: raise VerificationError("empty unit intersection")
    return _box(lo,hi)

def _ordinary_refinement(s,t,lam):
    e,gap,mu,d,lam2,A,q,w2,w,ht,H=_quantities(s,t,lam)
    if not q.lower()>0: raise VerificationError("ordinary q not positive")
    A=_inter(A,(1-t)+t*e); sq=q.sqrt(); gamma=_unit(lam*A/(w*sq)); u0=_unit(e*gap*_square(ht)/(w2*q))
    glo=max(arb(0),gamma.lower()); ghi=min(arb(1),gamma.upper()); ulo=max(u0.lower(),arb(1)-ghi*ghi); uhi=min(u0.upper(),arb(1)-glo*glo)
    if uhi<ulo: raise VerificationError("inconsistent gamma/u")
    u=_box(ulo,uhi); gc_lo=max(arb(0),arb(1)-u.upper()).sqrt(); gc_hi=max(arb(0),arb(1)-u.lower()).sqrt(); gamma=_inter(gamma,_box(gc_lo,gc_hi))
    lam3=lam2*lam; rho=s/sq; phi=d/sq; Ahat=A/sq
    def terms(R,Rg):
        return (-4*mu*R*lam*_pow(rho,3)*H/w,-2*Rg*lam2*H*H*Ahat*_pow(rho,5)/w2,-2*R*lam3*Ahat*_pow(rho,3)*(3*phi*H-gap*sq)/w)
    def upper_terms():
        if not u.upper()<1: raise VerificationError("u chart invalid")
        R=_series(u,"Psi",50); P=_series(u,"Psi_prime",50); return terms(R,-2*gamma*P)
    def lower_terms():
        if not u.lower()>0: raise VerificationError("gamma chart invalid")
        R=gamma.acos()/u.sqrt(); return terms(R,(gamma*R-1)/u)
    th=_point(U_STAR)
    if u.upper()<=th: return "u_upper",upper_terms()
    if u.lower()>=th: return "gamma_lower",lower_terms()
    uok=bool(u.upper()<1); gok=bool(u.lower()>0)
    if uok and gok:
        a,b=upper_terms(),lower_terms(); return "intersection",tuple(_inter(x,y) for x,y in zip(a,b))
    if uok: return "u_upper_cross_only",upper_terms()
    if gok: return "gamma_lower_cross_only",lower_terms()
    raise VerificationError("crossing cell has no valid chart")

def verify(record):
    expected={"t_domain":["63/64","1"],"lambda_domain":["5/8","33/50"],"t_boxes":8,"lambda_boxes":8,"s_panels":1024,"series_degree":50,"bits":160,"u_star":"3/5","required_sign":"NEG","sole_gate":"every parameter-box total.upper() < 0"}
    if record.get("contract")!=expected: raise VerificationError("contract mismatch")
    if record.get("schema")!="bg-oblate-spheroid.monotone-tube-refinement.v1": raise VerificationError("schema mismatch")
    supplied=record.get("parameter_boxes",[])
    if len(supplied)!=64: raise VerificationError("parameter box count mismatch")
    ctx.prec=192; svals,root=_s_partition(1024); tboxes=_split(Fraction(63,64),Fraction(1),8); lboxes=_split(Fraction(5,8),Fraction(33,50),8)
    out=[]; k=0
    for ti,(tl,tr) in enumerate(tboxes):
        t=_box(_point(tl),_point(tr))
        for li,(ll,lr) in enumerate(lboxes):
            lam=_box(_point(ll),_point(lr)); total=arb(0); counts={}
            for si,(sl,sr) in enumerate(zip(svals,svals[1:])):
                left=_point(sl); right=root if sr is None else _point(sr); s=_box(left,right)
                if ti==7 and si==0:
                    val,chart=_corner(s,t,lam); terms=(val,)
                else:
                    chart,three=_ordinary_refinement(s,t,lam); terms=three
                counts[chart]=counts.get(chart,0)+1; total+=sum(terms,arb(0))*(right-left)
            rec=supplied[k]; k+=1
            if rec.get("t_box")!=[str(tl),str(tr)] or rec.get("lambda_box")!=[str(ll),str(lr)]: raise VerificationError("box label mismatch")
            if rec.get("chart_counts")!=counts: raise VerificationError("chart inventory mismatch")
            if not total.upper()<0: raise VerificationError(f"GATING FAIL t={tl}:{tr} lambda={ll}:{lr} total={total}")
            out.append(total)
    if not record.get("gating_pass"): raise VerificationError("producer did not report pass")
    return out
