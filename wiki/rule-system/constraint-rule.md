---
title: Constraint Rule
category: Rule System
status: complete
attribution: llm
reviewed: false
---

# Constraint Rule

A **constraint rule** is a rule that *produces* one or more
[[core-data-model/constraint|constraint]] values at runtime rather than merely
consuming them as a filter. The computed constraints are added to the fact database
and can then be referenced by other rules as domain restrictions.

Constraint rules are the standard mechanism for choosing between mutually exclusive
physical models or numerical options based on a runtime parameter.

## Motivation

Most constraints are established statically in the fact database before `makeQuery`
is called (e.g., `geom_cells`, `boundary_faces`). A constraint rule covers the case
where the effective entity domain of a group of rules cannot be determined until a
[[core-data-model/param|param]] value is read — typically from the `.vars` file.

## Pattern

A constraint rule takes `param` inputs and outputs one or more `Constraint` values.
The body assigns either `~EMPTY` (all entities — the universe) or `EMPTY` (no
entities) to each output constraint, with exactly one constraint active at a time for
mutually exclusive choices:

```cpp
$rule singleton(V_limiter, B_limiter, N_limiter <- limiter) {
  if(*$limiter == "venkatakrishnan" || *$limiter == "V") {
    $V_limiter = ~EMPTY ;
    $B_limiter = EMPTY ;
    $N_limiter = EMPTY ;
  } else if(*$limiter == "barth" || *$limiter == "B") {
    $V_limiter = EMPTY ;
    $B_limiter = ~EMPTY ;
    $N_limiter = EMPTY ;
  } else {
    $V_limiter = ~EMPTY ;   // default
    $B_limiter = EMPTY ;
    $N_limiter = EMPTY ;
  }
}
```

where `limiter` is a `param<string>` set in the `.vars` file and the three
`Constraint` outputs are declared as:

```cpp
$type V_limiter Constraint ;
$type B_limiter Constraint ;
$type N_limiter Constraint ;
```

Rules that implement the venkatakrishnan limiter carry `constraint(V_limiter)`;
rules that implement the Barth limiter carry `constraint(B_limiter)`. The scheduler
automatically selects the active rule set based on which constraint is populated.

## Special Values

| Expression | Meaning |
|------------|---------|
| `~EMPTY` | The universe — all entities. Activates rules that constrain on this variable. |
| `EMPTY` | The empty set — no entities. Deactivates rules that constrain on this variable. |

## Relationship to `constraint` as a Filter

The `constraint(X)` clause in a `$rule` signature *reads* an existing constraint and
uses it to restrict the rule's execution domain. A constraint rule *writes* a
constraint into the fact database. These are complementary roles: constraint rules
produce the constraints that filter clauses consume.

---

*See also:* [[core-data-model/constraint|constraint]],
[[rule-system/singleton-rule|Singleton Rule]],
[[rule-system/optional-rule|Optional Rule]],
[[program-lifecycle/vars-file|.vars File Format]]
