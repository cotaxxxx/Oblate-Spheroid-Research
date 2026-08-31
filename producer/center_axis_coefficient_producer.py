#!/usr/bin/env python3
"""PROTOTYPE / NOT_BINDING Arb producer for center-axis coefficient claims."""
from fractions import Fraction
from flint import arb, ctx
from producer.endpoint_interval_producer import _point,_box,_partition,SQRT2
PANELS=1024; BITS=160; LEFT_N=32; RIGHT_N=64; CENTER_N=16; DEG=50; USTAR=arb(3)/5

def _coeffs():
    out=[Fraction(1)]; c=Fraction(1)
    for k in range(DEG+2):
        c*=Fraction((2*k+1)**2,2*(k+1)*(2*k+3)); out.append(c)
    return out
COEFFS=_coeffs()

def _psi_bundle(u,gamma):
    R=arb(0); Rp=arb(0); Rpp=arb(0)
    for n,c in enumerate(COEFFS[:DEG+1]):
        a=arb(c.numerator)/c.denominator; R+=a*(u**n)
        if n: Rp+=n*a*(u**(n-1))
        if n>1: Rpp+=n*(n-1)*a*(u**(n-2))
    U=u.upper(); c=COEFFS[DEG+1]; cn=arb(c.numerator)/c.denominator
    R+=_box(arb(0),cn*(u**(DEG+1)).upper()/(1-U))
    Rp+=_box(arb(0),(DEG+1)*cn*(u**DEG).upper()/(1-U*arb(DEG+2)/(DEG+1)))
    Rpp+=_box(arb(0),(DEG+1)*DEG*cn*(u**(DEG-1)).upper()/(1-U*arb(DEG+2)/DEG))
    return R,-2*gamma*Rp,4*gamma*gamma*Rpp-2*Rp

def _kernel(s,lam,derivative=False):
    e=s*s; mu=1-e; gap=1+mu; l2=lam*lam; q=1-mu*mu+l2*mu*mu; w2=mu*mu+l2*(1-mu*mu); w=w2.sqrt()
    H=mu*gap*(1-l2); K=-3*mu*H-gap*q; gamma=lam/(w*q.sqrt()); u=e*gap*mu*mu*(1-l2)*(1-l2)/(w2*q)
    gt=-lam*e*H/(w*q*q.sqrt()); gtt=lam*l2*e*K/(w*q*q*q.sqrt())
    if u.upper()<=USTAR: R,Rg,Rgg=_psi_bundle(u,gamma)
    else:
        R=u.sqrt().asin()/u.sqrt(); Rg=(gamma*R-1)/u; Rgg=((R+gamma*Rg)*u+2*gamma*(gamma*R-1))/(u*u)
    if not derivative: return s*(4*mu*R*gt-2*(Rg*gt*gt+R*gtt))
    ql=2*lam*mu*mu; wl=lam*(1-mu*mu)/w2; Hl=-2*lam*mu*gap; Kl=-3*mu*Hl-gap*ql
    gl=gamma*(1/lam-wl-lam*mu*mu/q); P=lam/(w*q*q.sqrt()); Pl=P*(1/lam-wl-3*lam*mu*mu/q); gtl=-e*(Pl*H+P*Hl)
    Q=lam*l2/(w*q*q*q.sqrt()); Ql=Q*(3/lam-wl-5*lam*mu*mu/q); gttl=e*(Ql*K+Q*Kl); Rl=Rg*gl; Rgl=Rgg*gl
    return s*(4*mu*(Rl*gt+R*gtl)-2*(Rgl*gt*gt+2*Rg*gt*gtl+Rl*gtt+R*gttl))
def integrate(ll,rr,derivative=False):
    grid,root=_partition(PANELS); lam=_box(_point(ll),_point(rr)); total=arb(0)
    for a,b in zip(grid,grid[1:]):
        aa=root if a==SQRT2 else _point(a); bb=root if b==SQRT2 else _point(b); total+=_kernel(_box(aa,bb),lam,derivative)*(bb-aa)
    return total
def split(a,b,n):
    d=(b-a)/n; return [(a+i*d,a+(i+1)*d) for i in range(n)]
def run():
    ctx.prec=BITS; claims=[]
    for label,a,b,n,deriv,sign in [('LEFT_NEG',Fraction(1,4),Fraction(2,5),LEFT_N,False,'NEG'),('CENTER_DERIV_POS',Fraction(2,5),Fraction(83,200),CENTER_N,True,'POS'),('RIGHT_POS',Fraction(83,200),Fraction(1),RIGHT_N,False,'POS')]:
        worst=None; ok=True
        for ll,rr in split(a,b,n):
            x=integrate(ll,rr,deriv); good=x.upper()<0 if sign=='NEG' else x.lower()>0; ok&=bool(good); m=-x.upper() if sign=='NEG' else x.lower()
            if worst is None or m<worst[0]: worst=(m,ll,rr,x)
        claims.append((label,ok,worst))
    print('CENTER_AXIS_COEFFICIENT_PRODUCER — PROTOTYPE / NOT_BINDING')
    for label,ok,w in claims: print(label,'PASS' if ok else 'UNRESOLVED','weakest_box',w[1],w[2],'enclosure',w[3])
    if not all(x[1] for x in claims): raise SystemExit('UNRESOLVED')
if __name__=='__main__': run()
