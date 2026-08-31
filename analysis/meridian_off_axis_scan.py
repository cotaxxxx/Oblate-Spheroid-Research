#!/usr/bin/env python3
"""DIAGNOSTIC_ONLY / NOT_BINDING meridian stationary-point scan.

Requires numpy for vectorized binary64 quadrature.  The theorem statement must not
be inferred from this scan without a later certified contract.
"""
from __future__ import annotations
import math
from dataclasses import dataclass
from typing import List, Tuple

try:
    import numpy as np
except ImportError as exc:
    raise SystemExit("This diagnostic requires numpy; no certification depends on it.") from exc

import mpmath as mp

LAMBDAS = [0.30, 0.50, 0.60, 0.65, 0.80, 0.95]
BASE_NMU, BASE_NPHI = 160, 256
REF_NMU, REF_NPHI = 240, 512
Q_GRID = np.arange(0.02, 0.981, 0.02, dtype=float)
TH_GRID = np.arange(49, dtype=float) * (math.pi / 96.0)
AXIS_TOL = 5e-6
VALIDATION_COMPONENT_TOL = 1e-8
VALIDATION_RESIDUAL_TOL = 1e-8
ROOT_PREVALIDATION_TOL = 1e-10
NEAR_BOUNDARY_Q = 0.95

# Reported expectations are independent controls only; they are not produced by
# the meridian evaluator and do not gate theorem claims.
REPORTED = {
    (5.0/8.0, 63.0/64.0): 4.37e-4,
    (5.0/8.0, 31.0/32.0): 1.9997e-2,
    (0.60, 1.0): -4.9168e-2,
    (1.00, 1.0): math.pi * math.pi / 32.0,
}


def _ralpha(alpha: np.ndarray, s: np.ndarray) -> np.ndarray:
    out = np.empty_like(alpha)
    small = np.abs(alpha) < 1e-5
    a2 = alpha[small] * alpha[small]
    out[small] = 1.0 + a2/6.0 + 7.0*a2*a2/360.0
    out[~small] = alpha[~small] / s[~small]
    return out


@dataclass
class MeridianEvaluator:
    lam: float
    nmu: int
    nphi: int

    def __post_init__(self):
        mu, wt = np.polynomial.legendre.leggauss(self.nmu)
        phi = (2.0 * math.pi / self.nphi) * np.arange(self.nphi, dtype=float)
        self.mu = mu[:, None]
        self.wmu = wt[:, None]
        self.phi = phi[None, :]
        self.dphi = 2.0 * math.pi / self.nphi
        self.a = np.sqrt(np.maximum(0.0, 1.0 - self.mu*self.mu))
        self.cp = np.cos(self.phi)
        self.sp = np.sin(self.phi)
        self.x = self.a * self.cp
        self.y = self.a * self.sp
        self.zs = self.lam * self.mu
        self.Nr = self.lam * self.a * self.cp
        self.Nz = self.mu
        self.w = np.sqrt(self.lam*self.lam*(1.0-self.mu*self.mu) + self.mu*self.mu)
        self.pref = 1.0 / (4.0 * math.pi * self.lam)

    def gradient_rz(self, r: float, z: float) -> Tuple[float,float,float]:
        dx = self.x - r
        dy = self.y
        dz = self.zs - z
        D2 = dx*dx + dy*dy + dz*dz
        D = np.sqrt(D2)
        h = self.lam*(1.0-r*self.a*self.cp) - z*self.mu
        c_raw = h/(D*self.w)
        violation = float(max(np.max(c_raw-1.0), np.max(-1.0-c_raw), 0.0))
        c = np.clip(c_raw, -1.0, 1.0)
        alpha = np.arccos(c)
        sina = np.sqrt(np.maximum(0.0, 1.0-c*c))
        R = _ralpha(alpha, sina)
        dcr = -self.Nr/(D*self.w) + h*dx/(D2*D*self.w)
        dcz = -self.Nz/(D*self.w) + h*dz/(D2*D*self.w)
        Gr = -self.Nr*alpha*alpha - 2.0*h*R*dcr
        Gz = -self.Nz*alpha*alpha - 2.0*h*R*dcz
        Er = self.pref * self.dphi * float(np.sum(self.wmu*Gr))
        Ez = self.pref * self.dphi * float(np.sum(self.wmu*Gz))
        return Er, Ez, violation

    def gradient_qtheta(self, q: float, th: float) -> Tuple[float,float,float,float,float]:
        r = q*math.sin(th)
        z = self.lam*q*math.cos(th)
        Er, Ez, viol = self.gradient_rz(r,z)
        Gq = math.sin(th)*Er + self.lam*math.cos(th)*Ez
        Gt = q*math.cos(th)*Er - self.lam*q*math.sin(th)*Ez
        return Gq, Gt, Er, Ez, viol


def axial_reference(t: float, lam: float, dps: int = 70) -> mp.mpf:
    """Independent high-precision transformed axial first-derivative kernel."""
    mp.mp.dps = dps
    L = mp.mpf(lam); T = mp.mpf(t)
    def f(s):
        mu = 1-s*s
        A = 1-T*mu
        d = T-mu
        q = s*s*(2-s*s) + L*L*d*d
        w2 = L*L*s*s*(2-s*s) + mu*mu
        w = mp.sqrt(w2)
        if q == 0:
            return mp.mpf('0')
        gam = L*A/(w*mp.sqrt(q))
        gam = min(mp.mpf(1), max(mp.mpf(-1), gam))
        al = mp.acos(gam)
        sa = mp.sqrt(max(mp.mpf('0'), 1-gam*gam))
        R = mp.mpf(1) if al == 0 else al/sa
        H = (1-s*s)*(2-s*s) + L*L*(2*s*s-2*(1-T)-s**4+(1-T)*s*s)
        gt = -L*s*s*H/(w*q**mp.mpf('1.5'))
        return s*(-mu*al*al - 2*A*R*gt)
    return mp.quad(f, [0, 1, mp.sqrt(2)])


def axis_consistency_control() -> bool:
    controls = [
        (5.0/8.0, 63.0/64.0),
        (5.0/8.0, 31.0/32.0),
        (0.60, 1.0),
        (1.00, 1.0),
    ]
    ok = True
    print("AXIS CONSISTENCY CONTROL")
    for lam,t in controls:
        ev = MeridianEvaluator(lam, REF_NMU, REF_NPHI)
        Gq,_,_,_,viol = ev.gradient_qtheta(t,0.0)
        ref = float(axial_reference(t,lam))
        expect = REPORTED[(lam,t)]
        dref = abs(Gq-ref)
        dexp = abs(ref-expect)
        sign_ok = (Gq == 0 and ref == 0) or (Gq*ref > 0)
        this_ok = sign_ok and dref <= AXIS_TOL
        # Endpoint quadrature is permitted a looser diagnostic comparison to the
        # rounded expectation but must still match the independent axial kernel.
        print(f"lambda={lam:.12g} t={t:.12g} meridian={Gq:.17g} axial_ref={ref:.17g} "
              f"abs_diff={dref:.3e} reported={expect:.17g} ref_reported_diff={dexp:.3e} "
              f"clamp_violation={viol:.3e} pass={this_ok}")
        ok = ok and this_ok
    print("AXIS_CONSISTENCY_CONTROL:", "PASS" if ok else "FAIL")
    return ok


def jacobian(ev: MeridianEvaluator, q: float, th: float, h: float=1e-5) -> np.ndarray:
    hq = min(h, 0.45*q, 0.45*(1.0-q))
    ht = min(h, max(1e-8,0.45*(th+1e-12)), max(1e-8,0.45*(math.pi/2-th+1e-12)))
    def F(qq,tt):
        a,b,_,_,_ = ev.gradient_qtheta(qq,tt)
        return np.array([a,b],dtype=float)
    if q-hq <= 0 or q+hq >= 1: hq = min(h, q/3, (1-q)/3)
    if th-ht < 0:
        f0,f1 = F(q,th),F(q,th+ht); cth=(f1-f0)/ht
    elif th+ht > math.pi/2:
        f0,f1 = F(q,th-ht),F(q,th); cth=(f1-f0)/ht
    else:
        cth=(F(q,th+ht)-F(q,th-ht))/(2*ht)
    cq=(F(q+hq,th)-F(q-hq,th))/(2*hq)
    return np.column_stack([cq,cth])


def refine_seed(ev: MeridianEvaluator, q0: float, th0: float) -> Tuple[float,float,float]:
    q,th=q0,th0
    for _ in range(30):
        F=np.array(ev.gradient_qtheta(q,th)[:2],dtype=float)
        n=float(np.linalg.norm(F))
        if n < ROOT_PREVALIDATION_TOL: break
        J=jacobian(ev,q,th)
        try:
            step=np.linalg.solve(J,-F)
        except np.linalg.LinAlgError:
            step=np.linalg.lstsq(J,-F,rcond=None)[0]
        scale=1.0
        accepted=False
        for _ in range(20):
            qn=q+scale*step[0]; tn=th+scale*step[1]
            if 0 < qn < 1 and 0 <= tn <= math.pi/2:
                Fn=np.array(ev.gradient_qtheta(qn,tn)[:2])
                if np.linalg.norm(Fn) <= max(n,1e-14):
                    q,th=qn,tn; accepted=True; break
            scale*=0.5
        if not accepted: break
    F=np.array(ev.gradient_qtheta(q,th)[:2])
    return q,th,float(np.linalg.norm(F))


def seeds_from_grid(Gq: np.ndarray, Gt: np.ndarray) -> List[Tuple[int,int]]:
    norm=np.hypot(Gq,Gt); seeds=set()
    nq,nt=Gq.shape
    for i in range(nq-1):
        for j in range(nt-1):
            a=Gq[i:i+2,j:j+2]; b=Gt[i:i+2,j:j+2]
            if a.min()<=0<=a.max() and b.min()<=0<=b.max(): seeds.add((i,j))
            if np.min(norm[i:i+2,j:j+2]) < 5e-3: seeds.add((i,j))
    for i in range(1,nq-1):
        for j in range(1,nt-1):
            x=norm[i,j]
            if x<2e-2 and x<=np.min(norm[i-1:i+2,j-1:j+2]): seeds.add((i-1,j-1))
    return sorted(seeds)


def scan_lambda(lam: float):
    ev=MeridianEvaluator(lam,BASE_NMU,BASE_NPHI)
    Gq=np.empty((len(Q_GRID),len(TH_GRID))); Gt=np.empty_like(Gq)
    for i,q in enumerate(Q_GRID):
        for j,th in enumerate(TH_GRID):
            Gq[i,j],Gt[i,j],_,_,_=ev.gradient_qtheta(float(q),float(th))
    seeds=seeds_from_grid(Gq,Gt)
    cands=[]
    for i,j in seeds:
        q0=float(0.5*(Q_GRID[i]+Q_GRID[min(i+1,len(Q_GRID)-1)]))
        t0=float(0.5*(TH_GRID[j]+TH_GRID[min(j+1,len(TH_GRID)-1)]))
        q,th,res=refine_seed(ev,q0,t0)
        if th < 1e-7: continue
        if not (0<q<1 and 0<=th<=math.pi/2): continue
        if any(math.hypot(q-a[0],th-a[1])<1e-6 for a in cands): continue
        cands.append((q,th,res))
    ref=MeridianEvaluator(lam,REF_NMU,REF_NPHI)
    rows=[]
    for q,th,res in cands:
        cq,ct,Er,Ez,viol=ev.gradient_qtheta(q,th)
        rq,rt,rEr,rEz,rviol=ref.gradient_qtheta(q,th)
        rres=math.hypot(rq,rt)
        stable=max(abs(rq-cq),abs(rt-ct))<VALIDATION_COMPONENT_TOL and rres<VALIDATION_RESIDUAL_TOL
        cls="EQUATORIAL_ORBIT" if abs(th-math.pi/2)<1e-6 else "GENERIC_OFF_AXIS_ORBIT"
        if q>NEAR_BOUNDARY_Q and not stable: cls="NEAR_BOUNDARY_UNRELIABLE"
        J=jacobian(ref,q,th); eig=np.linalg.eigvals(J)
        rows.append((q,th,q*math.sin(th),lam*q*math.cos(th),rEr,rEz,rq,rt,rres,res,cls,eig,rviol,stable))
    minnorm=float(np.min(np.hypot(Gq[:,1:],Gt[:,1:])))
    print(f"\nLAMBDA {lam:.12g}")
    print("number_of_off_axis_candidates",len(rows))
    for k,row in enumerate(rows,1):
        q,th,r,z,Er,Ez,rq,rt,rres,cres,cls,eig,viol,stable=row
        print(f"candidate {k}: q={q:.17g} theta={th:.17g} r={r:.17g} z={z:.17g} "
              f"E_r={Er:.17g} E_z={Ez:.17g} G_q={rq:.17g} G_theta={rt:.17g} "
              f"grad_norm={rres:.3e} coarse_residual={cres:.3e} class={cls} "
              f"J_eigs={eig} clamp_violation={viol:.3e} refined_stable={stable}")
    found=any(row[10] != "NEAR_BOUNDARY_UNRELIABLE" for row in rows)
    eq=any(row[10]=="EQUATORIAL_ORBIT" for row in rows)
    print("OFF_AXIS_FOUND:","YES" if found else "NO")
    print("EQUATORIAL_FOUND:","YES" if eq else "NO")
    print("MIN_OFF_AXIS_GRAD_NORM_ON_GRID",f"{minnorm:.17g}")


def center_hessian_hints():
    print("\nCENTER AXIS HESSIAN HINTS")
    for lam in LAMBDAS:
        vals=[]
        for eps in (1e-4,3e-4,1e-3):
            v=float(axial_reference(eps,lam,60))/eps; vals.append(v)
        if all(v>0 for v in vals): hint="POS"
        elif all(v<0 for v in vals): hint="NEG"
        else: hint="UNRESOLVED"
        print(f"lambda={lam:.12g} H_estimates={vals} CENTER_AXIS_HESSIAN_SIGN_HINT={hint}")


def main():
    print("MERIDIAN OFF-AXIS SCAN — DIAGNOSTIC_ONLY / NOT_BINDING")
    if not axis_consistency_control():
        raise SystemExit("ABORT: axis consistency control failed")
    center_hessian_hints()
    for lam in LAMBDAS: scan_lambda(lam)

if __name__ == "__main__": main()
