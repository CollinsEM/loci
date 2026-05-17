---
title: storeMat
category: Core Data Model
status: normative
---

# storeMat

A **storeMat** is a [[core-data-model/relation|Relation]] in which each entity maps to a
two-dimensional **square** matrix of values of element type `T`. The matrix dimension `n`
is uniform across all entities in the domain and is set at runtime via `setVecSize(n)`,
which allocates `n×n` elements per entity. `setVecSize` must be called before any values
are written, typically in a [[rule-system/prelude-block|prelude block]].

Data is stored internally as a flat per-entity array of `n*n` elements. A `Mat<T>`
flyweight object constructed from each entity's data block provides 2-D accessor
semantics: `A[r]` returns a row proxy, and `A[r][c]` accesses the element at row `r`,
column `c` (both 0-indexed).

## Declaration

```cpp
$type X_D storeMat<real> ;
```

## Dimension

`setVecSize(int n)` sets both the row count and the column count to `n` (square matrices
only). `vecSize()` returns `n`.

## Kernel Access Syntax

```cpp
$matName[r][c]   // element at row r, column c for the current entity
```

## Example

```cpp
$type jacobian storeMat<real> ;
$type numDof    param<int> ;

$rule pointwise(jacobian <- numDof), constraint(geom_cells),
prelude {
  $jacobian.setVecSize(*$numDof) ;   // allocates numDof×numDof per entity
} compute {
  for(int i=0; i<$numDof; ++i)
    for(int j=0; j<$numDof; ++j)
      $jacobian[i][j] = 0 ;
}
```

## Primary Use Case

Per-entity Jacobian matrices whose dimension is determined at runtime, typically paired
with a [[core-data-model/store-vec|storeVec]] holding the corresponding state or residual
vector. Also used for the diagonal, lower, and upper block matrices in the PETSc blocked
linear solver (`X_D`, `X_L`, `X_U`).

---

*See also:* [[core-data-model/store-vec|storeVec]], [[core-data-model/store|store]],
[[rule-system/prelude-block|Prelude Block]], [[core-data-model/relation|Relation]]
