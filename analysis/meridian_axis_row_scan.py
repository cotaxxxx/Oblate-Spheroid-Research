#!/usr/bin/env python3
"""DIAGNOSTIC_ONLY / NOT_BINDING axial-row scan using MeridianEvaluator theta=0."""
import math
import numpy as np
from analysis.meridian_off_axis_scan import MeridianEvaluator, REF_NMU, REF_NPHI

LAMBDAS=[0.30,0.50,0.60,0.65,0.80,0.95]
N=2000

def g(ev,t):
    return ev.gradient_qtheta(float(t),0.0)[0]

def bisect(ev,a,b,fa,fb):
    for _ in range(70):
        m=(a+b)/2.0; fm=g(ev,m)
        if fm==0 or (b-a)<1e-13: return m,fm
        if fa*fm<=0: b,fb=m,fm
        else: a,fa=m,fm
    m=(a+b)/2.0
    return m,g(ev,m)

def main():
    print('MERIDIAN AXIS ROW SCAN — DIAGNOSTIC_ONLY / NOT_BINDING')
    ts=np.linspace(1e-5,1.0,N+1)
    for lam in LAMBDAS:
        ev=MeridianEvaluator(lam,REF_NMU,REF_NPHI)
        vals=np.array([g(ev,t) for t in ts])
        roots=[]
        for i in range(N):
            fa,fb=vals[i],vals[i+1]
            if fa==0.0: roots.append((ts[i],fa))
            elif fa*fb<0:
                roots.append(bisect(ev,ts[i],ts[i+1],fa,fb))
        # merge numerical duplicates
        merged=[]
        for r,fr in roots:
            if not merged or abs(r-merged[-1][0])>1e-7: merged.append((r,fr))
        print(f'\nLAMBDA {lam:.12g}')
        print('sample_count',len(ts))
        print('sample_min',format(vals.min(),'.17g'))
        print('sample_max',format(vals.max(),'.17g'))
        print('all_samples_negative',bool(np.all(vals<0)))
        print('all_samples_positive',bool(np.all(vals>0)))
        print('nonzero_root_count',len(merged))
        for k,(r,fr) in enumerate(merged,1):
            print(f'root {k}: t={r:.17g} g={fr:.3e}')
        # selected sign checkpoints
        for t in (1e-5,0.05,0.25,0.5,0.75,0.9,0.95,0.98,1.0):
            print(f'g({t:.5f})={g(ev,t): .17g}')

if __name__=='__main__': main()
