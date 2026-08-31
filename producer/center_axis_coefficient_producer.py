#!/usr/bin/env python3
"""PROTOTYPE / NOT_BINDING Arb producer for center-axis coefficient claims."""
from fractions import Fraction
from flint import arb, ctx
from producer.endpoint_interval_producer import _point,_box,_partition,SQRT2
BITS=160; REG_PANELS=1024; POINT_PANELS=4096; MONO_N=64; DEG=50; USTAR=arb(3)/5

def _coeffs():
    out=[Fraction(1)]; c=Fraction(1)
    for k in range(DEG+2):
        c*=Fraction((2*k+1)**2,2*(k+1)*(2*k+3)); out.append(c)
    return out
COEFFS=_coeffs()

def _psi_bundle(u,gamma):
    R=arb(0); Rp=arb(0); Rpp=arb(0)
    p0=arb(1)
    powers=[p0]
    for _ in range(DEG+1): powers.append(powers[-1]*u)
    for n,c in enumerate(COEFFS[:DEG+1]):
        a=arb(c.numerator)/c.denominator; R+=a*powers[n]
        if n: Rp+=n*a*powers[n-1]
        if n>1: Rpp+=n*(n-1)*a*powers[n-2]
    U=u.upper(); c=COEFFS[DEG+1]; cn=arb(c.numerator)/c.denominator
    R+=_box(arb(0),cn*powers[DEG+1].upper()/(1-U))
    Rp+=_box(arb(0),(DEG+1)*cn*powers[DEG].upper()/(1-U*arb(DEG+2)/(DEG+1)))
    Rpp+=_box(arb(0),(DEG+1)*DEG*cn*powers[DEG-1].upper()/(1-U*arb(DEG+2)/DEG))
    return R,-2*gamma*Rp,4*gamma*gamma*Rpp-2*Rp

def _kernel(s,lam,derivative=False):
    e=s*s; mu=1-e; gap=1+mu; l2=lam*lam
    q=1-mu*mu+l2*mu*mu; w2=mu*mu+l2*(1-mu*mu); w=w2.sqrt()
    H=mu*gap*(1-l2); K=-3*mu*H-gap*q; gamma=lam/(w*q.sqrt())
    u=e*gap*mu*mu*(1-l2)*(1-l2)/(w2*q)
    gt=-lam*e*H/(w*q*q.sqrt()); gtt=lam*l2*e*K/(w*q*q*q.sqrt())
    if u.upper()<=USTAR:
        R,Rg,Rgg=_psi_bundle(u,gamma)
    else:
        R=u.sqrt().asin()/u.sqrt(); Rg=(gamma*R-1)/u
        Rgg=((R+gamma*Rg)*u+2*gamma*(gamma*R-1))/(u*u)
    if not derivative:
        return s*(4*mu*R*gt-2*(Rg*gt*gt+R*gtt))
    ql=2*lam*mu*mu; wl=lam*(1-mu*mu)/w2; Hl=-2*lam*mu*gap; Kl=-3*mu*Hl-gap*ql
    gl=gamma*(1/lam-wl-lam*mu*mu/q)
    P=lam/(w*q*q.sqrt()); Pl=P*(1/lam-wl-3*lam*mu*mu/q); gtl=-e*(Pl*H+P*Hl)
    Q=lam*l2/(w*q*q*q.sqrt()); Ql=Q*(3/lam-wl-5*lam*mu*mu/q); gttl=e*(Ql*K+Q*Kl)
    Rl=Rg*gl; Rgl=Rgg*gl
    return s*(4*mu*(Rl*gt+R*gtl)-2*(Rgl*gt*gt+2*Rg*gt*gtl+Rl*gtt+R*gttl))

def integrate(ll,rr,derivative=False,panels=REG_PANELS):
    grid,root=_partition(panels); lam=_box(_point(ll),_point(rr)); total=arb(0)
    for a,b in zip(grid,grid[1:]):
        aa=root if a==SQRT2 else _point(a); bb=root if b==SQRT2 else _point(b)
        total+=_kernel(_box(aa,bb),lam,derivative)*(bb-aa)
    return total

def split(a,b,n):
    d=(b-a)/n; return [(a+i*d,a+(i+1)*d) for i in range(n)]

def run():
    ctx.prec=BITS
    worst=None; mono_ok=True
    for ll,rr in split(Fraction(1,4),Fraction(1),MONO_N):
        x=integrate(ll,rr,True,REG_PANELS); good=x.lower()>0; mono_ok &= bool(good)
        if worst is None or x.lower()<worst[0]: worst=(x.lower(),ll,rr,x)
    left=integrate(Fraction(2,5),Fraction(2,5),False,POINT_PANELS)
    right=integrate(Fraction(83,200),Fraction(83,200),False,POINT_PANELS)
    left_ok=bool(left.upper()<0); right_ok=bool(right.lower()>0)
    sphere_H=integrate(Fraction(1),Fraction(1),False,POINT_PANELS)
    sphere_Hl=integrate(Fraction(1),Fraction(1),True,POINT_PANELS)
    exact_H=_point(Fraction(4,3)); exact_Hl=_point(Fraction(8,5))
    sphere_H_ok=bool(sphere_H.contains(exact_H)); sphere_Hl_ok=bool(sphere_Hl.contains(exact_Hl))
    print('CENTER_AXIS_COEFFICIENT_PRODUCER — PROTOTYPE / NOT_BINDING')
    print('GLOBAL_DERIV_POS', 'PASS' if mono_ok else 'UNRESOLVED', 'weakest_box',worst[1],worst[2],'enclosure',worst[3])
    print('POINT_2_5_NEG', 'PASS' if left_ok else 'UNRESOLVED', 'enclosure',left)
    print('POINT_83_200_POS', 'PASS' if right_ok else 'UNRESOLVED', 'enclosure',right)
    print('SPHERE_H_4_3', 'PASS' if sphere_H_ok else 'FAIL', 'enclosure',sphere_H)
    print('SPHERE_HLAMBDA_8_5', 'PASS' if sphere_Hl_ok else 'FAIL', 'enclosure',sphere_Hl)
    final_ok=mono_ok and left_ok and right_ok and sphere_H_ok and sphere_Hl_ok
    print('LOGICAL_FINAL_CLAIMS', 'PASS' if final_ok else 'UNRESOLVED', 'A1/A2 from global monotonicity; A3 by restriction; sphere controls gating')
    if not final_ok: raise SystemExit('UNRESOLVED')
if __name__=='__main__': run()
