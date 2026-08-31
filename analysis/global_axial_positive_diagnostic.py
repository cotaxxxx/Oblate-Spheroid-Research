#!/usr/bin/env python3
from fractions import Fraction
from collections import defaultdict
from flint import arb, ctx
from producer.endpoint_interval_producer import SQRT2, _box, _partition, _point
from producer.census_lower_edge_producer import _density

T0 = Fraction(1,32)
T1 = Fraction(31,32)
L0 = Fraction(5,8)
L1 = Fraction(33,50)
TB = 16
LB = 8
PANELS = 1024
BITS = 160

def split(a,b,n):
    w=(b-a)/n
    return [(a+i*w,a+(i+1)*w) for i in range(n)]

def iv(a,b):
    return _box(_point(a),_point(b))

def main():
    ctx.prec=BITS
    sends,sqrt2=_partition(PANELS)
    unresolved=[]
    weakest=None
    for tl,tr in split(T0,T1,TB):
        t=iv(tl,tr)
        for ll,lr in split(L0,L1,LB):
            lam=iv(ll,lr)
            total=arb(0); counts=defaultdict(int)
            for sl,sr in zip(sends,sends[1:]):
                left=sqrt2 if sl==SQRT2 else _point(sl)
                right=sqrt2 if sr==SQRT2 else _point(sr)
                val,chart=_density(_box(left,right),t,lam)
                counts[chart]+=1
                total += val*(right-left)
            rec=(total.lower(), tl,tr,ll,lr,total,dict(counts))
            if weakest is None or rec[0] < weakest[0]: weakest=rec
            if not total.lower()>0: unresolved.append(rec)
    print('GLOBAL_AXIAL_POSITIVE_DIAGNOSTIC — DIAGNOSTIC_ONLY / NOT_BINDING')
    print('domain t=[1/32,31/32], lambda=[5/8,33/50], boxes=16x8, s_panels=1024')
    lo,tl,tr,ll,lr,total,counts=weakest
    print('WEAKEST t_box:', tl,tr,'lambda_box:',ll,lr)
    print('WEAKEST total:', total)
    print('WEAKEST lower:', lo)
    print('WEAKEST chart_counts:', counts)
    print('UNRESOLVED_COUNT:', len(unresolved))
    for rec in unresolved[:20]:
        lo,tl,tr,ll,lr,total,counts=rec
        print('UNRESOLVED',tl,tr,ll,lr,total,counts)

if __name__=='__main__': main()
