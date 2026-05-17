---
title: Relation
category: Core Data Model
status: complete
attribution: llm
reviewed: false
---

# Relation

A **Relation** is a typed mapping from an [[core-data-model/entity-set|EntitySet]]
(its *domain*) to values of a specified type (its *codomain*). Relations are the sole
mechanism through which all simulation state, mesh structure, parameters, and control
information are represented in Loci.

## Relation Types

| Type | Codomain | Primary use |
|------|----------|------------|
| `store<T>` | single value of type T | Per-entity field data |
| `storeVec<T>` | 1-D array of T | Block per-entity data |
| `storeMat<T>` | 2-D matrix of T | Per-entity Jacobians |
| `Map` | single entity | One-to-one topology |
| `MapVec` | fixed array of entities | Fixed-arity topology |
| `multiMap` | variable sequence of entities | One-to-many topology |
| `param<T>` | single value, process-replicated | Global parameters |
| `blackbox<T>` | opaque per-process value | Third-party library state |
| `constraint` | EntitySet value | Domain guards / assertions |

## Type Registration

Any type `T` used as the value type of a Loci relation must be registered with the
runtime via the [[core-data-model/data-schema-traits|data_schema_traits]] mechanism
so that the runtime can serialise and communicate values of that type.

## Formal Definition

A Relation $R$ over domain $D \subseteq U$ with codomain $T$ is a total function
$R : D \to T$.

---

*See also:* [[core-data-model/store|store]], [[core-data-model/param|param]],
[[core-data-model/map|Map]], [[core-data-model/constraint|constraint]],
[[core-data-model/data-schema-traits|data_schema_traits]]
