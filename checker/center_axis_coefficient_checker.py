#!/usr/bin/env python3
"""Independent checker for center-axis coefficient sign claims. PROTOTYPE / NOT_BINDING."""
from fractions import Fraction
from flint import arb, ctx
from checker.endpoint_interval_checker import _point,_box,_partition,SQRT2

PANELS=1024
BITS=192
LEFT_N=32
RIGHT_N=64
CENTER_N=16


def _fixed_endpoint_hulls():
    return _box(arb(1),arb(2)), _box(-arb(1),-arb(1)/3), _box(arb(0),arb(2))


def _density(s,L,want_lambda_derivative=False,fixed_endpoint=False):
    s2=s*s; mu=1-s2; gap=1+mu; L2=L*L
    qq=1-mu*mu+L2*mu*mu
    ww2=mu*mu+L2*(1-mu*mu); ww=ww2.sqrt()
    HH=mu*gap*(1-L2)
    KK=-3*mu*HH-gap*qq
    gam=L/(ww*qq.sqrt())
    gam_t=-L*s2*HH/(ww*qq*qq.sqrt())
    gam_tt=L*L2*s2*KK/(ww*qq*qq*qq.sqrt())
    if fixed_endpoint:
        RR,RRg,RRgg=_fixed_endpoint_hulls()
    else:
        uu=1-gam*gam
        RR=gam.acos()/uu.sqrt()
        RRg=(gam*RR-1)/uu
        RRgg=((RR+gam*RRg)*uu+2*gam*(gam*RR-1))/(uu*uu)
    base=s*(4*mu*RR*gam_t-2*(RRg*gam_t*gam_t+RR*gam_tt))
    if not want_lambda_derivative:
        return base
    qq_L=2*L*mu*mu
    wwlog=L*(1-mu*mu)/ww2
    HH_L=-2*L*mu*gap
    KK_L=-3*mu*HH_L-gap*qq_L
    gam_L=gam*(1/L-wwlog-L*mu*mu/qq)
    PP=L/(ww*qq*qq.sqrt())
    PP_L=PP*(1/L-wwlog-3*L*mu*mu/qq)
    gam_t_L=-s2*(PP_L*HH+PP*HH_L)
    QQ=L*L2/(ww*qq*qq*qq.sqrt())
    QQ_L=QQ*(3/L-wwlog-5*L*mu*mu/qq)
    gam_tt_L=s2*(QQ_L*KK+QQ*KK_L)
    RR_L=RRg*gam_L
    RRg_L=RRgg*gam_L
    return s*(4*mu*(RR_L*gam_t+RR*gam_t_L)-2*(RRg_L*gam_t*gam_t+2*RRg*gam_t*gam_t_L+RR_L*gam_tt+RR*gam_tt_L))


def _integral(a,b,deriv):
    grid,root=_partition(PANELS); L=_box(_point(a),_point(b)); acc=arb(0); last=len(grid)-2
    for idx,(x,y) in enumerate(zip(grid,grid[1:])):
        xa=root if x==SQRT2 else _point(x); ya=root if y==SQRT2 else _point(y)
        cell=_box(xa,ya)
        acc += _density(cell,L,deriv,idx==0 or idx==last)*(ya-xa)
    return acc


def _boxes(a,b,n):
    h=(b-a)/n
    return [(a+k*h,a+(k+1)*h) for k in range(n)]


def verify():
    ctx.prec=BITS
    specs=[
        ('LEFT_NEG',Fraction(1,4),Fraction(2,5),LEFT_N,False,'NEG'),
        ('CENTER_DERIV_POS',Fraction(2,5),Fraction(83,200),CENTER_N,True,'POS'),
        ('RIGHT_POS',Fraction(83,200),Fraction(1,1),RIGHT_N,False,'POS')]
    print('CENTER_AXIS_COEFFICIENT_CHECKER — PROTOTYPE / NOT_BINDING')
    all_ok=True
    for name,a,b,n,deriv,sgn in specs:
        weakest=None; ok=True
        for l,r in _boxes(a,b,n):
            v=_integral(l,r,deriv)
            good=v.upper()<0 if sgn=='NEG' else v.lower()>0
            ok &= bool(good)
            m=-v.upper() if sgn=='NEG' else v.lower()
            if weakest is None or m<weakest[0]: weakest=(m,l,r,v)
        all_ok &= ok
        print(name,'PASS' if ok else 'UNRESOLVED','weakest_box',weakest[1],weakest[2],'enclosure',weakest[3])
    if not all_ok: raise SystemExit('UNRESOLVED')

if __name__=='__main__': verify()
