# Loci Framework Specification — Wiki

**Loci Application Developer Reference** · Draft 0.7.0 · May 2026

Complete reference documentation for writing Loci applications. Covers the full
developer-facing surface: foundational principles, core data model, rule types,
scheduling model, program lifecycle, and standard modules (FVM). Pages use
`[[wikilinks]]` for cross-references and are compatible with Obsidian, Emacs
org-mode (via `pandoc`), and Sphinx/MyST.

---

## Foundational Principles

> These four principles are architectural commitments, not implementation choices.
> Every specification decision is evaluated against them.

- [[principles/parallelism-transparency|Parallelism Transparency]]
- [[principles/static-schedule|Static Schedule]]
- [[principles/data-driven-computation|Data-Driven Computation]]
- [[principles/separation-of-concerns|Separation of Concerns]]

---

## Core Data Model

Entities, entity sets, and the container types that map entity sets to values.

- [[core-data-model/entity|Entity]]
- [[core-data-model/entity-set|EntitySet]]
- [[core-data-model/relation|Relation]]
- [[core-data-model/store|store]]
- [[core-data-model/store-vec|storeVec]]
- [[core-data-model/store-mat|storeMat]]
- [[core-data-model/map|Map]]
- [[core-data-model/map-vec|MapVec]]
- [[core-data-model/multi-map|multiMap]]
- [[core-data-model/param|param]]
- [[core-data-model/blackbox|blackbox]]
- [[core-data-model/constraint|constraint]]
- [[core-data-model/options-list|options_list]]
- [[core-data-model/data-schema-traits|data_schema_traits]]
- [[core-data-model/array|Array\<T,N\>]]
- [[core-data-model/vector3d|vector3d\<T\>]]
- [[core-data-model/vector2d|vector2d\<T\>]]

---

## Rule System

The rule types and constructs that express computations in Loci.

- [[rule-system/rule|Rule]]
- [[rule-system/pointwise-rule|Pointwise Rule]]
- [[rule-system/singleton-rule|Singleton Rule]]
- [[rule-system/unit-rule|Unit Rule]]
- [[rule-system/apply-rule|Apply Rule]]
- [[rule-system/build-rule|Build Rule]]
- [[rule-system/advance-rule|Advance Rule]]
- [[rule-system/collapse-rule|Collapse Rule]]
- [[rule-system/default-rule|Default Rule]]
- [[rule-system/optional-rule|Optional Rule]]
- [[rule-system/constraint-rule|Constraint Rule]]
- [[rule-system/conditional|Conditional]]
- [[rule-system/parametric-rule|Parametric Rule]]
- [[rule-system/priority-specifier|Priority Specifier]]
- [[rule-system/output|OUTPUT]]
- [[rule-system/prelude-block|Prelude Block]]
- [[rule-system/iterative-loop|Iterative Loop]]

---

## Scheduling and Execution Model

- [[scheduling/scheduler|Scheduler]]
- [[scheduling/dependency-graph|Dependency Graph]]
- [[scheduling/promote|promote]]
- [[scheduling/generalize|generalize]]

---

## Distributed Execution

- [[distributed-execution/ghost-entity|Ghost Entity]]
- [[distributed-execution/halo-exchange|Halo Exchange]]

---

## Program Lifecycle

The programmatic interface that appears in an application's `main()`.

- [[program-lifecycle/init-finalize|Loci::Init / Loci::Finalize]]
- [[program-lifecycle/global-rule-list|global_rule_list]]
- [[program-lifecycle/rule-db|rule_db]]
- [[program-lifecycle/load-module|Loci::load_module]]
- [[program-lifecycle/fact-db|fact_db]]
- [[program-lifecycle/get-allocation|get_allocation]]
- [[program-lifecycle/vars-file|.vars File Format]]
- [[program-lifecycle/read-vars|read_vars]]
- [[program-lifecycle/make-query|Loci::makeQuery]]
- [[program-lifecycle/hdf5-io|HDF5 I/O]]
- [[program-lifecycle/debugging|Debugging]]

---

## Standard Modules

Reusable Loci modules that ship with the framework.

- [[fvm/index|FVM Module]] — finite-volume mesh setup, metrics, gradients, MUSCL, PETSc solvers

---

## Loci Source Language

Preprocessor syntax recognized by the `lpp` tool.

- [[source-language/lpp|lpp (Loci Preprocessor)]]
- [[source-language/dollar-type|$type]]
- [[source-language/dollar-include|$include]]
- [[source-language/dollar-rule|$rule syntax]]
- [[source-language/dollar-once|$[Once]]]
- [[source-language/comments|Comments]]
- [[source-language/debugout|Loci::debugout]]
- [[source-language/prelude-compute-split|Prelude / Compute Split]]
- [[source-language/style-guide|Coding Style Guide]]

---

## Runtime Specification

Reference for framework and runtime developers implementing a conforming Loci backend,
preprocessor, or scheduler.

- [[runtime/index|Runtime Specification Overview]]
- [[runtime/rule-class-interface|C++ Rule Class Interface]]
- [[runtime/rule-registration|Rule Registration Mechanism]]
- [[runtime/scheduler-algorithm|Scheduler Algorithm]]
- [[runtime/lpp-conformance|lpp Conformance Obligations]]

---

## Document Status

Each page carries two frontmatter fields:

| Field | Values | Meaning |
|-------|--------|---------|
| `status` | `normative`, `draft`, `stub` | Editorial completeness |
| `audience` | `application`, `runtime`, `both` | Which document the page belongs to |

Pages without an `audience` field are implicitly `application`-only. Pages marked
`both` appear in both the Application Developer Reference and the Runtime
Specification.

