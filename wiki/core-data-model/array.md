---
title: "Array<T,N>"
category: Core Data Model
status: normative
---

# Array\<T,N\>

**`Array<T,N>`** is a fixed-size, compile-time array of `N` elements of type `T`. It is
a first-class Loci value type: it may be used directly as the element type of any
container (`store<Array<double,3>>`, `storeVec<Array<double,3>>`, etc.) and supports
full HDF5 I/O and MPI communication via a predefined `IDENTITY_CONVERTER`
[[core-data-model/data-schema-traits|data_schema_traits]] specialisation.

Unlike `std::array`, `Array<T,N>` provides element-wise arithmetic operators and a full
set of mathematical functions that operate component-wise via expression templates.

## Declaration

```cpp
$type coords store<Array<double,3>> ;   // 3 doubles per entity
```

## Construction

```cpp
Array<double,3> a ;             // default-constructed (elements uninitialised)
Array<double,3> b(0.0) ;        // all elements initialised to 0.0 (explicit)
```

## Access

```cpp
a[0] = 1.0 ;    // assignment via index
double v = a[2] ; // read via index (0-indexed, i < N)
```

The `begin()` / `end()` iterator interface is also provided, enabling use in standard
library algorithms.

## Arithmetic

All arithmetic operators are element-wise:

| Expression | Result |
|---|---|
| `a + b` | element-wise sum |
| `a - b` | element-wise difference |
| `a * b` | element-wise product |
| `a / b` | element-wise quotient |
| `a * s`, `s * a` | scalar multiply |
| `a / s` | scalar divide |
| `-a` | negation |
| `a += b`, `a -= b`, `a *= b`, `a /= b` | in-place forms |

Element-wise versions of `cos`, `sin`, `sqrt`, `exp`, `log`, `abs`, `min`, `max`, and
related math functions are also available.

## Example

```cpp
$type cellCoords store<Array<double,3>> ;
$type nodeCoords store<Array<double,3>> ;

$rule pointwise(cellCoords <- face2node->nodeCoords),
      constraint(geom_cells) {
  Array<double,3> sum(0.0) ;
  int n = 0 ;
  for(int i=0; i<$face2node.size(); ++i, ++n)
    sum += $face2node[i]->$nodeCoords ;
  $cellCoords = sum / double(n) ;
}
```

## Relationship to MapVec

[[core-data-model/map-vec|MapVec]]`<M>` stores its entity-to-entity mapping as
`Array<int,M>` internally — `Array` is its underlying storage primitive.

---

*See also:* [[core-data-model/store|store]], [[core-data-model/store-vec|storeVec]],
[[core-data-model/map-vec|MapVec]], [[core-data-model/vector3d|vector3d]],
[[core-data-model/data-schema-traits|data_schema_traits]]
