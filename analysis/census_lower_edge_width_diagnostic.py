#!/usr/bin/env python3
"""DIAGNOSTIC_ONLY width breakdown for corrected lower-edge first lambda box."""
from collections import defaultdict
from fractions import Fraction
from flint import arb,ctx
from producer.endpoint_interval_producer import SQRT2,_box,_partition,_point,_series
from producer.monotone_tube_interval_producer import _square,_pow,_unit_hull,_quantities

T=Fraction(63,64); LL=Fraction(5,8); LR=Fraction(32007,51200)
PANELS=1024; DEG=50; BITS=160; USTAR=Fraction(3,5)

def inter(x,y):
    lo=max(x.lower(),y.lower()); hi=min(x.upper(),y.upper())
    if hi<lo: raise ValueError('empty intersection')
    return _box(lo,hi)

def bounds(x):
    return {'mid':x.mid().str(30),'rad':x.rad().str(30),'lo':x.lower().str(30),'hi':x.upper().str(30)}

def density_terms(s,t,lam):
    e,gap,mu,d,lam2,A,q,w2,w,ht,H=_quantities(s,t,lam)
    A=inter(A,(1-t)+t*e)
    if not q.lower()>0: raise ValueError('q not positive')
    sq=q.sqrt(); gamma=_unit_hull(lam*A/(w*sq)); u0=_unit_hull(e*gap*_square(ht)/(w2*q))
    glo=max(arb(0),gamma.lower()); ghi=min(arb(1),gamma.upper())
    ulo=max(u0.lower(),arb(1)-ghi*ghi); uhi=min(u0.upper(),arb(1)-glo*glo)
    if uhi<ulo: raise ValueError('bad gamma/u')
    u=_box(ulo,uhi)
    gamma=inter(gamma,_box(max(arb(0),arb(1)-u.upper()).sqrt(),max(arb(0),arb(1)-u.lower()).sqrt()))
    rho=s/sq
    def upper():
        if not u.upper()<1: raise ValueError('upper invalid')
        Phi,_=_series(u,'Phi',DEG,clamped_nonnegative=True); R,_=_series(u,'Psi',DEG,clamped_nonnegative=True)
        return (-s*mu*Phi, 2*lam*A*R*_pow(rho,3)*H/w)
    def lower():
        if not u.lower()>0: raise ValueError('lower invalid')
        alpha=gamma.acos(); R=alpha/u.sqrt()
        return (-s*mu*alpha*alpha, 2*lam*A*R*_pow(rho,3)*H/w)
    th=_point(USTAR)
    if u.upper()<=th: return 'u_upper',upper()
    if u.lower()>=th: return 'gamma_lower',lower()
    uok=bool(u.upper()<1); gok=bool(u.lower()>0)
    if uok and gok:
        a,b=upper(),lower(); return 'intersection',(inter(a[0],b[0]),inter(a[1],b[1]))
    if uok: return 'u_upper_cross_only',upper()
    if gok: return 'gamma_lower_cross_only',lower()
    raise ValueError('no chart')

def main():
    ctx.prec=BITS; sends,sqrt2=_partition(PANELS); t=_point(T); lam=_box(_point(LL),_point(LR))
    totals=[arb(0),arb(0)]; by=defaultdict(lambda:[arb(0),arb(0)]); counts=defaultdict(int)
    maxcell=None
    for si,(sl,sr) in enumerate(zip(sends,sends[1:])):
        left=sqrt2 if sl==SQRT2 else _point(sl); right=sqrt2 if sr==SQRT2 else _point(sr); s=_box(left,right); width=right-left
        chart,terms=density_terms(s,t,lam); counts[chart]+=1
        contrib=[terms[0]*width,terms[1]*width]
        for j in range(2): totals[j]+=contrib[j]; by[chart][j]+=contrib[j]
        rad=(contrib[0]+contrib[1]).rad()
        if maxcell is None or rad>maxcell[0]: maxcell=(rad,si,str(sl),str(sr),chart,bounds(contrib[0]),bounds(contrib[1]),bounds(contrib[0]+contrib[1]))
    total=totals[0]+totals[1]
    print('CENSUS LOWER EDGE WIDTH DIAGNOSTIC — DIAGNOSTIC_ONLY / NOT_BINDING')
    print('lambda_box:',str(LL),str(LR),'chart_counts:',dict(counts))
    print('TOTAL:',bounds(total)); print('TERM1 -s*mu*angle^2:',bounds(totals[0])); print('TERM2 2*lambda*A*R*rho^3*H/w:',bounds(totals[1]))
    print('BY CHART:')
    for chart in sorted(by):
        print(' ',chart,'T1',bounds(by[chart][0]),'T2',bounds(by[chart][1]),'sum',bounds(by[chart][0]+by[chart][1]))
    print('MAX CELL:',maxcell)

if __name__=='__main__': main()
