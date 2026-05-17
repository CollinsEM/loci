---
title: Pointwise Rule
category: Rule System
status: normative
---

# Pointwise Rule

A **pointwise rule** computes an output value independently for each entity in its
execution domain. The kernel for entity `e` may access input values at `e` or at
entities reachable from `e` via [[core-data-model/map|Map]] chains, but does not
depend on values at other domain entities. Pointwise rules are trivially data-parallel.

## Example

```cpp
$rule pointwise(pressure <- rho, temperature, Rgas) {
  $pressure = $rho * $Rgas * $temperature ;
}
```

Here `Rgas` is a [[core-data-model/param|param]] — accessed as `$Rgas` in the compute
block like any other rule input.

## Characteristics

- Kernel executes once per entity in the execution domain.
- No ordering constraints between entities — the runtime may execute them in any order
  or in parallel.
- May read from adjacent entities via map chains (`$cl->$pressure`).
- May write to adjacent entities via map chains (unusual; typically done with apply rules).

---

*See also:* [[rule-system/singleton-rule|Singleton Rule]],
[[rule-system/apply-rule|Apply Rule]], [[rule-system/rule|Rule]]
