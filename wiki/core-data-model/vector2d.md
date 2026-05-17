---
title: "vector2d<T>"
category: Core Data Model
status: complete
attribution: llm
reviewed: false
---

# vector2d\<T\>

**`vector2d<T>`** is a two-component mathematical vector with members `x`, `y` of type
`T`. It is the 2-D analogue of [[core-data-model/vector3d|vector3d]] and shares the same
interface, with one important difference: the `cross` product of two 2-D vectors returns
a **scalar** (the z-component of the equivalent 3-D cross product) rather than a vector.

Like `vector3d`, it is a first-class Loci value type with a predefined
`IDENTITY_CONVERTER` [[core-data-model/data-schema-traits|data_schema_traits]]
specialisation.

## Construction

```cpp
vector2d<double> p(0.0, 0.0) ;
vector2d<double> q($u, $v) ;
vector2d<double> copy = q ;
```

## Member Access

```cpp
double vx = $vel2d.x ;
double vy = $vel2d.y ;

// Index form (0→x, 1→y)
double v0 = $vel2d[0] ;
```

## Arithmetic

Identical to [[core-data-model/vector3d|vector3d]]: component-wise `+`, `-`, scalar `*`
and `/`, in-place forms, and negation.

## Free Functions

```cpp
double d = dot(v1, v2) ;    // dot product → scalar
double c = cross(v1, v2) ;  // signed scalar (z-component of 3-D cross product)
double n = norm(v) ;         // Euclidean norm → scalar
```

`dot` and `cross` also accept a plain `T[2]` array as either argument.

---

*See also:* [[core-data-model/vector3d|vector3d]], [[core-data-model/array|Array]],
[[core-data-model/store|store]], [[core-data-model/data-schema-traits|data_schema_traits]]
