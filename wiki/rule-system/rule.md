---
title: Rule
category: Rule System
status: complete
attribution: llm
reviewed: false
---

# Rule

A **Rule** is the fundamental unit of computation in Loci — a declarative specification
consisting of three parts:

1. A **head** — the Relation produced (output) and the constraints restricting its
   execution domain.
2. A **body** — the Relations consumed (data dependencies).
3. A **kernel** — the local computational procedure, written in C++, that transforms
   input values to the output value.

Rules are referentially transparent with respect to the
[[program-lifecycle/fact-db|fact database]]: the output is determined entirely by the
declared inputs. This property enables automatic dependency-graph construction and safe
parallel execution.

Rules are written using the [[source-language/dollar-rule|$rule]] source syntax. The
Loci preprocessor expands this into C++ class definitions and rule registration calls
transparently.

## Formal Definition

$\mathcal{R} = (\text{head}, \text{body}, \text{kernel})$

where $\text{head} = (R_\text{out}, C_1, \ldots, C_k)$,
$\text{body} = \{R_1, \ldots, R_n\}$, and the kernel maps input values to the output
value. The effective execution domain is $C_1 \cap \cdots \cap C_k$, further refined
by map-reachability.

## Rule Types

| Type | Purpose |
|------|---------|
| [[rule-system/pointwise-rule|pointwise]] | Independent per-entity computation |
| [[rule-system/singleton-rule|singleton]] | Compute a `param` from other `param` values |
| [[rule-system/unit-rule|unit]] | Initialise a reduction accumulator |
| [[rule-system/apply-rule|apply]] | Transform-reduce over an entity domain |
| [[rule-system/default-rule|default]] | Assign a `param` its default value at startup |
| [[rule-system/optional-rule|optional]] | Declare an optional `param` variable |
| [[rule-system/build-rule|build]] | Set initial value for an iterative loop variable |
| [[rule-system/advance-rule|advance]] | Advance an iterative loop variable by one step |
| [[rule-system/collapse-rule|collapse]] | Extract the final value from a completed loop |
| [[rule-system/parametric-rule|parametric]] | Generic rule instantiated by substitution |

---

*See also:* [[source-language/dollar-rule|$rule syntax]],
[[scheduling/dependency-graph|Dependency Graph]]
