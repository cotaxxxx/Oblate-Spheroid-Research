# Judge request — oblate monotone tube

Status: `EXTERNAL_JUDGE_REQUESTED / NOT_BINDING`

## Target claim

Judge only the following claim:

```text
partial_t g_axis_ob(t,lambda) < 0
for (t,lambda) in [63/64,1] x [5/8,33/50],
with t=1 interpreted one-sidedly.
```

No claim outside this tube is in scope. No census/no-extra-root claim outside the tube is in scope.

## Pinned machine lineage

- refinement contract blob: `5808e84572b1428c58a9b4136b56c4b6f54339cb`
- refinement producer blob: `c2fee40053ab055ce352e93e1c6d1fc43e46310a`
- refinement checker blob: `fd778d6d3a2dc52ae38be87bf4eb800bfbdea6d3`
- raw audit receipt blob after attribution correction: `c3b3666d485a02a5acf4eb856e9c399118a53a9c`
- analytic C2/interchange lemma blob: `7cb9b8091596510203d74e09387bc1e8188b8b47`
- successful machine receipt: Actions #87, run id `33362970980`, refinement step SUCCESS, zero unresolved boxes
- later repeat: Actions #107, run id `33369692803`, refinement step SUCCESS

The failed fixed-initial-contract step in those workflows is intentionally retained historical evidence and is **not** the refinement gate. The separately declared refinement step is the relevant machine result.

## Machine contract

```text
t domain      = [63/64,1]
lambda domain = [5/8,33/50]
t boxes       = 8 exact boxes
lambda boxes  = 8 exact boxes
s partition   = inherited exact 1024-panel partition
producer bits = 160
checker bits  = 192
series degree = 50
u_star        = 3/5
required sign = NEG
sole gate     = every parameter-box total.upper() < 0
```

The checker reconstructs all 64 exact parameter boxes, the s cover, chart inventories and the density independently of the refinement producer.

## Algebra to audit

Pre-limit notation:

```text
mu=1-s^2, delta=1-t, d=s^2-delta,
A=1-t*mu,
q=s^2(2-s^2)+lambda^2 d^2,
w^2=lambda^2 s^2(2-s^2)+mu^2,
N=-s^2 H.
```

Formal second derivative:

```text
G_t=s[4 mu R gamma_t -2A(R_gamma gamma_t^2+R gamma_tt)].
```

Scaled identity on q>0:

```text
rho=s/sqrt(q), phi=d/sqrt(q), Ahat=A/sqrt(q),

T1=-4 mu R lambda rho^3 H/w,
T2=-2 R_gamma lambda^2 H^2 Ahat rho^5/w^2,
T3=-2 R lambda^3 Ahat rho^3[3 phi H-(2-s^2)sqrt(q)]/w,
G_t=T1+T2+T3.
```

## Chart policy to audit

Ordinary cells:

```text
u_hi <= 3/5 -> u_upper
u_lo >= 3/5 -> gamma_lower
crossing     -> T1/T2/T3 independently enclosed in both admissible charts,
                then intersected term by term
```

with

```text
u_upper:     R=Psi(u), R_gamma=-2 gamma Psi_prime(u)
gamma_lower: R=acos(gamma)/sqrt(u), R_gamma=(gamma R-1)/u.
```

The ordinary computation intersects the two exact forms of `A`, intersects factorized `u` with `1-gamma^2`, then tightens gamma back from u.

Corner cell only (`last t-box x first s-cell`): no division by q; use the a-priori hulls

```text
rho in [0,1/sqrt(gap_lo)],
phi in [-1/lambda_lo,1/lambda_lo],
Ahat=gap*s*rho-mu*phi,
R in [1,pi/2],
R_gamma in [-1,-1/3],
sqrt(q) in [0,sqrt(q_upper)].
```

## Analytic interchange obligation

Audit `analysis/MONOTONE_TUBE_C2_INTERCHANGE_LEMMA.md` independently. The intended key observation is that on `s in [0,1]`

```text
rho^2(2-s^2)+lambda^2 phi^2=1
```

gives uniform bounds on `rho`, `phi` and `Ahat`; therefore the scaled `T1,T2,T3` admit a uniform integrable majorant up to `t=1`. On `s in [1,sqrt(2)]`, q is uniformly bounded away from zero. Dominated differentiation plus the existing C1 endpoint continuity then identifies the endpoint integral with the one-sided derivative.

## Requested Judge output

Record exactly one of:

```text
PASS
FAIL: <specific mathematical or provenance defect>
UNRESOLVED: <specific missing obligation>
```

A PASS must identify the audited blobs/run and must be limited to the target claim above. It must not promote unrelated census or global no-fold claims.
