---
title: Advance Rule
category: Rule System
status: complete
attribution: llm
reviewed: false
---

# Advance Rule

An **advance rule** progresses an iterated variable from iteration `n` to iteration
`n+1`. It is identified by having an output annotated `varName{n+1}` with inputs
including `varName{n}`.

## Example

```cpp
$rule pointwise(u{n+1} <- u{n}, dt{n}, R{n}) {
  $u{n+1} = $u{n} + $dt{n} * $R{n} ;
}
```

Note: `dt{n}` is a [[core-data-model/param|param]] accessed as `$dt{n}` in the compute
block — no dereference operator needed.

## Role in the Iterative Loop

The advance rule is the body of the [[rule-system/iterative-loop|iterative loop]]. It
fires every iteration until the [[rule-system/conditional|conditional]] variable
associated with the paired [[rule-system/collapse-rule|collapse rule]] evaluates to
true, at which point the collapse rule fires and the loop terminates.

---

*See also:* [[rule-system/build-rule|Build Rule]],
[[rule-system/collapse-rule|Collapse Rule]],
[[rule-system/iterative-loop|Iterative Loop]]
