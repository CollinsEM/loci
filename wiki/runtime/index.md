---
title: Loci Runtime Specification
category: Runtime Specification
status: normative
audience: runtime
---

# Loci Runtime Specification

This section documents the obligations of a **conforming Loci runtime** — any
implementation of the Loci framework's preprocessor, scheduler, and parallel
execution backend. The normative reference implementation is `loci-4.1.2` (LGPLv3).

A conforming runtime must honour every behavioural guarantee stated in the
[[index|Application Developer Reference]] as observable from application code. The
pages in this section define *how* those guarantees must be implemented.

---

## Scope

The runtime specification covers:

- The **C++ rule class interface**: base classes, `name_store`, `input`, `output`
  registration, and the `calculate` / `compute` / `do_loop` execution structure
- The **rule registration mechanism**: how `$rule` declarations become globally
  registered C++ objects
- The **scheduler**: dependency graph construction, loop instantiation, promote /
  generalise insertion, and schedule linearisation
- The **preprocessor** (`lpp`): conformance obligations for source-to-source
  translation
- The **parallel execution model**: data distribution, ghost entity communication,
  halo exchange, and correctness guarantees

## Relationship to the Application Developer Reference

The Application Developer Reference defines the *observable behaviour* of Loci from
the application programmer's perspective. The runtime specification defines the
*mechanisms* that must produce that behaviour.

Concepts that appear in both documents:

- [[principles/parallelism-transparency|Parallelism Transparency]] — the invariant
  any conforming runtime must guarantee
- [[principles/static-schedule|Static Schedule]] — schedule construction timing
  requirements
- [[scheduling/scheduler|Scheduler]] — observable schedule construction sequence
- [[scheduling/promote|promote]] and [[scheduling/generalize|generalize]] — mandatory
  internal operations
- [[distributed-execution/ghost-entity|Ghost Entities]] and
  [[distributed-execution/halo-exchange|Halo Exchange]] — parallel communication obligations
- [[source-language/lpp|lpp]] — preprocessor interface and flag semantics

## Contents

- [[runtime/rule-class-interface|C++ Rule Class Interface]] — base classes and
  registration for each rule type
- [[runtime/rule-registration|Rule Registration Mechanism]] — `register_rule<T>`
  and the global rule list
- [[runtime/scheduler-algorithm|Scheduler Algorithm]] — dependency graph generation,
  iteration instantiation, volatile/static fact analysis
- [[runtime/lpp-conformance|lpp Conformance Obligations]] — what a conforming
  preprocessor must produce for each source construct
