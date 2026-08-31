#!/usr/bin/env python3
"""Arb producer candidate for the oblate near-boundary monotone tube."""
from __future__ import annotations
from fractions import Fraction
from flint import arb, ctx
from producer.endpoint_interval_producer import SQRT2,_box,_clamp_nonnegative,_partition,_point,_series
T_LEFT=Fraction(63,64); T_RIGHT=Fraction(1); L_LEFT=Fraction(5,8); L_RIGHT=Fraction(33,50)
T_SPLITS=8; L_SPLITS=8; S_PANELS=1024; SERIES_DEGREE=50; BITS=160

def _arb_interval(lo,hi): return _box(_point(lo),_point(hi))
def _unit_hull(x):
    lo=max(arb(0),x.lower()); hi=min(arb(1),x.upper())
    if hi<lo: raise ValueError("empty unit intersection")
    return _box(lo,hi)
def _square(x):
    lo,hi=x.lower(),x.upper()
    if lo<=0<=hi: return _box(arb(0),max((-lo)*(-lo),hi*hi))
    a,b=lo*lo,hi*hi; return _box(min(a,b),max(a,b))
def _pow(x,n):
    out=arb(1)
    for _ in range(n): out*=x
    return out
def _contains_zero(x): return x.lower()<=0<=x.upper()
def _nonfinite(x):
    z=str(x).lower(); return "nan" in z or "inf" in z
def _quantities(s,t,lam):
    e=_square(s); gap=2-e; mu=1-e; delta=1-t; d=e-delta; lam2=_square(lam); A=1-t*mu
    q=_clamp_nonnegative(e*gap+lam2*_square(d)); w2=lam2*e*gap+_square(mu); w=w2.sqrt(); ht=mu+lam2*d
    H=(1-e)*gap+lam2*(2*e-2*delta-e*e+delta*e)
    return e,gap,mu,d,lam2,A,q,w2,w,ht,H
def _corner(s,t,lam):
    e,gap,mu,d,lam2,A,q,w2,w,ht,H=_quantities(s,t,lam); lam3=lam2*lam
    rho=_box(arb(0),1/gap.lower().sqrt()); phi=arb(0,(1/lam).upper()); Ahat=gap*s*rho-mu*phi
    R=_box(arb(1),arb.pi()/2); Rg=_box(-arb(1),-arb(1)/3); sqrtq=q.sqrt()
    return (-4*mu*R*lam*_pow(rho,3)*H/w-2*Rg*lam2*H*H*Ahat*_pow(rho,5)/w2-2*R*lam3*Ahat*_pow(rho,3)*(3*phi*H-gap*sqrtq)/w),"corner_hull"
def _ordinary(s,t,lam,degree):
    e,gap,mu,d,lam2,A,q,w2,w,ht,H=_quantities(s,t,lam)
    if not q.lower()>0: raise ValueError("ordinary chart requires q>0")
    sq=q.sqrt(); q32=q*sq; q52=q*q32; lam3=lam2*lam
    gamma=_unit_hull(lam*A/(w*sq)); u0=_unit_hull(_clamp_nonnegative(e*gap*_square(ht)/(w2*q)))
    glo=max(arb(0),gamma.lower()); ghi=min(arb(1),gamma.upper()); ulo=max(u0.lower(),arb(1)-ghi*ghi); uhi=min(u0.upper(),arb(1)-glo*glo)
    if uhi<ulo: raise ValueError("inconsistent gamma/u enclosures")
    u=_box(ulo,uhi); gc_lo=max(arb(0),arb(1)-u.upper()).sqrt(); gc_hi=max(arb(0),arb(1)-u.lower()).sqrt(); g2lo=max(gamma.lower(),gc_lo); g2hi=min(gamma.upper(),gc_hi)
    if g2hi<g2lo: raise ValueError("empty reciprocal gamma/u intersection")
    gamma=_box(g2lo,g2hi)
    gt=-lam*e*H/(w*q32); gtt=lam3*e*(3*d*H-gap*q)/(w*q52)
    use_u=_contains_zero(ht) or not u.lower()>0
    if use_u:
        if not u.upper()<1: raise ValueError("u_upper requires u<1")
        R,_=_series(u,"Psi",degree,clamped_nonnegative=True); Psip,_=_series(u,"Psi_prime",degree,clamped_nonnegative=True); Rg=-2*gamma*Psip; chart="u_upper"
    else:
        R=gamma.acos()/u.sqrt(); Rg=(gamma*R-1)/u; chart="gamma_lower"
    G=s*(4*mu*R*gt-2*A*(Rg*gt*gt+R*gtt))
    if _nonfinite(G):
        raise ValueError(f"ordinary nonfinite chart={chart} e={e} d={d} A={A} q={q} w2={w2} ht={ht} H={H} gamma={gamma} u={u} gt={gt} gtt={gtt} R={R} Rg={Rg}")
    return G,chart
def _split(a,b,n):
    w=(b-a)/n; return [(a+i*w,a+(i+1)*w) for i in range(n)]
def produce_record(bits=BITS,panels=S_PANELS,degree=SERIES_DEGREE):
    ctx.prec=bits; sends,sqrt2=_partition(panels); tboxes=_split(T_LEFT,T_RIGHT,T_SPLITS); lboxes=_split(L_LEFT,L_RIGHT,L_SPLITS); records=[]; all_pass=True
    for ti,(tl,tr) in enumerate(tboxes):
        t=_arb_interval(tl,tr)
        for li,(ll,lr) in enumerate(lboxes):
            lam=_arb_interval(ll,lr); total=arb(0); counts={"gamma_lower":0,"u_upper":0,"corner_hull":0}
            for si,(sl,sr) in enumerate(zip(sends,sends[1:])):
                left=sqrt2 if sl==SQRT2 else _point(sl); right=sqrt2 if sr==SQRT2 else _point(sr); s=_box(left,right)
                try: val,chart=_corner(s,t,lam) if (ti==7 and si==0) else _ordinary(s,t,lam,degree)
                except ValueError as exc: raise ValueError(f"ti={ti} li={li} si={si} t={tl}:{tr} lambda={ll}:{lr} s={sl}:{sr}; {exc}") from exc
                if _nonfinite(val): raise ValueError(f"nonfinite kernel chart={chart} ti={ti} li={li} si={si} t={tl}:{tr} lambda={ll}:{lr} s={sl}:{sr} value={val}")
                counts[chart]+=1; total+=val*(right-left)
            passed=bool(total.upper()<0); all_pass=all_pass and passed
            records.append({"t_box":[str(tl),str(tr)],"lambda_box":[str(ll),str(lr)],"chart_counts":counts,"total_mid":total.mid().str(50),"total_rad":total.rad().str(50),"upper_negative":passed})
    return {"schema":"bg-oblate-spheroid.monotone-tube.v1","status":"PROTOTYPE_NOT_AUDITED_NOT_BINDING","contract":{"t_domain":["63/64","1"],"lambda_domain":["5/8","33/50"],"t_boxes":8,"lambda_boxes":8,"s_panels":panels,"series_degree":degree,"bits":bits,"required_sign":"NEG","sole_gate":"every parameter-box total.upper() < 0"},"parameter_boxes":records,"gating_pass":all_pass}
