---
title: FVM Periodic Boundary Conditions
category: FVM Module
status: complete
attribution: llm
reviewed: false
---

# FVM Periodic Boundary Conditions

The `fvm` module supports **periodic boundary conditions**, where matching faces on
opposite sides of a domain are treated as if they were connected. The module handles
both rotationally periodic (cyclic) and translationally periodic geometries.

## Topology Facts

`Loci::setupFVMGrid` populates the following periodic-specific facts:

| Fact | Type | Meaning |
|---|---|---|
| `pmap` | `Map` | Maps each periodic face to its partner face |
| `periodicTransform` | `store<Loci::rigid_transform>` | The rigid-body transformation from a periodic face to its partner |
| `periodicFaces` | `Constraint` | All faces participating in periodic BCs |

`pmap[f]` gives the partner face of face `f`. If `f` is a periodic face, `pmap[f]`
is the opposite face on the matched surface, and `periodicTransform[f]` describes
the rotation and/or translation that maps points on `f` to corresponding points on
`pmap[f]`.

## The `rigid_transform` Struct

`Loci::rigid_transform` (from `<LociGridReaders.h>`) represents a rigid-body
transformation: rotation about an axis followed by a translation. The transformation
maps a point `v` to `v' = R * (v + t1) + t2`.

| Member | Type | Meaning |
|---|---|---|
| `t1` | `vector3d<double>` | Pre-rotation translation (typically `−center`) |
| `t2` | `vector3d<double>` | Post-rotation translation (`center + translate`) |
| `R` | `tensor3d<double>` | Rotation matrix |
| `Rinv` | `tensor3d<double>` | Inverse rotation matrix |

### Methods

```cpp
// Apply the full rigid-body transform to a point
vector3d<T> p_prime = transform.transform(p) ;

// Apply only the rotation (no translation) — used for vector quantities
vector3d<T> v_prime = transform.rotate_vec(v) ;

// Apply the rotation to a tensor (e.g. stress tensor transformation)
tensor3d<T> S_prime = transform.rotate_tensor(S) ;
```

`rigid_transform` has a predefined `IDENTITY_CONVERTER`
[[core-data-model/data-schema-traits|data_schema_traits]] specialisation — it is
directly serialisable via HDF5 and MPI.

## `.vars` File Setup

Periodic boundary conditions are declared in the `boundary_conditions`
[[core-data-model/options-list|options_list]]. The VOG mesh file encodes which
faces are periodic and what the transformation parameters are; the `.vars` file
identifies the boundary name:

```
boundary_conditions: <
  BC_1=reflecting,
  BC_2=reflecting,
  periodic_left=periodic(name=periodic_right, rotation=45deg, axis=[0,0,1])
>
```

The exact syntax for periodic BC specification depends on the mesh generation tool
and solver. The `setupFVMGrid` function reads the pairing and transformation from
the VOG file directly; `boundary_conditions` only needs to label the boundary type
as `periodic`.

## Writing Rules for Periodic Faces

Rules that need values across periodic face pairs access the partner face via `pmap`:

```cpp
// Reconstruct face value using periodic partner
$rule pointwise(rho_f <- pmap->cl->rho, periodicTransform),
      constraint(periodicFaces) {
  // For periodic faces, right-side density comes from the partner's left cell
  $rho_f = $pmap->$cl->$rho ;
}
```

For vector quantities, the transformation must be applied to account for the
coordinate rotation between the two periodic surfaces:

```cpp
$rule pointwise(vel_f <- pmap->cl->vel, periodicTransform),
      constraint(periodicFaces) {
  // Rotate the velocity from the partner cell's frame into the current face's frame
  $vel_f = $periodicTransform.rotate_vec($pmap->$cl->$vel) ;
}
```

## Relationship to Ghost Cells

Periodic boundary faces are stored as boundary faces (with negative `cr`), but they
differ from wall boundaries in that their partner face's cell (`pmap->cl`) provides
the "ghost" cell data instead of a user-prescribed boundary value. The
`periodicFaces` constraint lets rules distinguish these faces from other boundary
types.

---

*See also:* [[fvm/mesh-topology|FVM Mesh Topology]],
[[fvm/vog-format|VOG Mesh File Format]],
[[distributed-execution/ghost-entity|Ghost Entity]],
[[core-data-model/options-list|options_list]]
