---
title: FVM Module
category: FVM Module
status: complete
attribution: llm
reviewed: false
---

# FVM Module

The **`fvm` module** provides reusable parametric rules and derived facts for
building finite-volume solvers on unstructured meshes. Load it with
`Loci::load_module("fvm", rdb)` and include `$include "FVM.lh"` in each
`.loci` source file that references its types.

---

- [[fvm/overview|Overview]] — loading, `$include "FVM.lh"`, canonical `main()` sequence
- [[fvm/vog-format|VOG Mesh File Format]] — HDF5 structure, face orientation convention, cluster encoding
- [[fvm/mesh-topology|Mesh Topology]] — facts from `setupFVMGrid`, boundary-condition naming, `lower`/`upper` maps
- [[fvm/grid-metrics|Grid Metrics]] — `area` (`.n`/`.sada`), `vol`, `cellcenter`, `facecenter`, `grid_vol`
- [[fvm/gradients|Spatial Gradients]] — `grads`/`gradv`/`gradv3d`, face variants, `X_f` boundary requirement
- [[fvm/muscl-extrapolation|MUSCL Extrapolation]] — `limiters`, `lefts`/`rights` and variants
- [[fvm/nodal-interpolation|Nodal Interpolation]] — `cell2node` family, plot-file pattern
- [[fvm/norms-integrations|Norms and Surface Integrations]] — `L2Norm`, `L1Norm`, `LinfNorm`, `integrateSurface`, `integrateFlux`
- [[fvm/petsc-solvers|PETSc Linear Solvers]] — `petscScalarSolve`, `petscBlockedSolve`, `X_B`/`X_D`/`X_L`/`X_U` convention
- [[fvm/periodic-bc|Periodic Boundary Conditions]] — `pmap`, `periodicTransform`, `rigid_transform`
