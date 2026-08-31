#!/usr/bin/env python3
"""Independent checker for center-axis coefficient signs. PROTOTYPE / NOT_BINDING."""
from fractions import Fraction
from flint import arb,ctx
from checker.endpoint_interval_checker import _point,_box,_partition,SQRT2
PANELS=1024; BITS=192; LEFT_N=32; RIGHT_N=64; CENTER_N=16; DEG=50; USTAR=arb(3)/5

def _c(n):
    z=Fraction(1)
    for k in range(n): z*=Fraction((2*k+1)**2,2*(k+1)*(2*k+3))
    return z

def _series(u,gam):
    cs=[_c(n) for n in range(DEG+2)]; R=arb(0); Rp=arb(0); Rpp=arb(0)
    for n,c in enumerate(cs[:DEG+1]):
        a=arb(c.numerator)/c.denominator
        R += a*(u**n)
        if n: Rp += n*a*(u**(n-1))
        if n>1: Rpp += n*(n-1)*a*(u**(n-2))
    U=u.upper(); cn=arb(cs[DEG+1].numerator)/cs[DEG+1].denominator
    R += _box(arb(0),cn*(u**(DEG+1)).upper()/(1-U))
    Rp += _box(arb(0),(DEG+1)*cn*(u**DEG).upper()/(1-U*arb(DEG+2)/(DEG+1)))
    Rpp += _box(arb(0),(DEG+1)*DEG*cn*(u**(DEG-1)).upper()/(1-U*arb(DEG+2)/DEG))
    return R,-2*gam*Rp,4*gam*gam*Rpp-2*Rp

def _density(s,L,dl=False):
    e=s*s; mu=1-e; gap=1+mu; L2=L*L; q=1-mu*mu+L2*mu*mu; w2=mu*mu+L2*(1-mu*mu); w=w2.sqrt()
    H=mu*gap*(1-L2); K=-3*mu*H-gap*q; gam=L/(w*q.sqrt())
    u=e*gap*mu*mu*(1-L2)*(1-L2)/(w2*q)
    gt=-L*e*H/(w*q*q.sqrt()); gtt=L*L2*e*K/(w*q*q*q.sqrt())
    if u.upper()<=USTAR: R,Rg,Rgg=_series(u,gam)
    else:
        R=u.sqrt().asin()/u.sqrt(); Rg=(gam*R-1)/u; Rgg=((R+gam*Rg)*u+2*gam*(gam*R-1))/(u*u)
    if not dl: return s*(4*mu*R*gt-2*(Rg*gt*gt+R*gtt))
    ql=2*L*mu*mu; wl=L*(1-mu*mu)/w2; Hl=-2*L*mu*gap; Kl=-3*mu*Hl-gap*ql
    gl=gam*(1/L-wl-L*mu*mu/q); P=L/(w*q*q.sqrt()); Pl=P*(1/L-wl-3*L*mu*mu/q); gtl=-e*(Pl*H+P*Hl)
    Q=L*L2/(w*q*q*q.sqrt()); Ql=Q*(3/L-wl-5*L*mu*mu/q); gttl=e*(Ql*K+Q*Kl)
    Rl=Rg*gl; Rgl=Rgg*gl
    return s*(4*mu*(Rl*gt+R*gtl)-2*(Rgl*gt*gt+2*Rg*gt*gtl+Rl*gtt+R*gttl))
def _int(a,b,dl):
    grid,root=_partition(PANELS); L=_box(_point(a),_point(b)); z=arb(0)
    for x,y in zip(grid,grid[1:]):
        xx=root if x==SQRT2 else _point(x); yy=root if y==SQRT2 else _point(y); z+=_density(_box(xx,yy),L,dl)*(yy-xx)
    return z
def _boxes(a,b,n):
    d=(b-a)/n; return [(a+i*d,a+(i+1)*d) for i in range(n)]
def verify():
    ctx.prec=BITS; okall=True
    print('CENTER_AXIS_COEFFICIENT_CHECKER — PROTOTYPE / NOT_BINDING')
    for name,a,b,n,dl,sgn in [('LEFT_NEG',Fraction(1,4),Fraction(2,5),LEFT_N,False,'NEG'),('CENTER_DERIV_POS',Fraction(2,5),Fraction(83,200),CENTER_N,True,'POS'),('RIGHT_POS',Fraction(83,200),Fraction(1),RIGHT_N,False,'POS')]:
        worst=None; ok=True
        for l,r in _boxes(a,b,n):
            v=_int(l,r,dl); good=v.upper()<0 if sgn=='NEG' else v.lower()>0; ok &= bool(good); m=-v.upper() if sgn=='NEG' else v.lower()
            if worst is None or m<worst[0]: worst=(m,l,r,v)
        okall &= ok; print(name,'PASS' if ok else 'UNRESOLVED','weakest_box',worst[1],worst[2],'enclosure',worst[3])
    if not okall: raise SystemExit('UNRESOLVED')
if __name__=='__main__': verify()
