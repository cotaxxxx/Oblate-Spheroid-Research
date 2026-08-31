#!/usr/bin/env python3
from fractions import Fraction
from flint import arb,ctx
from checker.monotone_tube_interval_checker import VerificationError,_point,_box,_split,_s_partition
from checker.monotone_tube_refinement_checker import _ordinary_refinement

def verify(record):
    exp={'t_domain':['31/32','63/64'],'lambda_domain':['5/8','33/50'],'t_boxes':8,'lambda_boxes':8,'s_panels':1024,'series_degree':50,'bits':160,'u_star':'3/5','required_sign':'NEG','sole_gate':'every parameter-box total.upper() < 0'}
    if record.get('contract')!=exp or record.get('schema')!='bg-oblate-spheroid.monotone-tube-lower-slab.v1': raise VerificationError('contract/schema mismatch')
    supplied=record.get('parameter_boxes',[])
    if len(supplied)!=64: raise VerificationError('box count mismatch')
    ctx.prec=192; svals,root=_s_partition(1024); tboxes=_split(Fraction(31,32),Fraction(63,64),8); lboxes=_split(Fraction(5,8),Fraction(33,50),8)
    k=0; out=[]
    for tl,tr in tboxes:
        t=_box(_point(tl),_point(tr))
        for ll,lr in lboxes:
            lam=_box(_point(ll),_point(lr)); total=arb(0); counts={}
            for sl,sr in zip(svals,svals[1:]):
                left=_point(sl); right=root if sr is None else _point(sr); s=_box(left,right); chart,terms=_ordinary_refinement(s,t,lam)
                counts[chart]=counts.get(chart,0)+1; total+=sum(terms,arb(0))*(right-left)
            rec=supplied[k]; k+=1
            if rec.get('t_box')!=[str(tl),str(tr)] or rec.get('lambda_box')!=[str(ll),str(lr)] or rec.get('chart_counts')!=counts: raise VerificationError('record mismatch')
            if not total.upper()<0: raise VerificationError(f'GATING FAIL t={tl}:{tr} lambda={ll}:{lr} total={total}')
            out.append(total)
    if not record.get('gating_pass'): raise VerificationError('producer fail')
    return out
