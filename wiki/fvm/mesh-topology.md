---
title: FVM Mesh Topology
category: FVM Module
status: normative
---

# FVM Mesh Topology

After `Loci::setupFVMGrid(facts, meshFile)` returns, the following facts are
installed in the fact database. These describe the unstructured mesh connectivity
and are the foundation for all subsequent metric and gradient computations.

## Primary Topology Facts

| Fact | Type | Domain | Description |
|---|---|---|---|
| `pos` | `store<vect3d>` | nodes | 3-D node positions |
| `face2node` | `multiMap` | faces | Nodes forming each face, right-hand-rule ordered |
| `cl` | `Map` | faces | Cell to the **left** of each face |
| `cr` | `Map` | faces | Cell to the **right** of each face |
| `ci` | `Map` | boundary faces | The one adjacent cell for boundary faces |
| `ref` | `Map` | boundary faces | Reference surface entity for the boundary |
| `pmap` | `Map` | periodic faces | Maps a periodic face to its partner |
| `geom_cells` | `constraint` | — | All physical (geometric) cells, excluding ghosts |
| `cells` | `constraint` | — | All cells including ghost cells at boundaries |
| `boundary_faces` | `constraint` | — | All boundary faces |
| `periodicFaces` | `constraint` | — | All faces participating in periodic BCs |

## Face Orientation

`face2node` nodes are ordered so that the right-hand-rule normal points **away
from the left cell and into the right cell**. For boundary faces the normal
points outward (out of the domain), so `cl` is always the physical cell and
`cr` is the ghost. The coloring invariant guarantees that following any sequence
of faces from left to right never cycles — this underpins the triangular
structure of the matrix assembler.

## Boundary Condition Facts

`Loci::setupBoundaryConditions(facts)` reads the `boundary_conditions`
`options_list` from the fact database (set by the `.vars` file) and creates:

- **`<bcname>_BC` constraints** — one per distinct boundary-condition name,
  containing all faces assigned to that condition. For example, `adiabatic_BC`
  and `specified_BC`.
- **`<optname>_BCoption` constraints** — one per sub-option key (e.g.
  `Twall_BCoption`), containing the surface entities where that option was given.
- **`BC_options` `store<options_list>`** — stores the full options list per
  surface entity; access numeric values via `getOptionUnits`.

### Extracting a Boundary Option

```cpp
// Extract Twall from boundary condition options
$rule pointwise(Twall <- BC_options), constraint(Twall_BCoption) {
  $BC_options.getOptionUnits("Twall", "kelvin", $Twall) ;
}
```

### Using a Boundary Constraint

```cpp
$rule pointwise(temperature_f <- ref->Twall), constraint(specified_BC) {
  $temperature_f = $ref->$Twall ;
}
```

## Matrix Connectivity Facts

`Loci::createLowerUpper(facts)` installs:

| Fact | Type | Description |
|---|---|---|
| `upper` | `multiMap` | Faces where the current cell is `cl` (upper-triangular entries) |
| `lower` | `multiMap` | Faces where the current cell is `cr` (lower-triangular entries) |
| `boundary_map` | `multiMap` | Boundary faces adjacent to each cell |

These are required by the PETSc solver interface and by many FVM module utilities.
Call `createLowerUpper` before `makeQuery` whenever the `fvm` module is used.

---

*See also:* [[fvm/overview|FVM Module Overview]],
[[fvm/grid-metrics|Grid Metrics]],
[[program-lifecycle/vars-file|.vars File Format]],
[[core-data-model/multi-map|multiMap]]
