---
title: Default Rule
category: Rule System
status: complete
attribution: llm
reviewed: false
---

# Default Rule

A **default rule** is an initialisation-phase rule that allocates a named
[[core-data-model/param|param]] variable, assigns it a prescribed default value, and
registers it in the [[program-lifecycle/fact-db|fact database]] at startup — before
schedule construction begins. The default value may subsequently be overridden by a
value specified in the `.vars` file.

## Example

```cpp
$type nu param<float> ;
$rule default(nu) {
  $nu = 1.0 ;
}
```

## Characteristics

- Executes during the `read_vars` phase, before `makeQuery` is called.
- The default value is applied first; any matching entry in the `.vars` file then
  overrides it.
- Declaring a `default` rule makes the variable *always present* in the fact database
  (unlike [[rule-system/optional-rule|optional rules]]). Dependent rules are never pruned
  due to this variable being absent.

---

*See also:* [[rule-system/optional-rule|Optional Rule]], [[core-data-model/param|param]],
[[program-lifecycle/read-vars|read_vars]]
