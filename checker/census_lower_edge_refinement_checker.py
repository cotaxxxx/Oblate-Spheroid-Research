#!/usr/bin/env python3
from fractions import Fraction
from math import isqrt
from flint import arb,ctx
from checker.census_lower_edge_checker import VerificationError,_point,_box,_density
L0=Fraction(5,8); L1=Fraction(33,50); LBOXES=256; T=Fraction(63,64)

def _split(a,b,n):
    w=(b-a)/n
    return [(a+i*w,a+(i+1)*w) for i in range(n)]

def verify(record):
    expected={"t":"63/64","lambda_domain":["5/8","33/50"],"lambda_boxes":256,"s_panels":1024,"series_degree":50,"bits":160,"u_star":"3/5","required_sign":"POS","sole_gate":"every lambda-box total.lower() > 0"}
    if record.get("schema")!="bg-oblate-spheroid.census-lower-edge-refinement.v1": raise VerificationError("schema mismatch")
    if record.get("contract")!=expected: raise VerificationError("contract mismatch")
    supplied=record.get("lambda_boxes",[])
    if len(supplied)!=256: raise VerificationError("lambda box count mismatch")
    ctx.prec=192
    n=1024; root=arb(2).sqrt(); rend=isqrt(2*n*n); vals=[Fraction(i,n) for i in range(rend+1)]+[None]
    t=_point(T); checked=[]
    for k,(ll,lr) in enumerate(_split(L0,L1,LBOXES)):
        lam=_box(_point(ll),_point(lr)); total=arb(0); counts={}
        for sl,sr in zip(vals,vals[1:]):
            left=_point(sl); right=root if sr is None else _point(sr)
            val,chart=_density(_box(left,right),t,lam)
            counts[chart]=counts.get(chart,0)+1
            total+=val*(right-left)
        rec=supplied[k]
        if rec.get("lambda_box")!=[str(ll),str(lr)]: raise VerificationError("lambda label mismatch")
        if rec.get("chart_counts")!=counts: raise VerificationError("chart inventory mismatch")
        if not total.lower()>0: raise VerificationError(f"GATING FAIL lambda={ll}:{lr} total={total}")
        checked.append((ll,lr,total))
    if not record.get("gating_pass"): raise VerificationError("producer did not pass")
    return checked
