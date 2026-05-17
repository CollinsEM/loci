---
title: Prelude Block
category: Rule System
status: normative
---

# Prelude Block

A **prelude block** is an optional section of a rule, introduced by the `prelude`
keyword, that operates on *containers* rather than on *values*. The prelude block is
executed before the `compute` block and before the kernel is invoked over individual
entities.

## Primary Uses

- Calling `setVecSize()` on [[core-data-model/store-vec|storeVec]] or
  [[core-data-model/store-mat|storeMat]] outputs to set their per-entity array
  dimensions before values are written.
- Performing file I/O operations that act on entire containers (e.g., writing an HDF5
  file), where the `$var.Rep()` container representation is required rather than
  individual entity values.

## Param Access Syntax

Within a prelude block, accessing a [[core-data-model/param|param]] variable requires
the `*$paramName` dereference syntax. This syntax is **exclusive** to the prelude
block; within the `compute` block, params are accessed as `$paramName` like any other
variable in the rule signature.

## Example

```cpp
$rule pointwise(Ivec{n=0} <- numBands),
      constraint(geom_cells),
prelude {
  // Container-level: set array size
  $Ivec{n=0}.setVecSize(*$numBands) ;   // *$ required in prelude
} compute {
  // Value-level: initialise each element
  for(int i=0; i<$numBands; ++i)        // no * in compute
    $Ivec{n=0}[i] = 0.0 ;
}
```

## Behavioural Guarantee

A conforming runtime must execute the prelude block exactly once per rule invocation,
before any per-entity execution of the compute block. The prelude block must complete
on all processes before the compute block begins execution.

---

*See also:* [[core-data-model/store-vec|storeVec]], [[core-data-model/store-mat|storeMat]],
[[source-language/prelude-compute-split|Prelude / Compute Split]],
[[core-data-model/param|param]]
