---
title: rule_db
category: Program Lifecycle
status: complete
audience: both
attribution: llm
reviewed: false
---

# rule_db

The **`rule_db`** is the programmatic object that holds the complete set of rules
available to the [[scheduling/scheduler|scheduler]] for a given
[[program-lifecycle/make-query|makeQuery]] invocation. It is constructed in `main()`
by the application developer and populated via two mechanisms:

1. **`rdb.add_rules(global_rule_list)`** — transfers all statically-registered rules
   from [[program-lifecycle/global-rule-list|global_rule_list]] into the `rule_db`.
2. **`Loci::load_module("name", rdb)`** — loads a named shared library module and adds
   its rules to the `rule_db`.

The `rule_db` must be fully populated before `Loci::makeQuery` is called. `makeQuery`
uses the rule database as the complete universe of available rules for schedule
construction; no rules may be added after `makeQuery` is invoked for a given scheduling
cycle.

## Example

```cpp
rule_db rdb ;
rdb.add_rules(global_rule_list) ;  // static rules from linked objects
Loci::load_module("fvm", rdb) ;    // dynamic rules from shared library
```

---

*See also:* [[program-lifecycle/global-rule-list|global_rule_list]],
[[program-lifecycle/load-module|Loci::load_module]],
[[program-lifecycle/make-query|Loci::makeQuery]]
