---
title: blackbox
category: Core Data Model
status: normative
---

# blackbox

A **blackbox** is a [[core-data-model/relation|Relation]] that functions like a
[[core-data-model/param|param]] for the purposes of dependency tracking — it may be
associated with the universal entity set or any constraint-defined subset and appears
as a declared input or output in rule bodies — but differs from a param in one
critical respect: **the Loci runtime is explicitly prohibited from inspecting,
synchronising, or manipulating the internal state of a blackbox value**.

A blackbox holds a per-process reference to an opaque data structure that manages its
own parallel state independently of Loci. It is the designated escape hatch for
integration with third-party numerical libraries (e.g., PETSc) that implement their
own communication and parallelisation strategies.

## Consequence

The [[principles/parallelism-transparency|Parallelism Transparency Principle]] does
**not** apply to blackbox values. The application developer accepts responsibility for
the correctness of its parallel state. Any communication of blackbox contents must be
performed explicitly within the rule kernels that operate on it.

---

*See also:* [[core-data-model/param|param]], [[core-data-model/relation|Relation]],
[[principles/parallelism-transparency|Parallelism Transparency]]
