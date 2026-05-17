---
title: Data-Driven Computation Principle
category: Foundational Principles
status: normative
audience: both
---

# Data-Driven Computation Principle

Computation in Loci is driven entirely by **data availability**. A rule becomes
eligible to execute when — and only when — all of its declared input relations
exist in the [[program-lifecycle/fact-db|fact database]] over the required entity
domains.

The programmer does not write explicit control flow, loops, or synchronisation
barriers. These are derived automatically from the dependency structure of the
rule set by the [[scheduling/scheduler|scheduler]].

## Implications

- A rule with unsatisfied inputs is simply not scheduled. This is not an error;
  it is how [[rule-system/optional-rule|optional rules]] and pruning work.
- A rule is not eligible until *all* inputs are present — partial satisfaction
  does not trigger partial execution.
- The scheduler determines the execution order; the programmer declares what is
  needed, not when to compute it.

---

*See also:* [[scheduling/scheduler|Scheduler]],
[[scheduling/dependency-graph|Dependency Graph]],
[[rule-system/optional-rule|Optional Rule]]
