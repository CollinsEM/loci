---
title: FVM MUSCL Extrapolation
category: FVM Module
status: normative
---

# FVM MUSCL Extrapolation

The `fvm` module provides MUSCL (Monotone Upstream-centred Scheme for
Conservation Laws) face-value extrapolation. The scheme extrapolates a
cell-centred quantity to both sides of each face using the cell-centre
gradient, limited by a monotone limiter.

## Limiter Types

Limiters suppress spurious oscillations near discontinuities by bounding
the gradient-based extrapolation.

| Type | Container | Meaning |
|---|---|---|
| `limiters(X)` | `store<real>` | Scalar limiter for scalar `X` |
| `limiterv(X)` | `storeVec<real>` | Per-component limiter for general vector `X` |
| `limiterv3d(X)` | `store<vect3d>` | Per-component limiter for 3-D vector `X` |

Limiters are computed automatically from the cell-centre gradient and the
neighbouring cell values; no user rules are needed.

## Face Extrapolation Types

### Scalar extrapolation

| Type | Container | Description |
|---|---|---|
| `lefts(X)` | `store<real>` | Scalar `X` extrapolated to the left side of each face |
| `rights(X)` | `store<real>` | Scalar `X` extrapolated to the right side of each face |
| `leftsP(X,M)` | `store<real>` | Left extrapolation, floor-limited to minimum `M` (positive-preserving) |
| `rightsP(X,M)` | `store<real>` | Right extrapolation, floor-limited to minimum `M` |

### 3-D vector extrapolation

| Type | Container | Description |
|---|---|---|
| `leftv3d(X)` | `store<vect3d>` | 3-D vector `X` extrapolated to the left side |
| `rightv3d(X)` | `store<vect3d>` | 3-D vector `X` extrapolated to the right side |

### General vector extrapolation

| Type | Container | Description |
|---|---|---|
| `leftvM(X)` | `storeVec<real>` | General vector `X` extrapolated to the left side |
| `rightvM(X)` | `storeVec<real>` | General vector `X` extrapolated to the right side |

## Extrapolation Formula

For scalar `X` at a face, the extrapolation is:

```
lefts(X)  = cl->X + cl->limiters(X) * dot(cl->grads(X), facecenter - cl->cellcenter)
rights(X) = cr->X + cr->limiters(X) * dot(cr->grads(X), facecenter - cr->cellcenter)
```

The `leftsP`/`rightsP` variants clamp the result to be ≥ M (useful for
positive-definite quantities such as pressure or density).

## Dependencies

Using `lefts(X)` / `rights(X)` requires that the following are computable for
`X`:
- `grads(X)` (cell-centre gradient) — which in turn requires `X_f` at boundary
  faces (see [[fvm/gradients|Spatial Gradients]])
- `limiters(X)` (monotone limiter)
- `cellcenter` (computed automatically by the `fvm` module)

## Example: Roe Flux with MUSCL Reconstruction

```cpp
$rule pointwise(rho_left, rho_right <- lefts(rho), rights(rho)) {
  $rho_left  = $lefts(rho) ;
  $rho_right = $rights(rho) ;
}
```

---

*See also:* [[fvm/gradients|Spatial Gradients]],
[[fvm/grid-metrics|Grid Metrics]]
