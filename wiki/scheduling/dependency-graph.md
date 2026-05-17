---
title: Dependency Graph
category: Scheduling and Execution Model
status: complete
audience: both
attribution: llm
reviewed: false
---

# Dependency Graph

The **dependency graph** is a directed acyclic graph (DAG) constructed by the
[[scheduling/scheduler|scheduler]] from the declared inputs and outputs of all
[[rule-system/rule|Rules]]. An edge from Rule $\mathcal{R}_A$ to Rule $\mathcal{R}_B$
indicates that $\mathcal{R}_B$ produces a Relation consumed by $\mathcal{R}_A$, so
$\mathcal{R}_B$ must execute before $\mathcal{R}_A$.

## Handling Iterative Loops

The [[rule-system/build-rule|build]] / [[rule-system/advance-rule|advance]] /
[[rule-system/collapse-rule|collapse]] pattern introduces a controlled recurrence that
would appear as a cycle in a naive graph. The scheduler handles this by recognising the
pattern and representing the iteration as a structured loop construct in the schedule
rather than as an unresolvable circular dependency.

A free cycle not conforming to this pattern constitutes an error.

---

*See also:* [[scheduling/scheduler|Scheduler]],
[[rule-system/iterative-loop|Iterative Loop]]
