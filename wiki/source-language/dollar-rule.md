---
title: $rule syntax
category: Loci Source Language
status: complete
attribution: llm
reviewed: false
---

# $rule Syntax

The **`$rule`** directive is the primary source-language construct by which an
application developer declares a [[rule-system/rule|Rule]]. It specifies the rule's
type, signature (inputs, outputs, constraints, conditionals), and kernel body.

## General Syntax

```cpp
$rule ruleType( outputVar <- inputVar1, inputVar2, ... ),
      constraint( constraintVar ),
      conditional( condVar ),
      option( optionName ) {
  // kernel body: C++ code with $ prefix on Loci variables
}
```

## Rule Type Keywords

Appearing immediately after `$rule`:
`pointwise`, `singleton`, `unit`, `apply`, `default`, `optional`

## Variable Access in the Kernel Body

Loci variables are accessed by prefixing their name with `$`. The access semantics
depend on container type and block context:

| Context | Syntax | Notes |
|---------|--------|-------|
| `store` in compute block | `$storeName` | Value for current entity |
| `param` in **compute** block | `$paramName` | Same as any other input |
| `param` in **prelude** block | `*$paramName` | Dereference required |
| Map chain | `$mapName->$relationName` | Navigate to adjacent entity |
| Iteration index | `$$n` | Current iteration counter (compute) |

Multiple maps may be chained: `$cl->$face2node->$pos`. Valid for both inputs and
outputs.

## Behavioural Guarantee

A conforming runtime must register each `$rule` with the rule database before schedule
construction begins. All metadata declared in the rule signature (inputs, outputs,
constraints, conditionals, operator) must be faithfully communicated to the scheduler.

---

*See also:* [[rule-system/rule|Rule]], [[source-language/dollar-type|$type declaration]],
[[rule-system/prelude-block|Prelude Block]]
