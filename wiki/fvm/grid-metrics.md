---
title: FVM Grid Metrics
category: FVM Module
status: complete
attribution: llm
reviewed: false
---

# FVM Grid Metrics

The `fvm` module computes the following geometric quantities from the mesh
topology facts. All are derived automatically by the scheduler; no user rules
are required.

## Per-Face Quantities

### `area` — `store<Loci::Area>`

The face area vector, stored as a struct with two members:

| Member | Type | Meaning |
|---|---|---|
| `area.n` | `vect3d` | Outward unit normal (pointing from `cl` to `cr`) |
| `area.sada` | `real` | Face area magnitude (√(A⃗·A⃗)) |

The face flux magnitude is typically `$area.sada * conductivity * dot(grad, $area.n)`.

### `facecenter` — `store<vect3d>`

Centroid of the face polygon.

### `mn`, `ln` — `store<vect3d>`

Two orthonormal vectors spanning the face plane, used internally for
non-orthogonal gradient corrections.

## Per-Cell Quantities

### `cellcenter` — `store<vect3d>`

Centroid of the cell. By default computed using the "wireframe" method (mass at
the cell surface); set `centroid: exact` in the `.vars` file for volumetric
mass-weighted centroids.

### `vol` — `store<real>`

Cell volume.

### `grid_vol` — `param<real>`

Total volume of the mesh (sum of all `vol` values over `geom_cells`).

## Coordinate Model

The `.vars` file parameter `gridCoordinates` selects the metric computation
model:

| Value | Meaning |
|---|---|
| `"cartesian"` (default) | Full 3-D Cartesian metrics |
| `"axisymmetric"` | 2-D axisymmetric; mesh must be a thin z-extrusion |

Setting `gridCoordinates: axisymmetric` activates axisymmetric volume and area
corrections. The module validates the extrusion thickness and aborts if the grid
is not consistent with an axisymmetric topology.

## Example

```cpp
// Heat flux through a face: q = k * (∇T · n̂) * |A|
$rule pointwise(qdot <- conductivity, grads_f(temperature), area) {
  $qdot = $area.sada * $conductivity * dot($grads_f(temperature), $area.n) ;
}
```

---

*See also:* [[fvm/mesh-topology|Mesh Topology]],
[[fvm/gradients|Spatial Gradients]],
[[core-data-model/vector3d|vector3d\<T\>]]
