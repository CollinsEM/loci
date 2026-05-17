---
title: Scheduler
category: Scheduling and Execution Model
status: complete
audience: both
attribution: llm
reviewed: false
---

# Scheduler

The **scheduler** is the runtime component responsible for constructing and executing
the compute graph. Per the [[principles/static-schedule|Static Schedule Principle]],
schedule construction occurs each time [[program-lifecycle/make-query|Loci::makeQuery]]
is invoked.

## Schedule Construction Steps

1. **Initialisation.** [[rule-system/default-rule|Default]] and
   [[rule-system/optional-rule|optional]] rules are processed; the `.vars` file is
   parsed. The [[program-lifecycle/fact-db|fact database]] is populated with existential
   facts. Optional variables not provided are left absent.

2. **Graph deduction.** Beginning from the [[program-lifecycle/make-query|query]], the
   scheduler performs a backward traversal of the rule database. Rules whose body
   Relations cannot be satisfied are pruned. This pruning propagates transitively: all
   rules depending on pruned outputs are also pruned.

3. **Domain refinement.** For each rule in the candidate schedule, the scheduler
   refines its execution domain by propagating [[core-data-model/map|Map]]-chain
   reachability. A rule is executable for entity `e` only if every input value required
   is reachable from `e` via the declared map chains. If the resulting domain violates a
   declared [[core-data-model/constraint|constraint]] precondition, the scheduler exits
   with a diagnostic.

4. **Loop structure recognition.** The scheduler identifies [[rule-system/build-rule|build]],
   [[rule-system/advance-rule|advance]], and [[rule-system/collapse-rule|collapse]] rules
   and constructs the corresponding [[rule-system/iterative-loop|iterative loop]]
   structures. [[scheduling/promote|Promote]] and [[scheduling/generalize|generalize]]
   operations are inserted transparently as needed.

5. **Schedule generation.** A valid topological ordering of the rule set is produced.
   Explicit [[core-data-model/param|param]] synchronisation steps are inserted at
   appropriate points. [[rule-system/output|OUTPUT]] rules are placed wherever their
   inputs are satisfied.

6. **Distribution and execution.** The schedule is distributed over available computing
   resources and executed. No further schedule modification occurs during execution.

---

*See also:* [[scheduling/dependency-graph|Dependency Graph]],
[[program-lifecycle/make-query|Loci::makeQuery]],
[[principles/static-schedule|Static Schedule Principle]]
