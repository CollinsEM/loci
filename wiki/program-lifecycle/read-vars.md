---
title: read_vars
category: Program Lifecycle
status: complete
attribution: llm
reviewed: false
---

# read_vars

**`read_vars(varsFile, rdb)`** is a method of [[program-lifecycle/fact-db|fact_db]]
that parses a `.vars` file and populates the fact database with the parameter values it
contains. The `.vars` file is a brace-delimited list of variable assignments provided
by the end user to configure the simulation without modifying or recompiling source
code.

## Example `.vars` File

```
{
  N: 50
  nu: 1.0
  stop_iter: 100
  boundary_conditions: <
    BC_1=adiabatic,
    BC_2=specified(Twall=300K)
  >
}
```

## Processing Sequence

1. `read_vars` consults the `rule_db` to identify all variables declared by
   [[rule-system/default-rule|default]] and [[rule-system/optional-rule|optional]] rules,
   establishing the set of known variable names and their types.
2. Variables declared by `default` rules are initialised to their default values and
   registered in the fact database.
3. For each variable assignment in the `.vars` file, if the variable name matches a
   known declared variable, its value is set (overriding any default) and it is
   registered in the fact database.
4. Variables declared by `optional` rules that are not present in the `.vars` file
   remain absent from the fact database, causing all transitively dependent rules to be
   pruned from the schedule.

## Ordering Constraint

`read_vars` must be called after the `rule_db` is fully populated (all `add_rules` and
`load_module` calls complete) and before `Loci::makeQuery` is called.

---

*See also:* [[program-lifecycle/vars-file|.vars File Format]],
[[program-lifecycle/fact-db|fact_db]],
[[rule-system/default-rule|Default Rule]], [[rule-system/optional-rule|Optional Rule]]
