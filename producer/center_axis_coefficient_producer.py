#!/usr/bin/env python3
"""PROTOTYPE / NOT_BINDING Arb producer for center-axis coefficient claims."""
from fractions import Fraction
from flint import arb, ctx
from producer.endpoint_interval_producer import _point,_box,_partition,SQRT2

PANELS=1024
BITS=160
LEFT_N=32
RIGHT_N=64
CENTER_N=16


def _hulls():
    R=_box(arb(1),arb(2))
    Rg=_box(-arb(1),-arb(1)/3)
    Rgg=_box(arb(0),arb(2))
    return R,Rg,Rgg


def _kernel(s,lam,derivative=False,endpoint=False):
    e=s*s; mu=1-e; gap=1+mu; l2=lam*lam
    q=1-mu*mu+l2*mu*mu
    w2=mu*mu+l2*(1-mu*mu); w=w2.sqrt()
    H=mu*gap*(1-l2)
    K=-3*mu*H-gap*q
    gamma=lam/(w*q.sqrt())
    gt=-lam*e*H/(w*q*q.sqrt())
    gtt=lam*l2*e*K/(w*q*q*q.sqrt())
    if endpoint:
        R,Rg,Rgg=_hulls()
    else:
        u=1-gamma*gamma
        R=gamma.acos()/u.sqrt()
        Rg=(gamma*R-1)/u
        Rgg=((R+gamma*Rg)*u+2*gamma*(gamma*R-1))/(u*u)
    G=s*(4*mu*R*gt-2*(Rg*gt*gt+R*gtt))
    if not derivative:
        return G
    ql=2*lam*mu*mu
    wl_over_w=lam*(1-mu*mu)/w2
    Hl=-2*lam*mu*gap
    Kl=-3*mu*Hl-gap*ql
    gl=gamma*(1/lam-wl_over_w-lam*mu*mu/q)
    P=lam/(w*q*q.sqrt())
    Pl=P*(1/lam-wl_over_w-3*lam*mu*mu/q)
    gtl=-e*(Pl*H+P*Hl)
    Q=lam*l2/(w*q*q*q.sqrt())
    Ql=Q*(3/lam-wl_over_w-5*lam*mu*mu/q)
    gttl=e*(Ql*K+Q*Kl)
    Rl=Rg*gl
    Rgl=Rgg*gl
    return s*(4*mu*(Rl*gt+R*gtl)-2*(Rgl*gt*gt+2*Rg*gt*gtl+Rl*gtt+R*gttl))


def integrate(ll,rr,derivative=False):
    endpoints,root=_partition(PANELS); lam=_box(_point(ll),_point(rr)); total=arb(0)
    last=len(endpoints)-2
    for k,(a,b) in enumerate(zip(endpoints,endpoints[1:])):
        aa=root if a==SQRT2 else _point(a); bb=root if b==SQRT2 else _point(b)
        s=_box(aa,bb)
        total += _kernel(s,lam,derivative,endpoint=(k==0 or k==last))*(bb-aa)
    return total


def split(a,b,n):
    d=(b-a)/n
    return [(a+i*d,a+(i+1)*d) for i in range(n)]


def run():
    ctx.prec=BITS
    claims=[]
    for label,a,b,n,deriv,sign in [
        ('LEFT_NEG',Fraction(1,4),Fraction(2,5),LEFT_N,False,'NEG'),
        ('CENTER_DERIV_POS',Fraction(2,5),Fraction(83,200),CENTER_N,True,'POS'),
        ('RIGHT_POS',Fraction(83,200),Fraction(1,1),RIGHT_N,False,'POS')]:
        worst=None; ok=True
        for ll,rr in split(a,b,n):
            x=integrate(ll,rr,deriv)
            good=x.upper()<0 if sign=='NEG' else x.lower()>0
            ok &= bool(good)
            margin=-x.upper() if sign=='NEG' else x.lower()
            if worst is None or margin<worst[0]: worst=(margin,ll,rr,x)
        claims.append((label,ok,worst))
    print('CENTER_AXIS_COEFFICIENT_PRODUCER — PROTOTYPE / NOT_BINDING')
    for label,ok,w in claims:
        print(label,'PASS' if ok else 'UNRESOLVED','weakest_box',w[1],w[2],'enclosure',w[3])
    print('REPORTED_NOT_GATING H(0.3)~-0.24350 H(0.4)~-0.019734 H(0.5)~0.236973')
    print('REPORTED_NOT_GATING Hlambda(0.4)~2.4675 Hlambda(0.5)~2.6172 lambda_c~0.4079588603')
    if not all(x[1] for x in claims): raise SystemExit('UNRESOLVED')

if __name__=='__main__': run()
