---
title: global_rule_list
category: Program Lifecycle
status: complete
audience: both
attribution: llm
reviewed: false
---

# global_rule_list

**`global_rule_list`** is a globally-scoped rule registry that is populated
automatically before `main()` executes. Every `$rule` declaration in every translation
unit linked into the executable registers itself into `global_rule_list` as a side
effect of static initialisation. By the time `main()` is reached, `global_rule_list`
contains the complete set of statically-linked rules available to the application.

The specific mechanism of registration is an implementation detail of the Loci
preprocessor and runtime. The behavioural guarantee is that all `$rule` declarations
in linked translation units are available via `global_rule_list` before any application
code in `main()` executes.

## Usage

`global_rule_list` is passed to `rdb.add_rules()` to populate the
[[program-lifecycle/rule-db|rule_db]]:

```cpp
rule_db rdb ;
rdb.add_rules(global_rule_list) ;
```

---

*See also:* [[program-lifecycle/rule-db|rule_db]], [[source-language/dollar-rule|$rule]]
