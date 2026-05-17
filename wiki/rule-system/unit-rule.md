---
title: Unit Rule
category: Rule System
status: normative
---

# Unit Rule

A **unit rule** executes *once per process* before any [[rule-system/apply-rule|apply rule]]
contributes to the same output variable. Its sole purpose is to initialise the output
accumulator to the **identity value** of the chosen reduction operation — for example,
`0` for summation or `1` for multiplication.

A unit rule and one or more apply rules together form a complete *reduction pattern*.

The scheduler guarantees that all unit rule executions complete before any apply rule
for the same variable begins.

## Syntax

```cpp
$rule unit(outputVar), constraint(UNIVERSE) {
  $outputVar = <identity_value> ;
}
```

## Example

```cpp
$rule unit(dt), constraint(UNIVERSE) {
  $dt = std::numeric_limits<float>::max() ;
}
```

`std::numeric_limits<float>::max()` is the identity value for the `Loci::Minimum`
reduction: any real value accumulated via `min` can only decrease from this starting
point.

## Relationship to apply Rule

The unit rule and apply rule are always paired. The unit rule establishes the
accumulator; the apply rule contributes to it. The reduction is not valid without both.

```
unit rule  →  initialises accumulator to identity
apply rule →  contributes to accumulator (once per entity)
runtime    →  combines partial results across processes
```

---

*See also:* [[rule-system/apply-rule|Apply Rule]], [[rule-system/rule|Rule]]
