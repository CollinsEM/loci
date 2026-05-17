---
title: Scheduler Algorithm
category: Runtime Specification
status: normative
audience: runtime
---

# Scheduler Algorithm

The Loci scheduler constructs an execution schedule by **recursive backward search**
through the rule database. Starting from the user-queried variable, it traces
dependencies backward until all required existential facts are accounted for. The
schedule is built once at `makeQuery` time and is static for the lifetime of that
query.

## Overview

Schedule construction proceeds in three phases:

1. **Rule database classification** — iteration-related rules (build, advance,
   collapse) are identified and grouped into `iterating_rule` placeholders. Remaining
   rules form a directed `rule_graph`.
2. **Backward search** (`Create-Graph`) — starting from the queried variable, the
   scheduler traces the `rule_graph` in reverse, instantiating iterations recursively
   as they are encountered.
3. **Schedule linearisation** — the resulting dependency graph is topologically
   sorted; communicate / compute / reduce sequences are generated for each parallel
   step.

## Iteration Hierarchy

Iterations are recognised by the build/advance/collapse rule pattern and organised
into a **time-level hierarchy**. Each iteration has a unique time identity
(`{n}`, `{n,it}`, `{n,it,igs}`, …). The stationary time (non-iterated rules) is the
root; nested loops are children.

The backward search is mutually recursive over three procedures:

| Procedure | Role |
|-----------|------|
| `Create-Graph(rg, sr, tlevel, dg)` | Backward search for a given time level; calls `Instantiate-Iter` when an `iterating_rule` is reached |
| `Instantiate-Iter(rg, r)` | Builds the dependency graph for iteration `r`; calls `Init-Iter` then `Create-Graph` for the iteration's time level |
| `Init-Iter(rg, tlevel)` | Initialises the iteration graph: inserts generalize rules, computes volatile facts, adds build/advance/collapse rules |

## Volatile vs. Static Facts

A **volatile fact** is one whose value changes during an iteration. A **static fact**
is one that remains constant across iterations. The distinction determines which
promotion mechanism applies:

| Fact class | Promotion mechanism |
|---|---|
| Volatile | **Rule promotion** — stationary rules are stamped with the time level `{n}` and added to the iteration graph |
| Static | **Fact promotion** — a `promote` edge asserts equivalence with the parent-level version (`A{n} ← A`) |

Volatile facts are identified by forward search from the iteration's initially-known
volatile set (build-rule outputs, advance-rule outputs, and the loop counter `$$n`).
Any fact reachable by forward traversal through the `rule_graph` from a volatile seed
is itself volatile.

## Promote and Generalize Insertion

Two internal rule types are inserted automatically:

**promote** — inserted for every iteration-static fact that must be made available
inside a loop. Records the equivalence `A{n} ≡ A` (or `A{n,it} ≡ A{n}` for nested
levels). The application developer never writes or sees these edges.

**generalize** — inserted once per iteration to unify the build-rule output
(`Q{n=0}`) with the loop variable (`Q{n}`) for the first iteration. After iteration 1,
`Q{n}` takes the value computed by the advance rule for `Q{n+1}`.

A conforming scheduler must insert both operations automatically and must never
require the application developer to express them explicitly.

## OUTPUT Handling

`OUTPUT` is a reserved fact that activates side-effectful operations (file I/O,
screen writes) inside an iteration. A conforming scheduler must:

- Create an `OUTPUT{n}` fact for each iteration level.
- Attach it to the internal looping rule for that iteration so that it remains in
  the advance subgraph.
- Check whether `OUTPUT{n}` is volatile (i.e., any user rule targets it). If so,
  add it to the iteration's search requests.

Rules targeting `OUTPUT` execute unconditionally every advance step unless guarded
by a [[rule-system/conditional|conditional]] variable.

## Parallel Schedule Generation

After the dependency graph is built, the scheduler generates communication steps:

1. **Barrier analysis** — for each variable crossing a process boundary, the
   scheduler inserts pre-communication (send/receive) operations.
2. **Chomp** — memory-reclamation passes that release container storage once its
   last consumer has executed. Disabled by `--nochomp`.
3. **Thread assignment** — rules with `option(disable_threading)` are routed to the
   single-threaded path; remaining rules may be distributed across OpenMP threads or
   CUDA kernels.

The output is a linearised sequence of `rule_compilerP` objects consumed by the
execution engine.

## Conformance Requirements

- The scheduler must produce identical observable results regardless of MPI process
  count, thread count, or execution order of independent rules.
- Schedule construction must complete before any rule `calculate` or `compute` method
  is called.
- A schedule built for a given `(rdb, facts, query)` triple must not be reused for
  a different triple. Each `makeQuery` call constructs a fresh schedule.

---

*See also:* [[scheduling/scheduler|Scheduler (application view)]],
[[scheduling/dependency-graph|Dependency Graph]],
[[scheduling/promote|promote]], [[scheduling/generalize|generalize]],
[[rule-system/iterative-loop|Iterative Loop]],
[[distributed-execution/halo-exchange|Halo Exchange]]
