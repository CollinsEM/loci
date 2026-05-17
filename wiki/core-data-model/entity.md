---
title: Entity
category: Core Data Model
status: normative
---

# Entity

An **Entity** is the fundamental unit of identity in a Loci application: an abstract,
opaque identifier representing a discrete element of the problem domain (mesh node,
face, cell, particle, etc.). Entities carry no intrinsic type or data. Identity is
conferred entirely by the [[core-data-model/relation|Relations]] (attributes and
connectivity) defined over them and by membership in named
[[core-data-model/entity-set|EntitySets]].

## Representation

Entities are represented as integers. An entity labeled by integer `n` is constructed
explicitly with `Entity(n)`. The valid range of entity labels is bounded by the
constants `Loci::UNIVERSE_MIN` and `Loci::UNIVERSE_MAX`.

```cpp
Entity e = Entity(10) ;   // entity labeled 10
```

While an entity's label may change during parallel execution (e.g., during load
redistribution), the application developer is unaware of this — label management is
handled transparently by the runtime.

## Formal Definition

The set of all possible entity identifiers forms the *Entity Universe* $U$. All
EntitySets and Relations are defined over subsets of $U$:

$$U = \{ i \in \mathbb{Z} \mid \texttt{UNIVERSE\_MIN} \le i \le \texttt{UNIVERSE\_MAX} \}$$

## Behavioural Guarantee

A conforming runtime must ensure that entity labels assigned through `get_allocation()`
are unique across the entire execution and that any label changes due to parallel
redistribution are invisible at the application level.

---

*See also:* [[core-data-model/entity-set|EntitySet]], [[core-data-model/relation|Relation]],
[[program-lifecycle/get-allocation|get_allocation]]
