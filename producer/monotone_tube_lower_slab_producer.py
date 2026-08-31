#!/usr/bin/env python3
from fractions import Fraction
from collections import defaultdict
from flint import arb,ctx
from producer.endpoint_interval_producer import SQRT2,_box,_partition,_point
from producer.monotone_tube_interval_producer import _arb_interval,_split
from producer.monotone_tube_refinement_producer import _ordinary
T0=Fraction(31,32); T1=Fraction(63,64); L0=Fraction(5,8); L1=Fraction(33,50)
TB=8; LB=8; PANELS=1024; BITS=160

def produce_record():
    ctx.prec=BITS; sends,sqrt2=_partition(PANELS); out=[]; ok=True
    for tl,tr in _split(T0,T1,TB):
        t=_arb_interval(tl,tr)
        for ll,lr in _split(L0,L1,LB):
            lam=_arb_interval(ll,lr); total=arb(0); counts=defaultdict(int)
            for sl,sr in zip(sends,sends[1:]):
                left=sqrt2 if sl==SQRT2 else _point(sl); right=sqrt2 if sr==SQRT2 else _point(sr); s=_box(left,right)
                chart,terms=_ordinary(s,t,lam); counts[chart]+=1; total+=sum(terms,arb(0))*(right-left)
            passed=bool(total.upper()<0); ok=ok and passed
            out.append({'t_box':[str(tl),str(tr)],'lambda_box':[str(ll),str(lr)],'chart_counts':dict(counts),'total_mid':total.mid().str(60),'total_rad':total.rad().str(60),'upper_negative':passed})
    return {'schema':'bg-oblate-spheroid.monotone-tube-lower-slab.v1','status':'PROTOTYPE_NOT_AUDITED_NOT_BINDING','contract':{'t_domain':['31/32','63/64'],'lambda_domain':['5/8','33/50'],'t_boxes':8,'lambda_boxes':8,'s_panels':1024,'series_degree':50,'bits':160,'u_star':'3/5','required_sign':'NEG','sole_gate':'every parameter-box total.upper() < 0'},'parameter_boxes':out,'gating_pass':ok}
