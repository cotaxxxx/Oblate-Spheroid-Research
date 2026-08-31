#!/usr/bin/env python3
"""Independent Arb checker for the oblate monotone-tube producer record.

Imports no producer kernel. Reconstructs all 64 parameter-box integrals from
its own formulas and applies only the fixed NEG gate.
"""

from __future__ import annotations

from fractions import Fraction
from math import comb, isqrt
from flint import arb, ctx


class VerificationError(RuntimeError):
    pass


def _point(x):
    return arb(x.numerator) / x.denominator if isinstance(x, Fraction) else arb(x)


def _box(lo, hi):
    return arb((lo + hi) / 2, (hi - lo) / 2)


def _clamp_nonnegative(x):
    lo = max(arb(0), x.lower()); hi = max(arb(0), x.upper())
    return _box(lo, hi)


def _unit_hull(x):
    lo = max(arb(0), x.lower()); hi = min(arb(1), x.upper())
    if hi < lo: raise VerificationError("empty unit intersection")
    return _box(lo, hi)


def _square(x):
    lo, hi = x.lower(), x.upper()
    if lo <= 0 <= hi:
        up = max((-lo) * (-lo), hi * hi)
        return _box(arb(0), up)
    a, b = lo * lo, hi * hi
    return _box(min(a, b), max(a, b))


def _pow(x, n):
    out = arb(1)
    for _ in range(n): out *= x
    return out


def _contains_zero(x):
    return x.lower() <= 0 <= x.upper()


def _zero_to_upper(x):
    hi = max(arb(0), x.upper())
    return arb(hi / 2, hi / 2)


def _series(u, name, degree):
    if not u.upper() < 1: raise VerificationError(f"{name} requires u<1")
    partial = arb(0)
    if name == "Psi":
        for n in range(degree + 1):
            c = Fraction(comb(2*n, n), 4**n * (2*n + 1)); partial += _point(c) * _pow(u, n)
        n = degree + 1; c = Fraction(comb(2*n, n), 4**n * (2*n + 1)); nxt = _point(c) * _pow(u, n)
    elif name == "Psi_prime":
        for n in range(1, degree + 1):
            c = Fraction(n * comb(2*n, n), 4**n * (2*n + 1)); partial += _point(c) * _pow(u, n-1)
        n = degree + 1; c = Fraction(n * comb(2*n, n), 4**n * (2*n + 1)); nxt = _point(c) * _pow(u, n-1)
    else: raise VerificationError("unsupported series")
    return partial + _zero_to_upper(nxt / (1-u))


def _quantities(s, t, lam):
    e = _square(s); gap = 2-e; mu = 1-e; delta = 1-t; d = e-delta
    lam2 = _square(lam); A = 1-t*mu
    q = _clamp_nonnegative(e*gap + lam2*_square(d))
    w2 = lam2*e*gap + _square(mu); w = w2.sqrt(); ht = mu + lam2*d
    H = (1-e)*gap + lam2*(2*e-2*delta-e*e+delta*e)
    return e,gap,mu,d,lam2,A,q,w2,w,ht,H


def _corner(s,t,lam):
    e,gap,mu,d,lam2,A,q,w2,w,ht,H = _quantities(s,t,lam)
    rho = _box(arb(0), 1/gap.lower().sqrt()); phi = arb(0, (1/lam).upper())
    Ahat = gap*s*rho - mu*phi
    R = _box(arb(1), arb.pi()/2); Rg = _box(-arb(1), -arb(1)/3)
    lam3 = lam2*lam; sqrtq = q.sqrt()
    return (-4*mu*R*lam*_pow(rho,3)*H/w
        -2*Rg*lam2*H*H*Ahat*_pow(rho,5)/w2
        -2*R*lam3*Ahat*_pow(rho,3)*(3*phi*H-gap*sqrtq)/w), "corner_hull"


def _ordinary(s,t,lam,degree):
    e,gap,mu,d,lam2,A,q,w2,w,ht,H = _quantities(s,t,lam)
    if not q.lower() > 0: raise VerificationError("ordinary q is not positive")
    sq=q.sqrt(); q32=q*sq; q52=q*q32
    gamma=_unit_hull(lam*A/(w*sq)); u=_unit_hull(_clamp_nonnegative(e*gap*_square(ht)/(w2*q)))
    gt=-lam*e*H/(w*q32); gtt=lam2*lam*e*(3*d*H-gap*q)/(w*q52)
    use_u = _contains_zero(ht) or not u.lower() > 0
    if use_u:
        if not u.upper() < 1: raise VerificationError("upper chart u reaches one")
        R=_series(u,"Psi",degree); Rg=-2*gamma*_series(u,"Psi_prime",degree); chart="u_upper"
    else:
        R=gamma.acos()/u.sqrt(); Rg=(gamma*R-1)/u; chart="gamma_lower"
    return s*(4*mu*R*gt-2*A*(Rg*gt*gt+R*gtt)), chart


def _split(a,b,n):
    w=(b-a)/n
    return [(a+i*w,a+(i+1)*w) for i in range(n)]


def _s_partition(n):
    root=arb(2).sqrt(); rend=isqrt(2*n*n)
    vals=[Fraction(i,n) for i in range(rend+1)]
    return vals+[None],root


def verify(record):
    c=record.get("contract",{})
    expected={"t_domain":["63/64","1"],"lambda_domain":["5/8","33/50"],
        "t_boxes":8,"lambda_boxes":8,"s_panels":1024,"series_degree":50,
        "bits":160,"required_sign":"NEG","sole_gate":"every parameter-box total.upper() < 0"}
    if c != expected: raise VerificationError("contract mismatch")
    ctx.prec=max(192,int(c["bits"])); svals,root=_s_partition(1024)
    tboxes=_split(Fraction(63,64),Fraction(1),8); lboxes=_split(Fraction(5,8),Fraction(33,50),8)
    supplied=record.get("parameter_boxes",[])
    if len(supplied)!=64: raise VerificationError("parameter box count mismatch")
    outputs=[]; k=0
    for ti,(tl,tr) in enumerate(tboxes):
        t=_box(_point(tl),_point(tr))
        for li,(ll,lr) in enumerate(lboxes):
            lam=_box(_point(ll),_point(lr)); total=arb(0)
            counts={"gamma_lower":0,"u_upper":0,"corner_hull":0}
            for si,(sl,sr) in enumerate(zip(svals,svals[1:])):
                left=_point(sl); right=root if sr is None else _point(sr); s=_box(left,right)
                if ti==7 and si==0: val,chart=_corner(s,t,lam)
                else: val,chart=_ordinary(s,t,lam,50)
                counts[chart]+=1; total += val*(right-left)
            rec=supplied[k]; k+=1
            if rec.get("t_box") != [str(tl),str(tr)] or rec.get("lambda_box") != [str(ll),str(lr)]:
                raise VerificationError("box label mismatch")
            if rec.get("chart_counts") != counts: raise VerificationError("chart inventory mismatch")
            if not total.upper() < 0: raise VerificationError(f"GATING FAIL t={tl}:{tr} lambda={ll}:{lr}")
            outputs.append(total)
    if not record.get("gating_pass"): raise VerificationError("producer did not report pass")
    return outputs
