---
title: FVM Module Overview
category: FVM Module
status: complete
attribution: llm
reviewed: false
---

# FVM Module Overview

The **`fvm` module** is a standard Loci module that provides reusable parametric
rules and derived facts for building finite-volume solvers on unstructured meshes.
It covers: mesh topology setup, grid metrics, spatial gradients, MUSCL face
extrapolation, nodal interpolation, surface integrations, L-norms, and a PETSc
linear solver interface.

## Loading the Module

The `fvm` module must be loaded into the `rule_db` before `makeQuery` is called:

```cpp
rule_db rdb ;
rdb.add_rules(global_rule_list) ;
Loci::load_module("fvm", rdb) ;
```

## Including the Type Declarations

In every `.loci` source file that references FVM variables, include the type
header using the Loci preprocessor directive:

```cpp
$include "FVM.lh"
```

This makes the parametric type names (`grads(X)`, `cell2node(X)`,
`petscScalarSolve(X)`, etc.) known to the `lpp` preprocessor and the runtime
type system.

## Canonical `main()` Sequence

```cpp
Loci::Init(&argc, &argv) ;

rule_db rdb ;
rdb.add_rules(global_rule_list) ;
Loci::load_module("fvm", rdb) ;

fact_db facts ;
facts.read_vars(varsFile, rdb) ;

if(!Loci::setupFVMGrid(facts, meshFile)) {
  cerr << "cannot read mesh" << endl ;
  Loci::Abort() ;
}
Loci::setupBoundaryConditions(facts) ;
Loci::createLowerUpper(facts) ;

Loci::makeQuery(facts, rdb, "solution") ;
Loci::Finalize() ;
```

## Module Pages

- [[fvm/mesh-topology|Mesh Topology]]
- [[fvm/grid-metrics|Grid Metrics]]
- [[fvm/gradients|Spatial Gradients]]
- [[fvm/muscl-extrapolation|MUSCL Extrapolation]]
- [[fvm/nodal-interpolation|Nodal Interpolation]]
- [[fvm/norms-integrations|Norms and Surface Integrations]]
- [[fvm/petsc-solvers|PETSc Linear Solvers]]

---

*See also:* [[program-lifecycle/load-module|Loci::load_module]],
[[program-lifecycle/fact-db|fact_db]],
[[program-lifecycle/make-query|Loci::makeQuery]]
