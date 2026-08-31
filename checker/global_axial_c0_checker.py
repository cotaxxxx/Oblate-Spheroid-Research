#!/usr/bin/env python3
"""Transcribed-copy checker for C0 quantitative pitchfork gates.

CHECKER_KERNEL=TRANSCRIBED_COPY_NOT_INDEPENDENT_DERIVATION
INDEPENDENCE_SCOPE=PRECISION/PARTITION/GATING
Evidence class: PROTOTYPE / NOT_BINDING.
"""
from fractions import Fraction
from math import isqrt
from flint import arb, ctx
from checker.endpoint_interval_checker import _point, _box

BITS = 192
DEG = 50
USTAR = arb(3) / 5
SQRT2 = "sqrt2"
T_LO, T_HI = Fraction(0), Fraction(5, 16)
L_LO, L_HI = Fraction(2, 5), Fraction(83, 200)
T_EDGE = Fraction(5, 16)
C0A_STAGES = (("A0", 8, 8, 512), ("A1", 16, 16, 1024), ("A2", 32, 32, 2048))
C0B_STAGES = (("B0", 16, 512), ("B1", 32, 1024), ("B2", 64, 2048))
MAX_S_PANEL_EVALS = (
    sum(2 * p * nt * nl for _, nt, nl, p in C0A_STAGES)
    + sum(2 * p * nl for _, nl, p in C0B_STAGES)
)


def _partition(panels):
    root = arb(2).sqrt()
    end = isqrt(2 * panels * panels)
    vals = [Fraction(i, panels) for i in range(end + 1)]
    return vals + [SQRT2], root


def _coeffs():
    out = [Fraction(1)]; c = Fraction(1)
    for k in range(DEG + 2):
        c *= Fraction((2*k+1)**2, 2*(k+1)*(2*k+3)); out.append(c)
    return out
COEFFS = _coeffs()


def _unit_nonnegative(x):
    lo = max(arb(0), x.lower()); hi = min(arb(1), x.upper())
    if hi < lo:
        raise ValueError("empty exact 0<=u<=1 intersection")
    return _box(lo, hi)


def _series(u, gam):
    R=arb(0); Rp=arb(0); Rpp=arb(0); Rppp=arb(0); powers=[arb(1)]
    for _ in range(DEG+1): powers.append(powers[-1]*u)
    for n,c in enumerate(COEFFS[:DEG+1]):
        a=arb(c.numerator)/c.denominator; R += a*powers[n]
        if n: Rp += n*a*powers[n-1]
        if n>1: Rpp += n*(n-1)*a*powers[n-2]
        if n>2: Rppp += n*(n-1)*(n-2)*a*powers[n-3]
    U=u.upper(); c=COEFFS[DEG+1]; cn=arb(c.numerator)/c.denominator
    R += _box(arb(0), cn*powers[DEG+1].upper()/(1-U))
    Rp += _box(arb(0), (DEG+1)*cn*powers[DEG].upper()/(1-U*arb(DEG+2)/(DEG+1)))
    Rpp += _box(arb(0), (DEG+1)*DEG*cn*powers[DEG-1].upper()/(1-U*arb(DEG+2)/DEG))
    Rppp += _box(arb(0), (DEG+1)*DEG*(DEG-1)*cn*powers[DEG-2].upper()/(1-U*arb(DEG+2)/(DEG-1)))
    return R, -2*gam*Rp, 4*gam*gam*Rpp-2*Rp, -8*gam**3*Rppp+12*gam*Rpp


def _geom(s,t,L):
    mu=1-s*s; e=1-mu*mu; L2=L*L; L4=L2*L2; A=1-t*mu; d=t-mu
    q=e+L2*d*d; w2=mu*mu+L2*e; w=w2.sqrt(); gam=L*A/(w*q.sqrt())
    h=mu*(1-L2)+L2*t; u=_unit_nonnegative(e*h*h/(w2*q))
    N=-mu*q-A*L2*d; N1=-L2*e; M=N1*q-3*N*L2*d
    M1=L4*e*d-3*L2*N; P=M1*q-5*M*L2*d
    M2=4*L4*e; P1=M2*q-3*L2*d*M1-5*L2*M
    sq=q.sqrt()
    g1=L*N/(w*q*sq); g2=L*M/(w*q*q*sq); g3=L*P/(w*q*q*q*sq)
    g4=L*(P1*q-7*P*L2*d)/(w*q*q*q*q*sq)
    return mu,A,gam,u,g1,g2,g3,g4


def _R(u,gam,stats):
    if u.upper() <= USTAR:
        stats["series"] += 1
        if u.lower() <= 0: stats["series_hits_moving_u0"] += 1
        return _series(u,gam)
    if u.lower() <= 0:
        stats["chart_unresolved"] += 1; raise ValueError("moving u=0 outside series chart")
    stats["direct"] += 1
    r=u.sqrt().asin()/u.sqrt(); rg=(gam*r-1)/u
    rgg=((r+gam*rg)*u+2*gam*(gam*r-1))/(u*u)
    rggg=(3*gam*(2*gam*gam+3)*r-(11*gam*gam+4))/(u*u*u)
    return r,rg,rgg,rggg


def _g3_density(s,t,L,stats):
    mu,A,gam,u,g1,g2,g3,g4=_geom(s,t,L); R,R1,R2,R3=_R(u,gam,stats)
    C2=R2*g1**3+3*R1*g1*g2+R*g3
    C3=R3*g1**4+6*R2*g1*g1*g2+3*R1*g2*g2+4*R1*g1*g3+R*g4
    return s*(8*mu*C2-2*A*C3)


def _g_density(s,t,L,stats):
    mu,A,gam,u,g1,_,_,_=_geom(s,t,L); R,_,_,_=_R(u,gam,stats)
    a2=u.sqrt().asin()**2
    return s*(-mu*a2-2*A*R*g1)


def _int(tl,tr,ll,lr,panels,mode,stats):
    grid,root=_partition(panels); t=_box(_point(tl),_point(tr)); L=_box(_point(ll),_point(lr)); z=arb(0)
    for a,b in zip(grid,grid[1:]):
        aa=root if a==SQRT2 else _point(a); bb=root if b==SQRT2 else _point(b); s=_box(aa,bb)
        y=_g3_density(s,t,L,stats) if mode=="g3" else _g_density(s,t,L,stats)
        z += y*(bb-aa)
    return z


def _split(a,b,n):
    h=(b-a)/n; return [(a+i*h,a+(i+1)*h) for i in range(n)]


def _gate_a():
    for label,nt,nl,p in C0A_STAGES:
        st={"series":0,"direct":0,"series_hits_moving_u0":0,"chart_unresolved":0}; bad=0; worst=None
        for tl,tr in _split(T_LO,T_HI,nt):
            for ll,lr in _split(L_LO,L_HI,nl):
                try:
                    v=_int(tl,tr,ll,lr,p,"g3",st); good=v.upper()<0
                except (ValueError,ZeroDivisionError): v=None; good=False
                if not good: bad+=1
                if v is not None and (worst is None or v.upper()>worst[0]): worst=(v.upper(),tl,tr,ll,lr,v)
        print("C0A_STAGE",label,"t_boxes",nt,"lambda_boxes",nl,"s_panels",p,"unresolved",bad,"chart_stats",st,"worst",None if worst is None else worst[1:])
        if bad==0: print("C0A_FIRST_PASS",label); return True,label,worst
    return False,None,worst


def _gate_b():
    for label,nl,p in C0B_STAGES:
        st={"series":0,"direct":0,"series_hits_moving_u0":0,"chart_unresolved":0}; bad=0; worst=None
        for ll,lr in _split(L_LO,L_HI,nl):
            try:
                v=_int(T_EDGE,T_EDGE,ll,lr,p,"g",st)/_point(T_EDGE); good=v.upper()<0
            except (ValueError,ZeroDivisionError): v=None; good=False
            if not good: bad+=1
            if v is not None and (worst is None or v.upper()>worst[0]): worst=(v.upper(),ll,lr,v)
        print("C0B_STAGE",label,"lambda_boxes",nl,"s_panels",p,"unresolved",bad,"chart_stats",st,"worst",None if worst is None else worst[1:])
        if bad==0: print("C0B_FIRST_PASS",label); return True,label,worst
    return False,None,worst


def verify():
    ctx.prec=BITS
    print("GLOBAL_AXIAL_C0_CHECKER — PROTOTYPE / NOT_BINDING")
    print("CHECKER_KERNEL TRANSCRIBED_COPY_NOT_INDEPENDENT_DERIVATION")
    print("INDEPENDENCE_SCOPE PRECISION/PARTITION/GATING")
    print("BITS",BITS,"DEG",DEG,"USTAR","3/5")
    print("C0A_STAGES",C0A_STAGES); print("C0B_STAGES",C0B_STAGES); print("PREDECLARED_MAX_S_PANEL_EVALS",MAX_S_PANEL_EVALS)
    a,as_,aw=_gate_a(); b,bs,bw=_gate_b(); ok=a and b
    print("LOGICAL_FINAL_C0","PASS" if ok else "UNRESOLVED","C0a_stage",as_,"C0b_stage",bs)
    if not ok: raise SystemExit("UNRESOLVED")

if __name__=="__main__": verify()
