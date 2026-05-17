---
title: param
category: Core Data Model
status: complete
attribution: llm
reviewed: false
---

# param

A **param** is a process-replicated, globally-consistent [[core-data-model/relation|Relation]]
whose domain is either the universal entity set or a named constraint-defined subset of
entities. Unlike a [[core-data-model/store|store]], a param holds a *single value per
process* — it does not vary per entity within its domain. Every process whose entity set
intersects the param's domain holds an identical, synchronised copy of the value.

The param is best understood by analogy to a *static class member*: every process
sharing the domain holds the same value, and any update is visible to all such processes
after synchronisation.

## Why Constrain a param to an Entity Subset?

A param constrained to `hex_cells` instantiates exactly one value per process per cell
type, shared across all hex cells. This is more efficient than a `store`, which would
replicate identical data at every entity. The constraint determines which processes
participate in owning and synchronising the param.

## Mutability

params are mutable, but only through the following four mechanisms, in order of
precedence at startup:

1. **[[rule-system/default-rule|default rule]]** — assigns an initial value; may be
   overridden by the `.vars` file.
2. **[[rule-system/optional-rule|optional rule]]** — reserves the variable; populated
   by the `.vars` file if present, otherwise the variable and all rules depending on it
   are pruned from the schedule.
3. **[[rule-system/singleton-rule|singleton rule]]** — computes a new param value from
   other param values during schedule execution.
4. **Reduction** ([[rule-system/unit-rule|unit]] + [[rule-system/apply-rule|apply]] rules)
   — accumulates per-entity contributions into a param value via an associative operator.

## Consistency Guarantee

The runtime guarantees that all copies of a param are fully synchronised across all
participating processes before any rule that depends on that param is permitted to
execute. This synchronisation is an explicit, scheduled step managed transparently by
the runtime.

## Access Syntax

| Context | Syntax | Notes |
|---------|--------|-------|
| `prelude` block | `*$paramName` | Dereference required; operates on the container |
| `compute` block | `$paramName` | Same as any other rule input variable |
| Iteration parameters (e.g., `$$n`) | `$$n` in compute; `*$$n` in prelude | Same rule applies |

The dereference operator `*` is **exclusive to the prelude block**. Within the compute
block, params are accessed identically to any other variable appearing in the rule
signature.

## Formal Definition

A param $P$ constrained to domain $D \subseteq U$ is a Relation $P : D \to T$ such
that $P$ takes a single value shared by all processes owning any entity $e \in D$.

---

*See also:* [[core-data-model/blackbox|blackbox]], [[core-data-model/store|store]],
[[core-data-model/constraint|constraint]], [[rule-system/prelude-block|Prelude Block]]
