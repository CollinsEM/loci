---
title: Collapse Rule
category: Rule System
status: normative
---

# Collapse Rule

A **collapse rule** extracts the final value from a completed
[[rule-system/iterative-loop|iterative loop]], producing an output variable without a
time-level annotation (a stationary output) from an iterated input. A collapse rule is
identified by the presence of a [[rule-system/conditional|conditional]] clause that
gates its execution.

The collapse rule fires — and the iteration terminates — when the conditional evaluates
to true. Until then, the collapse rule does not fire and the loop continues to advance.

## Example

```cpp
$rule pointwise(solution <- Q{n}),
      conditional(finishTimestep{n}),
      constraint(geom_cells) {
  $solution = $Q{n} ;
}
```

## Role in the Iterative Loop

The collapse rule is the exit gate of the
[[rule-system/iterative-loop|iterative loop]]. The
[[scheduling/scheduler|scheduler]] recognises the
[[rule-system/build-rule|build]] / [[rule-system/advance-rule|advance]] / collapse
pattern and constructs the loop structure accordingly.

---

*See also:* [[rule-system/build-rule|Build Rule]],
[[rule-system/advance-rule|Advance Rule]],
[[rule-system/conditional|Conditional]],
[[rule-system/iterative-loop|Iterative Loop]]
