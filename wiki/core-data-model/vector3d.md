---
title: "vector3d<T>"
category: Core Data Model
status: complete
attribution: llm
reviewed: false
---

# vector3d\<T\>

**`vector3d<T>`** is a three-component mathematical vector with members `x`, `y`, `z`
of type `T`. It is a first-class Loci value type usable in any container and supports
full HDF5 I/O and MPI communication via a predefined `IDENTITY_CONVERTER`
[[core-data-model/data-schema-traits|data_schema_traits]] specialisation.

In FVM solvers `T` is almost always `double`, and the alias `vect3d` (defined as
`Loci::vector3d<double>`) is used throughout the FVM module.

## Declaration

```cpp
$type pos      store<vect3d> ;    // node position
$type velocity store<vect3d> ;    // cell velocity vector
```

## Construction

```cpp
vect3d zero(0.0, 0.0, 0.0) ;
vect3d v($u, $v, $w) ;           // from three scalars
vect3d copy = v ;                 // copy construction
```

## Member Access

```cpp
double px = $pos.x ;
double py = $pos.y ;
double pz = $pos.z ;

// Index form also supported (0→x, 1→y, 2→z)
double p0 = $pos[0] ;
```

## Arithmetic

| Expression | Result |
|---|---|
| `a + b` | component-wise sum |
| `a - b` | component-wise difference |
| `a * s`, `s * a` | scalar multiply |
| `a / s` | scalar divide |
| `-a` | negation |
| `a += b`, `a -= b`, `a *= s`, `a /= s` | in-place forms |

## Free Functions

```cpp
double   d = dot(v1, v2) ;     // dot product → scalar
vect3d   c = cross(v1, v2) ;   // cross product → vector
double   n = norm(v) ;         // Euclidean norm → scalar
```

`cross` also accepts a plain `T[3]` array as either argument.

## Example

```cpp
$rule pointwise(area <- face2node->pos) {
  vect3d pt = $face2node[0]->$pos ;
  vect3d sum(0, 0, 0) ;
  int fsz = $face2node.num_elems() ;
  for(int i=1; i<fsz-1; ++i)
    sum += cross($face2node[i]->$pos - pt,
                 $face2node[i+1]->$pos - pt) ;
  $area = 0.5 * sum ;
}
```

## tensor3d\<T\>

**`tensor3d<T>`** is the rank-2 companion: a `vector3d<vector3d<T>>` (a 3×3 matrix of
`T` values). It adds two free functions:

```cpp
vector3d<T> dot(const tensor3d<T> &t, const vector3d<T> &v) ;  // matrix-vector product
tensor3d<T> product(const tensor3d<T> &t1, const tensor3d<T> &t2) ; // matrix-matrix product
```

---

*See also:* [[core-data-model/vector2d|vector2d]], [[core-data-model/array|Array]],
[[core-data-model/store|store]], [[core-data-model/data-schema-traits|data_schema_traits]]
