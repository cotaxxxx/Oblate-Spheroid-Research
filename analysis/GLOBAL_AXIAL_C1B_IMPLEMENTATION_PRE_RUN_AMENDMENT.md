# C1b implementation-detail pre-run amendment

Status: `PREDECLARED_AMENDMENT / MACHINE_NOT_RUN / NOT_BINDING`

This file fixes two implementation details left open by the parent contract before the first full C1b machine run. It does not change any mathematical sign gate, T/E stage, precision, tube width, predictor-acceptance constant, or refinement depth.

## 1. Non-gating predictor scan work

The P1 scan declared in `GLOBAL_AXIAL_C1B_PREDICTOR_PRE_RUN_AMENDMENT.md` uses Arb point boxes at producer/checker precision with

```text
s_panels = 256
```

for candidate generation only. The midpoint of each resulting Arb ball is used only to choose the first displayed `+` to `-` adjacent grid pair. These scan values are `REPORTED / NON_GATING` and may not discharge a wall, localization, exterior, or monotonicity obligation.

With fewer than `2*s_panels` s-cells per point, the absolute scan-work safety ceiling per attempted slab is

```text
513 * 2 * 256 = 262,656 s-cell evaluations.
```

This work is reported separately from the parent C1b gating ceiling.

## 2. E0 exact t allocation

The parent contract fixes `E0: initial t_boxes=24, lambda_boxes=8` for the exact exterior remainder. If both left and right exterior pieces are nonempty, the 24 t boxes are allocated proportionally to their exact rational widths, with a minimum of one box on each nonempty side. The left count is

```text
n_left = clamp(floor(24 * width_left / (width_left+width_right)), 1, 23)
```

and `n_right=24-n_left`. If only one exterior side is nonempty it receives all 24 boxes. Each side is then split into equal exact-rational subintervals.

Thus E0 always has exactly 24 t intervals across the nonempty exterior pieces, before the lambda product is formed.

## 3. E1/E2 local bisection

Each unresolved exterior rectangle `[t_L,t_R] x [lambda_L,lambda_R]` is bisected once in both coordinates at exact rational midpoints, producing four children. Resolved boxes are not recomputed. E1 and E2 apply this same local four-child rule to unresolved parents only.

The existing hard cap of 4096 live/terminal exterior boxes and the existing panel ceilings remain unchanged.
