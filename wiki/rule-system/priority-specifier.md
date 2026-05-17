---
title: Priority Specifier
category: Rule System
status: normative
---

# Priority Specifier

A **priority specifier** is a `::`-prefixed namespace qualifier attached to the output
variable name in a rule head, used to declare that the rule is a *specialisation* of a
more general rule that produces the same variable. It is the mechanism by which the
programmer resolves ambiguity when two or more rules would otherwise produce the same
output variable over overlapping entity domains.

## When to Use

The priority specifier is used when it would be advantageous to override the default
behaviour of an output variable, or when specific physical or geometric conditions
require a different rule implementation. For example, a general interior rule may
compute a face flux for all faces, while a specialised rule computes it differently at
adiabatic wall boundaries.

## Disambiguation Rules

- Two or more rules may produce the same output variable provided their effective entity
  domains are **disjoint** — no priority annotation is needed.
- When two rules would produce the same variable over **overlapping** domains, at least
  one must carry a priority qualifier.
- A rule with k `::` qualifiers overrides any rule with fewer than k qualifiers for the
  same base variable over the overlapping domain.
- Two rules with the **same number** of `::` qualifiers over overlapping domains
  constitute an irresolvable conflict; the scheduler reports an error.
- Priority qualifiers form a strict hierarchy: `new::adiabatic::qdot` overrides
  `adiabatic::qdot`.

## Example

```cpp
// General rule — applies to all faces
$rule pointwise(qdot <- conductivity, grads_f(temperature), area) {
  $qdot = $area.sada * $conductivity *
           dot($grads_f(temperature), $area.n) ;
}

// Specialised rule — overrides general rule at adiabatic boundaries
$rule pointwise(adiabatic::qdot), constraint(adiabatic_BC) {
  $qdot = 0 ;
}
```

---

*See also:* [[rule-system/rule|Rule]], [[core-data-model/constraint|constraint]],
[[scheduling/scheduler|Scheduler]]
