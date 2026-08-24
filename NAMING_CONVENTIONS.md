# Naming Conventions

These conventions prevent collisions with the prolate-spheroid certificates.

## Required names

| Object | Canonical name |
|---|---|
| Axial stationary kernel | `g_axis_ob` |
| Pole endpoint value | `b_ob` |
| Lambda derivative of pole value | `b_ob_prime` |
| Axial derivative at the boundary | `gt_boundary_ob` |
| Oblate boundary-entry parameter | `lambda_entry_ob` |
| Oblate center-axis degeneracy | `lambda_axis_ob` |
| Linear boundary-entry coefficient | `entry_slope_ob` |

## Forbidden ambiguous names

Do not use the following as standalone file stems, function names, or JSON
keys:

```text
B
G
lambda_entry
lambda_partial
lambda_axis
boundary_entry
```

Every oblate-specific exported quantity must carry the `_ob` marker.

## Evidence labels

Use only the following status vocabulary:

- `DIAGNOSTIC_ONLY`
- `NOT_BINDING`
- `PROTOTYPE`
- `NOT_AUDITED`
- `CERTIFIED`

`CERTIFIED` is forbidden until the complete clean-room dependency chain and
independent audit are present.
