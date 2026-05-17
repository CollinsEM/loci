---
title: Conditional
category: Rule System
status: normative
---

# Conditional

A **conditional** is a `param<bool>` variable used to gate the execution of a rule. A
rule annotated with `conditional(condVar{n})` will only execute when `condVar`
evaluates to `true` at that iteration. Conditionals may be applied to any rule type.

## Common Uses

- **[[rule-system/collapse-rule|Collapse rules]]** — gating termination of an iterative
  loop. The collapse rule fires only when the termination condition is met.
- **[[rule-system/output|OUTPUT rules]]** — gating periodic I/O, allowing plot files
  or diagnostic output to be written only every k iterations.

## Defining the Conditional Variable

The conditional variable is typically computed each iteration by a
[[rule-system/singleton-rule|singleton rule]] that evaluates the termination or trigger
criterion:

```cpp
$rule singleton(finishTimestep <- $$n, stop_iter) {
  $finishTimestep = ($$n > $stop_iter) ;
}
```

Note: `$$n` (the iteration counter) and `$stop_iter` (a param) are both accessed
without `*` in the compute block.

---

*See also:* [[rule-system/collapse-rule|Collapse Rule]], [[rule-system/output|OUTPUT]],
[[rule-system/iterative-loop|Iterative Loop]], [[rule-system/singleton-rule|Singleton Rule]]
