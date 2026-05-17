---
title: store
category: Core Data Model
status: complete
attribution: llm
reviewed: false
---

# store

A **store** is a [[core-data-model/relation|Relation]] whose codomain is a scalar or
structured value type `T`. Stores are the primary container for per-entity field data:
pressure, velocity, temperature, residuals, etc.

## Formal Definition

$R : D \to T$, where $T$ is a value type.

## Declaration Syntax

```cpp
$type store<vect3d> velocity ;   // 3D velocity field
$type store<double> pressure ;   // scalar pressure field
```

## Access in Rule Kernels

Within a rule kernel, the store value for the current entity is accessed as
`$storeName`. Values at adjacent entities are accessed via map chains:
`$mapName->$storeName`.

---

*See also:* [[core-data-model/store-vec|storeVec]], [[core-data-model/store-mat|storeMat]],
[[core-data-model/param|param]], [[core-data-model/relation|Relation]]
