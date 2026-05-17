---
title: Optional Rule
category: Rule System
status: normative
---

# Optional Rule

An **optional rule** declares a named [[core-data-model/param|param]] variable and
reserves a placeholder for it in the rule database *without* assigning a value or
registering it in the [[program-lifecycle/fact-db|fact database]]. If the variable is
subsequently provided by the `.vars` file (or by other means), it is registered and
becomes available to dependent rules. If it is not provided, it remains absent.

## Transitive Pruning

The consequence of absence is significant: the [[scheduling/scheduler|scheduler]] will
**transitively prune** all rules whose dependency chains require the absent variable.
This enables a single rule database to support multiple physical models.

For example, omitting an optional viscosity parameter `nu` automatically prunes all
viscous flux rules, producing an inviscid (Euler) solver from the same rule set that
would otherwise produce a viscous (Navier-Stokes) solver.

## Contrast with `default`

| | `default` rule | `optional` rule |
|-|---------------|----------------|
| Always in fact database? | Yes | Only if provided in `.vars` |
| Dependent rules pruned if absent? | Never | Yes, transitively |
| Overridable by `.vars` file? | Yes | Yes (it *must* be provided) |

---

*See also:* [[rule-system/default-rule|Default Rule]], [[core-data-model/param|param]],
[[scheduling/scheduler|Scheduler]]
