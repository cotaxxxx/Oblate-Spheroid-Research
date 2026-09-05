#!/usr/bin/env python3
from fractions import Fraction
from collections import defaultdict
from flint import arb, ctx
from producer.endpoint_interval_producer import SQRT2, _box, _partition, _point
from producer.monotone_tube_refinement_producer import _ordinary

T0=Fraction(0,1); T1=Fraction(1,32)
L0=Fraction(5,8); L1=Fraction(33,50)
TB=8; LB=8; PANELS=1024; BITS=160

def split(a,b,n):
    w=(b-a)/n
    return [(a+i*w,a+(i+1)*w) for i in range(n)]

def iv(a,b): return _box(_point(a),_point(b))

def main():
    ctx.prec=BITS
    sends,sqrt2=_partition(PANELS)
    unresolved=[]; weakest=None
    for tl,tr in split(T0,T1,TB):
        t=iv(tl,tr)
        for ll,lr in split(L0,L1,LB):
            lam=iv(ll,lr); total=arb(0); counts=defaultdict(int)
            for sl,sr in zip(sends,sends[1:]):
                left=sqrt2 if sl==SQRT2 else _point(sl)
                right=sqrt2 if sr==SQRT2 else _point(sr)
                chart,terms=_ordinary(_box(left,right),t,lam)
                counts[chart]+=1
                total += sum(terms,arb(0))*(right-left)
            rec=(total.lower(),tl,tr,ll,lr,total,dict(counts))
            if weakest is None or rec[0] < weakest[0]: weakest=rec
            if not total.lower()>0: unresolved.append(rec)
    print('GLOBAL_AXIAL_CENTER_DERIVATIVE_DIAGNOSTIC — DIAGNOSTIC_ONLY / NOT_BINDING')
    print('quantity=partial_t g_axis_ob; target POS; domain t=[0,1/32], lambda=[5/8,33/50]')
    lo,tl,tr,ll,lr,total,counts=weakest
    print('WEAKEST t_box:',tl,tr,'lambda_box:',ll,lr)
    print('WEAKEST total:',total)
    print('WEAKEST lower:',lo)
    print('WEAKEST chart_counts:',counts)
    print('UNRESOLVED_COUNT:',len(unresolved))
    for rec in unresolved[:20]:
        lo,tl,tr,ll,lr,total,counts=rec
        print('UNRESOLVED',tl,tr,ll,lr,total,counts)

if __name__=='__main__': main()
