---
title: FVM Spatial Gradients
category: FVM Module
status: complete
attribution: llm
reviewed: false
---

# FVM Spatial Gradients

The `fvm` module provides parametric gradient operators for scalar and vector
fields, evaluated at cell centres and at faces.

## Cell-Centre Gradient Types

| Type | Container | Meaning |
|---|---|---|
| `grads(X)` | `store<vect3d>` | Gradient of scalar `X` at cell centres |
| `gradv(X)` | `storeVec<vect3d>` | Gradient of each component of general vector `X` |
| `gradv3d(X)` | `store<tensor3d>` | Full rank-2 gradient tensor of 3-D vector `X` |

`gradv(X)` is sized to match the `storeVec` width of `X` at runtime.
`gradv3d(X)` stores the 3×3 tensor as a `tensor3d<real>` value.

## Face Gradient Types

Face gradients blend the cell-centre gradient with the normal difference across
the face for improved accuracy on non-orthogonal meshes.

| Type | Container | Meaning |
|---|---|---|
| `grads_f(X)` | `store<vect3d>` | Gradient of scalar `X` at faces |
| `gradv_f(X)` | `storeVec<vect3d>` | Gradient of each component of general vector `X` at faces |
| `gradv3d_f(X)` | `store<tensor3d>` | Gradient tensor of 3-D vector `X` at faces |

The face gradient stencil is selected by the `.vars` file parameter
`faceGradStencil` (default `"limited"`; options: `"positive"`, `"centered"`,
`"nishikawa"`).

## Boundary Face Value Requirement

Cell-centre gradient operators reconstruct the gradient from a least-squares
stencil that includes both interior neighbours and boundary faces. To use
`grads(X)` on a variable `X`, the solver must supply **boundary face values**
of `X` at all relevant boundary faces, stored in a variable named `X_f`.

For vector variants: `gradv(X)` requires `X_f` as a `storeVec` at boundary
faces; `gradv3d(X)` requires `X_f` as a `store<vect3d>` at boundary faces.

### Example: Boundary Value Rules for `temperature`

```cpp
// Adiabatic wall: zero-gradient — copy cell temperature to face
$rule pointwise(temperature_f <- cl->temperature), constraint(adiabatic_BC) {
  $temperature_f = $cl->$temperature ;
}

// Specified-temperature wall: use the user-supplied value
$rule pointwise(temperature_f <- ref->Twall), constraint(specified_BC) {
  $temperature_f = $ref->$Twall ;
}
```

With `temperature_f` defined on all boundary faces, `grads(temperature)` and
`grads_f(temperature)` are fully determined.

## Example: Using a Face Gradient

```cpp
$rule pointwise(qdot <- conductivity, grads_f(temperature), area) {
  $qdot = $area.sada * $conductivity * dot($grads_f(temperature), $area.n) ;
}
```

## Gradient Method Selection

The cell-centre gradient algorithm is selected by the `.vars` parameter
`gradType` (default `"standard"`; options: `"iterative1"`, `"iterative2"`).
The number of iteration steps for iterative methods is `gradSteps`.

---

*See also:* [[fvm/grid-metrics|Grid Metrics]],
[[fvm/muscl-extrapolation|MUSCL Extrapolation]],
[[core-data-model/vector3d|vector3d\<T\>]]
