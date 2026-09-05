#!/usr/bin/env python3
"""Independent checker for center-axis coefficient signs. PROTOTYPE / NOT_BINDING."""
from fractions import Fraction
from math import isqrt
from flint import arb,ctx
from checker.endpoint_interval_checker import _point,_box
BITS=192; REG_PANELS=1024; POINT_PANELS=4096; MONO_N=64; DEG=50; USTAR=arb(3)/5; SQRT2='sqrt2'

def _partition(panels):
    root=arb(2).sqrt(); rational_end=isqrt(2*panels*panels)
    vals=[Fraction(i,panels) for i in range(panels+1)]
    vals.extend(Fraction(i,panels) for i in range(panels+1,rational_end+1))
    return vals+[SQRT2],root

def _coeffs():
    out=[Fraction(1)]; z=Fraction(1)
    for k in range(DEG+1):
        z*=Fraction((2*k+1)**2,2*(k+1)*(2*k+3)); out.append(z)
    return out
COEFFS=_coeffs()

def _series(u,gam):
    R=arb(0); Rp=arb(0); Rpp=arb(0); powers=[arb(1)]
    for _ in range(DEG+1): powers.append(powers[-1]*u)
    for n,c in enumerate(COEFFS[:DEG+1]):
        a=arb(c.numerator)/c.denominator; R+=a*powers[n]
        if n: Rp+=n*a*powers[n-1]
        if n>1: Rpp+=n*(n-1)*a*powers[n-2]
    U=u.upper(); c=COEFFS[DEG+1]; cn=arb(c.numerator)/c.denominator
    R+=_box(arb(0),cn*powers[DEG+1].upper()/(1-U))
    Rp+=_box(arb(0),(DEG+1)*cn*powers[DEG].upper()/(1-U*arb(DEG+2)/(DEG+1)))
    Rpp+=_box(arb(0),(DEG+1)*DEG*cn*powers[DEG-1].upper()/(1-U*arb(DEG+2)/DEG))
    return R,-2*gam*Rp,4*gam*gam*Rpp-2*Rp

def _density(s,L,dl=False):
    e=s*s; mu=1-e; gap=1+mu; L2=L*L; q=1-mu*mu+L2*mu*mu; w2=mu*mu+L2*(1-mu*mu); w=w2.sqrt()
    H=mu*gap*(1-L2); K=-3*mu*H-gap*q; gam=L/(w*q.sqrt()); u=e*gap*mu*mu*(1-L2)*(1-L2)/(w2*q)
    gt=-L*e*H/(w*q*q.sqrt()); gtt=L*L2*e*K/(w*q*q*q.sqrt())
    if u.upper()<=USTAR:
        R,Rg,Rgg=_series(u,gam)
    else:
        R=u.sqrt().asin()/u.sqrt(); Rg=(gam*R-1)/u; Rgg=((R+gam*Rg)*u+2*gam*(gam*R-1))/(u*u)
    if not dl:
        return s*(4*mu*R*gt-2*(Rg*gt*gt+R*gtt))
    ql=2*L*mu*mu; wl=L*(1-mu*mu)/w2; Hl=-2*L*mu*gap; Kl=-3*mu*Hl-gap*ql
    gl=gam*(1/L-wl-L*mu*mu/q); P=L/(w*q*q.sqrt()); Pl=P*(1/L-wl-3*L*mu*mu/q); gtl=-e*(Pl*H+P*Hl)
    Q=L*L2/(w*q*q*q.sqrt()); Ql=Q*(3/L-wl-5*L*mu*mu/q); gttl=e*(Ql*K+Q*Kl); Rl=Rg*gl; Rgl=Rgg*gl
    return s*(4*mu*(Rl*gt+R*gtl)-2*(Rgl*gt*gt+2*Rg*gt*gtl+Rl*gtt+R*gttl))

def _int(a,b,dl,panels=REG_PANELS):
    grid,root=_partition(panels); L=_box(_point(a),_point(b)); z=arb(0)
    for x,y in zip(grid,grid[1:]):
        xx=root if x==SQRT2 else _point(x); yy=root if y==SQRT2 else _point(y); z+=_density(_box(xx,yy),L,dl)*(yy-xx)
    return z

def _boxes(a,b,n):
    d=(b-a)/n; return [(a+i*d,a+(i+1)*d) for i in range(n)]

def verify():
    ctx.prec=BITS; worst=None; mono=True
    for l,r in _boxes(Fraction(1,4),Fraction(1),MONO_N):
        v=_int(l,r,True,REG_PANELS); good=v.lower()>0; mono&=bool(good)
        if worst is None or v.lower()<worst[0]: worst=(v.lower(),l,r,v)
    left=_int(Fraction(2,5),Fraction(2,5),False,POINT_PANELS)
    right=_int(Fraction(83,200),Fraction(83,200),False,POINT_PANELS)
    lok=bool(left.upper()<0); rok=bool(right.lower()>0)
    sphere_H=_int(Fraction(1),Fraction(1),False,POINT_PANELS)
    sphere_Hl=_int(Fraction(1),Fraction(1),True,POINT_PANELS)
    exact_H=_point(Fraction(4,3)); exact_Hl=_point(Fraction(8,5))
    sphere_H_ok=bool(sphere_H.contains(exact_H)); sphere_Hl_ok=bool(sphere_Hl.contains(exact_Hl))
    print('CENTER_AXIS_COEFFICIENT_CHECKER — PROTOTYPE / NOT_BINDING')
    print('GLOBAL_DERIV_POS','PASS' if mono else 'UNRESOLVED','weakest_box',worst[1],worst[2],'enclosure',worst[3])
    print('POINT_2_5_NEG','PASS' if lok else 'UNRESOLVED','enclosure',left)
    print('POINT_83_200_POS','PASS' if rok else 'UNRESOLVED','enclosure',right)
    print('SPHERE_H_4_3','PASS' if sphere_H_ok else 'FAIL','enclosure',sphere_H)
    print('SPHERE_HLAMBDA_8_5','PASS' if sphere_Hl_ok else 'FAIL','enclosure',sphere_Hl)
    final_ok=mono and lok and rok and sphere_H_ok and sphere_Hl_ok
    print('LOGICAL_FINAL_CLAIMS','PASS' if final_ok else 'UNRESOLVED','A1/A2 from global monotonicity; A3 by restriction; sphere controls gating')
    if not final_ok: raise SystemExit('UNRESOLVED')
if __name__=='__main__': verify()
