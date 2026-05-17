---
title: Prelude / Compute Split
category: Loci Source Language
status: normative
---

# Prelude / Compute Split

A rule kernel may be divided into two named blocks with distinct operational scopes:

## prelude `{ }`

Operates on *containers* rather than individual entity values. Executed **once** for
the entire rule invocation, before the per-entity loop begins. Used for operations that
configure containers prior to value computation:

- Setting array dimensions on [[core-data-model/store-vec|storeVec]] or
  [[core-data-model/store-mat|storeMat]] outputs via `setVecSize()`.
- Performing file I/O on whole containers.

[[core-data-model/param|Param]] values are accessed via `*$paramName` within a prelude
block.

## compute `{ }`

Operates on *values*, applied **once per entity** in the rule's execution domain. This
is the standard kernel body. Param values are accessed as `$paramName` — no dereference
needed.

When both blocks are present, the prelude executes first, then the compute block is
applied over the entity sequence. When only a single brace-delimited body is provided
(the common case), it is treated as the `compute` block.

## Example

```cpp
$rule pointwise(Ivec{n=0} <- numBands),
      constraint(geom_cells),
prelude {
  $Ivec{n=0}.setVecSize(*$numBands) ;   // container-level; *$ required
} compute {
  for(int i=0; i<$numBands; ++i)        // value-level; no *
    $Ivec{n=0}[i] = 0.0 ;
}
```

## Behavioural Guarantee

A conforming runtime must execute the prelude block exactly once per rule invocation,
before any per-entity execution of the compute block. The prelude block must complete
on all processes before the compute block begins execution.

---

*See also:* [[rule-system/prelude-block|Prelude Block]],
[[core-data-model/store-vec|storeVec]], [[core-data-model/param|param]]
