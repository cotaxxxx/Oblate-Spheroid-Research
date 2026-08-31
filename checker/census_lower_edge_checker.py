#!/usr/bin/env python3
from fractions import Fraction
from math import comb,isqrt
from flint import arb,ctx
class VerificationError(RuntimeError): pass

def _point(x): return arb(x.numerator)/x.denominator if isinstance(x,Fraction) else arb(x)
def _box(lo,hi): return arb((lo+hi)/2,(hi-lo)/2)
def _square(x):
    lo,hi=x.lower(),x.upper()
    if lo<=0<=hi: return _box(arb(0),max((-lo)*(-lo),hi*hi))
    a,b=lo*lo,hi*hi; return _box(min(a,b),max(a,b))
def _pow(x,n):
    y=arb(1)
    for _ in range(n): y*=x
    return y
def _unit(x):
    lo=max(arb(0),x.lower()); hi=min(arb(1),x.upper())
    if hi<lo: raise VerificationError("empty unit")
    return _box(lo,hi)
def _inter(x,y):
    lo=max(x.lower(),y.lower()); hi=min(x.upper(),y.upper())
    if hi<lo: raise VerificationError("empty intersection")
    return _box(lo,hi)
def _zero_to_upper(x):
    hi=max(arb(0),x.upper()); return arb(hi/2,hi/2)
def _series(u,name,degree):
    if not u.upper()<1: raise VerificationError("series requires u<1")
    p=arb(0)
    if name=="Phi":
        for n in range(1,degree+1): p+=_point(Fraction(4**n,2*n*n*comb(2*n,n)))*_pow(u,n)
        n=degree+1; nxt=_point(Fraction(4**n,2*n*n*comb(2*n,n)))*_pow(u,n)
    elif name=="Psi":
        for n in range(degree+1): p+=_point(Fraction(comb(2*n,n),4**n*(2*n+1)))*_pow(u,n)
        n=degree+1; nxt=_point(Fraction(comb(2*n,n),4**n*(2*n+1)))*_pow(u,n)
    else: raise VerificationError("unknown series")
    return p+_zero_to_upper(nxt/(1-u))
def _quantities(s,t,lam):
    e=_square(s); gap=2-e; mu=1-e; delta=1-t; d=e-delta; l2=_square(lam); A=1-t*mu
    q=e*gap+l2*_square(d); q=_box(max(arb(0),q.lower()),max(arb(0),q.upper()))
    w2=l2*e*gap+_square(mu); w=w2.sqrt(); ht=mu+l2*d; H=(1-e)*gap+l2*(2*e-2*delta-e*e+delta*e)
    return e,gap,mu,d,l2,A,q,w2,w,ht,H
def _density(s,t,lam):
    e,gap,mu,d,l2,A,q,w2,w,ht,H=_quantities(s,t,lam); A=_inter(A,(1-t)+t*e)
    if not q.lower()>0: raise VerificationError("q not positive")
    sq=q.sqrt(); gamma=_unit(lam*A/(w*sq)); u0=_unit(e*gap*_square(ht)/(w2*q)); glo=max(arb(0),gamma.lower()); ghi=min(arb(1),gamma.upper())
    u=_box(max(u0.lower(),arb(1)-ghi*ghi),min(u0.upper(),arb(1)-glo*glo)); gamma=_inter(gamma,_box(max(arb(0),arb(1)-u.upper()).sqrt(),max(arb(0),arb(1)-u.lower()).sqrt()))
    rho=s/sq
    def upper(): return -s*mu*_series(u,"Phi",50)+2*lam*_series(u,"Psi",50)*A*_pow(rho,3)*H/w
    def lower():
        a=gamma.acos(); return -s*mu*a*a+2*lam*(a/u.sqrt())*A*_pow(rho,3)*H/w
    th=_point(Fraction(3,5))
    if u.upper()<=th: return upper(),"u_upper"
    if u.lower()>=th: return lower(),"gamma_lower"
    uok=bool(u.upper()<1); gok=bool(u.lower()>0)
    if uok and gok: return _inter(upper(),lower()),"intersection"
    if uok: return upper(),"u_upper_cross_only"
    if gok: return lower(),"gamma_lower_cross_only"
    raise VerificationError("no chart")
def verify(record):
    exp={"t":"63/64","lambda_domain":["5/8","33/50"],"lambda_boxes":1,"s_panels":1024,"series_degree":50,"bits":160,"u_star":"3/5","required_sign":"POS","sole_gate":"full-domain lower endpoint > 0"}
    if record.get("contract")!=exp: raise VerificationError("contract mismatch")
    if record.get("schema")!="bg-oblate-spheroid.census-lower-edge.v2": raise VerificationError("schema mismatch")
    ctx.prec=192; n=1024; root=arb(2).sqrt(); rend=isqrt(2*n*n); vals=[Fraction(i,n) for i in range(rend+1)]+[None]
    t=_point(Fraction(63,64)); lam=_box(_point(Fraction(5,8)),_point(Fraction(33,50))); total=arb(0); counts={}
    for sl,sr in zip(vals,vals[1:]):
        left=_point(sl); right=root if sr is None else _point(sr); val,chart=_density(_box(left,right),t,lam); counts[chart]=counts.get(chart,0)+1; total+=val*(right-left)
    if counts!=record.get("chart_counts"): raise VerificationError("chart inventory mismatch")
    if not total.lower()>0: raise VerificationError(f"GATING FAIL {total}")
    if not record.get("gating_pass"): raise VerificationError("producer did not pass")
    return total
