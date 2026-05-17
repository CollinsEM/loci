---
title: storeVec
category: Core Data Model
status: complete
attribution: llm
reviewed: false
---

# storeVec

A **storeVec** is a [[core-data-model/relation|Relation]] in which each entity maps to
a one-dimensional array of `n` values of element type `T`. The array length `n` is
uniform across all entities in the domain and is set at runtime before any values are
written, using the `setVecSize()` method — typically called in a
[[rule-system/prelude-block|prelude block]].

## Distinction from `store<vect3d>`

A `storeVec<double>` of size 3 and a `store<vect3d>` are equivalent from a data layout
perspective — both store three `double` values per entity. The distinction is at the
type level: `vect3d` (an alias for `Loci::vector3d<double>`) provides operator
overloads for 3D vector algebra. `storeVec<double>` provides plain array access with
no mathematical semantics.

## Access Pattern

Within a rule kernel, `storeVec` values are accessed via array indexing:
`$varName[i]` accesses the i-th element for the current entity.

## Typical Uses

- Per-entity quadrature point data
- Per-entity polynomial coefficients in high-order methods
- Per-species arrays in multi-species flow solvers
- State vectors for ODE systems

## Scalar Broadcast: mk\_Scalar

Within a compute block, the per-entity vector view (`$varName`) supports assignment and
compound assignment from a `mk_Scalar(v)` expression, which broadcasts a single value
`v` to all `n` elements without an explicit loop:

```cpp
$Ivec = mk_Scalar(0.0) ;     // set all n elements to 0
$Ivec += mk_Scalar(1.0) ;    // add 1 to every element
$Ivec *= mk_Scalar(0.5) ;    // scale every element by 0.5
```

This is equivalent to `for(int i=0; i<$numBands; ++i) $Ivec[i] = 0.0 ;` but more
concise. `mk_Scalar` is provided by the Loci header and requires no additional include.

## Example

```cpp
$type Ivec storeVec<double> ;
$type numBands param<int> ;

$rule pointwise(Ivec{n=0} <- numBands), constraint(geom_cells),
prelude {
  $Ivec{n=0}.setVecSize(*$numBands) ;   // set array size (prelude: *$ required)
} compute {
  for(int i=0; i<$numBands; ++i)        // initialise each element
    $Ivec{n=0}[i] = 0 ;
}
```

---

*See also:* [[core-data-model/store|store]], [[core-data-model/store-mat|storeMat]],
[[rule-system/prelude-block|Prelude Block]], [[core-data-model/relation|Relation]]
