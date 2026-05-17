---
title: Ghost Entity
category: Distributed Execution
status: complete
audience: both
attribution: llm
reviewed: false
---

# Ghost Entity

A **ghost entity** (also called a *halo entity*) is a read-only copy of an entity
owned by a neighbouring partition, held locally on the current process to satisfy data
dependencies of rules that operate at partition boundaries. Ghost entity values are
populated by the runtime during [[distributed-execution/halo-exchange|halo exchange]]
steps, transparently to the application developer.

Ghost entities support the [[principles/parallelism-transparency|Parallelism
Transparency Principle]]: the application developer writes rules that access adjacent
entities via map chains without any awareness of whether those entities are local or
remote.

---

*See also:* [[distributed-execution/halo-exchange|Halo Exchange]]
