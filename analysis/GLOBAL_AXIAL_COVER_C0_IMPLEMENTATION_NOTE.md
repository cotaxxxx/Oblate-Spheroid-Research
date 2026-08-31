# Global axial cover C0 — implementation note

Status: `CHAT_RAW_AUDIT_PASS / IMPLEMENTED_PROTOTYPE / MACHINE_PENDING / NOT_BINDING`

## Mathematical audit

User raw audit: `CHAT_RAW_AUDIT_PASS`.

Audited identities and logic:

- `Phi(tau,lambda)=g_axis_ob(t,lambda)/t`, `tau=t^2`, analytically continued by `Phi(0,lambda)=H_axis_ob(lambda)`.
- `partial_tau Phi=(1/4) integral_0^1 (1-x^2) partial_t^3 g_axis_ob(x t,lambda) dx`.
- Therefore `partial_t^3 g_axis_ob<0` on the C0 box implies strict `tau`-monotonicity of `Phi`.
- Together with A and the top-edge gate `Phi(25/256,lambda)<0`, this yields the quantitative pitchfork census in `0<=t<=5/16`.
- Exact stable complement for general t:
  `u=(1-mu^2)[mu(1-lambda^2)+lambda^2 t]^2/(w^2 q)`.
- The moving removable locus is `mu_0=-lambda^2 t/(1-lambda^2)`; intervals meeting it must use the analytic Psi chart.

## Fixed box

```text
t in [0,5/16]
lambda in [2/5,83/200]
tau in [0,25/256]
```

## Fixed gates

```text
C0a: partial_t^3 g_axis_ob(t,lambda) < 0
     on [0,5/16] x [2/5,83/200].

C0b: Phi(25/256,lambda) < 0
     for lambda in [2/5,83/200].
```

No `partial_lambda Phi` gate is required.

## HU-V1.2-style first-passing discipline

The producer and checker use the same pinned stage labels but reconstruct their own partitions. No undeclared refinement is permitted after a gating result.

C0a stage column:

```text
A0: t_boxes=8,  lambda_boxes=8,  s_panels=512
A1: t_boxes=16, lambda_boxes=16, s_panels=1024
A2: t_boxes=32, lambda_boxes=32, s_panels=2048
```

C0b stage column:

```text
B0: lambda_boxes=16, s_panels=512
B1: lambda_boxes=32, s_panels=1024
B2: lambda_boxes=64, s_panels=2048
```

The first stage with zero unresolved boxes is authoritative for that gate; later stages are not consulted.

A safe predeclared panel-evaluation budget is printed by both programs as `PREDECLARED_MAX_S_PANEL_EVALS`.

## Precision / chart policy

```text
producer bits = 160
checker bits = 192
Psi degree = 50
u threshold = 3/5
CHECKER_KERNEL = TRANSCRIBED_COPY_NOT_INDEPENDENT_DERIVATION
INDEPENDENCE_SCOPE = PRECISION/PARTITION/GATING
```

For each s,t,lambda interval, u is constructed from the exact factorized complement and intersected only with the exact range `0<=u<=1`.

Chart rule:

```text
if upper(u) <= 3/5:
    use Psi-series chart;
    this includes every interval meeting the moving u=0 locus.
elif lower(u) > 0:
    use direct u/gamma derivative chart.
else:
    mark the box unresolved; do not divide by u, u^2, or u^3.
```

The programs print counts for `series`, `direct`, `series_hits_moving_u0`, and `chart_unresolved`, so the moving-locus handling is raw-auditable from CI logs.

## Implementation pins before machine run

```text
producer: producer/global_axial_c0_producer.py
checker:  checker/global_axial_c0_checker.py
workflow: .github/workflows/oblate-global-axial-c0.yml
```

The C0a density uses the audited general-t recurrence for `gamma_t` through `gamma_tttt`, followed by the factorized `C_tt`, `C_ttt` assembly. C0b evaluates `g_axis_ob(5/16,lambda)/(5/16)` directly; `alpha^2` is evaluated stably as `asin(sqrt(u))^2`.

## REPORTED_NOT_GATING expectations

```text
Phi(25/256,2/5)        ~ -0.044440
Phi(25/256,lambda_c)   ~ -0.025542
Phi(25/256,83/200)     ~ -0.008864
partial_t^3 g on box   ~ -1.51 ... -1.70
root at lambda=83/200  ~ 0.25 < 5/16
```

These are comparison values only.

## Explicit exclusions

This note does not certify C0 before a successful producer/checker machine run and receipt/Judge chain. It does not cover the middle axial region, the boundary band connection, or any off-axis claim.
