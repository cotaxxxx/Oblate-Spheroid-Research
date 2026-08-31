#!/usr/bin/env python3
from fractions import Fraction
from flint import arb,ctx
from checker.census_lower_edge_checker import VerificationError,_point,_box,_density
from checker.monotone_tube_interval_checker import _s_partition

def split(a,b,n):
    w=(b-a)/n; return [(a+i*w,a+(i+1)*w) for i in range(n)]

def verify(record):
    exp={'t':'31/32','lambda_domain':['5/8','33/50'],'lambda_boxes':8,'s_panels':1024,'series_degree':50,'bits':160,'u_star':'3/5','required_sign':'POS','sole_gate':'every lambda-box total.lower() > 0'}
    if record.get('contract')!=exp or record.get('schema')!='bg-oblate-spheroid.census-lower-edge-31-32.v1': raise VerificationError('contract/schema mismatch')
    supplied=record.get('lambda_boxes',[])
    if len(supplied)!=8: raise VerificationError('box count mismatch')
    ctx.prec=192; svals,root=_s_partition(1024); t=_point(Fraction(31,32)); out=[]
    for rec,(ll,lr) in zip(supplied,split(Fraction(5,8),Fraction(33,50),8)):
        lam=_box(_point(ll),_point(lr)); total=arb(0); counts={}
        for sl,sr in zip(svals,svals[1:]):
            left=_point(sl); right=root if sr is None else _point(sr); val,chart=_density(_box(left,right),t,lam); counts[chart]=counts.get(chart,0)+1; total+=val*(right-left)
        if rec.get('lambda_box')!=[str(ll),str(lr)] or rec.get('chart_counts')!=counts: raise VerificationError('record mismatch')
        if not total.lower()>0: raise VerificationError(f'GATING FAIL lambda={ll}:{lr} total={total}')
        out.append((ll,lr,total))
    if not record.get('gating_pass'): raise VerificationError('producer fail')
    return out
