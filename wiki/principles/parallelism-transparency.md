---
title: Parallelism Transparency Principle
category: Foundational Principles
status: normative
audience: both
---

# Parallelism Transparency Principle

A Loci program specifies only **data dependencies between rules**. All parallel
execution strategy — MPI communication, OpenMP threading, CUDA kernel dispatch,
memory layout, load balancing — is the sole responsibility of the runtime.

A conforming program produces **identical results** regardless of backend or
process count.

## Sole Exception

[[core-data-model/blackbox|blackbox]] is an explicit opt-out. A `blackbox`
variable is dependency-tracked like a [[core-data-model/param|param]] but its
internal state is opaque to the runtime. The runtime may not inspect, partition,
or communicate `blackbox` contents. This escape hatch exists for integration with
third-party libraries that manage their own parallel state.

## Implications for Application Developers

- Do not write `MPI_Send`, `MPI_Recv`, `#pragma omp`, or any parallel construct
  inside a rule kernel.
- Do not assume any particular execution order between rules beyond what the
  declared dependency graph requires.
- Do not assume any particular mapping of entities to processes.

---

*See also:* [[principles/separation-of-concerns|Separation of Concerns]],
[[core-data-model/blackbox|blackbox]]
