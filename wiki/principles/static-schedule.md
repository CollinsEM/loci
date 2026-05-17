---
title: Static Schedule Principle
category: Foundational Principles
status: normative
audience: both
---

# Static Schedule Principle

The execution schedule of a Loci program is constructed **statically** whenever
[[program-lifecycle/make-query|Loci::makeQuery]] is invoked, from:

- the existential facts in the [[program-lifecycle/fact-db|fact database]],
- the set of rules in the [[program-lifecycle/rule-db|rule database]], and
- the programmer-specified query variable.

Once generated, the schedule does not change during execution. All data
dependencies are resolved before any rule kernel fires.

## Implications

- The application developer never writes explicit loops, barriers, or
  communication calls. These are derived from the dependency structure of
  the rule set.
- Schedule construction may be invoked multiple times in the same program
  (e.g., for adaptive mesh refinement). Each call to `makeQuery` produces a
  new static schedule from the current state of the fact and rule databases.
- Structural changes to the problem domain (e.g., adaptive mesh refinement)
  require halting the current schedule, modifying the fact database, and
  calling `makeQuery` again.

## Relationship to Other Principles

The Static Schedule Principle is what makes [[principles/parallelism-transparency|Parallelism Transparency]]
possible: because all dependencies are known before execution, the runtime
can partition and distribute work without application developer involvement.

---

*See also:* [[scheduling/scheduler|Scheduler]], [[program-lifecycle/make-query|Loci::makeQuery]]
