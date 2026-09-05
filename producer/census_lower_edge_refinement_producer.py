#!/usr/bin/env python3
from fractions import Fraction
from flint import arb,ctx
from producer.endpoint_interval_producer import SQRT2,_box,_partition,_point
from producer.census_lower_edge_producer import _density,T,PANELS,DEG,BITS,USTAR
L0=Fraction(5,8); L1=Fraction(33,50); LBOXES=256

def _split(a,b,n):
    w=(b-a)/n
    return [(a+i*w,a+(i+1)*w) for i in range(n)]

def produce_record():
    ctx.prec=BITS
    sends,sqrt2=_partition(PANELS)
    t=_point(T)
    out=[]; ok=True
    for ll,lr in _split(L0,L1,LBOXES):
        lam=_box(_point(ll),_point(lr)); total=arb(0); counts={}
        for sl,sr in zip(sends,sends[1:]):
            left=sqrt2 if sl==SQRT2 else _point(sl); right=sqrt2 if sr==SQRT2 else _point(sr)
            val,chart=_density(_box(left,right),t,lam)
            counts[chart]=counts.get(chart,0)+1
            total+=val*(right-left)
        passed=bool(total.lower()>0); ok=ok and passed
        out.append({"lambda_box":[str(ll),str(lr)],"chart_counts":counts,"total_mid":total.mid().str(60),"total_rad":total.rad().str(60),"lower_positive":passed})
    return {"schema":"bg-oblate-spheroid.census-lower-edge-refinement.v1","status":"PROTOTYPE_NOT_AUDITED_NOT_BINDING","contract":{"t":"63/64","lambda_domain":["5/8","33/50"],"lambda_boxes":256,"s_panels":1024,"series_degree":50,"bits":160,"u_star":"3/5","required_sign":"POS","sole_gate":"every lambda-box total.lower() > 0"},"lambda_boxes":out,"gating_pass":ok}
