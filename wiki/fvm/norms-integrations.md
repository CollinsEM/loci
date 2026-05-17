---
title: FVM Norms and Surface Integrations
category: FVM Module
status: normative
---

# FVM Norms and Surface Integrations

## Scalar Norms

The `fvm` module provides three volume-weighted scalar norms over `geom_cells`.
All are `param<real>` — global reductions to a single scalar value.

| Type | Formula | Meaning |
|---|---|---|
| `L2Norm(X)` | √(Σ X² · vol) / √(Σ vol) | Volume-weighted L-2 norm |
| `L1Norm(X)` | Σ |X| · vol / Σ vol | Volume-weighted L-1 norm |
| `LinfNorm(X)` | max |X| | L-∞ norm (global maximum) |

These are the standard tool for monitoring residual convergence. The `L2Norm`
is the most common choice for steady-state solvers.

### Example — Residual Monitor

```cpp
$rule singleton(OUTPUT <- L2Norm(qresidual), $n),
  option(disable_threading) {
  if(Loci::MPI_rank == 0)
    cout << "R" << *$$n << ": " << $L2Norm(qresidual) << endl ;
}
```

`option(disable_threading)` prevents duplicate output in multi-threaded builds.
The `MPI_rank == 0` guard prevents duplicate output across MPI ranks.

## Surface Integration Types

The `fvm` module can integrate a quantity over the boundary faces surrounding
each cell.

| Type | Container | Meaning |
|---|---|---|
| `integrateSurface(X)` | `store<real>` | Integral of scalar `X` over the bounding faces of each cell |
| `integrateFlux(X)` | `store<real>` | Integral of vector `X` dotted with the face outward normals over each cell's boundary |

These are less commonly used than the residual norms; they arise in high-order
schemes and in verification diagnostics.

---

*See also:* [[fvm/grid-metrics|Grid Metrics]],
[[fvm/gradients|Spatial Gradients]],
[[rule-system/output|OUTPUT]]
