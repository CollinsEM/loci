---
title: Singleton Rule
category: Rule System
status: normative
---

# Singleton Rule

A **singleton rule** computes a [[core-data-model/param|param]] value from other param
values. The kernel executes once and produces a single value deposited in the
[[program-lifecycle/fact-db|fact database]] as a param. Because all input params are
fully synchronised before execution, all processes are guaranteed to produce identical
output.

## Example

```cpp
$rule singleton(Rgas <- cp, cv) {
  $Rgas = $cp - $cv ;
}
```

## Characteristics

- Executes exactly once per scheduling cycle (not once per entity).
- All inputs are `param` values — globally consistent across all processes.
- Output is a `param` value — automatically synchronised before any dependent rule fires.
- Commonly used for derived physical constants, global norms, and iteration control variables.

## Common Use: OUTPUT

Singleton rules are also used for `OUTPUT` — writing diagnostics or solution files each
iteration. See [[rule-system/output|OUTPUT]].

---

*See also:* [[core-data-model/param|param]], [[rule-system/pointwise-rule|Pointwise Rule]],
[[rule-system/rule|Rule]]
