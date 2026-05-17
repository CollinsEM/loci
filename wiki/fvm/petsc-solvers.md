---
title: FVM PETSc Linear Solvers
category: FVM Module
status: complete
attribution: llm
reviewed: false
---

# FVM PETSc Linear Solvers

The `fvm` module exposes the PETSc sparse linear algebra toolkit through
three parametric rules. Each solver is keyed by a user-chosen name `X` that
ties together the matrix entries, right-hand side, and solution.

The PETSc interface is available only when Loci is compiled with `USE_PETSC`.

## Naming Convention

For a system named `X`, the application must provide four variables:

| Variable | Type (scalar) | Type (blocked) | Role |
|---|---|---|---|
| `X_B` | `store<real>` | `storeVec<real>` | Right-hand side (one value / block per cell) |
| `X_D` | `store<real>` | `storeMat<real_fj>` | Diagonal matrix entries |
| `X_L` | `store<real>` | `storeMat<real_fj>` | Lower off-diagonal entries (accessed via `lower`) |
| `X_U` | `store<real>` | `storeMat<real_fj>` | Upper off-diagonal entries (accessed via `upper`) |

`real_fj` is single-precision (`float`); the blocked solvers use mixed-precision
Jacobians (`storeMat<real_fj>`) with a double-precision solution.
`lower` and `upper` are the multiMaps installed by `createLowerUpper`.

## Solver Types

### `petscScalarSolve(X)` — Scalar Equation Solver

Solves one scalar equation per cell. `X_B`, `X_D`, `X_L`, `X_U` are all
`store<real>`.

```cpp
// Assemble diagonal
$rule unit(heat_D), constraint(geom_cells) {
  $heat_D = $vol / $deltaT ;
}
$rule apply(heat_D <- dqdotdQl)[Loci::Summation], constraint(geom_cells) {
  join($heat_D, $dqdotdQl) ;
}

// RHS: negative residual
$rule pointwise(heat_B <- qresidual) {
  $heat_B = -$qresidual ;
}

// Off-diagonal entries
$rule pointwise(heat_L <- dqdotdQl) { $heat_L = $dqdotdQl ; }
$rule pointwise(heat_U <- dqdotdQr) { $heat_U = -$dqdotdQr ; }

// Solve
$rule pointwise(deltaQ <- petscScalarSolve(heat)) {
  $deltaQ = $petscScalarSolve(heat) ;
}
```

### `petscBlockedSolve(X)` — Blocked Equation Solver (double-precision Jacobian)

Solves a block system per cell where the block size equals `X_B.vecSize()`.
`X_B` is `storeVec<real>`, `X_D`/`X_L`/`X_U` are `storeMat<real>` (n×n
square matrices — see [[core-data-model/store-mat|storeMat]]).

### `petscBlockedSSolve(X)` — Blocked Equation Solver (single-precision Jacobian)

Same interface as `petscBlockedSolve(X)` but with `storeMat<real_fj>` (single-
precision) Jacobian matrices. Reduces memory and bandwidth at some accuracy cost.

## `$type` Declarations

```cpp
// Scalar system example
$type heat_B store<real> ;
$type heat_D store<real> ;
$type heat_L store<real> ;
$type heat_U store<real> ;

// Blocked system example (n×n Jacobian blocks)
$type state_B storeVec<real> ;
$type state_D storeMat<real> ;
$type state_L storeMat<real> ;
$type state_U storeMat<real> ;
```

## Prerequisites

- `createLowerUpper(facts)` must be called before `makeQuery` so that the
  `lower` and `upper` multiMaps are available.
- The `fvm` module must be loaded via `Loci::load_module("fvm", rdb)`.
- PETSc must be initialised; Loci handles this internally during `Loci::Init`.

---

*See also:* [[fvm/mesh-topology|Mesh Topology (lower/upper maps)]],
[[core-data-model/store-mat|storeMat]],
[[core-data-model/store-vec|storeVec]]
