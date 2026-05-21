# Loci Framework Developer Reference

**Draft 0.7.0** · May 2026

Reference documentation for writing Loci applications. Covers the full
developer-facing surface: foundational principles, core data model, rule types,
scheduling model, program lifecycle, and standard modules (FVM). Pages use
`[[wikilinks]]` for cross-references and are compatible with Obsidian, Emacs
org-mode (via `pandoc`), and Sphinx/MyST.

---

## Design Principles

Loci is based on a data driven computation paradigm. This is paradigm
maps directly onto the typical problem solving approach of most
scientists and engineers:

1. Start with a set of facts that are already known or assumed to be
   true, and a query about some aspect of the system that needs to be
   derived.
2. Determine the domain over which a solution is to be obtained, and
   discretize the domain if necessary and establish the topological
   relationships of the discrete entities.
3. Assign realistic initial values to the quantities of interest on
   these discrete entities.
4. Compile a set of rules for transforming known quantities into
   unknown quantities based on established physical laws and/or numerical
   algorithms.
5. Use these rules and the topological relationships over the domain
   to establish a graph of dependent computations.
6. Given the query from the user for a particular value or set of
   values, create a schedule of calculations that will generate the
   requested information from the provided facts based on the initial
   assumptions.
7. Execute the computations in the most efficient manner possible over
   the provided computational units.
   
<!-- - [[principles/parallelism-transparency|Parallelism Transparency]] -->
<!-- - [[principles/static-schedule|Static Schedule]] -->
- [[principles/data-driven-computation|Data-Driven Computation]]
<!-- - [[principles/separation-of-concerns|Separation of Concerns]] -->

---

## Core Data Model

Entities, entity sets, and the container types that map entity sets to values.

<!-- - [[core-data-model/entity|Entity]] -->
<!-- - [[core-data-model/entity-set|EntitySet]] -->
<!-- - [[core-data-model/relation|Relation]] -->
<!-- - [[core-data-model/store|store]] -->
<!-- - [[core-data-model/store-vec|storeVec]] -->
<!-- - [[core-data-model/store-mat|storeMat]] -->
<!-- - [[core-data-model/map|Map]] -->
<!-- - [[core-data-model/map-vec|MapVec]] -->
<!-- - [[core-data-model/multi-map|multiMap]] -->
<!-- - [[core-data-model/param|param]] -->
<!-- - [[core-data-model/blackbox|blackbox]] -->
<!-- - [[core-data-model/constraint|constraint]] -->
<!-- - [[core-data-model/options-list|options_list]] -->
<!-- - [[core-data-model/data-schema-traits|data_schema_traits]] -->
<!-- - [[core-data-model/array|Array\<T,N\>]] -->
<!-- - [[core-data-model/vector3d|vector3d\<T\>]] -->
<!-- - [[core-data-model/vector2d|vector2d\<T\>]] -->

- Entity
- EntitySet
- Relation
- store
- storeVec
- storeMat
- Map
- MapVec
- multiMap
- param
- blackbox
- constraint
- options_list
- data_schema_traits
- Array\<T,N\>
- vector3d\<T\>
- vector2d\<T\>

---

## Rule System

The rule types and constructs that express computations in Loci.

<!-- - [[rule-system/rule|Rule]] -->
<!-- - [[rule-system/pointwise-rule|Pointwise Rule]] -->
<!-- - [[rule-system/singleton-rule|Singleton Rule]] -->
<!-- - [[rule-system/unit-rule|Unit Rule]] -->
<!-- - [[rule-system/apply-rule|Apply Rule]] -->
<!-- - [[rule-system/build-rule|Build Rule]] -->
<!-- - [[rule-system/advance-rule|Advance Rule]] -->
<!-- - [[rule-system/collapse-rule|Collapse Rule]] -->
<!-- - [[rule-system/default-rule|Default Rule]] -->
<!-- - [[rule-system/optional-rule|Optional Rule]] -->
<!-- - [[rule-system/constraint-rule|Constraint Rule]] -->
<!-- - [[rule-system/conditional|Conditional]] -->
<!-- - [[rule-system/parametric-rule|Parametric Rule]] -->
<!-- - [[rule-system/priority-specifier|Priority Specifier]] -->
<!-- - [[rule-system/output|OUTPUT]] -->
<!-- - [[rule-system/prelude-block|Prelude Block]] -->
<!-- - [[rule-system/iterative-loop|Iterative Loop]] -->

- Rule
- Pointwise Rule
- Singleton Rule
- Unit Rule
- Apply Rule
- Build Rule
- Advance Rule
- Collapse Rule
- Default Rule
- Optional Rule
- Constraint Rule
- Conditional
- Parametric Rule
- Priority Specifier
- OUTPUT
- Prelude Block
- Iterative Loop

---

## Scheduling and Execution Model

<!-- - [[scheduling/scheduler|Scheduler]] -->
<!-- - [[scheduling/dependency-graph|Dependency Graph]] -->
<!-- - [[scheduling/promote|promote]] -->
<!-- - [[scheduling/generalize|generalize]] -->

- Scheduler
- Dependency Graph
- promote
- generalize

---

## Distributed Execution

<!-- - [[distributed-execution/ghost-entity|Ghost Entity]] -->
<!-- - [[distributed-execution/halo-exchange|Halo Exchange]] -->

- Ghost Entity
- Halo Exchange

---

## Program Lifecycle

The programmatic interface that appears in an application's `main()`.

<!-- - [[program-lifecycle/init-finalize|Loci::Init / Loci::Finalize]] -->
<!-- - [[program-lifecycle/global-rule-list|global_rule_list]] -->
<!-- - [[program-lifecycle/rule-db|rule_db]] -->
<!-- - [[program-lifecycle/load-module|Loci::load_module]] -->
<!-- - [[program-lifecycle/fact-db|fact_db]] -->
<!-- - [[program-lifecycle/get-allocation|get_allocation]] -->
<!-- - [[program-lifecycle/vars-file|.vars File Format]] -->
<!-- - [[program-lifecycle/read-vars|read_vars]] -->
<!-- - [[program-lifecycle/make-query|Loci::makeQuery]] -->
<!-- - [[program-lifecycle/hdf5-io|HDF5 I/O]] -->
<!-- - [[program-lifecycle/debugging|Debugging]] -->

- `Loci::Init` / `Loci::Finalize`
- `global_rule_list`
- `rule_db`
- `Loci::load_module`
- `fact_db`
- `get_allocation`
- `.vars` File Format
- `read_vars`
- `Loci::makeQuery`
- HDF5 I/O
- Debugging

---

## Standard Modules

Reusable Loci modules that ship with the framework.

<!-- - [[fvm/index|FVM Module]] — finite-volume mesh setup, metrics, gradients, MUSCL, PETSc solvers -->

- `FVM` Module — finite-volume mesh setup, metrics, gradients, MUSCL, PETSc solvers

---

## Loci Source Language

Preprocessor syntax recognized by the `lpp` tool.

<!-- - [[source-language/lpp|lpp (Loci Preprocessor)]] -->
<!-- - [[source-language/dollar-type|$type]] -->
<!-- - [[source-language/dollar-include|$include]] -->
<!-- - [[source-language/dollar-rule|$rule syntax]] -->
<!-- - [[source-language/dollar-once|$[Once]]] -->
<!-- - [[source-language/comments|Comments]] -->
<!-- - [[source-language/debugout|Loci::debugout]] -->
<!-- - [[source-language/prelude-compute-split|Prelude / Compute Split]] -->
<!-- - [[source-language/style-guide|Coding Style Guide]] -->

- `lpp` (Loci Preprocessor)
- `$type`
- `$include`
- `$rule` syntax
- `$[Once]`
- Comments
- `Loci::debugout`
- Prelude / Compute Split
- Coding Style Guide

---

## Runtime Developer Guide

Reference for framework and runtime developers implementing the
Loci backend, preprocessor, and/or scheduler.

<!-- - [[runtime/index|Runtime Developer Guide Overview]] -->
<!-- - [[runtime/rule-class-interface|C++ Rule Class Interface]] -->
<!-- - [[runtime/rule-registration|Rule Registration Mechanism]] -->
<!-- - [[runtime/scheduler-algorithm|Scheduler Algorithm]] -->
<!-- - [[runtime/lpp-conformance|lpp Conformance Obligations]] -->

- Runtime Developer Guide Overview
- C++ Rule Class Interface
- Rule Registration Mechanism
- Scheduler Algorithm Overview

---

## Page Status

Each page carries frontmatter fields indicating its editorial state and content origin:

| Field | Values | Meaning |
|-------|--------|---------|
| `status` | `complete`, `draft`, `stub` | Editorial completeness |
| `audience` | `application`, `runtime`, `both` | Which audience the page targets |
| `attribution` | `human`, `llm`, `mixed` | Who produced the content |
| `reviewed` | `true`, `false` | Whether a subject matter expert has reviewed it |

Pages without an `audience` field are implicitly `application`-only. Pages marked
`both` are relevant to both application developers and runtime implementors.

