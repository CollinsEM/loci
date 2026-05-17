---
title: get_allocation
category: Program Lifecycle
status: normative
---

# get_allocation

**`get_allocation(n)`** is a method of [[program-lifecycle/fact-db|fact_db]] that
allocates `n` fresh [[core-data-model/entity|entity]] identifiers guaranteed to be
unique within the fact database. It returns an [[core-data-model/entity-set|EntitySet]]
containing exactly `n` entity labels that have not previously been allocated.

`get_allocation` is the normative mechanism for introducing new entities into the Loci
runtime. The fact database is the central authority over entity identity, and
`get_allocation` is the interface through which that authority is exercised. Application
developers must use `get_allocation` rather than assigning entity identifiers directly,
to guarantee uniqueness across all entities in the program.

## Example

```cpp
entitySet nodes = facts.get_allocation(N+1) ;
entitySet cells = facts.get_allocation(N) ;
```

---

*See also:* [[program-lifecycle/fact-db|fact_db]], [[core-data-model/entity|Entity]],
[[core-data-model/entity-set|EntitySet]]
